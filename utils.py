import ctypes
import random
import shutil
import easyocr
import sys
import time
import psutil
import pyperclip
import cv2
import numpy as np
import win32gui
import pyautogui
import config
import functools
import datetime
import threading
import os
from difflib import SequenceMatcher
import tkinter as tk
from tkinter import messagebox
from threading import Event
from pywinauto import Application, Desktop
from PIL import ImageGrab
from PIL import Image as PILImage
from PIL import ImageChops
from screeninfo import get_monitors
from loguru import logger
from difflib import SequenceMatcher
from openpyxl import Workbook, load_workbook
from openpyxl.drawing.image import Image as ExcelImage
from sklearn.cluster import KMeans

ctypes.windll.shcore.SetProcessDpiAwareness(0)  # 解决使用pyautowin时缩放问题
running_event = Event()

# ============================日志=======================
# 设置日志记录器
def setup_logger():
    log_dir = os.path.join(os.getcwd(), "log")
    print("Log Directory:", log_dir)
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "script_log_{time:YYYY-MM-DD}.log")
    logger.add(log_file, rotation="100 MB", retention="10 days",
               format="{time:YYYY-MM-DD HH:mm:ss.SSS} {level} {message}", level="INFO")
    logger.info("已开启日志记录")


# ============================窗格处理===================
# 连接窗口（好像只能用win32连接窗口,uia不行）
def connect_aoi_window():
    # try:
    #     windows = Desktop(backend="win32").windows()
    #     window_found = False
    #     aoi_amount = 0
    #     for w in windows:
    #         try:
    #             class_name = w.class_name()
    #             automation_id = w.automation_id()
    #             if class_name == "WindowsForms10.Window.8.app.0.ea7f4a_r8_ad1" and automation_id == "MainForm":
    #                 window_properties = w.get_properties()
    #                 logger.info(f"aoi窗口存在,详细信息：{window_properties}")
    #                 window_found = True
    #                 aoi_amount += 1
    #                 # break
    #         except Exception as e:
    #             continue
    #     logger.info(f"aoi窗口数量: {aoi_amount}")
    #     if not window_found:
    #         error_message = "未找到任何符合条件的aoi窗口。"
    #         logger.error(error_message)
    #         raise Exception(error_message)
    #     else:
    #         app = Application().connect(class_name="WindowsForms10.Window.8.app.0.ea7f4a_r8_ad1", auto_id="MainForm")
    #         main_window = app.window(auto_id="MainForm")
    #         if main_window.exists(timeout=10):
    #             logger.info("成功连接到窗口")
    #             return main_window
    #         else:
    #             error_message = "未找到窗口"
    #             logger.error(error_message)
    #             raise Exception(error_message)
    # except Exception as e:
    #     error_message = f"连接窗口时发生错误: {e}"
    #     logger.error(error_message)
        # raise Exception(error_message)
    try:
        # 使用 uia 后端进行连接
        app = Application(backend="uia").connect(title_re="Sinic-Tek 3D AOI", auto_id="MainForm")
        main_window = app.window(auto_id="MainForm")
        if main_window.exists(timeout=20):  # 增加超时时间
            logger.info("成功连接到窗口")
            return main_window
        else:
            error_message = "未找到窗口"
            logger.error(error_message)
            raise Exception(error_message)
    except Exception as e:
        error_message = f"连接窗口时发生错误: {e}"
        logger.error(error_message)
        raise Exception(error_message)
def window_interactive(title_re=None, auto_id=None, class_name=None, control_type="Button", name=None, action="click", text=None):
    try:
        logger.info(f"传入参数 - title_re: {title_re}, auto_id: {auto_id}, class_name: {class_name}, control_type: {control_type}, name: {name}, action: {action}, text: {text}")
        main_window = connect_aoi_window()
        logger.info("成功连接到主窗口")

        # 检查并组合存在的参数
        search_criteria = {}
        if title_re:
            search_criteria['title_re'] = f".*{title_re}.*"
        if auto_id:
            search_criteria['auto_id'] = auto_id
        if class_name:
            search_criteria['class_name'] = class_name
        if control_type:
            search_criteria['control_type'] = control_type
        if name:
            search_criteria['title'] = name
        
        if not search_criteria:
            raise ValueError("必须提供至少一个参数用于筛选控件")
        
        logger.info(f"使用筛选条件: {search_criteria} 查找目标控件")
        try:
            target_control = main_window.child_window(**search_criteria).wait('exists', timeout=10)
            logger.info(f"找到目标控件: {target_control}")
        except Exception as e:
            logger.error(f"查找控件时发生错误: {e}")
            raise Exception(f"查找控件时发生错误: {e}")
        
        # 检查控件是否存在
        if not target_control.exists():
            raise Exception("未找到符合条件的控件")
        
        target_control = target_control.wrapper_object()
        
        logger.info(f"目标控件信息: {target_control}")
        logger.info("找到目标控件，检查其可见性和启用状态")
        if not (target_control.is_visible() and target_control.is_enabled()):
            raise Exception("目标控件不可见或不可用")
        
        logger.info("目标控件可见且可用，准备执行操作")
        if action == "click":
            target_control.click()
            logger.info("成功点击目标控件")
        elif action == "set_text" and text is not None:
            target_control.set_text(text)
            logger.info(f"成功设置文本: {text}")
        else:
            raise ValueError("无效的操作或缺少文本内容")
    except Exception as e:
        error_message = f"操作目标控件时发生错误: {e}"
        logger.error(error_message)
        raise Exception(error_message)
# 处理登录时的一系列预处理（有可能为打开程式的界面）
def login_process():
    logger.warning("开始登录预处理")
    if search_symbol(config.LOGINING, 2):
        time.sleep(3)
    delete_documents(config.SHARE_LIB_PATH)
    delete_documents(config.ELEMENTS_LIB_PATH)
    try:
        # 获取屏幕分辨率
        user32 = ctypes.windll.user32
        current_width = user32.GetSystemMetrics(0)
        current_height = user32.GetSystemMetrics(1)
        
        # 如果当前分辨率不是1920x1080，则进行修改
        if current_width != 1920 or current_height != 1080:
            logger.debug(f"当前分辨率为{current_width}x{current_height}，正在修改为1920x1080...")
            user32.ChangeDisplaySettingsW(None, 0)
            devmode = ctypes.create_string_buffer(148)
            ctypes.memset(devmode, 0, 148)
            ctypes.memmove(devmode, b'\x00' * 148, 148)
            ctypes.memmove(devmode, b'\x00' * 40, 40)
            ctypes.memmove(devmode[40:], b'\x80\x07\x38\x04', 4)
            ctypes.memmove(devmode[44:], b'\x00\x00\x00\x00', 4)
            ctypes.memmove(devmode[108:], b'\x00\x00\x00\x00', 4)
            ctypes.memmove(devmode[112:], b'\x00\x00\x00\x00', 4)
            ctypes.memmove(devmode[116:], b'\x00\x00\x00\x00', 4)
            ctypes.memmove(devmode[120:], b'\x00\x00\x00\x00', 4)
            ctypes.memmove(devmode[124:], b'\x00\x00\x00\x00', 4)
            ctypes.memmove(devmode[128:], b'\x00\x00\x00\x00', 4)
            ctypes.memmove(devmode[132:], b'\x00\x00\x00\x00', 4)
            ctypes.memmove(devmode[136:], b'\x00\x00\x00\x00', 4)
            ctypes.memmove(devmode[140:], b'\x00\x00\x00\x00', 4)
            ctypes.memmove(devmode[144:], b'\x00\x00\x00\x00', 4)
            user32.ChangeDisplaySettingsW(devmode, 0)
            logger.info("分辨率修改成功")
        else:
            logger.info("当前分辨率已为1920x1080，无需修改")
    except Exception as e:
        error_message = f"修改分辨率时发生错误: {e}"
        logger.error(error_message)
        raise Exception(error_message)
    click_by_png(config.AOI_TOPIC, tolerance=0.8, type="bottom")
    # 确保登录后无弹框
    login_symbols = [
        (config.USER_LOGIN_LIGHT, 0.95),
        (config.USER_LOGIN_DARK, 0.95),
        (config.USER_LOGIN_CHINESE_LIGHT, 0.8),
        (config.USER_LOGIN_CHINESE_DARK, 0.8)
    ]
    if any(search_symbol(symbol, 1.5, tolerance=tol) for symbol, tol in login_symbols):
        write_text((865,500),"000")
        time.sleep(0.5)
        pyautogui.press('enter')
        if search_symbol(config.INVALID_PASSWORD, 1.5, tolerance=0.95):
            # 关闭密码错误窗口
            pyautogui.press('enter')
            time.sleep(0.5)
            # 输入下个密码
            write_text((865,500),"sinictek")
            time.sleep(0.5)
            pyautogui.press('enter')
            time.sleep(1)
            # 关闭登录成功窗口
            pyautogui.press('enter')
        else:
            # 关闭登录成功窗口
            pyautogui.press('enter')
    # 防止登录aoi后直接就是打开程式界面
    if search_symbol(config.WINDOW_CANCEL, 1.5, tolerance=0.8):
        click_by_png(config.WINDOW_CANCEL, tolerance=0.8)
    # 关闭打开程式窗口
    if search_symbol(config.OPEN_PROGRAM_TOPIC, 1.5, tolerance=0.8):
        click_by_png(config.CANCEL, tolerance=0.8)
    # 确保登录时没有开在线调参功能
    if search_symbol(config.RUN_DARK, 1.5):
        click_by_png(config.RUN_DARK, timeout=1.5)
        time.sleep(1)
    if search_symbol(config.CHANGE_PARAM_ONLINE, 1.5):
        click_by_png(config.CHANGE_PARAM_ONLINE, timeout=1.5)
        time.sleep(0.5)
    if search_symbol(config.QUESTION_MARK, 5, tolerance=0.75):
        if search_symbol(config.NO,2):
            click_by_png(config.NO,timeout=2)
        else:
            pyautogui.press("enter")
    logger.warning("登录预处理完成")

# 确保spc打开并前置
def check_and_launch_spc():
    spc_running = any("SPC.exe" == p.name() for p in psutil.process_iter())
    if not spc_running:
        logger.info("SPC程序未运行,正在启动...")
        app = Application().start(config.SPC_EXE_PATH)
        logger.info("等待SPC程序启动...")
        app.window(title_re=".*SPC.*").wait('ready', timeout=60)
        if search_symbol(config.SPC_LOGIN_USERNAME):
            pyautogui.click(1141, 448)
            click_by_png(config.SPC_USER_ADMIN)
            write_text((845,495),config.SPC_PASSWORD)
            click_by_png(config.SPC_LOGIN)
            time.sleep(3)
            if not search_symbol(config.SPC_SYSTEM_SETTING):
                raise Exception("SPC疑似登录失败,未检测到SPC界面")
        
    else:
        if search_symbol(config.SPC_TOPIC):
            click_by_png(config.SPC_TOPIC, type="right")
            


# 确保aoi打开并前置
def check_and_launch_aoi():
    # 先检测并杀掉有关的进程
    for proc in psutil.process_iter(['pid', 'name']):
        if any(name in proc.info['name'] for name in ["AOI", "SPCView"]):
            try:
                parent_proc = psutil.Process(proc.info['pid'])
                children = parent_proc.children(recursive=True)
                for child in children:
                    child.kill()
                parent_proc.kill()
                parent_proc.wait()
                logger.info(f"进程 {proc.info['name']} (PID: {proc.info['pid']}) 已被杀死")
            except Exception as kill_error:
                logger.error(f"无法杀掉进程 {proc.info['name']} (PID: {proc.info['pid']}): {kill_error}")

    
    aoi_running = any("AOI.exe" == p.name() for p in psutil.process_iter())
    if not aoi_running:
        logger.info("AOI程序未运行,正在启动...")
        app = Application().start(config.AOI_EXE_PATH)
        logger.info("等待AOI程序启动...")
        # app.window(title_re=".*AOI.*").wait('ready', timeout=60)
        # 发现程序在加载的话等30秒
        timeout = time.time() + 60
        while time.time() < timeout:
            if search_symbol(config.WARNING, 5,tolerance=0.75):
                pyautogui.press("enter")
            if search_symbol(config.LOGINING, tolerance=0.8):
                for proc in psutil.process_iter():
                    if "aoi_memory" in proc.name():
                        logger.info(f"正在杀死进程 {proc.name()}...")
                        proc.kill()
                        proc.wait()
                        logger.info(f"进程 {proc.name()} 已被杀死")
                break
            time.sleep(5)
        while search_symbol(config.LOGINING, 2,tolerance=0.8):
            time.sleep(3)
        search_symbol_erroring(config.AOI_TOPIC, 60,tolerance=0.75)
    else:
        for proc in psutil.process_iter():
            if "aoi_memory" in proc.name():
                logger.info(f"正在杀死进程 {proc.name()}...")
                proc.kill()
                proc.wait()
                logger.info(f"进程 {proc.name()} 已被杀死")
        # 优先点击标题置顶，用窗口置顶容易出问题
        while search_symbol(config.LOGINING, 2):
            time.sleep(3)
        if search_symbol(config.AOI_TOPIC, 2, tolerance=0.75):
            click_by_png(config.AOI_TOPIC, tolerance=0.8, type="bottom")
        else:
            logger.warning("AOI窗口标题未找到，尝试通过窗口句柄前置")
            main_window = connect_aoi_window()
            main_window.wait('ready', timeout=10)
            main_window.set_focus()
            main_window.wait('ready', timeout=10)
            # 确保窗口未最小化并且前置
            if main_window.is_minimized():
                main_window.restore()
            main_window.set_focus()  # 再次确保窗口前置
            # 获取窗口句柄
            hwnd = main_window.handle
            rect = win32gui.GetWindowRect(hwnd)
            # win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # 恢复窗口
            win32gui.SetForegroundWindow(hwnd)  # 前置窗口
            win32gui.BringWindowToTop(hwnd)  # 确保窗口在最前
            win32gui.MoveWindow(hwnd, rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1], True)
            logger.info("AOI窗口已前置并保持原大小。")
    login_process()
def close_aoi():
    for proc in psutil.process_iter():
        if "AOI.exe" == proc.name():
            logger.info("AOI程序正在运行,正在关闭...")
            proc.kill()
            proc.wait() 
            logger.info("AOI程序已关闭")
            break

def close_spc():
    for proc in psutil.process_iter():
        if "SPCViewMain.exe" == proc.name():
            logger.info("SPC程序正在运行,正在关闭...")
            proc.kill()
            proc.wait() 
            logger.info("SPC程序已关闭")
            break

# 确保在特定界面（通过特定标识物的存在）
def ensure_in_specific_window(name=None, auto_id=None, control_type=None):
    try:
        main_window = connect_aoi_window()
        criteria = {}
        if name:
            criteria['title'] = name
        if auto_id:
            criteria['auto_id'] = auto_id
        if control_type:
            criteria['control_type'] = control_type

        specific_symbol = main_window.child_window(**criteria)
        if specific_symbol.exists(timeout=3):
            logger.info(specific_symbol.get_properties())
            return True
        else:
            logger.info("未找到" + name + "窗格，可能目前不在指定的界面")
            return False
    except Exception as e:
        logger.error(f"发生错误: {e}")
        return False


# 点不到就报错（前提是能搜索到该按钮）
def click_by_controls(name=None, auto_id=None, control_type=None):
    try:
        main_window = connect_aoi_window()
        criteria = {}
        if name:
            criteria['title_re'] = f".*{name}.*"
        if auto_id:
            criteria['auto_id'] = auto_id
        if control_type:
            criteria['control_type'] = control_type

        button = main_window.child_window(**criteria)
        if button.exists(timeout=3):
            button.click_input()
            logger.info("已点击按钮：" + (name if name else "未指定名称"))
        else:
            logger.info("点击时未找到指定的按钮")
    except Exception as e:
        logger.error(f"发生错误: {e}")


# 确认程序无卡顿/闪退
def caton_or_flashback():
    try:
        # 检测主程序窗口是否还存在
        main_window = connect_aoi_window()
        # if not main_window.is_visible():
        #     raise Exception("AOI程序窗口不可见，可能已经崩溃")

        # 检测程序是否响应
        if not main_window.is_enabled():
            raise Exception("AOI程序无响应，可能已经卡顿")

        logger.info("AOI程序运行正常，无卡顿或闪退")
    except Exception as e:
        logger.error(f"检测到程序异常: {e}")
        raise Exception(f"AOI程序异常: {e}")



# ==============================识别处理===============================
# 寻找准星
def get_crosshair_center():
    logger.info("开始寻找准星")
    # 定义准星的颜色
    crosshair_color = (255, 69, 0)

    # 定义截图区域
    left = 540
    top = 150
    width = 1500 - 540
    height = 740 - 150

    # 截取指定区域的屏幕图像
    screenshot = pyautogui.screenshot(region=(left, top, width, height))
    screenshot_np = np.array(screenshot)

    # 转换颜色到HSV
    screenshot_hsv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2HSV)
    crosshair_color_hsv = cv2.cvtColor(np.uint8([[crosshair_color]]), cv2.COLOR_RGB2HSV)[0][0]

    # 定义颜色的HSV范围，更严格的范围
    hue_variation = 5
    saturation_variation = 50
    value_variation = 50
    lower_bound = np.array([crosshair_color_hsv[0] - hue_variation, crosshair_color_hsv[1] - saturation_variation,
                            crosshair_color_hsv[2] - value_variation])
    upper_bound = np.array([crosshair_color_hsv[0] + hue_variation, crosshair_color_hsv[1] + saturation_variation,
                            crosshair_color_hsv[2] + value_variation])

    # 创建颜色掩码
    mask = cv2.inRange(screenshot_hsv, lower_bound, upper_bound)

    # 计算掩码的质心
    M = cv2.moments(mask)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"]) + left
        cy = int(M["m01"] / M["m00"]) + top
        logger.info(f"全屏准星位置: ({cx}, {cy})")
        return (cx, cy)
    else:
        logger.error("未找到准星")
        return None


# 检测屏幕是否有大量某个颜色
def check_color_expand():
    # 捕获屏幕截图
    screenshot = ImageGrab.grab()
    screenshot_np = np.array(screenshot)

    # 定义目标颜色和容差
    target_color = np.array([188, 157, 160])  # 注意：OpenCV使用BGR格式
    tolerance = 20  # 容差值

    # 计算颜色范围
    lower_bound = target_color - tolerance
    upper_bound = target_color + tolerance

    # 创建掩码
    mask = cv2.inRange(screenshot_np, lower_bound, upper_bound)

    # 计算掩码中的白色像素比例
    coverage = np.sum(mask) / (screenshot_np.shape[0] * screenshot_np.shape[1] * 255)

    # 判断是否有大量的目标颜色
    if coverage > 0.25:
        logger.info("元件四周遮罩出现大量粉色")
        return True
    else:
        logger.info("元件四周遮罩未出现大量粉色")
        return False

# 检测滚动条占比，以确认元件/芯片数量(换方法了 废弃)
def check_chip_coverage(scrollbar_color, scrollbar_region):
    # 截取指定区域的屏幕图像
    screenshot = ImageGrab.grab(bbox=scrollbar_region)
    screenshot_np = np.array(screenshot)

    # 定义目标颜色和容差
    target_color = np.array(scrollbar_color)  # 直接使用RGB颜色
    tolerance = 5 

    # 计算颜色范围
    lower_bound = target_color - tolerance
    upper_bound = target_color + tolerance

    # 创建掩码
    mask = cv2.inRange(screenshot_np, lower_bound, upper_bound)

    # 计算掩码中的白色像素比例
    coverage = np.sum(mask) / (screenshot_np.shape[0] * screenshot_np.shape[1] * 255)

    # 返回百分比
    return coverage
# 检测斜杠太麻烦了 暂时没时间，用颜色代替了
def if_checked(top_left, bottom_right):
    # 调整坐标
    adjusted_top_left, adjusted_bottom_right = adjust_coordinates(top_left, bottom_right)

    # 截取屏幕上的复选框区域
    screenshot = ImageGrab.grab(
        bbox=(adjusted_top_left[0], adjusted_top_left[1], adjusted_bottom_right[0], adjusted_bottom_right[1]))
    screenshot_np = np.array(screenshot)
    screenshot_np = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

    # 定义目标颜色和容差
    target_colors = [(70, 70, 88), (32, 32, 54), (107, 107, 107)]
    tolerance = 10  # 容差值

    # 检查每个目标颜色
    for color in target_colors:
        lower_bound = np.array(color) - tolerance
        upper_bound = np.array(color) + tolerance

        # 创建掩码
        mask = cv2.inRange(screenshot_np, lower_bound, upper_bound)

        # 检查是否有目标颜色的像素点
        if np.any(mask):
            return True
    return False
# 确保打勾框打勾情况
def is_checked(top_left, bottom_right, expect_checked, times=1):
    # 使用if_checked函数来检查是否勾选
    time.sleep(1)
    check = if_checked(top_left, bottom_right)
    if check == expect_checked:
        pass
    else:
        center_x = (top_left[0] + bottom_right[0]) // 2
        center_y = (top_left[1] + bottom_right[1]) // 2
        pyautogui.click(center_x, center_y, clicks=times)
def filter_color(image, target_color):
    # 将图像转换为numpy数组
    image_np = np.array(image)
    # 定义颜色范围
    lower_bound = np.array(target_color) - 1  # 缩小颜色范围
    upper_bound = np.array(target_color) + 1  # 缩小颜色范围
    # 创建颜色掩码
    mask = cv2.inRange(image_np, lower_bound, upper_bound)
    # 应用掩码
    filtered_image = cv2.bitwise_and(image_np, image_np, mask=mask)
    return PILImage.fromarray(filtered_image)

# 识别图片并点击
def click_by_png(image_path, times=1, timeout=20, if_click_right=0, tolerance=0.8, region=None, instance=1, use_random=0, type="default", click_index=None, preference=None):
    start_time = time.time()
    clicked = False  # 添加一个标志来检测是否成功点击
    image_path = image_fit_screen(image_path)
    logger.info(f"正在识别并点击图片……图片路径为: {image_path}")
    
    # 读取目标图像并计算其平均颜色
    target_image = cv2.imread(image_path)
    target_avg_color = cv2.mean(target_image)[:3]
    
    while time.time() - start_time < timeout:
        try:
            screenshot = pyautogui.screenshot(region=region)
            screenshot_np = np.array(screenshot)
            
            # 过滤颜色
            filtered_screenshot = filter_color(screenshot, target_avg_color)
            filtered_screenshot_np = np.array(filtered_screenshot)
            
            locations = list(pyautogui.locateAllOnScreen(image_path, confidence=tolerance, region=region))
            if locations and len(locations) >= instance:
                if click_index is not None:
                    if click_index <= len(locations):
                        location = locations[click_index - 1]  # 获取第click_index个匹配的图片
                    else:
                        logger.error(f"click_index超出范围: {click_index}")
                        raise Exception(f"click_index超出范围: {click_index}")
                elif use_random == 1:
                    location = random.choice(locations)  # 随机选择一个匹配的图片
                elif preference:
                    if preference == "top":
                        location = min(locations, key=lambda loc: loc.top)
                    elif preference == "bottom":
                        location = max(locations, key=lambda loc: loc.top)
                    elif preference == "left":
                        location = min(locations, key=lambda loc: loc.left)
                    elif preference == "right":
                        location = max(locations, key=lambda loc: loc.left)
                else:
                    location = locations[instance - 1]  # 获取第instance个匹配的图片
                
                # 计算中心坐标
                center_x = location.left + location.width // 2
                if type == "bottom":
                    center_y = location.top + location.height  # 点击底部中间点
                elif type == "right":
                    center_x = location.left + location.width  # 点击右边中间点
                    center_y = location.top + location.height // 2
                elif type == "left":
                    center_x = location.left  # 点击左边中间点
                    center_y = location.top + location.height // 2
                else:
                    center_y = location.top + location.height // 2
                if if_click_right == 1:
                    pyautogui.click(center_x, center_y, button='right')
                else:
                    pyautogui.click(center_x, center_y, clicks=times)
                logger.info(f"点击图片成功，图片路径为{image_path}，坐标为({center_x}, {center_y})")
                clicked = True  # 更新标志为True表示成功点击
                break
            elif not locations:
                logger.info(f"未找到匹配的图片: {image_path}")
        except Exception as e:
            logger.error(f"在尝试点击过程中发生异常: {e}")
            pass
        time.sleep(1)
    if not clicked:  # 检查是否成功点击
        logger.error(f"超时: 在{timeout}秒内未能点击图片，图片路径为{image_path}")
        raise Exception(f"超时: 在{timeout}秒内未能点击图片，图片路径为{image_path}")

def search_symbol(symbol, timeout=10, region=None, tolerance=0.9):
    start_time = time.time()
    symbol = image_fit_screen(symbol)
    logger.info(f"在{timeout}秒内识别图片，要求准确度系数为{tolerance}，图片路径为{symbol}")
    
    # 读取目标图像并计算其平均颜色
    target_image = cv2.imread(symbol)
    target_avg_color = cv2.mean(target_image)[:3]
    
    if timeout != 0:
        while time.time() - start_time < timeout:
            try:
                screenshot = pyautogui.screenshot(region=region)
                screenshot_np = np.array(screenshot)
                screenshot_avg_color = cv2.mean(screenshot_np)[:3]
                
                # 过滤颜色
                filtered_screenshot = filter_color(screenshot, target_avg_color)
                filtered_screenshot_np = np.array(filtered_screenshot)
                
                location = pyautogui.locateOnScreen(symbol, region=region, confidence=tolerance)
                if location is not None:
                    center_x = location.left + location.width // 2
                    center_y = location.top + location.height // 2
                    logger.info(f"已确认{symbol}存在，坐标为({center_x}, {center_y})")
                    time.sleep(0.5)
                    return True
            except pyautogui.ImageNotFoundException:
                pass
            except Exception as e:
                logger.error(f"发生异常: {e}")
                raise Exception(f"发生异常: {e}")
        return False
    else:
        try:
            while True:
                screenshot = pyautogui.screenshot(region=region)
                screenshot_np = np.array(screenshot)
                screenshot_avg_color = cv2.mean(screenshot_np)[:3]
                
                # 过滤颜色
                filtered_screenshot = filter_color(screenshot, target_avg_color)
                filtered_screenshot_np = np.array(filtered_screenshot)
                
                location = pyautogui.locateOnScreen(symbol, region=region, confidence=tolerance)
                if location is not None:
                    center_x = location.left + location.width // 2
                    center_y = location.top + location.height // 2
                    logger.info(f"已确认{symbol}存在，坐标为({center_x}, {center_y})")
                    time.sleep(0.5)
                    return True
        except pyautogui.ImageNotFoundException:
            return False
        except Exception as e:
            logger.error(f"发生异常: {e}")
            raise Exception(f"发生异常: {e}")

def search_symbol_erroring(symbol, timeout=10, region=None, tolerance=0.9):
    start_time = time.time()
    symbol = image_fit_screen(symbol)
    logger.info(f"在{timeout}秒内识别图片，要求准确度系数为{tolerance}，图片路径为{symbol}，识别不到自动报错")
    
    # 读取目标图像并计算其平均颜色
    target_image = cv2.imread(symbol)
    target_avg_color = cv2.mean(target_image)[:3]
    
    if timeout != 0:
        while time.time() - start_time < timeout:
            try:
                screenshot = pyautogui.screenshot(region=region)
                screenshot_np = np.array(screenshot)
                screenshot_avg_color = cv2.mean(screenshot_np)[:3]
                
                # 过滤颜色
                filtered_screenshot = filter_color(screenshot, target_avg_color)
                filtered_screenshot_np = np.array(filtered_screenshot)
                
                location = pyautogui.locateOnScreen(symbol, region=region, confidence=tolerance)
                if location is not None:
                    center_x = location.left + location.width // 2
                    center_y = location.top + location.height // 2
                    logger.info(f"已确认{symbol}存在，坐标为({center_x}, {center_y})")
                    time.sleep(0.5)
                    return True
            except pyautogui.ImageNotFoundException:
                pass
            except Exception as e:
                logger.error(f"发生异常: {e}")
                raise Exception(f"发生异常: {e}")
        # 如果超时后还没有找到符号，抛出超时异常
        logger.error(f"超时: 没找到{symbol}")
        raise Exception(f"超时: 没找到{symbol}")
    else:
        try:
            while True:
                screenshot = pyautogui.screenshot(region=region)
                screenshot_np = np.array(screenshot)
                screenshot_avg_color = cv2.mean(screenshot_np)[:3]
                
                # 过滤颜色
                filtered_screenshot = filter_color(screenshot, target_avg_color)
                filtered_screenshot_np = np.array(filtered_screenshot)
                
                location = pyautogui.locateOnScreen(symbol, region=region, confidence=tolerance)
                if location is not None:
                    center_x = location.left + location.width // 2
                    center_y = location.top + location.height // 2
                    logger.info(f"已确认图片存在，识别到的坐标为({center_x}, {center_y})")
                    time.sleep(0.5)
                    return True
        except pyautogui.ImageNotFoundException:
            raise Exception(f"没找到图片: 图片路径为{symbol}")
        except Exception as e:
            logger.error(f"发生异常: {e}")
            raise Exception(f"发生异常: {e}")

def count_symbol_on_screen(symbol, region=None, confidence=0.9):
    """
    统计屏幕上某个标识的数量

    :param symbol: 要查找的标识图片
    :param region: 要查找的屏幕区域，格式为(x, y, width, height)，默认为None表示全屏查找
    :param confidence: 查找的置信度，默认为0.9
    :return: 返回找到的标识数量
    """
    try:
        locations = list(pyautogui.locateAllOnScreen(symbol, region=region, confidence=confidence))
        count = len(locations)
        logger.info(f"在屏幕上找到 {count} 个 {symbol}")
        return count
    except pyautogui.ImageNotFoundException:
        logger.error(f"未找到图片: {symbol}")
        return 0
    except Exception as e:
        logger.error(f"发生异常: {e}")
        raise Exception(f"发生异常: {e}")


# =========================UI=========================
def auto_close_msgbox(message, title, timeout=10000):
    def show_message():
        root = tk.Tk()
        root.withdraw()
        top = tk.Toplevel(root)
        top.title(title)
        label = tk.Label(top, text=message)
        label.pack(padx=20, pady=20)
        top.after(timeout, top.destroy)
        root.after(timeout + 100, root.destroy)  # 确保在弹框销毁后销毁root
        root.mainloop()

    threading.Thread(target=show_message).start()

# =========================装饰器=========================
# 用于记录每个用例函数的最终状态
test_case_status = {}

def screenshot_error_to_excel(max_attempts=2, running_event=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_attempts):
                if running_event and not running_event.is_set():
                    break
                try:
                    logger.info(f"开始执行 {func.__name__} (尝试 {attempt + 1}/{max_attempts})")
                    auto_close_msgbox(f"开始执行 {func.__name__}", "信息", 5000, topmost=True)
                    
                    result = func(*args, **kwargs)
                    
                    if running_event and not running_event.is_set():
                        raise Exception("Execution stopped by user")
                    
                    logger.info(f"{func.__name__} 执行完毕，无报错")
                    auto_close_msgbox(f"{func.__name__} 执行完毕，无报错", "信息", 5000, topmost=True)
                    
                    test_case_status[func.__name__] = "success"  # 标记为成功
                    return result, None
                except Exception as e:
                    last_exception = e
                    logger.error(f"{func.__name__} 执行出错 (尝试 {attempt + 1}/{max_attempts}): {e}")
                    current_function_name = func.__name__
                    path = sys.executable
                    screenshot_to_excel(current_function_name, path, e)
                    
                    if attempt < max_attempts - 1:
                        logger.warning(f"准备重试 {func.__name__}")
                        for proc in psutil.process_iter(['pid', 'name']):
                            if any(name in proc.info['name'] for name in ["AOI", "SPCView"]):
                                try:
                                    parent_proc = psutil.Process(proc.info['pid'])
                                    children = parent_proc.children(recursive=True)
                                    for child in children:
                                        child.kill()
                                    parent_proc.kill()
                                    parent_proc.wait()
                                except Exception as kill_error:
                                    logger.error(f"无法杀掉进程 {proc.info['name']} (PID: {proc.info['pid']}): {kill_error}")
                        
                        aoi_still_running = any("AOI" in p.info['name'] for p in psutil.process_iter(['name']))
                        spcview_still_running = any("SPCView" in p.info['name'] for p in psutil.process_iter(['name']))
                        if not aoi_still_running and not spcview_still_running:
                            logger.info("所有AOI和SPCView进程已关闭，准备重试")
                        else:
                            logger.error("AOI或SPCView进程关闭失败，但仍将尝试重试")
                    else:
                        logger.error(f"{func.__name__} 达到最大尝试次数 ({max_attempts})")
                        auto_close_msgbox(f"方法名: {func.__name__}, 异常信息: {str(e)}", "错误信息", 5000, topmost=True)
                        test_case_status[func.__name__] = "failed"  # 标记为失败
            return None, last_exception
        return wrapper
    return decorator
def auto_close_msgbox(message, title, timeout=10000, topmost=False):
    def show_message():
        root = tk.Tk()
        root.withdraw()
        top = tk.Toplevel(root)
        top.title(title)
        label = tk.Label(top, text=message)
        label.pack(padx=20, pady=20)
        if topmost:
            top.attributes("-topmost", True)
        top.after(timeout, top.destroy)
        root.after(timeout + 100, root.destroy)  # 确保在弹框销毁后销毁root
        root.mainloop()

    threading.Thread(target=show_message).start()
# 报错时截图存至excel，后关闭aoi
def screenshot_to_excel(test_case_name, path, exception):
    logger.info("开始截图异常情况")
    # 获取当前工作目录
    current_dir = os.getcwd()
    log_dir = os.path.join(current_dir, "log")
    logger.info("创建log目录")
    os.makedirs(log_dir, exist_ok=True)  # 确保log目录存在
    logger.info("创建完成")

    try:
        # 截图
        screenshot = ImageGrab.grab()
        screenshot_file = os.path.join(log_dir, "temp_screenshot.png")
        logger.info("开始保存截图")
        screenshot.save(screenshot_file)  # 保存截图为文件
        logger.info("保存截图完成")

        # 定义Excel文件路径
        excel_path = os.path.join(log_dir, "test_results.xlsx")

        # 检查Excel文件是否存在，如果不存在则创建
        if not os.path.exists(excel_path):
            logger.info("创建excel")
            wb = Workbook()
        else:
            logger.info("加载excel")
            wb = load_workbook(excel_path)
        ws = wb.active

        # 确定下一个空白行
        row = ws.max_row + 1
        logger.info("写入数据")

        # 写入数据
        ws[f"A{row}"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ws[f"B{row}"] = test_case_name
        ws[f"C{row}"] = path
        ws[f"D{row}"] = str(exception)
        logger.info("插入图片")

        # 将截图插入到Excel
        img = ExcelImage(screenshot_file)
        img.anchor = f"E{row}"  # 设置图片的锚点
        ws.add_image(img)
        logger.info("数据处理完毕，开始保存excel")
        wb.save(excel_path)
        logger.info("Excel文件保存在:", excel_path)
        logger.info("保存完毕")
    except Exception as e:
        logger.error(f"在保存截图和数据到Excel时发生错误: {e}")
    finally:
        if os.path.exists(screenshot_file):
            os.remove(screenshot_file)  # 清理临时文件


# ====================业务处理========================

def make_package():
    logger.info("开始制造封装")
    if search_symbol(config.TOOL_DARK, timeout=2):
        click_by_png(config.TOOL_DARK)
    click_by_png(config.PACKAGE_TYPE_MANAGE)
    pyautogui.keyDown('shift')
    pyautogui.click(730, 375)
    pyautogui.keyUp('shift')

    click_by_png(config.EDIT_PACKAGE_TYPE)
    write_text((900,525),"test")
    click_by_png(config.YES)
    write_text((820,290),'test')
    click_by_png(config.QUERY)
    # 读取封装a
    pyautogui.click((980,360))
    click_by_png(config.COPY_PART_NO_NAME)
    package_a = pyperclip.paste()
    # 读取封装b
    pyautogui.click((980,375))
    click_by_png(config.COPY_PART_NO_NAME)
    package_b = pyperclip.paste()
    time.sleep(1)

    click_by_png(config.CLOSE_BUTTON)
    logger.info("封装制造完毕")
    click_by_png(config.EDIT_DARK)

    return package_a,package_b


# 整版界面处理元件
def board_component_process(menu_choice):
    target_color = (0, 255, 0)
    while True:
        # 截取区域内的屏幕图像
        screenshot = pyautogui.screenshot(region=config.COMPONENT_REGION)
        screenshot_np = np.array(screenshot)
        # 寻找颜色匹配的像素点
        matches = np.where(np.all(screenshot_np == target_color, axis=-1))
        if matches[0].size > 0:
            # 获取所有匹配的点的坐标
            coordinates = list(zip(matches[1], matches[0]))
            # 按照x坐标从大到小排序（从右到左）
            coordinates.sort(reverse=True, key=lambda coord: coord[0])
            for x, y in coordinates:
                # 转换为区域内的相对坐标
                x += config.COMPONENT_REGION[0]
                y += config.COMPONENT_REGION[1]
                # 右键点击
                pyautogui.rightClick(x, y)
                # 搜索符号
                if search_symbol(menu_choice, timeout=10, tolerance=0.7):
                    click_by_png(menu_choice, timeout=10, tolerance=0.7)
                    break
                else:
                    pyautogui.click((400, 5))
            break

# 添加待料
def add_waiting_material():
    for _ in range(2):
        click_by_png(config.ADD_STANDARD_IMAGE)
        click_by_png(config.YES)
        if search_symbol(config.ADD_IMAGE_CLOSE, 5):
            click_by_png(config.ADD_IMAGE_CLOSE)
        time.sleep(5)


# 画检测窗口
# def add_window(button="w"):
#     time.sleep(1.5)
#     crosshair_center = get_crosshair_center()
#     if crosshair_center is None:
#         logger.info("未找到准星中心")
#         return

#     nearby_point = (crosshair_center[0] + 3, crosshair_center[1] + 3)
#     logger.info(nearby_point)
#     # 绘制框框（获取准星旁边的颜色，扩大到颜色分界处，截取坐标）
#     target_color = pyautogui.screenshot(region=config.COMPONENT_REGION).getpixel(nearby_point)
#     # 转换颜色到HSV
#     target_color_hsv = cv2.cvtColor(np.uint8([[target_color]]), cv2.COLOR_RGB2HSV)[0][0]
#     # 定义颜色的HSV范围，初始范围
#     hue_variation = 5
#     saturation_variation = 10
#     value_variation = 10
#     found = False
#     last_top_left = None
#     last_bottom_right = None

#     while not found:
#         lower_bound = np.array([target_color_hsv[0] - hue_variation, target_color_hsv[1] - saturation_variation,
#                                 target_color_hsv[2] - value_variation])
#         upper_bound = np.array([target_color_hsv[0] + hue_variation, target_color_hsv[1] + saturation_variation,
#                                 target_color_hsv[2] + value_variation])
#         # 截取config.COMPONENT_REGION内的屏幕图像
#         screenshot = pyautogui.screenshot(region=config.COMPONENT_REGION)
#         screenshot_np = np.array(screenshot)
#         screenshot_hsv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2HSV)
#         # 创建颜色掩码
#         mask = cv2.inRange(screenshot_hsv, lower_bound, upper_bound)

#         # 使用形态学操作增强边界
#         kernel = np.ones((5, 5), np.uint8)
#         mask = cv2.dilate(mask, kernel, iterations=2)
#         mask = cv2.erode(mask, kernel, iterations=2)

#         # 使用边缘检测
#         edges = cv2.Canny(mask, 100, 200)

#         # 寻找连贯区域的轮廓
#         contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#         target_contour = None
#         for contour in contours:
#             if cv2.pointPolygonTest(contour, nearby_point, False) >= 0:
#                 target_contour = contour
#                 found = True
#                 break
#             # 如果找到了符合条件的连贯区域
#         if target_contour is not None:
#             x, y, w, h = cv2.boundingRect(target_contour)
#             # 扩大区域
#             expand_margin = 10
#             top_left = (x - expand_margin, y - expand_margin)
#             bottom_right = (x + w + expand_margin, y + h + expand_margin)
#             last_top_left = top_left
#             last_bottom_right = bottom_right
#             logger.info("找到疑似cad区域，左上及右下坐标如下" + str(top_left) + "," + str(bottom_right))
#         else:
#             # 增加HSV范围并重试
#             hue_variation += 1
#             saturation_variation += 2
#             value_variation += 2
#             if hue_variation > 180 or saturation_variation > 255 or value_variation > 255:
#                 logger.info("未识别出cad区域，可能准心不在cad内")
#                 raise Exception("未识别出cad区域，可能准心不在cad内")
                

#     if last_top_left and last_bottom_right:
#         # 使用pyautogui模拟鼠标拖动
#         pyautogui.press(button)
#         pyautogui.moveTo(last_top_left, duration=1)
#         pyautogui.mouseDown()
#         pyautogui.moveTo(last_bottom_right, duration=1)
#         pyautogui.mouseUp()
#         logger.info("cad描边完毕")
#     else:
#         logger.info("未找到任何区域")

def add_window(button="w"):
    time.sleep(2.5)
    crosshair_center = get_crosshair_center()
    if crosshair_center is None:
        logger.error("未找到准星中心，使用默认坐标(935,445)")
        crosshair_center = (935, 445)

    # 初始化区域大小和扩展步长
    region_size = 50  # 扩大初始搜索区域到50像素
    expansion_step = 5
    found = False
    top_left = bottom_right = None
    start_time = time.time()  # 记录开始时间

    while not found and time.time() - start_time < 30:
        logger.info("正在寻找区域......")
        # 计算当前区域
        region = (crosshair_center[0] - region_size, crosshair_center[1] - region_size, 2 * region_size, 2 * region_size)
        screenshot = pyautogui.screenshot(region=region)
        screenshot_np = np.array(screenshot)
        screenshot_hsv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2HSV)

        # 将图像数据转换为二维数组
        pixel_colors = screenshot_hsv.reshape((-1, 3))

        # 使用K-means聚类找到最常见的颜色块
        kmeans = KMeans(n_clusters=5, random_state=0, n_init=10).fit(pixel_colors)
        unique, counts = np.unique(kmeans.labels_, return_counts=True)
        dominant_cluster = unique[np.argmax(counts)]
        dominant_color_hsv = kmeans.cluster_centers_[dominant_cluster]

        # 定义颜色的HSV范围
        hue_variation = 10
        saturation_variation = 40
        value_variation = 40
        lower_bound = np.array([dominant_color_hsv[0] - hue_variation, dominant_color_hsv[1] - saturation_variation,
                                dominant_color_hsv[2] - value_variation], dtype=np.uint8)
        upper_bound = np.array([dominant_color_hsv[0] + hue_variation, dominant_color_hsv[1] + saturation_variation,
                                dominant_color_hsv[2] + value_variation], dtype=np.uint8)

        # 创建颜色掩码
        mask = cv2.inRange(screenshot_hsv, lower_bound, upper_bound)

        # 使用形态学操作增强边界
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=2)
        mask = cv2.erode(mask, kernel, iterations=2)

        # 使用边缘检测
        edges = cv2.Canny(mask, 100, 200)

        # 寻找连贯区域的轮廓
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            # 找到最大的轮廓
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            # 检查准星是否在轮廓内
            if (x <= region_size and x + w >= region_size and y <= region_size and y + h >= region_size):
                top_left = (x + region[0], y + region[1])  # 转换为原始图像的坐标
                bottom_right = (x + w + region[0], y + h + region[1])
                found = True
                logger.info(f"找到疑似cad区域，左上及右下坐标如下: {top_left}, {bottom_right}")
            else:
                region_size += expansion_step  # 扩大搜索区域
                if region_size > 500:  # 设置最大搜索限制
                    logger.info("扩展到最大范围后未找到任何区域")
                    break
        else:
            region_size += expansion_step  # 扩大搜索区域
            if region_size > 500:  # 设置最大搜索限制
                logger.info("扩展到最大范围后未找到任何区域")
                break

    if found:
        # 使用pyautogui模拟鼠标拖动
        if button:
            pyautogui.press(button)
        pyautogui.moveTo(top_left, duration=1)
        pyautogui.mouseDown()
        pyautogui.moveTo(bottom_right, duration=1)
        pyautogui.mouseUp()
        logger.info("cad描边完毕")
    else:
        logger.info("未找到任何区域,开始瞎画")
        if button:
            pyautogui.press(button)
        pyautogui.moveTo(872 + random.randint(-5, 5), 362 + random.randint(-5, 5), duration=1)
        pyautogui.mouseDown()
        pyautogui.moveTo(1000 + random.randint(-5, 5), 528 + random.randint(-5, 5), duration=1)
        pyautogui.mouseUp()
        logger.info("瞎画完成")
# 打开程式(随机) 
def open_program(program_type=0):
    """
    打开程式
    :param program_type: 0 - 默认, 1 - non-compressed, 2 - compressed
    """
    # 先检测有没有什么傻逼窗口 关掉
    if search_symbol(config.NO, 1.5):
        click_by_png(config.NO, tolerance=0.9)
    pyautogui.press('enter')
    time.sleep(1)
    # 再检测有没有狗日的登录框

    login_symbols = [
        (config.USER_LOGIN_LIGHT, 0.95),
        (config.USER_LOGIN_DARK, 0.95),
        (config.USER_LOGIN_CHINESE_LIGHT, 0.8),
        (config.USER_LOGIN_CHINESE_DARK, 0.8)
    ]
    if any(search_symbol(symbol, 1.5, tolerance=tol) for symbol, tol in login_symbols):
        write_text((865,500),"000")
        time.sleep(0.5)
        pyautogui.press('enter')
        if search_symbol(config.INVALID_PASSWORD, 1.5, tolerance=0.95):
            # 关闭密码错误窗口
            pyautogui.press('enter')
            time.sleep(0.5)
            # 输入下个密码
            write_text((865,500),"sinictek")
            time.sleep(0.5)
            pyautogui.press('enter')
            time.sleep(1)
            # 关闭登录成功窗口
            pyautogui.press('enter')
        else:
            # 关闭登录成功窗口
            pyautogui.press('enter')
    # 现在才开始打开程式
    click_by_png(config.OPEN_PROGRAM)
    # 双击程式
    if program_type == 0:
        symbols = [config.OPEN_PROGRAM_PLUS, config.OPEN_PROGRAM_CURSOR]
        for symbol in symbols:
            if search_symbol(symbol, 3):
                click_by_png(symbol, 2)
                click_by_png(config.YES)
                while search_symbol(config.PROGRAM_LOADING, 5):
                    time.sleep(5)
    if program_type == 1:
        plus_positions = list(pyautogui.locateAllOnScreen(config.OPEN_PROGRAM_PLUS))
        cursor_positions = list(pyautogui.locateAllOnScreen(config.OPEN_PROGRAM_CURSOR))
        for pos in plus_positions + cursor_positions:
            pyautogui.click(pos)
            time.sleep(1)
        click_by_png(config.OPEN_PROGRAM_PLUS, 2)
        if search_symbol(config.OPEN_PROGRAM_EMPTY, 3):
            raise Exception("该程式无job")
        click_by_png(config.YES)
        while search_symbol(config.PROGRAM_LOADING, 5):
            time.sleep(5)
    if program_type == 2:
        plus_positions = list(pyautogui.locateAllOnScreen(config.OPEN_PROGRAM_PLUS))
        cursor_positions = list(pyautogui.locateAllOnScreen(config.OPEN_PROGRAM_CURSOR))
        for pos in plus_positions + cursor_positions:
            pyautogui.click(pos)
            time.sleep(1)
        click_by_png(config.OPEN_PROGRAM_CURSOR, 2)
        if search_symbol(config.OPEN_PROGRAM_EMPTY, 3):
            raise Exception("该程式无job")
        click_by_png(config.YES)
        while search_symbol(config.PROGRAM_LOADING, 5):
            time.sleep(5)
    return



# 获取最近编辑的一个程式
def get_topest_program():
    cursor_positions = list(pyautogui.locateAllOnScreen(config.OPEN_PROGRAM_CURSOR))
    plus_positions = list(pyautogui.locateAllOnScreen(config.OPEN_PROGRAM_PLUS))
    all_positions = cursor_positions + plus_positions
    if all_positions:
        topest = sorted(all_positions, key=lambda pos: pos.top)[0]
    else:
        logger.error("未找到任何cursor或plus的坐标")
        raise Exception("未找到任何cursor或plus的坐标")

    return topest


# 确保在编辑界面
def ensure_in_edit_mode():
    login_symbols = [
        (config.USER_LOGIN_LIGHT, 0.95),
        (config.USER_LOGIN_DARK, 0.95),
        (config.USER_LOGIN_CHINESE_LIGHT, 0.8),
        (config.USER_LOGIN_CHINESE_DARK, 0.8)
    ]
    if any(search_symbol(symbol, 1.5, tolerance=tol) for symbol, tol in login_symbols):
        write_text((865,500),"000")
        time.sleep(0.5)
        pyautogui.press('enter')
        if search_symbol(config.INVALID_PASSWORD, 3):
            pyautogui.press('enter')
            write_text((865,500),"sinictek")
            time.sleep(0.5)
            pyautogui.press('enter')                        
    # 先尝试打开程式元件栏
    found_light = search_symbol(config.PROGRAM_COMPONENT_LIGHT, 0)
    found_dark = search_symbol(config.PROGRAM_COMPONENT_DARK, 0)

    if found_light or found_dark:
        if found_dark:
            click_by_png(config.PROGRAM_COMPONENT_DARK)
        if not click_component():
            # 如果点击元件失败，则执行以下代码
            open_program()
            if search_symbol(config.BOARD_AUTO, 50):
                if search_symbol(config.PROGRAM_COMPONENT_DARK, 30):
                    time.sleep(3)
                    click_by_png(config.PROGRAM_COMPONENT_DARK)
            click_component()
    else:
        open_program()
        if search_symbol(config.BOARD_AUTO, 50):
            if search_symbol(config.PROGRAM_COMPONENT_DARK, 30):
                time.sleep(3)
                click_by_png(config.PROGRAM_COMPONENT_DARK)
        click_component()
    # 防止有是否保存的提示
    if search_symbol(config.NO, 2):
        click_by_png(config.NO)
    time.sleep(7)
    click_by_png(config.EDIT_DARK)
    time.sleep(3)

# 确保打开了有多个拼版的job
def ensure_multiple_collages():
    click_by_png(config.OPEN_PROGRAM)
    time.sleep(1)
    # 搜索并点击屏幕上所有＋
    plus_positions = list(pyautogui.locateAllOnScreen(config.OPEN_PROGRAM_PLUS))
    for pos in plus_positions:
        pyautogui.click(pos)
        time.sleep(3)
        # read_text_ocr识别率太低了 改用图片
        if not search_symbol(config.OPEN_PROGRAM_SINGLE_BOARD, 5, config.PROGRAM_INFORMATION_REGION, 0.99):
            click_by_png(config.OPEN_PROGRAM_LOAD_1)
            click_by_png(config.YES)
            return
    logger.error("未找到多个拼版的job")
    raise Exception("未找到多个拼版的job")


# 点击元件
def click_component(click_index=None):
    try:
        # 几种元件里点一个
        components = [config.NO_CHECKED_COMPONENT, config.CHECKED_COMPONENT, config.PASS_COMPONENT, config.NO_PASS_COMPONENT]
        # random.shuffle(components)  # 随机排序元件列表
        for component in components:
            if search_symbol(component, 2, tolerance=0.95, region=config.BOARD_INFORMATION_REGION):
                time.sleep(1)
                click_by_png(component, 2, use_random=1, tolerance=0.8, region=config.BOARD_INFORMATION_REGION, click_index=click_index)
                time.sleep(5)
                return True
        return False
    except Exception as e:
        logger.error(f"点击元件时出错: {e}")
        return False

# 检测该料号的窗口算法参数都已编辑完成，相同封装类型的其他料号的元件的窗口算法参数编辑情况        
def check_same_package_same_param(if_same_param):
    try:
        time.sleep(3)
        # 先截图已选择元件的对应区域
        logger.debug("点击测试按钮")
        click_by_png(config.TEST, 2, region=config.BOARD_INFORMATION_REGION)
        time.sleep(5)
        # 截图PackageType区域和算法参数区域 前者判断封装类型，后者判断参数相同
        logger.debug("截图PackageType区域和算法参数区域")
        package_type_image_old = pyautogui.screenshot(region=config.PACKAGE_TYPE_REGION)
        alg_param_image_old = pyautogui.screenshot(region=config.ALG_PARAM_REGION)
        
        # 遍历所有元件类型
        components = [config.NO_CHECKED_COMPONENT, config.CHECKED_COMPONENT, config.PASS_COMPONENT, config.NO_PASS_COMPONENT]
        for component in components:
            # 找到屏幕上所有该类型元件的位置
            logger.debug(f"查找元件类型: {component}")
            try:
                component_positions = list(pyautogui.locateAllOnScreen(component, region=config.BOARD_INFORMATION_REGION))
            except Exception as e:
                logger.warning(f"查找元件类型 {component} 时出错: {e}")
                continue
            if not component_positions:
                raise Exception("未找到任何元件")
            for pos in component_positions:
                logger.debug(f"双击元件位置: {pos}")
                pyautogui.doubleClick(pos)
                time.sleep(5)  # 等待界面响应
                
                # 检查是否是相同封装类型的元件 相同的话参数是否一致 不相同的话参数不一致
                logger.debug("检查封装类型")
                package_type_image_new = pyautogui.screenshot(region=config.PACKAGE_TYPE_REGION)
                if package_type_image_old == package_type_image_new:
                    # 检查算法参数是否一致
                    logger.debug("检查算法参数是否一致")
                    alg_param_image_new = pyautogui.screenshot(region=config.ALG_PARAM_REGION)
                    if alg_param_image_old == alg_param_image_new:
                        # 参数一致
                        if if_same_param:
                            logger.info("参数已编辑")
                        else:
                            raise Exception("参数已编辑，但预期为未编辑")
                    else:
                        # 参数不一致
                        if not if_same_param:
                            logger.info("参数未编辑")
                        else:
                            raise Exception("参数未编辑，但预期为已编辑")
                else:
                    alg_param_image_new = pyautogui.screenshot(region=config.ALG_PARAM_REGION)
                    if alg_param_image_old == alg_param_image_new:
                        raise Exception("不同封装类型算法参数一致")
    except Exception as e:
        logger.error(f"检查相同封装类型参数时出错: {e}")
        raise
# 检测屏幕区域内是否存在指定颜色
def check_color_in_region(target_color=(220, 20, 60), region=(862, 344, 1010 - 862, 543 - 344)):
    """
    检测屏幕指定区域内是否存在指定颜色的像素点。如果region为坐标点，则检测点周围10个像素范围内是否存在指定颜色。

    :param target_color: 要检测的颜色，格式为(R, G, B)
    :param region: 要检测的屏幕区域，格式为(x, y, width, height))或坐标点(x, y)或单个坐标点(x, y)
    :return: 如果找到指定颜色，返回True，否则返回False
    """
    if isinstance(region, tuple) and len(region) == 2:
        # 如果region为坐标点，则检测点周围10个像素范围内是否存在指定颜色
        logger.info(f"检测区域为坐标点: {region}")
        x, y = region
        for dx in range(-10, 11):
            for dy in range(-10, 11):
                try:
                    # 确保 x + dx 和 y + dy 是整数
                    x_coord = int(x + dx)
                    y_coord = int(y + dy)
                    pixel_color = pyautogui.pixel(x_coord, y_coord)
                    if pixel_color == target_color:
                        return True
                except Exception as e:
                    logger.warning(f"获取像素颜色时出错: {e}")
                    continue
        return False
    elif isinstance(region, tuple) and len(region) == 4:
        # 捕获指定区域的屏幕截图
        logger.info(f"检测区域为区域: {region}")
        screenshot = pyautogui.screenshot(region=region)

        # 遍历区域内的所有像素
        for x in range(region[2]):
            for y in range(region[3]):
                pixel_color = screenshot.getpixel((x, y))
                if pixel_color == target_color:
                    return True
        return False
    else:
        raise ValueError("region参数格式不正确，应为(x, y)、(x, y, width, height)")
    
# ===================================设置快捷键====================================
def shortcut_key_online_parameter_display_sync_package():
    # UI设置--快捷键设置--元件编辑，【在线调参显示同步封装】设置快捷键K
    if search_symbol(config.SETTING_DARK, 1):
        click_by_png(config.SETTING_DARK)
    else:
        search_symbol_erroring(config.SETTING_LIGHT, 1)
    click_by_png(config.PARAM_HARDWARE_SETTING)
    time.sleep(2)
    click_by_png(config.PARAM_SHORTCUT_KEY_SETTING)
    time.sleep(2)

    scroll_down((380, 250), config.SHORTCUT_KEY_COMPONENT_EDIT_REGION)
    write_text_textbox(config.PARAM_ONLINE_PARAMETER_DISPLAY_SYNC_PACKAGE, "K", if_select_all=False)
    time.sleep(1)
    click_by_png(config.APPLY,timeout=1.5, tolerance=0.95)
    if search_symbol(config.NO, 1.5, tolerance=0.95):
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    else:
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    time.sleep(0.5)
    pyautogui.press('enter')
    while search_symbol(config.PARAM_SETTING_TOPIC):
        time.sleep(1.5)
# ====================================设置勾选====================================

# 参数设置--数据导出配置--在线调参，【保留最后PCB板数】设置N
def param_keep_the_last_pcb_number():
    if search_symbol(config.SETTING_DARK, 1):
        click_by_png(config.SETTING_DARK)
    else:
        search_symbol_erroring(config.SETTING_LIGHT, 1)
    click_by_png(config.PARAM_HARDWARE_SETTING)
    time.sleep(2)
    click_by_png(config.PARAM_DATA_EXPORT_SETTING)
    time.sleep(2)
    # 注意 轨道1/2不选的话会有问题
    if search_symbol(config.PARAM_TRACK_1, 2) and search_symbol(config.PARAM_TRACK_2, 2):
        click_by_png(config.PARAM_TRACK_1)

    write_text_textbox(config.PARAM_KEEP_THE_LAST_PCB_NUMBER, "N")
    time.sleep(1)
    click_by_png(config.APPLY,timeout=1.5, tolerance=0.95)
    if search_symbol(config.NO, 1.5, tolerance=0.95):
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    else:
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    time.sleep(0.5)
    pyautogui.press('enter')
    while search_symbol(config.PARAM_SETTING_TOPIC):
        time.sleep(1.5)

# 参数设置--数据导出配置--在线调参，勾选【Good元件】、【NG元件】，或勾选【所有】
def param_good_and_ng_component_limits(good_limit, ng_limit):
    if search_symbol(config.SETTING_DARK, 1):
        click_by_png(config.SETTING_DARK)
    else:
        search_symbol_erroring(config.SETTING_LIGHT, 1)
    click_by_png(config.PARAM_HARDWARE_SETTING)
    time.sleep(2)
    click_by_png(config.PARAM_DATA_EXPORT_SETTING)
    time.sleep(2)

    # 先确定轨道1/2选了
    if search_symbol(config.PARAM_TRACK_1, 2) and search_symbol(config.PARAM_TRACK_2, 2):
        click_by_png(config.PARAM_TRACK_1)

    # 再确定没有勾选所有
    if search_symbol(config.PARAM_ONLINE_ALL_YES, 2):
        click_by_png(config.PARAM_ONLINE_ALL_YES,type="bottom")

    if good_limit is not None:
        if search_symbol(config.PARAM_GOOD_COMPONENT_LIMIT, 2):
            click_by_png(config.PARAM_GOOD_COMPONENT_LIMIT)
        while search_symbol(config.PARAM_AMOUNT_LIMIT_ALL_YES, 2, tolerance=0.95):
            click_by_png(config.PARAM_AMOUNT_LIMIT_ALL_YES,timeout=2,tolerance=0.95,type="right")
        write_text((1275, 730), good_limit)
    if ng_limit is not None:
        if search_symbol(config.PARAM_NG_COMPONENT_LIMIT, 2):
            click_by_png(config.PARAM_NG_COMPONENT_LIMIT)
        while search_symbol(config.PARAM_AMOUNT_LIMIT_ALL_YES, 2, tolerance=0.95):
            click_by_png(config.PARAM_AMOUNT_LIMIT_ALL_YES,timeout=2,tolerance=0.95,type="right")
        write_text((1275, 755), ng_limit)
    # 无传参则勾所有
    if good_limit is None and ng_limit is None:
        if search_symbol(config.PARAM_GOOD_COMPONENT_LIMIT, 2):
            click_by_png(config.PARAM_GOOD_COMPONENT_LIMIT)
        if search_symbol(config.PARAM_NG_COMPONENT_LIMIT, 2):
            click_by_png(config.PARAM_NG_COMPONENT_LIMIT)
        while search_symbol(config.PARAM_AMOUNT_LIMIT_ALL_NO, 2, tolerance=0.95):
            click_by_png(config.PARAM_AMOUNT_LIMIT_ALL_NO,timeout=2,tolerance=0.95,type="right")

    time.sleep(1)
    click_by_png(config.APPLY,timeout=1.5, tolerance=0.95)
    if search_symbol(config.NO, 1.5, tolerance=0.95):
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    else:
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    time.sleep(0.5)
    pyautogui.press('enter')
    while search_symbol(config.PARAM_SETTING_TOPIC):
        time.sleep(1.5)



# 勾选共享元件库路径
def check_share_lib_path(if_checked):
    # 点开设置--硬件设置--数据导出配置--元件库配置
    if search_symbol(config.SETTING_DARK, 1):
        click_by_png(config.SETTING_DARK)
    else:
        search_symbol_erroring(config.SETTING_LIGHT, 1)
    click_by_png(config.PARAM_HARDWARE_SETTING)
    time.sleep(2)
    click_by_png(config.PARAM_DATA_EXPORT_SETTING)
    time.sleep(2)
    # 确保共享元件库路径为勾选状态 （用的坐标）
    is_checked((902, 291), (914, 303), if_checked, 1)
    time.sleep(1)
    click_by_png(config.APPLY,timeout=1.5, tolerance=0.95)
    if search_symbol(config.NO, 1.5, tolerance=0.95):
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    else:
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    time.sleep(0.5)
    pyautogui.press('enter')
    while search_symbol(config.PARAM_SETTING_TOPIC):
        time.sleep(1.5)

# 勾选保存程式默认导出到公共库+勾选自动保存【设置】-【UI配置】-【程序设置】
def check_default_export_auto_save(if_default_export, if_auto_save):
    if search_symbol(config.SETTING_DARK, 1):
        click_by_png(config.SETTING_DARK)
    else:
        search_symbol_erroring(config.SETTING_LIGHT, 1)
    click_by_png(config.PARAM_HARDWARE_SETTING)
    time.sleep(2)
    click_by_png(config.PARAM_UI_SETTING)
    time.sleep(1)
    is_checked((659, 699), (671, 711), if_default_export)
    is_checked((659, 491), (671, 503), if_auto_save)
    time.sleep(0.5)
    click_by_png(config.APPLY,timeout=1.5, tolerance=0.95)
    if search_symbol(config.NO, 1.5, tolerance=0.95):
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    else:
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    time.sleep(0.5)
    pyautogui.press('enter')
    while search_symbol(config.PARAM_SETTING_TOPIC):
        time.sleep(1.5)
# 参数配置--UI配置--软件界面：不选【自动加载程式】 TODO 这边用图的 后面需改
def check_auto_load_program(if_auto_load_program):
    if search_symbol(config.SETTING_DARK, 1):
        click_by_png(config.SETTING_DARK)
    else:
        search_symbol_erroring(config.SETTING_LIGHT, 1)
    click_by_png(config.PARAM_HARDWARE_SETTING)
    time.sleep(2)
    click_by_png(config.PARAM_UI_SETTING)
    time.sleep(1)
    if if_auto_load_program:
        if search_symbol(config.SETTING_UI_AUTO_LOAD_PROGRAM_NO, 2):
            click_by_png(config.SETTING_UI_AUTO_LOAD_PROGRAM_NO)
    else:
        if search_symbol(config.SETTING_UI_AUTO_LOAD_PROGRAM_YES, 2):
            click_by_png(config.SETTING_UI_AUTO_LOAD_PROGRAM_YES)
    time.sleep(0.5)
    click_by_png(config.APPLY,timeout=1.5, tolerance=0.95)
    if search_symbol(config.NO, 1.5, tolerance=0.95):
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    else:
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    time.sleep(0.5)
    pyautogui.press('enter')
    while search_symbol(config.PARAM_SETTING_TOPIC):
        time.sleep(1.5)


        



# 【设置】-【硬件设置】-【UI配置】-【图像设置】搜索范围xy最大扩展： 最小设置0.8，搜索范围扩展x y:设置100%
def check_xy_max_extension():
    if search_symbol(config.SETTING_DARK, 1):
        click_by_png(config.SETTING_DARK)
    else:
        search_symbol_erroring(config.SETTING_LIGHT, 1)
    click_by_png(config.PARAM_HARDWARE_SETTING)
    time.sleep(2)
    click_by_png(config.PARAM_UI_SETTING)
    time.sleep(1)
    write_text((530, 90), "100")
    write_text((530, 115), "100")
    write_text((530, 145), "0.8")
    write_text((530, 170), "0.8")
    time.sleep(0.5)
    click_by_png(config.APPLY,timeout=1.5, tolerance=0.95)
    if search_symbol(config.NO, 1.5, tolerance=0.95):
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    else:
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    time.sleep(0.5)
    pyautogui.press('enter')
    while search_symbol(config.PARAM_SETTING_TOPIC):
        time.sleep(1.5)

#【设置】-【硬件设置】-【UI配置】-【软件界面】-不勾【不允许黏贴元件到元件】
def check_not_allow_paste_component_to_component(if_not_allow):
    if search_symbol(config.SETTING_DARK, 1):
        click_by_png(config.SETTING_DARK)
    else:
        search_symbol_erroring(config.SETTING_LIGHT, 1)
    click_by_png(config.PARAM_HARDWARE_SETTING)
    time.sleep(2)
    is_checked((1268, 846), (1280, 1005), if_not_allow)
    click_by_png(config.APPLY,timeout=1.5, tolerance=0.95)
    if search_symbol(config.NO, 1.5, tolerance=0.95):
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    else:
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    time.sleep(0.5)
    pyautogui.press('enter')
    while search_symbol(config.PARAM_SETTING_TOPIC):
        time.sleep(1.5)

#【设置】-【硬件设置】-【UI配置】-【软件界面】-不勾【不允许黏贴元件到空白处】
def check_not_allow_paste_component_to_blank(if_not_allow):
    if search_symbol(config.SETTING_DARK, 1):
        click_by_png(config.SETTING_DARK)
    else:
        search_symbol_erroring(config.SETTING_LIGHT, 1)
    click_by_png(config.PARAM_HARDWARE_SETTING)
    time.sleep(2)
    is_checked((1268, 872), (1280, 884), if_not_allow)
    click_by_png(config.APPLY,timeout=1.5, tolerance=0.95)
    if search_symbol(config.NO, 1.5, tolerance=0.95):
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    else:
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    time.sleep(0.5)
    pyautogui.press('enter')
    while search_symbol(config.PARAM_SETTING_TOPIC):
        time.sleep(1.5)

# 勾选 允许跨元件复制
def check_cross_component_copy():
    # 参数配置-UI配置-软件界面：选择【允许跨元件复制】
    if search_symbol(config.SETTING_DARK, 1):
        click_by_png(config.SETTING_DARK)
    else:
        search_symbol_erroring(config.SETTING_LIGHT, 1)
    click_by_png(config.PARAM_HARDWARE_SETTING)
    time.sleep(2)
    is_checked((1268, 993), (1280, 1005), True)
    click_by_png(config.APPLY,timeout=1.5, tolerance=0.95)
    if search_symbol(config.NO, 1.5, tolerance=0.95):
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    else:
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    time.sleep(0.5)
    pyautogui.press('enter')
    while search_symbol(config.PARAM_SETTING_TOPIC):
        time.sleep(1.5)


# 允许同步相同的封装,  默认同步封装
def check_not_sync_same_and_default_package(if_not_sync_same_package, if_default_sync_package):
    # 参数配置--UI配置--程序设置
    if search_symbol(config.SETTING_DARK, 1):
        click_by_png(config.SETTING_DARK)
    else:
        search_symbol_erroring(config.SETTING_LIGHT, 1)
    click_by_png(config.PARAM_HARDWARE_SETTING)
    time.sleep(2)
    click_by_png(config.PARAM_UI_SETTING)
    time.sleep(2)
    is_checked((659, 825), (671, 837), if_not_sync_same_package)
    is_checked((659, 849), (671, 861), if_default_sync_package)
    click_by_png(config.APPLY,timeout=1.5, tolerance=0.95)
    if search_symbol(config.NO, 1.5, tolerance=0.95):
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    else:
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    time.sleep(0.5)
    pyautogui.press('enter')
    while search_symbol(config.PARAM_SETTING_TOPIC):
        time.sleep(1.5)

def check_not_sync_same_package(if_not_sync_same_package):
    # 参数配置--UI配置--程序设置
    if search_symbol(config.SETTING_DARK, 1):
        click_by_png(config.SETTING_DARK)
    else:
        search_symbol_erroring(config.SETTING_LIGHT, 1)
    click_by_png(config.PARAM_HARDWARE_SETTING)
    time.sleep(2)
    click_by_png(config.PARAM_UI_SETTING)
    time.sleep(2)
    is_checked((659, 825), (671, 837), if_not_sync_same_package)
    click_by_png(config.APPLY,timeout=1.5, tolerance=0.95)
    if search_symbol(config.NO, 1.5, tolerance=0.95):
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    else:
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    time.sleep(0.5)
    pyautogui.press('enter')
    while search_symbol(config.PARAM_SETTING_TOPIC):
        time.sleep(1.5)


# 参数配置--硬件设置--数据导出配置--元件库--导入筛选限制
def check_import_filtering_restriction(percent):
    if search_symbol(config.SETTING_DARK, 3):
        click_by_png(config.SETTING_DARK)
    else:
        search_symbol_erroring(config.SETTING_LIGHT, 1)
    click_by_png(config.PARAM_HARDWARE_SETTING)
    time.sleep(2)
    click_by_png(config.PARAM_DATA_EXPORT_SETTING)
    time.sleep(2)
    write_text((1340,225), percent)
    time.sleep(1.5)
    click_by_png(config.APPLY,timeout=1.5, tolerance=0.95)
    if search_symbol(config.NO, 1.5, tolerance=0.95):
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    else:
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    time.sleep(0.5)
    pyautogui.press('enter')
    while search_symbol(config.PARAM_SETTING_TOPIC):
        time.sleep(1.5)


# 【设置】--【硬件设置】--【数据导出配置】--【元件库设置】--导出库后刷新树结构
def check_refresh_tree(if_fresh):
    if search_symbol(config.SETTING_DARK, 1):
        click_by_png(config.SETTING_DARK)
    else:
        search_symbol_erroring(config.SETTING_LIGHT, 1)
    click_by_png(config.PARAM_HARDWARE_SETTING)
    time.sleep(2)
    click_by_png(config.PARAM_DATA_EXPORT_SETTING)
    time.sleep(2)
    is_checked((1182, 123), (1194, 135), if_fresh)
    time.sleep(1)
    click_by_png(config.APPLY,timeout=1.5, tolerance=0.95)
    if search_symbol(config.NO, 1.5, tolerance=0.95):
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    else:
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    time.sleep(0.5)
    pyautogui.press('enter')
    while search_symbol(config.PARAM_SETTING_TOPIC):
        time.sleep(1.5)

# UI设置，演算法配置-点击开发者选项，输入密码：devsinictekaoi
def check_open_developer_options(type=None):
    if search_symbol(config.SETTING_DARK, 1):
        click_by_png(config.SETTING_DARK)
    else:
        search_symbol_erroring(config.SETTING_LIGHT, 1)
    click_by_png(config.PARAM_HARDWARE_SETTING)
    time.sleep(2)
    click_by_png(config.PARAM_ALGORITHM_SETTING)
    time.sleep(2)
    click_by_png(config.PARAM_ALGORITHM_DEVELOPER_OPTIONS)
    time.sleep(2)
    pyautogui.write("devsinictekaoi")
    pyautogui.press('enter')

    if type == "save_3d_data_yes":
        if search_symbol(config.DEVELOPER_OPTIONS_SAVE_3D_DATA_NO, 3):
            click_by_png(config.DEVELOPER_OPTIONS_SAVE_3D_DATA_NO)
    elif type == "save_3d_data_no":
        if search_symbol(config.DEVELOPER_OPTIONS_SAVE_3D_DATA_YES, 3):
            click_by_png(config.DEVELOPER_OPTIONS_SAVE_3D_DATA_YES)
    elif type == "save_check_data_yes":
        if search_symbol(config.DEVELOPER_OPTIONS_SAVE_CHECK_DATA_NO, 3):
            click_by_png(config.DEVELOPER_OPTIONS_SAVE_CHECK_DATA_NO)
    elif type == "save_check_data_no":
        if search_symbol(config.DEVELOPER_OPTIONS_SAVE_CHECK_DATA_YES, 3):
            click_by_png(config.DEVELOPER_OPTIONS_SAVE_CHECK_DATA_YES)

    click_by_png(config.DEVELOPER_OPTIONS_YES)
    time.sleep(1)
    click_by_png(config.APPLY,timeout=1.5, tolerance=0.95)
    if search_symbol(config.NO, 1.5, tolerance=0.95):
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    else:
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    time.sleep(0.5)
    pyautogui.press('enter')
    while search_symbol(config.PARAM_SETTING_TOPIC):
        time.sleep(1.5)


# 参数配置--演算法配置--关联子框检测模式
def check_patent_not_NG(type):
    if search_symbol(config.SETTING_DARK, 1):
        click_by_png(config.SETTING_DARK)
    else:
        search_symbol_erroring(config.SETTING_LIGHT, 1)
    click_by_png(config.PARAM_HARDWARE_SETTING)
    time.sleep(2)
    click_by_png(config.PARAM_ALGORITHM_SETTING)
    time.sleep(2)
    # 不计算
    if type == 1:
        pyautogui.click((935, 180))
        time.sleep(0.5)
        pyautogui.click((935, 200))
    # 继续计算
    if type == 2:
        pyautogui.click((935, 180))
        time.sleep(0.5)
        pyautogui.click((935, 215))
    # 继续关联
    if type == 3:
        pyautogui.click((935, 180))
        time.sleep(0.5)
        pyautogui.click((935, 230))
    click_by_png(config.APPLY,timeout=1.5, tolerance=0.95)
    if search_symbol(config.NO, 1.5, tolerance=0.95):
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    else:
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    time.sleep(0.5)
    pyautogui.press('enter')
    while search_symbol(config.PARAM_SETTING_TOPIC):
        time.sleep(1.5)

# 设置-硬件设置-演算法配置-勾选保存DJB文件
def check_save_djb(if_save_djb):
    if search_symbol(config.SETTING_DARK, 1):
        click_by_png(config.SETTING_DARK)
    else:
        search_symbol_erroring(config.SETTING_LIGHT, 1)
    click_by_png(config.PARAM_HARDWARE_SETTING)
    time.sleep(2)
    click_by_png(config.PARAM_ALGORITHM_SETTING)
    time.sleep(2)
    if if_save_djb:
        if search_symbol(config.SETTING_ALGORITHM_SAVE_DJB_NO):
            click_by_png(config.SETTING_ALGORITHM_SAVE_DJB_NO)
    else:
        if search_symbol(config.SETTING_ALGORITHM_SAVE_DJB_YES):
            click_by_png(config.SETTING_ALGORITHM_SAVE_DJB_YES)

    click_by_png(config.APPLY,timeout=1.5, tolerance=0.95)
    if search_symbol(config.NO, 1.5, tolerance=0.95):
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    else:
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    time.sleep(0.5)
    pyautogui.press('enter')
    while search_symbol(config.PARAM_SETTING_TOPIC):
        time.sleep(1.5)

# 设置-硬件设置-演算法配置-勾选所有算法（关闭所有算法）
def check_all_algs():
    if search_symbol(config.SETTING_DARK, 1):
        click_by_png(config.SETTING_DARK)
    else:
        search_symbol_erroring(config.SETTING_LIGHT, 1)
    click_by_png(config.PARAM_HARDWARE_SETTING)
    time.sleep(2)
    click_by_png(config.PARAM_ALGORITHM_SETTING)
    time.sleep(2)
    if search_symbol(config.SETTING_ALGORITHM_ALL_ALGS_NO, 3):
        click_by_png(config.SETTING_ALGORITHM_ALL_ALGS_NO)
        click_by_png(config.SETTING_ALGORITHM_MARK_MATCHING_YES)
        click_by_png(config.SETTING_ALGORITHM_BARCODE_DETECTION_YES)
    else:
        if search_symbol(config.SETTING_ALGORITHM_MARK_MATCHING_YES, 3):
            click_by_png(config.SETTING_ALGORITHM_MARK_MATCHING_YES)
        if search_symbol(config.SETTING_ALGORITHM_BARCODE_DETECTION_YES, 3):
            click_by_png(config.SETTING_ALGORITHM_BARCODE_DETECTION_YES)
    # 为了方便 勾选一下颜色分析
    if search_symbol(config.SETTING_ALGORITHM_COLOR_ANALYSE_NO, 3):
        click_by_png(config.SETTING_ALGORITHM_COLOR_ANALYSE_NO)

    click_by_png(config.APPLY,timeout=1.5, tolerance=0.95)
    if search_symbol(config.NO, 1.5, tolerance=0.95):
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    else:
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    time.sleep(0.5)
    pyautogui.press('enter')
    while search_symbol(config.PARAM_SETTING_TOPIC):
        time.sleep(1.5)

# 【设置】-【硬件设置】-【UI配置】-【软件界面】-不勾【自动选择窗口】
def check_auto_choose_window(if_auto_choose):
    if search_symbol(config.SETTING_DARK, 1):
        click_by_png(config.SETTING_DARK)
    else:
        search_symbol_erroring(config.SETTING_LIGHT, 1)
    click_by_png(config.PARAM_HARDWARE_SETTING)
    time.sleep(2)
    click_by_png(config.PARAM_UI_SETTING)
    time.sleep(2)
    is_checked((1268, 921), (1280, 933), if_auto_choose)
    click_by_png(config.APPLY,timeout=1.5, tolerance=0.95)
    if search_symbol(config.NO, 1.5, tolerance=0.95):
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    else:
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    time.sleep(0.5)
    pyautogui.press('enter')
    while search_symbol(config.PARAM_SETTING_TOPIC):
        time.sleep(1.5)


def check_export_ok(if_export_ok, if_export_all_ok):
    # 参数配置--UI配置--程序设置
    if search_symbol(config.SETTING_DARK, 1):
        click_by_png(config.SETTING_DARK)
    else:
        search_symbol_erroring(config.SETTING_LIGHT, 1)
    click_by_png(config.PARAM_HARDWARE_SETTING)
    time.sleep(2)
    click_by_png(config.PARAM_UI_SETTING)
    time.sleep(2)
    is_checked((659, 726), (671, 738), if_export_ok)
    is_checked((659, 751), (671, 763), if_export_all_ok)
    click_by_png(config.APPLY,timeout=1.5, tolerance=0.95)
    if search_symbol(config.NO, 1.5, tolerance=0.95):
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    else:
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    time.sleep(0.5)
    pyautogui.press('enter')
    while search_symbol(config.PARAM_SETTING_TOPIC):
        time.sleep(1.5)

# 导出相同料号新增序列号 【设置】--【硬件设置】--【数据导出配置】--【元件库设置】--导出相同料号新增序列号
def check_export_pn_add_sn(if_export_pn_add_sn):
    if search_symbol(config.SETTING_DARK, 1):
        click_by_png(config.SETTING_DARK)
    else:
        search_symbol_erroring(config.SETTING_LIGHT, 1)
    click_by_png(config.PARAM_HARDWARE_SETTING)
    time.sleep(2)
    click_by_png(config.PARAM_DATA_EXPORT_SETTING)
    time.sleep(2)
    is_checked((902, 145), (914, 157), if_export_pn_add_sn)
    time.sleep(1)
    click_by_png(config.APPLY,timeout=1.5, tolerance=0.95)
    if search_symbol(config.NO, 1.5, tolerance=0.95):
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    else:
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    time.sleep(0.5)
    pyautogui.press('enter')
    while search_symbol(config.PARAM_SETTING_TOPIC):
        time.sleep(1.5)

def check_allow_preview(if_allow):
    if search_symbol(config.SETTING_DARK, 1):
        click_by_png(config.SETTING_DARK)
    else:
        search_symbol_erroring(config.SETTING_LIGHT, 1)
    click_by_png(config.PARAM_HARDWARE_SETTING)
    time.sleep(2)
    click_by_png(config.PARAM_DATA_EXPORT_SETTING)
    time.sleep(2)
    is_checked((1182, 145), (1194, 157), if_allow)
    time.sleep(1)
    click_by_png(config.APPLY,timeout=1.5, tolerance=0.95)
    if search_symbol(config.NO, 1.5, tolerance=0.95):
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    else:
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    time.sleep(0.5)
    pyautogui.press('enter')
    while search_symbol(config.PARAM_SETTING_TOPIC):
        time.sleep(1.5)

#【设置】-【硬件设置】-【UI配置】-【图像设置】-【支持回退操作】
def check_allow_fallback(if_allow):
    if search_symbol(config.SETTING_DARK, 1):
        click_by_png(config.SETTING_DARK)
    else:
        search_symbol_erroring(config.SETTING_LIGHT, 1)
    click_by_png(config.PARAM_HARDWARE_SETTING)
    time.sleep(2)
    click_by_png(config.PARAM_UI_SETTING)
    time.sleep(2)
    is_checked((333, 541), (345, 553), if_allow)
    time.sleep(1)
    click_by_png(config.APPLY,timeout=1.5, tolerance=0.95)
    if search_symbol(config.NO, 1.5, tolerance=0.95):
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    else:
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    time.sleep(0.5)
    pyautogui.press('enter')
    while search_symbol(config.PARAM_SETTING_TOPIC):
        time.sleep(1.5)
    


# 【设置】-【硬件设置】-【UI配置】-【软件界面】-【允许跨元件复制】
def check_allow_copy_cross_component(if_allow):
    if search_symbol(config.SETTING_DARK, 1):
        click_by_png(config.SETTING_DARK)
    else:
        search_symbol_erroring(config.SETTING_LIGHT, 1)
    click_by_png(config.PARAM_HARDWARE_SETTING)
    time.sleep(2)
    click_by_png(config.PARAM_UI_SETTING)
    time.sleep(2)
    is_checked((1268, 993), (1280, 1005), if_allow)
    time.sleep(1)
    click_by_png(config.APPLY,timeout=1.5, tolerance=0.95)
    if search_symbol(config.NO, 1.5, tolerance=0.95):
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    else:
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    time.sleep(0.5)
    pyautogui.press('enter')
    while search_symbol(config.PARAM_SETTING_TOPIC):
        time.sleep(1.5)
# 勾选【设置】--【硬件设置】--【数据导出配置】--【元件库设置】--导出代料影像数，输入1
def check_export_wm_img_1():
    if search_symbol(config.SETTING_DARK, 1):
        click_by_png(config.SETTING_DARK)
    else:
        search_symbol_erroring(config.SETTING_LIGHT, 1)
    click_by_png(config.PARAM_HARDWARE_SETTING)
    time.sleep(2)
    click_by_png(config.PARAM_DATA_EXPORT_SETTING)
    time.sleep(2)
    write_text((1070, 225), '1')
    time.sleep(1)
    click_by_png(config.APPLY,timeout=1.5, tolerance=0.95)
    if search_symbol(config.NO, 1.5, tolerance=0.95):
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    else:
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    time.sleep(0.5)
    pyautogui.press('enter')
    while search_symbol(config.PARAM_SETTING_TOPIC):
        time.sleep(1.5)

# 勾选【设置】--【硬件设置】--【数据导出配置】--【元件库设置】--导出代料影像数，输入1，勾选所有
def check_export_wm_img_1_all(if_export_wm_img_1_all):
    if search_symbol(config.SETTING_DARK, 1):
        click_by_png(config.SETTING_DARK)
    else:
        search_symbol_erroring(config.SETTING_LIGHT, 1)
    click_by_png(config.PARAM_HARDWARE_SETTING)
    time.sleep(2)
    click_by_png(config.PARAM_DATA_EXPORT_SETTING)
    time.sleep(2)
    write_text((1070, 225), '1')
    time.sleep(1)
    is_checked((1131, 221), (1143, 233), if_export_wm_img_1_all)
    time.sleep(1)
    click_by_png(config.APPLY,timeout=1.5, tolerance=0.95)
    if search_symbol(config.NO, 1.5, tolerance=0.95):
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    else:
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    time.sleep(0.5)
    pyautogui.press('enter')
    while search_symbol(config.PARAM_SETTING_TOPIC):
        time.sleep(1.5)


# 导入库同步封装类型 【设置】--【硬件设置】--【数据导出配置】--【元件库设置】--导入库同步封装类型
def check_import_sync_package(if_import_sync_package):
    if search_symbol(config.SETTING_DARK, 1):
        click_by_png(config.SETTING_DARK)
    else:
        search_symbol_erroring(config.SETTING_LIGHT, 1)
    click_by_png(config.PARAM_HARDWARE_SETTING)
    time.sleep(2)
    click_by_png(config.PARAM_DATA_EXPORT_SETTING)
    time.sleep(2)
    is_checked((1182, 168), (1194, 180), if_import_sync_package)
    time.sleep(1)
    click_by_png(config.APPLY,timeout=1.5, tolerance=0.95)
    if search_symbol(config.NO, 1.5, tolerance=0.95):
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    else:
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    time.sleep(0.5)
    pyautogui.press('enter')
    while search_symbol(config.PARAM_SETTING_TOPIC):
        time.sleep(1.5)

# 勾选【设置】--【硬件设置】--【数据导出配置】--【元件库设置】--选择料号，输入天数1天
def check_pn_1_day():
    if search_symbol(config.SETTING_DARK, 1):
        click_by_png(config.SETTING_DARK)
    else:
        search_symbol_erroring(config.SETTING_LIGHT, 1)
    click_by_png(config.PARAM_HARDWARE_SETTING)
    time.sleep(2)
    click_by_png(config.PARAM_DATA_EXPORT_SETTING)
    time.sleep(2)
    is_checked((1182, 193), (1194, 205), True)
    time.sleep(1)
    write_text((1320, 200), '1')
    time.sleep(1)
    click_by_png(config.APPLY,timeout=1.5, tolerance=0.95)
    if search_symbol(config.NO, 1.5, tolerance=0.95):
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    else:
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    time.sleep(0.5)
    pyautogui.press('enter')
    while search_symbol(config.PARAM_SETTING_TOPIC):
        time.sleep(1.5)

# 勾选【设置】--【演算法配置】--【Component Lib Inspect Setting]--导入元件库删除OCV待料 
def check_import_delete_ocv_wm(if_delete):
    if search_symbol(config.SETTING_DARK, 1):
        click_by_png(config.SETTING_DARK)
    else:
        search_symbol_erroring(config.SETTING_LIGHT, 1)
    click_by_png(config.PARAM_HARDWARE_SETTING)
    time.sleep(2)
    click_by_png(config.PARAM_ALGORITHM_SETTING)
    time.sleep(2)
    is_checked((700, 243), (712, 255), if_delete)
    time.sleep(1)
    click_by_png(config.APPLY,timeout=1.5, tolerance=0.95)
    if search_symbol(config.NO, 1.5, tolerance=0.95):
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    else:
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    time.sleep(0.5)
    pyautogui.press('enter')
    while search_symbol(config.PARAM_SETTING_TOPIC):
        time.sleep(1.5)

# 【设置】--【演算法配置】--【演算法配置】--允许cad teach
def check_allow_cad_teach(if_allow):
    if search_symbol(config.SETTING_DARK, 1):
        click_by_png(config.SETTING_DARK)
    else:
        search_symbol_erroring(config.SETTING_LIGHT, 1)
    click_by_png(config.PARAM_HARDWARE_SETTING)
    time.sleep(2)
    click_by_png(config.PARAM_ALGORITHM_SETTING)
    time.sleep(2)
    is_checked((349, 374), (361, 386), if_allow)
    time.sleep(1)
    click_by_png(config.APPLY,timeout=1.5, tolerance=0.95)
    if search_symbol(config.NO, 1.5, tolerance=0.95):
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    else:
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    time.sleep(0.5)
    pyautogui.press('enter')
    while search_symbol(config.PARAM_SETTING_TOPIC):
        time.sleep(1.5)
# 【设置】--【数据导出配置】--【元件库设置】--导入更新元件高度
def check_import_update_height(if_update):
    if search_symbol(config.SETTING_DARK, 1):
        click_by_png(config.SETTING_DARK)
    else:
        search_symbol_erroring(config.SETTING_LIGHT, 1)
    click_by_png(config.PARAM_HARDWARE_SETTING)
    time.sleep(2)
    click_by_png(config.PARAM_DATA_EXPORT_SETTING)
    time.sleep(2)
    is_checked((902, 244), (914, 256), if_update)
    time.sleep(1)
    click_by_png(config.APPLY,timeout=1.5, tolerance=0.95)
    if search_symbol(config.NO, 1.5, tolerance=0.95):
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    else:
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    time.sleep(0.5)
    pyautogui.press('enter')
    while search_symbol(config.PARAM_SETTING_TOPIC):
        time.sleep(1.5)

# 【设置】--【数据导出配置】--【元件库设置】--导入更新元件x/y
def check_import_component_xy(if_update):
    if search_symbol(config.SETTING_DARK, 1):
        click_by_png(config.SETTING_DARK)
    else:
        search_symbol_erroring(config.SETTING_LIGHT, 1)
    click_by_png(config.PARAM_HARDWARE_SETTING)
    time.sleep(2)
    click_by_png(config.PARAM_DATA_EXPORT_SETTING)
    time.sleep(2)
    is_checked((902, 266), (914, 278), if_update)
    time.sleep(1)
    click_by_png(config.APPLY,timeout=1.5, tolerance=0.95)
    if search_symbol(config.NO, 1.5, tolerance=0.95):
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    else:
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    time.sleep(0.5)
    pyautogui.press('enter')
    while search_symbol(config.PARAM_SETTING_TOPIC):
        time.sleep(1.5)

# 【元件信息】--标准xyh前面的勾选框 注意：在编辑界面才可使用
def check_standard_xyh(if_checked):
    pyautogui.rightClick(config.CENTRE)
    time.sleep(1)
    click_by_png(config.COMPONENT_INFORMATION)
    time.sleep(1)
    is_checked((375, 574), (387, 586), if_checked)
    time.sleep(1)
    click_by_png(config.PROGRAM_ATTRIBUTE_CLOSE)
    time.sleep(1)

# 【设置】--【硬件设置】--【数据导出配置】--【元件库设置】--导出图像到元件库
def check_export_image_libs(if_export):
    if search_symbol(config.SETTING_DARK, 1):
        click_by_png(config.SETTING_DARK)
    else:
        search_symbol_erroring(config.SETTING_LIGHT, 1)
    click_by_png(config.PARAM_HARDWARE_SETTING)
    time.sleep(2)
    click_by_png(config.PARAM_DATA_EXPORT_SETTING)
    time.sleep(2)
    is_checked((902, 123), (914, 157), if_export)
    time.sleep(1)
    click_by_png(config.APPLY,timeout=1.5, tolerance=0.95)
    if search_symbol(config.NO, 1.5, tolerance=0.95):
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    else:
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    time.sleep(0.5)
    pyautogui.press('enter')
    while search_symbol(config.PARAM_SETTING_TOPIC):
        time.sleep(1.5)

# 【设置】--【数据导出配置】--【元件库设置】--过滤辅助窗口（3d基准面、板弯补偿算法）
def filter_auxiliary_window(if_filter):
    if search_symbol(config.SETTING_DARK, 1):
        click_by_png(config.SETTING_DARK)
    else:
        search_symbol_erroring(config.SETTING_LIGHT, 1)
    click_by_png(config.PARAM_HARDWARE_SETTING)
    time.sleep(2)
    click_by_png(config.PARAM_DATA_EXPORT_SETTING)
    time.sleep(2)
    is_checked((902, 194), (914, 206), if_filter)
    time.sleep(1)
    click_by_png(config.APPLY,timeout=1.5, tolerance=0.95)
    if search_symbol(config.NO, 1.5, tolerance=0.95):
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    else:
        click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    time.sleep(0.5)
    pyautogui.press('enter')
    while search_symbol(config.PARAM_SETTING_TOPIC):
        time.sleep(1.5)

def modify_component():
    time.sleep(2)
    pyautogui.press("b")
    time.sleep(5)
    pyautogui.keyDown('left')
    time.sleep(2)
    pyautogui.keyUp('left')

# ================================================文件处理=====================================
# 确认是否文件夹下生成了新数据
def check_new_data(path):
    # 检查文件夹内所有文件和子文件夹
    recent_creations = []
    all_files_and_dirs = []
    for root, dirs, files in os.walk(path):
        for name in files + dirs:
            # 获取文件或文件夹的完整路径
            full_path = os.path.join(root, name)
            # 获取文件或文件夹的创建时间
            ctime = os.path.getctime(full_path)
            # 记录检测到的文件或文件夹及其创建时间
            logger.debug(f"检测到文件或文件夹：{full_path}，创建时间：{ctime}")
            all_files_and_dirs.append(full_path)
            # 如果文件或文件夹在指定的时间内被创建
            if time.time() - ctime < 120:
                recent_creations.append(full_path)
    logger.info(f"路径 {path} 下的所有文件和文件夹: {all_files_and_dirs}")
    if recent_creations:
        logger.info(f"最近创建的文件或文件夹: {recent_creations}")
        return True
    else:
        logger.info("没有最近创建的文件或文件夹")
        return False
def check_data_amount(path):
    a = 0
    for filename in os.listdir(path):
        a += 1
    return a


# 将剪切板内的内容与文件夹内内容作对比
def check_amount_content(coordinate, path):
    # 读内容至剪切板
    read_text_choosed(coordinate[0], coordinate[1])
    clipboard_content = pyperclip.paste()
    lines = clipboard_content.split('\n')

    if not lines:
        raise Exception("剪切板内容为空")

    # 提取第一行的数字
    try:
        expected_count = int(lines[0].strip())
    except Exception:
        raise Exception("第一行不包含有效的数字")

    # 获取文件夹中的所有文件名
    files = os.listdir(path)
    # 过滤掉Default文件夹
    files = [file for file in files if "Default" not in file]
    # 检查每一行内容是否存在于文件夹中的某个文件名中(需要忽略Default文件夹)
    matched_files = []
    for line in lines[1:]:  # 从第二行开始，因为第一行是数字
        found = False
        for file in files:
            if line in file:
                matched_files.append(file)
                found = True
                break
        if not found:
            print(f"没有找到匹配的文件：{line}")

    # 检查文件总数是否与第一行数字一致
    actual_count = len(matched_files)

    if actual_count == expected_count:
        print("文件数量匹配成功")
    else:
        print(f"文件数量不匹配：期望 {expected_count}, 实际 {actual_count}")


ALL_COMPONENTS = []


# 获取程式元件列表
def get_component_list():
    global ALL_COMPONENTS
    time.sleep(3)
    # 注意首次加载板的时候出现的和后续加载时的面板不同
    # 首次加载应该识别程式元件 点击后打开
    # 点击程式元件面板
    search_symbol(config.PROGRAM_COMPONENT_DARK, 60)
    time.sleep(5)
    click_by_controls(config.PROGRAM_COMPONENT_DARK, 2)
    time.sleep(0.3)
    confidence_level = 0.9
    try:
        # 识别未检测的元件坐标并保存，标记为no_checked
        no_checked_components = list(
            pyautogui.locateAllOnScreen(config.NO_CHECKED_COMPONENT, confidence=confidence_level))
        no_checked_positions = [{'x': pos.left, 'y': pos.top, 'status': 'no_checked', 'seen': False} for pos in
                                no_checked_components]
    except pyautogui.ImageNotFoundException:
        no_checked_positions = []
        logger.info("未检测的元件图像未找到。")

    try:
        # 识别已检测的元件坐标并保存，标记为checked
        checked_components = list(pyautogui.locateAllOnScreen(config.CHECKED_COMPONENT, confidence=confidence_level))
        checked_positions = [{'x': pos.left, 'y': pos.top, 'status': 'checked', 'seen': False} for pos in
                             checked_components]
    except pyautogui.ImageNotFoundException:
        checked_positions = []
        logger.info("已检测的元件图像未找到。")
    # 更新全局变量all_components
    ALL_COMPONENTS = no_checked_positions + checked_positions


# 获取选择框
def get_choose_box():
    logger.info("开始获取选择框")
    # 定位中心点附近的黄色方块
    center_x, center_y = 935, 445
    search_region = (center_x - 393, center_y - 148, 786, 296)  # 更新搜索区域
    screenshot = pyautogui.screenshot(region=search_region)
    image = np.array(screenshot)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 定义黄色的HSV范围
    lower_yellow = np.array([30, 255, 255])
    upper_yellow = np.array([30, 255, 255])

    # 根据阈值构建掩模
    mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)

    # 寻找轮廓
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # 过滤小轮廓
    yellow_blocks = [cv2.boundingRect(cnt) for cnt in contours if cv2.contourArea(cnt) > 6]
    logger.info(yellow_blocks)
    # 检查找到的方块数量
    if len(yellow_blocks) == 8:
        # 按照距离中心点的距离排序
        yellow_blocks.sort(key=lambda pos: (pos[0] + pos[2] // 2 - center_x + search_region[0]) ** 2 + (
                pos[1] + pos[3] // 2 - center_y + search_region[1]) ** 2)
        logger.info(yellow_blocks)
        # 选择第5个最近的方块
        target_block = yellow_blocks[4]  # 选择第五个最近的方块，索引为4
        target_x = target_block[0] + target_block[2] // 2 + search_region[0]
        target_y = target_block[1] + target_block[3] // 2 + search_region[1]
        screen_width, screen_height = pyautogui.size()
        screen_target_x = target_x * screen_width / 1920
        screen_target_y = target_y * screen_height / 1080
        target = (screen_target_x, screen_target_y)
        logger.debug(target)
        return True, target
    elif len(yellow_blocks) == 4:
        # 随机选择一个方块
        target_block = random.choice(yellow_blocks)
        target_x = target_block[0] + target_block[2] // 2 + search_region[0]
        target_y = target_block[1] + target_block[3] // 2 + search_region[1]
        screen_width, screen_height = pyautogui.size()
        screen_target_x = target_x * screen_width / 1920
        screen_target_y = target_y * screen_height / 1080
        target = (screen_target_x, screen_target_y)
        logger.debug(target)
        return True, target
    elif len(yellow_blocks) > 0:
        return True, None
    else:
        return False, None

# 扩大算法框
def expand_choose_box(point=config.CENTRE):
    # 获取选择框
    success, target = get_choose_box()
    if success and target is not None:
        # 左键点击按住方块中心点
        pyautogui.mouseDown(target)
        time.sleep(0.5)
        # 计算拖拽方向，远离中心点
        direction_x = target[0] - point[0]
        direction_y = target[1] - point[1]
        move_x = 50 if direction_x >= 0 else -50
        move_y = 50 if direction_y >= 0 else -50
        # 往远离中心点的方向拖拽50单位
        pyautogui.moveRel(move_x, move_y, duration=1)
        time.sleep(0.5)
        # 松开鼠标
        pyautogui.mouseUp()
    else:
        logger.debug(f"Success: {success}, Target: {target}")
        logger.error("未能成功获取选择框，随机选择一个黄色点拖曳")
        # 选择region.COMPONENT_OPERATION_REGION内任一rgb为（255，255，0)的点
        yellow_point = get_color_direction_coordinate((255, 255, 0), config.COMPONENT_OPERATION_REGION, 'left')
        if yellow_point is not None:
            # 左键点击按住黄色点
            pyautogui.mouseDown(yellow_point)
            time.sleep(0.5)
            # 计算拖拽方向，远离中心点
            direction_x = yellow_point[0] - point[0]
            direction_y = yellow_point[1] - point[1]
            move_x = 50 if direction_x >= 0 else -50
            move_y = 50 if direction_y >= 0 else -50
            # 往远离中心点的方向拖拽50单位
            pyautogui.moveRel(move_x, move_y, duration=1)
            time.sleep(0.5)
            # 松开鼠标
            pyautogui.mouseUp()
        else:
            logger.error("未能找到黄色点")
# 获取color颜色在某个区域最靠某个方向的像素点的基于全屏的坐标点
def get_color_direction_coordinate(color, region, direction):
    # 截取指定区域的屏幕 (保留RGB格式)
    screenshot = pyautogui.screenshot(region=region)
    screenshot = np.array(screenshot)
    
    # 精确颜色匹配（可以增加一点点容差进行调试）
    lower_color = np.array([color[0] - 1, color[1] - 1, color[2] - 1])
    upper_color = np.array([color[0] + 1, color[1] + 1, color[2] + 1])
    
    # 生成颜色掩码
    mask = cv2.inRange(screenshot, lower_color, upper_color)
    
    # 获取非零像素点的坐标
    coords = cv2.findNonZero(mask)
    
    if coords is None:
        logger.error("未找到指定颜色的像素点")
        return None
    
    # 根据方向选择最靠近的像素点
    if direction == 'left':
        target_coord = min(coords, key=lambda x: x[0][0])
    elif direction == 'right':
        target_coord = max(coords, key=lambda x: x[0][0])
    elif direction == 'up':
        target_coord = min(coords, key=lambda x: x[0][1])
    elif direction == 'down':
        target_coord = max(coords, key=lambda x: x[0][1])
    else:
        raise Exception("get_color_direction_coordinate传参有问题")
    
    # 返回全屏的坐标 (直接加上区域的起始坐标)
    screen_x = target_coord[0][0] + region[0]
    screen_y = target_coord[0][1] + region[1]
    
    return screen_x, screen_y
# 计算该区域内颜色为rgb的像素点的数量
def get_color_in_region(color, region):
    # 截取指定区域的屏幕
    screenshot = pyautogui.screenshot(region=region)
    screenshot = np.array(screenshot)
    
    # 不需要颜色空间转换，直接处理RGB颜色
    # screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR) # 可以省略这一行
    
    # 设置颜色范围，增加小容差 ±1
    lower_color = np.array([color[0] - 1, color[1] - 1, color[2] - 1])
    upper_color = np.array([color[0] + 1, color[1] + 1, color[2] + 1])
    
    # 生成颜色掩码，只有匹配的像素值会被设置为255，其他为0
    mask = cv2.inRange(screenshot, lower_color, upper_color)
    
    # 计算匹配颜色的像素点数量
    pixel_count = cv2.countNonZero(mask)
    
    return pixel_count

# 识别屏幕上是否存在指定文字
def detect_text(target_text):
    # 截取屏幕
    screenshot = pyautogui.screenshot()

    # 将截图转换为OpenCV格式
    screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # 使用EasyOCR识别文字
    reader = easyocr.Reader(['ch_sim'])
    result = reader.readtext(screenshot_cv, detail=0)

    # 检查是否包含目标文字
    for text in result:
        similarity = SequenceMatcher(None, target_text, text).ratio()
        if similarity >= 0.66:
            logger.info(f"识别到与“{target_text}”相似的文字：{text}")
            return text  # 返回识别到的文字

    logger.info(f"未识别到与“{target_text}”相似的文字")
    return None

# 检查文字前面的勾选框状态 TODO
def check_checkbox_status_before_text(target_text):
    # 截取屏幕
    screenshot = pyautogui.screenshot()

    # 将截图转换为OpenCV格式
    screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # 使用EasyOCR识别文字
    reader = easyocr.Reader(['ch_sim'])
    result = reader.readtext(screenshot_cv, detail=0)

    # 检查是否包含目标文字
    for text in result:
        similarity = SequenceMatcher(None, target_text, text).ratio()
        if similarity >= 0.66:
            logger.info(f"识别到与“{target_text}”相似的文字：{text}")
            return True

    logger.info(f"未识别到与“{target_text}”相似的文字")
    return False

# 调整将CAD框随机变大，再变小
def adjust_cad_frame():
    search_symbol(config.EDIT_BACK, 10)
    time.sleep(2)
    # 选中框框快捷键
    pyautogui.press('b')
    logger.info("选中检测框")
    time.sleep(1.5)
    success, point = get_choose_box()
    logger.info(point)
    # 识别到完整的选择框
    if success:
        if point is not None:
            logger.info("move")
            x, y = point
            logger.info(x, y)
            pyautogui.moveTo(x, y, duration=0.5)
            pyautogui.mouseDown()
            # 计算区域边界
            left_bound, top_bound, width, height = 540, 150, 1327 - 540, 738 - 150
            right_bound = left_bound + width
            bottom_bound = top_bound + height

            # 计算到边界的最小距离
            min_dist_to_left = point[0] - left_bound
            min_dist_to_right = right_bound - point[0]
            min_dist_to_top = point[1] - top_bound
            min_dist_to_bottom = bottom_bound - point[1]

            # 选择最小距离并计算随机移动距离
            min_dist = min(min_dist_to_left, min_dist_to_right, min_dist_to_top, min_dist_to_bottom)
            move_dist = random.randint(1, min_dist)

            # 确定移动方向
            if min_dist == min_dist_to_left:
                move_x = -move_dist
                move_y = 0
            elif min_dist == min_dist_to_right:
                move_x = move_dist
                move_y = 0
            elif min_dist == min_dist_to_top:
                move_x = 0
                move_y = -move_dist
            else:
                move_x = 0
                move_y = move_dist

            # 执行扩大选择框操作
            pyautogui.moveRel(move_x, move_y, duration=2)
            time.sleep(0.5)
            pyautogui.mouseUp()
            # 最大点
            big_x, big_y = pyautogui.position()
            time.sleep(1)
            # 执行缩小选择框操作
            center_x, center_y = 935, 445
            pyautogui.moveTo(big_x, big_y)
            pyautogui.mouseDown()
            move_to_center_x = random.randint(0, abs(center_x - big_x))
            move_to_center_y = random.randint(0, abs(center_y - big_y))
            if center_x < big_x:
                move_to_center_x = -move_to_center_x
            if center_y < big_y:
                move_to_center_y = -move_to_center_y
            target = (move_to_center_x, move_to_center_y)
            pyautogui.moveRel(target[0], target[1], duration=1)
            pyautogui.mouseUp()
        # TODO 识别到不完整的选择框 估计是选择框出界了
        else:
            pass
    else:
        sys.exit("未识别到选择框")


def random_choose_light():
    # 绝对坐标列表（1920x1080分辨率）
    absolute_coords = [
        (555, 315), (555, 450), (555, 580), (555, 715),
        (680, 315), (680, 450), (680, 580),
        (820, 315), (820, 450), (820, 580),
    ]
    # 获取当前屏幕分辨率
    screen_width, screen_height = pyautogui.size()
    # 将绝对坐标转换为相对坐标
    relative_coords = [
        (int(x * screen_width / 1920), int(y * screen_height / 1080)) for x, y in absolute_coords
    ]
    # 随机选择一个坐标
    chosen_coord = random.choice(relative_coords)
    # 单击选中的坐标
    pyautogui.click(chosen_coord)

def random_open_program():
    # 先检测有没有什么傻逼窗口 关掉
    if search_symbol(config.NO, 1.5):
        click_by_png(config.NO, tolerance=0.9)
    pyautogui.press('enter')
    click_by_png(config.OPEN_PROGRAM)
    if search_symbol(config.NO, 3):
        click_by_png(config.NO, tolerance=0.9)
    time.sleep(3)
    options = [config.OPEN_PROGRAM_CURSOR, config.OPEN_PROGRAM_PLUS]
    found = False
    for option in random.sample(options, len(options)):  # 随机排序尝试
        if search_symbol(option, 2):
            click_by_png(option, 2)
            found = True
            break
    if not found:
        raise Exception("打开程式界面没有搜索到程式")
    time.sleep(1)
    click_by_png(config.YES)
    while search_symbol(config.PROGRAM_LOADING):
        time.sleep(5)
    time.sleep(3)

# 算法参数面板随机改变值(缩小即无效)
def random_change_param(if_test=0):
    # 分为两种改随机的方式:
    # 下拉框为面积内随机选（点击点，输入各个下拉框面积，下拉随机值（限定范围），随机选面积内一点点击，但麻烦）


    # 先点击算法 根据算法点不同的点
    # 使用for循环点击各个点，输入0-500随机数字
    alg_modes = {
        config.CW_COLOR_ANALYSISING: config.CW_COLOR_ANALYSISING_POINTS,
        config.CW_COLOR_MATCHING: config.CW_COLOR_MATCHING_POINTS,
        config.CW_IMAGE_MATCHING: config.CW_IMAGE_MATCHING_POINTS,
        config.CW_COLOR_AREA: config.CW_COLOR_AREA_POINTS,
        config.CW_SQUARE_POSITIONING: config.CW_SQUARE_POSITIONING_POINTS,
        config.CW_PIN_SIMILARITY_MATCHING: config.CW_PIN_SIMILARITY_MATCHING_POINTS,
    }

    found = False
    for mode, points in alg_modes.items():
        if search_symbol(mode, region=config.COMPONENT_WINDOW_REGION):
            click_by_png(mode, region=config.COMPONENT_WINDOW_REGION)
            time.sleep(8)
            found = True
            break

    if not found:
        return False
    # 修改参数
    for point in points:
        pyautogui.doubleClick(point)
        random_number = random.randint(0, 500)
        pyautogui.typewrite(str(random_number))
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(0.5)
        pyautogui.press('enter')
    # 点击测试窗口/元件/分组/整版
    start_time = time.time()
    test_config = {
        1: (config.TEST_WINDOW, 3),
        2: (config.TEST_COMPONENT, 10),
        3: (config.TEST_GROUP, 20),
        4: (config.TEST_BOARD, 20)
    }

    if if_test in test_config:
        click_by_png(test_config[if_test][0], test_config[if_test][1])
        if if_test > 1:  # 对于2, 3, 4的情况需要进行循环检测
            while True:
                if not search_symbol(config.TESTING_COMPONENT, 5, tolerance=0.8):
                    break
                if time.time() - start_time > 600:  # 超过十分钟
                    raise Exception("程序一直处于测试元件中")
                elif time.time() - start_time > 300:  # 超过五分钟
                    for proc in psutil.process_iter(['name']):
                        if "Sinic-Tek" in proc.info['name'] and "NEW" in proc.info['name']:
                            proc.terminate()  # 关闭进程
                time.sleep(5)
        time.sleep(5)
    else:
        return
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('enter')
    return True

    
# 添加标准影像的参数面板
def random_change_image_param():
    points = config.IMAGE_PARAM_POINTS
    for point in points:
        time.sleep(1.5)
        pyautogui.doubleClick(point)
        time.sleep(0.5)
        random_number = random.randint(0, 80)
        pyautogui.typewrite(str(random_number))
        time.sleep(0.5)
        pyautogui.press('enter')

# 随机修改rgb值
def random_change_rgb():
    #对(835,825) (835,870) (835,915) (835,950)
    points = [(835, 825), (835, 870), (835, 915), (835, 950)]
    for point in points:
        pyautogui.click(point)
        time.sleep(20)
        pyautogui.hotkey('ctrl', 'a')
        random_number = random.randint(0, 255)
        time.sleep(10)
        pyautogui.typewrite(str(random_number))
    pyautogui.press('enter')
    time.sleep(10)


# ==========================工具类======================
# =========================excel=======================
def adjust_image_size(image_path, max_width, max_height):
    try:
        with PILImage.open(image_path) as img:
            original_width, original_height = img.size
            ratio = min(max_width / original_width, max_height / original_height)
            new_width = int(original_width * ratio)
            new_height = int(original_height * ratio)
            return new_width, new_height
    except Exception as e:
        logger.error(f"Error adjusting image size for {image_path}: {e}")
        return None, None

def insert_image_limited(ws, cell, image_path, max_width=75, max_height=75):
    if os.path.exists(image_path):
        new_width, new_height = adjust_image_size(image_path, max_width, max_height)
        if new_width is None or new_height is None:
            cell.value = "错误"
            return
        img = ExcelImage(image_path)
        img.width = new_width
        img.height = new_height
        img.anchor = cell.coordinate
        ws.add_image(img)
        cell.value = ""
    else:
        cell.value = "空"
        logger.debug(f"图片路径不存在: {image_path}")

# 图片适应屏幕分辨率
def image_fit_screen(image_path):
    # 获取当前屏幕分辨率
    screen_width, screen_height = pyautogui.size()
    if screen_width == 1920 and screen_height == 1080:
        return image_path
    else:
        logger.error("屏幕宽度: {}, 屏幕高度: {}", screen_width, screen_height)
        # 打开图像文件
        img = PILImage.open(image_path)
        # 调整图像大小到当前屏幕分辨率
        img = img.resize((int(img.width * screen_width / 1920), int(img.height * screen_height / 1080)),
                        PILImage.Resampling.LANCZOS)
        # 确定项目根目录
        project_root = os.path.dirname(os.path.abspath(__file__))  # 假设此脚本位于项目根目录
        temp_dir = os.path.join(project_root, 'temp')
        # 如果temp文件夹不存在，则创建它
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        # 构建临时文件路径
        filename = os.path.basename(image_path)  # 获取原始图像的文件名
        temp_image_path = os.path.join(temp_dir, f"temp_{filename}")  # 在temp目录下创建新的文件名
        temp_image_path = os.path.normpath(temp_image_path)
        img.save(temp_image_path)
        return temp_image_path

def points_are_similar(points1, points2, max_error=10):
    if len(points1) != len(points2):
        return False
    for p1, p2 in zip(points1, points2):
        if abs(p1[0] - p2[0]) > max_error or abs(p1[1] - p2[1]) > max_error:
            return False
    return True
# 确保指定位置内是该文本
def text_in_bbox(text, bbox):
    # 点击输入框
    center_x = (bbox[0] + bbox[2]) / 2
    center_y = (bbox[1] + bbox[3]) / 2
    pyautogui.click(center_x, center_y)
    time.sleep(0.5)  # 等待点击生效

    # 全选并复制
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')

    # 读取剪贴板内容
    clipboard_text = pyperclip.paste()

    # 检查剪贴板内容是否包含预期文本
    if text not in clipboard_text:
        pyautogui.typewrite(text)
        pyautogui.press('enter')


def compare_images(img1, img2):
    return ImageChops.difference(img1, img2).getbbox() is None


# ========================处理数据=============================
# 坐标系调整
def adjust_coordinates(top_left, bottom_right, base_resolution=(1920, 1080)):
    # 获取当前屏幕分辨率
    monitor = get_monitors()[0]
    current_resolution = (monitor.width, monitor.height)

    # 计算坐标调整比例
    x_ratio = current_resolution[0] / base_resolution[0]
    y_ratio = current_resolution[1] / base_resolution[1]

    # 调整坐标
    adjusted_top_left = (int(top_left[0] * x_ratio), int(top_left[1] * y_ratio))
    adjusted_bottom_right = (int(bottom_right[0] * x_ratio), int(bottom_right[1] * y_ratio))

    return adjusted_top_left, adjusted_bottom_right

# 检查A、B或C是否大部分存在于all_content中，支持substring内可能有错别字
def contains(substring, full_string, threshold=0.8):
    # 去除换行符并分割成多行
    substring_lines = substring.replace('\n', ' ').split()
    full_string = full_string.replace('\n', ' ')
    
    for line in substring_lines:
        # 先找到最相近的那一段
        best_match = max(full_string.split(), key=lambda x: SequenceMatcher(None, line, x).ratio())
        matcher = SequenceMatcher(None, line, best_match)
        match_ratio = matcher.ratio()
        logger.debug(f"Comparing line: {line} with best_match: {best_match}, match ratio: {match_ratio}")
        if match_ratio >= threshold:
            return True
    
    # 如果没有一行匹配度超过阈值，检查所有行的平均匹配度
    total_ratio = sum(SequenceMatcher(None, line, full_string).ratio() for line in substring_lines) / len(substring_lines)
    logger.debug(f"Total match ratio: {total_ratio}")
    return total_ratio >= threshold

def get_center_coordinates(coord1, coord2):
    """
    计算两个坐标点的中心坐标。
    :param coord1: 第一个坐标点 (x1, y1)
    :param coord2: 第二个坐标点 (x2, y2)
    :return: 中心坐标 (x, y)
    """
    x_center = (coord1[0] + coord2[0]) // 2
    y_center = (coord1[1] + coord2[1]) // 2
    return (x_center, y_center)
def get_frame_points(region, color):
    try:
        logger.info(f"开始截取区域: {region}")
        screenshot = pyautogui.screenshot(region=region)
        screenshot_np = np.array(screenshot)
        screenshot_hsv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2HSV)

        # 将 RGB 颜色转换为 HSV 颜色
        color_hsv = cv2.cvtColor(np.uint8([[color]]), cv2.COLOR_RGB2HSV)[0][0]
        logger.info(f"目标颜色的HSV值: {color_hsv}")

        # 定义颜色的HSV范围，只找color这个rgb
        lower_bound = np.array([color_hsv[0] - 5, color_hsv[1] - 5, color_hsv[2] - 5])
        upper_bound = np.array([color_hsv[0] + 5, color_hsv[1] + 5, color_hsv[2] + 5])
        logger.info(f"颜色范围: {lower_bound} - {upper_bound}")

        # 创建颜色掩码
        mask = cv2.inRange(screenshot_hsv, lower_bound, upper_bound)

        # 使用形态学操作增强边界
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=5)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=5)

        # 寻找连贯区域的轮廓
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            raise Exception("未找到指定颜色的框")

        # 调试：显示检测到的轮廓
        # contour_img = cv2.drawContours(screenshot_np.copy(), contours, -1, (0, 255, 0), 2)
        # cv2.imshow("Contours", contour_img)
        # cv2.waitKey(0)

        # 假设只有一个框，获取其四个对角点
        logger.info(f"检测到的框的数量: {len(contours)}")
        contour = max(contours, key=cv2.contourArea)

        # 使用多边形逼近算法
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # 获取轮廓的顶点 
        points = approx.reshape(-1, 2)
        points_fullscreen = [(point[0] + region[0], point[1] + region[1]) for point in points]
        logger.debug(points_fullscreen)
        if len(points_fullscreen) == 8:
            merged_points = []
            pairs = [(0, 7), (1, 2), (3, 4), (5, 6)]
            for i, j in pairs:
                x_center = (points_fullscreen[i][0] + points_fullscreen[j][0]) // 2
                y_center = (points_fullscreen[i][1] + points_fullscreen[j][1]) // 2
                merged_points.append((x_center, y_center))
            points_fullscreen = merged_points
        
        # 在屏幕上显示各个点的位置
        if len(points_fullscreen) == 4:
            for point in points_fullscreen:
                cv2.circle(screenshot_np, point, 5, (0, 0, 255), -1)
                cv2.putText(screenshot_np, f"{point}", (point[0] + 10, point[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
            
            # 调整窗口大小以显示所有点
            height, width, _ = screenshot_np.shape
            # cv2.namedWindow("AAA", cv2.WINDOW_NORMAL)
            # cv2.resizeWindow("AAA", width, height)
            # cv2.imshow("AAA", screenshot_np)
            # cv2.waitKey(0)
        else:
            logger.error("未能检测到四个顶点")
        return points_fullscreen
    except Exception as e:
        logger.error(f"获取框的坐标时发生错误: {e}")
        raise

# # 获取文本位置并确认其左侧勾选框勾选状态并作勾选操作
# def get_text_and_check_checkbox(image_path, text, checkbox_image_path, checkbox_checked_image_path=None):
#
#
#










def write_text(coordinate, text, if_select_all=True):
    
    pyautogui.click(coordinate)
    time.sleep(0.5)
    if if_select_all:   
        pyautogui.click(coordinate, clicks=2, interval=0.1)
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.5)
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')
def write_text_textbox(image_path, text, color=(255, 255, 255), direction="right", locate_direction="left", if_select_all=True):
    try:
        logger.debug(f"开始处理图片: {image_path}, 方向: {direction}, 颜色: {color}, 识别方向: {locate_direction}")
        time.sleep(2)
        
        # 获取图片在屏幕上的位置
        symbol = image_fit_screen(image_path)
        logger.info(f"开始寻找 {symbol}")
        
        try:
            locations = list(pyautogui.locateAllOnScreen(symbol, confidence=0.95))
            if locations:
                if locate_direction == "left":
                    location = min(locations, key=lambda loc: loc.left)
                elif locate_direction == "right":
                    location = max(locations, key=lambda loc: loc.left)
                elif locate_direction == "top":
                    location = min(locations, key=lambda loc: loc.top)
                elif locate_direction == "bottom":
                    location = max(locations, key=lambda loc: loc.top)
                logger.debug(f"图片位置: {location}")
            else:
                raise Exception("未找到指定的图片")
        except pyautogui.ImageNotFoundException:
            raise Exception("未找到指定的图片")
        except Exception as e:
            logger.error(f"发生异常: {e}")
            raise Exception(f"发生异常: {e}")

        # 获取颜色为 color 的区域，基于 location 的中心点，按方向搜索
        x, y, width, height = map(int, [location.left, location.top, location.width, location.height])
        center_x = x + width // 2
        center_y = y + height // 2
        logger.debug(f"识别标识的中心点坐标: ({center_x}, {center_y})")

        # 根据方向设置搜索区域，确保范围合适
        if direction == "right":
            # 向右：从 location 的右边界开始，限制为上下边界范围
            screenshot = pyautogui.screenshot(region=(x + width, y, 1920 - (x + width), height))
        elif direction == "left":
            # 向左：从 location 的左边界开始，限制为上下边界范围
            screenshot = pyautogui.screenshot(region=(0, y, x, height))
        elif direction == "above":
            # 向上：从 location 的上边界开始，限制为左右边界范围
            screenshot = pyautogui.screenshot(region=(x, 0, width, y))
        elif direction == "below":
            # 向下：从 location 的下边界开始，限制为左右边界范围
            screenshot = pyautogui.screenshot(region=(x, y + height, width, 1080 - (y + height)))
        else:
            raise Exception("无效的方向参数")

        # 转换截图为 numpy 数组并进行颜色匹配
        screenshot_np = np.array(screenshot)
        lower_bound = np.array(color) - 10
        upper_bound = np.array(color) + 10
        mask = cv2.inRange(screenshot_np, lower_bound, upper_bound)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            raise Exception("未找到指定颜色的区域")
        logger.debug(f"找到的轮廓数量: {len(contours)}")

        # 过滤掉较小的轮廓
        min_contour_area = 50  # 设置最小轮廓面积阈值
        contours = [contour for contour in contours if cv2.contourArea(contour) > min_contour_area]
        if not contours:
            raise Exception("未找到符合条件的颜色区域")
        logger.debug(f"过滤后的轮廓数量: {len(contours)}")

        # 可视化调试：在屏幕上显示所有识别到的轮廓
        # debug_image = screenshot_np.copy()
        # cv2.drawContours(debug_image, contours, -1, (0, 255, 0), 2)
        # cv2.imshow("All Contours", debug_image)
        # cv2.waitKey(0)

        # 获取离标识最近的颜色为 color 的区域
        def get_distance_to_center(contour):
            M = cv2.moments(contour)
            if M["m00"] == 0:
                return float('inf')
            contour_center_x = int(M["m10"] / M["m00"])
            contour_center_y = int(M["m01"] / M["m00"])
            return contour_center_x, contour_center_y

        # 记录所有轮廓的中心点和距离标识中心点的距离
        for contour in contours:
            contour_center_x, contour_center_y = get_distance_to_center(contour)
            screen_contour_center_x = x + contour_center_x
            screen_contour_center_y = y + contour_center_y
            distance_x = abs(screen_contour_center_x - center_x)
            distance_y = abs(screen_contour_center_y - center_y)
            logger.debug(f"轮廓中心点: ({screen_contour_center_x}, {screen_contour_center_y}), 距离标识中心点的横向距离: {distance_x}, 纵向距离: {distance_y}")

        # 查找离中心点300范围内的颜色区域
        if direction in ["right", "left"]:
            valid_contours = [c for c in contours if abs(x + get_distance_to_center(c)[0] - center_x) <= 300 and abs(x + get_distance_to_center(c)[0] - center_x) > 15]
            if not valid_contours:
                raise Exception("未找到300范围内的颜色区域")
            if direction == "right":
                closest_contour = min(valid_contours, key=lambda c: x + get_distance_to_center(c)[0])
            else: 
                closest_contour = max(valid_contours, key=lambda c: x + get_distance_to_center(c)[0])
            distance = abs(x + get_distance_to_center(closest_contour)[0] - center_x)
            logger.debug(f"基于X轴中心点判断，距离为: {distance}")
        elif direction in ["above", "below"]:
            valid_contours = [c for c in contours if abs(y + get_distance_to_center(c)[1] - center_y) <= 300 and abs(y + get_distance_to_center(c)[1] - center_y) > 15]
            if not valid_contours:
                raise Exception("未找到300范围内的颜色区域")
            if direction == "above":
                closest_contour = max(valid_contours, key=lambda c: y + get_distance_to_center(c)[1])
            else:
                closest_contour = min(valid_contours, key=lambda c: y + get_distance_to_center(c)[1])
            distance = abs(y + get_distance_to_center(closest_contour)[1] - center_y)
            logger.debug(f"基于Y轴中心点判断，距离为: {distance}")

        # 获取轮廓B的中心点
        M = cv2.moments(closest_contour)
        if M["m00"] != 0:
            contour_center_x = int(M["m10"] / M["m00"])
            contour_center_y = int(M["m01"] / M["m00"])
            
            # 根据相对位置计算在全屏中的坐标
            full_screen_center_x = x + contour_center_x
            full_screen_center_y = y + contour_center_y
            logger.info(f"识别到的轮廓中心点的全屏坐标: ({full_screen_center_x}, {full_screen_center_y})")

            # 可视化调试：在屏幕上显示选择的轮廓
            debug_image_selected = screenshot_np.copy()
            cv2.drawContours(debug_image_selected, [closest_contour], -1, (255, 0, 0), 2)
            cv2.imshow("Selected Contour", debug_image_selected)
            cv2.waitKey(0)

            # 检查距离是否超过200
            if distance > 200:
                detected_color = screenshot_np[contour_center_y, contour_center_x]
                logger.error(f"找到的区域与标识距离超过200, 坐标: ({full_screen_center_x}, {full_screen_center_y}), 颜色: {detected_color}")
                raise Exception("找到的区域与标识距离超过200")

            # 将文本写入该区域B的中心点
            write_text((full_screen_center_x, full_screen_center_y), text, if_select_all)
            logger.info(f"写入完毕，内容为：{text}")
        else:
            raise Exception("未找到合适的颜色区域")
    except Exception as e:
        logger.error(f"处理图片时发生错误: {e}")
        raise


def read_text(x, y):
    # 获取当前屏幕分辨率
    monitor = get_monitors()[0]
    current_resolution = (monitor.width, monitor.height)

    # 计算坐标调整比例
    x_ratio = current_resolution[0] / 1920
    y_ratio = current_resolution[1] / 1080

    # 调整坐标
    adjusted_x = int(x * x_ratio)
    adjusted_y = int(y * y_ratio)

    # 单击调整后的坐标
    pyautogui.click(adjusted_x, adjusted_y)

    # 全选并复制
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')

    # 读取剪贴板内容
    clipboard_text = pyperclip.paste()

    return clipboard_text


# 由于部分控件无法直接ctrl+a 被迫用这种方式去读取内容
def read_text_choosed(x, y):
    # 左键按住x，y的坐标点
    pyautogui.moveTo(x, y)
    pyautogui.mouseDown()

    # 鼠标拖到指定位置后松开
    pyautogui.moveTo(1900, 1025)
    pyautogui.mouseUp()

    # 复制到剪切板
    pyautogui.hotkey('ctrl', 'c')


# 点击选中颜色
def click_color(times, region, target_color_rgb=(239, 240, 242), right_click=0):
    # 截取区域内的屏幕图像
    screenshot = pyautogui.screenshot(region=region)
    screenshot_np = np.array(screenshot)
    # 寻找颜色匹配的像素点
    matches = np.where(np.all(screenshot_np == target_color_rgb, axis=-1))
    if matches[0].size > 0:
        # 随机获取一个匹配的点的坐标
        random_index = random.randint(0, len(matches[0]) - 1)
        x, y = matches[1][random_index], matches[0][random_index]
        # 转换为区域内的相对坐标
        x += region[0]
        y += region[1]
        logger.info("找到目标点"+str(x)+","+str(y))
        # 如果times为0，则只移动鼠标不点击
        if times == 0:
            pyautogui.moveTo(x, y)
            return True
        # 点击指定次数
        for _ in range(times):
            # 获取目标点周围的随机一个像素点
            offset_x = random.randint(-1, 1)
            offset_y = random.randint(-1, 1)
            click_x = x + offset_x
            click_y = y + offset_y
            if right_click == 1:
                pyautogui.rightClick(click_x, click_y)
            else:
                pyautogui.click(click_x, click_y)
        return True
    logger.info("未找到匹配的像素点")
    return False
# 计算坐标点附近range像素点范围内 颜色为color的像素点个数
def count_color_in_range(coordinate, range, color):
    screenshot = pyautogui.screenshot()
    screenshot_np = np.array(screenshot)
    start_x, start_y = coordinate[0] - range, coordinate[1] - range
    end_x, end_y = coordinate[0] + range, coordinate[1] + range
    matches = np.where(np.all(screenshot_np[start_y:end_y, start_x:end_x] == color, axis=-1))
    logger.info(f"找到的像素点数量: {len(matches[0])}")
    return len(matches[0])
# 获取鼠标指针处的颜色
def get_mouse_color(mouse_coordinate):
    screenshot = pyautogui.screenshot()
    screenshot_np = np.array(screenshot)
    target_color_rgb = screenshot_np[mouse_coordinate[1], mouse_coordinate[0]]
    return target_color_rgb

# 比较两张图片是否相同（转为灰度图像）
def compare_images(image1, image2):
    # 将截图转换为灰度图像
    image1_gray = image1.convert('L')
    image2_gray = image2.convert('L')

    # 使用ImageChops.difference来比较图像差异
    diff = ImageChops.difference(image1_gray, image2_gray)

    # 如果差异图像的极值为0，说明两张图像相同
    return diff.getbbox() is None

# 矫正识别结果的错别字，并处理冒号后的文本
def correct_typos(text):
    target_texts = ["检测窗口", "未完待续", "错件"]
    matched_texts = []
    for target_text in target_texts:
        match_count = 0
        # 检查输入文本与目标文本的每个字符
        for char in text:
            if char in target_text:
                match_count += 1
        # 如果匹配的字符数达到1个或以上，则记录目标文本
        if match_count >= 1:
            matched_texts.append(target_text)
    # 如果有匹配的文本，则返回所有匹配的文本，否则返回原始文本
    result_texts = matched_texts if matched_texts else text

    # 处理冒号后的文本
    if ':' in text:
        result_texts = text.split(':', 1)[1]

    return result_texts
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


# # 识别屏幕上指定区域
# def read_text_ocr(top_left_point, bottom_right_point, color="black"):
#     logger.info("开始识别文字")
#     # 截取屏幕上指定区域的图像，并打印截图区域
#     bbox = (top_left_point[0], top_left_point[1], bottom_right_point[0], bottom_right_point[1])
#     screenshot = ImageGrab.grab(bbox=bbox)
#     screenshot_np = np.array(screenshot)
#     # 调用颜色过滤方法，过滤为指定颜色
#     have_specific_color, filtered_image = filter_color(screenshot_np, color)
#     if not have_specific_color:
#         logger.error("指定颜色未在截图中找到")
#         return "未找到指定颜色"

#     # 使用EasyOCR进行文字识别，首先尝试识别英文
#     reader = easyocr.Reader(['en', 'ch_sim'], gpu=False)  # 同时加载英文和简体中文模型，禁用GPU加速以提高兼容性
#     results = reader.readtext(filtered_image, detail=1, paragraph=True)  # 启用段落模式以提高识别连贯性
#     # 输出识别结果
#     recognized_text = ' '.join([text for (bbox, text, prob) in results])
#     corrected_text = correct_typos(recognized_text)  # 使用correct_typos函数矫正识别结果
#     logger.info(f"识别的文字: {corrected_text}")

#     return corrected_text

def read_text_ocr(top_left_point, bottom_right_point):
    logger.info("开始识别文字")
    # 截取屏幕上指定区域的图像，并打印截图区域
    bbox = (top_left_point[0], top_left_point[1], bottom_right_point[0], bottom_right_point[1])
    screenshot = ImageGrab.grab(bbox=bbox)

    # 使用EasyOCR进行文字识别，首先尝试识别英文和简体中文
    reader = easyocr.Reader(['en', 'ch_sim'], gpu=False)  # 同时加载英文和简体中文模型，禁用GPU加速以提高兼容性
    results = reader.readtext(np.array(screenshot), detail=1, paragraph=True)  # 启用段落模式以提高识别连贯性

    # 安全地提取文本，考虑到可能的不同元组长度
    recognized_text = ''.join([text for item in results for text in (item[1] if len(item) > 1 else [])])

    # 使用correct_typos函数矫正识别结果
    corrected_text = correct_typos(recognized_text)
    logger.info(f"识别的文字: {corrected_text}")

    return corrected_text

# 在区域内下滚，直到滚到底（鼠标位置，识别区域）
def scroll_down(coordinate, region, scroll_amount=None):
    if scroll_amount is not None:
        # 如果有传入入参，滑动入参的值后就停止
        pyautogui.moveTo(coordinate)
        pyautogui.scroll(scroll_amount)
        return
    else:
        scroll_amount = -400
        while True:
            # 截取初始区域截图
            region_last_time = pyautogui.screenshot(region=region)
            # 下滚指定单位
            pyautogui.moveTo(coordinate)
            pyautogui.scroll(scroll_amount)
            time.sleep(1)  # 等待滚动完成
            
            # 截取当前区域截图
            region_current_time = pyautogui.screenshot(region=region)
            if compare_images(region_current_time, region_last_time):
                return True
            else:
                region_last_time = region_current_time





# 下拉框，选择所需要的图/文字(参数名意思：图 0 /文字 1 图片路径/识别的文字  区域)
def drop_down_box_search(type, content, region, click_times=1, timeout=6, similarity_threshold=0.8):
    # 根据类型选择操作
    if type == 0:
        # 搜索并点击图片
        start_time = time.time()
        while time.time() - start_time < timeout:
            found = search_symbol(content, region=region, timeout=1)
            if found:
                click_by_png(content, region=region, times=click_times)
                pyautogui.press("enter")
                return True
            else:
                # 鼠标移到region最右侧中间
                right_edge_x = region[0] + region[2]
                middle_y = region[1] + region[3] / 2
                pyautogui.moveTo(right_edge_x, middle_y)
                pyautogui.scroll(-200)  # 再下滚
        return False
    elif type == 1:
        # 使用OCR搜索并点击文字
        reader = easyocr.Reader(['ch_sim', 'en'])  # 使用中文简体和英文的模型
        start_time = time.time()
        while time.time() - start_time < timeout:
            # 截取指定区域的屏幕
            screenshot = pyautogui.screenshot(region=region)
            results = reader.readtext(np.array(screenshot))
            # 遍历识别结果，寻找目标文字
            for result in results:
                bbox, text_found, prob = result
                if similar(content, text_found) >= similarity_threshold:
                    top_left = bbox[0]
                    bottom_right = bbox[2]
                    x = (top_left[0] + bottom_right[0]) / 2
                    y = (top_left[1] + bottom_right[1]) / 2

                    full_x = region[0] + x
                    full_y = region[1] + y

                    for _ in range(click_times):
                        pyautogui.click(full_x, full_y)
                    pyautogui.press("enter")
                    return True
            # 如果没有找到匹配的文字，将鼠标移到区域的最右侧并向下滚动200单位
            right_edge_x = region[0] + region[2]
            middle_y = region[1] + region[3] / 2
            pyautogui.moveTo(right_edge_x, middle_y)
            pyautogui.scroll(-200)
        return False

# =====================================文件处理=====================================
# 删除文件夹下所有文件
def delete_documents(path):
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)




