import datetime
from loguru import logger
import pyautogui
import utils,config
import tkinter as tk
from tkinter import messagebox
import time
import psutil
import pandas as pd
import matplotlib.pyplot as plt
import re
import os
import threading
from openpyxl import Workbook, load_workbook
from openpyxl.chart import LineChart, Reference

# 获取当前脚本或可执行文件所在目录
base_dir = os.path.dirname(os.path.abspath(__file__))

# 获取base_dir的上级的上级文件夹
parent_dir = os.path.dirname(os.path.dirname(base_dir))

# 构建 Excel 文件的路径
excel_path = os.path.join(parent_dir, 'offline_test_results.xlsx')
logger.debug(f"excel_path: {excel_path}")

@utils.screenshot_error_to_excel()
def launch_rv():
    utils.check_and_launch_rv()

@utils.screenshot_error_to_excel()
def launch_spc():
    utils.check_and_launch_spc()
@utils.screenshot_error_to_excel()
def check_close_all_algs():
    utils.check_close_all_algs()

@utils.screenshot_error_to_excel()
def write_text_textbox():
    utils.write_text_textbox(config.RV_PASSWORD, write_content=config.RV_PASSWORD_TEXT)
@utils.screenshot_error_to_excel()
def delete_bad_mark():
    utils.delete_bad_mark()
timeout_seconds = 600

def parse_log_file(log_file_path):
    times = []
    alg_cal_times = []

    try:
        with open(log_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                match = re.search(r'AlgCalTime\(S\):([\d.]+)', line)
                if match:
                    time_str = line.split(' ')[0]  # 假设时间在行首
                    alg_cal_time = float(match.group(1))
                    
                    # 将时间字符串转换为datetime对象
                    current_time = datetime.datetime.strptime(time_str, '%H:%M:%S.%f')

                    times.append(current_time.strftime('%Y-%m-%d %H:%M:%S'))
                    alg_cal_times.append(alg_cal_time)
                    logger.debug(f"匹配成功: 时间={times[-1]}, AlgCalTime={alg_cal_times[-1]}")
    except FileNotFoundError:
        logger.error(f"日志文件未找到: {log_file_path}")
        return [], []

    logger.info(f"解析完成: 共找到{len(times)}条记录")
    return times, alg_cal_times

def save_memory_data(memory_data, title, excel_path):
    logger.info(f"开始保存内存数据，文档位置: {excel_path}, 标题: {title}")
    df = pd.DataFrame(memory_data, columns=['Time', 'Memory'])

    # 如果文件不存在则创建
    if not os.path.exists(excel_path):
        logger.info(f"文件 {excel_path} 不存在，正在创建新文件")
        wb = Workbook()
        wb.save(excel_path)

    # 保存数据到Excel
    with pd.ExcelWriter(excel_path, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name=title, index=False)
        logger.info(f"内存数据已保存到Excel，sheet名称: {title}")

    # 生成折线图
    create_excel_chart(excel_path, title, 'Memory')
    logger.info(f"内存数据折线图已生成，文档位置: {excel_path}, 标题: {title}")

def save_alg_cal_time_plot(times, alg_cal_times, title, excel_path):
    logger.info(f"开始保存算法计算时间数据，文档位置: {excel_path}, 标题: {title}")
    df = pd.DataFrame({'Time': times, 'AlgCalTime': alg_cal_times})

    # 如果文件不存在则创建
    if not os.path.exists(excel_path):
        logger.info(f"文件 {excel_path} 不存在，正在创建新文件")
        wb = Workbook()
        wb.save(excel_path)

    with pd.ExcelWriter(excel_path, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name=title, index=False)
        logger.info(f"算法计算时间数据已保存到Excel，sheet名称: {title}")

    create_excel_chart(excel_path, title, 'AlgCalTime')
    logger.info(f"算法计算时间折线图已生成，文档位置: {excel_path}, 标题: {title}")

def create_excel_chart(excel_path, sheet_name, y_axis_label):
    logger.info(f"开始创建Excel折线图，文档位置: {excel_path}, sheet名称: {sheet_name}, Y轴标签: {y_axis_label}")
    wb = load_workbook(excel_path)
    ws = wb[sheet_name]

    chart = LineChart()
    chart.title = f"{sheet_name} 折线图"
    chart.style = 13
    chart.y_axis.title = y_axis_label
    chart.x_axis.title = 'Time'
    chart.width = 20  # 设置折线图宽度
    chart.height = 10  # 设置折线图高度

    data = Reference(ws, min_col=2, min_row=1, max_col=2, max_row=ws.max_row)
    categories = Reference(ws, min_col=1, min_row=2, max_row=ws.max_row)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(categories)

    # 设置折线图的线条宽度
    for series in chart.series:
        series.graphicalProperties.line.width = 20000  # 单位为EMU，1pt = 12700 EMU

    # 确保所有时间段都有显示
    chart.x_axis.majorUnit = 1  # 设置X轴的主要单位为1，确保每个时间点都显示

    ws.add_chart(chart, "C1")
    logger.info(f"折线图已添加到工作表，位置: C1")

    wb.save(excel_path)
    logger.info(f"Excel文档已保存，文档位置: {excel_path}")

def get_process_memory_usage(process_name):
    """获取指定进程的内存使用率"""
    try:
        for proc in psutil.process_iter(['name', 'memory_info']):
            if proc.info['name'] == process_name:
                return proc.info['memory_info'].rss / (1024 * 1024)  # 以MB为单位
    except Exception as e:
        logger.error(f"获取进程内存使用率时发生错误: {e}")
    return 0

def test_current_window():
    if not utils.search_symbol(config.TEST_WINDOW, tolerance=0.7):
        messagebox.showwarning("警告", "请先选中窗口，并确保测试当前窗口的按钮存在")
        return

    memory_data = []
    start_time = time.time()

    try:
        while True:
            # 点击图片
            utils.click_by_png(config.TEST_WINDOW, timeout=1)
            time.sleep(1)
            # 获取当前时间和内存使用
            current_time = time.time()
            memory_usage = get_process_memory_usage("AOI.exe")

            # 记录数据
            memory_data.append((datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), memory_usage))

            # 每分钟保存一次数据
            if (current_time - start_time) >= 60:
                logger.info(f"excel_path: {excel_path}")
                save_memory_data(memory_data, "Test Window", excel_path)
                start_time = current_time

    except KeyboardInterrupt:
        logger.info("用户中断，保存数据。")
    except Exception as e:
        logger.error(f"发生异常: {e}")
    finally:
        logger.info(f"excel_path: {excel_path}")
        save_memory_data(memory_data, "Test Component", excel_path)

def test_current_group():
    if not utils.search_symbol(config.TEST_GROUP, tolerance=0.7):
        messagebox.showwarning("警告", "请先选中窗口，并确保测试当前分组的按钮存在")
        return

    memory_data = []

    def record_memory_usage():
        while True:
            # 获取AOI.exe进程的内存使用
            memory_usage = get_process_memory_usage("AOI.exe")
            memory_data.append((datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), memory_usage))
            time.sleep(1)

    def save_memory_periodically():
        while True:
            time.sleep(30)
            logger.info(f"excel_path: {excel_path}")
            save_memory_data(memory_data, "Test Group", excel_path)

    try:
        threading.Thread(target=record_memory_usage, daemon=True).start()
        threading.Thread(target=save_memory_periodically, daemon=True).start()

        while True:
            utils.click_by_png(config.TEST_GROUP, timeout=1)
            while utils.search_symbol(config.TESTING_COMPONENT, timeout=1):
                time.sleep(1)

    except KeyboardInterrupt:
        logger.info("用户中断，保存数据。")
    except Exception as e:
        logger.error(f"发生异常: {e}")
    finally:
        logger.info(f"excel_path: {excel_path}")
        save_memory_data(memory_data, "Test Component", excel_path)

def test_current_component():
    if not utils.search_symbol(config.TEST_COMPONENT, tolerance=0.7):
        messagebox.showwarning("警告", "请先选中窗口，并确保测试当前元件的按钮存在")
        return

    memory_data = []

    def record_memory_usage():
        while True:
            # 获取AOI.exe进程的内存使用
            memory_usage = get_process_memory_usage("AOI.exe")
            memory_data.append((datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), memory_usage))
            time.sleep(1)

    def save_memory_periodically():
        while True:
            time.sleep(30)
            logger.info(f"excel_path: {excel_path}")
            save_memory_data(memory_data, "Test Component", excel_path)

    try:
        threading.Thread(target=record_memory_usage, daemon=True).start()
        threading.Thread(target=save_memory_periodically, daemon=True).start()

        while True:
            utils.click_by_png(config.TEST_COMPONENT, timeout=1)
            while utils.search_symbol(config.TESTING_COMPONENT, timeout=3):
                time.sleep(1)

    except KeyboardInterrupt:
        logger.info("用户中断，保存数据。")
    except Exception as e:
        logger.error(f"发生异常: {e}")
    finally:
        logger.info(f"excel_path: {excel_path}")
        save_memory_data(memory_data, "Test Component", excel_path)

def test_current_board():
    if not utils.search_symbol(config.TEST_BOARD, timeout=3, tolerance=0.7):
        messagebox.showwarning("警告", "请先选中窗口，并确保测试当前整板的按钮存在")
        return

    memory_data = []

    if not os.path.exists(excel_path):
        wb = Workbook()
        wb.save(excel_path)

    def record_memory_usage():
        while True:
            # 获取AOI.exe进程的内存使用
            memory_usage = get_process_memory_usage("AOI.exe")
            memory_data.append((datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), memory_usage))
            time.sleep(1)

    def save_memory_periodically():
        while True:
            time.sleep(30)
            logger.info(f"excel_path: {excel_path}")
            save_memory_data(memory_data, "Test Board Memory", excel_path)

    def save_alg_cal_time_periodically():
        while True:
            time.sleep(30)
            save_alg_cal_time_plot(times, alg_cal_times, "Test Board AlgCalTime", excel_path)

    try:
        threading.Thread(target=record_memory_usage, daemon=True).start()
        threading.Thread(target=save_memory_periodically, daemon=True).start()
        threading.Thread(target=save_alg_cal_time_periodically, daemon=True).start()

        while True:
            if not utils.search_symbol(config.TESTING_COMPONENT, timeout=5):
                log_file_path = r'D:\EYAOI\Logger\Lane_0\AlgSimpCalTime_' + datetime.datetime.now().strftime('%Y-%m-%d') + '.log'
                try:
                    times, alg_cal_times = parse_log_file(log_file_path)
                except Exception as e:
                    logger.error(f"解析日志文件时发生错误: {e}")
                    times, alg_cal_times = [], []
                if not times or not alg_cal_times:
                    logger.info("日志文件解析失败或无数据")
                    logger.info("开始点击")
                    utils.click_by_png(config.TEST_BOARD, 2, timeout=3, tolerance=0.7)
                    logger.info("点击完成")
                    if utils.search_symbol(config.QUESTION_MARK, 1):
                        pyautogui.press("enter")

            while utils.search_symbol(config.TESTING_COMPONENT, timeout=3):
                time.sleep(1)

    except KeyboardInterrupt:
        logger.info("用户中断，保存数据。")
    except Exception as e:
        logger.error(f"发生异常: {e}")
    finally:
        logger.info(f"excel_path: {excel_path}")
        save_memory_data(memory_data, "Test Board Memory", excel_path)
        save_alg_cal_time_plot(times, alg_cal_times, "Test Board AlgCalTime", excel_path)
