
import datetime
import os
import shutil
from loguru import logger
import utils
import config
import pyautogui
import time

@utils.screenshot_error_to_excel()
def sjdc_001_01():
    utils.check_and_launch_aoi()
    utils.check_export_test_data(False)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range (3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,20,tolerance=0.75)
    if not utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 300, tolerance=0.75):
        raise Exception("循环单次时疑似超过五分钟")
    # 检测F盘DataExport下有没有三分钟内生成的数据
    folder_path = f"F:/DataExport"
    if not utils.check_new_data(path=folder_path, name=job_name):
        raise Exception(f"{folder_path}下疑似未生成该笔数据")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def sjdc_001_02():
    utils.check_and_launch_aoi()
    utils.check_export_test_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range (3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,20,tolerance=0.75)
    if not utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 300, tolerance=0.75):
        raise Exception("循环单次时疑似超过五分钟")
    # 检测F盘DataExport下有没有五分钟内生成的数据
    data_export_path = r"F:\DataExport"
    current_time = time.time()
    found_recent_file = False

    for root, dirs, files in os.walk(data_export_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_creation_time = os.path.getctime(file_path)
            file_modification_time = os.path.getmtime(file_path)
            # 如果文件是在五分钟内创建或修改的
            if current_time - file_creation_time <= 300 or current_time - file_modification_time <= 300:
                found_recent_file = True
                break
        if found_recent_file:
            break

    if not found_recent_file:
        raise Exception(f"{data_export_path}路径下无五分钟内生成的测试数据")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def sjdc_002_01():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(False)
    # 1.【打开】job
    # 2.进入元件编辑界面
    utils.ensure_in_edit_mode()
    utils.is_checked((66,255),(78,267),False)
    utils.is_checked((84,273),(96,285),True)
    # 3.点击【测试整板】
    utils.click_by_png(config.TEST_BOARD)
    if utils.search_symbol(config.QUESTION_MARK, 3):
        pyautogui.press("enter")
    start_time = time.time()
    while utils.search_symbol(config.TESTING_COMPONENT):
        if time.time() - start_time > 300:
            raise Exception("测试元件超过五分钟")
        time.sleep(3)
    if utils.search_symbol(config.QUESTION_MARK, 5):
        raise Exception("出现弹窗提醒是否将该笔离线数据发送到rv")
    time.sleep(3)
    # 4.在rv中查看是否有该笔数据
    utils.check_and_launch_rv()
    utils.check_new_data_in_rv(False)
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def sjdc_002_02():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(False)
    utils.check_output_data_delay(0)
    # 1.【打开】job
    utils.open_program()
    utils.click_by_png(config.PROGRAM_COMPONENT_DARK)
    utils.is_checked((66,255),(78,267),False)
    utils.is_checked((84,273),(96,285),True)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range (3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,20,tolerance=0.75)
    if not utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 300, tolerance=0.75):
        raise Exception("循环单次时疑似超过五分钟")

    # 3.点【停止】--【进入细调】
    if utils.search_symbol(config.QUESTION_MARK, 5):
        raise Exception("测试整板结束后出现弹窗提醒")
    else:
        utils.click_by_png(config.STOP)
        utils.click_by_png(config.TESTING_INTERFACE_ENTER_DETAIL_INTERFACE)
        time.sleep(5)
    # 4.点击【测试整板】
    utils.click_by_png(config.TEST_BOARD)
    if utils.search_symbol(config.QUESTION_MARK, 3):
        pyautogui.press("enter")

    start_time = time.time()
    while utils.search_symbol(config.TESTING_COMPONENT):
        if time.time() - start_time > 300:
            raise Exception("测试元件超过五分钟")
        time.sleep(3)
    if utils.search_symbol(config.QUESTION_MARK, 5):
        raise Exception("出现弹窗提醒是否将该笔离线数据发送到rv")
    time.sleep(3)
    # 5.在rv中查看是否有该笔数据
    utils.check_and_launch_rv()
    utils.check_new_data_in_rv(False)

    utils.close_aoi()

@utils.screenshot_error_to_excel()
def sjdc_002_03():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(False)
    utils.check_output_data_delay(3)
    # 1.【打开】job
    utils.open_program()
    utils.click_by_png(config.PROGRAM_COMPONENT_DARK)
    utils.is_checked((66,255),(78,267),False)
    utils.is_checked((84,273),(96,285),True)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range (3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,20,tolerance=0.75)
    if not utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 300, tolerance=0.75):
        raise Exception("循环单次时疑似超过五分钟")

    # 3.运行结束后倒计时点【细调】
    if utils.search_symbol(config.QUESTION_MARK, 5):
        pyautogui.press("enter")
    else:
        raise Exception("未找到停止进细调弹框")
    time.sleep(5)
    # 4.点击【测试整板】
    utils.click_by_png(config.TEST_BOARD)
    if utils.search_symbol(config.QUESTION_MARK, 3):
        pyautogui.press("enter")
    start_time = time.time()
    while utils.search_symbol(config.TESTING_COMPONENT):
        if time.time() - start_time > 300:
            raise Exception("测试元件超过五分钟")
        time.sleep(3)
    if utils.search_symbol(config.QUESTION_MARK, 5):
        raise Exception("出现弹窗提醒是否将该笔离线数据发送到rv")
    time.sleep(3)
    # 5.在rv中查看是否有该笔数据
    utils.check_and_launch_rv()
    utils.check_new_data_in_rv(False)

    utils.close_aoi()

@utils.screenshot_error_to_excel()
def sjdc_002_04():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(False)
    utils.check_output_data_delay(3)
    # 1.【打开】job
    utils.open_program()
    utils.click_by_png(config.PROGRAM_COMPONENT_DARK)
    utils.is_checked((66,255),(78,267),False)
    utils.is_checked((84,273),(96,285),True)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range (3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,20,tolerance=0.75)
    if not utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 300, tolerance=0.75):
        raise Exception("循环单次时疑似超过五分钟")

    # 3.运行结束后倒计时点【停止】--【进入细调】
    if utils.search_symbol(config.QUESTION_MARK, 5):
        pyautogui.press("enter")
    else:
        raise Exception("未找到停止进细调弹框")
    # 4.点击【测试整板】
    utils.click_by_png(config.TEST_BOARD)
    if utils.search_symbol(config.QUESTION_MARK, 3):
        pyautogui.press("enter")
    start_time = time.time()
    while utils.search_symbol(config.TESTING_COMPONENT):
        if time.time() - start_time > 300:
            raise Exception("测试元件超过五分钟")
        time.sleep(3)
    if utils.search_symbol(config.QUESTION_MARK, 5):
        raise Exception("出现弹窗提醒是否将该笔离线数据发送到rv")
    time.sleep(3)
    # 5.在rv中查看是否有该笔数据
    utils.check_and_launch_rv()    
    utils.check_new_data_in_rv(False)

    utils.close_aoi()

@utils.screenshot_error_to_excel()
def sjdc_002_05():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    # 2.进入元件编辑界面
    utils.ensure_in_edit_mode()
    utils.is_checked((66,255),(78,267),False)
    utils.is_checked((84,273),(96,285),True)
    # 3.点击【测试整板】
    utils.click_by_png(config.TEST_BOARD)
    if utils.search_symbol(config.QUESTION_MARK, 3):
        pyautogui.press("enter")
    start_time = time.time()
    while utils.search_symbol(config.TESTING_COMPONENT):
        if time.time() - start_time > 300:
            raise Exception("测试元件超过五分钟")
        time.sleep(3)

    # 4.弹窗提醒是否将该笔离线数据发送到rv，点【是】
    if not utils.search_symbol(config.QUESTION_MARK, 5):
        raise Exception("未出现弹窗提醒是否将该笔离线数据发送到rv")
    else:
        pyautogui.press("enter")
    time.sleep(3)
    # 5.在rv中查看是否有该笔数据
    utils.check_and_launch_rv() 
    utils.check_new_data_in_rv(True)
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def sjdc_002_06():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(False)
    utils.check_output_data_delay(0)
    # 1.【打开】job
    utils.open_program()
    utils.click_by_png(config.PROGRAM_COMPONENT_DARK)
    utils.is_checked((66,255),(78,267),False)
    utils.is_checked((84,273),(96,285),True)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range (3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,20,tolerance=0.75)
    if not utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 300, tolerance=0.75):
        raise Exception("循环单次时疑似超过五分钟")

    # 3.点【停止】--【进入细调】
    if utils.search_symbol(config.QUESTION_MARK, 5):
        pyautogui.press("enter")
    else:
        raise Exception("未找到停止进细调弹框")
    # 4.点击【测试整板】
    utils.click_by_png(config.TEST_BOARD)
    if utils.search_symbol(config.QUESTION_MARK, 3):
        pyautogui.press("enter")
    start_time = time.time()
    while utils.search_symbol(config.TESTING_COMPONENT):
        if time.time() - start_time > 300:
            raise Exception("测试元件超过五分钟")
        time.sleep(3)
    # 5.弹窗提醒是否将该笔离线数据发送到rv，点【是】
    if not utils.search_symbol(config.QUESTION_MARK, 5):
        raise Exception("未出现弹窗提醒是否将该笔离线数据发送到rv")
    else:
        pyautogui.press("enter")
    time.sleep(3)
    # 6.在rv中查看是否有该笔数据
    utils.check_and_launch_rv() 
    utils.check_new_data_in_rv(True)
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def sjdc_002_07():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(False)
    utils.check_output_data_delay(3)
    # 1.【打开】job
    utils.open_program()
    utils.click_by_png(config.PROGRAM_COMPONENT_DARK)
    utils.is_checked((66,255),(78,267),False)
    utils.is_checked((84,273),(96,285),True)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range (3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,20,tolerance=0.75)
    if not utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 300, tolerance=0.75):
        raise Exception("循环单次时疑似超过五分钟")

    # 3.运行结束后倒计时点【细调】
    if utils.search_symbol(config.QUESTION_MARK, 5):
        pyautogui.press("enter")
    else:
        raise Exception("未找到停止进细调弹框")
    time.sleep(5)
    # 4.点击【测试整板】
    utils.click_by_png(config.TEST_BOARD)
    if utils.search_symbol(config.QUESTION_MARK, 3):
        pyautogui.press("enter")
    start_time = time.time()
    while utils.search_symbol(config.TESTING_COMPONENT):
        if time.time() - start_time > 300:
            raise Exception("测试元件超过五分钟")
        time.sleep(3)
    # 5.弹窗提醒是否将该笔离线数据发送到rv，点【是】
    if not utils.search_symbol(config.QUESTION_MARK, 5):
        raise Exception("未找到弹窗提醒是否将该笔离线数据发送到rv")
    else:
        pyautogui.press("enter")
    time.sleep(3)
    # 6.在rv中查看是否有该笔数据
    utils.check_and_launch_rv() 
    utils.check_new_data_in_rv(True)
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def sjdc_002_08():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    utils.check_output_data_delay(3)
    # 1.【打开】job
    utils.open_program()
    utils.click_by_png(config.PROGRAM_COMPONENT_DARK)
    utils.is_checked((66,255),(78,267),False)
    utils.is_checked((84,273),(96,285),True)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range (3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,20,tolerance=0.75)
    if not utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 300, tolerance=0.75):
        raise Exception("循环单次时疑似超过五分钟")

    # 3.运行结束后倒计时点【停止】--【进入细调】
    if utils.search_symbol(config.QUESTION_MARK, 5):
        pyautogui.press("enter")
    else:
        raise Exception("未找到停止进细调弹框")
    # 4.点击【测试整板】
    utils.click_by_png(config.TEST_BOARD)
    if utils.search_symbol(config.QUESTION_MARK, 3):
        pyautogui.press("enter")
    start_time = time.time()
    while utils.search_symbol(config.TESTING_COMPONENT):
        if time.time() - start_time > 300:
            raise Exception("测试元件超过五分钟")
        time.sleep(3)
    # 5.弹窗提醒是否将该笔离线数据发送到rv，点【是】
    if not utils.search_symbol(config.QUESTION_MARK, 5):
        raise Exception("未找到弹窗提醒是否将该笔离线数据发送到rv")
    else:
        pyautogui.press("enter")
    time.sleep(3)
    # 6.在rv中查看是否有该笔数据
    utils.check_and_launch_rv()
    utils.check_new_data_in_rv(True)

    utils.close_aoi()
@utils.screenshot_error_to_excel()
def sjdc_003_01():
    utils.check_and_launch_aoi()
    old_folder = "F:/DataExport"
    utils.check_output_path(False, old_folder)
    utils.check_use_date_folder(0)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    time.sleep(10)
    # 3.打开输出路径对应的文件夹，查看该job的job名文件夹
    folder_path = f"F:/DataExport"
    if not utils.check_new_data(path=folder_path, name=job_name):
        raise Exception(f"{folder_path}下疑似未生成该笔数据")

    utils.close_aoi()

@utils.screenshot_error_to_excel()
def sjdc_003_02():
    utils.check_and_launch_aoi()
    old_folder = "F:/DataExport"
    utils.check_output_path(False, old_folder)
    utils.check_use_date_folder(3)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.打开输出路径对应的文件夹，查看当天的年份文件夹，在年份文件夹中找到当天的月份文件夹，在月份文件夹中找到当天的日期文件夹，查看该job的job名文件夹
    folder_path = f"F:/DataExport"
    goal_path = f"{folder_path}/{time.strftime('%Y')}/{time.strftime('%m')}/{time.strftime('%d')}"
    if not utils.check_new_data(path=goal_path, name=job_name):
        raise Exception(f"{goal_path}下疑似未生成该笔数据")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def sjdc_003_03():
    utils.check_and_launch_aoi()
    old_folder = "F:/DataExport"
    utils.check_output_path(False, old_folder)
    utils.check_use_date_folder(2)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.打开输出路径对应的文件夹，查看当天的年份文件夹，在年份文件夹中找到当天的月份文件夹，查看该job的job名文件夹
    folder_path = f"F:/DataExport"
    goal_path = f"{folder_path}/{time.strftime('%Y')}/{time.strftime('%m')}"
    if not utils.check_new_data(path=goal_path, name=job_name):
        raise Exception(f"{goal_path}下疑似未生成该笔数据")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def sjdc_003_04():
    utils.check_and_launch_aoi()
    old_folder = "F:/DataExport"
    utils.check_output_path(False, old_folder)
    utils.check_use_date_folder(1)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.打开输出路径对应的文件夹，查看当天的年份文件夹，查看该job的job名文件夹
    folder_path = f"F:/DataExport"
    goal_path = f"{folder_path}/{time.strftime('%Y')}"
    if not utils.check_new_data(path=goal_path, name=job_name):
        raise Exception(f"{goal_path}下疑似未生成该笔数据")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def sjdc_004_01():
    utils.check_and_launch_aoi()
    old_folder = "F:/DataExport"
    utils.check_output_path(False, old_folder)
    utils.check_use_date_folder(0)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range (3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,30,tolerance=0.75)

    if not utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 180, tolerance=0.75):
        logger.error("疑似三分钟都没检测完一块板")
    # 3.打开设置的路径文件夹
    utils.check_new_data(path="F:/DataExport")

@utils.screenshot_error_to_excel()
def sjdc_004_02():
    utils.check_and_launch_aoi()
    old_folder = "F:/DataExport"
    utils.check_output_path(False, old_folder)
    utils.check_use_date_folder(3)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.打开设置的路径文件夹
    utils.check_new_data(path="F:/DataExport", name=f"{datetime.datetime.now():%Y-%m-%d}")

@utils.screenshot_error_to_excel()
def sjdc_004_03():
    utils.check_and_launch_aoi()
    utils.check_use_date_folder(False)
    old_folder = "F:/DataExport"
    new_folder = "F:/DataExport/test"
    utils.check_output_path(True,new_folder)

    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.打开更改前的路径文件夹
    if utils.check_new_data(path=old_folder):
        raise Exception(f"{old_folder}下生成了新数据")
    # 4.打开更改后的路径文件夹
    if not utils.check_new_data(path=new_folder):
        raise Exception(f"{new_folder}下未生成新数据")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def sjdc_004_04():
    utils.check_and_launch_aoi()
    utils.check_use_date_folder(False)
    old_folder = "F:/DataExport"
    new_folder = "F:/DataExport/test"
    utils.check_output_path(True, new_folder)
    os.chmod(new_folder, 0o777)  # 将文件夹权限设置为对所有人可读写执行

    today_date_folder = datetime.now().strftime("%Y-%m-%d")
    for folder in [old_folder, new_folder]:
        path_to_delete = os.path.join(folder, today_date_folder)
        if os.path.exists(path_to_delete):
            shutil.rmtree(path_to_delete)
            logger.info(f"已删除文件夹: {path_to_delete}")
        else:
            logger.info(f"文件夹不存在，无需删除: {path_to_delete}")

    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.打开更改前的路径文件夹
    if utils.check_new_data(path=old_folder, name=f"{datetime.datetime.now():%Y-%m-%d}"):
        raise Exception(f"{old_folder}下生成了年-月-日格式的文件夹")
    # 4.打开更改后的路径文件夹
    if not utils.check_new_data(path=new_folder, name=f"{datetime.datetime.now():%Y-%m-%d}"):
        raise Exception(f"{new_folder}下未生成年-月-日格式的文件夹")
    
    utils.close_aoi()
    

@utils.screenshot_error_to_excel()
def sjdc_005_01():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.查看UI右侧job信息中线体号
    utils.check_line_number_in_ui()
    # 4.在rv中查看
    utils.check_and_launch_rv()
    utils.check_new_data_in_rv(True)

@utils.screenshot_error_to_excel()
def sjdc_005_02():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.查看UI右侧job信息中线体号
    utils.check_line_number_in_ui()
    # 4.在rv中查看
    utils.check_and_launch_rv()
    utils.check_new_data_in_rv(True)

@utils.screenshot_error_to_excel()
def sjdc_006_01():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.记录导出数据时间
    utils.record_export_data_time()

@utils.screenshot_error_to_excel()
def sjdc_006_02():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.记录导出数据时间
    utils.record_export_data_time()

@utils.screenshot_error_to_excel()
def sjdc_006_03():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.记录导出数据时间
    utils.record_export_data_time()

@utils.screenshot_error_to_excel()
def sjdc_007_01():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.在RV查看该笔数据，选择【全部】
    utils.check_and_launch_rv()
    utils.check_new_data_in_rv(True)
    # 4.在SPC查看该笔数据，勾选【良好】
    utils.check_and_launch_spc()
    utils.check_good_data_in_spc()

@utils.screenshot_error_to_excel()
def sjdc_007_02():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.在RV查看该笔数据，选择【全部】
    utils.check_and_launch_rv()
    utils.check_new_data_in_rv(True)
    # 4.在SPC查看该笔数据，勾选【良好】
    utils.check_and_launch_spc()
    utils.check_good_data_in_spc()

@utils.screenshot_error_to_excel()
def sjdc_007_03():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.在RV查看该笔数据，选择【全部】
    utils.check_and_launch_rv()
    utils.check_new_data_in_rv(True)
    # 4.在SPC查看该笔数据，勾选【良好】
    utils.check_and_launch_spc()
    utils.check_good_data_in_spc()

@utils.screenshot_error_to_excel()
def sjdc_007_04():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.【设置】--【硬件设置】--【数据导出配置】--【数据导出配置】--不勾选【只导出NG】和【使用Good\NG分开传输】
    utils.set_data_export_config(False, False)
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在RV查看该笔数据，选择【全部】，在SPC查看该笔数据，勾选【良好】
    utils.check_and_launch_rv()
    utils.check_new_data_in_rv(True)
    utils.check_and_launch_spc()
    utils.check_good_data_in_spc()
    # 5.【设置】--【硬件设置】--【数据导出配置】--【数据导出配置】--勾选【使用Good\NG分开传输】
    utils.set_data_export_config(True, False)
    # 6.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 7.在RV查看该笔数据，选择【全部】，在SPC查看该笔数据，勾选【良好】
    utils.check_and_launch_rv()
    utils.check_new_data_in_rv(True)
    utils.check_and_launch_spc()
    utils.check_good_data_in_spc()
    # 8.【设置】--【硬件设置】--【数据导出配置】--【数据导出配置】--勾选【只导出NG】
    utils.set_data_export_config(False, True)
    # 9.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 10.在RV查看该笔数据，选择【全部】，在SPC查看该笔数据，勾选【良好】
    utils.check_and_launch_rv()
    utils.check_new_data_in_rv(True)
    utils.check_and_launch_spc()
    utils.check_good_data_in_spc()

@utils.screenshot_error_to_excel()
def sjdc_008_01():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)

@utils.screenshot_error_to_excel()
def sjdc_008_02():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)

@utils.screenshot_error_to_excel()
def sjdc_008_03():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)

@utils.screenshot_error_to_excel()
def sjdc_008_04():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)

@utils.screenshot_error_to_excel()
def sjdc_009_01():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【设置】--【硬件设置】--【数据导出设置】--【数据导出配置】-- 主机，可以查看主机ip
    utils.set_data_export_config_host()
    utils.check_host_ip()

@utils.screenshot_error_to_excel()
def sjdc_010_01():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.在rv中查看该笔数据
    utils.check_and_launch_rv()
    utils.check_new_data_in_rv(True)

@utils.screenshot_error_to_excel()
def sjdc_010_02():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.在rv中查看该笔数据
    utils.check_and_launch_rv()
    utils.check_new_data_in_rv(True)

@utils.screenshot_error_to_excel()
def sjdc_010_03():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.在rv中查看该笔数据
    utils.check_and_launch_rv()
    utils.check_new_data_in_rv(True)

@utils.screenshot_error_to_excel()
def sjdc_010_04():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.在rv中查看该笔数据
    utils.check_and_launch_rv()
    utils.check_new_data_in_rv(True)

@utils.screenshot_error_to_excel()
def sjdc_010_05():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.在dv复判界面中复判该笔数据
    utils.check_and_launch_dv()
    utils.review_data_in_dv()
    # 4.在rv中查看该笔数据
    utils.check_and_launch_rv()
    utils.check_new_data_in_rv(True)

@utils.screenshot_error_to_excel()
def sjdc_010_06():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.在dv复判界面中复判该笔数据
    utils.check_and_launch_dv()
    utils.review_data_in_dv()
    # 4.在rv中查看该笔数据
    utils.check_and_launch_rv()
    utils.check_new_data_in_rv(True)

@utils.screenshot_error_to_excel()
def sjdc_010_07():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】一个良好板的job或关闭除条码检测外的全部算法（【设置】--【硬件设置】--【演算法配置】--【所有算法】，所有算法都勾选后，取消勾选【条码检测】）
    utils.open_good_board_job_or_disable_algorithms_except_barcode()
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.在rv中查看该笔数据
    utils.check_and_launch_rv()
    utils.check_new_data_in_rv(True)

@utils.screenshot_error_to_excel()
def sjdc_010_08():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.在dv复判界面中复判该笔数据为通过板
    utils.check_and_launch_dv()
    utils.review_data_in_dv_as_pass()
    # 4.在rv中查看该笔数据
    utils.check_and_launch_rv()
    utils.check_new_data_in_rv(True)

@utils.screenshot_error_to_excel()
def sjdc_010_09():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.在dv复判界面中复判该笔数据为不良板
    utils.check_and_launch_dv()
    utils.review_data_in_dv_as_fail()
    # 4.在rv中查看该笔数据
    utils.check_and_launch_rv()
    utils.check_new_data_in_rv(True)

@utils.screenshot_error_to_excel()
def sjdc_011_01():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【设置】--【硬件设置】--【数据导出设置】--【数据导出配置】-- rv输出，可以查看输出rv的ip
    utils.set_data_export_config_rv_output()
    utils.check_rv_output_ip()

@utils.screenshot_error_to_excel()
def sjdc_012_01():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.在文件夹中查看当前笔数据
    utils.check_data_in_folder()

@utils.screenshot_error_to_excel()
def sjdc_012_02():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.打开输出路径对应的文件夹，查看该job的job名文件夹
    utils.open_output_path_folder()
    utils.check_job_name_folder()

@utils.screenshot_error_to_excel()
def sjdc_012_03():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.打开输出路径对应的文件夹，查看该job的job名文件夹
    utils.open_output_path_folder()
    utils.check_job_name_folder()

@utils.screenshot_error_to_excel()
def sjdc_013_01():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.下拉框更改【影像压缩】为100%
    utils.change_image_compression_to_100()
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\fov）中查看导出的图片属性
    utils.check_exported_image_properties("F:\\DataExport\\job名称\\最近一片数据\\fov")

@utils.screenshot_error_to_excel()
def sjdc_013_02():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.下拉框更改【影像压缩】为100%
    utils.change_image_compression_to_100()
    # 4.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\fov）中查看导出的图片属性
    utils.check_exported_image_properties("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\fov")

@utils.screenshot_error_to_excel()
def sjdc_013_03():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.下拉框更改【影像压缩】为非100%
    utils.change_image_compression_to_non_100()
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\fov）中查看导出的图片属性
    utils.check_exported_image_properties("F:\\DataExport\\job名称\\最近一片数据\\fov")

@utils.screenshot_error_to_excel()
def sjdc_013_04():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.下拉框更改【影像压缩】为非100%
    utils.change_image_compression_to_non_100()
    # 4.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\fov）中查看导出的图片属性属性
    utils.check_exported_image_properties("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\fov")

@utils.screenshot_error_to_excel()
def sjdc_013_05():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.下拉框更改【影像压缩】为100%
    utils.change_image_compression_to_100()
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\fov）中查看导出的图片属性
    utils.check_exported_image_properties("F:\\DataExport\\job名称\\最近一片数据\\fov")

@utils.screenshot_error_to_excel()
def sjdc_013_06():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.下拉框更改【影像压缩】为100%
    utils.change_image_compression_to_100()
    # 4.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\fov）中查看导出的图片属性
    utils.check_exported_image_properties("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\fov")

@utils.screenshot_error_to_excel()
def sjdc_013_07():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.下拉框更改【影像压缩】为非100%
    utils.change_image_compression_to_non_100()
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\fov）中查看导出的图片属性
    utils.check_exported_image_properties("F:\\DataExport\\job名称\\最近一片数据\\fov")

@utils.screenshot_error_to_excel()
def sjdc_013_08():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.下拉框更改【影像压缩】为非100%
    utils.change_image_compression_to_non_100()
    # 4.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\fov）中查看导出的图片属性属性
    utils.check_exported_image_properties("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\fov")

@utils.screenshot_error_to_excel()
def sjdc_014_01():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.下拉框更改【影像质量】为100%
    utils.change_image_quality_to_100()
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\fov）中查看导出的图片属性
    utils.check_exported_image_properties("F:\\DataExport\\job名称\\最近一片数据\\fov")

@utils.screenshot_error_to_excel()
def sjdc_014_02():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.下拉框更改【影像质量】为100%
    utils.change_image_quality_to_100()
    # 4.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\fov）中查看导出的图片属性
    utils.check_exported_image_properties("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\fov")

@utils.screenshot_error_to_excel()
def sjdc_014_03():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.下拉框更改【影像质量】为非100%
    utils.change_image_quality_to_non_100()
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\fov）中查看导出的图片属性
    utils.check_exported_image_properties("F:\\DataExport\\job名称\\最近一片数据\\fov")

@utils.screenshot_error_to_excel()
def sjdc_014_04():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.下拉框更改【影像质量】为非100%
    utils.change_image_quality_to_non_100()
    # 4.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\fov）中查看导出的图片属性
    utils.check_exported_image_properties("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\fov")

@utils.screenshot_error_to_excel()
def sjdc_014_05():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.下拉框更改【影像质量】为100%
    utils.change_image_quality_to_100()
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\fov）中查看导出的图片属性
    utils.check_exported_image_properties("F:\\DataExport\\job名称\\最近一片数据\\fov")

@utils.screenshot_error_to_excel()
def sjdc_014_06():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.下拉框更改【影像质量】为100%
    utils.change_image_quality_to_100()
    # 4.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\fov）中查看导出的图片属性
    utils.check_exported_image_properties("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\fov")

@utils.screenshot_error_to_excel()
def sjdc_014_07():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.下拉框更改【影像质量】为非100%
    utils.change_image_quality_to_non_100()
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\fov）中查看导出的图片属性
    utils.check_exported_image_properties("F:\\DataExport\\job名称\\最近一片数据\\fov")

@utils.screenshot_error_to_excel()
def sjdc_014_08():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.下拉框更改【影像质量】为非100%
    utils.change_image_quality_to_non_100()
    # 4.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\fov）中查看导出的图片属性
    utils.check_exported_image_properties("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\fov")

@utils.screenshot_error_to_excel()
def sjdc_015_01():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.更改【影像最小像素】的值
    utils.change_minimum_pixel_value()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\FOV）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\FOV")

@utils.screenshot_error_to_excel()
def sjdc_015_02():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.更改【影像最小像素】的值
    utils.change_minimum_pixel_value()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\FOV）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\FOV")

@utils.screenshot_error_to_excel()
def sjdc_015_03():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.更改【影像最小像素】的值
    utils.change_minimum_pixel_value()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\FOV）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\FOV")

@utils.screenshot_error_to_excel()
def sjdc_015_04():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.更改【影像最小像素】的值
    utils.change_minimum_pixel_value()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\FOV）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\FOV")

@utils.screenshot_error_to_excel()
def sjdc_015_05():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.更改【影像最小像素】的值
    utils.change_minimum_pixel_value()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\FOV）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\FOV")

@utils.screenshot_error_to_excel()
def sjdc_015_06():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.更改【影像最小像素】的值
    utils.change_minimum_pixel_value()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\FOV）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\FOV")

@utils.screenshot_error_to_excel()
def sjdc_015_07():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.更改【影像最小像素】的值
    utils.change_minimum_pixel_value()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\FOV）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\FOV")

@utils.screenshot_error_to_excel()
def sjdc_015_08():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.更改【影像最小像素】的值
    utils.change_minimum_pixel_value()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\FOV）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\FOV")

@utils.screenshot_error_to_excel()
def sjdc_016_01():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.在文件夹中查看当前笔数据
    utils.check_data_in_folder()

@utils.screenshot_error_to_excel()
def sjdc_016_02():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.打开输出路径对应的文件夹，查看该job的job名文件夹
    utils.open_output_path_folder()
    utils.check_job_name_folder()

@utils.screenshot_error_to_excel()
def sjdc_017_01():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.打开输出路径对应的文件夹，查看该job的job名文件夹
    utils.open_output_path_folder()
    utils.check_job_name_folder()

@utils.screenshot_error_to_excel()
def sjdc_017_02():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.打开输出路径对应的文件夹，查看该job的job名文件夹
    utils.open_output_path_folder()
    utils.check_job_name_folder()

@utils.screenshot_error_to_excel()
def sjdc_018_01():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.下拉框更改【影像压缩】为100%
    utils.change_image_compression_to_100()
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\Component）中查看导出的图片属性
    utils.check_exported_image_properties("F:\\DataExport\\job名称\\最近一片数据\\Component")

@utils.screenshot_error_to_excel()
def sjdc_018_02():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.下拉框更改【影像压缩】为100%
    utils.change_image_compression_to_100()
    # 4.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component）中查看导出的图片属性
    utils.check_exported_image_properties("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component")

@utils.screenshot_error_to_excel()
def sjdc_018_03():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.下拉框更改【影像压缩】为非100%
    utils.change_image_compression_to_non_100()
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\Component）中查看导出的图片属性
    utils.check_exported_image_properties("F:\\DataExport\\job名称\\最近一片数据\\Component")

@utils.screenshot_error_to_excel()
def sjdc_018_04():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.下拉框更改【影像压缩】为非100%
    utils.change_image_compression_to_non_100()
    # 4.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component）中查看导出的图片属性属性
    utils.check_exported_image_properties("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component")

@utils.screenshot_error_to_excel()
def sjdc_018_05():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.下拉框更改【影像压缩】为100%
    utils.change_image_compression_to_100()
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\Component）中查看导出的图片属性
    utils.check_exported_image_properties("F:\\DataExport\\job名称\\最近一片数据\\Component")

@utils.screenshot_error_to_excel()
def sjdc_018_06():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.下拉框更改【影像压缩】为100%
    utils.change_image_compression_to_100()
    # 4.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component）中查看导出的图片属性
    utils.check_exported_image_properties("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component")

@utils.screenshot_error_to_excel()
def sjdc_018_07():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.下拉框更改【影像压缩】为非100%
    utils.change_image_compression_to_non_100()
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\Component）中查看导出的图片属性
    utils.check_exported_image_properties("F:\\DataExport\\job名称\\最近一片数据\\Component")

@utils.screenshot_error_to_excel()
def sjdc_018_08():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.下拉框更改【影像压缩】为非100%
    utils.change_image_compression_to_non_100()
    # 4.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component）中查看导出的图片属性属性
    utils.check_exported_image_properties("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component")

@utils.screenshot_error_to_excel()
def sjdc_018_09():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.下拉框更改【影像质量】为100%
    utils.change_image_quality_to_100()
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\Component）中查看导出的图片属性
    utils.check_exported_image_properties("F:\\DataExport\\job名称\\最近一片数据\\Component")

@utils.screenshot_error_to_excel()
def sjdc_018_10():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.下拉框更改【影像质量】为100%
    utils.change_image_quality_to_100()
    # 4.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component）中查看导出的图片属性
    utils.check_exported_image_properties("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component")

@utils.screenshot_error_to_excel()
def sjdc_018_11():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.下拉框更改【影像质量】为非100%
    utils.change_image_quality_to_non_100()
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\Component）中查看导出的图片属性
    utils.check_exported_image_properties("F:\\DataExport\\job名称\\最近一片数据\\Component")

@utils.screenshot_error_to_excel()
def sjdc_018_12():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.下拉框更改【影像质量】为非100%
    utils.change_image_quality_to_non_100()
    # 4.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component）中查看导出的图片属性
    utils.check_exported_image_properties("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component")

@utils.screenshot_error_to_excel()
def sjdc_018_13():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.下拉框更改【影像质量】为100%
    utils.change_image_quality_to_100()
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\Component）中查看导出的图片属性
    utils.check_exported_image_properties("F:\\DataExport\\job名称\\最近一片数据\\Component")

@utils.screenshot_error_to_excel()
def sjdc_018_14():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.下拉框更改【影像质量】为100%
    utils.change_image_quality_to_100()
    # 4.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component）中查看导出的图片属性
    utils.check_exported_image_properties("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component")

@utils.screenshot_error_to_excel()
def sjdc_018_15():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.下拉框更改【影像质量】为非100%
    utils.change_image_quality_to_non_100()
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\Component）中查看导出的图片属性
    utils.check_exported_image_properties("F:\\DataExport\\job名称\\最近一片数据\\Component")

@utils.screenshot_error_to_excel()
def sjdc_018_16():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.下拉框更改【影像质量】为非100%
    utils.change_image_quality_to_non_100()
    # 4.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component）中查看导出的图片属性
    utils.check_exported_image_properties("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component")

@utils.screenshot_error_to_excel()
def sjdc_018_17():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.更改【影像最小像素】的值
    utils.change_minimum_pixel_value()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\Component）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\Component")

@utils.screenshot_error_to_excel()
def sjdc_018_18():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.更改【影像最小像素】的值
    utils.change_minimum_pixel_value()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component")

@utils.screenshot_error_to_excel()
def sjdc_018_19():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.更改【影像最小像素】的值
    utils.change_minimum_pixel_value()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\Component）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\Component")

@utils.screenshot_error_to_excel()
def sjdc_018_20():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.更改【影像最小像素】的值
    utils.change_minimum_pixel_value()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component")

@utils.screenshot_error_to_excel()
def sjdc_018_21():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.更改【影像最小像素】的值
    utils.change_minimum_pixel_value()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\Component）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\Component")

@utils.screenshot_error_to_excel()
def sjdc_018_22():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.更改【影像最小像素】的值
    utils.change_minimum_pixel_value()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component")

@utils.screenshot_error_to_excel()
def sjdc_018_23():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.更改【影像最小像素】的值
    utils.change_minimum_pixel_value()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\Component）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\Component")

@utils.screenshot_error_to_excel()
def sjdc_018_24():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.更改【影像最小像素】的值
    utils.change_minimum_pixel_value()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component")

@utils.screenshot_error_to_excel()
def sjdc_019_01():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component")

@utils.screenshot_error_to_excel()
def sjdc_019_02():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component")

@utils.screenshot_error_to_excel()
def sjdc_019_03():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component")

@utils.screenshot_error_to_excel()
def sjdc_019_04():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component")

@utils.screenshot_error_to_excel()
def sjdc_019_05():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component")

@utils.screenshot_error_to_excel()
def sjdc_020_01():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.在文件夹（F:\DataExport\job名称\最近一片数据\Component）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\Component")

@utils.screenshot_error_to_excel()
def sjdc_020_02():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.在文件夹（F:\DataExport\job名称\最近一片数据\Component）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\Component")

@utils.screenshot_error_to_excel()
def sjdc_020_03():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.在文件夹（F:\DataExport\job名称\最近一片数据\Component）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\Component")

@utils.screenshot_error_to_excel()
def sjdc_020_04():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.【设置】--【硬件设置】--【数据导出配置】--【数据导出配置】--【元件影像输出】--【扩展区域】--【最大】设置的比百分比后的值大
    utils.set_component_image_output_max_larger_than_percentage()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\Component）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\Component")

@utils.screenshot_error_to_excel()
def sjdc_020_05():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.【设置】--【硬件设置】--【数据导出配置】--【数据导出配置】--【元件影像输出】--【扩展区域】--【最大】设置的比百分比后的值小
    utils.set_component_image_output_max_smaller_than_percentage()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\Component）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\Component")

@utils.screenshot_error_to_excel()
def sjdc_021_01():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.检测两个ng元件，一个元件有3d算法，一个元件没有
    utils.detect_two_ng_components_one_with_3d_one_without()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component\ng）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component\\ng")

@utils.screenshot_error_to_excel()
def sjdc_021_02():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.检测两个ng元件，一个元件有3d算法，一个元件没有
    utils.detect_two_ng_components_one_with_3d_one_without()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component\ng）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component\\ng")

@utils.screenshot_error_to_excel()
def sjdc_021_03():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.检测两个ng元件，一个元件有3d算法，一个元件没有
    utils.detect_two_ng_components_one_with_3d_one_without()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\Component\ng）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\Component\\ng")

@utils.screenshot_error_to_excel()
def sjdc_021_04():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.检测两个ng元件，一个元件有3d算法，一个元件没有
    utils.detect_two_ng_components_one_with_3d_one_without()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\Component\ng）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\Component\\ng")

@utils.screenshot_error_to_excel()
def sjdc_021_05():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.检测两个good元件，一个元件有3d算法，一个元件没有
    utils.detect_two_good_components_one_with_3d_one_without()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component\good）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component\\good")

@utils.screenshot_error_to_excel()
def sjdc_021_06():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.检测两个good元件，一个元件有3d算法，一个元件没有
    utils.detect_two_good_components_one_with_3d_one_without()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component\good）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component\\good")

@utils.screenshot_error_to_excel()
def sjdc_021_07():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.检测两个good元件，一个元件有3d算法，一个元件没有
    utils.detect_two_good_components_one_with_3d_one_without()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\Component\good）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\Component\\good")

@utils.screenshot_error_to_excel()
def sjdc_021_08():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.检测两个good元件，一个元件有3d算法，一个元件没有
    utils.detect_two_good_components_one_with_3d_one_without()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\Component\good）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\Component\\good")

@utils.screenshot_error_to_excel()
def sjdc_022_01():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.只检测一个元件，该元件不同窗口的光源设置不一致，且部分ng部分good
    utils.detect_single_component_with_inconsistent_light_settings()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component\ng）中查看导出的图片中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component\\ng")

@utils.screenshot_error_to_excel()
def sjdc_022_02():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.只检测一个元件，该元件不同窗口的光源设置不一致，且部分ng部分good
    utils.detect_single_component_with_inconsistent_light_settings()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component\ng）中查看导出的图片中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component\\ng")

@utils.screenshot_error_to_excel()
def sjdc_022_03():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.只检测一个元件，该元件不同窗口的光源设置不一致，且部分ng部分good
    utils.detect_single_component_with_inconsistent_light_settings()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\Component\ng）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\Component\\ng")

@utils.screenshot_error_to_excel()
def sjdc_022_04():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.只检测一个元件，该元件不同窗口的光源设置不一致，且部分ng部分good
    utils.detect_single_component_with_inconsistent_light_settings()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\Component\ng）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\Component\\ng")

@utils.screenshot_error_to_excel()
def sjdc_023_01():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.检测两个good元件，一个元件有3d算法，一个元件没有
    utils.detect_two_good_components_one_with_3d_one_without()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component\good）中查看导出的图片中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component\\good")

@utils.screenshot_error_to_excel()
def sjdc_023_02():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.检测两个good元件，一个元件有3d算法，一个元件没有
    utils.detect_two_good_components_one_with_3d_one_without()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component\good）中查看导出的图片中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component\\good")

@utils.screenshot_error_to_excel()
def sjdc_023_03():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.检测两个good元件，一个元件有3d算法，一个元件没有
    utils.detect_two_good_components_one_with_3d_one_without()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\Component\good）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\Component\\good")

@utils.screenshot_error_to_excel()
def sjdc_023_04():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.检测两个good元件，一个元件有3d算法，一个元件没有
    utils.detect_two_good_components_one_with_3d_one_without()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\Component\good）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\Component\\good")

@utils.screenshot_error_to_excel()
def sjdc_023_05():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.检测两个ng元件，一个元件有3d算法，一个元件没有
    utils.detect_two_ng_components_one_with_3d_one_without()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component\ng）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component\\ng")

@utils.screenshot_error_to_excel()
def sjdc_023_06():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.检测两个ng元件，一个元件有3d算法，一个元件没有
    utils.detect_two_ng_components_one_with_3d_one_without()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\Component\ng）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\Component\\ng")

@utils.screenshot_error_to_excel()
def sjdc_024_01():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.检测good元件
    utils.detect_good_component()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component\good）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component\\good")

@utils.screenshot_error_to_excel()
def sjdc_024_02():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.检测good元件
    utils.detect_good_component()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component\good）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component\\good")

@utils.screenshot_error_to_excel()
def sjdc_024_03():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.检测good元件
    utils.detect_good_component()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component\good）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component\\good")

@utils.screenshot_error_to_excel()
def sjdc_024_04():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.检测good元件
    utils.detect_good_component()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component\good）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component\\good")

@utils.screenshot_error_to_excel()
def sjdc_024_05():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.检测good元件
    utils.detect_good_component()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\Component\good）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\Component\\good")

@utils.screenshot_error_to_excel()
def sjdc_024_06():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.检测good元件
    utils.detect_good_component()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\Component\good）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\Component\\good")

@utils.screenshot_error_to_excel()
def sjdc_024_07():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.检测good元件
    utils.detect_good_component()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\Component\good）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\Component\\good")

@utils.screenshot_error_to_excel()
def sjdc_024_08():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.检测good元件
    utils.detect_good_component()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\Component\good）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\Component\\good")

@utils.screenshot_error_to_excel()
def sjdc_025_01():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.检测ng元件
    utils.detect_ng_component()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component\ng）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component\\ng")

@utils.screenshot_error_to_excel()
def sjdc_025_02():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.检测ng元件
    utils.detect_ng_component()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component\ng）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component\\ng")

@utils.screenshot_error_to_excel()
def sjdc_025_03():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.检测ng元件
    utils.detect_ng_component()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component\ng）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component\\ng")

@utils.screenshot_error_to_excel()
def sjdc_025_04():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.检测ng元件
    utils.detect_ng_component()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component\ng）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component\\ng")

@utils.screenshot_error_to_excel()
def sjdc_025_05():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.检测ng元件
    utils.detect_ng_component()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component\ng）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component\\ng")

@utils.screenshot_error_to_excel()
def sjdc_025_06():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.检测ng元件
    utils.detect_ng_component()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component\ng）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component\\ng")

@utils.screenshot_error_to_excel()
def sjdc_025_07():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.检测ng元件
    utils.detect_ng_component()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component\ng）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component\\ng")

@utils.screenshot_error_to_excel()
def sjdc_025_08():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.检测ng元件
    utils.detect_ng_component()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component\ng）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component\\ng")

@utils.screenshot_error_to_excel()
def sjdc_025_09():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.检测ng元件
    utils.detect_ng_component()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\Component\ng）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\Component\\ng")

@utils.screenshot_error_to_excel()
def sjdc_025_10():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.检测ng元件
    utils.detect_ng_component()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\Component\ng）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\Component\\ng")

@utils.screenshot_error_to_excel()
def sjdc_025_11():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.检测ng元件
    utils.detect_ng_component()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\Component\ng）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\Component\\ng")

@utils.screenshot_error_to_excel()
def sjdc_025_12():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.检测ng元件
    utils.detect_ng_component()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\Component\ng）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\Component\\ng")

@utils.screenshot_error_to_excel()
def sjdc_025_13():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.检测ng元件
    utils.detect_ng_component()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\Component\ng）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\Component\\ng")

@utils.screenshot_error_to_excel()
def sjdc_025_14():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.检测ng元件
    utils.detect_ng_component()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\Component\ng）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\Component\\ng")

@utils.screenshot_error_to_excel()
def sjdc_025_15():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.检测ng元件
    utils.detect_ng_component()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\Component\ng）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\Component\\ng")

@utils.screenshot_error_to_excel()
def sjdc_025_16():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.检测ng元件
    utils.detect_ng_component()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\Component\ng）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\Component\\ng")

@utils.screenshot_error_to_excel()
def sjdc_025_17():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.检测good元件
    utils.detect_good_component()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component\good）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component\\good")

@utils.screenshot_error_to_excel()
def sjdc_025_18():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.检测good元件
    utils.detect_good_component()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\Component\good）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\Component\\good")

@utils.screenshot_error_to_excel()
def sjdc_026_01():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component\good）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component\\good")

@utils.screenshot_error_to_excel()
def sjdc_026_02():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component\good）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component\\good")

@utils.screenshot_error_to_excel()
def sjdc_026_03():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component\good）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component\\good")

@utils.screenshot_error_to_excel()
def sjdc_026_04():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.在文件夹（F:\DataExport\job名称\最近一片数据\Component\good）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\Component\\good")

@utils.screenshot_error_to_excel()
def sjdc_026_05():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.在文件夹（F:\DataExport\job名称\最近一片数据\Component\good）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\Component\\good")

@utils.screenshot_error_to_excel()
def sjdc_026_06():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.在文件夹（F:\DataExport\job名称\最近一片数据\Component\good）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\Component\\good")

@utils.screenshot_error_to_excel()
def sjdc_027_01():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component")

@utils.screenshot_error_to_excel()
def sjdc_027_02():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.在文件夹（F:\DataExport\job名称\最近一片数据\Component）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\Component")

@utils.screenshot_error_to_excel()
def sjdc_028_01():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component\ng）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component\\ng")

@utils.screenshot_error_to_excel()
def sjdc_028_02():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component\ng）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component\\ng")

@utils.screenshot_error_to_excel()
def sjdc_028_03():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component\ng）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component\\ng")

@utils.screenshot_error_to_excel()
def sjdc_028_04():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.在文件夹（F:\DataExport\job名称\最近一片数据\Component\ng）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\Component\\ng")

@utils.screenshot_error_to_excel()
def sjdc_028_05():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.在文件夹（F:\DataExport\job名称\最近一片数据\Component\ng）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\Component\\ng")

@utils.screenshot_error_to_excel()
def sjdc_028_06():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 获取job名
    utils.click_by_png(config.SAVE_AS_JOB)
    job_name = utils.read_text(800,540)
    utils.click_by_png(config.CANCEL)
    time.sleep(3)
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.在文件夹（F:\DataExport\job名称\最近一片数据\Component\ng）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\Component\\ng")

@utils.screenshot_error_to_excel()
def sjdc_029_01():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.【运行】该程式，在弹出dv界面后复判全部不良
    utils.click_by_png(config.PLAY)
    utils.review_all_ng_in_dv()
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 3.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component\ng）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component\\ng")

@utils.screenshot_error_to_excel()
def sjdc_029_02():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.【运行】该程式，在弹出dv界面后复判全部不良
    utils.click_by_png(config.PLAY)
    utils.review_all_ng_in_dv()
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 3.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component\ng）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component\\ng")

@utils.screenshot_error_to_excel()
def sjdc_029_03():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.【运行】该程式，在弹出dv界面后复判全部不良
    utils.click_by_png(config.PLAY)
    utils.review_all_ng_in_dv()
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 3.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component\ng）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component\\ng")

@utils.screenshot_error_to_excel()
def sjdc_029_04():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.【运行】该程式，在弹出dv界面后复判全部不良
    utils.click_by_png(config.PLAY)
    utils.review_all_ng_in_dv()
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 3.在文件夹（F:\DataExport\job名称\最近一片数据\Component\ng）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\Component\\ng")

@utils.screenshot_error_to_excel()
def sjdc_029_05():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.【运行】该程式，在弹出dv界面后复判全部不良
    utils.click_by_png(config.PLAY)
    utils.review_all_ng_in_dv()
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 3.在文件夹（F:\DataExport\job名称\最近一片数据\Component\ng）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\Component\\ng")

@utils.screenshot_error_to_excel()
def sjdc_029_06():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.【运行】该程式，在弹出dv界面后复判全部不良
    utils.click_by_png(config.PLAY)
    utils.review_all_ng_in_dv()
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 3.在文件夹（F:\DataExport\job名称\最近一片数据\Component\ng）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\Component\\ng")

@utils.screenshot_error_to_excel()
def sjdc_030_01():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.勾选任意光源（单个或多个均可）
    utils.select_any_light_source()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component\good）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component\\good")

@utils.screenshot_error_to_excel()
def sjdc_030_02():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.勾选任意光源（单个或多个均可）
    utils.select_any_light_source()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\Component\good）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\Component\\good")

@utils.screenshot_error_to_excel()
def sjdc_030_03():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.勾选任意光源（单个或多个均可）
    utils.select_any_light_source()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component\ng）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component\\ng")

@utils.screenshot_error_to_excel()
def sjdc_030_04():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.勾选任意光源（单个或多个均可）
    utils.select_any_light_source()
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\Component\ng）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\Component\\ng")

@utils.screenshot_error_to_excel()
def sjdc_031_01():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.右键【程式元件】--【board】处--【强制按料号导出影像】--勾选一个元件测试结果均为good的料号--在光源选择处选择该料号要强制导出的光源--点【是】
    utils.force_export_image_by_part_number("good")
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component\good）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component\\good")

@utils.screenshot_error_to_excel()
def sjdc_031_02():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.右键【程式元件】--【board】处--【强制按料号导出影像】--勾选一个元件测试结果均为good的料号--在光源选择处选择该料号要强制导出的光源--点【是】
    utils.force_export_image_by_part_number("good")
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\Component\good）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\Component\\good")

@utils.screenshot_error_to_excel()
def sjdc_031_03():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.右键【程式元件】--【board】处--【强制按料号导出影像】--勾选一个元件测试结果均为ng的料号--在光源选择处选择该料号要强制导出的光源--点【是】
    utils.force_export_image_by_part_number("ng")
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\年\月\日\job名称\最近一片数据\Component\ng）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\年\\月\\日\\job名称\\最近一片数据\\Component\\ng")

@utils.screenshot_error_to_excel()
def sjdc_031_04():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job
    utils.open_program()
    # 2.右键【程式元件】--【board】处--【强制按料号导出影像】--勾选一个元件测试结果均为ng的料号--在光源选择处选择该料号要强制导出的光源--点【是】
    utils.force_export_image_by_part_number("ng")
    # 3.【运行】该程式
    utils.click_by_png(config.PLAY)
    for _ in range(3):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    # 4.在文件夹（F:\DataExport\job名称\最近一片数据\Component\ng）中查看导出的图片
    utils.check_exported_image_in_folder("F:\\DataExport\\job名称\\最近一片数据\\Component\\ng")
@utils.screenshot_error_to_excel()
def sjdc_032_01():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job，右键【程式元件】--【board】处--【导出DJB选项】--勾选一个元件测试结果均为good的料号--点【是】
    utils.export_djb_option("good")
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.在文件夹（D:\EYAOI\BIN\DebugDBJFileExport）中查看导出的djb
    utils.check_exported_djb_in_folder("D:\\EYAOI\\BIN\\DebugDBJFileExport")

@utils.screenshot_error_to_excel()
def sjdc_032_02():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job，右键【程式元件】--【board】处--【导出DJB选项】--勾选一个元件测试结果均为good的料号--点【是】
    utils.export_djb_option("good")
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.在文件夹（D:\EYAOI\BIN\DebugDBJFileExport）中查看导出的djb
    utils.check_exported_djb_in_folder("D:\\EYAOI\\BIN\\DebugDBJFileExport")

@utils.screenshot_error_to_excel()
def sjdc_032_03():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job，右键【程式元件】--【board】处--【导出DJB选项】--勾选一个元件测试结果均为ng的料号--点【是】
    utils.export_djb_option("ng")
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.在文件夹（D:\EYAOI\BIN\DebugDBJFileExport）中查看导出的djb
    utils.check_exported_djb_in_folder("D:\\EYAOI\\BIN\\DebugDBJFileExport")

@utils.screenshot_error_to_excel()
def sjdc_032_04():
    utils.check_and_launch_aoi()
    utils.check_offline_send_data(True)
    # 1.【打开】job，右键【程式元件】--【board】处--【导出DJB选项】--勾选一个元件测试结果均为ng的料号--点【是】
    utils.export_djb_option("ng")
    # 2.【运行】该程式
    utils.click_by_png(config.PLAY, 2)
    for _ in range (4):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(3)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,100,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    # 3.在文件夹（D:\EYAOI\BIN\DebugDBJFileExport）中查看导出的djb
    utils.check_exported_djb_in_folder("D:\\EYAOI\\BIN\\DebugDBJFileExport")