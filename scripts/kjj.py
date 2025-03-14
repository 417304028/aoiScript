import os
import random
import time

import pyautogui
import pyperclip
from loguru import logger

import config
import utils


@utils.screenshot_error_to_excel()
def kjj_001_01():
    # 1.【打开】任一job
    # 2.【设置】--【硬件设置】--【快捷键设置】，查看元件编辑界面的快捷键
    # 3.进入元件编辑界面，使用快捷键
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 增加引脚
    utils.add_window("q")
    if not utils.search_symbol(config.PIN_ANGLE):
        raise Exception("增加引脚快捷键疑似无效")
    utils.click_by_png(config.YES)
    # 获取颜色
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.X_OFFSET)
    utils.click_by_png(config.YES)
    time.sleep(8)
    if not utils.search_symbol(config.ALG_IMAGE_TYPE_WEIGHT,config.ALG_PARAM_REGION):
        pyautogui.click((1885,375))
        utils.click_by_png(config.ALG_IMAGE_TYPE_CHOOSE_WEIGHT, config.ALG_PARAM_REGION)
    pyautogui.press("s")
    pyautogui.click(config.CENTRE)
    if not utils.search_symbol(config.ALG_IMAGE_TYPE_COLOR_SPACE, config.ALG_PARAM_REGION):
        raise Exception("获取颜色快捷键疑似无效")
    # 切换本体(引脚)/窗口
    pyautogui.hotkey("ctrl", "a")
    utils.click_color(1, config.COMPONENT_WINDOW_REGION, (0, 0, 255))
    for _ in range(3):
        initial_color = pyautogui.screenshot().getpixel(config.CENTRE)
        pyautogui.hotkey("ctrl", "b")
        new_color = pyautogui.screenshot().getpixel(config.CENTRE)
        if new_color == initial_color:
            raise Exception("切换本体(引脚)/窗口快捷键疑似无效")
    # 取消选择
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("escape")
    # 检测config.CENTRE附近的20个像素点范围内有没有(255，255，0)的点
    screenshot = pyautogui.screenshot()
    for x in range(config.CENTRE[0] - 10, config.CENTRE[0] + 11):
        for y in range(config.CENTRE[1] - 10, config.CENTRE[1] + 11):
            if screenshot.getpixel((x, y)) == (255, 255, 0):
                break
        else:
            continue
        break
    else:
        raise Exception("取消选择快捷键疑似无效")
    
    # 选择下一个窗口
    before_screenshot = pyautogui.screenshot(region=config.ALG_PARAM_REGION)
    pyautogui.hotkey("ctrl", "tab")
    time.sleep(5) 
    after_screenshot = pyautogui.screenshot(region=config.ALG_PARAM_REGION)
    if before_screenshot == after_screenshot:
        raise Exception("选择下一个窗口快捷键疑似无效")
    # 复制 黏贴
    before_component_window = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    pyautogui.hotkey("ctrl", "c")
    pyautogui.moveTo(config.CENTRE)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(3)
    after_component_window = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if before_component_window == after_component_window:
        raise Exception("复制 黏贴快捷键疑似无效")
    # 注意：使用前设置里需把允许撤销勾上
    for action in ["ctrl+z", "ctrl+y"]:
        before_component_window = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
        pyautogui.hotkey(*action.split('+'))
        time.sleep(3)
        after_component_window = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
        if before_component_window == after_component_window:
            raise Exception(f"{action}快捷键疑似无效")
    # 移动操作
    move_operations = {
        "向左移动": "left",
        "向右移动": "right",
        "向上移动": "up",
        "向下移动": "down",
        "放大": "ctrl+shift+up",
        "缩小": "ctrl+shift+down"
    }
    for operation, key in move_operations.items():
        before_screenshot = pyautogui.screenshot(region=config.COMPONENT_REGION)
        for _ in range(3):
            pyautogui.press(key)
            time.sleep(0.5)
        after_screenshot = pyautogui.screenshot(region=config.COMPONENT_REGION)
        if before_screenshot == after_screenshot:
            raise Exception(f"{operation}快捷键疑似无效")
    # 测试窗口
    pyautogui.hotkey("ctrl", "tab")
    time.sleep(5)
    pyautogui.press("space")
    time.sleep(5)
    if utils.search_symbol(config.ALG_PARAM_EMPTY):
        raise Exception("测试窗口快捷键使用后右侧疑似无参数")
    # 测试元件
    start_time = time.time()
    pyautogui.press("d")
    if not utils.search_symbol(config.TESTING_COMPONENT):
        raise Exception("测试元件快捷键使用后疑似无反应")
    while utils.search_symbol(config.TESTING_COMPONENT):
        if time.time() - start_time > 1200:  # 20分钟
            raise Exception("测试元件时超过20分钟")
        time.sleep(5)
    # 测试料号
    start_time = time.time()
    pyautogui.press("f")
    if not utils.search_symbol(config.TESTING_COMPONENT):
        raise Exception("测试料号快捷键使用后疑似无反应")
    while utils.search_symbol(config.TESTING_COMPONENT):
        if time.time() - start_time > 1200:  # 20分钟
            raise Exception("测试料号时超过20分钟")
        time.sleep(5)
    # 测试整板
    start_time = time.time()
    pyautogui.press("b")
    if not utils.search_symbol(config.TESTING_COMPONENT):
        raise Exception("测试整板快捷键疑似无效")
    while utils.search_symbol(config.TESTING_COMPONENT):
        if time.time() - start_time > 1200:  # 20分钟
            raise Exception("测试整板时超过20分钟")
        time.sleep(5)
    # 导入此元件库
    pyautogui.press("f1")
    if not utils.search_symbol(config.QUESTION_MARK):
        raise Exception("导入此元件库快捷键疑似无效")
    utils.click_by_png(config.NO)
    # 导入所有元件库
    time.sleep(2)
    pyautogui.press("f3")
    if not utils.search_symbol(config.QUESTION_MARK):
        raise Exception("导入所有元件库快捷键疑似无效")
    utils.click_by_png(config.NO)
    # 导出此料号到元件库
    pyautogui.press("f2")
    if not utils.search_symbol(config.ELEMENTS_INFORMATION):
        raise Exception("导出此料号到元件库快捷键疑似无效")
    utils.click_by_png(config.CANCEL)
    # 导出所有料号到元件库
    pyautogui.press("f4")
    if not utils.search_symbol(config.QUESTION_MARK):
        raise Exception("导出所有料号到元件库快捷键疑似无效")
    utils.click_by_png(config.NO)
    # 旋转元件
    before_screenshot = pyautogui.screenshot(region=config.COMPONENT_REGION)
    pyautogui.press("r")
    after_screenshot = pyautogui.screenshot(region=config.COMPONENT_REGION)
    if before_screenshot == after_screenshot:
        raise Exception("旋转元件快捷键疑似无效")
    # 选择元件CAD框
    pyautogui.press("c")
    if not utils.check_color_in_region((255,255,0), config.COMPONENT_REGION):
        raise Exception("选择元件CAD框快捷键疑似无效")
    # 链接所有元件检测框
    pyautogui.press("f5")
    if not utils.check_color_in_region((220, 20, 60), config.COMPONENT_REGION):
        raise Exception("链接所有元件检测框快捷键疑似无效")

    # 移动到下一个元件
    try:
        test_y_before = pyautogui.locateOnScreen(config.TEST, region=config.BOARD_COMPONENTS_REGION).top + pyautogui.locateOnScreen(config.TEST, region=config.BOARD_COMPONENTS_REGION).height // 2
        pyautogui.press("x")
        if utils.search_symbol(config.QUESTION_MARK):
            utils.click_by_png(config.NO)
        time.sleep(3)
        test_y_after = pyautogui.locateOnScreen(config.TEST, region=config.BOARD_COMPONENTS_REGION).top + pyautogui.locateOnScreen(config.TEST, region=config.BOARD_COMPONENTS_REGION).height // 2
    except pyautogui.ImageNotFoundException:
        raise Exception("移动到下一个元件时，未能识别到被选中的元件")
    # 查看y坐标有没有大于7的变动
    if abs(test_y_before - test_y_after) <= 7:
        raise Exception("疑似未能切换到下一个元件")
    
    # 返回到整版视图
    pyautogui.press("backspace")
    if utils.search_symbol(config.QUESTION_MARK,3):
        pyautogui.press("enter")
    if not utils.search_symbol(config.BOARD_AUTO,tolerance=0.75):
        raise Exception("返回到整版视图快捷键疑似无效")
    # 显示首件图

    # 显示元件3D图

    # 增加焊盘标志

    # 在线调参显示同步封装

@utils.screenshot_error_to_excel()
def kjj_001_02():
    # 1.【打开】任一job
    utils.check_and_launch_aoi()
    utils.open_program()
    # 2.【设置】--【硬件设置】--【快捷键设置】，查看主程序界面的快捷键
    # 3.进入主程序界面，使用快捷键
    # 打开程式
    pyautogui.press("o")
    if not utils.search_symbol(config.OPEN_PROGRAM_TOPIC):
        raise Exception("打开程式快捷键疑似无效")
    utils.click_by_png(config.CANCEL)

    # 打开Debug程式
    pyautogui.hotkey("ctrl", "shift", "f2")
    if not utils.search_symbol(config.OPEN_DJB_TOPIC):
        raise Exception("保存Debug程式快捷键疑似无效")
    pyautogui.press("esc")
    # 打开元件库
    pyautogui.press("f5")
    if not utils.search_symbol(config.ELEMENTS_VIEW_SEARCH, region=config.ELEMENTS_VIEW_REGION):
        raise Exception("打开元件库快捷键疑似无效")
    # 删除所有记录文件 检测D:\EYAOI\Logger下文件有没有变少
    initial_file_count = len(os.listdir("D:\\EYAOI\\Logger"))
    logger.debug(f"initial_file_count = "+ initial_file_count)
    pyautogui.hotkey("ctrl", "shift", "l")
    # 检查文件数量是否减少
    time.sleep(1)  # 等待文件删除完成
    logger.debug(f"final_file_count =" + final_file_count)
    final_file_count = len(os.listdir("D:\\EYAOI\\Logger"))
    if final_file_count >= initial_file_count:
        raise Exception("删除所有记录文件快捷键疑似无效")
    # 进板
    # pyautogui.press("insert")
    # 归零
    # pyautogui.press("home")
    # 开始测试
    # pyautogui.press("r")
    # 停止测试
    # pyautogui.press("e")
    # 保存程式
    pyautogui.press("s")
    if not utils.search_symbol(config.QUESTION_MARK):
        raise Exception("保存程式快捷键疑似无效")
    utils.click_by_png(config.NO)
    utils.ensure_in_edit_mode()
    # 保存Debug程式
    pyautogui.hotkey("ctrl", "shift", "f12")
    while utils.search_symbol(config.EXPORTING_DJB):
        time.sleep(1)
    if not utils.search_symbol(config.SAVE_AS_TOPIC):
        raise Exception("保存Debug程式快捷键疑似无效")
    pyautogui.press("esc")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def kjj_001_03():
    # 1.【打开】任一job
    utils.check_and_launch_aoi()
    utils.open_program()
    # 2.【设置】--【硬件设置】--【快捷键设置】，查看整板编辑面的快捷键
    # 3.进入整板编辑界面，使用快捷键
    # 复制元件
    utils.click_color(0, config.COMPONENT_REGION, (0,255,0))
    mouse_coordinate = pyautogui.position()
    a = utils.count_color_in_range(mouse_coordinate, 50, (0,255,0))
    pyautogui.click()
    pyautogui.hotkey("ctrl", "c")
    # 粘贴元件
    pyautogui.hotkey("ctrl", "v")
    b = utils.count_color_in_range(mouse_coordinate, 50, (0,255,0))
    if b <= a:
        raise Exception("ctrl cv快捷键疑似无效")
    # 手动编辑拼版编号
    utils.click_by_png(config.BOARD_SPLICING_OPERATION)
    utils.click_color(1, config.COMPONENT_REGION, (220, 20, 60))
    pyautogui.press("F1")
    if not utils.search_symbol(config.OK_COLLECTION):
        raise Exception("手动编辑拼版编号快捷键疑似无效")
    utils.close_aoi()
# @utils.screenshot_error_to_excel()
# def kjj_001_04():
#     # 1.【打开】任一job
#     utils.check_and_launch_aoi()
#     utils.open_program()
#     # 2.【设置】--【硬件设置】--【快捷键设置】，查看缺陷视图界面的快捷键
#     # 3.【运行】该程式

#     # 4.弹出dv复判界面，在dv复判界面，使用快捷键
#     # 上一个元件
#     pyautogui.press("up")
#     # 下一个元件

#     # 上一个窗口
#     pyautogui.press("left")
#     # 下一个窗口
#     pyautogui.press("right")
#     # 元件通过
#     pyautogui.press("down")
#     # 元件不良
#     pyautogui.press("numpad0")
#     # 全部通过
#     pyautogui.press("f11")
#     # 全部不良
#     pyautogui.press("f12")
#     # 确认提交
#     pyautogui.press("return")
#     utils.close_aoi()

# @utils.screenshot_error_to_excel()
# def kjj_001_05():
#     pass

@utils.screenshot_error_to_excel()
def kjj_001_06():
    # 1.【打开】任一job
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 2.【设置】--【硬件设置】--【快捷键设置】，点击想要修改的快捷键后的【重置】按键，再点击输入框，使用修改后的快捷键，【应用】--【关闭】
    if utils.search_symbol(config.SETTING_DARK, 1):
        utils.click_by_png(config.SETTING_DARK)
    else:
        utils.search_symbol_erroring(config.SETTING_LIGHT, 1)
    utils.click_by_png(config.PARAM_HARDWARE_SETTING)
    time.sleep(2)
    utils.click_by_png(config.PARAM_SHORTCUT_KEY_SETTING)
    time.sleep(1)

    pyautogui.click((1040, 140))
    time.sleep(1)
    pyautogui.click((885,137))
    pyautogui.press("r")
    if not utils.search_symbol(config.WARNING):
        raise Exception("快捷键冲突未出现提醒")
    pyautogui.press("enter")
    pyautogui.click((1040, 140))
    pyautogui.click((885,137))
    pyautogui.press("p")

    utils.click_by_png(config.APPLY,timeout=1.5, tolerance=0.95)
    if utils.search_symbol(config.NO, 1.5, tolerance=0.95):
        utils.click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    else:
        utils.click_by_png(config.CLOSE, 2, timeout=1.5, tolerance=0.95)
    time.sleep(0.5)
    pyautogui.press('enter')
    while utils.search_symbol(config.PARAM_SETTING_TOPIC):
        time.sleep(1.5)
    # 3.进入测试视图界面，使用快捷键
    pyautogui.press("o")
    if utils.search_symbol(config.OPEN_PROGRAM_TOPIC) or utils.search_symbol(config.QUESTION_MARK):
        raise Exception("更改快捷键后 原快捷键仍有效")
    pyautogui.press("p")
    if utils.search_symbol(config.QUESTION_MARK):
        utils.click_by_png(config.NO)
    if not utils.search_symbol(config.OPEN_PROGRAM_TOPIC):
        raise Exception("修改的快捷键疑似无效")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def kjj_001_07():
    # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【元件编辑】-切换本体（引脚）/窗口（例如设置Y）
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 2.打开任意一个旧job,选择一个有本体有引脚的元件进入元件编辑界面
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(6)
    # 3.按Y
    a = utils.count_color_in_range(config.CENTRE, 100, (139,0,0))
    pyautogui.hotkey("ctrl", "b")
    time.sleep(1)
    b = utils.count_color_in_range(config.CENTRE, 100, (139,0,0))
    if b == a:
        raise Exception("切换本体(引脚)/窗口快捷键疑似无效")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def kjj_001_08():
    # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【元件编辑】-全选（例如设置Control+A）
    # 2.打开任意一个旧job,选择一个有多个算法窗口元件点击进入
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(6)
    # 3.按Control+A,
    a = utils.count_color_in_range(config.CENTRE, 100, (0,0,255))
    pyautogui.hotkey("ctrl", "a")
    time.sleep(1)
    b = utils.count_color_in_range(config.CENTRE, 100, (0,0,255))
    if b <= a:
        raise Exception("全选快捷键疑似无效")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def kjj_001_09():
    # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【元件编辑】-返回到整板视图（例如设置Backspace）
    # 2.打开任意一个旧job,选择任意一个元件点击进入
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 3.按Backspace
    time.sleep(5)
    pyautogui.press("backspace")
    # 4.选择是
    if utils.search_symbol(config.QUESTION_MARK,3):
        pyautogui.press("enter")
    else:
        raise Exception("无弹窗提示")
    if not utils.search_symbol(config.BOARD_AUTO,tolerance=0.75):
        raise Exception("返回到整版视图快捷键疑似无效")

    utils.close_aoi()

@utils.screenshot_error_to_excel()
def kjj_001_10():
    # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【元件编辑】-返回到整板视图（例如设置Backspace）
    # 2.打开任意一个旧job,选择任意一个元件点击进入
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 3.按Backspace
    time.sleep(5)
    pyautogui.press("backspace")
    # 4.选择否
    if utils.search_symbol(config.QUESTION_MARK,3):
        utils.click_by_png(config.NO)
    else:
        raise Exception("无弹窗提示")
    if utils.search_symbol(config.BOARD_AUTO,tolerance=0.75):
        raise Exception("未留在元件编辑界面")

    utils.close_aoi()


@utils.screenshot_error_to_excel()
def kjj_001_11():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    utils.check_allow_copy_cross_component(False)
    # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【元件编辑】-复制（例如设置Control+C）
    # 2.打开任意一个旧job,选择一个有多个算法窗口元件点击进入
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(6)
    # 3.选中某一元件窗口，按Control+C
    pyautogui.hotkey("ctrl", "tab")
    time.sleep(5) 
    # 4.【编辑】-【粘贴】
    pyautogui.hotkey("ctrl", "c")
    a = utils.count_color_in_range(config.CENTRE, 200, (0,0,255))
    pyautogui.hotkey("ctrl", "v")
    time.sleep(5)
    b = utils.count_color_in_range(config.CENTRE, 200, (0,0,255))
    if b == a:
        raise Exception("ctrl cv快捷键疑似无效")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def kjj_001_12():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    utils.check_allow_copy_cross_component(True)
    # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【元件编辑】-复制（例如设置Control+C）
    # 2.打开任意一个旧job,选择一个有多个算法窗口元件点击进入
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(6)
    # 3.选中某一元件窗口，按Control+C
    pyautogui.hotkey("ctrl", "tab")
    time.sleep(5) 
    pyautogui.hotkey("ctrl", "c")
    # 4.换一个不同料号的元件进入
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION)
    utils.click_component()
    if utils.search_symbol(config.QUESTION_MARK):
        utils.click_by_png(config.NO)
        time.sleep(5)
    pyautogui.click(config.CENTRE)
    # 5.【编辑】-【粘贴】
    if utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        pyautogui.hotkey("ctrl", "a")
        pyautogui.press("delete")
        time.sleep(1)
        pyautogui.press("enter")
        time.sleep(1)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(5)
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        raise Exception("跨元件复制失败，未发现新窗口")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def kjj_001_13():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【元件编辑】-粘贴（例如设置Control+V）
    # 2.打开任意一个旧job,选择一个有多个算法窗口元件点击进入
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(6)
    pyautogui.click(config.CENTRE)
    # 3.选中某一元件窗口，【编辑】-【复制】
    pyautogui.hotkey("ctrl", "tab")
    time.sleep(5) 
    a = utils.count_color_in_range(config.CENTRE, 400, (0,0,255))
    pyautogui.hotkey("ctrl", "c")
    time.sleep(2)
    pyautogui.press("escape")
    time.sleep(2)
    # 4.按Control+V
    pyautogui.hotkey("ctrl", "v")
    time.sleep(5)
    b = utils.count_color_in_range(config.CENTRE, 400, (0,0,255))
    if b <= a:
        raise Exception("黏贴失败")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def kjj_001_14():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    utils.check_allow_fallback(False)
    # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【元件编辑】-撤销（例如设置Control+Z）
    # 2.打开任意一个旧job,选择一个有多个算法窗口元件点击进入
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(6)
    # 3.选中某一元件窗口--移动位置--拉大算法框
    pyautogui.hotkey("ctrl", "tab")
    time.sleep(7) 
    utils.expand_choose_box()
    # 4.按Control+Z
    before_screenshot = pyautogui.screenshot(region=config.COMPONENT_REGION)
    pyautogui.hotkey("ctrl", "z")
    time.sleep(3)
    after_screenshot = pyautogui.screenshot(region=config.COMPONENT_REGION)
    if before_screenshot == after_screenshot:
        raise Exception("不勾选支持回退但仍被回退")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def kjj_001_15():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    utils.check_allow_fallback(True)
    # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【元件编辑】-撤销（例如设置Control+Z）
    # 2.打开任意一个旧job,选择一个有多个算法窗口元件点击进入
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(6)
    # 3.选中某一元件窗口--移动位置--拉大算法框
    pyautogui.hotkey("ctrl", "tab")
    time.sleep(5) 
    before_screenshot = pyautogui.screenshot(region=config.COMPONENT_REGION)
    utils.expand_choose_box()
    # 4.按Control+Z
    pyautogui.hotkey("ctrl", "z")
    time.sleep(3)
    after_screenshot = pyautogui.screenshot(region=config.COMPONENT_REGION)
    if before_screenshot != after_screenshot:
        raise Exception("勾选支持回退但回退失败")
    utils.close_aoi()
    
@utils.screenshot_error_to_excel()
def kjj_001_16():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    utils.check_allow_fallback(True)
    # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【元件编辑】-恢复（例如设置Control+Y）
    # 2.打开任意一个旧job,选择一个有多个算法窗口元件点击进入
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(6)
    # 3.选中某一元件窗口--拉大算法框
    pyautogui.hotkey("ctrl", "tab")
    time.sleep(5) 
    logger.info("a")
    mark_point_before = utils.get_color_direction_coordinate((0,0,255),config.COMPONENT_REGION,"left")
    utils.expand_choose_box()
    # 4.先按撤销（Control+Z）
    pyautogui.hotkey("ctrl", "z")
    time.sleep(5)
    logger.info("b")
    mark_point_after = utils.get_color_direction_coordinate((138,43,226),config.COMPONENT_REGION,"left")
    logger.info(f"mark_point_before: {mark_point_before}, mark_point_after: {mark_point_after}")
    if mark_point_before[0] >= mark_point_after[0]:
        raise Exception("算法框未恢复为初始大小")
    # 5.在按Control+Y
    logger.info("c")
    pyautogui.hotkey("ctrl", "y")
    time.sleep(3)
    logger.debug(3)
    logger.info(f"mark_point_after: {mark_point_after}")
    mark_point_final = utils.get_color_direction_coordinate((138,43,226),config.COMPONENT_REGION,"left")
    logger.info(f"mark_point_final: {mark_point_final}")
    if mark_point_after[0] <= mark_point_final[0]:
        raise Exception("算法框未恢复为步骤三操作大小")
    logger.info("d")

    utils.close_aoi()

@utils.screenshot_error_to_excel()
def kjj_001_17():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【元件编辑】-向左移动（例如设置Left）
    # 2.打开任意一个旧job,选择一个有多个算法窗口元件点击进入
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(6)
    # 3.选中某一元件窗口
    pyautogui.hotkey("ctrl", "tab")
    time.sleep(5) 
    # 4.按Left
    mark_point_before = utils.get_color_direction_coordinate((0,0,255),config.COMPONENT_REGION,"left")
    logger.info(f"mark_point_before: {mark_point_before}")
    for _ in range(20):
        pyautogui.press("left")
        time.sleep(0.1)
    mark_point_after = utils.get_color_direction_coordinate((0,0,255),config.COMPONENT_REGION,"left")
    logger.info(f"mark_point_after: {mark_point_after}")
    if mark_point_before[0] <= mark_point_after[0]:
        raise Exception("算法框未左移")
    # 5.选中cad框
    pyautogui.press("c")
    # 6.按Left
    mark_point_before = utils.get_color_direction_coordinate((0,0,255),config.COMPONENT_REGION,"left")
    logger.info(f"cad mark_point_before: {mark_point_before}")
    window_point_before = utils.get_color_direction_coordinate((138,43,226),config.COMPONENT_REGION,"left")
    logger.info(f"cad window_point_before: {window_point_before}")
    for _ in range(20):
        pyautogui.press("left")
        time.sleep(0.1)
    mark_point_after = utils.get_color_direction_coordinate((0,0,255),config.COMPONENT_REGION,"left")
    logger.info(f"cad mark_point_after: {mark_point_after}")
    window_point_after = utils.get_color_direction_coordinate((138,43,226),config.COMPONENT_REGION,"left")
    logger.info(f"cad window_point_after: {window_point_after}")
    if window_point_before[0] <= window_point_after[0]:
        raise Exception("算法框未左移")
    if mark_point_before[0] <= mark_point_after[0]:
        raise Exception("cad框未左移")
    utils.close_aoi()


@utils.screenshot_error_to_excel()
def kjj_001_18():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【元件编辑】-向右移动（例如设置Right）
    # 2.打开任意一个旧job,选择一个有多个算法窗口元件点击进入
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(6)
    # 3.选中某一元件窗口
    pyautogui.hotkey("ctrl", "tab")
    time.sleep(5) 
    # 4.按right
    mark_point_before = utils.get_color_direction_coordinate((0,0,255),config.COMPONENT_REGION,"left")
    logger.info(f"mark_point_before: {mark_point_before}")
    for _ in range(20):
        pyautogui.press("right")
        time.sleep(0.1)
    mark_point_after = utils.get_color_direction_coordinate((0,0,255),config.COMPONENT_REGION,"left")
    logger.info(f"mark_point_after: {mark_point_after}")
    if mark_point_before[0] >= mark_point_after[0]:
        raise Exception("算法框未右移")
    # 5.选中cad框
    pyautogui.press("c")
    # 6.按right
    mark_point_before = utils.get_color_direction_coordinate((0,0,255),config.COMPONENT_REGION,"left")
    logger.info(f"cad mark_point_before: {mark_point_before}")
    window_point_before = utils.get_color_direction_coordinate((138,43,226),config.COMPONENT_REGION,"left")
    logger.info(f"cad window_point_before: {window_point_before}")
    for _ in range(20):
        pyautogui.press("right")
        time.sleep(0.1)
    mark_point_after = utils.get_color_direction_coordinate((0,0,255),config.COMPONENT_REGION,"left")
    logger.info(f"cad mark_point_after: {mark_point_after}")
    window_point_after = utils.get_color_direction_coordinate((138,43,226),config.COMPONENT_REGION,"left")
    logger.info(f"cad window_point_after: {window_point_after}")
    if window_point_before[0] >= window_point_after[0]:
        raise Exception("算法框未右移")
    if mark_point_before[0] >= mark_point_after[0]:
        raise Exception("cad框未右移")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def kjj_001_19():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【元件编辑】-向上移动（例如设置Up）
    # 2.打开任意一个旧job,选择一个有多个算法窗口元件点击进入
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(6)
    # 3.选中某一元件窗口
    pyautogui.hotkey("ctrl", "tab")
    time.sleep(5) 
    # 4.按Up
    mark_point_before = utils.get_color_direction_coordinate((0,0,255),config.COMPONENT_REGION,"up")
    logger.info(f"mark_point_before: {mark_point_before}")
    for _ in range(20):
        pyautogui.press("up")
        time.sleep(0.1)
    mark_point_after = utils.get_color_direction_coordinate((0,0,255),config.COMPONENT_REGION,"up")
    logger.info(f"mark_point_after: {mark_point_after}")
    if mark_point_before[1] <= mark_point_after[1]:
        raise Exception("算法框未上移")
    # 5.选中cad框
    pyautogui.press("c")
    # 6.按Up
    mark_point_before = utils.get_color_direction_coordinate((0,0,255),config.COMPONENT_REGION,"up")
    window_point_before = utils.get_color_direction_coordinate((138,43,226),config.COMPONENT_REGION,"up")
    for _ in range(20):
        pyautogui.press("up")
        time.sleep(0.1)
    mark_point_after = utils.get_color_direction_coordinate((0,0,255),config.COMPONENT_REGION,"up")
    window_point_after = utils.get_color_direction_coordinate((138,43,226),config.COMPONENT_REGION,"up")
    if window_point_before[1] <= window_point_after[1]:
        raise Exception("算法框未上移")
    if mark_point_before[1] <= mark_point_after[1]:
        raise Exception("cad框未上移")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def kjj_001_20():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【元件编辑】-向下移动（例如设置Down）
    # 2.打开任意一个旧job,选择一个有多个算法窗口元件点击进入
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(6)
    # 3.选中某一元件窗口
    pyautogui.hotkey("ctrl", "tab")
    time.sleep(5) 
    # 4.按Down
    mark_point_before = utils.get_color_direction_coordinate((0,0,255),config.COMPONENT_REGION,"down")
    for _ in range(20):
        pyautogui.press("down")
        time.sleep(0.1)
    mark_point_after = utils.get_color_direction_coordinate((0,0,255),config.COMPONENT_REGION,"down")
    if mark_point_before[1] >= mark_point_after[1]:
        raise Exception("算法框未下移")
    # 5.选中cad框
    pyautogui.press("c")
    # 6.按Down
    mark_point_before = utils.get_color_direction_coordinate((0,0,255),config.COMPONENT_REGION,"down")
    window_point_before = utils.get_color_direction_coordinate((138,43,226),config.COMPONENT_REGION,"down")
    for _ in range(20):
        pyautogui.press("down")
        time.sleep(0.1)
    mark_point_after = utils.get_color_direction_coordinate((0,0,255),config.COMPONENT_REGION,"down")
    window_point_after = utils.get_color_direction_coordinate((138,43,226),config.COMPONENT_REGION,"down")
    if window_point_before[1] >= window_point_after[1]:
        raise Exception("算法框未下移")
    if mark_point_before[1] >= mark_point_after[1]:
        raise Exception("cad框未下移")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def kjj_001_21():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【元件编辑】-放大（例如设置Shift,Control+up）
    # 2.打开任意一个旧job,选择一个元件点击进入
    # 3.按Shift,Control+up
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(6)
    pyautogui.hotkey("ctrl", "tab")
    time.sleep(5) 
    before_color_pixel_num = utils.get_color_in_region((0,0,255),config.COMPONENT_REGION)
    logger.info(f"before_color_pixel_num: {before_color_pixel_num}")
    for _ in range(8):
        pyautogui.hotkey("ctrl", "shift", "up")
        time.sleep(1)
    after_color_pixel_num = utils.get_color_in_region((0,0,255),config.COMPONENT_REGION)
    logger.info(f"after_color_pixel_num: {after_color_pixel_num}")
    if before_color_pixel_num >= after_color_pixel_num:
        raise Exception("放大失败")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def kjj_001_22():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【元件编辑】-缩小（例如设置Shift,Control+Down）
    # 2.打开任意一个旧job,选择一个元件点击进入
    # 3.点击右下角＋号适当放大界面
    # 4.按Shift,Control+Down
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(6)
    pyautogui.hotkey("ctrl", "tab")
    time.sleep(5) 
    before_color_pixel_num = utils.get_color_in_region((0,0,255),config.COMPONENT_REGION)
    for _ in range(8):
        pyautogui.hotkey("ctrl", "shift", "down")
        time.sleep(1)
    after_color_pixel_num = utils.get_color_in_region((0,0,255),config.COMPONENT_REGION)
    if before_color_pixel_num <= after_color_pixel_num:
        raise Exception("缩小失败")
    utils.close_aoi()

# @utils.screenshot_error_to_excel()
# def kjj_001_23():
    # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【元件编辑】-增加引脚（例如设置P）
    # 2.打开任意一个旧job,选择一个有引脚的元件点击进入
    # 3.按P
    # 4.选择一边引脚，选择最边上引脚位置，左击鼠标按照引脚位置框起来松开鼠标
    # 5.点是
    # 6.同步骤四、五，选择另一边最边上引脚画上
    # 5.选中俩个画好的引脚
    # 6.按P，弹出新增引脚窗口(自动识别引脚数量)，点是
    # pass

@utils.screenshot_error_to_excel()
def kjj_001_24():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    pyautogui.hotkey("ctrl","a")
    pyautogui.press("delete")
    pyautogui.press("enter")
    time.sleep(3)
    # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【元件编辑】-增加窗口（例如设置W）
    # 2.打开任意一个旧job,选择一个元件点击进入
    # 3.按W，出现十字架，随意画一个框
    utils.add_window()
    if not utils.search_symbol(config.ADD_CHECKED_TYPE_SELF):
        raise Exception("未看到检测窗口类型为本体")
    # 4.随机选择一个算法加上，比如选择方形定位+默认，点是
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    time.sleep(8)
    if not utils.search_symbol(config.ALG_W_0,region=config.COMPONENT_WINDOW_REGION):
        raise Exception("窗口添加失败")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def kjj_001_25():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    pyautogui.hotkey("ctrl","a")
    time.sleep(3)
    pyautogui.press("delete")
    pyautogui.press("enter")
    time.sleep(3)
    pyautogui.press("escape")
    time.sleep(1)
    # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【元件编辑】-增加窗口（例如设置W）
    # 2.打开任意一个旧job,选择一个有引脚元件点击进入
    # 3.点击任意引脚位置，按W，出现十字架，随意画一个框
    for _ in range(5):
        pyautogui.hotkey("ctrl", "shift", "up")
        time.sleep(1)
    # if not utils.click_color(1,config.COMPONENT_REGION,(70,130,180)):
    #     raise Exception("未找到引脚")
    utils.add_window()
    # if not utils.search_symbol(config.ADD_CHECKED_TYPE_PIN):
    #     raise Exception("未看到检测窗口类型为引脚")
    # 5.随机选择一个算法加上，比如选择颜色面积+默认，点是
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    time.sleep(8)
    if not utils.search_symbol(config.ALG_W_0,region=config.COMPONENT_WINDOW_REGION):
        raise Exception("窗口添加失败")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def kjj_001_26():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【元件编辑】-测试窗口（例如设置Space）
    # 2.打开任意一个旧job,选择一个有多个算法窗口元件点击进入
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(6)
    # 3.选中某一元件窗口
    pyautogui.hotkey("ctrl", "tab")
    time.sleep(5) 
    # 4.按Space
    pyautogui.press("space")
    time.sleep(5)
    good = utils.click_color(0,config.CHECK_RESULT_REGION,(0,128,0))
    ng = utils.click_color(0,config.CHECK_RESULT_REGION,(255,0,0))
    if not good and not ng:
        raise Exception("未看到测试结果")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def kjj_001_27():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    utils.check_auto_choose_window(False)
    # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【元件编辑】-测试窗口（例如设置Space）
    # 2.打开任意一个旧job,选择一个有多个算法窗口元件点击进入
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(6)
    # 3.选中某一元件窗口
    pyautogui.press("esc")
    # 4.按Space
    pyautogui.press("space")
    if utils.search_symbol(config.WARNING):
        raise Exception("不选择元件窗口的时候点击测试窗口时未出现弹框")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def kjj_001_28():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【元件编辑】-测试元件（例如设置S）
    # 2.打开任意一个旧job,选择一个有多个算法窗口元件点击进入
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(6)
    # 3.按S
    start_time = time.time()
    pyautogui.press("d")
    if not utils.search_symbol(config.TESTING_COMPONENT):
        raise Exception("测试元件快捷键使用后疑似无反应")
    while utils.search_symbol(config.TESTING_COMPONENT):
        if time.time() - start_time > 1200:  # 20分钟
            raise Exception("测试元件时超过20分钟")
        time.sleep(5)
    # 4.测试完成
    good = utils.click_color(0,config.CHECK_RESULT_REGION,(0,128,0))
    ng = utils.click_color(0,config.CHECK_RESULT_REGION,(255,0,0))
    if not good and not ng:
        raise Exception("未看到测试结果")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def kjj_001_29():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【元件编辑】-测试料号（例如设置D）
    # 2.打开任意一个旧job,选择某个料号下有多个元件的其中一个元件点击进入
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(6)
    # 3.按D
    start_time = time.time()
    pyautogui.press("f")
    if not utils.search_symbol(config.TESTING_COMPONENT):
        raise Exception("测试料号快捷键使用后疑似无反应")
    while utils.search_symbol(config.TESTING_COMPONENT):
        if time.time() - start_time > 1200:  # 20分钟
            raise Exception("测试料号时超过20分钟")
        time.sleep(5)
    # 4.测试完成
    good = utils.click_color(0,config.CHECK_RESULT_REGION,(0,128,0))
    ng = utils.click_color(0,config.CHECK_RESULT_REGION,(255,0,0))
    if not good and not ng:
        raise Exception("未看到测试结果")
    utils.close_aoi()
@utils.screenshot_error_to_excel()
def kjj_001_30():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【元件编辑】-测试整板（例如设置F）
    # 2.打开任意一个旧job,选择一个元件点击进入
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(6)
    # 3.按F
    start_time = time.time()
    pyautogui.press("b")
    if not utils.search_symbol(config.TESTING_COMPONENT):
        raise Exception("测试整板快捷键疑似无效")
    while utils.search_symbol(config.TESTING_COMPONENT):
        if time.time() - start_time > 1200:  # 20分钟
            raise Exception("测试整板时超过20分钟")
        time.sleep(5)
    # 4.测试完成
    good = utils.click_color(0,config.CHECK_RESULT_REGION,(0,128,0))
    ng = utils.click_color(0,config.CHECK_RESULT_REGION,(255,0,0))
    if not good and not ng:
        raise Exception("未看到测试结果")
    utils.close_aoi()

# @utils.screenshot_error_to_excel()
# def kjj_001_31():
    # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【元件编辑】-导入此元件库（例如设置F1）
    # 2.打开任意一个旧job,选择一个元件点击进入,删除所有检测框
    # 3.按F1
    # 4.下拉选择有此元件的元件库--是
    # 5.菜单栏点击【元件库】--【手动选择】--【元件库视图】，找到导入此元件的信息，对比导入的内容
    # 6.切换查看此料号下其他元件
    # pass

# @utils.screenshot_error_to_excel()
# def kjj_001_32():
    # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【元件编辑】-导入所有元件库（例如设置F2）
    # 2.打开任意一个旧job,选择一个元件点击进入,
    # 3.按F2
    # 4.下拉选择某个的元件库--是
    # 5.菜单栏点击【元件库】--【手动选择】--【元件库视图】，找到导入此元件的信息，对比导入的内容
    # 6.在任意切换一个元件，重复5步骤进行对比
    # pass

@utils.screenshot_error_to_excel()
def kjj_001_33():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【元件编辑】-导出此料号到元件库（例如设置F3）
    # 2.打开任意一个旧job,选择一个有算法窗口的元件点击进入
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(6)
    # 3.按F3
    pyautogui.press("f2")
    if not utils.search_symbol(config.ELEMENTS_INFORMATION):
        raise Exception("导出此料号到元件库快捷键疑似无效")
    # 4.分类名称输入一个新的元件库名称，其余默认--是
    elements_type_name = "elements_type_name"
    utils.write_text((960,470), elements_type_name)
    time.sleep(1)
    utils.click_by_png(config.YES)
    while utils.search_symbol(config.EXPORTING_ELEMENTS):
        time.sleep(1.5)
    time.sleep(1)
    # 5.菜单栏点击【元件库】--【手动选择】--【元件库视图】，点击√和刷新
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.MANUAL_SELECT)
    # 6.找到导出此元件的信息（设置的新元件库，芯片类型，封装，料号下），对比此时元件上的内容
    time.sleep(2)
    utils.click_by_png(config.ELEMENTS_VIEW_REFRESH, region=config.ELEMENTS_VIEW_REGION,tolerance=0.95)
    pyautogui.click((546,232))
    utils.is_checked((375,246),(387,258),False)
    if not utils.drop_down_box_search(0, config.ELEMENTS_TYPE_NAME, region=config.ELEMENTS_VIEW_DROPDOWN_BOX_REGION):
        raise Exception("手动选择框内没有找到新增的元件库")
    utils.click_by_png(config.ELEMENTS_VIEW_ABC, region=config.ELEMENTS_VIEW_REGION)
    if not utils.search_symbol(config.BOARD_HARDWARE_ICON,region=config.ELEMENTS_VIEW_REGION):
        raise Exception("手动选择框内没有找到对应元件")
    utils.click_by_png(config.BOARD_HARDWARE_ICON,region=config.ELEMENTS_VIEW_REGION)
    time.sleep(1)
    # 查看图片底下信息
    image_point = (666,333)
    pyautogui.click(image_point)
    time.sleep(0.5)
    component_information = utils.read_text(400,700)
    # 比对内容
    pyautogui.click(config.CENTRE)
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)
    time.sleep(1)    

    # 封装类型
    utils.is_checked((1082,274),(1094,286),True)
    package_type = utils.read_text(920,280)
    if package_type is None or package_type not in component_information:
        logger.error(f"{package_type} 的信息不一致或缺失: {package_type}")
        raise Exception(f"{package_type} 的信息不一致或缺失: {package_type}")
    utils.close_aoi()
@utils.screenshot_error_to_excel()
def kjj_001_34():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【元件编辑】-导出所有料号到元件库（例如设置F4）
    # 2.打开任意一个旧job,选择一个有算法窗口的元件点击进入
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(6)
        utils.click_by_png(config.EDIT_BACK)
        if utils.search_symbol(config.QUESTION_MARK):
            pyautogui.press("enter")
            time.sleep(5)
        utils.click_by_png(config.TEST,2, region=config.BOARD_INFORMATION_REGION,tolerance=0.95)
        time.sleep(5)
    # 3.按F4
    # 确保各元件都被勾选
    if utils.search_symbol(config.PART_CHOSED):
        utils.click_by_png(config.PART_CHOSED)
    else:
        utils.is_checked((66,255),(78,267),True)
    pyautogui.press("f4")
    if not utils.search_symbol(config.QUESTION_MARK):
        raise Exception("导出所有料号到元件库快捷键疑似无效")
    # 4.分类名称输入一个新的元件库名称，其余默认--是
    utils.write_text((900, 525), "elements_type_name")
    utils.click_by_png(config.YES)
    while utils.search_symbol(config.EXPORTING_ELEMENTS):
        time.sleep(1.5)
    time.sleep(0.5)
    # 5.菜单栏点击【元件库】--【手动选择】--【元件库视图】，点击√和刷新
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.MANUAL_SELECT)
    # 6.找到导出此元件的信息（设置的新元件库，芯片类型，封装，料号下），对比此时元件上的内容
    time.sleep(2)
    utils.click_by_png(config.ELEMENTS_VIEW_REFRESH, region=config.ELEMENTS_VIEW_REGION,tolerance=0.95)
    pyautogui.click((546,232))
    utils.is_checked((375,246),(387,258),False)
    if not utils.drop_down_box_search(0, config.ELEMENTS_TYPE_NAME, region=config.ELEMENTS_VIEW_DROPDOWN_BOX_REGION):
        raise Exception("手动选择框内没有找到新增的元件库")
    utils.click_by_png(config.BOARD_ENLARGE, region=config.ELEMENTS_VIEW_REGION,tolerance=0.95)
    if not utils.search_symbol(config.BOARD_HARDWARE_ICON,region=config.ELEMENTS_VIEW_REGION):
        raise Exception("手动选择框内没有找到对应元件")
    utils.click_by_png(config.BOARD_HARDWARE_ICON,region=config.ELEMENTS_VIEW_REGION)
    time.sleep(1)
    # 查看图片底下信息
    image_point = (666,333)
    pyautogui.click(image_point)
    time.sleep(0.5)
    component_information = utils.read_text(400,700)
    # 比对内容
    pyautogui.click(config.CENTRE)
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)
    time.sleep(1)    
    logger.debug(1)
    # 封装类型
    utils.is_checked((1082,274),(1094,286),True)
    package_type = utils.read_text(920,280)
    if package_type is None or package_type not in component_information:
        logger.error(f"{package_type} 的信息不一致或缺失: {package_type}")
        raise Exception(f"{package_type} 的信息不一致或缺失: {package_type}")
    utils.click_by_png(config.PROGRAM_ATTRIBUTE_CLOSE)
    logger.debug(2)
    # 7.换任意一个其他料号的元件，重复步骤5和6
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION)
    utils.click_component()
    if utils.search_symbol(config.QUESTION_MARK):
        utils.click_by_png(config.NO)
        time.sleep(5)
    pyautogui.click((546,232))
    utils.is_checked((375,246),(387,258),False)
    logger.debug(3)
    if not utils.drop_down_box_search(0, config.ELEMENTS_TYPE_NAME, region=config.ELEMENTS_VIEW_DROPDOWN_BOX_REGION):
        raise Exception("手动选择框内没有找到新增的元件库")
    utils.click_by_png(config.ELEMENTS_VIEW_REFRESH, region=config.ELEMENTS_VIEW_REGION,tolerance=0.95)
    utils.click_by_png(config.ELEMENTS_VIEW_ABC, region=config.ELEMENTS_VIEW_REGION)
    if not utils.search_symbol(config.BOARD_HARDWARE_ICON,region=config.ELEMENTS_VIEW_REGION):
        raise Exception("手动选择框内没有找到对应元件")
    utils.click_by_png(config.BOARD_HARDWARE_ICON,region=config.ELEMENTS_VIEW_REGION)
    time.sleep(1)
    # 查看图片底下信息
    image_point = (666,333)
    pyautogui.click(image_point)
    time.sleep(0.5)
    component_information = utils.read_text(400,700)
    # 比对内容
    pyautogui.click(config.CENTRE)
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)
    time.sleep(1)    
    logger.debug(4)
    # 封装类型
    utils.is_checked((1082,274),(1094,286),True)
    package_type = utils.read_text(920,280)
    if package_type is None or package_type not in component_information:
        logger.error(f"{package_type} 的信息不一致或缺失: {package_type}")
        raise Exception(f"{package_type} 的信息不一致或缺失: {package_type}")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def kjj_001_35():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【元件编辑】-旋转元件（例如设置T）
    # 2.打开任意一个旧job,选择一个元件点击进入
    # 3.按R
    before_screenshot = pyautogui.screenshot(region=config.COMPONENT_REGION)
    pyautogui.press("r")
    after_screenshot = pyautogui.screenshot(region=config.COMPONENT_REGION)
    if before_screenshot == after_screenshot:
        raise Exception("旋转元件快捷键疑似无效")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def kjj_001_36():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【元件编辑】-选择元件CAD框（例如设置A）
    # 2.打开任意一个旧job,选择一个元件点击进入
    # 3.按A
    pyautogui.press("c")
    if not utils.check_color_in_region((0,0,255), config.COMPONENT_REGION):
        raise Exception("选择元件CAD框快捷键疑似无效")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def kjj_001_37():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【元件编辑】-链接所有元件检测框（例如设置Z）
    # 2.打开任意一个旧job,选择这个元件点击进入
    # 3.按Z
    def add_and_click(image):
        utils.add_window()
        utils.click_by_png(image)
        utils.click_by_png(config.YES)
        time.sleep(8)

    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        add_and_click(config.SQUARE_POSITIONING)
        add_and_click(config.COLOR_AREA)
    elif not utils.search_symbol(config.ALG_W_1, 5, region=config.COMPONENT_WINDOW_REGION):
        add_and_click(config.COLOR_AREA)
    
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("f5")
    time.sleep(1)
    # if not utils.search_symbol(config.QUESTION_MARK):
    #     raise Exception("未弹 请选择被连接的父窗口 弹窗")
    # pyautogui.press("enter")
    # time.sleep(1)
    if not utils.check_color_in_region((220, 20, 60), config.COMPONENT_REGION):
        raise Exception("链接所有元件检测框快捷键疑似无效")
    utils.close_aoi()

# @utils.screenshot_error_to_excel()
# def kjj_001_38():
#     utils.check_and_launch_aoi()
#     utils.ensure_in_edit_mode()
#     # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【元件编辑】-链接所有元件检测框（例如设置Z）
#     # 2.打开任意一个旧job,选择这个元件点击进入
#     # 3.按Z
#     def add_and_click(image):
#         utils.add_window()
#         utils.click_by_png(image)
#         utils.click_by_png(config.YES)
#         time.sleep(8)

#     if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
#         add_and_click(config.SQUARE_POSITIONING)
#         add_and_click(config.COLOR_AREA)
#     elif not utils.search_symbol(config.ALG_W_1, 5, region=config.COMPONENT_WINDOW_REGION):
#         add_and_click(config.COLOR_AREA)

#     pyautogui.hotkey("ctrl", "a")
#     pyautogui.press("f5")
#     time.sleep(1)
#     # 4.选择一个窗口作为父窗口--是
#     if not utils.search_symbol(config.QUESTION_MARK):
#         raise Exception("未弹 请选择被连接的父窗口 弹窗")
#     pyautogui.press("enter")
#     time.sleep(1)
#     if not utils.check_color_in_region((220, 20, 60), config.COMPONENT_REGION):
#         raise Exception("链接所有元件检测框快捷键疑似无效")

#     utils.close_aoi()

@utils.screenshot_error_to_excel()
def kjj_001_39():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【元件编辑】-获取颜色（例如设置C）
    # 2.打开任意一个旧job,选择一个元件点击进入，选择任意可以抽色的算法，不如本体检测
    # 3.按C-选择你想抽取颜色的区域框一下
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.X_OFFSET)
    utils.click_by_png(config.YES)
    time.sleep(8)
    if not utils.search_symbol(config.ALG_IMAGE_TYPE_WEIGHT,region=config.ALG_PARAM_REGION):
        pyautogui.click((1885,375))
        utils.click_by_png(config.ALG_IMAGE_TYPE_CHOOSE_WEIGHT, region=config.ALG_PARAM_REGION)
    pyautogui.press("s")
    pyautogui.click(config.CENTRE)
    if not utils.search_symbol(config.ALG_IMAGE_TYPE_COLOR_SPACE, region=config.ALG_PARAM_REGION):
        raise Exception("获取颜色快捷键疑似无效")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def kjj_001_40():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【元件编辑】-选择下一个窗口（例如设置Control+Tab）
    # 2.打开任意一个旧job,选择一个有多检测窗口的元件点击进入。在选择随意一个窗口
    # 3.按Control+Tab
    if not utils.search_symbol(config.ALG_W_1, 5, region=config.COMPONENT_WINDOW_REGION):
        if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
            utils.add_window()
            utils.click_by_png(config.SQUARE_POSITIONING)
            utils.click_by_png(config.YES)
            time.sleep(8)
        else:
            utils.add_window()
            utils.click_by_png(config.SQUARE_POSITIONING)
            utils.click_by_png(config.YES)
            time.sleep(8)
    before_screenshot = pyautogui.screenshot(region=config.ALG_PARAM_REGION)
    pyautogui.hotkey("ctrl", "tab")
    time.sleep(5) 
    after_screenshot = pyautogui.screenshot(region=config.ALG_PARAM_REGION)
    if before_screenshot == after_screenshot:
        raise Exception("选择下一个窗口快捷键疑似无效")

@utils.screenshot_error_to_excel()
def kjj_001_41():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【元件编辑】-下一个元件（例如设置X）
    # 2.打开任意一个旧job,选择一个元件点击进入
    # 4.按X
    try:
        test_y_before = pyautogui.locateOnScreen(config.TEST, region=config.BOARD_COMPONENTS_REGION).top + pyautogui.locateOnScreen(config.TEST, region=config.BOARD_COMPONENTS_REGION).height // 2
        pyautogui.press("x")
        if utils.search_symbol(config.QUESTION_MARK):
            utils.click_by_png(config.NO)
        time.sleep(3)
        test_y_after = pyautogui.locateOnScreen(config.TEST, region=config.BOARD_COMPONENTS_REGION).top + pyautogui.locateOnScreen(config.TEST, region=config.BOARD_COMPONENTS_REGION).height // 2
    except pyautogui.ImageNotFoundException:
        raise Exception("移动到下一个元件时，未能识别到被选中的元件")
    # 查看y坐标有没有大于7的变动
    if abs(test_y_before - test_y_after) <= 7:
        raise Exception("疑似未能切换到下一个元件")
    utils.close_aoi()

# @utils.screenshot_error_to_excel()
# def kjj_001_42():
#     utils.check_and_launch_aoi()
#     utils.ensure_in_edit_mode()
#     # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【元件编辑】-显示首件图（例如设置J）
#     # 2.打开此job,选择一个元件点击进入
#     # 3.按J
#     pyautogui.press("j")
#     while utils.search_symbol(config.QUESTION_MARK):
#         pyautogui.press("enter")
#         time.sleep(1)

@utils.screenshot_error_to_excel()
def kjj_001_43():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【元件编辑】-显示元件3D图（例如设置L）
    # 2.打开任意一个job,选择一个有算法的元件点击进入
    # 3.按L
    pyautogui.press("l")
    time.sleep(5)
    black_pixel_count = 0
    total_pixels = 0
    screenshot = pyautogui.screenshot(region=config.COMPONENT_REGION)
    for x in range(screenshot.width):
        for y in range(screenshot.height):
            if screenshot.getpixel((x, y)) == (0, 0, 0):
                black_pixel_count += 1
            total_pixels += 1
    if total_pixels > 0:
        black_pixel_ratio = black_pixel_count / total_pixels * 100
        if black_pixel_ratio < 40:
            raise Exception("显示元件3D图快捷键疑似失效")
    utils.close_aoi()

# @utils.screenshot_error_to_excel()
# def kjj_001_44():
#     # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【元件编辑】-增加焊盘标志（例如设置H）
#     # 2.打开任意一个job,选择一个元件点击进入
#     # 3.按H
#     # 4.在焊盘位置画一个框
#     pass

# @utils.screenshot_error_to_excel()
# def kjj_001_45():
#     # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【元件编辑】-整板异物保存调试选项（例如设置A）
#     # 2.运行测试--点击进入细调界面--左边整板信息点击整板异物
#     # 3.按A
#     # 4.勾选保存整板异物--是--返回测试界面--在运行一片
#     # 5.运行结束查看此路径下D:\EYAOI\Bin\Debug
#     pass

# @utils.screenshot_error_to_excel()
# def kjj_001_46():
#     # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【元件编辑】-整板异物保存调试选项（例如设置A）
#     # 2.运行测试--点击进入细调界面--左边整板信息点击整板异物
#     # 3.按A
#     # 4.勾选保存整板异物NG--是--返回测试界面--在运行一片
#     # 5.运行结束查看此路径下D:\EYAOI\Bin\Debug
#     pass

# @utils.screenshot_error_to_excel()
# def kjj_001_47():
#     # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【元件编辑】-整板异物保存调试选项（例如设置A）
#     # 2.运行测试--点击进入细调界面--左边整板信息点击整板异物
#     # 3.按A
#     # 4.勾选保存整板异物--是
#     # 5.整板信息--整板异物--点击右下角测试整板异物
#     # 6.进度条消失，查看此路径下D:\EYAOI\Bin\Debug
#     pass

# @utils.screenshot_error_to_excel()
# def kjj_001_48():
#     # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【元件编辑】-整板异物保存调试选项（例如设置A）
#     # 2.运行测试--点击进入细调界面--左边整板信息点击整板异物
#     # 3.按A
#     # 4.勾选保存整板异物NG--是
#     # 5.整板信息--整板异物--点击右下角测试整板异物
#     # 7.进度条消失，查看此路径下D:\EYAOI\Bin\Debug
#     pass

@utils.screenshot_error_to_excel()
def kjj_001_49():
    utils.check_and_launch_aoi()
    utils.open_program()
    # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【主程序】-打开程式（例如设置O）
    # 2.打开任意一个job,加载完毕后，在主程序界面
    # 3.按O
    pyautogui.press("o")
    if not utils.search_symbol(config.OPEN_PROGRAM_TOPIC, 3):
        raise Exception("打开程式快捷键疑似无效")
    # 4.选择任意你想打开的程式，将其从程式列表双击进入被选程式列表，点是
    symbols = [config.OPEN_PROGRAM_PLUS, config.OPEN_PROGRAM_CURSOR]
    for symbol in symbols:
        if utils.search_symbol(symbol, 3):
            utils.click_by_png(symbol, 2)
            utils.click_by_png(config.YES)
            while utils.search_symbol(config.PROGRAM_LOADING, 5):
                time.sleep(5)
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def kjj_001_50():
    utils.check_and_launch_aoi()
    # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【主程序】-保存Debug程式（例如设置F12）
    # 2.打开任意一个job,任意选择一个元件点击进入
    utils.ensure_in_edit_mode()
    # 3.按F12
    pyautogui.hotkey("ctrl", "shift", "f12")
    while utils.search_symbol(config.EXPORTING_DJB):
        time.sleep(1)
    if not utils.search_symbol(config.SAVE_AS_TOPIC):
        raise Exception("保存Debug程式快捷键疑似无效")
    # 4.进度条结束
    # 5.选择djb要存的路径，点击保存
    path = utils.read_text(125,45)
    logger.debug(f"路径: {path}")
    utils.write_text((155,435),"test_save_debug")
    clipboard_content = pyperclip.paste()
    logger.debug(f"黏贴板的内容: {clipboard_content}")
    utils.click_by_png(config.WINDOW_SAVE)
    time.sleep(5)
    # 6.打开存的路径位置，查看
    now = time.time()
    for file in os.listdir(path):
        if file.endswith('.djb'):
            file_path = os.path.join(path, file)
            file_time = os.path.getmtime(file_path)
            if now - file_time <= 120:  # 检查文件是否在2分钟内创建
                logger.info(f"在{path}下找到djb文件")
                utils.close_aoi()
                return
    logger.info(f"未能在{path}下找到djb文件")
    raise Exception(f"未能在{path}下找到djb文件")
    
    

# @utils.screenshot_error_to_excel()
# def kjj_001_51():
#     utils.check_and_launch_aoi()
#     # 1.接“主程序界面--保存Debug程式快捷键“案例
#     # 2.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【主程序】-打开Debug程式（例如设置F2）
#     # 3.打开任意job,按F2
#     # 4.选择“主程序界面--保存Debug程式快捷键“案例中保存的djb文件，打开
#     utils.ensure_in_edit_mode()
#     pyautogui.hotkey("ctrl", "shift", "f2")
#     if not utils.search_symbol(config.OPEN_DJB_TOPIC):
#         raise Exception("打开Debug程式快捷键疑似无效")
#     utils.write_text((215, 475), "test_save_debug")
#     pyautogui.press("enter")
#     time.sleep(3)
#     pyautogui.click(config.CENTRE)
#     utils.add_window()
#     if not utils.search_symbol(config.SQUARE_POSITIONING):
#         raise Exception("打开djb后疑似无法编辑")
#     utils.close_aoi()

@utils.screenshot_error_to_excel()
def kjj_001_52():
    utils.check_and_launch_aoi()
    utils.open_program()
    # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【主程序】-打开元件库（例如设置C）
    # 2.打开任意job,选择任意一个元件进入元件编辑界面
    # 3.按C
    pyautogui.press("f5")
    if not utils.search_symbol(config.ELEMENTS_VIEW_SEARCH, region=config.ELEMENTS_VIEW_REGION):
        raise Exception("打开元件库快捷键疑似无效")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def kjj_001_53():
    utils.check_and_launch_aoi()
    utils.open_program()
    # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【主程序】-删除所有记录文件（例如设置Ctrl,Shift+L）
    # 2.打开任意job,在整板界面
    # 3.按Ctrl,Shift+L
    pyautogui.hotkey("ctrl", "shift", "l")
    if not utils.search_symbol(config.DELETE_LOG_SUCCESS):
        raise Exception("删除所有记录文件快捷键疑似无效")
    utils.close_aoi()

# @utils.screenshot_error_to_excel()
# def kjj_001_54():
#     # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【主程序】-进板（例如设置Insert）
#     # 2.打开任意job，在整板界面选择任意一个可以看到右上角轨道信息的Tab（比如系统）
#     # 3.按Insert
#     pass

# @utils.screenshot_error_to_excel()
# def kjj_001_55():
#     # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【主程序】-归零（例如设置Home）
#     # 2.打开任意job，选择整板界面
#     # 3.按Home
#     # 4.归零完成后
#     pass

# @utils.screenshot_error_to_excel()
# def kjj_001_56():
#     # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【主程序】-开始测试（例如设置R）
#     # 2.打开任意job,选择整板界面
#     # 3.按R，【请确认如下配置项】-【是】-【元件标准图检查】-【是】
#     pass

# @utils.screenshot_error_to_excel()
# def kjj_001_57():
#     # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【主程序】-停止测试（例如设置E）
#     # 2.打开任意job,点击运行
#     # 3.按E
#     pass

# @utils.screenshot_error_to_excel()
# def kjj_001_58():
#     # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【主程序】-开始测试（例如设置R）
#     # 2.接停止测试快捷键案例，在测试界面
#     # 3.按R
#     # 4.选是（有可能有元件标准图检查汇总界面，点是即可 ）
#     pass

@utils.screenshot_error_to_excel()
def kjj_001_59():
    utils.check_and_launch_aoi()
    utils.open_program()
    # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【主程序】-保存程式（例如设置Ctrl+S）
    # 2.打开任意job,在整板界面
    # 3.按Ctrl+S
    pyautogui.press("s")
    if not utils.search_symbol(config.QUESTION_MARK):
        raise Exception("保存程式快捷键疑似无效")
    # 4.点是
    pyautogui.press("enter")
    # 5.进度条结束
    while utils.search_symbol(config.SAVING_PROGRAM):
        time.sleep(1)
    if not utils.search_symbol(config.LOG_SAVE_SUCCESS, region=config.LOG_REGION):
        raise Exception("未显示保存完成")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def kjj_001_60():
    utils.check_and_launch_aoi()
    utils.open_program()
    utils.check_not_allow_paste_component_to_blank(False)
    utils.check_not_allow_paste_component_to_component(False)
    # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【整板编辑】-复制元件（例如设置Ctrl+C）
    # 2.打开任意job，进入整板界面，任意选择一个元件选中
    utils.click_color(1, config.COMPONENT_REGION, (0,255,0))
    # 3.按Ctrl+C
    time.sleep(1)
    pyautogui.hotkey("ctrl", "c")
    # 4.选择任意一个其他大小不一样的元件，点击选择粘贴到此元件
    utils.click_color(1, config.COMPONENT_REGION, (0,255,0))
    mouse_coordinate = pyautogui.position()
    pyautogui.click((260,10))
    before_count = utils.count_color_in_range(mouse_coordinate, 100, (0,255,0))
    pyautogui.click(mouse_coordinate)
    time.sleep(1)
    pyautogui.rightClick(mouse_coordinate)
    utils.click_by_png(config.PASTE_TO_COMPONENT)
    # 5.点是
    if not utils.search_symbol(config.QUESTION_MARK):
        raise Exception("黏贴到此元件未出现弹窗")
    pyautogui.press("enter")
    time.sleep(3)
    after_count = utils.count_color_in_range(mouse_coordinate, 100, (0,255,0))
    if after_count == before_count:
        raise Exception("此元件疑似无黏贴到另一个所选的元件")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def kjj_001_61():
    utils.check_and_launch_aoi()
    utils.open_program()
    utils.check_not_allow_paste_component_to_component(False)
    # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【整板编辑】-粘贴元件（例如设置Ctrl+V）
    # 2.打开任意job，进入整板界面，任意选择一个元件选中,右击选择复制此元件
    utils.click_color(1, config.COMPONENT_REGION, (0,255,0))
    pyautogui.hotkey("ctrl", "c")
    # 3.选择任意一个其他元件，按Ctrl+V
    utils.click_color(0, config.COMPONENT_REGION, (0,255,0))
    mouse_coordinate = pyautogui.position()
    pyautogui.click((260,10))
    before_count = utils.count_color_in_range(mouse_coordinate, 100, (0,255,0))
    pyautogui.click(mouse_coordinate)
    pyautogui.hotkey("ctrl", "v")
    # 4.点是
    if not utils.search_symbol(config.QUESTION_MARK):
        raise Exception("黏贴到此元件未出现弹窗")
    pyautogui.press("enter")
    time.sleep(3)
    after_count = utils.count_color_in_range(mouse_coordinate, 100, (0,255,0))
    if after_count == before_count:
        raise Exception("此元件疑似无黏贴到另一个所选的元件")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def kjj_001_62():
    utils.check_and_launch_aoi()
    utils.open_program()
    utils.check_not_allow_paste_component_to_component(True)
    # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【整板编辑】-粘贴元件（例如设置Ctrl+V）
    # 2.打开任意job，进入整板界面，任意选择一个元件选中,右击选择复制此元件
    utils.click_color(1, config.COMPONENT_REGION, (0,255,0))
    pyautogui.hotkey("ctrl", "c")
    # 3.选择任意一个其他元件，按Ctrl+V
    utils.click_color(1, config.COMPONENT_REGION, (0,255,0))
    mouse_coordinate = pyautogui.position()
    before_count = utils.count_color_in_range(mouse_coordinate, 100, (0,0,255))
    pyautogui.hotkey("ctrl", "v")
    time.sleep(3)
    after_count = utils.count_color_in_range(mouse_coordinate, 100, (0,0,255))
    if after_count != before_count:
        raise Exception("此元件疑似被黏贴到另一个所选的元件")
    utils.close_aoi()
@utils.screenshot_error_to_excel()
def kjj_001_63():
    utils.check_and_launch_aoi()
    utils.open_program()
    utils.check_not_allow_paste_component_to_blank(False)
    # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【整板编辑】-粘贴元件（例如设置Ctrl+V）
    # 2.打开任意job，进入整板界面，任意选择一个元件选中,右击选择复制此元件
    utils.click_color(1, config.COMPONENT_REGION, (0,255,0))
    pyautogui.hotkey("ctrl", "c")
    # 4.选择任意一个空白位置，按Ctrl+V
    random_x = random.randint(config.COMPONENT_REGION[0], config.COMPONENT_REGION[2])
    random_y = random.randint(config.COMPONENT_REGION[1], config.COMPONENT_REGION[3])
    pyautogui.click((random_x, random_y))
    before_count = utils.count_color_in_range((random_x,random_y), 100, (0,255,0))
    pyautogui.hotkey("ctrl","v")
    time.sleep(3)
    after_count = utils.count_color_in_range((random_x,random_y), 100, (0,255,0))
    if after_count <= before_count:
        raise Exception("疑似未能被黏贴到空白处")
    utils.close_aoi()
@utils.screenshot_error_to_excel()
def kjj_001_64():
    utils.check_and_launch_aoi()
    utils.open_program()
    utils.check_not_allow_paste_component_to_blank(True)
    # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【整板编辑】-粘贴元件（例如设置Ctrl+V）
    # 2.打开任意job，进入整板界面，任意选择一个元件选中,右击选择复制此元件
    utils.click_color(1, config.COMPONENT_REGION, (0,255,0))
    pyautogui.hotkey("ctrl", "c")
    # 5.鼠标选择任意一个空白位置，按Ctrl+V
    random_x = random.randint(config.COMPONENT_REGION[0], config.COMPONENT_REGION[2])
    random_y = random.randint(config.COMPONENT_REGION[1], config.COMPONENT_REGION[3])
    pyautogui.click((random_x, random_y))
    before_count = utils.count_color_in_range((random_x,random_y), 100, (0,255,0))
    pyautogui.hotkey("ctrl","v")
    time.sleep(3)
    after_count = utils.count_color_in_range((random_x,random_y), 100, (0,255,0))
    if after_count > before_count:
        raise Exception("疑似未能被黏贴到空白处")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def kjj_001_65():
    utils.check_and_launch_aoi()
    utils.open_program()
    # 1.【设置】-【硬件设置】-【快捷键设置】-【快捷键设置】-【整板编辑】-手动编辑拼板编号（例如设置Ctrl+P）
    # 2.打开任意拼板job,板--拼板操作--选中某个拼板
    # 3.按Ctrl+P
    # 4.输入编号--点是
    utils.click_by_png(config.BOARD_SPLICING_OPERATION)
    utils.click_color(1, config.COMPONENT_REGION, (220, 20, 60))
    pyautogui.press("F1")
    if not utils.search_symbol(config.OK_COLLECTION):
        raise Exception("手动编辑拼版编号快捷键疑似无效")
    utils.close_aoi()
