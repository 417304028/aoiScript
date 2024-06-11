import sys
import time
import psutil
import pyperclip
import win32gui
import win32com
import win32con
import pythoncom
import pyautogui
import config
import functools
import win32com.client
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
        print("AOI已启动，正在恢复正常窗口")
        app = Application().connect(path="AOI.exe")
        main_window = app.window(title_re=".*AOI.*")
        if main_window.is_minimized():
            main_window.restore()
        main_window.set_focus()


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
def click_button(image_path, num):
    print("寻找按钮并点击..." + image_path)
    start_time = time.time()
    clicked = False  # 添加一个标志来检测是否成功点击
    while time.time() - start_time < 5:
        try:
            if num == 1:
                pyautogui.click(image_path)
                print("点击" + image_path + "成功")
                clicked = True  # 更新标志为True表示成功点击
                break
            elif num == 2:
                pyautogui.doubleClick(image_path)
                print("双击" + image_path + "成功")
                clicked = True  # 更新标志为True表示成功点击
                break
        except Exception as e:
            print(f"尝试点击{image_path}时报错: 错误信息: {e}")
            time.sleep(1)

    if not clicked:  # 检查是否成功点击
        raise Exception(f"超时: 在规定时间内未能点击{image_path}")


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


# 确保在元器件编辑界面
def ensure_in_edit_program():
    try:
        print("尝试连接到AOI.exe...")
        app = Application().connect(path="AOI.exe")
        print("连接成功，尝试获取主窗口...")
        
        # 尝试获取主窗口，使用更简单的正则表达式
        try:
            main_window = app.window(title_re=".*Sinic-Tek 3D AOI.*")
        except Exception as e:
            print(f"获取主窗口失败: {e}")
            return
        
        # 打印主窗口对象
        print("主窗口对象:", main_window)
        
        # 先找到 splitContainerControl3 窗格
        print("尝试查找 splitContainerControl3 窗格...")
        split_container = main_window.child_window(auto_id="splitContainerControl3")
        # split_container = main_window.child_window(auto_id="splitContainerControl3", control_type="Pane")
        if split_container.exists(timeout=10):
            print("找到 splitContainerControl3 窗格，尝试查找 程式元件 窗格...")
            # 在 splitContainerControl3 窗格中查找 程式元件 窗格
            edit_component_window = split_container.child_window(title="程式元件", control_type="Pane")
            if edit_component_window.exists(timeout=10):
                print("在元器件编辑界面")
            else:
                print("不在元器件编辑界面")
        else:
            print("未找到 splitContainerControl3 窗格")
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
