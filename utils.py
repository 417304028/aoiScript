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
import os
import re
from pywinauto import Application, Desktop
from PIL import ImageGrab, Image
from PIL import ImageChops
from screeninfo import get_monitors
from loguru import logger
from openpyxl import Workbook, load_workbook
from openpyxl.drawing.image import Image as ExcelImage

ctypes.windll.shcore.SetProcessDpiAwareness(0)  # 解决使用pyautowin时缩放问题


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
    # app = Application().connect(title_re=u".*Sinic-Tek 3D AOI.*",
    #                             auto_id="MainForm")
    # top_window = app.window(auto_id="MainForm")
    # top_window.wait('ready', timeout=10)
    # time.sleep(0.3)
    # if top_window.exists():
    #     logger.info("成功连接到aoi窗口")
    #     return top_window
    # else:
    #     raise Exception
    try:
        # app = Application(backend="uia").connect(auto_id="MainForm")
        windows = Desktop(backend="uia").windows()
        window_found = False
        pattern = re.compile(r".*Sinic-Tek 3D AOI.*")  # 正则表达式匹配包含 "Sinic-Tek 3D AOI" 的标题
        aoi_amount = 0
        for w in windows:
            if pattern.match(w.window_text()):
                window_properties = w.get_properties()
                logger.info(f"aoi窗口存在,详细信息：{window_properties}")
                window_found = True
                aoi_amount += 1
                # break
        logger.info(f"aoi窗口数量: {aoi_amount}")
        if not window_found:  # 如果循环结束后标志仍为False，表示没有找到窗口
            logger.error("aoi窗口不存在")
        if window_found:
            app = Application().connect(title_re=".*Sinic-Tek 3D AOI.*")
            main_window = app.window(auto_id="MainForm")
            if main_window.exists(timeout=10):
                logger.info("成功连接到窗口")
                return main_window
            else:
                logger.error("未找到窗口")
    except Exception as e:
        logger.error(f"连接窗口时发生错误: {e}")


# 确保aoi打开并前置
def check_and_launch_aoi():
    aoi_running = any("AOI.exe" == p.name() for p in psutil.process_iter())
    if not aoi_running:
        logger.info("AOI程序未运行,正在启动...")
        app = Application().start(config.AOI_EXE_PATH)
        logger.info("等待AOI程序启动...")
        app.window(title_re=".*AOI.*").wait('ready', timeout=60)
        search_symbol_erroring(config.AOI_TOPIC, 30)
    else:
        main_window = connect_aoi_window()
        main_window.wait('ready', timeout=10)
        main_window.set_focus()
        main_window.wait('ready', timeout=10)
        search_symbol_erroring(config.AOI_TOPIC, 20)
        # 确保窗口未最小化并且前置
        if main_window.is_minimized():
            main_window.restore()
        main_window.set_focus()  # 再次确保窗口前置
        # 获取窗口句柄
        hwnd = main_window.handle
        win32gui.SetForegroundWindow(hwnd)
        # 确保窗口不被最大化或改变大小
        rect = win32gui.GetWindowRect(hwnd)
        win32gui.MoveWindow(hwnd, rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1], True)











        # # 确保窗口未最小化
        # if main_window.is_minimized():
        #     main_window.restore()
        #     logger.info("窗口已恢复")
        # # 确保窗口最大化
        # if not main_window.is_maximized():
        #     main_window.maximize()
        #     logger.info("窗口已最大化")
        # # 获取窗口句柄
        # hwnd = main_window.handle
        # win32gui.SetForegroundWindow(hwnd)
        # win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
        # logger.info(hwnd)
        # win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        # logger.info("窗口已置顶")


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
        if not main_window.is_visible():
            raise Exception("AOI程序窗口不可见，可能已经崩溃")

        # 检测程序是否响应
        if not main_window.is_enabled():
            raise Exception("AOI程序无响应，可能已经卡顿")

        logger.info("AOI程序运行正常，无卡顿或闪退")
    except Exception as e:
        logger.error(f"检测到程序异常: {e}")
        raise


# ==============================识别处理===============================
# 寻找准星
def get_crosshair_center():
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
        logger.info("全屏准星位置:", (cx, cy))
        return (cx, cy)
    else:
        logger.error("未找到准星")
        raise Exception("未找到准星")


# 检测屏幕是否有大量某个颜色
def check_color_expand():
    # 捕获屏幕截图
    screenshot = ImageGrab.grab()
    screenshot_np = np.array(screenshot)

    # 定义目标颜色和容差
    target_color = np.array([190, 156, 159])  # 注意：OpenCV使用BGR格式
    tolerance = 15  # 容差值

    # 计算颜色范围
    lower_bound = target_color - tolerance
    upper_bound = target_color + tolerance

    # 创建掩码
    mask = cv2.inRange(screenshot_np, lower_bound, upper_bound)

    # 计算掩码中的白色像素比例
    coverage = np.sum(mask) / (screenshot_np.shape[0] * screenshot_np.shape[1] * 255)

    # 判断是否有大量的目标颜色
    if coverage > 0.075:  # 假设我们定义“大量”为覆盖超过7.5%的屏幕
        logger.info("元件四周遮罩出现大量粉色")
        return True
    else:
        logger.info("元件四周遮罩未出现大量粉色")
        return False


def if_checked(top_left, bottom_right):
    # 调整坐标
    adjusted_top_left, adjusted_bottom_right = adjust_coordinates(top_left, bottom_right)

    # 截取屏幕上的复选框区域
    screenshot = ImageGrab.grab(
        bbox=(adjusted_top_left[0], adjusted_top_left[1], adjusted_bottom_right[0], adjusted_bottom_right[1]))
    screenshot_np = np.array(screenshot)
    screenshot_np = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

    # 将图像转换为灰度图
    gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)

    # 使用自适应阈值方法
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    # 计算白色像素的数量（勾选标记）
    white_pixels = np.sum(thresh == 255)

    # 判断是否勾选（根据白色像素是否超过一定阈值）
    pixel_threshold = 42  # 根据实际情况调整阈值
    check = (white_pixels >= pixel_threshold)

    # 为了调试，显示处理后的图像
    # cv2.imshow('Threshold Image', thresh)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return check

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


def click_by_png(image_path, times=1, timeout=20, if_click_right=0, tolerance=0.8, region=None):
    start_time = time.time()
    clicked = False  # 添加一个标志来检测是否成功点击
    image_path = image_fit_screen(image_path)
    logger.info(f"尝试点击图片: {image_path}")
    while time.time() - start_time < timeout:
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=tolerance, region=region)
            if location:
                # 计算中心坐标
                center_x = location.left + location.width // 2
                center_y = location.top + location.height // 2
                if if_click_right == 1:
                    pyautogui.click(center_x, center_y, button='right')
                else:
                    pyautogui.click(center_x, center_y, clicks=times)
                logger.info(f"点击{image_path}成功")
                clicked = True  # 更新标志为True表示成功点击
                break
        except Exception as e:
            pass
        time.sleep(0.5)
    if not clicked:  # 检查是否成功点击
        logger.error(f"超时: 在{timeout}秒内未能点击{image_path}")
        raise Exception(f"超时: 在{timeout}秒内未能点击{image_path}")


def search_symbol(symbol, timeout=10, region=None, tolerance=0.9):
    start_time = time.time()
    symbol = image_fit_screen(symbol)
    logger.info(f"开始寻找{symbol}")
    if timeout != 0:
        while time.time() - start_time < timeout:
            try:
                # 使用confidence参数来设置匹配的近似度
                location = pyautogui.locateOnScreen(symbol, region=region, confidence=tolerance)
                if location is not None:
                    logger.info("已确认" + symbol + "存在")
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
                location = pyautogui.locateOnScreen(symbol, region=region, confidence=tolerance)
                if location is not None:
                    logger.info("已确认" + symbol + "存在")
                    return True
        except pyautogui.ImageNotFoundException:
            return False
        except Exception as e:
            logger.error(f"发生异常: {e}")
            raise Exception(f"发生异常: {e}")


def search_symbol_erroring(symbol, timeout = 10, region=None):
    start_time = time.time()
    symbol = image_fit_screen(symbol)
    logger.info(f"开始寻找:{symbol}")
    if timeout != 0:
        while time.time() - start_time < timeout:
            try:
                if pyautogui.locateOnScreen(symbol, region=region) is not None:
                    logger.info("已确认" + symbol + "存在")
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
                if pyautogui.locateOnScreen(symbol, region=region) is not None:
                    logger.info("已确认" + symbol + "存在")
                    return True
        except pyautogui.ImageNotFoundException:
            raise Exception(f"没找到图片: {symbol}")
        except Exception as e:
            logger.error(f"发生异常: {e}")
            raise Exception(f"发生异常: {e}")


# =========================装饰器=========================

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


# 装饰器，出问题时截图并保存至excel
def screenshot_error_to_excel(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        max_attempts = 2  # 设置最大尝试次数
        attempts = 0
        while attempts < max_attempts:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                attempts += 1
                current_function_name = func.__name__
                path = sys.executable
                screenshot_to_excel(current_function_name, path, e)
                logger.error(f"发生异常: {e}")

                # 杀死AOI进程
                for proc in psutil.process_iter(['pid', 'name']):
                    if "AOI" in proc.info['name']:
                        proc.kill()
                        proc.wait()  # 等待进程确实被杀死

                # 确保所有AOI进程都已经关闭
                aoi_still_running = any("AOI" in p.info['name'] for p in psutil.process_iter(['name']))
                if not aoi_still_running:
                    logger.info("所有AOI进程已关闭")
                #     check_and_launch_aoi()
                else:
                    logger.error("AOI进程关闭失败")

                # if attempts >= max_attempts:
                #     raise  # 可选：重新抛出异常以便外部也能知道异常发生
                # else:
                #     time.sleep(10)  # 给系统一点时间来处理进程重启

    return wrapper


# ====================业务处理========================
# 添加待料
def add_waiting_material():
    for _ in range(3):
        click_by_png(config.ADD_STANDARD_IMAGE)
        click_by_png(config.IMAGE_PROCESS_YES)
        if search_symbol(config.ADD_IMAGE_CLOSE, 5):
            click_by_png(config.ADD_IMAGE_CLOSE)


# 画检测窗口
def add_window(button="w"):
    time.sleep(1.5)
    crosshair_center = get_crosshair_center()
    if crosshair_center is None:
        logger.info("未找到准星中心")
        return

    nearby_point = (crosshair_center[0] + 3, crosshair_center[1] + 3)
    logger.info(nearby_point)
    # 绘制框框（获取准星旁边的颜色，扩大到颜色分界处，截取坐标）
    target_color = pyautogui.screenshot().getpixel(nearby_point)
    # 转换颜色到HSV
    target_color_hsv = cv2.cvtColor(np.uint8([[target_color]]), cv2.COLOR_RGB2HSV)[0][0]
    # 定义颜色的HSV范围，初始范围
    hue_variation = 5
    saturation_variation = 10
    value_variation = 10
    found = False
    last_top_left = None
    last_bottom_right = None

    while not found:
        lower_bound = np.array([target_color_hsv[0] - hue_variation, target_color_hsv[1] - saturation_variation,
                                target_color_hsv[2] - value_variation])
        upper_bound = np.array([target_color_hsv[0] + hue_variation, target_color_hsv[1] + saturation_variation,
                                target_color_hsv[2] + value_variation])
        # 截取整个屏幕图像
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)
        screenshot_hsv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2HSV)
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
        target_contour = None
        for contour in contours:
            if cv2.pointPolygonTest(contour, nearby_point, False) >= 0:
                target_contour = contour
                found = True
                break
            # 如果找到了符合条件的连贯区域
        if target_contour is not None:
            x, y, w, h = cv2.boundingRect(target_contour)
            # 扩大区域
            expand_margin = 10
            top_left = (x - expand_margin, y - expand_margin)
            bottom_right = (x + w + expand_margin, y + h + expand_margin)
            last_top_left = top_left
            last_bottom_right = bottom_right
            logger.info("找到疑似cad区域，左上及右下坐标如下" + str(top_left) + "," + str(bottom_right))
        else:
            # 增加HSV范围并重试
            hue_variation += 1
            saturation_variation += 2
            value_variation += 2
            if hue_variation > 180 or saturation_variation > 255 or value_variation > 255:
                logger.info("未识别出cad区域，可能准心不在cad内")
                break

    if last_top_left and last_bottom_right:
        # 使用pyautogui模拟鼠标拖动
        pyautogui.press(button)
        pyautogui.moveTo(last_top_left, duration=1)
        pyautogui.mouseDown()
        pyautogui.moveTo(last_bottom_right, duration=1)
        pyautogui.mouseUp()
        logger.info("cad描边完毕")
    else:
        logger.info("未找到任何区域")


# 打开程式(随机)
def open_program():
    click_by_png(config.OPEN_PROGRAM)
    # 双击程式
    if search_symbol(config.OPEN_PROGRAM_PLUS, 5):
        click_by_png(config.OPEN_PROGRAM_PLUS, 2)
        click_by_png(config.OPEN_PROGRAM_YES)
        return
    if search_symbol(config.OPEN_PROGRAM_CURSOR, 5):
        click_by_png(config.OPEN_PROGRAM_CURSOR, 2)
        click_by_png(config.OPEN_PROGRAM_YES)
        return


# 获取最近编辑的一个程式
def get_topest_program():
    cursor_positions = list(pyautogui.locateAllOnScreen(config.CURSOR))
    plus_positions = list(pyautogui.locateAllOnScreen(config.PLUS))
    all_positions = cursor_positions + plus_positions
    if all_positions:
        topest = sorted(all_positions, key=lambda pos: pos.top)[0]
    else:
        logger.error("未找到任何cursor或plus的坐标")
        raise Exception("未找到任何cursor或plus的坐标")

    return topest


# 确保在编辑界面
def ensure_in_edit_mode():
    # 先立刻马上打开程式元件栏
    found_light = search_symbol(config.PROGRAM_COMPONENT_LIGHT, 0)
    found_dark = search_symbol(config.PROGRAM_COMPONENT_DARK, 0)

    if found_light or found_dark:
        if found_dark:
            click_by_png(config.PROGRAM_COMPONENT_DARK)
        click_component()
    else:
        open_program()
        if search_symbol(config.BOARD_AUTO, 50):
            if search_symbol(config.PROGRAM_COMPONENT_DARK, 30):
                time.sleep(3)
                click_by_png(config.PROGRAM_COMPONENT_DARK)
        click_component()
    time.sleep(5)
    click_by_png(config.EDIT_DARK)

# 确保打开了有多个拼版的job
def ensure_multiple_collages():
    check_and_launch_aoi()
    click_by_png(config.OPEN_PROGRAM)
    # 搜索并点击屏幕上所有＋
    plus_positions = list(pyautogui.locateAllOnScreen(config.OPEN_PROGRAM_PLUS))
    a = 0
    for pos in plus_positions:
        pyautogui.doubleClick(pos)
        time.sleep(0.5)
        math = read_text_ocr((1055, 748), (1070, 762))
        if math != 1:
            a += 1
            click_by_png(config.OPEN_PROGRAM_LOAD)
            click_by_png(config.OPEN_PROGRAM_YES)
            break
    if a == 0:
        logger.error("未找到多个拼版的job")
        raise Exception("未找到多个拼版的job")


# 点击元件
def click_component():
    # 几种元件里点一个
    if search_symbol(config.NO_CHECKED_COMPONENT, 2):
        click_by_png(config.NO_CHECKED_COMPONENT, 2)
        return True
    else:
        if search_symbol(config.CHECKED_COMPONENT, 2):
            click_by_png(config.CHECKED_COMPONENT, 2)
            return True
        else:
            if search_symbol(config.PASS_COMPONENT, 2):
                click_by_png(config.PASS_COMPONENT, 2)
                return True
            else:
                if search_symbol(config.NO_PASS_COMPONENT, 2):
                    click_by_png(config.NO_PASS_COMPONENT, 2)
                    return True
                else:
                    raise

# 检测屏幕区域(362,149)至(1506,739)区域内是否存在(220,20,60)的颜色
def check_window_relate():
    # 定义要检测的颜色
    target_color = (220, 20, 60)
    # 定义检测区域
    region = (362, 149, 1506 - 362, 739 - 149)
    # 在指定区域内搜索颜色
    found = pyautogui.pixelMatchesColor(region[0], region[1], target_color, region=region)
    return found


# 勾选共享元件库路径
def check_share_lib_path(if_checked):
    # 点开设置--硬件设置--数据导出配置--元件库配置
    click_by_png(config.SETTING_DARK)
    click_by_png(config.PARAM_HARDWARE_SETTING)
    click_by_png(config.PARAM_DATA_EXPORT_SETTING)
    time.sleep(2)
    # 确保共享元件库路径为勾选状态 （用的坐标）
    is_checked((902, 291), (914, 303), if_checked, 1)
    time.sleep(1)
    click_by_png(config.PARAM_SETTING_YES,2)
    click_by_png(config.CLOSE)
    time.sleep(1.5)


# 勾选 允许跨元件复制
def check_cross_component_copy():
    # 参数配置-UI配置-软件界面：选择【允许跨元件复制】
    click_by_png(config.SETTING_DARK)
    click_by_png(config.PARAM_HARDWARE_SETTING)
    click_by_png(config.PARAM_UI_SETTING)
    time.sleep(1)
    is_checked((1268, 993), (1280, 1005), True)
    click_by_png(config.PARAM_SETTING_YES)
    click_by_png(config.CLOSE)


# 允许同步相同的封装,  默认同步封装
def check_sync_package(if_sync_same_package, if_default_sync_package):
    # 参数配置--UI配置--程序设置
    click_by_png(config.SETTING_DARK)
    click_by_png(config.PARAM_HARDWARE_SETTING)
    click_by_png(config.PARAM_UI_SETTING)
    time.sleep(1)
    is_checked((659, 852), (671, 864), if_sync_same_package)
    is_checked((659, 876), (671, 888), if_default_sync_package)
    click_by_png(config.PARAM_SETTING_YES)
    click_by_png(config.CLOSE)


# 参数配置--演算法配置--关联子框检测模式
def check_patent_not_NG(type):
    if search_symbol(config.SETTING_DARK, 1):
        click_by_png(config.SETTING_DARK)
    else:
        search_symbol_erroring(config.SETTING_LIGHT, 1)
    click_by_png(config.PARAM_HARDWARE_SETTING)
    click_by_png(config.PARAM_ALGORITHM_SETTING)
    # 不计算
    if type == 1:
        pyautogui.click((935, 180))
        pyautogui.click((935, 200))
    # 继续计算
    if type == 2:
        pyautogui.click((935, 180))
        pyautogui.click((935, 215))
    # 继续关联
    if type == 3:
        pyautogui.click((935, 180))
        pyautogui.click((935, 230))
    click_by_png(config.PARAM_SETTING_YES)
    click_by_png(config.CLOSE)


def check_export_ok(if_export_ok, if_export_all_ok):
    # 参数配置--UI配置--程序设置
    click_by_png(config.SETTING_DARK)
    click_by_png(config.PARAM_HARDWARE_SETTING)
    click_by_png(config.PARAM_UI_SETTING)
    time.sleep(1)
    is_checked((659, 726), (671, 738), if_export_ok)
    is_checked((659, 751), (671, 763), if_export_all_ok)
    click_by_png(config.PARAM_SETTING_YES)
    click_by_png(config.CLOSE)


def modify_component():
    pyautogui.press("b")
    pyautogui.keyDown('left')
    time.sleep(2)
    pyautogui.keyUp('left')


# 确认是否文件夹下生成了新数据
def check_new_data(path):
    for filename in os.listdir(path):
        # 获取文件的完整路径
        file_path = os.path.join(path, filename)
        # 获取文件的修改时间
        file_mtime = os.path.getmtime(file_path)
        # 如果文件在指定的时间内被修改或创建
        if time.time() - file_mtime < 10:
            return True
        else:
           return False


# 计算文件夹内data数量
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
        target = (target_x, target_y)
        logger.info(target_x, target_y)
        return True, target
    elif len(yellow_blocks) > 0:
        return True, None
    else:
        return False, None


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


# 算法参数面板随机改变值(缩小即无效)
def random_change_param():
    # 分为两种改随机的方式:
    # 下拉框为面积内随机选（点击点，输入各个下拉框面积，下拉随机值（限定范围），随机选面积内一点点击，但麻烦）
    # 使用for循环点击各个点，输入0-1000随机数字
    points = config.ALG_PARAM_POINTS
    for point in points:
        pyautogui.doubleClick(point)
        random_number = random.randint(0, 500)
        pyautogui.typewrite(str(random_number))
        
# 添加标准影像的参数面板
def random_change_image_param():
    points = config.IMAGE_PARAM_POINTS
    for point in points:
        time.sleep(1.5)
        pyautogui.doubleClick(point)
        time.sleep(0.5)
        random_number = random.randint(0, 80)
        pyautogui.typewrite(str(random_number))

# 随机修改rgb值
def random_change_rgb():
    #对(835,825) (835,870) (835,915) (835,950)
    points = [(835, 825), (835, 870), (835, 915), (835, 950)]
    for point in points:
        pyautogui.click(point)
        pyautogui.hotkey('ctrl', 'a')
        random_number = random.randint(0, 255)
        pyautogui.typewrite(str(random_number))
    pyautogui.press('enter')


# ==========================工具类======================
# 图片适应屏幕分辨率
def image_fit_screen(image_path):
    # 获取当前屏幕分辨率
    screen_width, screen_height = pyautogui.size()
    if screen_width != 1920 or screen_height != 1080:
        logger.error("屏幕宽度: {}, 屏幕高度: {}", screen_width, screen_height)
        return image_path
    # 打开图像文件
    img = Image.open(image_path)
    # 调整图像大小到当前屏幕分辨率
    img = img.resize((int(img.width * screen_width / 1920), int(img.height * screen_height / 1080)),
                     Image.Resampling.LANCZOS)
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


def filter_green(image):
    # 定义绿色的HSV范围
    lower_green = np.array([60, 100, 100])
    upper_green = np.array([90, 255, 255])
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_green, upper_green)
    result = cv2.bitwise_and(image, image, mask=mask)
    if np.sum(mask) > 0:
        return True, result
    else:
        return False, image


def filter_red(image):
    # 定义红色的HSV范围
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)
    result = cv2.bitwise_and(image, image, mask=mask)
    if np.sum(mask) > 0:
        return True, result
    else:
        return False, image


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


def write_text(coordinate, text):
    pyautogui.click(coordinate)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.write(text)


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


# 矫正识别结果的错别字
def correct_typos(text):
    target_texts = ["检测窗口", "未完待续"]
    for target_text in target_texts:
        match_count = 0
        # 检查输入文本与目标文本的每个字符
        for char in text:
            if char in target_text:
                match_count += 1
        # 如果匹配的字符数达到2个或以上，则返回目标文本
        if match_count >= 2:
            return target_text
    return text  # 如果没有足够的匹配，返回原始文本


# 识别屏幕上指定区域
def read_text_ocr(top_left_point, bottom_right_point):
    logger.info("开始识别")
    # 截取屏幕上指定区域的图像
    screenshot = ImageGrab.grab(
        bbox=(top_left_point[0], top_left_point[1], bottom_right_point[0], bottom_right_point[1]))
    screenshot_np = np.array(screenshot)
    screenshot_np = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

    # 调用颜色过滤方法
    have_specific_color, filtered_image = filter_red(screenshot_np)
    if have_specific_color:
        logger.info("red")
    if not have_specific_color:
        logger.info("green")
        have_specific_color, filtered_image = filter_green(screenshot_np)

    # 使用EasyOCR进行文字识别
    reader = easyocr.Reader(['ch_sim'])
    results = reader.readtext(filtered_image)

    # 在截图上绘制矩形框标记识别区域
    cv2.rectangle(filtered_image, (0, 0), (filtered_image.shape[1], filtered_image.shape[0]), (0, 255, 0), 2)

    # 输出识别结果
    recognized_text = ' '.join([correct_typos(text) for (bbox, text, prob) in results])
    logger.info(f"识别的文字: {recognized_text}")

    logger.info("识别结束")
    return recognized_text


# =====================================文件处理=====================================
# 删除文件夹下所有文件
def delete_documents(path):
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
