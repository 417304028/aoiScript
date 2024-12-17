import datetime
import os
import random
import shutil
from loguru import logger
import psutil
import pyperclip
import utils
import time
import pyautogui
import config

# @utils.screenshot_error_to_excel()
# def tccs_001_01():
#     # 1.打开任一job，【运行】程式
#     # 2.在页面弹出【停止或进入细调】时，在倒计时结束前点击【细调】，进入细调界面
#     # 3.在细调界面，选中目标算法框，在页面右侧更改【算法参数】--【阈值】
#     # 4.更改完参数后点击【返回】
#     # 5.弹窗中点击【出板】
#     # 6.手动将出板口的板拿走
#     # 7.查看该元件及该料号在RV的显示

# @utils.screenshot_error_to_excel()
# def tccs_001_02():
#     # 1.打开任一job，【运行】程式
#     # 2.在页面弹出【停止或进入细调】时，在倒计时结束前点击【细调】，进入细调界面
#     # 3.在细调界面，选中目标算法框，在页面右侧更改【算法参数】--【阈值】
#     # 4.更改完参数后点击【测试当前窗口】
#     # 5.测试完成后点击【返回】
#     # 6.弹窗中点击【出板】
#     # 7.手动将出板口的板拿走
#     # 8.查看该元件及该料号在RV的显示

# @utils.screenshot_error_to_excel()
# def tccs_001_03():
#     # 1.打开任一job，【运行】程式
#     # 2.在页面弹出【停止或进入细调】时，在倒计时结束前点击【细调】，进入细调界面
#     # 3.在细调界面，选中目标算法框，在页面右侧更改【算法参数】--【阈值】
#     # 4.更改完参数后点击【测试当前元件】
#     # 5.测试完成后点击【返回】
#     # 6.弹窗中点击【出板】
#     # 7.手动将出板口的板拿走
#     # 8.查看该元件及该料号在RV的显示

# @utils.screenshot_error_to_excel()
# def tccs_001_04():
#     # 1.打开任一job，【运行】程式
#     # 2.在页面弹出【停止或进入细调】时，在倒计时结束前点击【细调】，进入细调界面
#     # 3.在细调界面，选中目标算法框，在页面右侧更改【算法参数】--【阈值】
#     # 4.更改完参数后点击【测试当前分组】
#     # 5.测试完成后点击【返回】
#     # 6.弹窗中点击【出板】
#     # 7.手动将出板口的板拿走
#     # 8.查看该元件及该料号在RV的显示

# @utils.screenshot_error_to_excel()
# def tccs_001_05():
#     # 1.打开任一job，【运行】程式
#     # 2.在页面弹出【停止或进入细调】时，在倒计时结束前点击【细调】，进入细调界面
#     # 3.在细调界面，选中目标算法框，在页面右侧更改【算法参数】--【阈值】
#     # 4.更改完参数后点击【测试当前整版】
#     # 5.测试完成后点击【返回】
#     # 6.弹窗中点击【出板】
#     # 7.手动将出板口的板拿走
#     # 8.查看该元件及该料号在RV的显示

# @utils.screenshot_error_to_excel()
# def tccs_002_01():
#     # 1.打开任一job，【运行】程式
#     # 2.在页面弹出【停止或进入细调】时，在倒计时结束前点击【细调】，进入细调界面
#     # 3.在细调界面，选中目标算法框，在页面右侧更改【算法参数】--【阈值】
#     # 4.更改完参数后点击【返回】
#     # 5.弹窗中点击【出板】
#     # 6.手动将出板口的板拿走
#     # 7.查看该元件及该料号在RV的显示

# @utils.screenshot_error_to_excel()
# def tccs_002_02():
#     # 1.打开任一job，【运行】程式
#     # 2.在页面弹出【停止或进入细调】时，在倒计时结束前点击【细调】，进入细调界面
#     # 3.在细调界面，选中目标算法框，在页面右侧更改【算法参数】--【阈值】
#     # 4.更改完参数后点击【测试当前窗口】
#     # 5.测试完成后点击【返回】
#     # 6.弹窗中点击【出板】
#     # 7.手动将出板口的板拿走
#     # 8.查看该元件及该料号在RV的显示

# @utils.screenshot_error_to_excel()
# def tccs_002_03():
#     # 1.打开任一job，【运行】程式
#     # 2.在页面弹出【停止或进入细调】时，在倒计时结束前点击【细调】，进入细调界面
#     # 3.在细调界面，选中目标算法框，在页面右侧更改【算法参数】--【阈值】
#     # 4.更改完参数后点击【测试当前元件】
#     # 5.测试完成后点击【返回】
#     # 6.弹窗中点击【出板】
#     # 7.手动将出板口的板拿走
#     # 8.查看该元件及该料号在RV的显示

# @utils.screenshot_error_to_excel()
# def tccs_002_04():
#     # 1.打开任一job，【运行】程式
#     # 2.在页面弹出【停止或进入细调】时，在倒计时结束前点击【细调】，进入细调界面
#     # 3.在细调界面，选中目标算法框，在页面右侧更改【算法参数】--【阈值】
#     # 4.更改完参数后点击【测试当前分组】
#     # 5.测试完成后点击【返回】
#     # 6.弹窗中点击【出板】
#     # 7.手动将出板口的板拿走
#     # 8.查看该元件及该料号在RV的显示

# @utils.screenshot_error_to_excel()
# def tccs_002_05():
#     # 1.打开任一job，【运行】程式
#     # 2.在页面弹出【停止或进入细调】时，在倒计时结束前点击【细调】，进入细调界面
#     # 3.在细调界面，选中目标算法框，在页面右侧更改【算法参数】--【阈值】
#     # 4.更改完参数后点击【测试当前整版】
#     # 5.测试完成后点击【返回】
#     # 6.弹窗中点击【出板】
#     # 7.手动将出板口的板拿走
#     # 8.查看该元件及该料号在RV的显示

# @utils.screenshot_error_to_excel()
# def tccs_003_01():
#     # 前提条件2、3交给人工
#     # 1.打开任一job，【运行】程式
#     # 2.在页面弹出【停止或进入细调】时，在倒计时结束前点击【细调】，进入细调界面
#     # 3.在细调界面，选中目标算法框，在页面右侧更改【算法参数】--【阈值】
#     # 4.更改完参数后点击【返回】
#     # 5.弹窗中点击【出板】
#     # 6.查看该元件及该料号在RV的显示

# @utils.screenshot_error_to_excel()
# def tccs_003_02():
#     # 1.打开任一job，【运行】程式
#     # 2.在页面弹出【停止或进入细调】时，在倒计时结束前点击【细调】，进入细调界面
#     # 3.在细调界面，选中目标算法框，在页面右侧更改【算法参数】--【阈值】
#     # 4.更改完参数后点击【测试当前窗口】
#     # 5.测试完成后点击【返回】
#     # 6.弹窗中点击【出板】
#     # 7.查看该元件及该料号在RV的显示

# @utils.screenshot_error_to_excel()
# def tccs_003_03():
#     # 1.打开任一job，【运行】程式
#     # 2.在页面弹出【停止或进入细调】时，在倒计时结束前点击【细调】，进入细调界面
#     # 3.在细调界面，选中目标算法框，在页面右侧更改【算法参数】--【阈值】
#     # 4.更改完参数后点击【测试当前元件】
#     # 5.测试完成后点击【返回】
#     # 6.弹窗中点击【出板】
#     # 7.查看该元件及该料号在RV的显示

# @utils.screenshot_error_to_excel()
# def tccs_003_04():
#     # 1.打开任一job，【运行】程式
#     # 2.在页面弹出【停止或进入细调】时，在倒计时结束前点击【细调】，进入细调界面
#     # 3.在细调界面，选中目标算法框，在页面右侧更改【算法参数】--【阈值】
#     # 4.更改完参数后点击【测试当前分组】
#     # 5.测试完成后点击【返回】
#     # 6.弹窗中点击【出板】
#     # 7.查看该元件及该料号在RV的显示

# @utils.screenshot_error_to_excel()
# def tccs_003_05():
#     # 1.打开任一job，【运行】程式
#     # 2.在页面弹出【停止或进入细调】时，在倒计时结束前点击【细调】，进入细调界面
#     # 3.在细调界面，选中目标算法框，在页面右侧更改【算法参数】--【阈值】
#     # 4.更改完参数后点击【测试当前整版】
#     # 5.测试完成后点击【返回】
#     # 6.弹窗中点击【出板】
#     # 7.查看该元件及该料号在RV的显示

# @utils.screenshot_error_to_excel()
# def tccs_004_01():
#     # 1.打开任一job，【运行】程式
#     # 2.在页面弹出【停止或进入细调】时，在倒计时结束前点击【细调】，进入细调界面
#     # 3.在细调界面，选中目标算法框，在页面右侧更改【算法参数】--【阈值】
#     # 4.更改完参数后点击【返回】
#     # 5.弹窗中点击【出板】
#     # 6.查看该元件及该料号在RV的显示

# @utils.screenshot_error_to_excel()
# def tccs_004_02():
#     # 1.打开任一job，【运行】程式
#     # 2.在页面弹出【停止或进入细调】时，在倒计时结束前点击【细调】，进入细调界面
#     # 3.在细调界面，选中目标算法框，在页面右侧更改【算法参数】--【阈值】
#     # 4.更改完参数后点击【测试当前窗口】
#     # 5.测试完成后点击【返回】
#     # 6.弹窗中点击【出板】
#     # 7.查看该元件及该料号在RV的显示

# @utils.screenshot_error_to_excel()
# def tccs_004_03():
#     # 1.打开任一job，【运行】程式
#     # 2.在页面弹出【停止或进入细调】时，在倒计时结束前点击【细调】，进入细调界面
#     # 3.在细调界面，选中目标算法框，在页面右侧更改【算法参数】--【阈值】
#     # 4.更改完参数后点击【测试当前元件】
#     # 5.测试完成后点击【返回】
#     # 6.弹窗中点击【出板】
#     # 7.查看该元件及该料号在RV的显示

# @utils.screenshot_error_to_excel()
# def tccs_004_04():
#     # 1.打开任一job，【运行】程式
#     # 2.在页面弹出【停止或进入细调】时，在倒计时结束前点击【细调】，进入细调界面
#     # 3.在细调界面，选中目标算法框，在页面右侧更改【算法参数】--【阈值】
#     # 4.更改完参数后点击【测试当前分组】
#     # 5.测试完成后点击【返回】
#     # 6.弹窗中点击【出板】
#     # 7.查看该元件及该料号在RV的显示

# @utils.screenshot_error_to_excel()
# def tccs_004_05():
#     # 1.打开任一job，【运行】程式
#     # 2.在页面弹出【停止或进入细调】时，在倒计时结束前点击【细调】，进入细调界面
#     # 3.在细调界面，选中目标算法框，在页面右侧更改【算法参数】--【阈值】
#     # 4.更改完参数后点击【测试当前整版】
#     # 5.测试完成后点击【返回】
#     # 6.弹窗中点击【出板】
#     # 7.查看该元件及该料号在RV的显示

# @utils.screenshot_error_to_excel()
# def tccs_005_01():
#     # 1.打开任一job，【运行】程式
#     # 2.在页面弹出【停止或进入细调】时，在倒计时结束前点击【细调】，进入细调界面
#     # 3.在细调界面，选中目标算法框，在页面右侧更改【算法参数】--【阈值】
#     # 4.更改完参数后点击【返回】
#     # 5.弹窗中点击【出板】
#     # 6.查看该元件及该料号在RV的显示

# @utils.screenshot_error_to_excel()
# def tccs_005_02():
#     # 1.打开任一job，【运行】程式
#     # 2.在页面弹出【停止或进入细调】时，在倒计时结束前点击【细调】，进入细调界面
#     # 3.在细调界面，选中目标算法框，在页面右侧更改【算法参数】--【阈值】
#     # 4.更改完参数后点击【测试当前窗口】
#     # 5.测试完成后点击【返回】
#     # 6.弹窗中点击【出板】
#     # 7.查看该元件及该料号在RV的显示

# @utils.screenshot_error_to_excel()
# def tccs_005_03():
#     # 1.打开任一job，【运行】程式
#     # 2.在页面弹出【停止或进入细调】时，在倒计时结束前点击【细调】，进入细调界面
#     # 3.在细调界面，选中目标算法框，在页面右侧更改【算法参数】--【阈值】
#     # 4.更改完参数后点击【测试当前元件】
#     # 5.测试完成后点击【返回】
#     # 6.弹窗中点击【出板】
#     # 7.查看该元件及该料号在RV的显示

# @utils.screenshot_error_to_excel()
# def tccs_005_04():
#     # 1.打开任一job，【运行】程式
#     # 2.在页面弹出【停止或进入细调】时，在倒计时结束前点击【细调】，进入细调界面
#     # 3.在细调界面，选中目标算法框，在页面右侧更改【算法参数】--【阈值】
#     # 4.更改完参数后点击【测试当前分组】
#     # 5.测试完成后点击【返回】
#     # 6.弹窗中点击【出板】
#     # 7.查看该元件及该料号在RV的显示

# @utils.screenshot_error_to_excel()
# def tccs_005_05():
#     # 1.打开任一job，【运行】程式
#     # 2.在页面弹出【停止或进入细调】时，在倒计时结束前点击【细调】，进入细调界面
#     # 3.在细调界面，选中目标算法框，在页面右侧更改【算法参数】--【阈值】
#     # 4.更改完参数后点击【测试当前整版】
#     # 5.测试完成后点击【返回】
#     # 6.弹窗中点击【出板】
#     # 7.查看该元件及该料号在RV的显示

# @utils.screenshot_error_to_excel()
# def tccs_006_01():
#     # 1.打开任一job，【运行】程式
#     # 2.在页面弹出【停止或进入细调】时，在倒计时结束前点击【细调】，进入细调界面
#     # 3.在细调界面，选中目标算法框，在页面右侧更改【算法参数】--【阈值】
#     # 4.更改完参数后点击【返回】
#     # 5.弹窗中点击【出板】
#     # 6.查看该元件及该料号在RV的显示

# @utils.screenshot_error_to_excel()
# def tccs_006_02():
#     # 1.打开任一job，【运行】程式
#     # 2.在页面弹出【停止或进入细调】时，在倒计时结束前点击【细调】，进入细调界面
#     # 3.在细调界面，选中目标算法框，在页面右侧更改【算法参数】--【阈值】
#     # 4.更改完参数后点击【测试当前窗口】
#     # 5.测试完成后点击【返回】
#     # 6.弹窗中点击【出板】
#     # 7.查看该元件及该料号在RV的显示

# @utils.screenshot_error_to_excel()
# def tccs_006_03():
#     # 1.打开任一job，【运行】程式
#     # 2.在页面弹出【停止或进入细调】时，在倒计时结束前点击【细调】，进入细调界面
#     # 3.在细调界面，选中目标算法框，在页面右侧更改【算法参数】--【阈值】
#     # 4.更改完参数后点击【测试当前元件】
#     # 5.测试完成后点击【返回】
#     # 6.弹窗中点击【出板】
#     # 7.查看该元件及该料号在RV的显示

# @utils.screenshot_error_to_excel()
# def tccs_006_04():
#     # 1.打开任一job，【运行】程式
#     # 2.在页面弹出【停止或进入细调】时，在倒计时结束前点击【细调】，进入细调界面
#     # 3.在细调界面，选中目标算法框，在页面右侧更改【算法参数】--【阈值】
#     # 4.更改完参数后点击【测试当前分组】
#     # 5.测试完成后点击【返回】
#     # 6.弹窗中点击【出板】
#     # 7.查看该元件及该料号在RV的显示

# @utils.screenshot_error_to_excel()
# def tccs_006_05():
#     # 1.打开任一job，【运行】程式
#     # 2.在页面弹出【停止或进入细调】时，在倒计时结束前点击【细调】，进入细调界面
#     # 3.在细调界面，选中目标算法框，在页面右侧更改【算法参数】--【阈值】
#     # 4.更改完参数后点击【测试当前整版】
#     # 5.测试完成后点击【返回】
#     # 6.弹窗中点击【出板】
#     # 7.查看该元件及该料号在RV的显示

@utils.screenshot_error_to_excel()
def tccs_007_01():
    utils.check_and_launch_aoi()
    # 1.打开任一job，【运行】程式
    utils.open_program()
    utils.click_by_png(config.PLAY)
    time.sleep(5)
    utils.caton_or_flashback("AOI.exe")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def tccs_007_02():
    utils.check_and_launch_aoi()
    # 1.打开任一job
    utils.ensure_in_edit_mode()
    # 2.检测一个有字符检测的元件，且字符检测只有一个待料
    utils.find_component_window(config.ALG_OCV, image = config.WAIT_MATERIAL_EMPTY)
    # 3.【运行】程式
    utils.click_by_png(config.PLAY)
    for _ in range (2):
        if utils.search_symbol(config.QUESTION_MARK):
            pyautogui.press("enter")
    time.sleep(3)
    for _ in range (2):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(2)
    time.sleep(5)
    utils.caton_or_flashback("AOI.exe")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def tccs_007_03():
    utils.check_and_launch_aoi()
    utils.check_close_all_algs(False)
    # 1.打开任一job
    utils.ensure_in_edit_mode()
    # 2.检测一个有字符检测的元件，且字符检测只有一个待料
    utils.find_component_window(config.ALG_OCV,image=config.WAIT_MATERIAL_EMPTY)
    # 3.选择OCV窗口，切换到“显示过滤图像”，点二值化（0至255）
    utils.click_by_png(config.DISPLAY_FILTERED_IMAGE)
    utils.is_checked((638,955),(650,967),True)
    time.sleep(3)
    # 3.添加待料（要自动识别到有字符即可），点确认添加待料
    utils.click_by_png(config.ADD_STANDARD_IMAGE)
    utils.search_symbol_erroring(config.IMAGE_PROCESS_TOPIC)
    random_coordinate = random.choice(config.LIGHT_VIEWS_POINTS)
    pyautogui.click(random_coordinate)
    utils.click_by_png(config.YES)
    if not utils.check_color_in_region((248,0,0),config.OCR_RESULT_REGION):
        raise Exception("ocv未识别到字符")
    utils.click_by_png(config.APPLY)
    time.sleep(3)
    utils.caton_or_flashback("AOI.exe")
    utils.close_aoi()
    

@utils.screenshot_error_to_excel()
def tccs_008_01():
    utils.check_and_launch_aoi()
    utils.check_close_all_algs(False)
    # 1.打开任一job
    utils.open_program()
    # 2.选择已有的可添加代料的算法，点击【+】--选择光源--【确定】添加代料
    utils.find_component_window((config.CW_BODY_CHECK, config.CW_IMAGE_MATCHING))
    utils.click_by_png(config.ADD_STANDARD_IMAGE)
    utils.search_symbol_erroring(config.IMAGE_PROCESS_TOPIC)
    used_coordinates = set()
    random_coordinate = random.choice(config.LIGHT_VIEWS_POINTS)
    used_coordinates.add(random_coordinate)
    pyautogui.click(random_coordinate)
    utils.click_by_png(config.YES)
    if not utils.check_color_in_region((248,0,0),config.OCR_RESULT_REGION):
        raise Exception("ocv未识别到字符")
    utils.click_by_png(config.APPLY)
    time.sleep(5)
    # 3.重复操作2，添加不同光源的代料
    utils.click_by_png(config.ADD_STANDARD_IMAGE)
    utils.search_symbol_erroring(config.IMAGE_PROCESS_TOPIC)
    remaining_coordinates = list(set(config.LIGHT_VIEWS_POINTS) - used_coordinates)
    random_coordinate = random.choice(remaining_coordinates)
    pyautogui.click(random_coordinate)
    utils.click_by_png(config.YES)
    if not utils.check_color_in_region((248,0,0),config.OCR_RESULT_REGION):
        raise Exception("ocv未识别到字符")
    utils.click_by_png(config.APPLY)
    time.sleep(5)
    utils.caton_or_flashback("AOI.exe")
    utils.close_aoi()


@utils.screenshot_error_to_excel()
def tccs_008_02():
    utils.check_and_launch_aoi()
    utils.check_close_all_algs(False)
    # 1.打开任一job
    utils.ensure_in_edit_mode()
    # 2.选择字符检测，点击【+】--选择光源--【确定】添加代料
    utils.find_component_window(config.ALG_OCV)
    utils.click_by_png(config.ADD_STANDARD_IMAGE)
    utils.search_symbol_erroring(config.IMAGE_PROCESS_TOPIC)
    used_coordinates = set()
    random_coordinate = random.choice(config.LIGHT_VIEWS_POINTS)
    used_coordinates.add(random_coordinate)
    pyautogui.click(random_coordinate)
    utils.click_by_png(config.YES)
    if not utils.check_color_in_region((248,0,0),config.OCR_RESULT_REGION):
        raise Exception("ocv未识别到字符")
    utils.click_by_png(config.APPLY)
    time.sleep(5)
    # 3.重复操作2，添加不同光源的代料
    utils.click_by_png(config.ADD_STANDARD_IMAGE)
    utils.search_symbol_erroring(config.IMAGE_PROCESS_TOPIC)
    remaining_coordinates = list(set(config.LIGHT_VIEWS_POINTS) - used_coordinates)
    random_coordinate = random.choice(remaining_coordinates)
    pyautogui.click(random_coordinate)
    utils.click_by_png(config.YES)
    if not utils.check_color_in_region((248,0,0),config.OCR_RESULT_REGION):
        raise Exception("ocv未识别到字符")
    utils.click_by_png(config.APPLY)
    time.sleep(5)
    utils.caton_or_flashback("AOI.exe")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def tccs_008_03():
    utils.check_and_launch_aoi()
    utils.check_close_all_algs(False)
    # 1.打开任一job
    utils.ensure_in_edit_mode()
    # 2.检测一个有字符检测的元件，且字符检测只有一个待料
    utils.find_component_window(config.ALG_OCV,image=config.WAIT_MATERIAL_EMPTY)
    # 3.选择OCV窗口，切换到“显示过滤图像”，点二值化（0至255）
    utils.click_by_png(config.DISPLAY_FILTERED_IMAGE)
    utils.is_checked((638,955),(650,967),True)
    time.sleep(3)
    # 3.添加待料（要自动识别到有字符即可），点确认添加待料
    utils.click_by_png(config.ADD_STANDARD_IMAGE)
    utils.search_symbol_erroring(config.IMAGE_PROCESS_TOPIC)
    random_coordinate = random.choice(config.LIGHT_VIEWS_POINTS)
    pyautogui.click(random_coordinate)
    utils.click_by_png(config.YES)
    if not utils.check_color_in_region((248,0,0),config.OCR_RESULT_REGION):
        raise Exception("ocv未识别到字符")
    utils.click_by_png(config.APPLY)
    time.sleep(5)
    # 4.【运行】程式
    utils.click_by_png(config.PLAY)
    for _ in range (2):
        if utils.search_symbol(config.QUESTION_MARK):
            pyautogui.press("enter")
    time.sleep(3)
    for _ in range (2):
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(2)
    time.sleep(5)
    utils.caton_or_flashback("AOI.exe")
    utils.close_aoi()


@utils.screenshot_error_to_excel()
def tccs_008_04():
    utils.check_and_launch_aoi()
    utils.check_close_all_algs(False)
    utils.check_output_data_delay(0)
    # 1.打开任一job，【运行】程式
    utils.open_program()
    utils.click_by_png(config.PROGRAM_COMPONENT_DARK)
    utils.is_checked((66,255),(78,267),True)
    utils.click_by_png(config.PLAY, 2)
    for _ in range (3):
        time.sleep(5)
        pyautogui.press("enter")
        time.sleep(5)
    # 2.在页面计算进度条达到100%后，点击【停止】--【进入细调界面】
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,60,tolerance=0.75)
    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
        
    utils.click_by_png(config.STOP)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_STOP,tolerance=0.75)
    utils.click_by_png(config.TESTING_INTERFACE_ENTER_DETAIL_INTERFACE)
    time.sleep(5)
    # 3.选择已有的可添加代料的算法，点击【+】--选择光源--【确定】添加代料
    utils.find_component_window((config.CW_BODY_CHECK, config.CW_IMAGE_MATCHING))
    utils.click_by_png(config.ADD_STANDARD_IMAGE)
    utils.search_symbol_erroring(config.IMAGE_PROCESS_TOPIC)
    used_coordinates = set()
    random_coordinate = random.choice(config.LIGHT_VIEWS_POINTS)
    used_coordinates.add(random_coordinate)
    pyautogui.click(random_coordinate)
    utils.click_by_png(config.YES)
    if not utils.check_color_in_region((248,0,0),config.OCR_RESULT_REGION):
        raise Exception("ocv未识别到字符")
    utils.click_by_png(config.APPLY)
    time.sleep(5)
    # 4.重复操作3，添加不同光源的代料
    utils.click_by_png(config.ADD_STANDARD_IMAGE)
    utils.search_symbol_erroring(config.IMAGE_PROCESS_TOPIC)
    remaining_coordinates = list(set(config.LIGHT_VIEWS_POINTS) - used_coordinates)
    random_coordinate = random.choice(remaining_coordinates)
    pyautogui.click(random_coordinate)
    utils.click_by_png(config.YES)
    if not utils.check_color_in_region((248,0,0),config.OCR_RESULT_REGION):
        raise Exception("ocv未识别到字符")
    utils.click_by_png(config.APPLY)
    time.sleep(5)
    utils.caton_or_flashback("AOI.exe")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def tccs_008_05():
    utils.check_and_launch_aoi()
    utils.check_close_all_algs(False)
    utils.check_output_data_delay(0)
    # 1.打开任一job，【运行】程式
    utils.open_program()
    utils.click_by_png(config.PROGRAM_COMPONENT_DARK)
    utils.is_checked((66,255),(78,267),True)
    utils.click_by_png(config.PLAY, 2)
    for _ in range (3):
        time.sleep(5)
        pyautogui.press("enter")
        time.sleep(5)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,60,tolerance=0.75)
    # 2.在页面计算进度条达到100%后，点击【停止】--【进入细调界面】
    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")

    utils.click_by_png(config.STOP)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_STOP,tolerance=0.75)
    utils.click_by_png(config.TESTING_INTERFACE_ENTER_DETAIL_INTERFACE)
    time.sleep(5)
    # 3.选择字符检测，点击【+】--选择光源--【确定】添加代料
    utils.find_component_window(config.ALG_OCV)
    utils.click_by_png(config.ADD_STANDARD_IMAGE)
    utils.search_symbol_erroring(config.IMAGE_PROCESS_TOPIC)
    used_coordinates = set()
    random_coordinate = random.choice(config.LIGHT_VIEWS_POINTS)
    used_coordinates.add(random_coordinate)
    pyautogui.click(random_coordinate)
    utils.click_by_png(config.YES)
    if not utils.check_color_in_region((248,0,0),config.OCR_RESULT_REGION):
        raise Exception("ocv未识别到字符")
    utils.click_by_png(config.APPLY)
    time.sleep(5)
    # 4.重复操作3，添加不同光源的代料
    utils.click_by_png(config.ADD_STANDARD_IMAGE)
    utils.search_symbol_erroring(config.IMAGE_PROCESS_TOPIC)
    remaining_coordinates = list(set(config.LIGHT_VIEWS_POINTS) - used_coordinates)
    random_coordinate = random.choice(remaining_coordinates)
    pyautogui.click(random_coordinate)
    utils.click_by_png(config.YES)
    if not utils.check_color_in_region((248,0,0),config.OCR_RESULT_REGION):
        raise Exception("ocv未识别到字符")
    utils.click_by_png(config.APPLY)
    time.sleep(5)
    utils.caton_or_flashback("AOI.exe")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def tccs_008_06():
    utils.check_and_launch_aoi()
    utils.check_close_all_algs(False)
    utils.check_output_data_delay(0)
    # 1.打开任一job，【运行】程式
    utils.open_program()
    utils.click_by_png(config.PROGRAM_COMPONENT_DARK)
    utils.is_checked((66,255),(78,267),True)
    utils.click_by_png(config.PLAY, 2)
    for _ in range (3):
        time.sleep(5)
        pyautogui.press("enter")
        time.sleep(5)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,60,tolerance=0.75)
    # 2.在页面计算进度条达到100%后，点击【停止】--【进入细调界面】
    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    utils.click_by_png(config.STOP)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_STOP,tolerance=0.75)
    utils.click_by_png(config.TESTING_INTERFACE_ENTER_DETAIL_INTERFACE)
    time.sleep(5)
    # 3.选择OCV窗口，切换到“显示过滤图像”，点二值化（0至255）
    utils.click_by_png(config.DISPLAY_FILTERED_IMAGE)
    utils.is_checked((638,955),(650,967),True)
    time.sleep(3)
    # 4.选择字符检测，点击【+】--选择光源--【确定】添加代料
    utils.find_component_window(config.ALG_OCV)
    utils.click_by_png(config.ADD_STANDARD_IMAGE)
    utils.search_symbol_erroring(config.IMAGE_PROCESS_TOPIC)
    used_coordinates = set()
    random_coordinate = random.choice(config.LIGHT_VIEWS_POINTS)
    used_coordinates.add(random_coordinate)
    pyautogui.click(random_coordinate)
    utils.click_by_png(config.YES)
    if not utils.check_color_in_region((248,0,0),config.OCR_RESULT_REGION):
        raise Exception("ocv未识别到字符")
    utils.click_by_png(config.APPLY)
    time.sleep(5)
    # 5.重复操作4，添加不同光源的代料
    utils.click_by_png(config.ADD_STANDARD_IMAGE)
    utils.search_symbol_erroring(config.IMAGE_PROCESS_TOPIC)
    remaining_coordinates = list(set(config.LIGHT_VIEWS_POINTS) - used_coordinates)
    random_coordinate = random.choice(remaining_coordinates)
    pyautogui.click(random_coordinate)
    utils.click_by_png(config.YES)
    if not utils.check_color_in_region((248,0,0),config.OCR_RESULT_REGION):
        raise Exception("ocv未识别到字符")
    utils.click_by_png(config.APPLY)
    time.sleep(5)
    utils.caton_or_flashback("AOI.exe")
    utils.close_aoi()

# TODO 难度太大
# @utils.screenshot_error_to_excel()
# def tccs_009_01():
#     utils.check_and_launch_aoi()
#     utils.check_patent_not_NG(3)
#     # 1.打开任一job
#     utils.ensure_in_edit_mode()
#     # 2.选中已关联父框，全选后移偏
#     pyautogui.hotkey("ctrl","a")
#     pyautogui.press("delete")
#     if utils.search_symbol(config.QUESTION_MARK):
#         pyautogui.press("enter")

#     for action in [config.SQUARE_POSITIONING, config.COLOR_AREA]:
#         utils.add_window()
#         utils.click_by_png(action)
#         utils.click_by_png(config.YES)
#         time.sleep(7)
#     pyautogui.hotkey("ctrl","a")
#     utils.click_by_png(config.RELATE_WINDOW)
#     pyautogui.hotkey("ctrl","tab")
#     time.sleep(3)
#     frame_center = utils.get_frame_center((0,0,255))
#     # 按住frame_center 往任意方向拖动50-100距离
#     pyautogui.mouseDown(frame_center)
#     time.sleep(0.5)
#     move_x = random.randint(50, 100) * random.choice([-1, 1])
#     move_y = random.randint(50, 100) * random.choice([-1, 1])
#     pyautogui.moveRel(move_x, move_y, duration=1)
#     time.sleep(0.5)
#     pyautogui.mouseUp()

#     # 3.点击【测试当前元件】
#     utils.click_by_png(config.TEST_COMPONENT)
#     if utils.search_symbol(config.QUESTION_MARK):
#         pyautogui.press("enter")
#     while utils.search_symbol(config.TESTING_COMPONENT):
#         time.sleep(1)

#     # 子框随父框移动,切在移动后的位置进行计算
#     utils.get_color_in_region




    # utils.close_aoi()

# # TODO
# @utils.screenshot_error_to_excel()
# def tccs_009_02():
#     utils.check_and_launch_aoi()
#     utils.check_patent_not_NG(3)
#     # 1.打开任一job，【运行】程式
#     utils.open_program()
#     utils.click_by_png(config.PROGRAM_COMPONENT_DARK)
#     utils.is_checked((66,255),(78,267),True)
#     utils.click_by_png(config.PLAY, 2)
#     for _ in range (3):
#         time.sleep(5)
#         pyautogui.press("enter")
#         time.sleep(5)
#     utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,60,tolerance=0.75)
#     # 2.选中已关联父框，全选后移偏
#     pyautogui.hotkey("ctrl","a")







#     # 方形定位和颜色面积
#     # 3.在页面计算进度条达到100%后，点击【停止】--【进入细调界面】
#     if not utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 300, tolerance=0.75):
#         raise Exception("循环单次时疑似超过五分钟")
#     utils.click_by_png(config.STOP)
#     utils.search_symbol_erroring(config.TESTING_INTERFACE_STOP,tolerance=0.75)
#     utils.click_by_png(config.TESTING_INTERFACE_ENTER_DETAIL_INTERFACE)
#     time.sleep(5)
#     # 4.查看移偏元件

# @utils.screenshot_error_to_excel()
# def tccs_0010_01():
#     # 1.打开任一job，【运行】程式
#     # 2.在页面弹出【停止或进入细调】时，在倒计时结束前点击【细调】，进入细调界面
#     # 3.在细调界面，选中目标算法框，在页面右侧更改【算法参数】--【阈值】，使不良元件都调试成良好元件
#     # 4.测试完成后点击【返回】
#     # 5.弹窗中点击【出板】
#     # 6.在ngbuffer看收到的信号

# @utils.screenshot_error_to_excel()
# def tccs_0010_02():
#     # 1.打开任一job，【运行】程式
#     # 2.在页面弹出【停止或进入细调】时，在倒计时结束前点击【细调】，进入细调界面
#     # 3.看继电器亮灯
#     # 4.在细调界面，选中目标算法框，在页面右侧更改【算法参数】--【阈值】，使不良元件都调试成良好元件
#     # 5.测试完成后UI点击【返回】
#     # 6.RV复判后，看继电器亮灯

# @utils.screenshot_error_to_excel()
# def tccs_0010_03():
#     # 1.打开任一job，【运行】程式
#     # 2.在页面弹出【停止或进入细调】时，在倒计时结束前点击【细调】，进入细调界面
#     # 3.在细调界面，选中目标算法框，在页面右侧更改【算法参数】--【阈值】，使不良元件都调试成良好元件
#     # 4.测试完成后点击【返回】
#     # 5.弹窗中点击【出板】
#     # 6.在ngbuffer看收到的信号

# @utils.screenshot_error_to_excel()
# def tccs_0011_01():
#     # 1.打开任一job，【运行】程式
#     # 2.在页面弹出【停止或进入细调】时，在倒计时结束前点击【细调】，进入细调界面
#     # 3.在细调界面，选中目标算法框，在页面右侧更改【算法参数】--【阈值】，使不良元件都调试成良好元件
#     # 4.测试完成后点击【返回】
#     # 5.弹窗中点击【出板】
#     # 6.在中间层看收到的信号

# @utils.screenshot_error_to_excel()
# def tccs_0011_02():
#     # 1.打开任一job，【运行】程式
#     # 2.在页面弹出【停止或进入细调】时，在倒计时结束前点击【细调】，进入细调界面
#     # 3.看继电器亮灯
#     # 4.在细调界面，选中目标算法框，在页面右侧更改【算法参数】--【阈值】，使不良元件都调试成良好元件
#     # 5.测试完成后UI点击【返回】
#     # 6.RV复判后，看继电器亮灯

@utils.screenshot_error_to_excel()
def tccs_012_01():
    utils.check_and_launch_aoi()
    # 1.打开任一job，【运行】程式
    utils.open_program()
    utils.click_by_png(config.PROGRAM_COMPONENT_DARK)
    utils.is_checked((66,255),(78,267),True)
    utils.click_by_png(config.PLAY, 2)
    for _ in range (3):
        time.sleep(5)
        pyautogui.press("enter")
        time.sleep(5)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,60,tolerance=0.75)
    # 2.在页面计算进度条达到100%后，点击【停止】--【进入细调界面】
    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    utils.click_by_png(config.STOP)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_STOP,tolerance=0.75)
    utils.click_by_png(config.TESTING_INTERFACE_ENTER_DETAIL_INTERFACE)
    time.sleep(5)
    # 3.任意选择一个有算法的元件移动算法框
    utils.find_component_window(1)
    before_left_point = utils.get_color_direction_coordinate((255,255,255),config.COMPONENT_OPERATION_REGION,"left")
    before_up_point = utils.get_color_direction_coordinate((255,255,255),config.COMPONENT_OPERATION_REGION,"up")
    pyautogui.click(config.CENTRE)
    time.sleep(3)
    pyautogui.drag(-50, -50, duration=1)
    after_left_point = utils.get_color_direction_coordinate((255,255,255),config.COMPONENT_OPERATION_REGION,"left")
    after_up_point = utils.get_color_direction_coordinate((255,255,255),config.COMPONENT_OPERATION_REGION,"up")
    if after_left_point >= before_left_point and after_up_point >= before_up_point:
        raise Exception("算法框未成功左移或上移")
    utils.close_aoi()

    

@utils.screenshot_error_to_excel()
def tccs_012_02():
    utils.check_and_launch_aoi()
    # 1.打开任意job,运行程式
    utils.open_program()
    # 2.计算完成后，停止进入细调，在超出此元件roi的范围外添加一个检测框 TODO
    utils.click_by_png(config.PROGRAM_COMPONENT_DARK)
    utils.is_checked((66,255),(78,267),True)
    utils.click_by_png(config.PLAY, 2)
    for _ in range (3):
        time.sleep(5)
        pyautogui.press("enter")
        time.sleep(5)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,60,tolerance=0.75)

    start_time = time.time()
    while True:
        if utils.search_symbol(config.TESTING_INTERFACE_PERCENT_100, 5, tolerance=0.75):
            break
        if time.time() - start_time > 300:
            raise Exception("循环单次时疑似超过五分钟")
    utils.click_by_png(config.STOP)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_STOP,tolerance=0.75)
    utils.click_by_png(config.TESTING_INTERFACE_ENTER_DETAIL_INTERFACE)
    time.sleep(5)

    before_left_point = utils.get_color_direction_coordinate((255,255,255),config.COMPONENT_OPERATION_REGION,"left")
    before_up_point = utils.get_color_direction_coordinate((255,255,255),config.COMPONENT_OPERATION_REGION,"up")

    pyautogui.press("w")
    time.sleep(3)
    pyautogui.moveTo(730, 420)
    pyautogui.mouseDown()
    pyautogui.moveTo(1100, 480, duration=1)
    pyautogui.mouseUp()
    time.sleep(3)

    after_left_point = utils.get_color_direction_coordinate((255,255,255),config.COMPONENT_OPERATION_REGION,"left")
    after_up_point = utils.get_color_direction_coordinate((255,255,255),config.COMPONENT_OPERATION_REGION,"up")
    if after_left_point >= before_left_point and after_up_point >= before_up_point:
        raise Exception("算法框未成功左移或上移")
    utils.close_aoi()

# @utils.screenshot_error_to_excel()
# def tccs_012_03():
#     # 测试表格中的用例【金山文档 | WPS云文档】 细条测试 TODO
#     # https://kdocs.cn/l/cvw8JGzbm95v
    