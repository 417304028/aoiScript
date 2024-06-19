import ctypes
import random
import easyocr
import sys
import time
from screeninfo import get_monitors
import psutil
import pyperclip
import cv2
import numpy as np
import pyautogui
import config
import functools
import datetime
import os
from pywinauto import Application
from PIL import ImageGrab,Image
from PIL import ImageChops
from openpyxl import Workbook, load_workbook
from openpyxl.drawing.image import Image as ExcelImage

ctypes.windll.shcore.SetProcessDpiAwareness(0)  # 解决使用pyautowin时缩放问题


# ============================窗格处理===================
# 连接窗口（好像只能用win32连接窗口,uia不行）
def connect_aoi_window():
    # app = Application().connect(title_re=u".*Sinic-Tek 3D AOI.*",
    #                             auto_id="MainForm")
    # top_window = app.window(auto_id="MainForm")
    # top_window.wait('ready', timeout=10)
    # time.sleep(0.3)
    # if top_window.exists():
    #     print("成功连接到aoi窗口")
    #     return top_window
    # else:
    #     raise Exception
    try:
        app = Application(backend="uia").connect(auto_id="MainForm")
        main_window = app.window(auto_id="MainForm")
        if main_window.exists(timeout=10):
            print("成功连接到窗口")
            return main_window
        else:
            print("未找到窗口")
    except Exception as e:
        print(f"连接窗口时发生错误: {e}")

# 确保aoi打开并前置
def check_and_launch_aoi():
    aoi_running = any("AOI.exe" == p.name() for p in psutil.process_iter())
    if not aoi_running:
        print("AOI程序未运行,正在启动...")
        app = Application().start(config.AOI_EXE_PATH)
        print("等待AOI程序启动...")
        app.window(title_re=".*AOI.*").wait('ready', timeout=60)
    else:
        main_window = connect_aoi_window()
        main_window.set_focus()
        main_window.wait('ready', timeout=10)
        # # 确保窗口未最小化
        # if main_window.is_minimized():
        #     main_window.restore()
        #     print("窗口已恢复")
        # # 确保窗口最大化
        # if not main_window.is_maximized():
        #     main_window.maximize()
        #     print("窗口已最大化")
        # # 获取窗口句柄
        # hwnd = main_window.handle
        # win32gui.SetForegroundWindow(hwnd)
        # win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
        # print(hwnd)
        # win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        # print("窗口已置顶")


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
            print(specific_symbol.get_properties())
            return True
        else:
            print("未找到" + name + "窗格，可能目前不在指定的界面")
            return False
    except Exception as e:
        print(f"发生错误: {e}")
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
            print("已点击按钮：" + (name if name else "未指定名称"))
        else:
            print("点击时未找到指定的按钮")
    except Exception as e:
        print(f"发生错误: {e}")


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
        print("全屏准星位置:", (cx, cy))
        return (cx, cy)
    else:
        raise Exception("未找到准星")

# 打勾框是否打勾
def is_checked(top_left, bottom_right, pixel_threshold=18):
    # 调整坐标
    adjusted_top_left, adjusted_bottom_right = adjust_coordinates(top_left, bottom_right)

    # 截取屏幕上的复选框区域
    screenshot = ImageGrab.grab(
        bbox=(adjusted_top_left[0], adjusted_top_left[1], adjusted_bottom_right[0], adjusted_bottom_right[1]))
    screenshot_np = np.array(screenshot)
    screenshot_np = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

    # 将图像转换为灰度图
    gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)

    # 应用阈值来突出显示勾选区域
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    # 计算白色像素的数量（勾选标记）
    white_pixels = np.sum(thresh == 255)

    # 判断是否勾选（根据对勾占据的像素点来设置阈值）
    return white_pixels >= pixel_threshold

def click_by_png(image_path, times=1, timeout=5):
    start_time = time.time()
    clicked = False  # 添加一个标志来检测是否成功点击
    image_path = image_fit_screen(image_path)
    print(f"尝试点击图片: {image_path}")
    while time.time() - start_time < timeout:
        try:
            location = pyautogui.locateCenterOnScreen(image_path)
            if location:
                if times == 1:
                    pyautogui.click(location)
                elif times == 2:
                    pyautogui.doubleClick(location)
                print(f"点击{image_path}成功")
                clicked = True  # 更新标志为True表示成功点击
                break
        except Exception as e:
            print(f"尝试点击{image_path}时报错: 错误信息: {e}")
        time.sleep(0.5)
    if not clicked:  # 检查是否成功点击
        raise Exception(f"超时: 在{timeout}秒内未能点击{image_path}")

def search_symbol(symbol, timeout, region=None):
    start_time = time.time()
    symbol = image_fit_screen(symbol)
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
    symbol = image_fit_screen(symbol)
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


# =========================装饰器=========================
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


# ====================业务处理========================
# 画检测窗口
def add_check_window():
    try:
        connect_aoi_window()
        time.sleep(1.5)
        crosshair_center = get_crosshair_center()
        if crosshair_center is None:
            print("未找到准星中心")
            return

        nearby_point = (crosshair_center[0] + 3, crosshair_center[1] + 3)
        print(nearby_point)
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
                print("找到疑似cad区域，左上及右下坐标如下" + str(top_left) + "," + str(bottom_right))
            else:
                # 增加HSV范围并重试
                hue_variation += 1
                saturation_variation += 2
                value_variation += 2
                if hue_variation > 180 or saturation_variation > 255 or value_variation > 255:
                    print("未识别出cad区域，可能准心不在cad内")
                    break

        if last_top_left and last_bottom_right:
            # 使用pyautogui模拟鼠标拖动
            pyautogui.press("w")
            pyautogui.moveTo(last_top_left, duration=1)
            pyautogui.mouseDown()
            pyautogui.moveTo(last_bottom_right, duration=1)
            pyautogui.mouseUp()
            print("cad描边完毕")
        else:
            print("未找到任何区域")

    except Exception as e:
        print(f"发生错误: {e}")

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
        print("未检测的元件图像未找到。")

    try:
        # 识别已检测的元件坐标并保存，标记为checked
        checked_components = list(pyautogui.locateAllOnScreen(config.CHECKED_COMPONENT, confidence=confidence_level))
        checked_positions = [{'x': pos.left, 'y': pos.top, 'status': 'checked', 'seen': False} for pos in
                             checked_components]
    except pyautogui.ImageNotFoundException:
        checked_positions = []
        print("已检测的元件图像未找到。")
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
    print(yellow_blocks)
    # 检查找到的方块数量
    if len(yellow_blocks) == 8:
        # 按照距离中心点的距离排序
        yellow_blocks.sort(key=lambda pos: (pos[0] + pos[2] // 2 - center_x + search_region[0]) ** 2 + (
                pos[1] + pos[3] // 2 - center_y + search_region[1]) ** 2)
        print(yellow_blocks)
        # 选择第5个最近的方块
        target_block = yellow_blocks[4]  # 选择第五个最近的方块，索引为4
        target_x = target_block[0] + target_block[2] // 2 + search_region[0]
        target_y = target_block[1] + target_block[3] // 2 + search_region[1]
        target = (target_x, target_y)
        print(target_x, target_y)
        return True, target
    elif len(yellow_blocks) > 0:
        return True, None
    else:
        return False, None

# 调整将CAD框随机变大，再变小
def adjust_cad_frame():
    search_symbol(config.EDIT_BACK_BUTTON, 10)
    time.sleep(2)
    # 选中框框快捷键
    pyautogui.press('b')
    print("选中检测框")
    time.sleep(1.5)
    success, point = get_choose_box()
    print(point)
    # 识别到完整的选择框
    if success:
        if point is not None:
            print("move")
            x, y = point
            print(x, y)
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
    points = [(1720, 398), (1720, 418), (1720, 440), (1720, 460), (1720, 480), (1720, 500), (1720, 630), (1720, 650), (1720, 690), (1720, 715), (1720, 735), (1720, 775), (1720, 840), (1720, 860)]
    for point in points:
        pyautogui.click(point)
        pyautogui.hotkey('ctrl', 'a')
        random_number = random.randint(0, 1000)
        pyautogui.typewrite(str(random_number))


# ==========================工具类======================
# 图片适应屏幕分辨率
def image_fit_screen(image_path):
    # 获取当前屏幕分辨率
    screen_width, screen_height = pyautogui.size()
    # 打开图像文件
    img = Image.open(image_path)
    # 调整图像大小到当前屏幕分辨率
    img = img.resize((int(img.width * screen_width / 1920), int(img.height * screen_height / 1080)), Image.ANTIALIAS)
    # 保存到临时文件
    temp_image_path = f"temp_{image_path}"
    img.save(temp_image_path)
    return temp_image_path

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

def read_text(point):
    # 获取当前屏幕分辨率
    monitor = get_monitors()[0]
    current_resolution = (monitor.width, monitor.height)

    # 计算坐标调整比例
    x_ratio = current_resolution[0] / 1920
    y_ratio = current_resolution[1] / 1080

    # 调整坐标
    adjusted_point = (int(point[0] * x_ratio), int(point[1] * y_ratio))

    # 单击调整后的坐标
    pyautogui.click(adjusted_point[0], adjusted_point[1])

    # 全选并复制
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')

    # 读取剪贴板内容
    clipboard_text = pyperclip.paste()

    return clipboard_text

def read_text_ocr(top_left_point, bottom_right_point):
    # 创建一个OCR识别器，指定中文简体和英文
    reader = easyocr.Reader(['ch_sim'])

    # 截取屏幕上指定区域的图像
    screenshot = ImageGrab.grab(
        bbox=(top_left_point[0], top_left_point[1], bottom_right_point[0], bottom_right_point[1]))
    screenshot_np = np.array(screenshot)
    screenshot_np = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

    # 使用EasyOCR进行文字识别
    results = reader.readtext(screenshot_np)

    # 输出识别结果
    for (bbox, text, prob) in results:
        print(f"识别的文字: {text}, 置信度: {prob}")
