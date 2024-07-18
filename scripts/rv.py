import csv
import time
import pyperclip
import utils
import config
import re
import os
import shutil
import glob
import datetime
import pyautogui
import pandas as pd
from pywinauto import Application,Desktop
from loguru import logger
    # 前置程序（假定程序已打开）
def front_rv_ai_test():
    windows = Desktop(backend="uia").windows()
    window_found = False
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
            main_window.maximize()
            main_window.wait('ready', timeout=10)
        else:
            status = -1
            logger.error("未找到窗口")
            raise Exception("未找到窗口")
    else:
        status = -1
        logger.error("未找到程序")
        raise Exception("未找到程序")
    # 点击程序里的训练
    if utils.search_symbol_erroring(config.RV_TOPIC):
        logger.info("识别到窗口标题")

# ai复判 总路径(包含train,test文件夹),结果路径（含定位图片及输出数据文档）
def rv_ai_test(train_eval_path, result_path):
    status = 1
    train_contents = set()
    eval_contents = set()

    # 开始从提供的路径向上遍历，直到找到包含pyd的目录,用pyd_path保存
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

    # 搜索train_eval_path下所有名字含train的文件夹(可能为自身) ,装入train_contents
    train_folders = [os.path.join(train_eval_path, d) for d in os.listdir(train_eval_path) if 'train' in d and os.path.isdir(os.path.join(train_eval_path, d))]
    train_contents.update(train_folders)
    logger.info(f"train_contents: {train_contents}")
    # 遍历train_contents集合中的每个元素
    for train_content in train_contents:
        pyperclip.copy(train_content)
        
        # 点击训练按钮
        utils.click_by_png(config.RV_SIMULATE_TO_TRAIN)
        utils.click_by_png(config.RV_TRAIN_SUCCESS)
        pyautogui.press('enter')
        # 右击,刷新
        refresh_count = 0
        while refresh_count < 6:
            utils.click_by_png(config.RV_JOB_NAME, if_click_right=1)
            utils.click_by_png(config.RV_REFRESH_JOB)
            time.sleep(10)  # 每隔十秒刷新一次

            # 查看训练状态
            utils.click_by_png(config.RV_TRAIN_STATUS)
            pyautogui.press('ctrl', 'c')
            train_result = pyperclip.paste()

            if '待训练' in train_result:
                refresh_count += 1
                if refresh_count == 6:
                    train_result = '待训练'
                    break
            elif '训练完成' in train_result:
                train_result = '训练完成'
                break
            elif '训练失败' in train_result:
                train_result = '训练失败'
                break
            else:
                status = -1
                logger.error("训练状态未知")
                raise Exception("训练状态未知")
        # 检测pyd_path下是否有train_logs的文件夹,没有的话创建该文件夹,在文件夹内创建 年-月-日.csv(若不存在的话) 
        train_logs_path = os.path.join(pyd_path, 'train_logs')
        os.makedirs(train_logs_path, exist_ok=True)
        today_date = datetime.datetime.now().strftime("%Y-%m-%d")
        csv_file_path = os.path.join(train_logs_path, f"{today_date}.csv")
        # 列名为'train路径','train状态'. train路径为train_content,train状态为train_result,先确定列名存在,再逐行往内加入数据
        if not os.path.exists(csv_file_path):
            with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['train路径', 'train状态'])
        with open(csv_file_path, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([train_content, train_result])
        # 保存并关闭该csv
        file.close()
        utils.click_by_png(config.RV_JOB_NAME,if_click_right=1)
        utils.click_by_png(config.RV_DELETE_JOB)
    # =====================================================================================================
    # eval_folders装入所有train_eval_path下名字含eval的文件夹,后装入eval_contents
    eval_folders = [os.path.join(train_eval_path, d) for d in os.listdir(train_eval_path) if 'eval' in d and os.path.isdir(os.path.join(train_eval_path, d))]
    eval_contents.update(eval_folders)
    logger.info(f"eval_contents: {eval_contents}")

    for eval_content in eval_contents:
        pyperclip.copy(eval_content)
        # 点击推理按钮
        utils.click_by_png(config.RV_SIMULATE_TO_EVAL)
        utils.click_by_png(config.RV_EVAL_SUCCESS)
        pyautogui.press('enter')
        # 右击,刷新
        utils.click_by_png(config.RV_JOB_NAME, if_click_right=1)
        utils.click_by_png(config.RV_REFRESH_JOB)
        # 查看状态
        retry_count = 0
        while retry_count < 6:
            utils.click_by_png(config.RV_CLOSE_MISSION_MANAGE)
            pyautogui.press('ctrl', 'a')
            pyautogui.press('ctrl', 'c')
            logger.info("开始解析推理状态")
            # 解析剪切板内容为列表，每行一个元素
            clipboard_content = pyperclip.paste()
            task_lines = clipboard_content.split('\n')
            # 初始化变量来存储最近的添加时间和对应的记录
            latest_time = None
            latest_record = None
            # 遍历每行，解析出添加时间和任务状态
            for line in task_lines:
                parts = line.split('\t')
                if len(parts) >= 6:
                    task_id, task_type, task_status, result, add_time, next_time = parts
                    # 将添加时间字符串转换为datetime对象
                    try:
                        add_time_dt = datetime.datetime.strptime(add_time, "%Y/%m/%d %H:%M:%S")
                        # 检查是否是最近的时间
                        if latest_time is None or add_time_dt > latest_time:
                            latest_time = add_time_dt
                            latest_record = (task_type, result)
                    except Exception:
                        continue
            # 检查最近记录是否包含'推理'和'成功'
            if latest_record and '推理' in latest_record[0] and '成功' in latest_record[1]:
                eval_result = '推理成功'
                break
            else:
                utils.click_by_png(config.RV_CLOSE_MISSION_MANAGE)
                time.sleep(10)  # 等待10秒后再次尝试
                retry_count += 1
        if retry_count == 6:
            eval_result = '推理失败'
            eval_image_name = "None"
            eval_image = "None"
            utils.click_by_png(config.RV_CLOSE_MISSION_MANAGE)
       
        # 推理成功后才去拿数据
        if eval_result == '推理成功':
            # eval图片名称为eval_content下所有图片的名称
            eval_image_names = os.listdir(eval_content)
            eval_images = [os.path.join(eval_content, name) for name in eval_image_names]
        utils.click_by_png(config.RV_JOB_NAME,if_click_right=1)
        utils.click_by_png(config.RV_DELETE_JOB)
        # 复制pyd文件夹下/logs/res_static文件夹内当天的 年-月-日.csv 黏贴到pyd下eval_logs文件夹内(如果该csv和文件夹都没有的话才这么做)
        today_date = datetime.datetime.now().strftime("%Y-%m-%d")
        source_csv_path = os.path.join(pyd_path, "logs", "res_static", f"{today_date}.csv")
        target_folder_path = os.path.join(pyd_path, "eval_logs")
        os.makedirs(target_folder_path, exist_ok=True)
        target_csv_path = os.path.join(target_folder_path, f"{today_date}.csv")
        if not os.path.exists(target_csv_path):
            shutil.copy(source_csv_path, target_csv_path)
        # 打开csv
        df = pd.read_csv(target_csv_path)

        # 为每个图片名称和图片路径创建一行数据
        for eval_image_name, eval_image in zip(eval_image_names, eval_images):
            df_row = df[df['id'].astype(str) == eval_image_name.split('.')[0]]  # 假设id和图片名称前缀相同
            if not df_row.empty:
                df.loc[df_row.index, 'eval路径'] = train_eval_path
                df.loc[df_row.index, '定位的图片路径'] = result_path
                df.loc[df_row.index, 'eval图片名称'] = eval_image_name
                df.loc[df_row.index, 'eval图片'] = eval_image
                df.loc[df_row.index, 'eval结果'] = eval_result

        # 将新列插入到最前面
        cols = df.columns.tolist()
        new_cols = cols[-5:] + cols[:-5]
        df = df[new_cols]

        # 删除id列
        df.drop('id', axis=1, inplace=True)

        # 保存修改后的CSV文件
        df.to_csv(target_csv_path, index=False)

    logger.info(f"ai复判完成")
    status = 0

    return status