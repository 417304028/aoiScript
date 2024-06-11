import random
import sys
import time
import config
import pyperclip
import cv2
import numpy as np
import pyautogui
import utils
import gui.main_window as mw
import scripts.lxbj

# CURRENT_COMPONENT_STATUS = None
ALL_COMPONENTS = []
# pyautogui 的全局暂停时间
pyautogui.PAUSE = 1  # 暂停1s


# 确认打开aoi后，点击打开程式
def open_job():
    if not utils.search_symbol(config.AOI_TOPIC, 20):
        sys.exit("未能在规定时间内确认AOI状态，操作中止。")
    time.sleep(0.2)
    utils.search_symbol(config.OPEN_PROGRAM, 20)
    # 打开程式
    utils.click_button(config.OPEN_PROGRAM, 1)
    # TODO：其实转为获取句柄更快
    time.sleep(0.4)
    # 点击模板
    utils.click_button(config.PROGRAM_NAME, 1)
    time.sleep(0.3)
    # 点轨1
    utils.click_button(config.LOAD_PROGRAM, 1)
    # 点是
    utils.click_button(config.OPEN_PROGRAM_YES, 1)


# 获取程式元件列表
def get_component_list():
    global ALL_COMPONENTS
    time.sleep(3)
    # 注意首次加载板的时候出现的和后续加载时的面板不同
    # 首次加载应该识别程式元件 点击后打开
    # 点击程式元件面板
    utils.search_symbol(config.PROGRAM_COMPONENT_DARK, 60)
    time.sleep(5)
    utils.click_button(config.PROGRAM_COMPONENT_DARK, 2)
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
    utils.search_symbol(config.EDIT_BACK_BUTTON, 10)
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


def move_cad():
    # 将鼠标移动到指定位置
    pyautogui.moveTo(935, 445)
    # 按下鼠标左键准备拖动
    pyautogui.mouseDown()
    # 生成随机的x和y偏移量，范围在-300到300之间
    x_offset = random.randint(-300, 300)
    y_offset = random.randint(-300, 300)
    # 执行鼠标拖动操作
    pyautogui.moveRel(x_offset, y_offset, duration=0.5)
    # 释放鼠标左键完成拖动
    pyautogui.mouseUp()
    print("完成拖动")


# 画CAD框
def add_cad_frame():
    utils.search_symbol(config.EDIT_BACK_BUTTON, 5)
    # 获取(937, 447)处的颜色
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
    pyautogui.rightClick(935, 445)
    utils.click_button(config.ADD_WINDOW, 1)
    # 使用pyautogui模拟鼠标拖动
    pyautogui.moveTo(top_left, duration=1)
    pyautogui.mouseDown()
    pyautogui.moveTo(bottom_right, duration=1)
    pyautogui.mouseUp()
    print("cad描边完毕")


# 缺陷类型选择X偏移，随机调整左下角抽色空间的RT值，点击测试当前窗口，获取当前高度上下限的结果值
def x_offset_test():
    time.sleep(2)
    utils.click_button(config.SQUARE_POSITIONING, 1)
    utils.click_button(config.X_OFFSET, 1)
    utils.click_button(config.ADD_CHECKED_YES, 1)
    time.sleep(0.2)
    print("开始方形定位——x偏移检测")

    # 调整RT值
    set_random_value(840, 850, 1)
    set_random_value(840, 870, 1)
    set_random_value(840, 945, 1)
    set_random_value(840, 965, 1)
    pyautogui.press('enter')
    time.sleep(0.5)
    utils.click_button(config.TEST_WINDOW, 1)
    time.sleep(0.5)
    pyautogui.doubleClick(1780, 395)
    pyautogui.keyDown('ctrl')
    pyautogui.press('c')
    pyautogui.keyUp('ctrl')
    top_result = pyperclip.paste()
    pyautogui.doubleClick(1780, 415)
    pyautogui.keyDown('ctrl')
    pyautogui.press('c')
    pyautogui.keyUp('ctrl')
    bottom_result = pyperclip.paste()
    print(top_result, bottom_result)
    print("x_offset_test完成")


def set_random_value(x, y, type):
    if type == 0:  # 0代表RGB值
        random_num = random.randint(0, 300)
    elif type == 1:  # 1代表RT值
        random_num = random.randint(0, 1437)
    pyautogui.click(x, y)
    pyautogui.keyDown('ctrl')
    pyautogui.press('a')
    pyautogui.keyUp('ctrl')
    pyautogui.press('backspace')
    pyautogui.typewrite(str(random_num))


# 打开2D模式，随机调整rgb值，点击测试当前元件，再调整RGB值，点击测试当前该窗口
def change_rgb_test():
    utils.click_button(config.ALG2D, 1)
    # rgb三个数字框 改0-300任意数值 改完后回车
    set_random_value(835, 825, 0)
    set_random_value(835, 870, 0)
    set_random_value(835, 915, 0)
    pyautogui.press('enter')
    time.sleep(0.1)
    utils.click_button(config.TEST_COMPONENT, 1)
    set_random_value(835, 825, 0)
    set_random_value(835, 870, 0)
    set_random_value(835, 915, 0)
    pyautogui.press('enter')
    utils.click_button(config.TEST_WINDOW, 1)


# 随机切换光源，随机调整方形定位算法的框大小及位置，点击测试，读取高度上下限的结果值
def change_light_test():
    utils.click_button(config.GUI_EDIT_LIGHT, 1)
    try:
        utils.search_symbol(config.GUI_EDIT_LIGHT_MENU, 5)
        # 在屏幕上找到图片
        location = pyautogui.locateOnScreen(config.GUI_EDIT_LIGHT_MENU)
        if location:
            # 计算图片的宽度和高度
            width, height = location.width, location.height
            # 生成图片范围内的随机点击坐标
            click_x = location.left + random.randint(0, width)
            click_y = location.top + random.randint(0, height)
            # 执行点击操作
            pyautogui.click(x=click_x, y=click_y)
            print(f"点击光源选择菜单的({click_x}, {click_y}位置)")
            time.sleep(0.5)
        else:
            sys.exit("找光源编辑菜单出错")
    except pyautogui.ImageNotFoundException:
        sys.exit("未找到光源编辑菜单")
    # 现在光源切换完毕，开始调整方形定位算法框大小及位置
    # adjust_cad_frame()
    add_cad_frame()
    utils.click_button(config.SQUARE_POSITIONING, 1)
    utils.click_button(config.X_OFFSET, 1)
    utils.click_button(config.ADD_CHECKED_YES, 1)
    # 点击测试
    utils.click_button(config.TEST_WINDOW, 1)
    time.sleep(0.5)
    pyautogui.doubleClick(1780, 395)
    pyautogui.keyDown('ctrl')
    pyautogui.press('c')
    pyautogui.keyUp('ctrl')
    top_result = pyperclip.paste()
    pyautogui.click(1780, 418)
    pyautogui.keyDown('ctrl')
    pyautogui.press('c')
    pyautogui.keyUp('ctrl')
    bottom_result = pyperclip.paste()
    print(top_result, bottom_result)


def component_test(component):
    x, y = component['x'], component['y']
    time.sleep(2)
    pyautogui.doubleClick(x, y)
    pyautogui.press('enter')
    component['seen'] = True
    if component['status'] == 'no_checked':
        # for i in range(3):
        # if i == 0:
        # 调整将CAD框随机变大，再变小，再随机移动CAD；
        print("处理未检测的元件")
        adjust_cad_frame()
        move_cad()
        # 画一个方形定位算法（最好和CAD重合），缺陷类型选择X偏移，随机调整左下角抽色空间的RT值，点击测试当前窗口，获取当前高度上下限的结果值
        add_cad_frame()
        x_offset_test()
        # 打开2D模式，随机调整RGB值，点击测试当前文件，再调整RGB值，点击测试当前窗口
        change_rgb_test()
        # 随机切换光源，随机调整方形定位算法的框大小及位置，点击测试，读取高度上下限的结果值
        change_light_test()
        # print(f"该元件已处理第 {i+1} 次")
    elif component['status'] == 'checked':
        print("处理已检测的元件")
        for i in range(3):
            # 调整将CAD框随机变大，再变小，再随机移动CAD；
            sys.exit("停停停，先测到这里")
            adjust_cad_frame()
            # 画一个方形定位算法（最好和CAD重合），缺陷类型选择X偏移，随机调整左下角抽色空间的RT值，点击测试当前窗口，获取当前高度上下限的结果值
            x_offset_test()
            # 打开2D模式，随机调整RGB值，点击测试当前文件，再调整RGB值，点击测试当前窗口
            change_rgb_test()
            # 随机切换光源，随机调整方形定位算法的框大小及位置，点击测试，读取高度上下限的结果值
            random_change_light()
            print(f"该元件已处理第 {i + 1} 次")


if __name__ == '__main__':
    # mw.start_gui()
    scripts.lxbj.lxbj_001_03()
