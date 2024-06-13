import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(0) # 解决使用pyautowin时缩放问题
import sys
import time
import psutil
import pyperclip
import cv2
import numpy as np
import pyautogui
import config
import functools
import win32gui,win32con
import datetime
import os
from pywinauto import Application
from PIL import ImageGrab
from PIL import ImageChops
from openpyxl import Workbook, load_workbook
from openpyxl.drawing.image import Image as ExcelImage


# 确保aoi打开并前置
def check_and_launch_aoi():
    aoi_running = any("AOI.exe" == p.name() for p in psutil.process_iter())
    if not aoi_running:
        print("AOI程序未运行,正在启动...")
        app = Application().start(config.AOI_EXE_PATH)
        print("等待AOI程序启动...")
        app.window(title_re=".*AOI.*").wait('visible', timeout=60)
    else:
        main_window = connect_aoi_window()
        # 确保窗口未最小化
        if main_window.is_minimized():
            main_window.restore()
            print("窗口已恢复")
        # 确保窗口最大化
        if not main_window.is_maximized():
            main_window.maximize()
            print("窗口已最大化")
        # 获取窗口句柄
        hwnd = main_window.handle
        # 将窗口置顶
        win32gui.SetForegroundWindow(hwnd)
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        print("窗口已置顶")


def search_symbol(symbol, timeout, region=None):
    start_time = time.time()
    if timeout is not None:
        while time.time() - start_time < timeout:
            try:
                if pyautogui.locateOnScreen(symbol, region=region) is not None:
                    print("已确认" + symbol + "存在")
                    return True
            except pyautogui.ImageNotFoundException:
                print("正在识别" + symbol)
            except Exception as e:
                raise Exception(f"发生异常: {e}")
        return False
    else:
        try:
            while True:
                if pyautogui.locateOnScreen(symbol, region=region) is not None:
                    print("已确认" + symbol + "存在")
                    return True
        except pyautogui.ImageNotFoundException:
            return False
        except Exception as e:
            raise Exception(f"发生异常: {e}")


def search_symbol_erroring(symbol, timeout, region=None):
    start_time = time.time()
    if timeout is not None:
        while time.time() - start_time < timeout:
            try:
                if pyautogui.locateOnScreen(symbol, region=region) is not None:
                    print("已确认" + symbol + "存在")
                    return True
            except pyautogui.ImageNotFoundException:
                print("正在识别" + symbol)
            except Exception as e:
                raise Exception(f"发生异常: {e}")
        # 如果超时后还没有找到符号，抛出超时异常
        raise Exception(f"超时: 没找到" + symbol)
    else:
        try:
            while True:
                if pyautogui.locateOnScreen(symbol, region=region) is not None:
                    print("已确认" + symbol + "存在")
                    return True
        except pyautogui.ImageNotFoundException:
            raise Exception(f"没找到图片: {symbol}")
        except Exception as e:
            raise Exception(f"发生异常: {e}")


# 5s内尝试识别并点击按钮
# def click_button(image_path, num):
#     print("寻找按钮并点击..." + image_path)
#     start_time = time.time()
#     clicked = False  # 添加一个标志来检测是否成功点击
#     while time.time() - start_time < 5:
#         try:
#             if num == 1:
#                 pyautogui.click(image_path)
#                 print("点击" + image_path + "成功")
#                 clicked = True  # 更新标志为True表示成功点击
#                 break
#             elif num == 2:
#                 pyautogui.doubleClick(image_path)
#                 print("双击" + image_path + "成功")
#                 clicked = True  # 更新标志为True表示成功点击
#                 break
#         except Exception as e:
#             print(f"尝试点击{image_path}时报错: 错误信息: {e}")
#             time.sleep(1)

#     if not clicked:  # 检查是否成功点击
#         raise Exception(f"超时: 在规定时间内未能点击{image_path}")


def screenshot_to_excel(test_case_name, path, exception):
    print("开始截图异常情况")
    # 使用 sys.executable 获取 .exe 文件的目录
    exe_dir = os.path.dirname(sys.executable)
    log_dir = os.path.join(exe_dir, "log")
    print("创建log目录")
    os.makedirs(log_dir, exist_ok=True)  # 确保log目录存在
    print("创建完成")

    try:
        # 截图
        screenshot = ImageGrab.grab()
        screenshot_file = os.path.join(log_dir, "temp_screenshot.png")
        print("开始保存截图")
        screenshot.save(screenshot_file)  # 保存截图为文件
        print("保存截图完成")

        # 定义Excel文件路径
        excel_path = os.path.join(log_dir, "test_results.xlsx")

        # 检查Excel文件是否存在，如果不存在则创建
        if not os.path.exists(excel_path):
            print("创建excel")
            wb = Workbook()
        else:
            print("加载excel")
            wb = load_workbook(excel_path)
        ws = wb.active

        # 确定下一个空白行
        row = ws.max_row + 1
        print("写入数据")

        # 写入数据
        ws[f"A{row}"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ws[f"B{row}"] = test_case_name
        ws[f"C{row}"] = path
        ws[f"D{row}"] = str(exception)
        print("插入图片")

        # 将截图插入到Excel
        img = ExcelImage(screenshot_file)
        img.anchor = f"E{row}"  # 设置图片的锚点
        ws.add_image(img)
        print("数据处理完毕，开始保存excel")
        wb.save(excel_path)
        print("Excel文件保存在:", excel_path)
        print("保存完毕")
    except Exception as e:
        print(f"在保存截图和数据到Excel时发生错误: {e}")
    finally:
        if os.path.exists(screenshot_file):
            os.remove(screenshot_file)  # 清理临时文件


# 装饰器，出问题时截图并保存至excel
def screenshot_error_to_excel(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            current_function_name = func.__name__
            path = sys.executable
            screenshot_to_excel(current_function_name, path, e)
            raise  # 可选：重新抛出异常以便外部也能知道异常发生

    return wrapper


def compare_images(img1, img2):
    return ImageChops.difference(img1, img2).getbbox() is None


# 打开程式界面用的
def check_load_program(symbol, program_bbox, program_loaded_bbox):
    # 左边有程式才加载
    exist_symbol = search_symbol(symbol, None, program_bbox)
    if exist_symbol:
        click_button(symbol, 2)
        time.sleep(0.5)
        # 查看右侧是否多了个程式
        loaded_symbol = search_symbol_erroring(symbol, None, program_loaded_bbox)
        if loaded_symbol:
            return True
    else:
        return False


# 点不到就报错
def click_button(name):
    main_window = connect_aoi_window()
    if main_window.exists():
        print("start to click button")
        button = main_window.child_window(title=name, control_type="Button")
        print(button.exists())
        print("控件名称:", button.element_info.name)
        print("控件类型:", button.element_info.control_type)
        print("是否可用:", button.element_info.enabled)
        print("是否可见:", button.element_info.visible)
        print("位置:", button.element_info.rectangle)
        rect = button.element_info.rectangle
        # 计算中心点坐标
        center_x = rect.left + (rect.right - rect.left) // 2
        center_y = rect.top + (rect.bottom - rect.top) // 2
        print(center_x, center_y)
        # button.set_focus()
        # time.sleep(1)

        # 使用pyautogui点击中心点 TODO 他妈的点不了
        pyautogui.click(center_x, center_y)
        button.click_input()
    else:
        print("no click")


# 确保在元器件编辑界面
def ensure_in_edit_program(title):
    try:
        main_window = connect_aoi_window()
        # 逐级查找 '程式元件' 选项卡
        program_component_tab = main_window.child_window(title=title)
        if program_component_tab.exists(timeout=3):
            print("控件类型:", program_component_tab.element_info.control_type)
            print("位置:", program_component_tab.element_info.rectangle)
            return True
        else:
            print("未找到" + title + "选项卡")
            return False
    except Exception as e:
        print(f"发生错误: {e}")
        return False


# 连接窗口
def connect_aoi_window():
    print("尝试连接到aoi窗格")
    # app = Application('win32').connect(path=config.AOI_EXE_PATH)
    app = Application().connect(path=config.AOI_EXE_PATH)
    main_window = app.window(title_re=".*Sinic-Tek 3D AOI.*", auto_id="MainForm")
    if main_window.exists():
        print("成功连接到aoi窗格")
        return main_window
    else:
        return Exception


# 画检测框
def add_check_window(first, second):
    try:
        main_window = connect_aoi_window()
        if main_window.exists():
            print("成功连接到 'Sinic-Tek 3D AOI' 程序")
            click_button("检测窗口")
            # 绘制框框（获取准星旁边的颜色，扩大到颜色分界处，截取坐标）
            target_color = pyautogui.screenshot().getpixel((936, 446))
            # 转换颜色到HSV
            target_color_hsv = cv2.cvtColor(np.uint8([[target_color]]), cv2.COLOR_RGB2HSV)[0][0]
            # 定义颜色的HSV范围，初始范围
            hue_variation = 15
            saturation_variation = 30
            value_variation = 30
            found = False
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
                # 寻找连贯区域的轮廓
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                # 找到包含点(935, 445)的连贯区域
                target_contour = None
                for contour in contours:
                    if cv2.pointPolygonTest(contour, (936, 446), False) >= 0:
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
                    print("Top-left corner:", top_left)
                    print("Bottom-right corner:", bottom_right)
                    print("找到疑似cad区域")
                else:
                    # 增加HSV范围并重试
                    hue_variation += 5
                    saturation_variation += 10
                    value_variation += 10
                    print("hue_variation:", hue_variation)
                    if hue_variation > 180 or saturation_variation > 255 or value_variation > 255:
                        print("未识别出cad区域，可能准心不在cad内")
            # 使用pyautogui模拟鼠标拖动
            pyautogui.moveTo(top_left, duration=1)
            pyautogui.mouseDown()
            pyautogui.moveTo(bottom_right, duration=1)
            pyautogui.mouseUp()
            print("cad描边完毕")
            #=======================================================
            # 找到并点击“高级”选项卡，再点击second选项卡
            time.sleep(1)
            first_tab = main_window.child_window(title=first, control_type="TabItem")
            if first_tab.exists():
                first_tab.click_input()
                print("已点击" + first + "选项卡")
                time.sleep(1)
                second_tab = main_window.child_window(title=second, control_type="TabItem")
                second_tab.wait('visible', timeout=5)
                if second_tab.exists():
                    second_tab.click_input()
                    print("已点击" + second + "选项卡")
            else:
                raise Exception
            # 等到含 影像处理 的窗口出现
    except Exception as e:
        print(f"发生错误: {e}")


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


def random_change_param():
    return None
