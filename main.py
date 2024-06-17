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

if __name__ == '__main__':
    # mw.start_gui()
    scripts.lxbj.lxbj_001_02()
    