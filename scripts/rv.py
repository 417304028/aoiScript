import csv
import glob
import time
import openpyxl
from openpyxl.styles import Font
from openpyxl.drawing.image import Image
from dateutil import parser
import pyperclip
import utils
import config
import re
import os
import datetime
import pyautogui
import pandas as pd
from pywinauto import Application,Desktop
from loguru import logger


# 前置程序（假定程序已打开）
def front_rv_window():
    try:
        utils.click_by_png(config.RV_TOPIC_DARK)
        find_topic = True
    except Exception:
        find_topic = False
    if not find_topic:
        logger.info("未搜索到标题，改为搜索窗格")
        windows = Desktop(backend="win32").windows()
        window_found = False
        logger.info("开始寻找程序窗口")
        pattern = re.compile(r".*Sinictek-训练.*")  # 正则表达式匹配包含 "Sinictek-训练" 的标题
        sinictek_amount = 0
        for w in windows:
            if pattern.match(w.window_text()):
                window_properties = w.get_properties()
                logger.info(f"'Sinictek-训练'窗口存在,详细信息：{window_properties}")
                window_found = True
                sinictek_amount += 1
        logger.info(f"'Sinictek-训练'窗口数量: {sinictek_amount}")
        if window_found:
            app = Application().connect(title_re=".*Sinictek-训练.*")
            main_window = app.window(title_re="Sinictek-训练")
            if main_window.exists(timeout=10):
                logger.info("成功连接到窗口")
                main_window.wait('ready', timeout=10)
                main_window.set_focus()
                # main_window.bring_to_front()
                # main_window.maximize()
                main_window.wait('ready', timeout=10)
            else:
                logger.error("未找到窗口")
                raise Exception("未找到窗口")
        else:
            logger.error("未找到程序")
            raise Exception("未找到程序")

# ai复判 总路径(包含train,test文件夹),结果路径（含定位图片及输出数据文档）
def rv_ai_test(train_eval_path, result_path):
    status = 1
    front_rv_window()
    train_paths = set()
    # 搜索train_eval_path下所有名字含train的文件夹(可能为自身) ,装入train_paths
    for root, dirs, files in os.walk(train_eval_path):
        for d in dirs:
            if 'train' in d:
                train_folder = os.path.join(root, d)
                if os.path.isdir(train_folder):
                    train_paths.add(train_folder)
    logger.info(f"train_paths: {train_paths}")
    # 查询pyd目录(后面生成脚本日志文件夹要用)
    # 从提供的路径向上遍历，直到找到包含pyd的目录,用pyd_path保存
    logger.info(f"查询pyd路径")
    pyd_path = result_path
    substring = 'pyd'
    root_path = os.path.abspath(os.sep)
    found = False  # 用于标记是否找到包含子字符串的目录

    while pyd_path != root_path:
        if substring in os.path.basename(pyd_path):
            found = True  # 找到了包含子字符串的目录
            logger.info(f"找到pyd路径: {pyd_path}")
            break
        pyd_path = os.path.dirname(pyd_path)

    if not found:  # 如果没有找到
        status = -1
        logger.error(f"在路径 {result_path} 中未找到包含 '{substring}' 的目录")
        raise Exception(f"在路径 {result_path} 中未找到包含 '{substring}' 的目录")

    logger.info(f"开始遍历{train_paths}")
    # 遍历train_paths集合中的每个元素
    for train_path in train_paths:
        pyperclip.copy(train_path)
        # 点击训练按钮
        utils.click_by_png(config.RV_SIMULATE_TO_TRAIN)
        refresh_count = 0
        while refresh_count < 7:
            time.sleep(1)
            pyautogui.press('enter')
            utils.click_by_png(config.RV_JOB_NAME, timeout=60, if_click_right=1)
            time.sleep(1)
            pyautogui.press('down',2)
            pyautogui.press('enter')
            logger.info(f"训练刷新第{refresh_count}次")
            time.sleep(1)
            # 查看训练状态
            utils.click_by_png(config.RV_TRAIN_STATUS)
            time.sleep(1)
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(1)
            pyautogui.hotkey('ctrl', 'c')
            train_result = pyperclip.paste()
            logger.info(train_result)
            if '训练完成' in train_result:
                train_result = '训练完成'
                break
            elif '训练失败' in train_result:
                train_result = '训练失败'
                break
            elif '待训练' in train_result:
                refresh_count += 1
                time.sleep(10)  # 每隔十秒刷新一次
                if refresh_count == 6:
                    train_result = '待训练'
                    break
            else:
                status = -1
                logger.error("训练状态未知")
        # 检测pyd_path下是否有train_logs的文件夹,没有的话创建该文件夹,在文件夹内创建 年-月-日.csv(若不存在的话) 
        train_logs_path = os.path.join(pyd_path, 'train_logs')
        os.makedirs(train_logs_path, exist_ok=True)
        today_date = datetime.datetime.now().strftime("%Y-%m-%d")
        csv_file_path = os.path.join(train_logs_path, f"{today_date}.csv")
        # 处理train.csv
        if not os.path.exists(csv_file_path):
            with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['train路径', 'train状态'])
        with open(csv_file_path, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([train_path, train_result])
        # 保存并关闭该csv
        file.close()
        logger.info("训练完毕，开始推理")
        
        # 查询train_path同级文件夹下名字包含test的文件夹 装入eval_path
        eval_paths = glob.glob(os.path.join(os.path.dirname(train_path), '*test*'))
        if not eval_paths:  # 检查列表是否为空
            logger.error("未找到推理的路径")
            raise Exception("未找到推理的路径")
        else:
            eval_path = eval_paths[0]  # 选择找到的第一个路径
            logger.info(f"找到推理路径: {eval_path}")
        # 处理模拟至推理过程 
        with open("temp_eval_path.txt", "w", encoding='utf-8') as temp_file:
            temp_file.write(eval_path)
        # 从记事本读取eval_path到剪切板
        with open("temp_eval_path.txt", "r", encoding='utf-8') as temp_file:
            eval_path_from_txt = temp_file.read()
            pyperclip.copy('')  
            time.sleep(0.5)
            pyperclip.copy(eval_path)
            pyperclip.copy(eval_path_from_txt) 
        clipboard_content = pyperclip.paste()
        logger.info(f"剪切板内容: {clipboard_content}")
        time.sleep(0.5)
        utils.click_by_png(config.RV_SIMULATE_TO_EVAL)
        time.sleep(2)
        os.remove("temp_eval_path.txt")
        pyautogui.press('enter')

        # 刷新任务状态并提取结果
        retry_count = 0
        utils.click_by_png(config.RV_JOB_NAME, timeout=6, if_click_right=1)
        time.sleep(1)
        pyautogui.press('down',2)
        pyautogui.press('enter')
        # 点击重新推理
        utils.click_by_png(config.RV_TRAIN_STATUS, if_click_right=1)
        if not utils.search_symbol(config.RV_CLICK_RESTART_EVAL, 5):
            time.sleep(5)
        utils.click_by_png(config.RV_CLICK_RESTART_EVAL)
        click_time = datetime.datetime.now()
        logger.info(f"点击重新推理时间: {click_time.strftime('%Y-%m-%d %H:%M:%S')}")
        # 获取eval_result
        while retry_count < 6:
            logger.info(f"推理刷新第{retry_count}次")
            time.sleep(5)
            utils.click_by_png(config.RV_MISSION_MANAGE, tolerance=0.7)
            time.sleep(1)
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(1.5)
            pyautogui.hotkey('ctrl', 'c')
            logger.info("开始解析推理状态")
            clipboard_content = pyperclip.paste()
            task_lines = clipboard_content.split('\n')
            latest_time = None
            latest_record = None
            # 解析任务状态
            for line in task_lines[1:]:  # 忽略第一行标题
                parts = line.split('\t')
                if len(parts) >= 6:
                    task_id, task_type, task_status, result, add_time, next_time = parts
                    # 将添加时间字符串转换为datetime对象
                    try:
                        add_time_dt = datetime.datetime.strptime(add_time.strip(), '%Y/%m/%d %H:%M:%S')
                    except ValueError as e:
                        logger.warning(f"日期解析失败：{add_time}，错误：{e}")
                    # 检查添加时间是否在click_time的前后2分钟内
                    if click_time - datetime.timedelta(minutes=2) <= add_time_dt <= click_time + datetime.timedelta(minutes=2):
                        # 检查是否是最近的时间
                        if latest_time is None or add_time_dt > latest_time:
                            latest_time = add_time_dt
                            latest_record = (task_type, task_status, result)
                            logger.info(f"task_type = {task_type},task_status = {task_status},task_result = {result}")
            if latest_record:
                logger.info(f"第{retry_count}次推理,记录为：{latest_record}")
                logger.info(f"找到最新记录：任务类型={task_type}，任务状态={task_status}，结果={result}，添加时间={add_time}")
            else:
                logger.error("没有找到符合条件的记录")
            # 取两分钟内的记录，如果在队列中的话，则记录其task_id，3分钟后如果还是显示队列中则
            if latest_record and '推理' in latest_record[0] and '成功' in latest_record[2]:
                eval_result = '推理成功'
                utils.click_by_png(config.RV_CLOSE_MISSION_MANAGE, 5)
                break
            elif latest_record and '推理' in latest_record[0] and '失败' in latest_record[2]:
                eval_result = '推理失败'
                utils.click_by_png(config.RV_CLOSE_MISSION_MANAGE, 5)
                break
            elif "队列" in latest_record[1]:
                retry_count += 0.5
                logger.debug(f"推理处于队列中")
                utils.click_by_png(config.RV_CLOSE_MISSION_MANAGE, 5)
            else:
                utils.click_by_png(config.RV_CLOSE_MISSION_MANAGE, 5)
                time.sleep(10)  # 等待10秒后再次尝试
                retry_count += 1
        if retry_count == 6:
            eval_result = '推理失败'
        time.sleep(1)
        eval_results = []
        eval_results.append((eval_path, eval_result))
        
        # 删除job
        utils.click_by_png(config.RV_JOB_NAME, if_click_right=1)
        pyautogui.press('down')
        pyautogui.press('enter')

    logger.info("开始处理数据...")
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    log_path = os.path.join(pyd_path, "logs", "res_static", f"{today_date}.csv")
    logger.info(f"log_path: {log_path}")
    if not os.path.exists(log_path):
        logger.error("未找到log文件")
        raise Exception("未找到log文件")
    # 新增日志文件
    new_log_path = os.path.join(pyd_path, "eval_logs")
    os.makedirs(new_log_path, exist_ok=True)
    new_xlsx_path = os.path.join(new_log_path, f"{today_date}.xlsx")
    logger.info(f"new_xlsx_path: {new_xlsx_path}")

    if not os.path.exists(new_xlsx_path):
        # 读取CSV文件
        df_csv = pd.read_csv(log_path)
        # 添加新列
        df_csv = df_csv.assign(eval路径=None, 定位的图片路径=None, eval图片名称=None, eval结果=None, eval图片=None)
        # 重新排序列，将新列放在前面
        columns_order = ['eval路径', '定位的图片路径', 'eval图片名称', 'eval结果', 'eval图片'] + [col for col in df_csv.columns if col not in ['eval路径', '定位的图片路径', 'eval图片名称', 'eval结果', 'eval图片']]
        df_csv = df_csv[columns_order]
        # 保存为XLSX
        df_csv.to_excel(new_xlsx_path, index=False, engine='openpyxl')
        logger.info("对xlsx作预处理")
        # 打开xlsx
        df_xlsx = pd.read_excel(new_xlsx_path, engine='openpyxl')
        # 去除列名中的空白符
        df_xlsx.columns = [col.strip() for col in df_xlsx.columns]
        # 使用openpyxl直接加载工作簿以修改列名样式
        wb = openpyxl.load_workbook(new_xlsx_path)
        ws = wb.active
        # 取消列名加粗
        for cell in ws[1]:  # 第一行是列名
            cell.font = Font(bold=False)
        # 保存修改后的工作簿
        wb.save(new_xlsx_path)
        # 重新加载DataFrame以确保列名更改生效
        df_xlsx = pd.read_excel(new_xlsx_path, engine='openpyxl')
        # 去除列名中的空白符和其他特殊字符
        df_xlsx.columns = [re.sub(r'\s+', '', col) for col in df_xlsx.columns]
        logger.info("对xlsx作预处理完成")
        
    else:
        # 直接处理文档
        df_xlsx = pd.read_excel(new_xlsx_path, engine='openpyxl')
    
    # 确保工作簿和工作表被正确初始化
    wb = openpyxl.load_workbook(new_xlsx_path)
    ws = wb.active  # 确保这是正确的工作表
    # 确保id列为字符串类型并去除空格
    df_xlsx['id'] = df_xlsx['id'].astype(str).str.strip()

    logger.info("开始处理图片和更新数据...")
    logger.warning(f"eval_results: {eval_results}")
    for eval_path, eval_result in eval_results:

        eval_image_paths = glob.glob(os.path.join(eval_path, '**/*.bmp'), recursive=True)
        for eval_image_path in eval_image_paths:
            eval_image_name = os.path.splitext(os.path.basename(eval_image_path))[0]
            # 查找匹配的行
            df_rows = df_xlsx[df_xlsx['id'] == eval_image_name.strip()]
            if df_rows.empty:
                logger.error(f"未找到与图片名称 {eval_image_name} 完全匹配的id")
            else:
                for index, row in df_rows.iterrows():
                    excel_row = index + 2  # 假设数据从第二行开始
                    logger.info(f"更新数据：{eval_path}, {eval_image_path}, {eval_image_name}, {eval_result}")
                    ws.cell(row=excel_row, column=1).value = eval_path
                    ws.cell(row=excel_row, column=2).value = eval_image_path
                    ws.cell(row=excel_row, column=3).value = eval_image_name
                    ws.cell(row=excel_row, column=4).value = eval_result

                    # 打印更新后的行以确认数据
                    updated_row_values = [cell.value for cell in ws[excel_row]]
                    logger.info(f"更新后的数据行: {updated_row_values}")

        df_xlsx.to_excel(new_xlsx_path, index=False, engine='openpyxl')
        wb.save(new_xlsx_path)
        # 插入图片
        logger.info("开始插入图片...")
        batch_size = 10  # 每批处理的图片数量
        batch_count = 0  # 当前批次中已处理的图片数量

        for eval_image_path in eval_image_paths:
            eval_image_name = os.path.splitext(os.path.basename(eval_image_path))[0]
            df_rows = df_xlsx[df_xlsx['id'] == eval_image_name.strip()]
            if not df_rows.empty:
                for index, row in df_rows.iterrows():
                    try:
                        logger.info(f"正在更新行: {index}")
                        img = Image(eval_image_path)
                        cell = ws['E' + str(index + 2)]
                        
                        # 调整图片大小的比例（根据需要调整）
                        img.width, img.height = img.width / 7, img.height / 7
                        # 调整行高
                        ws.row_dimensions[index + 2].height = img.height * 0.75
                        # 调整列宽
                        ws.column_dimensions['E'].width = img.width * 0.14
                        # 设置图片的锚点
                        img.anchor = cell.coordinate
                        # 将图片添加到工作表
                        ws.add_image(img)

                        logger.info(f"成功为 {eval_image_name} 添加图片")
                    except Exception as e:
                        logger.error(f"处理图片 {eval_image_name} 时出错: {e}")

                    batch_count += 1
                    if batch_count >= batch_size:
                        # 达到批次大小，保存工作簿
                        logger.info("达到批次大小，正在保存工作簿...")
                        wb.save(new_xlsx_path)
                        batch_count = 0  # 重置批次计数器

        # 处理完所有图片后再次保存工作簿
        logger.info("所有图片处理完毕，正在保存工作簿...")
        wb.save(new_xlsx_path)

        # 重新加载工作簿以验证数据
        logger.info("重新加载工作簿以验证数据...")
        verify_wb = openpyxl.load_workbook(new_xlsx_path)
        verify_ws = verify_wb.active
    for row in verify_ws.iter_rows(min_row=2, max_row=20, values_only=True):
        logger.info(f"验证行数据: {row}")

    status = 0
    logger.info(f"ai复判完成,status: {status}")
    return status






