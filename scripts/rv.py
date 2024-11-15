import csv
import glob
import time
import openpyxl
from openpyxl.styles import Font
import pyperclip
import utils
import config
import re
import os
import datetime
import chardet
import pyautogui
import pandas as pd
from pywinauto import Application, Desktop
from loguru import logger

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
        pattern = re.compile(r".*Sinictek-训练.*")
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

def sync_csv_to_xlsx(csv_path, xlsx_path):
    try:
        logger.info("将csv更新的数据同步至xlsx...")

        # 读取CSV和XLSX文件
        df_csv = pd.read_csv(csv_path)
        df_xlsx = pd.read_excel(xlsx_path, engine='openpyxl')

        # 确保id列为字符串类型并去除空格
        df_csv['id'] = df_csv['id'].astype(str).str.strip()
        df_xlsx['id'] = df_xlsx['id'].astype(str).str.strip()

        # 遍历CSV中的每一行，将数据同步到XLSX
        for index, row in df_csv.iterrows():
            csv_id = row['id']
            # 查找XLSX中对应的行
            xlsx_row = df_xlsx[df_xlsx['id'] == csv_id]
            if not xlsx_row.empty:
                # 检查CSV行是否已存在于XLSX中
                if (xlsx_row.iloc[0, 6:] == row).all():
                    logger.info(f"CSV中的行已存在于XLSX中，跳过同步: {row.to_dict()}")
                    continue
                # 更新XLSX中对应的列，假设df_csv的列数为N
                for col_index, col_name in enumerate(df_csv.columns):
                    # 在XLSX中对应的列索引为6 + col_index
                    df_xlsx.loc[xlsx_row.index, df_xlsx.columns[col_index + 6]] = row[col_name]
            else:
                # 如果XLSX中没有对应的行，则添加新行
                new_row = pd.Series([None] * 6 + list(row), index=df_xlsx.columns)
                df_xlsx = pd.concat([df_xlsx, new_row.to_frame().T], ignore_index=True)

        # 保存更新后的XLSX文件
        with pd.ExcelWriter(xlsx_path, engine='openpyxl') as writer:
            df_xlsx.to_excel(writer, index=False)

        logger.info("csv更新的数据同步至xlsx同步完成")
    except Exception as e:
        logger.error(f"处理Excel文件时发生错误: {e}")
        raise Exception(f"处理Excel文件时发生错误: {e}")



# ai复判 总路径(包含train,test文件夹),结果路径（含定位图片及输出数据文档）
def rv_ai_test(train_eval_path, result_path, mode):
    status = 1
    # 从提供的路径向上遍历，直到找到包含pyd的目录,用pyd_path保存
    logger.info(f"查询pyd路径")
    pyd_path = result_path
    substring = 'py'
    root_path = os.path.abspath(os.sep)
    found = False  # 用于标记是否找到包含子字符串的目录

    while pyd_path != root_path:
        if substring in os.path.basename(pyd_path):
            found = True  # 找到了包含子字符串的目录
            logger.info(f"找到pyd路径: {pyd_path}")
            break
        pyd_path = os.path.dirname(pyd_path)

    if not found:
        status = -1
        logger.error(f"在路径 {result_path} 中未找到包含 '{substring}' 的目录")
        raise Exception(f"在路径 {result_path} 中未找到包含 '{substring}' 的目录")
    

    # 仅仅将csv处理为xlsx
    if not train_eval_path and result_path:

        logger.info("训练推理为空，结果路径非空，开始处理结果路径下的.csv文件")
        csv_files = glob.glob(os.path.join(result_path, '*.csv'))
        if not csv_files:
            logger.error("未找到任何.csv文件")
            raise Exception("未找到任何.csv文件")
        
        for csv_file in csv_files:
            logger.info(f"处理文件: {csv_file}")
            csv_file_name = os.path.splitext(os.path.basename(csv_file))[0]
            eval_xlsx_path = os.path.join(result_path, f"{csv_file_name}.xlsx")
            completed_txt_path = os.path.join(pyd_path, "脚本已运行完成.txt")
            if os.path.exists(completed_txt_path):
                os.remove(completed_txt_path)
            try:
                with open(csv_file, 'rb') as file:
                    content = file.read()
                    result = chardet.detect(content)
                    encoding = result['encoding'] if result['encoding'] else 'utf-8'
                    try:
                        content = content.decode(encoding)
                    except UnicodeDecodeError:
                        content = content.decode('gbk', errors='ignore')

                df_csv = pd.read_csv(csv_file, encoding=encoding)
                # 添加新列
                df_csv = df_csv.assign(eval结果=None, good_ng=None, eval图片=None, 定位图片=None, train图片=None, eval路径=None)
                # 重新排序列，将新列放在前面
                columns_order = ['eval结果', 'good_ng', 'eval图片', '定位图片', 'train图片', 'eval路径'] + [col for col in df_csv.columns if col not in ['eval结果', 'good_ng', 'eval图片', '定位图片', 'train图片', 'eval路径']]
                df_csv = df_csv[columns_order]
                df_csv.to_excel(eval_xlsx_path, index=False, engine='openpyxl')
                logger.info("对xlsx作预处理")
                df_xlsx = pd.read_excel(eval_xlsx_path, engine='openpyxl')
                df_xlsx.columns = [col.strip() for col in df_xlsx.columns]
                wb = openpyxl.load_workbook(eval_xlsx_path)
                ws = wb.active
                for cell in ws[1]:
                    cell.font = Font(bold=False)
                ws.column_dimensions['C'].width = 18
                ws.column_dimensions['D'].width = 18
                ws.column_dimensions['E'].width = 18
                wb.save(eval_xlsx_path)
                df_xlsx = pd.read_excel(eval_xlsx_path, engine='openpyxl')
                df_xlsx.columns = [re.sub(r'\s+', '', col) for col in df_xlsx.columns]
                logger.info("对xlsx作预处理完成")
                
                wb = openpyxl.load_workbook(eval_xlsx_path)
                ws = wb.active
                for index, row in df_xlsx.iterrows():
                    excel_row = index + 2
                    if excel_row > 1:
                        ws.row_dimensions[excel_row].height = 75
                    id = ws.cell(row=excel_row, column=8).value

                    eval_image_cell = ws.cell(row=excel_row, column=3)
                    eval_image_path = ws.cell(row=excel_row, column=9).value        
                    try:
                        if eval_image_path:
                            eval_image_path = os.path.normpath(eval_image_path)
                            if os.path.exists(eval_image_path):
                                utils.insert_image_limited(ws, eval_image_cell, eval_image_path)
                            else:
                                eval_image_cell.value = "空"
                                logger.info(f"id: {id}, eval图片路径不存在: {eval_image_path}")
                        else:
                            eval_image_cell.value = "空"
                    except Exception as e:
                        logger.info(f"id: {id}, 处理eval图片 {eval_image_path} 时出错: {e}")

                    cad_cell = ws.cell(row=excel_row, column=4)
                    cad_loc_path = os.path.join(pyd_path, 'cad_com_loc', f"{id}.bmp")        
                    try:
                        if not os.path.exists(cad_loc_path):
                            cad_loc_path = os.path.join(pyd_path, 'cad_com_loc', f"{id}.jpg")
                        if not os.path.exists(cad_loc_path):
                            cad_loc_path = os.path.join(pyd_path, 'cad_com_loc', f"{id}.png")
                        cad_loc_path = os.path.normpath(cad_loc_path)
                        if cad_loc_path and os.path.exists(cad_loc_path):
                            utils.insert_image_limited(ws, cad_cell, cad_loc_path)
                        else:
                            cad_cell.value = "空"
                            logger.error(f"id: {id}, cad_loc图片路径不存在: {cad_loc_path}")
                    except Exception as e:
                        logger.error(f"id: {id}, cad_img处理图片 {cad_loc_path} 时出错: {e}")

                    if ws.cell(row=excel_row, column=10).value is None:
                        ws.cell(row=excel_row, column=5).value = "空"
                    else:
                        train_image_path = ws.cell(row=excel_row, column=10).value
                        train_cell = ws.cell(row=excel_row, column=5)
                        try:
                            logger.info(f"id: {id}, train_image_path: {train_image_path}")
                            if train_image_path and os.path.exists(train_image_path):
                                train_image_path = os.path.normpath(train_image_path)
                                utils.insert_image_limited(ws, train_cell, train_image_path)
                            else:
                                train_cell.value = "空"
                        except Exception as e:
                            logger.info(f"id: {id}, train_img处理图片 {train_image_path} 时出错: {e}")

                logger.info("所有图片处理完毕，正在保存工作簿...")
                wb.save(eval_xlsx_path)
                logger.info(f"处理完成: {eval_xlsx_path}")
            except Exception as e:
                logger.error(f"处理文件 {csv_file} 时发生错误: {e}")
                raise Exception(f"处理文件 {csv_file} 时发生错误: {e}")
        status = 0
        logger.info(f"处理完成,status: {status}")
        return status

    front_rv_window()
    train_paths = [] # 用于存储train_path
    eval_results = [] # 用于存储各个eval_path及其结果
    train_statuses = [] # 用于存储各个train_path及其状态 用于后续显示
    
    # 搜索train_eval_path下层及更下层文件夹中同时拥有名字内含train的文件夹和含test文件夹的文件夹
    for root, dirs, files in os.walk(train_eval_path):
        if root != train_eval_path:  # 忽略train_eval_path该级文件夹
            train_folder = None
            test_folder = None
            for d in dirs:
                if 'train' in d:
                    train_folder = os.path.join(root, d)
                if 'test' in d:
                    test_folder = os.path.join(root, d)
            if train_folder and test_folder:
                if os.path.isdir(train_folder) and os.path.isdir(test_folder):
                    train_paths.append(train_folder)
    logger.success(f"读取train_eval_path下所有的训练路径train_paths: {train_paths}")

    if not train_paths:  # 检查列表是否为空
        logger.error("未找到训练路径")
        raise Exception("未找到训练路径")

    # 检测pyd_path下是否有train_logs的文件夹,没有的话创建该文件夹,在文件夹内创建 年-月-日.csv(若不存在的话) 
    train_logs_dir_path = os.path.join(pyd_path, 'train_logs')
    os.makedirs(train_logs_dir_path, exist_ok=True)
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    train_logs_path = os.path.join(train_logs_dir_path, f"{today_date}.csv")
    trained_success_list = []

    # 读取里边为训练完成的训练路径装入trained_success_list。
    if os.path.exists(train_logs_path):
        with open(train_logs_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # 跳过表头
            for row in reader:
                if row[1] == '训练完成':
                    trained_success_list.append(row[0])
    else:
        # 文件不存在的话把检索到的train_paths装入csv
        with open(train_logs_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['train路径', 'train状态'])
            for train_path in train_paths:
                writer.writerow([train_path, '待训练'])

    for train_path in train_paths:
        try:
            # 如果有训练完成的，则跳过
            if train_path in trained_success_list:
                logger.info(f"训练路径{train_path}训练状态为完成，跳过")
                continue

            pyperclip.copy(train_path)
            logger.info(f"开始训练{train_path}")
            utils.click_by_png(config.RV_SIMULATE_TO_TRAIN)
            if utils.search_symbol_erroring(config.RV_TRAIN_SUCCESS, 30):
                time.sleep(0.5)
                pyautogui.press('enter')
            time.sleep(0.5)
            refresh_count = 0
            while refresh_count < 300:
                if refresh_count == 1:
                    # 重新训练
                    time.sleep(1)
                    utils.click_by_png(config.RV_TRAIN_STATUS, timeout=60, if_click_right=1)
                    time.sleep(0.5)
                    pyautogui.press('down', 8)
                    time.sleep(0.5)
                    pyautogui.press('enter')
                    time.sleep(2)
                # 刷新
                utils.click_by_png(config.RV_JOB_NAME, timeout=60, if_click_right=1)
                time.sleep(0.5)
                pyautogui.press('down', 2)
                pyautogui.press('enter')
                logger.info(f"训练刷新第{refresh_count}次")
                time.sleep(0.5)
                # 查看训练状态
                utils.click_by_png(config.RV_TRAIN_STATUS)
                time.sleep(0.5)
                pyautogui.hotkey('ctrl', 'a')
                time.sleep(0.5)
                pyautogui.hotkey('ctrl', 'c')
                train_result = pyperclip.paste()
                logger.info(train_result)
                if '训练完成' in train_result:
                    train_result = '训练完成'
                    train_statuses.append((train_path, train_result))
                    logger.info("训练状态: 训练完成")
                    break
                elif '训练失败' in train_result:
                    train_result = '训练失败'
                    train_statuses.append((train_path, train_result))
                    logger.error("训练状态: 训练失败")
                    break
                elif '待训练' in train_result:
                    refresh_count += 1
                    logger.info(f"训练状态: 待训练, 刷新次数: {refresh_count}")
                    if refresh_count == 1:
                        time.sleep(0.5)
                    else:
                        time.sleep(7)
                    # if refresh_count == 9:
                    #     train_result = '待训练'
                    #     train_statuses.append((train_path, train_result))
                    #     logger.error("训练状态: 待训练, 达到最大刷新次数")
                    #     break
                else:
                    refresh_count = 1
                    logger.error("复制到的训练状态未知，重试中")
                    time.sleep(5)

            logger.info(f"{train_path}训练完毕，开始推理")
            
            # 查询train_path同级文件夹下名字包含test的文件夹 装入eval_path
            eval_paths = glob.glob(os.path.join(os.path.dirname(train_path), '*test*'))
            if not eval_paths:  # 检查列表是否为空
                logger.error("未找到推理的路径")
                raise Exception("未找到推理的路径")
            else:
                logger.info(f"训练路径为:{train_path}, 推理路径为:{eval_paths}")
            for eval_path in eval_paths:
                # 训练失败的话就不用推理了
                if train_result == '训练失败':
                    eval_result = '训练失败，因此未推理'
                    eval_results.append((eval_path, eval_result, good_ng))
                    break

                if mode == "normal":
                    good_ng = "空"
                    # 复制路径处理
                    if os.path.exists("temp_eval_path.txt"):
                        os.remove("temp_eval_path.txt")
                    with open("temp_eval_path.txt", "w", encoding='utf-8') as temp_file:
                        temp_file.write(eval_path)
                    # 从记事本读取eval_path到剪切板
                    with open("temp_eval_path.txt", "r", encoding='utf-8') as temp_file:
                        eval_path_from_txt = temp_file.read()
                        pyperclip.copy('')
                        time.sleep(2)
                        pyperclip.copy(eval_path_from_txt)
                    
                    # 确保剪切板内容正确
                    clipboard_content = pyperclip.paste()
                    for i in range(5):
                        pyperclip.copy(eval_path_from_txt)
                        time.sleep(2)
                        clipboard_content = pyperclip.paste()
                        logger.info(f"第{i+1}次复制检测，剪切板内容: {clipboard_content}，期望内容: {eval_path_from_txt}")
                        if clipboard_content == eval_path_from_txt:
                            break
                    
                    if clipboard_content != eval_path_from_txt:
                        logger.error("无法确保剪切板内容正确，操作中止")
                        raise Exception("剪切板内容不匹配")
                    
                    time.sleep(1)
                    logger.warning(f"剪切板内容: {clipboard_content}，准备点击推理")
                    time.sleep(1)
                    # 开始推理
                    utils.click_by_png(config.RV_SIMULATE_TO_EVAL, tolerance=0.95)
                    logger.warning(f"点击完模拟至推理了，目前的剪切板内容：{pyperclip.paste()},先前的剪切板内容为：{clipboard_content}")
                    time.sleep(0.5)
                    os.remove("temp_eval_path.txt")
                    utils.search_symbol_erroring(config.RV_EVAL_SUCCESS, 30)
                    time.sleep(0.5)
                    pyautogui.press('enter')
                    # 刷新任务状态并提取结果
                    utils.click_by_png(config.RV_JOB_NAME, timeout=6, if_click_right=1)
                    time.sleep(0.5)
                    pyautogui.press('down', 2)
                    pyautogui.press('enter')
                    time.sleep(2)
                    utils.click_by_png(config.RV_TRAIN_STATUS, if_click_right=1)
                    time.sleep(0.5)
                    if not utils.search_symbol(config.RV_CLICK_RESTART_EVAL, 5):
                        time.sleep(5)
                    utils.click_by_png(config.RV_CLICK_RESTART_EVAL)
                    click_time = datetime.datetime.now()
                    logger.info(f"点击重新推理时间: {click_time.strftime('%Y-%m-%d %H:%M:%S')}")
                    retry_count = 0
                    while retry_count < 300:
                        logger.info(f"推理刷新第{retry_count}次")
                        time.sleep(5)
                        utils.click_by_png(config.RV_MISSION_MANAGE, tolerance=0.7)
                        time.sleep(0.5)
                        pyautogui.hotkey('ctrl', 'a')
                        time.sleep(1.5)
                        pyautogui.hotkey('ctrl', 'c')
                        logger.info("开始解析推理状态")
                        clipboard_content = pyperclip.paste()
                        task_lines = clipboard_content.split('\n')
                        latest_time = None
                        latest_record = None
                        for line in task_lines[1:]:
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
                            if train_result == '待训练':
                                eval_result = f"{train_result}, {eval_result}"
                            utils.click_by_png(config.RV_CLOSE_MISSION_MANAGE, timeout=5)
                            break
                        elif latest_record and '推理' in latest_record[0] and '失败' in latest_record[2]:
                            eval_result = '推理失败'
                            if train_result == '待训练':
                                eval_result = f"{train_result}, {eval_result}"
                            utils.click_by_png(config.RV_CLOSE_MISSION_MANAGE, timeout=5)
                            break
                        elif "队列" in latest_record[1]:
                            retry_count += 0.5
                            logger.info(f"推理处于队列中")
                            utils.click_by_png(config.RV_CLOSE_MISSION_MANAGE, timeout=5)
                        else:
                            utils.click_by_png(config.RV_CLOSE_MISSION_MANAGE, timeout=5)
                            time.sleep(10)  # 等待10秒后再次尝试
                            retry_count += 1
                    # if retry_count == 6:
                    #     eval_result = '推理失败'
                    #     if train_result == '待训练':
                    #         eval_result = f"{train_result}, {eval_result}"
                    time.sleep(1)
                    eval_results.clear()
                    eval_results.append((eval_path, eval_result, good_ng))
                elif mode == "good_ng":
                    # 获取eval_path下的good和ng文件夹路径
                    good_path = os.path.join(eval_path, 'good')
                    ng_path = os.path.join(eval_path, 'ng')
                    # 分为good和ng两种情况
                    if os.path.exists(good_path):
                        logger.info(f"good存在: {good_path}")
                        good_ng = "good"
                        # 复制路径处理
                        if os.path.exists("temp_good_path.txt"):
                            os.remove("temp_good_path.txt")
                        with open("temp_good_path.txt", "w", encoding='utf-8') as temp_file:
                            temp_file.write(good_path)
                        # 从记事本读取eval_path到剪切板
                        with open("temp_good_path.txt", "r", encoding='utf-8') as temp_file:
                            good_path_from_txt = temp_file.read()
                            pyperclip.copy('')
                            time.sleep(2)
                            pyperclip.copy(good_path_from_txt)
                            
                        # 确保剪切板内容正确
                        clipboard_content = pyperclip.paste()
                        for i in range(5):
                            pyperclip.copy(eval_path_from_txt)
                            time.sleep(2)
                            clipboard_content = pyperclip.paste()
                            logger.info(f"第{i+1}次复制检测，剪切板内容: {clipboard_content}，期望内容: {eval_path_from_txt}")
                            if clipboard_content == eval_path_from_txt:
                                break
                        
                        if clipboard_content != eval_path_from_txt:
                            logger.error("无法确保剪切板内容正确，操作中止")
                            raise Exception("剪切板内容不匹配")
                        
                        time.sleep(1)
                        logger.warning(f"剪切板内容: {clipboard_content}，准备点击推理")
                        time.sleep(1)
                        # 开始推理
                        utils.click_by_png(config.RV_SIMULATE_TO_EVAL, tolerance=0.95)
                        time.sleep(0.5)
                        os.remove("temp_good_path.txt")
                        utils.search_symbol_erroring(config.RV_EVAL_SUCCESS, 30)
                        time.sleep(0.5)
                        pyautogui.press('enter')
                        # 刷新任务状态
                        utils.click_by_png(config.RV_JOB_NAME, timeout=6, if_click_right=1)
                        time.sleep(0.5)
                        pyautogui.press('down',2)
                        pyautogui.press('enter')
                        # 点击重新推理 推理完成后再去点手动筛选
                        time.sleep(2)
                        utils.click_by_png(config.RV_TRAIN_STATUS, if_click_right=1)
                        if not utils.search_symbol(config.RV_CLICK_RESTART_EVAL, 5):
                            time.sleep(5)
                        utils.click_by_png(config.RV_CLICK_RESTART_EVAL)
                        click_time = datetime.datetime.now()
                        logger.info(f"点击重新推理时间: {click_time.strftime('%Y-%m-%d %H:%M:%S')}")
                        # 重新推理，点击任务状态，获取eval_result
                        retry_count = 0
                        while retry_count < 300:
                            logger.info(f"推理刷新第{retry_count}次")
                            time.sleep(5)
                            utils.click_by_png(config.RV_MISSION_MANAGE, tolerance=0.7)
                            time.sleep(0.5)
                            pyautogui.hotkey('ctrl', 'a')
                            time.sleep(1)
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
                                if train_result == '待训练':
                                    eval_result = f"{train_result}, {eval_result}"
                                utils.click_by_png(config.RV_CLOSE_MISSION_MANAGE, timeout=5)
                                break
                            elif latest_record and '推理' in latest_record[0] and '失败' in latest_record[2]:
                                eval_result = '推理失败'
                                if train_result == '待训练':
                                    eval_result = f"{train_result}, {eval_result}"
                                utils.click_by_png(config.RV_CLOSE_MISSION_MANAGE, timeout=5)
                                break
                            elif "队列" in latest_record[1]:
                                retry_count += 0.5
                                logger.info(f"推理处于队列中")
                                utils.click_by_png(config.RV_CLOSE_MISSION_MANAGE, timeout=5)
                            else:
                                utils.click_by_png(config.RV_CLOSE_MISSION_MANAGE, timeout=5)
                                time.sleep(10)  # 等待10秒后再次尝试
                                retry_count += 1
                        # if retry_count == 6:
                        #     eval_result = '推理失败'
                        #     if train_result == '待训练':
                        #         eval_result = f"{train_result}, {eval_result}"
                        eval_results.clear()
                        eval_results.append((good_path, eval_result, good_ng))
                        time.sleep(3)
                        # 手动筛选，本页pass
                        utils.click_by_png(config.RV_JOB_NAME, if_click_right=1)
                        time.sleep(1)
                        utils.click_by_png(config.RV_MANUAL_FILTER)
                        time.sleep(1)
                        # 不断pass 直到没图片
                        while True:
                            if utils.search_symbol(config.RV_IMAGE_ZERO, 5, tolerance=0.95):
                                utils.click_by_png(config.RV_CURRENT_CLOSE, tolerance=0.99)
                                break
                            utils.click_by_png(config.RV_PASS, tolerance=0.9)
                            time.sleep(1)
                            pyautogui.press('enter')
                            time.sleep(3)
                    if os.path.exists(ng_path):
                        logger.info(f"ng存在: {ng_path}")
                        good_ng = "ng"
                        # 复制路径处理
                        if os.path.exists("temp_ng_path.txt"):
                            os.remove("temp_ng_path.txt")
                        with open("temp_ng_path.txt", "w", encoding='utf-8') as temp_file:
                            temp_file.write(ng_path)
                        # 从记事本读取eval_path到剪切板
                        with open("temp_ng_path.txt", "r", encoding='utf-8') as temp_file:
                            ng_path_from_txt = temp_file.read()
                            pyperclip.copy('')
                            time.sleep(2)
                            pyperclip.copy(ng_path_from_txt)

                        # 确保剪切板内容正确
                        clipboard_content = pyperclip.paste()
                        for i in range(5):
                            pyperclip.copy(eval_path_from_txt)
                            time.sleep(2)
                            clipboard_content = pyperclip.paste()
                            logger.info(f"第{i+1}次复制检测，剪切板内容: {clipboard_content}，期望内容: {eval_path_from_txt}")
                            if clipboard_content == eval_path_from_txt:
                                break
                        
                        if clipboard_content != eval_path_from_txt:
                            logger.error("无法确保剪切板内容正确，操作中止")
                            raise Exception("剪切板内容不匹配")
                        
                        time.sleep(1)
                        logger.warning(f"剪切板内容: {clipboard_content}，准备点击推理")
                        time.sleep(1)  
                        # 开始推理
                        utils.click_by_png(config.RV_SIMULATE_TO_EVAL, tolerance=0.95)
                        time.sleep(0.5)
                        os.remove("temp_ng_path.txt")
                        utils.search_symbol_erroring(config.RV_EVAL_SUCCESS, 30)
                        time.sleep(1)
                        pyautogui.press('enter')
                        # 刷新任务状态
                        utils.click_by_png(config.RV_JOB_NAME, timeout=6, if_click_right=1)
                        time.sleep(0.5)
                        pyautogui.press('down',2)
                        pyautogui.press('enter')
                        # 点击重新推理
                        time.sleep(2)
                        utils.click_by_png(config.RV_TRAIN_STATUS, if_click_right=1)
                        if not utils.search_symbol(config.RV_CLICK_RESTART_EVAL, 5):
                            time.sleep(5)
                        utils.click_by_png(config.RV_CLICK_RESTART_EVAL)
                        click_time = datetime.datetime.now()
                        logger.info(f"点击重新推理时间: {click_time.strftime('%Y-%m-%d %H:%M:%S')}")
                        # 获取eval_result
                        retry_count = 0
                        while retry_count < 300:
                            logger.info(f"推理刷新第{retry_count}次")
                            time.sleep(5)
                            utils.click_by_png(config.RV_MISSION_MANAGE, tolerance=0.7)
                            time.sleep(0.5)
                            pyautogui.hotkey('ctrl', 'a')
                            time.sleep(1)
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
                                if train_result == '待训练':
                                    eval_result = f"{train_result}, {eval_result}"
                                utils.click_by_png(config.RV_CLOSE_MISSION_MANAGE, timeout=5)
                                break
                            elif latest_record and '推理' in latest_record[0] and '失败' in latest_record[2]:
                                eval_result = '推理失败'
                                if train_result == '待训练':
                                    eval_result = f"{train_result}, {eval_result}"
                                utils.click_by_png(config.RV_CLOSE_MISSION_MANAGE, timeout=5)
                                break
                            elif "队列" in latest_record[1]:
                                retry_count += 0.5
                                logger.info(f"推理处于队列中")
                                utils.click_by_png(config.RV_CLOSE_MISSION_MANAGE, timeout=5)
                            else:
                                utils.click_by_png(config.RV_CLOSE_MISSION_MANAGE, timeout=5)
                                time.sleep(10)  # 等待10秒后再次尝试
                                retry_count += 1
                        # if retry_count == 6:
                        #     eval_result = '推理失败'
                        #     if train_result == '待训练':
                        #         eval_result = f"{train_result}, {eval_result}"
                        eval_results.clear()
                        eval_results.append((ng_path, eval_result, good_ng))
                        time.sleep(3)
                        # 手动筛选，本页ng
                        utils.click_by_png(config.RV_JOB_NAME, if_click_right=1)
                        time.sleep(1)
                        utils.click_by_png(config.RV_MANUAL_FILTER)
                        time.sleep(1)
                        # 搜是否图片为0 没搜到的话不断ng 直到没图片
                        while True:
                            if utils.search_symbol(config.RV_IMAGE_ZERO, 5, tolerance=0.95):
                                utils.click_by_png(config.RV_CURRENT_CLOSE, tolerance=0.99)
                                break
                            utils.click_by_png(config.RV_NG, tolerance=0.9)
                            time.sleep(1)
                            pyautogui.press('enter')
                            time.sleep(3)

        except Exception as e:
            logger.error(f"在处理{train_path}时发生错误: {e}")
            raise Exception(f"在处理{train_path}时发生错误: {e}")                    

        # 删除job
        utils.click_by_png(config.RV_JOB_NAME, if_click_right=1)
        pyautogui.press('down')
        pyautogui.press('enter')

        have_trained_before = False
        # 训练-推理结束，转csv为xlsx，并同步数据至xlsx 
        try:
            today_date = datetime.datetime.now().strftime("%Y-%m-%d")
            log_csv_path = os.path.join(pyd_path, "logs", "res_static", f"{today_date}.csv")
            logger.info(f"log_path: {log_csv_path}")
            if not os.path.exists(log_csv_path):
                logger.error("未找到推理后生成的csv文件")
                raise Exception("未找到推理后生成的csv文件")
            
            # 新增日志文件
            log_xlsx_path = os.path.join(pyd_path, "eval_logs")
            os.makedirs(log_xlsx_path, exist_ok=True)
            eval_xlsx_path = os.path.join(log_xlsx_path, f"{today_date}.xlsx")
            completed_txt_path = os.path.join(pyd_path, "脚本已运行完成.txt")
            if os.path.exists(completed_txt_path):
                os.remove(completed_txt_path)
            logger.info(f"推理结果生成路径: {eval_xlsx_path}")

            # 如果xlsx不存在 则新增xlsx 存在则把csv内数据同步至xlsx
            if not os.path.exists(eval_xlsx_path):
                with open(log_csv_path, 'rb') as file:
                    content = file.read()
                    result = chardet.detect(content)
                    encoding = result['encoding'] if result['encoding'] else 'utf-8'
                    # 尝试使用探测到的编码打开文件，如果失败则使用GBK编码尝试
                    try:
                        content = content.decode(encoding)
                    except UnicodeDecodeError:
                        content = content.decode('gbk', errors='ignore')

                # 使用探测到的编码读取文件
                df_csv = pd.read_csv(log_csv_path, encoding=encoding)
                # 添加新列
                df_csv = df_csv.assign(eval结果=None, good_ng=None, eval图片=None, 定位图片=None, train图片=None, eval路径=None)
                # 重新排序列，将新列放在前面
                columns_order = ['eval结果', 'good_ng', 'eval图片', '定位图片', 'train图片', 'eval路径'] + [col for col in df_csv.columns if col not in ['eval结果', 'good_ng', 'eval图片', '定位图片', 'train图片', 'eval路径']]
                df_csv = df_csv[columns_order]
                # 保存为XLSX
                df_csv.to_excel(eval_xlsx_path, index=False, engine='openpyxl')
                logger.info("对xlsx作预处理")
                # 打开xlsx
                df_xlsx = pd.read_excel(eval_xlsx_path, engine='openpyxl')
                # 去除列名中的空白符
                df_xlsx.columns = [col.strip() for col in df_xlsx.columns]
                # 使用openpyxl直接加载工作簿以修改列名样式
                wb = openpyxl.load_workbook(eval_xlsx_path)
                ws = wb.active
                # 取消列名加粗
                for cell in ws[1]:  # 第一行是列名
                    cell.font = Font(bold=False)
                # 设置B列和D列的列宽为18字符
                ws.column_dimensions['C'].width = 18
                ws.column_dimensions['D'].width = 18
                ws.column_dimensions['E'].width = 18
                # 保存修改后的工作簿
                wb.save(eval_xlsx_path)
                # 重新加载DataFrame以确保列名更改生效
                df_xlsx = pd.read_excel(eval_xlsx_path, engine='openpyxl')
                # 去除列名中的空白符和其他特殊字符
                df_xlsx.columns = [re.sub(r'\s+', '', col) for col in df_xlsx.columns]
                logger.info("推理结束后对xlsx作预处理完成，此后每条train路径完成后都会进行一次同步")
                
            else:
                have_trained_before = True
                sync_csv_to_xlsx(log_csv_path, eval_xlsx_path)
        except Exception as e:
            logger.error(f"转csv为xlsx并同步数据至xlsx时发生错误: {e}")
            raise Exception(f"转csv为xlsx并同步数据至xlsx时发生错误: {e}")
        def clean_id(id_str):
            return str(id_str).strip().replace('\n', '').replace('\r', '').replace('\t', '')

        logger.info("开始将推理结果同步至xlsx")
        wb = openpyxl.load_workbook(eval_xlsx_path)
        ws = wb.active
        logger.info("工作簿和工作表已初始化")

        # 更新df_xlsx
        df_xlsx = pd.read_excel(eval_xlsx_path, engine='openpyxl')
        df_xlsx.columns = [col.strip() for col in df_xlsx.columns]
        df_xlsx.columns = [re.sub(r'\s+', '', col) for col in df_xlsx.columns]

        logger.info("开始更新eval_results至eval_xlsx...")
        logger.warning(f"eval_results: {eval_results}")
        for eval_path, eval_result, good_ng in eval_results:
            eval_image_paths = []
            eval_image_paths.extend(glob.glob(os.path.join(eval_path, '**/*.bmp'), recursive=True))
            eval_image_paths.extend(glob.glob(os.path.join(eval_path, '**/*.jpg'), recursive=True))
            eval_image_paths.extend(glob.glob(os.path.join(eval_path, '**/*.png'), recursive=True))
            logger.info(f"推理路径下找到的图片路径为: {eval_image_paths}")
            # 图片名称即id。通过id查找匹配的行 给其赋值
            for eval_image_path in eval_image_paths:
                eval_image_name = clean_id(os.path.splitext(os.path.basename(eval_image_path))[0])
                logger.info(f"处理的图片id为: {eval_image_name}")

                try:
                    # 打印调试信息
                    logger.warning(f"待匹配的eval_image_name: '{eval_image_name}'")
                    logger.warning(f"所有行中的id值: {df_xlsx['id'].tolist()}")
                    logger.info("除标题行外所有行内容如下：")
                    for row in ws.iter_rows(min_row=2, values_only=True):  # 从第二行开始打印
                        logger.info(row)
                    # 除了标题行外 每一个id值不为空的行都要log
                    for index, row in df_xlsx.iterrows():
                        if pd.notna(row['id']):
                            logger.info(f"行 {index + 2} 的id值: {row['id']}")
                    logger.warning(f"所有行中的id值: {df_xlsx['id'].tolist()}")

                    # 确保id列为字符串类型并去除空格、换行符、回车符和制表符
                    df_xlsx['id'] = df_xlsx['id'].apply(clean_id).astype(str)
                    
                    # 搜索所有id列有值的行（除了标题行外）
                    for index, row in df_xlsx.iterrows():
                        if pd.notna(row['id']):
                            logger.info(f"行 {index + 2} 的id列数据类型: {type(row['id'])}")

                    # 使用字符串包含关系进行匹配
                    matching_rows = df_xlsx[df_xlsx['id'].astype(str).str.contains(eval_image_name, na=False)]
                    if not matching_rows.empty:
                        for index in matching_rows.index:
                            excel_row = index + 2
                            logger.info(f"匹配到的行号：{index + 1}")
                            logger.info(f"更新eval_results至xslx内查找到的对应行：eval_path: {eval_path}, eval_image_path: {eval_image_path}, eval_image_name: {eval_image_name}, eval_result: {eval_result}")
                            ws.cell(row=excel_row, column=1, value=eval_result)
                            ws.cell(row=excel_row, column=2, value=good_ng)
                            ws.cell(row=excel_row, column=3, value=eval_image_path)
                            ws.cell(row=excel_row, column=6, value=eval_image_path)
                            logger.info(f"已匹配到第 {index + 1} 行")
                        wb.save(eval_xlsx_path)
                    else:
                        logger.warning(f"未找到匹配的行，id为: {eval_image_name}")
                except Exception as e:
                    logger.error(f"更新eval_results至xslx时发生错误: {e}")

            logger.info("推理结束，开始记录训练结果（该路径已 训练-推理 完成）")
            try:
                # 处理train.csv，填入train路径及train状态
                logger.info(f"读取训练日志文件: {train_logs_path}")
                df_train_logs = pd.read_csv(train_logs_path, encoding='utf-8')
                logger.info(f"训练日志文件内容: {df_train_logs}")
                
                if train_path in df_train_logs['train路径'].values:
                    logger.info(f"更新训练路径 {train_path} 的训练状态为 {train_result}")
                    df_train_logs.loc[df_train_logs['train路径'] == train_path, 'train状态'] = train_result
                    # 将train状态的单元格标注为黄色
                    for index, row in df_train_logs.iterrows():
                        if row['train路径'] == train_path:
                            df_train_logs.at[index, 'train状态'] = train_result
                    df_train_logs.to_csv(train_logs_path, index=False, encoding='utf-8')
                    logger.info(f"训练路径 {train_path} 的训练状态已更新并保存")
                else:
                    logger.info(f"训练路径 {train_path} 不存在于训练日志中，添加新记录")
                    new_row = pd.DataFrame([[train_path, train_result]], columns=['train路径', 'train状态'])
                    df_train_logs = pd.concat([df_train_logs, new_row], ignore_index=True)
                    df_train_logs.to_csv(train_logs_path, index=False, encoding='utf-8')
                    logger.info(f"新记录已添加并保存到训练日志文件")
                
                logger.info("训练日志文件已关闭")
            except Exception as e:
                logger.error(f"记录训练结果时发生错误: {e}")
                raise Exception(f"记录训练结果时发生错误: {e}")
            finally:
                logger.info("记录训练结果操作完成")

    # 所有train路径训练完毕之后 再作排序 排序完之后再加入图
    if have_trained_before:
        logger.info(f"检测到之前已训练，开始删除xlsx内所有图片...删除前图片数量：{len(ws._images)}")
        ws._images = [image for image in ws._images if image.anchor._from.col in [2, 3, 4]]
        logger.info("已删除所有在C, D, E列的图片")
        logger.info(f"删除后图片数量: {len(ws._images)}")
    ws = wb.active
    data = list(ws.values)
    header = data[0]  # 保存标题行
    non_empty_rows = [row for row in ws.iter_rows(min_row=2, values_only=True) if any(row)]
    logger.info(f"xlsx内有数据的行数: {len(non_empty_rows)}")
    # 根据 id 列名排序，忽略标题行，并去重
    seen = set()
    unique_data = []
    for row in sorted(data[1:], key=lambda x: x[header.index('id')]):
        if row[header.index('id')] not in seen:
            unique_data.append(row)
            seen.add(row[header.index('id')])
    for row_idx, row in enumerate([header] + unique_data, 1):
        #  TODO 就这傻逼地方 不判断none的话会导致bug
        for col_idx, value in enumerate(row, 1):
            if value is None:
                ws.cell(row=row_idx, column=col_idx).value = None
            else:
                ws.cell(row=row_idx, column=col_idx, value = value)
    logger.info("行数据已排序，正在保存工作簿...")
    wb.save(eval_xlsx_path)
    # 重新加载工作簿以验证数据
    logger.info("开始处理图片")
    # 单独处理图片
    for index, row in df_xlsx.iterrows():
        excel_row = index + 2
        # 设置首行外其他行的行高为100磅
        if excel_row > 1:
            ws.row_dimensions[excel_row].height = 75  # 100磅约等于75像素
        id = ws.cell(row=excel_row, column=8).value

        # 处理eval图片
        eval_image_cell = ws.cell(row=excel_row, column=3)  
        eval_image_path = eval_image_cell.value        
        try:
            if eval_image_path:
                eval_image_path = os.path.normpath(eval_image_path)
                if os.path.exists(eval_image_path):
                    utils.insert_image_limited(ws, eval_image_cell, eval_image_path)
                else:
                    eval_image_cell.value = "空"
                    logger.info(f"id: {id}, eval图片路径不存在: {eval_image_path}")
            else:
                eval_image_cell.value = "空"
        except Exception as e:
            logger.info(f"id: {id}, 处理eval图片 {eval_image_path} 时出错: {e}")
        # 处理定位图片
        cad_cell = ws.cell(row=excel_row, column=4)
        cad_loc_path = os.path.join(pyd_path, 'cad_com_loc', f"{id}.bmp")        
        try:
            if not os.path.exists(cad_loc_path):
                cad_loc_path = os.path.join(pyd_path, 'cad_com_loc', f"{id}.jpg")
            if not os.path.exists(cad_loc_path):
                cad_loc_path = os.path.join(pyd_path, 'cad_com_loc', f"{id}.png")
            cad_loc_path = os.path.normpath(cad_loc_path)
            if cad_loc_path and os.path.exists(cad_loc_path):
                utils.insert_image_limited(ws, cad_cell, cad_loc_path)
            else:
                cad_cell.value = "空"
                logger.error(f"id: {id}, cad_loc图片路径不存在: {cad_loc_path}")
        except Exception as e:
            logger.error(f"id: {id}, cad_img处理图片 {cad_loc_path} 时出错: {e}")
        # 处理train_img_path
        if ws.cell(row=excel_row, column=10).value is None:
            ws.cell(row=excel_row, column=5).value = "空"
        else:
            train_image_path = ws.cell(row=excel_row, column=10).value
            train_cell = ws.cell(row=excel_row, column=5)
            try:
                logger.info(f"id: {id}, train_image_path: {train_image_path}")
                if train_image_path and os.path.exists(train_image_path):
                    train_image_path = os.path.normpath(train_image_path)
                    utils.insert_image_limited(ws, train_cell, train_image_path)
                else:
                    train_cell.value = "空"
            except Exception as e:
                logger.info(f"id: {id}, train_img处理图片 {train_image_path} 时出错: {e}")

    # 处理完所有图片后再次保存工作簿
    logger.info("所有图片处理完毕，正在保存工作簿...")
    
    wb.save(eval_xlsx_path)
    with open(os.path.join(os.path.dirname(eval_xlsx_path), "脚本已运行完成.txt"), "w") as f:
        pass

    status = 0
    logger.info(f"ai复判完成")
    logger.info(f"train_statuses: {train_statuses}")
    return status, train_statuses
