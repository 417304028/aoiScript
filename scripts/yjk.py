import datetime
import fnmatch
import os
import random
import time

import pyautogui
import pyperclip
from loguru import logger

import config
import utils


# 遍历所有硬件icon的话麻烦死了 让测试自己多跑几次
@utils.screenshot_error_to_excel()
def yjk_001_01():
    # 1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    if not utils.search_symbol(config.ALG_W_, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
    time.sleep(3)
    # 2、点击【菜单栏】--【元件库】--【导出当前料号】
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.EXPORT_CURRENT_PN)
    # 3、弹框 设置默认，点击是。
    utils.search_symbol_erroring(config.TYPE_NAME_DEFAULT)
    utils.search_symbol_erroring(config.ELEMENTS_INFORMATION)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(5)
    # 4、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】，
    utils.click_by_png(config.MANUAL_SELECT)
    utils.click_by_png(config.ELEMENTS_VIEW_REFRESH, region=config.ELEMENTS_VIEW_REGION,tolerance=0.95)
    # 1）下拉框查找所选的元件库
    pyautogui.click((546,232))
    utils.is_checked((375,246),(387,258),True)
    pyautogui.press("enter")
    utils.search_symbol_erroring(config.TYPE_NAME_DEFAULT)
    # 2）点击所选的元件库 扩展 （元件库->芯片类型->封装类型->料号）
    utils.click_by_png(config.BOARD_ENLARGE, region=config.ELEMENTS_VIEW_REGION, tolerance=0.95)
    utils.click_by_png(config.BOARD_HARDWARE_ICON, region = config.ELEMENTS_VIEW_REGION)
    # 3）点击图片
    image_point = (666,333)
    pyautogui.click(image_point)
    time.sleep(0.5)
    # 检测读取到的信息是否在该元件信息里
    component_information = utils.read_text(400,700)
    logger.info(f"元件信息框内容: {component_information}")
    # 4）查看下面信息与导出的料号信息（元件上右键--【元件信息】）对比。
    pyautogui.click(config.CENTRE)
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)
    time.sleep(1)    
    # 芯片类型
    utils.is_checked((1070,174),(1082,186),True)
    chip_type = utils.read_text_ocr((1432,150),(1504,164))
    # 料号
    utils.is_checked((1082,252),(1094,264),True)
    pn_ci = utils.read_text(910,255)
    # 封装类型
    utils.is_checked((1082,274),(1094,286),True)
    package_type = utils.read_text(920,280)
    # cad尺寸
    width = utils.read_text(910,405)
    height = utils.read_text(1040,405)
    # xyh
    comp_x = utils.read_text(940,610)
    comp_y = utils.read_text(1000,610)
    comp_h = utils.read_text(1060,610)

    for info, label in zip([chip_type, package_type, width, height, comp_x, comp_y, comp_h], ["芯片类型", "封装类型", "width", "height", "comp_x", "comp_y", "comp_h"]):
        logger.info(f"检查 {label}: {info}")
        if info is None or info not in component_information:
            logger.error(f"{label} 的信息不一致或缺失: {info}")
            raise Exception(f"{label} 的信息不一致或缺失: {info}")

    # 5、所选的元件库文件夹（元件库路径：【设置】--【数据导出配置】--【元件库设置】--【元件库路径】），查看整板上的料号是否都有导到此元件库此元件库；分类名称、芯片类型、料号、封装类型是否与导出的料号信息对应
    search_pattern = f"{chip_type}@{package_type}@{pn_ci}@@Default@*@{comp_x}@{comp_y}@*.scl"
    logger.debug(f"search_pattern: {search_pattern}")
    try:
        # 遍历元件库路径中的所有文件
        found_files = []
        for file in os.listdir(os.path.join(config.ELEMENTS_LIB_PATH, "default")):
            if fnmatch.fnmatch(file, search_pattern):
                found_files.append(file)
                file_path = os.path.join(config.ELEMENTS_LIB_PATH, "default", file)
                modification_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
                if modification_time not in component_information:
                    raise Exception(f"文件 {file} 的修改时间 {modification_time} 未在 {component_information} 中找到")
        # 检查是否找到匹配的文件
        if not found_files:
            raise Exception("没有找到匹配的.scl文件")
        else:
            logger.info(f"找到匹配的.scl文件: {found_files}")
    except Exception as e:
        raise Exception(f"遍历文件时发生错误: {str(e)}")
    
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def yjk_001_02():
    # 1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    if not utils.search_symbol(config.ALG_W_, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
    time.sleep(3)
    # 2、点击【菜单栏】--【元件库】--【导出当前料号】
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.EXPORT_CURRENT_PN)
    # 3、弹框 设置默认，点击取消。
    utils.search_symbol_erroring(config.TYPE_NAME_DEFAULT)
    utils.search_symbol_erroring(config.ELEMENTS_INFORMATION)
    utils.click_by_png(config.CANCEL)
    # 4、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】和元件库路径，查看是否有导出
    if utils.check_new_data(config.ELEMENTS_LIB_PATH):
        raise Exception("元件被导出了")
    utils.close_aoi()


@utils.screenshot_error_to_excel()
def yjk_001_03():
    utils.check_and_launch_aoi()
    # 1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    if not utils.search_symbol(config.ALG_W_, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
    time.sleep(3)
    # 2、点击【菜单栏】--【元件库】--【导出当前料号】
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.EXPORT_CURRENT_PN)
    # 3、弹框 
    utils.search_symbol_erroring(config.ELEMENTS_INFORMATION)
    # 切换分类名称 没有可切的啊切什么切 识别文字 后续搜的时候用得了
    type_name = utils.read_text(960,470)
    # 修改芯片类型
    pyautogui.click((960,500))
    time.sleep(1)
    if utils.search_symbol(config.TYPE_NAME_C):
        utils.click_by_png(config.TYPE_NAME_C)
    else:
        pyautogui.click((960,500))
    time.sleep(1)
    # 修改封装类型，点击是
    tpt = "test_package_type"
    utils.write_text((955,560),tpt)
    time.sleep(1)
    pyautogui.press("enter")
    # 4、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】
    utils.click_by_png(config.MANUAL_SELECT)
    # 1）下拉框查找切换的元件库
    pyautogui.click((546,232))
    utils.is_checked((375,246),(387,258),False)
    if not utils.drop_down_box_search(1, type_name, region=config.ELEMENTS_VIEW_DROPDOWN_BOX_REGION):
        raise Exception("没有找到切换的元件库")
    # 2）点击所切换的元件库 扩展 （元件库->芯片类型->封装类型->料号）
    utils.click_by_png(config.BOARD_ENLARGE, region=config.ELEMENTS_VIEW_REGION, tolerance=0.95)
    utils.click_by_png(config.BOARD_HARDWARE_ICON, region=config.ELEMENTS_VIEW_REGION)
    # 3）点击图片
    image_point = (666,333)
    pyautogui.click(image_point)
    time.sleep(0.5)
    # 4）查看下面信息与导出的料号信息（元件上右键--【元件信息】）对比。
    component_information = utils.read_text(400,700)

    time.sleep(1)
    pyautogui.click(config.CENTRE)
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)
    time.sleep(1)    # 芯片类型
    utils.is_checked((1070,174),(1082,186),True)
    chip_type = utils.read_text_ocr((1432,150),(1504,164))
    # 封装类型
    utils.is_checked((1082,297),(1094,309),True)
    package_type = utils.read_text(920,300)
    # 料号
    utils.is_checked((1082,275),(1094,287),True)
    pn_ci = utils.read_text(910,280)
    # cad尺寸
    width = utils.read_text(910,405)
    height = utils.read_text(1040,405)
    # xyh
    comp_x = utils.read_text(940,610)
    comp_y = utils.read_text(1000,610)
    comp_h = utils.read_text(1060,610)

    for info, label in zip([chip_type, package_type, width, height, comp_x, comp_y, comp_h], ["芯片类型", "封装类型", "width", "height", "comp_x", "comp_y", "comp_h"]):
        logger.info(f"检查 {label}: {info}")
        if info is None or info not in component_information:
            logger.error(f"{label} 的信息不一致或缺失: {info}")
            raise Exception(f"{label} 的信息不一致或缺失: {info}")

    # 5、所选的元件库文件夹（元件库路径：【设置】--【数据导出配置】--【元件库设置】--【元件库路径】），查看整板上的料号是否都有导到此元件库此元件库；分类名称、芯片类型、料号、封装类型是否与导出的料号信息对应
    search_pattern = f"{chip_type}@{package_type}@{pn_ci}@@Default@*@{comp_x}@{comp_y}@*.scl"
    logger.debug(f"search_pattern: {search_pattern}")
    try:
        # 遍历元件库路径中的所有文件
        found_files = []
        for file in os.listdir(os.path.join(config.ELEMENTS_LIB_PATH, "default")):
            if fnmatch.fnmatch(file, search_pattern):
                found_files.append(file)
                file_path = os.path.join(config.ELEMENTS_LIB_PATH, "default", file)
                modification_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
                if modification_time not in component_information:
                    raise Exception(f"文件 {file} 的修改时间 {modification_time} 未在 {component_information} 中找到")
        # 检查是否找到匹配的文件
        if not found_files:
            raise Exception("没有找到匹配的.scl文件")
        else:
            logger.info(f"找到匹配的.scl文件: {found_files}")
    except Exception as e:
        raise Exception(f"遍历文件时发生错误: {str(e)}")
    
    utils.close_aoi()
@utils.screenshot_error_to_excel()
def yjk_001_04():
    # 1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    if not utils.search_symbol(config.ALG_W_, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
    time.sleep(3)
    # 2、点击【菜单栏】--【元件库】--【导出当前料号】
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.EXPORT_CURRENT_PN)
    # 3、弹框 
    utils.search_symbol_erroring(config.ELEMENTS_INFORMATION)
    # 新增分类名称
    etn = "elements_type_name"
    utils.write_text((960,470),etn)
    time.sleep(1)
    # 修改芯片类型
    pyautogui.click((960,500))
    time.sleep(1)
    if utils.search_symbol(config.TYPE_NAME_C):
        utils.click_by_png(config.TYPE_NAME_C)
    else:
        pyautogui.click((960,500))
    time.sleep(1)
    # 修改封装类型，点击是
    tpt = "test_package_type"
    utils.write_text((955,560),tpt)
    time.sleep(1)
    pyautogui.press("enter")
    # 4、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】
    utils.click_by_png(config.MANUAL_SELECT)
    # 1）下拉框查找新增的元件库
    pyautogui.click((546,232))
    utils.is_checked((375,246),(387,258),False)
    if not utils.drop_down_box_search(0, config.ELEMENTS_TYPE_NAME, region=config.ELEMENTS_VIEW_DROPDOWN_BOX_REGION):
        raise Exception("没有找到新增的元件库")

    # 2）点击所新增的元件库 扩展 （元件库->芯片类型->封装类型->料号）
    utils.click_by_png(config.BOARD_ENLARGE, region=config.ELEMENTS_VIEW_REGION, tolerance=0.95)
    utils.click_by_png(config.BOARD_HARDWARE_ICON, region=config.ELEMENTS_VIEW_REGION)
    # 3）点击图片
    image_point = (666,333)
    pyautogui.click(image_point)
    time.sleep(0.5)
    # 4）查看下面信息与导出的料号信息（元件上右键--【元件信息】）对比。
    component_information = utils.read_text(400,700)
    pyautogui.click(config.CENTRE)
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)
    time.sleep(1)    # 芯片类型
    utils.is_checked((1070,174),(1082,186),True)
    chip_type = utils.read_text_ocr((1432,150),(1504,164))
    # 封装类型
    utils.is_checked((1082,297),(1094,309),True)
    package_type = utils.read_text(920,300)
    # 料号
    utils.is_checked((1082,275),(1094,287),True)
    pn_ci = utils.read_text(910,280)
    # cad尺寸
    width = utils.read_text(910,405)
    height = utils.read_text(1040,405)
    # xyh
    comp_x = utils.read_text(940,610)
    comp_y = utils.read_text(1000,610)
    comp_h = utils.read_text(1060,610)

    for info, label in zip([chip_type, package_type, width, height, comp_x, comp_y, comp_h], ["芯片类型", "封装类型", "width", "height", "comp_x", "comp_y", "comp_h"]):
        logger.info(f"检查 {label}: {info}")
        if info is None or info not in component_information:
            logger.error(f"{label} 的信息不一致或缺失: {info}")
            raise Exception(f"{label} 的信息不一致或缺失: {info}")

    # 5、所选的元件库文件夹（元件库路径：【设置】--【数据导出配置】--【元件库设置】--【元件库路径】），查看整板上的料号是否都有导到此元件库此元件库；分类名称、芯片类型、料号、封装类型是否与导出的料号信息对应
    search_pattern = f"{chip_type}@{package_type}@{pn_ci}@@{etn}@*@{comp_x}@{comp_y}@*.scl"
    logger.debug(f"search_pattern: {search_pattern}")
    try:
        # 遍历元件库路径中的所有文件
        found_files = []
        for file in os.listdir(os.path.join(config.ELEMENTS_LIB_PATH, etn)):
            if fnmatch.fnmatch(file, search_pattern):
                found_files.append(file)
                file_path = os.path.join(config.ELEMENTS_LIB_PATH, etn, file)
                modification_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
                if modification_time not in component_information:
                    raise Exception(f"文件 {file} 的修改时间 {modification_time} 未在 {component_information} 中找到")
        # 检查是否找到匹配的文件
        if not found_files:
            raise Exception("没有找到匹配的.scl文件")
        else:
            logger.info(f"找到匹配的.scl文件: {found_files}")
    except Exception as e:
        raise Exception(f"遍历文件时发生错误: {str(e)}")
        
    utils.close_aoi()
# TODOTODOTODO
@utils.screenshot_error_to_excel()
def yjk_001_05():
    utils.check_and_launch_aoi()
    utils.check_import_sync_package(True)
    # 1、选任一元件，双击进入【编辑界面】
    utils.ensure_in_edit_mode()
    # 3、选有此料号的元件库名称，点击是
    # 4、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】，找到导入的是哪个元件库 哪个料号（点击ABC 标志），元件信息、元件窗口，进行对比
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.MANUAL_SELECT)
    utils.click_by_png(config.ELEMENTS_VIEW_ABC, region=config.ELEMENTS_VIEW_REGION)
    utils.click_by_png(config.BOARD_HARDWARE_ICON, region=config.ELEMENTS_VIEW_REGION)
    image_point = (666,333)
    pyautogui.click(image_point)
    time.sleep(0.5)
    component_information = utils.read_text(400,700)
    pyautogui.click(config.CENTRE)
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)
    time.sleep(1)    # 芯片类型
    utils.is_checked((1070,174),(1082,186),True)
    chip_type = utils.read_text_ocr((1432,150),(1504,164))
    # 封装类型
    utils.is_checked((1082,297),(1094,309),True)
    package_type = utils.read_text(920,300)
    # 料号
    utils.is_checked((1082,275),(1094,287),True)
    pn_ci = utils.read_text(910,280)
    # cad尺寸
    width = utils.read_text(910,405)
    height = utils.read_text(1040,405)
    # xyh
    comp_x = utils.read_text(940,610)
    comp_y = utils.read_text(1000,610)
    comp_h = utils.read_text(1060,610)

    for info, label in zip([chip_type, package_type, width, height, comp_x, comp_y, comp_h], ["芯片类型", "封装类型", "width", "height", "comp_x", "comp_y", "comp_h"]):
        logger.info(f"检查 {label}: {info}")
        if info is None or info not in component_information:
            logger.error(f"{label} 的信息不一致或缺失: {info}")
            raise Exception(f"{label} 的信息不一致或缺失: {info}")

    utils.close_aoi()
@utils.screenshot_error_to_excel()
def yjk_001_06():
    utils.check_and_launch_aoi()
    # 1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
    utils.ensure_in_edit_mode()
    if not utils.search_symbol(config.ALG_W_, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
    time.sleep(3)
    # 2、点击【菜单栏】--【元件库】--【导出当前料号】
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.EXPORT_CURRENT_PN)
    # 3、弹框 设置默认，点击是。
    utils.search_symbol_erroring(config.TYPE_NAME_DEFAULT)
    utils.search_symbol_erroring(config.ELEMENTS_INFORMATION)
    time.sleep(1)
    pn = utils.read_text(960,530)
    pyautogui.press("enter")
    time.sleep(5)
    # 4、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】，
    utils.click_by_png(config.MANUAL_SELECT)
    utils.click_by_png(config.ELEMENTS_VIEW_REFRESH, region=config.ELEMENTS_VIEW_REGION,tolerance=0.95)
    # 1）下拉框查找所选的元件库
    pyautogui.click((546,232))
    utils.is_checked((375,246),(387,258),True)
    pyautogui.press("enter")
    utils.search_symbol_erroring(config.TYPE_NAME_DEFAULT)
    # 2）点击所选的元件库 扩展 （元件库->芯片类型->封装类型->料号）
    utils.click_by_png(config.BOARD_ENLARGE, region=config.ELEMENTS_VIEW_REGION, tolerance=0.95)
    utils.click_by_png(config.BOARD_HARDWARE_ICON, region = config.ELEMENTS_VIEW_REGION)
    # 3）查看整板上的料号是否都有导到此元件库 检测个球啊 只能测个当前料号 
    image_point = (666,333)
    pyautogui.click(image_point)
    time.sleep(0.5)
    component_information = utils.read_text(400,700)
    # 4）查看下面信息与导出的料号信息（元件上右键--【元件信息】）对比。
    # 检测读取到的信息是否在该元件信息里
    pyautogui.click(config.CENTRE)
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)
    time.sleep(1)    
    # 芯片类型
    utils.is_checked((1070,174),(1082,186),True)
    chip_type = utils.read_text_ocr((1432,150),(1504,164))
    # 料号
    utils.is_checked((1082,252),(1094,264),True)
    pn_ci = utils.read_text(910,255)
    # 封装类型
    utils.is_checked((1082,274),(1094,286),True)
    package_type = utils.read_text(920,280)
    # cad尺寸
    width = utils.read_text(910,405)
    height = utils.read_text(1040,405)
    # xyh
    comp_x = utils.read_text(940,610)
    comp_y = utils.read_text(1000,610)
    comp_h = utils.read_text(1060,610)
    
    if pn_ci != pn:
        raise Exception("导出前和导出后料号不一致")

    for info, label in zip([chip_type, package_type, width, height, comp_x, comp_y, comp_h], ["芯片类型", "封装类型", "width", "height", "comp_x", "comp_y", "comp_h"]):
        logger.info(f"检查 {label}: {info}")
        if info is None or info not in component_information:
            logger.error(f"{label} 的信息不一致或缺失: {info}")
            raise Exception(f"{label} 的信息不一致或缺失: {info}")

    # 5、所选的元件库文件夹（元件库路径：【设置】--【数据导出配置】--【元件库设置】--【元件库路径】），查看整板上的料号是否都有导到此元件库此元件库；分类名称、芯片类型、料号、封装类型是否与导出的料号信息对应
    search_pattern = f"{chip_type}@{package_type}@{pn_ci}@@Default@*@{comp_x}@{comp_y}@*.scl"
    logger.debug(f"search_pattern: {search_pattern}")
    try:
        # 遍历元件库路径中的所有文件
        found_files = []
        for file in os.listdir(os.path.join(config.ELEMENTS_LIB_PATH, "default")):
            if fnmatch.fnmatch(file, search_pattern):
                found_files.append(file)
                file_path = os.path.join(config.ELEMENTS_LIB_PATH, "default", file)
                modification_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
                if modification_time not in component_information:
                    raise Exception(f"文件 {file} 的修改时间 {modification_time} 未在 {component_information} 中找到")
        # 检查是否找到匹配的文件
        if not found_files:
            raise Exception("没有找到匹配的.scl文件")
        else:
            logger.info(f"找到匹配的.scl文件: {found_files}")
    except Exception as e:
        raise Exception(f"遍历文件时发生错误: {str(e)}")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def yjk_001_07():
    utils.check_and_launch_aoi()
    # 1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
    utils.ensure_in_edit_mode()
    if not utils.search_symbol(config.ALG_W_, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
    time.sleep(3)
    # 2、点击【菜单栏】--【元件库】--【导出所有】
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.EXPORT_ALL_PN)
    # 3、弹框 设置默认，点击取消。
    utils.search_symbol_erroring(config.TYPE_NAME_DEFAULT)
    utils.search_symbol_erroring(config.IF_EXPORT_ALL_PN)
    utils.click_by_png(config.NO)
    # 4、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】和元件库路径，查看是否有导出
    utils.click_by_png(config.MANUAL_SELECT)
    utils.click_by_png(config.BOARD_ENLARGE, region=config.ELEMENTS_VIEW_REGION, tolerance=0.95)
    if utils.search_symbol(config.BOARD_HARDWARE_ICON, region = config.ELEMENTS_VIEW_REGION) and utils.check_new_data(config.ELEMENTS_LIB_PATH):
        raise Exception(f"默认-取消后仍导出了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def yjk_001_08():
    utils.check_and_launch_aoi()
    # 1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
    utils.ensure_in_edit_mode()
    if not utils.search_symbol(config.ALG_W_, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
    time.sleep(3)
    # 2、点击【菜单栏】--【元件库】--【导出所有】
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.EXPORT_ALL_PN)
    # 3、弹框 任选一个已有的元件库，点击是。
    utils.search_symbol_erroring(config.TYPE_NAME_DEFAULT)
    time.sleep(0.5)
    utils.click_by_png(config.DJB_YES)
    time.sleep(0.5)
    pyautogui.click((1118,336),clicks=2,duration=0.1)
    pyautogui.click((840,360))
    pyautogui.hotkey("ctrl","c")
    pn_name_copy = pyperclip.paste()
    logger.info(f"导出料号名称: {pn_name_copy}")
    pyautogui.click((1118,358))
    time.sleep(1)
    utils.click_by_png(config.YES)
    while utils.search_symbol(config.EXPORTING_ELEMENTS):
        time.sleep(1.5)
    time.sleep(2)
    # 4、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】，
    utils.click_by_png(config.MANUAL_SELECT)
    utils.click_by_png(config.ELEMENTS_VIEW_REFRESH, region=config.ELEMENTS_VIEW_REGION,tolerance=0.95)
    time.sleep(1)
    # 1）下拉框查找所选的元件库
    pyautogui.click((546,232))
    utils.is_checked((375,246),(387,258),True)
    pyautogui.press("enter")
    utils.search_symbol_erroring(config.TYPE_NAME_DEFAULT)
    # 2）点击所选的元件库 扩展 （元件库->芯片类型->封装类型->料号）
    utils.click_by_png(config.BOARD_ENLARGE,region=config.ELEMENTS_VIEW_REGION, tolerance=0.95)
    time.sleep(1)
    utils.click_by_png(config.BOARD_HARDWARE_ICON,region=config.ELEMENTS_VIEW_REGION, tolerance=0.95)
    time.sleep(1)
    # 3）查看整板上的料号是否都有导到此元件库 查个屁 太麻烦了 测一个顶天了
    image_point = (666,333)
    pyautogui.click(image_point)
    time.sleep(1)
    component_information = utils.read_text(400,700)
    # 4）查看下面信息与导出的料号信息（元件上右键--【元件信息】）对比。
    pyautogui.click(config.CENTRE)
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)
    time.sleep(1)
    # 料号名称
    pn_name = utils.read_text_ocr((364,273),(551,411))
    # 检测pn_name中任意连贯的六个字母是否在pn_name_copy中
    found = any(pn_name[i:i+6] in pn_name_copy for i in range(len(pn_name) - 5))
    if not found:
        raise Exception("疑似没有对应的料号名称")

    # 芯片类型
    utils.is_checked((1070,174),(1082,186),True)
    chip_type = utils.read_text_ocr((1432,150),(1504,164))
    # 料号
    utils.is_checked((1082,252),(1094,264),True)
    pn_ci = utils.read_text(910,255)
    # 封装类型
    utils.is_checked((1082,274),(1094,286),True)
    package_type = utils.read_text(920,280)
    # cad尺寸
    width = utils.read_text(910,405)
    height = utils.read_text(1040,405)
    # xyh
    comp_x = utils.read_text(940,610)
    comp_y = utils.read_text(1000,610)
    comp_h = utils.read_text(1060,610)

    for info, label in zip([chip_type, package_type, width, height, comp_x, comp_y, comp_h], ["芯片类型", "封装类型", "width", "height", "comp_x", "comp_y", "comp_h"]):
        logger.info(f"检查 {label}: {info}")
        if info is None or info not in component_information:
            logger.error(f"{label} 的信息不一致或缺失: {info}")
            raise Exception(f"{label} 的信息不一致或缺失: {info}")
    # 5、所选的元件库文件夹（元件库路径：【设置】--【数据导出配置】--【元件库设置】--【元件库路径】），查看整板上的料号是否都有导到此元件库此元件库；分类名称、芯片类型、料号、封装类型是否与导出的料号信息对应
    search_pattern = f"{chip_type}@{package_type}@{pn_ci}@@Default@*@{comp_x}@{comp_y}@*.scl"
    logger.debug(f"search_pattern: {search_pattern}")
    try:
        # 遍历元件库路径中的所有文件
        found_files = []
        for file in os.listdir(os.path.join(config.ELEMENTS_LIB_PATH, "default")):
            if fnmatch.fnmatch(file, search_pattern):
                found_files.append(file)
                file_path = os.path.join(config.ELEMENTS_LIB_PATH, "default", file)
                modification_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
                if modification_time not in component_information:
                    raise Exception(f"文件 {file} 的修改时间 {modification_time} 未在 {component_information} 中找到")
        # 检查是否找到匹配的文件
        if not found_files:
            raise Exception("没有找到匹配的.scl文件")
        else:
            logger.info(f"找到匹配的.scl文件: {found_files}")
    except Exception as e:
        raise Exception(f"遍历文件时发生错误: {str(e)}")
    
    utils.close_aoi()


@utils.screenshot_error_to_excel()
def yjk_001_09():
    utils.check_and_launch_aoi()
    # 1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
    utils.ensure_in_edit_mode()
    if not utils.search_symbol(config.ALG_W_, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
    time.sleep(3)
    # 2、点击【菜单栏】--【元件库】--【导出所有】
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.EXPORT_ALL_PN)
    # 3、弹框 新增元件库分类名称，点击是。
    utils.search_symbol_erroring(config.IF_EXPORT_ALL_PN)
    time.sleep(0.5)
    elements_type_name = "elements_type_name"
    utils.write_text((900, 525), elements_type_name)
    time.sleep(1)
    pyautogui.press("enter")
    # 复制料号
    pyautogui.click((840,360))
    pyautogui.hotkey("ctrl","c")
    pn = pyperclip.paste()
    logger.info(f"导出料号名称: {pn}")
    utils.click_by_png(config.YES)
    while utils.search_symbol(config.EXPORTING_ELEMENTS):
        time.sleep(1.5)
    time.sleep(0.5)
    # 4、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】，
    utils.click_by_png(config.MANUAL_SELECT)
    utils.click_by_png(config.ELEMENTS_VIEW_REFRESH, region=config.ELEMENTS_VIEW_REGION,tolerance=0.95)
    # 1）下拉框查找所选的元件库
    time.sleep(2)
    pyautogui.click((546,232))
    utils.is_checked((375,246),(387,258),False)
    if not utils.drop_down_box_search(0, config.ELEMENTS_TYPE_NAME, region=config.ELEMENTS_VIEW_DROPDOWN_BOX_REGION):
        raise Exception("没有找到新增的元件库")

    # 2）点击所选的元件库 扩展 （元件库->芯片类型->封装类型->料号）
    utils.click_by_png(config.BOARD_ENLARGE,region=config.ELEMENTS_VIEW_REGION, tolerance=0.95)
    time.sleep(1)
    utils.click_by_png(config.BOARD_HARDWARE_ICON,region=config.ELEMENTS_VIEW_REGION, tolerance=0.95)
    time.sleep(1)
    # 3）查看整板上的料号是否都有导到此元件库
    image_point = (666,333)
    pyautogui.click(image_point)
    time.sleep(0.5)
    component_information = utils.read_text(400,700)
    # 4）查看下面信息与导出的料号信息（元件上右键--【元件信息】）对比。
    pyautogui.click(config.CENTRE)
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)
    time.sleep(1)
    # # 料号名称
    # pn_name = utils.read_text_ocr((364,273),(551,411))
    # # 检测pn_name中任意连贯的六个字母是否在pn中
    # found = any(pn_name[i:i+6] in pn for i in range(len(pn_name) - 5))
    # if not found:
    #     raise Exception("疑似没有对应的料号名称")



    # 芯片类型
    utils.is_checked((1070,174),(1082,186),True)
    chip_type = utils.read_text_ocr((1432,150),(1504,164))
    # 料号
    utils.is_checked((1082,252),(1094,264),True)
    pn_ci = utils.read_text(910,255)
    # 封装类型
    utils.is_checked((1082,274),(1094,286),True)
    package_type = utils.read_text(920,280)
    # cad尺寸
    width = utils.read_text(910,405)
    height = utils.read_text(1040,405)
    # xyh
    comp_x = utils.read_text(940,610)
    comp_y = utils.read_text(1000,610)
    comp_h = utils.read_text(1060,610)
    
    # if pn_ci != pn:
    #     raise Exception(f"{pn_ci} 信息不一致")

    for info, label in zip([chip_type, package_type, width, height, comp_x, comp_y, comp_h], ["芯片类型", "封装类型", "width", "height", "comp_x", "comp_y", "comp_h"]):
        logger.info(f"检查 {label}: {info}")
        if info is None or info not in component_information:
            logger.error(f"{label} 的信息不一致或缺失: {info}")
            raise Exception(f"{label} 的信息不一致或缺失: {info}")

    # 5、所选的元件库文件夹（元件库路径：【设置】--【数据导出配置】--【元件库设置】--【元件库路径】），查看整板上的料号是否都有导到此元件库此元件库；分类名称、芯片类型、料号、封装类型是否与导出的料号信息对应
    search_pattern = f"{chip_type}@{package_type}@{pn_ci}@@Default@*@{comp_x}@{comp_y}@*.scl"
    logger.debug(f"search_pattern: {search_pattern}")
    try:
        # 遍历元件库路径中的所有文件
        found_files = []
        for file in os.listdir(os.path.join(config.ELEMENTS_LIB_PATH, elements_type_name)):
            if fnmatch.fnmatch(file, search_pattern):
                found_files.append(file)
                file_path = os.path.join(config.ELEMENTS_LIB_PATH, elements_type_name, file)
                modification_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
                if modification_time not in component_information:
                    raise Exception(f"文件 {file} 的修改时间 {modification_time} 未在 {component_information} 中找到")
        # 检查是否找到匹配的文件
        if not found_files:
            raise Exception("没有找到匹配的.scl文件")
        else:
            logger.info(f"找到匹配的.scl文件: {found_files}")
    except Exception as e:
        raise Exception(f"遍历文件时发生错误: {str(e)}")
    
    utils.close_aoi()
# @utils.screenshot_error_to_excel()
# def yjk_001_10():
#     utils.check_and_launch_aoi()
#     # 1、选任一元件，双击进入【编辑界面】
#     utils.ensure_in_edit_mode()
#     # 2、点击【菜单栏】--【元件库】--【导入所有】
#     utils.click_by_png(config.ELEMENTS)
#     utils.click_by_png(config.IMPORT_ALL_PN)
#     # 3、选有 多个料号的元件库名称，点击是
#
#     # 4、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】，找到导入的是哪个元件库 哪个料号（点击ABC 标志），元件信息、元件窗口，进行对比
#     utils.close_aoi()
#
# @utils.screenshot_error_to_excel()
# def yjk_001_11():
#     utils.check_and_launch_aoi()
#     # 1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
#     utils.ensure_in_edit_mode()
#     utils.add_window()
#     utils.click_by_png(config.SQUARE_POSITIONING)
#     utils.click_by_png(config.YES)
#     time.sleep(3)
#     # 2、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】
#     utils.click_by_png(config.ELEMENTS)
#     utils.click_by_png(config.MANUAL_SELECT)
#     # 3、点击ABC
#     utils.click_by_png(config.ELEMENTS_VIEW_ABC, tolerance=0.95, region= config.ELEMENTS_VIEW_REGION)

#     utils.close_aoi()
@utils.screenshot_error_to_excel()
def yjk_001_12():
    utils.check_and_launch_aoi()
    # 1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
    utils.ensure_in_edit_mode()
    if not utils.search_symbol(config.ALG_W_, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
    time.sleep(3)
    # 复制料号
    pyautogui.click(config.CENTRE)
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)
    time.sleep(1)    
    # 料号
    utils.is_checked((641,252),(653,264),True)
    pn_ci = utils.read_text(470,255)
    time.sleep(1)
    # 关闭元件信息框
    pyautogui.click((970, 110))
    # 2、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】
    utils.click_by_png(config.ELEMENTS)
    # 先导出所有
    utils.click_by_png(config.EXPORT_ALL_PN)
    utils.search_symbol_erroring(config.IF_EXPORT_ALL_PN)
    time.sleep(1)
    pyautogui.press("enter")
    pyautogui.click((1118, 336))
    pyautogui.press("enter")
    while utils.search_symbol(config.EXPORTING_ELEMENTS):
        time.sleep(1.5)
    time.sleep(0.5)
    utils.click_by_png(config.MANUAL_SELECT)
    time.sleep(1)
    # 3、PN栏输入 当前元件的料号，点击查询标志
    utils.write_text((430,185),pn_ci)
    utils.click_by_png(config.ELEMENTS_VIEW_SEARCH, tolerance=0.95,region=config.ELEMENTS_VIEW_REGION)
    utils.click_by_png(config.BOARD_ENLARGE,region=config.ELEMENTS_VIEW_REGION, tolerance=0.95)
    utils.search_symbol_erroring(config.BOARD_HARDWARE_ICON,region=config.ELEMENTS_VIEW_REGION)
    # 4、点击撤销标志
    pyautogui.click(480,185)
    utils.search_symbol_erroring(config.ELEMENTS_VIEW_PN_EMPTY,region=config.ELEMENTS_VIEW_REGION)

    utils.close_aoi()
@utils.screenshot_error_to_excel()
def yjk_001_13():
    utils.check_and_launch_aoi()
    # 1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
    utils.ensure_in_edit_mode()
    if not utils.search_symbol(config.ALG_W_, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
    time.sleep(3)
    # 获取封装类型
    pyautogui.click(config.CENTRE)
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)
    time.sleep(1)    
    # 封装类型
    utils.is_checked((641,274),(653,286),True)
    package_type = utils.read_text(470,280)
    time.sleep(1)
    pyautogui.click((970, 110))

    # 2、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】
    utils.click_by_png(config.ELEMENTS)
    # 先导出所有
    utils.click_by_png(config.EXPORT_ALL_PN)
    utils.search_symbol_erroring(config.IF_EXPORT_ALL_PN)
    time.sleep(1)
    pyautogui.press("enter")
    pyautogui.click((1118, 336))
    pyautogui.press("enter")
    while utils.search_symbol(config.EXPORTING_ELEMENTS):
        time.sleep(1.5)
    time.sleep(0.5)
    utils.click_by_png(config.MANUAL_SELECT)
    time.sleep(1)
    # 3、PT栏输入 当前元件的封装类型，点击查询标志
    utils.write_text((430,210),package_type)
    utils.click_by_png(config.ELEMENTS_VIEW_SEARCH, tolerance=0.95,region=config.ELEMENTS_VIEW_REGION)
    utils.click_by_png(config.BOARD_ENLARGE,region=config.ELEMENTS_VIEW_REGION, tolerance=0.95)
    utils.search_symbol_erroring(config.BOARD_HARDWARE_ICON,region=config.ELEMENTS_VIEW_REGION)
    # 4、点击撤销标志
    pyautogui.click(480,205)
    utils.search_symbol_erroring(config.ELEMENTS_VIEW_PT_EMPTY,region=config.ELEMENTS_VIEW_REGION)

    utils.close_aoi()

# @utils.screenshot_error_to_excel()
# def yjk_001_14():
#     utils.check_and_launch_aoi()
#     # 1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
#     utils.ensure_in_edit_mode()
#     # 2、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】
#     utils.click_by_png(config.ELEMENTS)
#     # 先导出所有后才有元件库
#     utils.click_by_png(config.EXPORT_ALL_PN)
#     utils.search_symbol_erroring(config.IF_EXPORT_ALL_PN)
#     time.sleep(0.5)
#     elements_type_name = "elements_type_name"
#     utils.write_text((900, 525), elements_type_name)
#     time.sleep(1)
#     pyautogui.press("enter")
#     pyautogui.click((1118, 336))
#     pyautogui.press("enter")
#     while utils.search_symbol(config.EXPORTING_ELEMENTS):
#         time.sleep(1.5)
#     time.sleep(0.5)
#     # 导出下一个元件库
#     utils.click_by_png(config.EXPORT_ALL_PN)
#     utils.search_symbol_erroring(config.IF_EXPORT_ALL_PN)
#     time.sleep(0.5)
#     test = "test"
#     utils.write_text((900, 525), test)
#     time.sleep(1)
#     pyautogui.press("enter")
#     pyautogui.click((1118, 336))
#     pyautogui.press("enter")
#     while utils.search_symbol(config.EXPORTING_ELEMENTS):
#         time.sleep(1.5)
#     time.sleep(0.5)
#
#     utils.click_by_png(config.MANUAL_SELECT)
#     # 3、点击下拉框勾选某些元件库，点击OK
#     time.sleep(2)
#     pyautogui.click((546,232))
#     element_view_test
#     # 4、再次点击下拉框，勾选Select All

    #
    #
    # utils.close_aoi()

@utils.screenshot_error_to_excel()
def yjk_001_15():
    utils.check_and_launch_aoi()
    # 1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
    utils.ensure_in_edit_mode()
    if not utils.search_symbol(config.ALG_W_, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
    time.sleep(3)
    # 2、点击【菜单栏】--【元件库】--【导出所有】/【导出当前料号】
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.EXPORT_ALL_PN)
    # 3、弹框新增元件库分类名称，点击是
    utils.search_symbol_erroring(config.IF_EXPORT_ALL_PN)
    time.sleep(0.5)
    elements_type_name = "elements_type_name"
    utils.write_text((900, 525), elements_type_name)
    time.sleep(1)
    pyautogui.press("enter")
    pyautogui.click((1118, 336))
    pyautogui.press("enter")
    while utils.search_symbol(config.EXPORTING_ELEMENTS):
        time.sleep(1.5)
    time.sleep(0.5)
    # 4、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】
    utils.click_by_png(config.MANUAL_SELECT)
    # 点击刷新（循环标志）
    utils.click_by_png(config.ELEMENTS_VIEW_REFRESH)
    # 5、点击最上方的元件库 扩展 （元件库->芯片类型->封装类型->料号），查看导出的元件库料号，是否都显示
    time.sleep(2)
    pyautogui.click((546,232))
    utils.is_checked((375,246),(387,258),False)
    if not utils.drop_down_box_search(0, config.ELEMENTS_TYPE_NAME, region=config.ELEMENTS_VIEW_DROPDOWN_BOX_REGION):
        raise Exception("没有找到新增的元件库")
    utils.click_by_png(config.BOARD_ENLARGE,region=config.ELEMENTS_VIEW_REGION, tolerance=0.95)
    utils.search_symbol_erroring(config.BOARD_HARDWARE_ICON,region=config.ELEMENTS_VIEW_REGION)
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def yjk_001_16():
    utils.check_and_launch_aoi()
    utils.check_refresh_tree(False)
    # 1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
    utils.ensure_in_edit_mode()
    if not utils.search_symbol(config.ALG_W_, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
    time.sleep(3)
    # 2、点击【菜单栏】--【元件库】--【导出所有】/【导出当前料号】
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.EXPORT_ALL_PN)
    # 3、弹框新增元件库分类名称，点击是
    utils.search_symbol_erroring(config.IF_EXPORT_ALL_PN)
    time.sleep(0.5)
    elements_type_name = "elements_type_name"
    utils.write_text((900, 525), elements_type_name)
    time.sleep(1)
    pyautogui.press("enter")
    pyautogui.click((1118, 336))
    pyautogui.press("enter")
    while utils.search_symbol(config.EXPORTING_ELEMENTS):
        time.sleep(1.5)
    time.sleep(0.5)
    # 4、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】 显示在最前面 切
    utils.click_by_png(config.MANUAL_SELECT)
    # 5、点击最上方的元件库 扩展 （元件库->芯片类型->封装类型->料号），查看导出的元件库料号，是否都显示
    time.sleep(2)
    pyautogui.click((546,232))
    utils.is_checked((375,246),(387,258),False)
    if not utils.drop_down_box_search(0, config.ELEMENTS_TYPE_NAME, region=config.ELEMENTS_VIEW_DROPDOWN_BOX_REGION):
        raise Exception("没有找到新增的元件库")
    utils.search_symbol_erroring(config.BOARD_HARDWARE_ICON)
    utils.close_aoi()
@utils.screenshot_error_to_excel()
def yjk_001_17():
    utils.check_and_launch_aoi()
    utils.check_export_image_libs(False)
    # 1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
    utils.ensure_in_edit_mode()
    if not utils.search_symbol(config.ALG_W_, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
    time.sleep(3)
    # 2、点击【菜单栏】--【元件库】--【导出所有】/【导出当前料号】
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.EXPORT_ALL_PN)
    # 3、弹框新增元件库分类名称，点击是
    utils.search_symbol_erroring(config.IF_EXPORT_ALL_PN)
    time.sleep(0.5)
    elements_type_name = "elements_type_name"
    utils.write_text((900, 525), elements_type_name)
    time.sleep(1)
    pyautogui.press("enter")
    pyautogui.click((1118, 336))
    pyautogui.press("enter")
    while utils.search_symbol(config.EXPORTING_ELEMENTS):
        time.sleep(1.5)
    time.sleep(0.5)
    # 4、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】
    utils.click_by_png(config.MANUAL_SELECT)
    # 5、找到刚刚导出的元件库，扩展，双击料号，查看第一张图片
    time.sleep(2)
    pyautogui.click((546,232))
    utils.is_checked((375,246),(387,258),False)
    if not utils.drop_down_box_search(0, config.ELEMENTS_TYPE_NAME, region=config.ELEMENTS_VIEW_DROPDOWN_BOX_REGION):
        raise Exception("没有找到新增的元件库")
    utils.click_by_png(config.BOARD_ENLARGE,region=config.ELEMENTS_VIEW_REGION, tolerance=0.95)
    time.sleep(1)
    utils.click_by_png(config.BOARD_HARDWARE_ICON,region=config.ELEMENTS_VIEW_REGION, tolerance=0.95)
    time.sleep(1)
    # 有显示图片，图片底色是绿色，有算法框
    if utils.search_symbol(config.ELEMENTS_VIEW_PICTURE_EMPTY_UP):
        raise Exception("未显示图片")
    if not utils.check_color_in_region((0,100,0),config.ELEMENTS_VIEW_IMAGE_REGION):
        raise Exception("图片底色不是绿色")
    image_point = (666,333)
    pyautogui.click(image_point)
    time.sleep(0.5)
    component_information = utils.read_text(400,700)
    frame = "[1]"
    if frame not in component_information:
        raise Exception("算法框未显示")
    utils.close_aoi()
@utils.screenshot_error_to_excel()
def yjk_001_18():
    utils.check_and_launch_aoi()
    utils.check_export_image_libs(True)
    # 1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
    utils.ensure_in_edit_mode()
    if not utils.search_symbol(config.ALG_W_, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
    time.sleep(3)
    # 2、点击【菜单栏】--【元件库】--【导出所有】/【导出当前料号】
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.EXPORT_ALL_PN)
    # 3、弹框新增元件库分类名称，点击是
    utils.search_symbol_erroring(config.IF_EXPORT_ALL_PN)
    time.sleep(0.5)
    elements_type_name = "elements_type_name"
    utils.write_text((900, 525), elements_type_name)
    time.sleep(1)
    pyautogui.press("enter")
    pyautogui.click((1118, 336))
    pyautogui.press("enter")
    while utils.search_symbol(config.EXPORTING_ELEMENTS):
        time.sleep(1.5)
    time.sleep(0.5)
    # 4、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】
    utils.click_by_png(config.MANUAL_SELECT)
    # 5、找到刚刚导出的元件库，扩展，双击料号，查看第一张图片
    time.sleep(2)
    pyautogui.click((546,232))
    utils.is_checked((375,246),(387,258),False)
    if not utils.drop_down_box_search(0, config.ELEMENTS_TYPE_NAME, region=config.ELEMENTS_VIEW_DROPDOWN_BOX_REGION):
        raise Exception("没有找到新增的元件库")
    utils.click_by_png(config.BOARD_ENLARGE,region=config.ELEMENTS_VIEW_REGION, tolerance=0.95)
    time.sleep(1)
    utils.click_by_png(config.BOARD_HARDWARE_ICON,region=config.ELEMENTS_VIEW_REGION, tolerance=0.95)
    time.sleep(1)
    if utils.search_symbol(config.ELEMENTS_VIEW_PICTURE_EMPTY_UP, 2, config.ELEMENTS_VIEW_REGION):
        raise Exception("无显示实际元件的图片")
    image_point = (666,333)
    pyautogui.click(image_point)
    time.sleep(0.5)
    component_information = utils.read_text(400,700)
    frame = "[1]"
    if frame not in component_information:
        raise Exception("算法框未显示")

    utils.close_aoi()
@utils.screenshot_error_to_excel()
def yjk_001_19():
    utils.check_and_launch_aoi()
    utils.check_export_pn_add_sn(False)
    # 1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
    utils.ensure_in_edit_mode()
    if not utils.search_symbol(config.ALG_W_, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
    time.sleep(3)
    # 2、点击【菜单栏】--【元件库】--【导出所有】
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.EXPORT_ALL_PN)
    # 3、弹框新增元件库分类名称，点击是
    utils.search_symbol_erroring(config.IF_EXPORT_ALL_PN)
    time.sleep(0.5)
    elements_type_name = "elements_type_name"
    utils.write_text((900, 525), elements_type_name)
    time.sleep(1)
    pyautogui.press("enter")
    pyautogui.click((1118, 336))
    pyautogui.press("enter")
    while utils.search_symbol(config.EXPORTING_ELEMENTS):
        time.sleep(1.5)
    time.sleep(0.5)
    # 4、编辑界面，点击【菜单栏】--【编辑】--【检测窗口】，多个元件，新增窗口
    for _ in range(3):
        utils.click_component()
        if utils.search_symbol(config.QUESTION_MARK, 3):
            time.sleep(1)
            pyautogui.press("enter")
            time.sleep(5)
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
        time.sleep(3)
    # 5、再次重复步骤2
    utils.click_by_png(config.EXPORT_ALL_PN)
    pyautogui.press("enter")
    pyautogui.click((1118, 336))
    pyautogui.press("enter")
    while utils.search_symbol(config.EXPORTING_ELEMENTS):
        time.sleep(1.5)
    # 6、弹框下拉框选步骤3 的分类名称，点击是
    pyautogui.click(1094,525)
    utils.click_by_png(config.ELEMENTS_TYPE_NAME)
    time.sleep(1)
    pyautogui.press("enter")
    # 7、弹出是否覆盖弹框，点击所有
    while utils.search_symbol(config.EXPORTING_ELEMENTS):
        time.sleep(1.5)
    utils.search_symbol_erroring(config.QUESTION_MARK)
    utils.click_by_png(config.ALL)
    while utils.search_symbol(config.EXPORTING_ELEMENTS):
        time.sleep(1.5)
    export_time = datetime.datetime.now().strftime("%H:%M")
    time.sleep(0.5)
    # 8、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】
    utils.click_by_png(config.MANUAL_SELECT)
    # 9、找到刚刚导出的元件库，扩展，双击料号
    time.sleep(2)
    pyautogui.click((546,232))
    utils.is_checked((375,246),(387,258),False)
    if not utils.drop_down_box_search(0, config.ELEMENTS_TYPE_NAME, region=config.ELEMENTS_VIEW_DROPDOWN_BOX_REGION):
        raise Exception("没有找到新增的元件库")
    utils.click_by_png(config.BOARD_ENLARGE,region=config.ELEMENTS_VIEW_REGION, tolerance=0.95)
    time.sleep(1)
    utils.click_by_png(config.BOARD_HARDWARE_ICON,region=config.ELEMENTS_VIEW_REGION, tolerance=0.95)
    time.sleep(1)
    # 10、查看第一张图片
    image_point = (666,333)
    pyautogui.click(image_point)
    time.sleep(0.5)
    # 1）导出时间是否是刚刚时间
    component_information = utils.read_text(400,700)
    # 检查导出时间的前后一分钟是否在component_information中
    export_time_dt = datetime.datetime.strptime(export_time, "%H:%M")
    one_minute = datetime.timedelta(minutes=1)
    times_to_check = [
        (export_time_dt - one_minute).strftime("%H:%M"),
        export_time_dt.strftime("%H:%M"),
        (export_time_dt + one_minute).strftime("%H:%M")
    ]
    time_found = any(time_str in component_information for time_str in times_to_check)
    if not time_found:
        raise Exception("导出时间的前后一分钟未在元件信息中找到")
    # 2）下面的窗口 是否有刚刚新增的窗口
    if "方形定位" not in component_information:
        raise Exception("没有刚刚的窗口'")
    if not utils.search_symbol(config.ELEMENTS_VIEW_PICTURE_EMPTY_DOWN, region=config.ELEMENTS_VIEW_REGION):
        raise Exception("料号有多张图片")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def yjk_001_20():
    utils.check_and_launch_aoi()
    utils.check_export_pn_add_sn(False)
    # 1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
    utils.ensure_in_edit_mode()
    if not utils.search_symbol(config.ALG_W_, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
    time.sleep(3)
    # 2、点击【菜单栏】--【元件库】--【导出当前料号】
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.EXPORT_CURRENT_PN)
    # 3、弹框新增元件库分类名称，点击是
    utils.search_symbol_erroring(config.ELEMENTS_INFORMATION)
    time.sleep(0.5)
    elements_type_name = "elements_type_name"
    utils.write_text((960,470), elements_type_name)
    time.sleep(1)
    pyautogui.press("enter")
    while utils.search_symbol(config.EXPORTING_ELEMENTS):
        time.sleep(1.5)
    time.sleep(0.5)   
    # 4、编辑界面，点击【菜单栏】--【编辑】--【检测窗口】，任选一个元件新增窗口
    utils.click_component()
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    while utils.search_symbol(config.SAVING_PROGRAM):
        time.sleep(2)
    time.sleep(1)
    if not utils.search_symbol(config.ALG_W_, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
    time.sleep(3)
    # 5、再次重复步骤2
    utils.click_by_png(config.EXPORT_ALL_PN)
    # 6、弹框下拉框选步骤3 的分类名称，点击是
    pyautogui.click(1094,525)
    utils.click_by_png(config.ELEMENTS_TYPE_NAME)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(0.5)
    pyautogui.click((1118, 336))
    pyautogui.press("enter")
    # 7、是否覆盖弹框，点击是
    while utils.search_symbol(config.EXPORTING_ELEMENTS):
        time.sleep(0.2)
    utils.search_symbol_erroring(config.QUESTION_MARK)
    utils.click_by_png(config.CHOOSED_YES)
    while utils.search_symbol(config.EXPORTING_ELEMENTS):
        time.sleep(1.5)
    export_time = datetime.datetime.now().strftime("%H:%M")
    # 8、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】
    utils.click_by_png(config.MANUAL_SELECT)
    # 9、找到刚刚导出的元件库，扩展，双击料号
    time.sleep(2)
    pyautogui.click((546,232))
    utils.is_checked((375,246),(387,258),False)
    if not utils.drop_down_box_search(0, config.ELEMENTS_TYPE_NAME, region=config.ELEMENTS_VIEW_DROPDOWN_BOX_REGION):
        raise Exception("没有找到新增的元件库")
    utils.click_by_png(config.BOARD_ENLARGE,region=config.ELEMENTS_VIEW_REGION, tolerance=0.95)
    time.sleep(1)
    utils.click_by_png(config.BOARD_HARDWARE_ICON,region=config.ELEMENTS_VIEW_REGION, tolerance=0.95)
    time.sleep(1)
    # 10、查看第一张图片
    image_point = (666,333)
    pyautogui.click(image_point)
    time.sleep(0.5)
    # 1）导出时间是否是刚刚时间
    component_information = utils.read_text(400,700)
    # 检查导出时间的前后一分钟是否在component_information中
    export_time_dt = datetime.datetime.strptime(export_time, "%H:%M")
    one_minute = datetime.timedelta(minutes=1)
    times_to_check = [
        (export_time_dt - one_minute).strftime("%H:%M"),
        export_time_dt.strftime("%H:%M"),
        (export_time_dt + one_minute).strftime("%H:%M")
    ]
    time_found = any(time_str in component_information for time_str in times_to_check)
    if not time_found:
        raise Exception("导出时间的前后一分钟未在元件信息中找到")
    # 2）下面的窗口 是否有刚刚新增的窗口
    if "方形定位" not in component_information:
        raise Exception("没有刚刚的窗口'")
    if utils.search_symbol(config.ELEMENTS_VIEW_PICTURE_EMPTY_UP, 2, config.ELEMENTS_VIEW_REGION):
        raise Exception("料号缺少图片")
    
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def yjk_001_21():
    utils.check_and_launch_aoi()
    utils.check_export_pn_add_sn(False)
    # 1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
    utils.ensure_in_edit_mode()
    if not utils.search_symbol(config.ALG_W_, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
    time.sleep(3)
    # 2、点击【菜单栏】--【元件库】--【导入所有】/【导出当前料号】
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.EXPORT_CURRENT_PN)
    # 3、弹框新增元件库分类名称，点击是
    utils.search_symbol_erroring(config.ELEMENTS_INFORMATION)
    time.sleep(0.5)
    elements_type_name = "elements_type_name"
    utils.write_text((960,470), elements_type_name)
    time.sleep(1)
    pyautogui.press("enter")
    while utils.search_symbol(config.EXPORTING_ELEMENTS):
        time.sleep(1.5)
    time.sleep(1)
    # 4、编辑界面，点击【菜单栏】--【编辑】--【检测窗口】，新增窗口
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(3)
    # 5、再次重复步骤2
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.EXPORT_CURRENT_PN)
    # 6、弹框下拉框选步骤3 的分类名称，点击是
    pyautogui.click(1074,470)
    utils.click_by_png(config.ELEMENTS_TYPE_NAME)
    time.sleep(1)
    pyautogui.press("enter")
    # 7、弹出覆盖弹框,点否
    while utils.search_symbol(config.EXPORTING_ELEMENTS):
        time.sleep(1.5)
    utils.search_symbol_erroring(config.NO)
    utils.click_by_png(config.NO)
    while utils.search_symbol(config.EXPORTING_ELEMENTS):
        time.sleep(1.5)
    export_time = datetime.datetime.now().strftime("%H:%M")
    time.sleep(0.5)
    # 8、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】
    utils.click_by_png(config.MANUAL_SELECT)    
    # 9、找到刚刚导出的元件库，扩展，双击料号
    time.sleep(2)
    pyautogui.click((546,232))
    utils.is_checked((375,246),(387,258),False)
    if not utils.drop_down_box_search(0, config.ELEMENTS_TYPE_NAME, region=config.ELEMENTS_VIEW_DROPDOWN_BOX_REGION):
        raise Exception("没有找到新增的元件库")
    utils.click_by_png(config.BOARD_ENLARGE,region=config.ELEMENTS_VIEW_REGION, tolerance=0.95)
    time.sleep(1)
    utils.click_by_png(config.BOARD_HARDWARE_ICON,region=config.ELEMENTS_VIEW_REGION, tolerance=0.95)
    time.sleep(1)
    # 10、查看第一张图片
    image_point = (666,333)
    pyautogui.click(image_point)
    time.sleep(0.5)
    # 1）导出时间是否是刚刚时间
    component_information = utils.read_text(400,700)
    # 检查导出时间的前后十秒是否在component_information中
    export_time_dt = datetime.datetime.strptime(export_time, "%H:%M")
    ten_seconds = datetime.timedelta(seconds=10)
    times_to_check = [
        (export_time_dt - ten_seconds).strftime("%H:%M"),
        export_time_dt.strftime("%H:%M"),
        (export_time_dt + ten_seconds).strftime("%H:%M")
    ]
    time_found = any(time_str in component_information for time_str in times_to_check)
    if time_found:
        raise Exception("导出时间为第二次导出的时间")
    # 2）下面的窗口 是否有刚刚新增的窗口
    if "颜色面积" in component_information:
        raise Exception("元件库视图-元件信息内有新增的算法'")
    if utils.search_symbol(config.ELEMENTS_VIEW_PICTURE_EMPTY_UP, 2, config.ELEMENTS_VIEW_REGION):
        raise Exception("料号缺少图片")
    
    utils.close_aoi()
@utils.screenshot_error_to_excel()
def yjk_001_22():
    utils.check_and_launch_aoi()
    utils.check_export_pn_add_sn(True)
    # 1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
    utils.ensure_in_edit_mode()
    if not utils.search_symbol(config.ALG_W_, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
    time.sleep(3)
    # 2、点击【菜单栏】--【元件库】--【导出所有】
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.EXPORT_ALL_PN)
    utils.search_symbol_erroring(config.IF_EXPORT_ALL_PN)
    # 3、弹框新增元件库分类名称，点击是
    time.sleep(0.5)
    elements_type_name = "elements_type_name"
    utils.write_text((900, 525), elements_type_name)
    time.sleep(1)
    pyautogui.press("enter")
    pyautogui.click((1118, 336))
    pyautogui.press("enter")
    while utils.search_symbol(config.EXPORTING_ELEMENTS):
        time.sleep(1.5)
    time.sleep(2)
    # 4、编辑界面，点击【菜单栏】--【编辑】--【检测窗口】，多选几个元件新增窗口
    for _ in range(3):
        logger.error(1)
        utils.click_component()
        if utils.search_symbol(config.QUESTION_MARK, 3):
            time.sleep(1)
            pyautogui.press("enter")
            if utils.search_symbol(config.SAVING_PROGRAM):
                time.sleep(1)
        time.sleep(8)
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
        time.sleep(3)
    # 5、再次重复步骤2
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.EXPORT_ALL_PN)
    # 6、弹框下拉框选步骤3 的分类名称，点击是
    pyautogui.click(1094,525)
    utils.click_by_png(config.ELEMENTS_TYPE_NAME)
    time.sleep(1)
    pyautogui.press("enter")
    pyautogui.click((1118, 336))
    pyautogui.press("enter")
    # 7、是否弹出覆盖弹框 (不弹)
    while utils.search_symbol(config.EXPORTING_ELEMENTS, 2):
        time.sleep(1.5)
    if utils.search_symbol(config.QUESTION_MARK, 3):
        raise Exception("弹出覆盖弹框")
    export_time = datetime.datetime.now().strftime("%H:%M")
    # 8、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】
    utils.click_by_png(config.MANUAL_SELECT)
    # 9、找到刚刚导出的元件库，扩展，双击料号
    time.sleep(2)
    pyautogui.click((546,232))
    utils.is_checked((375,246),(387,258),False)
    if not utils.drop_down_box_search(0, config.ELEMENTS_TYPE_NAME, region=config.ELEMENTS_VIEW_DROPDOWN_BOX_REGION):
        raise Exception("没有找到新增的元件库")
    utils.click_by_png(config.BOARD_ENLARGE,region=config.ELEMENTS_VIEW_REGION, tolerance=0.95)
    time.sleep(1)
    utils.click_by_png(config.BOARD_HARDWARE_ICON,region=config.ELEMENTS_VIEW_REGION, tolerance=0.95)
    time.sleep(1)
    # 10、查看第一张图片
    image_point = (666,333)
    pyautogui.click(image_point)
    time.sleep(2)
    # 1）导出时间是否是刚刚时间
    component_information = utils.read_text(400,700)
    # 检查导出时间的前后一分钟是否在component_information中
    export_time_dt = datetime.datetime.strptime(export_time, "%H:%M")
    one_minute = datetime.timedelta(minutes=1)
    times_to_check = [
        (export_time_dt - one_minute).strftime("%H:%M"),
        export_time_dt.strftime("%H:%M"),
        (export_time_dt + one_minute).strftime("%H:%M")
    ]
    time_found = any(time_str in component_information for time_str in times_to_check)
    if not time_found:
        raise Exception("导出时间的前后一分钟未在元件信息中找到")
    # 2）下面的窗口 是否有刚刚新增的窗口
    if "方形定位" not in component_information:
        raise Exception("没有刚刚的窗口'")
    if utils.search_symbol(config.ELEMENTS_VIEW_PICTURE_EMPTY_UP, 2, config.ELEMENTS_VIEW_REGION):
        raise Exception("元件上方图片缺失")
    if utils.search_symbol(config.ELEMENTS_VIEW_PICTURE_EMPTY_DOWN, 2, config.ELEMENTS_VIEW_REGION):
        raise Exception("元件下方图片缺失")

    utils.close_aoi()
@utils.screenshot_error_to_excel()
def yjk_001_23():
    utils.check_and_launch_aoi()
    utils.check_export_pn_add_sn(True)
    utils.ensure_in_edit_mode()
    if not utils.search_symbol(config.ALG_W_, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
    time.sleep(3)
    # 2、点击【菜单栏】--【元件库】--【导出当前料号】
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.EXPORT_CURRENT_PN)
    # 3、弹框新增元件库分类名称，点击是
    utils.search_symbol_erroring(config.ELEMENTS_INFORMATION)
    time.sleep(0.5)
    elements_type_name = "elements_type_name"
    utils.write_text((960,470), elements_type_name)
    time.sleep(1)
    utils.click_by_png(config.YES)
    while utils.search_symbol(config.EXPORTING_ELEMENTS):
        time.sleep(1.5)
    time.sleep(2.5)
    # 4、编辑界面，点击【菜单栏】--【编辑】--【检测窗口】，任选一个元件 新增窗口
    utils.click_component()
    time.sleep(5)
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(3)
    # 5、再次重复步骤2
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.EXPORT_CURRENT_PN)
    # 6、弹框下拉框选步骤3 的分类名称，点击是
    pyautogui.click(1074,470)
    utils.click_by_png(config.ELEMENTS_TYPE_NAME)
    time.sleep(1)
    utils.click_by_png(config.YES)
    # 7、是否弹出覆盖弹框 (不弹)
    while utils.search_symbol(config.EXPORTING_ELEMENTS, 2):
        time.sleep(1.5)
    if utils.search_symbol(config.QUESTION_MARK, 3):
        raise Exception("弹出覆盖弹框")
    export_time = datetime.datetime.now().strftime("%H:%M")
    # 8、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】
    utils.click_by_png(config.MANUAL_SELECT)
    # 9、找到刚刚导出的元件库，扩展，双击料号
    time.sleep(2)
    pyautogui.click((546,232))
    utils.is_checked((375,246),(387,258),False)
    if not utils.drop_down_box_search(0, config.ELEMENTS_TYPE_NAME, region=config.ELEMENTS_VIEW_DROPDOWN_BOX_REGION):
        raise Exception("没有找到新增的元件库")
    utils.click_by_png(config.BOARD_ENLARGE,region=config.ELEMENTS_VIEW_REGION, tolerance=0.95)
    time.sleep(1)
    utils.click_by_png(config.BOARD_HARDWARE_ICON,region=config.ELEMENTS_VIEW_REGION, tolerance=0.95)
    time.sleep(1)
    # 10、查看第一张图片
    image_point = (666,333)
    pyautogui.click(image_point)
    time.sleep(0.5)
    # 1）导出时间是否是刚刚时间
    component_information = utils.read_text(400,700)
    # 检查导出时间的前后十秒是否在component_information中
    export_time_dt = datetime.datetime.strptime(export_time, "%H:%M")
    ten_seconds = datetime.timedelta(seconds=10)
    times_to_check = [
        (export_time_dt - ten_seconds).strftime("%H:%M"),
        export_time_dt.strftime("%H:%M"),
        (export_time_dt + ten_seconds).strftime("%H:%M")
    ]
    time_found = any(time_str in component_information for time_str in times_to_check)
    if not time_found:
        raise Exception("导出时间的前后十秒未在元件信息中找到")
    # 2）下面的窗口 是否有刚刚新增的窗口
    if "颜色面积" not in component_information:
        raise Exception("没有刚刚的窗口'")
    if utils.search_symbol(config.ELEMENTS_VIEW_PICTURE_EMPTY_UP, 2, config.ELEMENTS_VIEW_REGION):
        raise Exception("元件上方图片缺失")
    if utils.search_symbol(config.ELEMENTS_VIEW_PICTURE_EMPTY_DOWN, 2, config.ELEMENTS_VIEW_REGION):
        raise Exception("元件下方图片缺失")
    utils.close_aoi()
@utils.screenshot_error_to_excel()
def yjk_001_24():
    utils.check_and_launch_aoi()
    utils.check_allow_preview(False)
    # 1、主界面整板上，任选一个元件，双击元件进入【编辑界面】
    utils.ensure_in_edit_mode()
    # 2、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】
    utils.click_by_png(config.ELEMENTS)
    # 得先有
    utils.click_by_png(config.EXPORT_ALL_PN)
    pyautogui.press("enter")
    pyautogui.click((1118, 336))
    pyautogui.press("enter")
    while utils.search_symbol(config.EXPORTING_ELEMENTS, 2):
        time.sleep(0.5)
    if utils.search_symbol(config.QUESTION_MARK, 3):
        pyautogui.press("enter")
    time.sleep(1)
    utils.click_by_png(config.MANUAL_SELECT)
    # 3、任选一个料号，点击图片 (检测框不在元件上)
    pyautogui.click((546,232))
    utils.is_checked((375,246),(387,258),True)
    pyautogui.press("enter")
    utils.click_by_png(config.BOARD_ENLARGE,region=config.ELEMENTS_VIEW_REGION, tolerance=0.95)
    time.sleep(1)
    utils.click_by_png(config.BOARD_HARDWARE_ICON,region=config.ELEMENTS_VIEW_REGION, tolerance=0.95)
    time.sleep(1)
    image_point = (666,333)
    pyautogui.click(image_point)
    time.sleep(0.5)
    # 右侧界面预览，而预览无数据只有图
    if not utils.search_symbol(config.RULER, timeout=5, region=config.ELEMENTS_VIEW_COMPONENT_REGION):
        raise Exception("设置了不可以预览但实际可以")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def yjk_001_25():
    utils.check_and_launch_aoi()
    utils.check_allow_preview(True)
    # 1、主界面整板上，任选一个元件，双击元件进入【编辑界面】
    utils.ensure_in_edit_mode()
    # 2、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】
    utils.click_by_png(config.ELEMENTS)
    # 得先有
    utils.click_by_png(config.EXPORT_ALL_PN)
    pyautogui.press("enter")
    pyautogui.click((1118, 336))
    pyautogui.press("enter")
    while utils.search_symbol(config.EXPORTING_ELEMENTS, 2):
        time.sleep(0.5)
    if utils.search_symbol(config.QUESTION_MARK, 3):
        pyautogui.press("enter")
    time.sleep(1)
    utils.click_by_png(config.MANUAL_SELECT)
    # 3、任选一个料号，点击图片 (检测框不在元件上)
    pyautogui.click((546,232))
    utils.is_checked((375,246),(387,258),True)
    pyautogui.press("enter")
    utils.click_by_png(config.BOARD_ENLARGE,region=config.ELEMENTS_VIEW_REGION, tolerance=0.95)
    time.sleep(1)
    utils.click_by_png(config.BOARD_HARDWARE_ICON,region=config.ELEMENTS_VIEW_REGION, tolerance=0.95)
    time.sleep(1)
    image_point = (666,333)
    pyautogui.click(image_point)
    time.sleep(0.5)
    # 右侧界面预览，而预览无数据只有图
    if utils.search_symbol(config.RULER, timeout=5, region=config.ELEMENTS_VIEW_COMPONENT_REGION):
        raise Exception("设置了可以预览但实际不行")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def yjk_001_26():
    utils.check_and_launch_aoi()
    utils.check_import_sync_package(False)
    # 1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
    utils.ensure_in_edit_mode()
    if not utils.search_symbol(config.ALG_W_, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
    time.sleep(3)
    # 2、右键 点击元件信息，修改封装类型成NULL
    pyautogui.click(config.CENTRE)
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)
    time.sleep(1)
    # 封装类型
    utils.is_checked((641,274),(653,286),True)
    utils.write_text((470,280), "NULL")
    time.sleep(0.5)
    pyautogui.click((970,110))
    # 3、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.MANUAL_SELECT)
    # ，任意选一个料号 封装类型不是NULL，双击图片
    utils.click_by_png(config.BOARD_ENLARGE,region=config.ELEMENTS_VIEW_REGION, tolerance=0.95)
    time.sleep(1)
    start_time = time.time()
    while True:
        utils.click_by_png(config.BOARD_HARDWARE_ICON, region=config.ELEMENTS_VIEW_REGION, use_random=1)
        image_point = (666, 333)
        pyautogui.click(image_point)
        time.sleep(0.5)
        component_information = utils.read_text(400, 700)
        if "Package Type" in component_information and "NULL" not in component_information.split("Package Type")[1]:
            break
        if time.time() - start_time > 60:
            raise Exception("超过1分钟都没找到封装类型不是NULL的料号")
    time.sleep(2)
    pyautogui.doubleClick(image_point)
    time.sleep(5)
    # 4、右键 点击元件信息，查看封装类型 （是元件库里的）
    pyautogui.click(config.CENTRE)
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)
    time.sleep(1)
    # 封装类型
    utils.is_checked((1082,274),(1094,286),True)
    package_type = utils.read_text(920,280)
    if "NULL" in package_type:
        raise Exception("封装类型为NULL")
    
    utils.close_aoi()


@utils.screenshot_error_to_excel()
def yjk_001_27():
    utils.check_and_launch_aoi()
    utils.check_import_sync_package(False)
    # 1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
    utils.ensure_in_edit_mode()
    if not utils.search_symbol(config.ALG_W_, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
    time.sleep(3)
    pyautogui.click(config.CENTRE)
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)
    time.sleep(1)  
    # 封装类型  
    utils.is_checked((641,274),(653,286),True)
    package_type = utils.read_text(470,280)
    pyautogui.click((970,110))
    # 2、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.MANUAL_SELECT)
    # ，任意选一个料号 封装类型跟此元件不一样，双击图片
    utils.click_by_png(config.BOARD_ENLARGE,region=config.ELEMENTS_VIEW_REGION, tolerance=0.95)
    start_time = time.time()
    while True:
        utils.click_by_png(config.BOARD_HARDWARE_ICON, region=config.ELEMENTS_VIEW_REGION, use_random=1)
        image_point = (666, 333)
        pyautogui.click(image_point)
        time.sleep(0.5)
        component_information = utils.read_text(400, 700)
        if "Package Type" in component_information and package_type not in component_information.split("Package Type")[1]:
            break
        if time.time() - start_time > 60:
            raise Exception(f"超过1分钟都没找到封装类型不是{package_type}的料号")
    time.sleep(2)
    pyautogui.doubleClick(image_point)
    time.sleep(5)
    # 3、右键 点击元件信息，查看封装类型
    pyautogui.click(config.CENTRE)   
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)
    time.sleep(1)
    utils.is_checked((1082,274),(1094,286),True)
    package_type_current = utils.read_text(920,280)
    if package_type not in package_type_current:
        raise Exception(f"封装类型不一致，当前{package_type_current}，原先{package_type}")
    utils.close_aoi()
@utils.screenshot_error_to_excel()
def yjk_001_28():
    utils.check_and_launch_aoi()
    utils.check_import_sync_package(True)
    # 1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
    utils.ensure_in_edit_mode()
    if not utils.search_symbol(config.ALG_W_, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
    time.sleep(3)
    pyautogui.click(config.CENTRE)
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)
    time.sleep(1)
    utils.is_checked((641,274),(653,286),True)
    package_type = utils.read_text(470,280)
    pyautogui.click((970,110))
    # 2、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.MANUAL_SELECT)
    # ，任意选一个料号 封装类型跟此元件不一样，双击图片
    utils.click_by_png(config.BOARD_ENLARGE,region=config.ELEMENTS_VIEW_REGION, tolerance=0.95)
    start_time = time.time()
    while True:
        utils.click_by_png(config.BOARD_HARDWARE_ICON, region=config.ELEMENTS_VIEW_REGION, use_random=1)
        image_point = (666, 333)
        pyautogui.click(image_point)
        time.sleep(0.5)
        component_information = utils.read_text(400, 700)
        if "Package Type" in component_information and package_type not in component_information.split("Package Type")[1]:
            break
        if time.time() - start_time > 60:
            raise Exception(f"超过1分钟都没找到封装类型不是{package_type}的料号")
    time.sleep(2)
    pyautogui.doubleClick(image_point)
    time.sleep(5)
    # 3、右键 点击元件信息，查看封装类型
    pyautogui.click(config.CENTRE)
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)
    time.sleep(1)
    utils.is_checked((1082,274),(1094,286),True)
    package_type_current = utils.read_text(920,280)
    if package_type in package_type_current:
        raise Exception(f"封装类型非元件库里的，当前{package_type_current}，原先{package_type}")
    utils.close_aoi()
@utils.screenshot_error_to_excel()
def yjk_001_29():
    utils.check_and_launch_aoi()
    utils.check_pn_1_day()
    # 1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
    utils.ensure_in_edit_mode()
    # 2、编辑界面，点击【菜单栏】--【编辑】--【检测窗口】，任选一个元件 新增窗口
    if not utils.search_symbol(config.ALG_W_, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
    time.sleep(3)
    # 3、点击【菜单栏】--【元件库】--【导出所有】
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.EXPORT_ALL_PN)
    # 4、弹框新增元件库类型，点击是，弹出可选择导出的料号
    utils.search_symbol_erroring(config.IF_EXPORT_ALL_PN)
    time.sleep(0.5)
    elements_type_name = "elements_type_name"
    utils.write_text((900, 525), elements_type_name)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(0.5)
    # 确认一天内对应的勾选框勾选
    points_dates = config.SELECT_PN_EXPORT_LIB_POINTS_DATES
    previous_date = None
    for item in points_dates:
        point = item["date"]
        checkbox = item["checkbox"]
        pyautogui.click(point)
        pyautogui.hotkey("ctrl", "c")
        current_date = pyperclip.paste()
        if current_date == "" or current_date == previous_date:
            break
        previous_date = current_date
        try:
            current_date_dt = datetime.datetime.strptime(current_date, "%Y-%m-%d %H:%M:%S")
            days_difference = (datetime.datetime.now() - current_date_dt).days
            top_left, bottom_right = checkbox
            checkbox_checked = utils.if_checked(top_left, bottom_right)
            if days_difference <= 1 and not checkbox_checked:
                raise Exception(f"日期{current_date}的勾选框未勾选(即一天内的勾选框未勾选)")
            elif days_difference > 1 and checkbox_checked:
                raise Exception(f"日期{current_date}的勾选框被勾选(即一天外的勾选框被勾选了)")
        except ValueError as e:
            raise Exception(f"处理日期时出错了，复制的日期为: {current_date}，错误信息: {str(e)}")
    # 5、勾选所有，点击导出
    pyautogui.click((1118, 336))
    pyautogui.press("enter")
    while utils.search_symbol(config.EXPORTING_ELEMENTS):
        time.sleep(1.5)
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def yjk_001_30():
    utils.check_and_launch_aoi()
    utils.check_export_wm_img_1()
    # 1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
    utils.ensure_in_edit_mode()
    time.sleep(3)
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    # 2、编辑界面，点击【菜单栏】--【编辑】--【检测窗口】，任选一个元件 新增需要添加代料的窗口，添加2个代料
    utils.add_window()
    utils.click_by_png(config.ADD_CHECKED_SENIOR)
    utils.click_by_png(config.COLOR_MATCHING)
    utils.click_by_png(config.YES)
    time.sleep(3)
    utils.click_by_png(config.YES)
    time.sleep(5)
    # utils.click_by_png(config.ADD_IMAGE_CLOSE)
    for _ in range(2):
        utils.search_symbol_erroring(config.ADD_STANDARD_IMAGE)
        utils.click_by_png(config.ADD_STANDARD_IMAGE)
        time.sleep(1)
        utils.click_by_png(config.YES)
        time.sleep(5)
        # utils.click_by_png(config.ADD_IMAGE_CLOSE)
    # 3、点击【菜单栏】--【元件库】--【导出当前料号】
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.EXPORT_CURRENT_PN)
    # 4、弹框新增元件库类型，点击是
    utils.search_symbol_erroring(config.ELEMENTS_INFORMATION)
    time.sleep(0.5)
    elements_type_name = "elements_type_name"
    utils.write_text((960,470), elements_type_name)
    time.sleep(1)
    utils.click_by_png(config.YES)
    while utils.search_symbol(config.EXPORTING_ELEMENTS):
        time.sleep(1.5)
    time.sleep(0.5)       
    # 5、点击【菜单栏】--【元件库】--【导入当前料号】
    utils.click_by_png(config.IMPORT_CURRENT_PN)
    time.sleep(1)
    pyautogui.click((1094,525))
    time.sleep(1)
    utils.click_by_png(config.ELEMENTS_TYPE_NAME)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(5)
    # 6、查看步骤2添加的窗口代料是否是1
    utils.click_by_png(config.CW_COLOR_MATCHING)
    time.sleep(3)
    utils.search_symbol_erroring(config.WAIT_MATERIAL_EMPTY,region=config.PALETTE_REGION)
    utils.close_aoi()
@utils.screenshot_error_to_excel()
def yjk_001_31():
    utils.check_and_launch_aoi()
    utils.check_export_wm_img_1_all(True)
    # 1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
    utils.ensure_in_edit_mode()
    time.sleep(3)
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    # 2、编辑界面，点击【菜单栏】--【编辑】--【检测窗口】，任选一个元件 新增需要添加代料的窗口，添加3个代料
    utils.add_window()
    utils.click_by_png(config.ADD_CHECKED_SENIOR)
    utils.click_by_png(config.COLOR_MATCHING)
    utils.click_by_png(config.YES)
    time.sleep(3)
    utils.click_by_png(config.YES)
    time.sleep(5)
    for _ in range(2):
        utils.search_symbol_erroring(config.ADD_STANDARD_IMAGE)
        utils.click_by_png(config.ADD_STANDARD_IMAGE)
        time.sleep(1)
        utils.click_by_png(config.YES)
        time.sleep(10)
    # 3、点击【菜单栏】--【元件库】--【导出当前料号】
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.EXPORT_CURRENT_PN)
    # 4、弹框新增元件库类型，点击是
    utils.search_symbol_erroring(config.ELEMENTS_INFORMATION)
    time.sleep(0.5)
    elements_type_name = "elements_type_name"
    utils.write_text((960,470), elements_type_name)
    time.sleep(1)
    utils.click_by_png(config.YES)
    while utils.search_symbol(config.EXPORTING_ELEMENTS):
        time.sleep(1.5)
    time.sleep(0.5)   
    # 5、点击【菜单栏】--【元件库】--【导入当前料号】
    utils.click_by_png(config.IMPORT_CURRENT_PN)
    time.sleep(1)
    pyautogui.click((1094,525))
    time.sleep(1)
    utils.click_by_png(config.ELEMENTS_TYPE_NAME)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(5)
    # 6、查看步骤2添加的窗口代料是否是3
    utils.click_by_png(config.CW_COLOR_MATCHING)
    time.sleep(3)
    if not utils.search_symbol(config.WAIT_MATERIAL_EMPTY,5, region=config.PALETTE_REGION):
        raise Exception("代料数量不为3")
    utils.close_aoi()
@utils.screenshot_error_to_excel()
def yjk_001_32():
    utils.check_and_launch_aoi()
    utils.check_import_delete_ocv_wm(True)
    # 1、主界面整板上，任选一个有字符检测待料的元件，双击进入元件编辑界面
    utils.ensure_in_edit_mode()
    utils.add_window()
    utils.click_by_png(config.ADD_CHECKED_OCV)
    utils.click_by_png(config.YES)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
    if utils.search_symbol_erroring(config.OCV_EDIT_APPLY):
        # 得先填充内容
        utils.write_text((820, 270), "4")
        utils.write_text((820, 300), "fuck")
        utils.click_by_png(config.OCV_EDIT_APPLY)
        time.sleep(3)
    # 2、菜单栏点击【导出当前料号】，弹框 新增分类名称，点击是
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.EXPORT_CURRENT_PN)
    utils.search_symbol_erroring(config.ELEMENTS_INFORMATION)
    time.sleep(0.5)
    elements_type_name = "elements_type_name"
    utils.write_text((960,470), elements_type_name)
    time.sleep(1)
    pyautogui.press("enter")
    while utils.search_symbol(config.EXPORTING_ELEMENTS):
        time.sleep(1.5)
    time.sleep(0.5)  
    # 3、双击其他料号的元件，进入元件编辑界面
    pyautogui.moveTo(200, 400)
    for _ in range(10):
        pyautogui.scroll(-200)
        time.sleep(1)
    utils.click_component()
    time.sleep(1)
    if utils.search_symbol(config.QUESTION_MARK, 3):
        pyautogui.press("enter")
    time.sleep(1)
    while utils.search_symbol(config.SAVING_PROGRAM):
        time.sleep(2)
    time.sleep(1)
    # 4、点击菜单栏--【元件库】--【手动选择】
    utils.click_by_png(config.MANUAL_SELECT)
    # 5、查询步骤2 导出的料号，双击图片
    time.sleep(2)
    pyautogui.click((546,232))
    utils.is_checked((375,246),(387,258),False)
    if not utils.drop_down_box_search(0, config.ELEMENTS_TYPE_NAME, region=config.ELEMENTS_VIEW_DROPDOWN_BOX_REGION):
        raise Exception("没有找到新增的元件库")
    utils.click_by_png(config.BOARD_ENLARGE,region=config.ELEMENTS_VIEW_REGION, tolerance=0.95)
    time.sleep(1)
    utils.click_by_png(config.BOARD_HARDWARE_ICON,region=config.ELEMENTS_VIEW_REGION, tolerance=0.95)
    time.sleep(1)  
    image_point = (666,333)
    pyautogui.click(image_point, clicks=2, duration=0.1)
    while utils.search_symbol(config.LOADING_ELEMENTS):
        time.sleep(2)
    time.sleep(2)  
    # 6、查看字符检测待料图 是否有删除
    utils.click_by_png(config.ALG_OCV)
    utils.search_symbol_erroring(config.WAIT_MATERIAL_ALL_EMPTY,region=config.PALETTE_REGION)
    utils.close_aoi()
@utils.screenshot_error_to_excel()
def yjk_001_33():
    utils.check_and_launch_aoi()
    # 1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
    utils.ensure_in_edit_mode()
    if not utils.search_symbol(config.ALG_W_, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
    time.sleep(3)
    # 2、右键点击【元件信息】--【标准】，修改xyh值
    pyautogui.click(config.CENTRE)
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)
    time.sleep(1)    
    # x
    x = f"{random.uniform(0.5, 1):.3f}"
    utils.write_text((490, 610), x)
    # y
    y = f"{random.uniform(0.5, 1):.3f}"
    utils.write_text((550, 610), y)
    # h
    h = f"{random.uniform(0.5, 1):.3f}"
    utils.write_text((610, 610), h)
    time.sleep(1)
    pyautogui.click((970, 110))
    # 3、上方菜单栏点击【导出当前料号】/【导出所有】
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.EXPORT_CURRENT_PN)
    # 4、弹框新增元件库类型，点击确认
    utils.search_symbol_erroring(config.ELEMENTS_INFORMATION)
    time.sleep(0.5)
    elements_type_name = "elements_type_name"
    utils.write_text((960,470), elements_type_name)
    time.sleep(1)
    pyautogui.press("enter")
    while utils.search_symbol(config.EXPORTING_ELEMENTS):
        time.sleep(1.5)
    time.sleep(0.5)
    # 5、上方菜单栏点击【手动选择】--【元件库视图】
    utils.click_by_png(config.MANUAL_SELECT)
    # 6、找到导出的是哪个料号，点击图片，查看元件xyh值，进行对比
    time.sleep(2)
    pyautogui.click((546,232))
    utils.is_checked((375,246),(387,258),False)
    if not utils.drop_down_box_search(0, config.ELEMENTS_TYPE_NAME, region=config.ELEMENTS_VIEW_DROPDOWN_BOX_REGION):
        raise Exception("没有找到新增的元件库")
    utils.click_by_png(config.BOARD_ENLARGE,region=config.ELEMENTS_VIEW_REGION, tolerance=0.95)
    time.sleep(1)
    utils.click_by_png(config.BOARD_HARDWARE_ICON,region=config.ELEMENTS_VIEW_REGION, tolerance=0.95)
    time.sleep(1) 
    image_point = (666,333)
    pyautogui.click(image_point)
    time.sleep(0.5)
    component_information = utils.read_text(400,700)
    for value, label in zip([x, y, h], ['x', 'y', 'h']):
        if value not in component_information:
            raise Exception(f"{label}值{value}未在元件信息中找到")
    if utils.search_symbol(config.ELEMENTS_VIEW_PICTURE_EMPTY_UP,region=config.ELEMENTS_VIEW_REGION):
        raise Exception("没有导出")

    utils.close_aoi()

@utils.screenshot_error_to_excel()
def yjk_001_34():
    utils.check_and_launch_aoi()
    utils.check_allow_cad_teach(False)
    utils.check_import_update_height(True)
    # 1、主界面整板上，任选一个没有方形定位算法的元件，双击元件进入【编辑界面】 草你妈 没有方形定位算法的有算法的元件 也不描述清楚
    utils.ensure_in_edit_mode()
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    # ======
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(4)
    # ======
    # 2、点击【菜单栏】--【元件库】--【导出当前料号】
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.EXPORT_CURRENT_PN)
    # 3、弹框新增元件库类型，点击确认
    utils.search_symbol_erroring(config.ELEMENTS_INFORMATION)
    time.sleep(0.5)
    elements_type_name = "elements_type_name"
    utils.write_text((960,470), elements_type_name)
    time.sleep(1)
    utils.click_by_png(config.YES)
    while utils.search_symbol(config.EXPORTING_ELEMENTS):
        time.sleep(1.5)
    time.sleep(0.5)       
    # 4、右键点击【元件信息】--【标准】，修改h值
    pyautogui.click(config.CENTRE)
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)
    time.sleep(1)
    h = f"{random.uniform(0.5, 1):.3f}"
    utils.write_text((610, 610), h)
    time.sleep(1)
    pyautogui.click((970, 110))
    # 5、导入 刚刚导出的料号，对比h值
    utils.click_by_png(config.IMPORT_CURRENT_PN)
    time.sleep(1)
    pyautogui.click((1094,525))
    time.sleep(1)
    if not utils.drop_down_box_search(0, config.ELEMENTS_TYPE_NAME, region=config.PN_IMPORT_DROPDOWN_BOX_REGION):
        raise Exception("没有找到新增的元件库")
    time.sleep(3)
    pyautogui.click(config.CENTRE)
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)
    time.sleep(1)
    comp_h = utils.read_text(610,610)

    if h not in comp_h:
        raise Exception(f"导入的h值{comp_h}与元件库的h值{h}不一致")

    utils.close_aoi()

@utils.screenshot_error_to_excel()
def yjk_001_35():
    utils.check_and_launch_aoi()
    utils.check_allow_cad_teach(False)
    utils.check_import_update_height(False)
    # 1、主界面整板上，任选一个没有方形定位算法的元件，双击元件进入【编辑界面】 草你妈 没有方形定位算法的有算法的元件 也不描述清楚
    utils.ensure_in_edit_mode()
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    # ======
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(4)
    # ======
    # 2、点击【菜单栏】--【元件库】--【导出当前料号】
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.EXPORT_CURRENT_PN)
    # 3、弹框新增元件库类型，点击确认
    utils.search_symbol_erroring(config.ELEMENTS_INFORMATION)
    time.sleep(0.5)
    elements_type_name = "elements_type_name"
    utils.write_text((960,470), elements_type_name)
    time.sleep(1)
    utils.click_by_png(config.YES)
    while utils.search_symbol(config.EXPORTING_ELEMENTS):
        time.sleep(1.5)
    time.sleep(0.5)       
    # 4、右键点击【元件信息】--【标准】，修改h值
    pyautogui.click(config.CENTRE)
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)
    time.sleep(1)    
    h = f"{random.uniform(0.5, 1):.3f}"
    utils.write_text((610, 610), h)
    time.sleep(1)
    pyautogui.click(970, 110)
    # 5、点击【菜单栏】--【元件库】--【导出当前料号】，弹框选步骤3的元件库类型，对比h值
    utils.click_by_png(config.EXPORT_CURRENT_PN)
    pyautogui.click(1074,470)
    utils.click_by_png(config.ELEMENTS_TYPE_NAME)
    time.sleep(3)
    utils.click_by_png(config.YES)
    time.sleep(5)
    pyautogui.click(config.CENTRE)
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)
    time.sleep(1)    
    comp_h = utils.read_text(610,610)

    if h not in comp_h:
        raise Exception(f"导入的h值{comp_h}与元件库的h值{h}不一致")

    utils.close_aoi()


@utils.screenshot_error_to_excel()
def yjk_001_36():
    utils.check_and_launch_aoi()
    utils.check_allow_cad_teach(False)
    # 不管这边选啥 都对结果没影响。也就是说要验证两次h值
    sbchoice = random.choice([True, False])
    utils.check_import_update_height(sbchoice)
    # 1、主界面整板上，任选一个有方形定位算法的元件，双击元件进入【编辑界面】
    utils.ensure_in_edit_mode()
    utils.add_window()
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    time.sleep(5)
    # 2、点击【菜单栏】--【元件库】--【导出当前料号】
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.EXPORT_CURRENT_PN)
    # 3、弹框新增元件库类型，点击确认
    utils.search_symbol_erroring(config.ELEMENTS_INFORMATION)
    time.sleep(0.5)
    elements_type_name = "elements_type_name"
    utils.write_text((960,470), elements_type_name)
    time.sleep(1)
    utils.click_by_png(config.YES)
    while utils.search_symbol(config.EXPORTING_ELEMENTS):
        time.sleep(1.5)
    time.sleep(0.5)       
    # 4、右键点击【元件信息】--【标准】，修改h值
    pyautogui.click(config.CENTRE)
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)
    time.sleep(1)    
    h = f"{random.uniform(0.5, 1):.3f}"
    utils.write_text((610, 610), h)
    time.sleep(1)
    pyautogui.click(970, 110)
    # 5、点击【菜单栏】--【元件库】--【导出当前料号】，弹框选步骤3的元件库类型，对比h值
    utils.click_by_png(config.EXPORT_CURRENT_PN)
    pyautogui.click(1074,470)
    utils.click_by_png(config.ELEMENTS_TYPE_NAME)
    time.sleep(3)
    utils.search_symbol_erroring(config.ELEMENTS_INFORMATION)
    time.sleep(5)
    pyautogui.click(config.CENTRE) 
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)
    time.sleep(1)    
    comp_h = utils.read_text(610,610)

    if h not in comp_h:
        raise Exception("勾选的情况会影响到h值")

    utils.close_aoi()

@utils.screenshot_error_to_excel()
def yjk_001_37():
    utils.check_and_launch_aoi()
    utils.check_allow_cad_teach(False)
    utils.check_import_component_xy(False)
    utils.check_standard_xyh(False)
    # 1、主界面整板上，任选一个没有方形定位算法的元件，双击元件进入【编辑界面】
    utils.ensure_in_edit_mode()
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    # ======
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(5)
    # ======
    # 2、点击【菜单栏】--【元件库】--【导出当前料号】
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.EXPORT_CURRENT_PN)
    # 3、弹框新增元件库类型，点击确认
    utils.search_symbol_erroring(config.ELEMENTS_INFORMATION)
    time.sleep(0.5)
    elements_type_name = "elements_type_name"
    utils.write_text((960,470), elements_type_name)
    time.sleep(1)
    utils.click_by_png(config.YES)
    while utils.search_symbol(config.EXPORTING_ELEMENTS):
        time.sleep(1.5)
    time.sleep(0.5)    
    # 4、右键点击【元件信息】--【标准】，修改xy值
    pyautogui.click(config.CENTRE)
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)
    time.sleep(1)    
    x = f"{random.uniform(0.5, 1):.3f}"
    y = f"{random.uniform(0.5, 1):.3f}"
    utils.write_text((490, 610), x)
    utils.write_text((550, 610), y)
    time.sleep(1)
    pyautogui.click(970, 110)
    # 5、点击【菜单栏】--【元件库】--【导出当前料号】，弹框选步骤3的元件库类型
    utils.click_by_png(config.EXPORT_CURRENT_PN)
    pyautogui.click(1074,470)
    utils.click_by_png(config.ELEMENTS_TYPE_NAME)
    time.sleep(3)
    utils.click_by_png(config.YES)
    time.sleep(5)
    # 6、右键点击元件信息，查看标准xy
    pyautogui.click(config.CENTRE)
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)
    time.sleep(1)
    comp_x = utils.read_text(490, 610)
    comp_y = utils.read_text(550, 610)
    if x in comp_x or y in comp_y:
        raise Exception("xy值非该元件尺寸")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def yjk_001_38():
    utils.check_and_launch_aoi()
    utils.check_allow_cad_teach(False)
    utils.check_import_component_xy(True)
    utils.check_standard_xyh(False)
    utils.ensure_in_edit_mode()
    # 1、主界面整板上，任选一个没有方形定位算法的元件，双击元件进入【编辑界面】
    utils.ensure_in_edit_mode()
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    # ======
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(3)
    utils.click_by_png(config.YES)
    time.sleep(5)
    # 先读取元件的xy
    pyautogui.click(config.CENTRE)
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)
    time.sleep(1)
    read_x = utils.read_text(490, 610)
    read_y = utils.read_text(550, 610)
    pyautogui.click(970, 110)
    # 2、点击【菜单栏】--【元件库】--【导出当前料号】
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.EXPORT_CURRENT_PN)
    # 3、弹框新增元件库类型，点击确认
    utils.search_symbol_erroring(config.ELEMENTS_INFORMATION)
    time.sleep(0.5)
    elements_type_name = "elements_type_name"
    utils.write_text((960,470), elements_type_name)
    time.sleep(1)
    utils.click_by_png(config.YES)
    while utils.search_symbol(config.EXPORTING_ELEMENTS):
        time.sleep(1.5)
    time.sleep(0.5)    
    # 4、右键点击【元件信息】--【标准】，修改xy值
    pyautogui.click(config.CENTRE)
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)
    time.sleep(1)
    x = f"{random.uniform(0.5, 1):.3f}"
    y = f"{random.uniform(0.5, 1):.3f}"
    utils.write_text((490, 610), x)
    utils.write_text((550, 610), y)
    time.sleep(1)
    pyautogui.click(970, 110)
    # 5、点击【菜单栏】--【元件库】--【导出当前料号】，弹框选步骤3的元件库类型
    utils.click_by_png(config.EXPORT_CURRENT_PN)
    pyautogui.click(1074,470)
    utils.click_by_png(config.ELEMENTS_TYPE_NAME)
    time.sleep(3)
    utils.click_by_png(config.YES)
    time.sleep(5)
    # 6、右键点击元件信息，查看标准xy
    pyautogui.click(config.CENTRE)
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)
    time.sleep(1)
    comp_x = utils.read_text(490,610)
    comp_y = utils.read_text(550,610)
    if read_x not in comp_x or read_y not in comp_y:
        raise Exception("xy值非元件库里的值")
    utils.close_aoi()


@utils.screenshot_error_to_excel()
def yjk_001_39():
    utils.check_and_launch_aoi()
    utils.check_standard_xyh(True)
    utils.check_allow_cad_teach(False)
    utils.check_import_component_xy(True)
    utils.check_import_update_height(True)
    # 1、主界面整板上，任选一个有算法的元件，双击元件进入【编辑界面】
    utils.ensure_in_edit_mode()
    if not utils.search_symbol(config.ALG_W_, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
    time.sleep(3)
    # 2、点击【菜单栏】--【元件库】--【导出当前料号】
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.EXPORT_CURRENT_PN)
    # 3、弹框新增元件库类型，点击确认
    utils.search_symbol_erroring(config.ELEMENTS_INFORMATION)
    time.sleep(0.5)
    elements_type_name = "elements_type_name"
    utils.write_text((960,470), elements_type_name)
    time.sleep(1)
    utils.click_by_png(config.YES)
    while utils.search_symbol(config.EXPORTING_ELEMENTS):
        time.sleep(1.5)
    time.sleep(0.5)    
    # 4、右键点击【元件信息】--【标准】，修改xyh值
    pyautogui.click(config.CENTRE)
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)
    time.sleep(1)
    x = f"{random.uniform(0.5, 1):.3f}"
    y = f"{random.uniform(0.5, 1):.3f}"
    h = f"{random.uniform(0.5, 1):.3f}"
    utils.write_text((490, 610), x)
    utils.write_text((550, 610), y)
    utils.write_text((610, 610), h)
    time.sleep(1)
    pyautogui.click(970, 110)
    # 5、点击【菜单栏】--【元件库】--【导入当前料号】，弹框选步骤3的元件库类型
    utils.click_by_png(config.IMPORT_CURRENT_PN)
    time.sleep(1)
    pyautogui.click((1094,525))
    time.sleep(1)
    utils.click_by_png(config.ELEMENTS_TYPE_NAME)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(5)
    # 6、右键点击元件信息，查看标准xyh
    pyautogui.click(config.CENTRE)
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)
    time.sleep(1)
    comp_x = utils.read_text(940,610)
    comp_y = utils.read_text(1000,610)
    comp_h = utils.read_text(1060,610)
    if x not in comp_x or y not in comp_y or h not in comp_h:
        raise Exception("xyh值非步骤4的值")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def yjk_001_40():
    utils.check_and_launch_aoi()
    utils.filter_auxiliary_window(True)
    # 1、选任一元件，双击进入【编辑界面】
    utils.ensure_in_edit_mode()
    # 2、新增3d基准面、板弯补偿算法，导出此料号
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(2)
    utils.add_window()
    utils.click_by_png(config.REFERENCE_PLANE_3D)
    utils.click_by_png(config.YES)
    time.sleep(3)
    utils.add_window()
    utils.click_by_png(config.PLATE_BENDING_COMPENSATION)
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    time.sleep(7)
    # 导出当前料号
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.EXPORT_CURRENT_PN)
    utils.click_by_png(config.YES)
    time.sleep(2)
    utils.search_symbol_erroring(config.CW_COPLANARITY_3D, region=config.COMPONENT_WINDOW_REGION)
    utils.search_symbol_erroring(config.CW_SQUARE_POSITIONING, region=config.COMPONENT_WINDOW_REGION)
    # 3、清空算法，导入 刚导出的料号
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(2)
    utils.click_by_png(config.IMPORT_CURRENT_PN)
    utils.click_by_png(config.YES)
    while utils.search_symbol(config.IMPORTING_ELEMENTS):
        time.sleep(1.5)
    time.sleep(1)
    if utils.search_symbol(config.CW_COPLANARITY_3D, region=config.COMPONENT_WINDOW_REGION):
        raise Exception("3d基准面未清空")
    if utils.search_symbol(config.CW_SQUARE_POSITIONING, region=config.COMPONENT_WINDOW_REGION):
        raise Exception("板弯补偿算法未清空")
    # 4、删除重添加或编辑 3d基准面、板弯补偿算法，导入 刚导出的料号
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(2)

    utils.add_window()
    utils.click_by_png(config.REFERENCE_PLANE_3D)
    utils.click_by_png(config.YES)
    time.sleep(5)
    utils.add_window()
    utils.click_by_png(config.PLATE_BENDING_COMPENSATION)
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    time.sleep(5)
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.IMPORT_CURRENT_PN)
    utils.click_by_png(config.YES,tolerance=0.7)
    while utils.search_symbol(config.IMPORTING_ELEMENTS):
        time.sleep(1.5)
    time.sleep(1)
    utils.search_symbol_erroring(config.CW_COPLANARITY_3D, region=config.COMPONENT_WINDOW_REGION)
    utils.search_symbol_erroring(config.CW_SQUARE_POSITIONING, region=config.COMPONENT_WINDOW_REGION)

    # 5、删除3d基准面、板弯补偿算法，导入 刚导出的料号
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(2)
    utils.click_by_png(config.IMPORT_CURRENT_PN)
    if utils.search_symbol(config.IF_IMPORT_CURRENT_PN):
        pyautogui.press("enter")
    while utils.search_symbol(config.IMPORTING_ELEMENTS):
        time.sleep(1.5)
    time.sleep(1)
    if utils.search_symbol(config.CW_COPLANARITY_3D, region=config.COMPONENT_WINDOW_REGION):
        raise Exception("5、3d基准面也被导入")
    if utils.search_symbol(config.CW_SQUARE_POSITIONING, region=config.COMPONENT_WINDOW_REGION):
        raise Exception("5、板弯补偿算法被导入")
    utils.close_aoi()

# # TODO 需要在线aoi
# @utils.screenshot_error_to_excel()
# def yjk_001_41():
#     # 1、新建job，弹出 是否导入默认库弹框，点击是
#     # 2、查看主界面导入的元件 是否是所选的元件库
#     # 3、重新改变 下拉框选择任一元件库【设置】--【数据导出配置】--【元件库设置】--【默认】
#     # 4、选任一元件，双击进入【编辑界面】
#     utils.ensure_in_edit_mode()
#     # 5、点击菜单栏-【元件库】-【导出当前料号】/【导出所有】/【导入当前料号】/【导入所有】，弹出的框 ，显示的元件库名称 是步骤3所选择的
#     utils.click_by_png(config.ELEMENTS)
#     utils.click_by_png(config.EXPORT_CURRENT_PN)
#     utils.close_aoi()
@utils.screenshot_error_to_excel()
def yjk_001_42():
    # 1、输入百分比值【设置】--【硬件设置】--【数据导出配置】--【元件库】--【导入筛选限制】
    utils.check_and_launch_aoi()
    utils.check_import_filtering_restriction("80")
    # 2、主界面整板上，任选一个元件，双击元件进入【编辑界面】
    utils.ensure_in_edit_mode()
    # 3、点击菜单栏【元件库】--【手动选择】，宽度高度是当前元件的xy尺寸
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.EXPORT_ALL_PN)
    utils.search_symbol_erroring(config.IF_EXPORT_ALL_PN)
    time.sleep(0.5)
    pyautogui.press("enter")
    time.sleep(0.5)
    pyautogui.click((1118, 336))
    utils.click_by_png(config.YES)
    while utils.search_symbol(config.EXPORTING_ELEMENTS):
        time.sleep(1.5)
    time.sleep(0.5)
    utils.click_by_png(config.MANUAL_SELECT)
    pyautogui.click((546, 232))
    utils.is_checked((375,246),(387,258),True)
    pyautogui.press("enter")
    # 4、随机点击芯片类型
    utils.click_by_png(config.BOARD_ENLARGE, region=config.ELEMENTS_VIEW_REGION, tolerance=0.95)
    # 遍历所有元件，计算点击的量和无图的量 比例为x
    no_pic_count = 0
    click_count = 0
    icons = pyautogui.locateAllOnScreen(config.BOARD_HARDWARE_ICON, region=config.ELEMENTS_VIEW_REGION)
    for icon in icons:
        pyautogui.click(icon)
        click_count += 1
        if utils.search_symbol(config.ELEMENTS_VIEW_PICTURE_EMPTY_UP, region=config.ELEMENTS_VIEW_REGION):
            no_pic_count += 1
    x = no_pic_count / click_count
    # 5、重复步骤1、步骤4
    utils.check_import_filtering_restriction("0")
    time.sleep(2)
    utils.click_by_png(config.ELEMENTS_VIEW_REFRESH,region=config.ELEMENTS_VIEW_REGION)
    utils.click_by_png(config.BOARD_ENLARGE, region=config.ELEMENTS_VIEW_REGION, tolerance=0.95)
    # 遍历所有元件，计算无图的量比点击的量 比例为y
    no_pic_count = 0
    click_count = 0
    icons = pyautogui.locateAllOnScreen(config.BOARD_HARDWARE_ICON, region=config.ELEMENTS_VIEW_REGION)
    for icon in icons:
        pyautogui.click(icon)
        click_count += 1
        if not utils.search_symbol(config.ELEMENTS_VIEW_PICTURE_EMPTY_UP, region=config.ELEMENTS_VIEW_REGION):
            no_pic_count += 1
    y = no_pic_count / click_count
    logger.debug(f"x:{x},y:{y}")
    if x>y:
        raise Exception("不符合：百分比值越小，限制越多")

    utils.close_aoi()

# 不勾共享元件库路径
@utils.screenshot_error_to_excel()
def yjk_001_43():
    # 先打开并前置aoi
    utils.check_and_launch_aoi()
    # 查看共享元件库路径【设置】-【硬件设置】-【数据导出配置】-【共享元件库路径】路径基本不变，因此我路径先用绝对路径了
    # utils.read_text(config.SHARE_LIB_PATH_COORDINATE)
    # 不勾选
    utils.check_share_lib_path(False)
    # 选任一元件，双击进入编辑界面（确保在编辑界面）
    utils.ensure_in_edit_mode()
    # 修改元件
    utils.modify_component()
    # 点击保存按钮
    utils.click_by_png(config.SAVE)
    time.sleep(2)
    # 查看弹窗是否隐藏（导出到公共元件库）检查是否置灰
    if_grey = utils.search_symbol_erroring(config.EXPORT_PUBLIC_PROGRAM_GRAY, 10)
    if if_grey:
        pyautogui.press("enter")
        logger.info("置灰")
    # 确保共享文件库文件夹内没有新数据生成
    if utils.check_new_data(config.SHARE_LIB_PATH):
        logger.error("共享元件库文件夹内有新数据生成")
        raise Exception("共享元件库文件夹内有新数据生成")
    else:
        logger.info("共享元件库文件夹内没有新数据生成")
    utils.close_aoi()
# 不勾共享元件库路径
@utils.screenshot_error_to_excel()
def yjk_001_44():
    utils.check_and_launch_aoi()
    utils.check_share_lib_path(False)
    utils.ensure_in_edit_mode()
    # 点击菜单栏-工具-同步到公共元件库
    utils.click_by_png(config.TOOL)
    utils.click_by_png(config.SYNC_TO_PUBLIC_LIBS)
    # 检测到提示框（没有该预期结果就报错）
    utils.search_symbol_erroring(config.PLEASE_OPEN_PUBLIC_LIBS)
    pyautogui.press("enter")
    utils.close_aoi()

# 勾共享元件库路径
@utils.screenshot_error_to_excel()
def yjk_001_45():
    utils.check_and_launch_aoi()
    utils.check_share_lib_path(True)
    utils.check_default_export_auto_save(True, False)
    utils.ensure_in_edit_mode()
    # 修改元件，左侧列表切换元件，弹框点击是
    utils.modify_component()
    utils.click_by_png(config.SAVE)
    time.sleep(1)
    logger.error("第一次检测勾选框")
    utils.search_symbol_erroring(config.EXPORT_PUBLIC_PROGRAM_CHECKED)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(5)
    utils.modify_component()
    utils.click_component()
    time.sleep(1)
    if utils.search_symbol(config.QUESTION_MARK, 3):
        pyautogui.press("enter")
    utils.click_by_png(config.SAVE)
    # 再次确认默认勾选（切换元件后点击保存）
    logger.error("第二次检测勾选框")
    utils.search_symbol_erroring(config.EXPORT_PUBLIC_PROGRAM_CHECKED)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(5)
    # 最后确认默认勾选（点击返回）
    utils.modify_component()
    if utils.search_symbol(config.EDIT_DARK, 3):
        utils.click_by_png(config.EDIT_DARK)
    else:
        utils.search_symbol_erroring(config.EDIT_LIGHT)
    utils.click_by_png(config.EDIT_BACK)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(3)
    utils.click_by_png(config.SAVE)
    logger.error("第三次检测勾选框")
    utils.search_symbol_erroring(config.EXPORT_PUBLIC_PROGRAM_CHECKED)
    time.sleep(1)
    pyautogui.press("enter")
    if utils.check_new_data(config.SHARE_LIB_PATH):
        logger.info("共享元件库文件夹内有新数据生成")
    else:
        raise Exception("共享元件库文件夹内没有新数据生成")
    utils.close_aoi()


# 勾共享元件库路径
@utils.screenshot_error_to_excel()
def yjk_001_46():
    utils.check_and_launch_aoi()
    utils.check_share_lib_path(True)
    utils.check_default_export_auto_save(False, False)
    utils.ensure_in_edit_mode()
    # 修改元件
    time.sleep(8)
    # 第一次进入会直接选中，不需要按b了
    for _ in range(6):
        pyautogui.press('down')
        time.sleep(0.5)
    # utils.modify_component()
    utils.click_by_png(config.SAVE)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    logger.info("第一次检测未勾选框")
    utils.search_symbol_erroring(config.EXPORT_PUBLIC_PROGRAM_GRAY)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(8)
    # 修改元件，左侧列表切换元件，再次确定
    for _ in range(6):
        pyautogui.press('down')
        time.sleep(0.5)
    utils.click_component()
    if utils.search_symbol(config.QUESTION_MARK, 3):
        time.sleep(1)
        pyautogui.press("enter")
        if utils.search_symbol(config.SAVING_PROGRAM):
            time.sleep(1)
    utils.click_by_png(config.SAVE)
    logger.info("第二次检测未勾选框")
    time.sleep(1)
    utils.search_symbol_erroring(config.EXPORT_PUBLIC_PROGRAM_GRAY)
    pyautogui.press("enter")
    time.sleep(8)
    # 修改元件，点击返回
    for _ in range(6):
        pyautogui.press('down')
        time.sleep(0.5)
    utils.click_by_png(config.EDIT_BACK)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    utils.click_by_png(config.SAVE)
    time.sleep(1)
    logger.info("第三次检测未勾选框")
    utils.search_symbol_erroring(config.EXPORT_PUBLIC_PROGRAM_GRAY)
    time.sleep(3)
    pyautogui.press("enter")
    time.sleep(3)
    pyautogui.press("enter")
    time.sleep(5)
    # 傻逼用例描述 他妈的明明都是置灰无法勾选
    utils.click_by_png(config.TOOL_DARK)
    utils.click_by_png(config.SYNC_TO_PUBLIC_LIBS)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    if utils.check_new_data(config.SHARE_LIB_PATH):
        logger.info("共享元件库文件夹内有新数据生成")
    else:
        raise Exception("共享元件库文件夹内没有新数据生成")
    utils.close_aoi()


@utils.screenshot_error_to_excel()
def yjk_001_47():
    utils.check_and_launch_aoi()
    utils.check_share_lib_path(True)
    utils.check_default_export_auto_save(True, True)
    utils.ensure_in_edit_mode()
    # 修改元件 保存 是
    utils.modify_component()
    utils.click_by_png(config.SAVE)
    time.sleep(1)
    pyautogui.press("enter")
    # 修改元件 返回 是 保存 是
    time.sleep(3)
    utils.modify_component()
    utils.click_by_png(config.EDIT_BACK)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(3)
    utils.click_by_png(config.SAVE)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    # 傻逼用例描述
    utils.click_by_png(config.TOOL_DARK)
    utils.click_by_png(config.SYNC_TO_PUBLIC_LIBS)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    if utils.check_new_data(config.SHARE_LIB_PATH):
        logger.info("共享元件库文件夹内有新数据生成")
    else:
        raise Exception("共享元件库文件夹内没有新数据生成")
    utils.close_aoi()


# 勾共享元件库路径-最近编辑的样式
@utils.screenshot_error_to_excel()
def yjk_001_48():
    utils.check_and_launch_aoi()
    utils.check_share_lib_path(True)
    utils.check_default_export_auto_save(False, True)
    utils.ensure_in_edit_mode()
    # 修改元件，点击保存，手动勾选导出到公共元件库
    for _ in range(6):
        pyautogui.press('down')
        time.sleep(0.5)
    utils.click_by_png(config.SAVE)
    time.sleep(2)
    if utils.search_symbol(config.QUESTION_MARK):
        pyautogui.press("enter")
    time.sleep(1)
    utils.click_by_png(config.EXPORT_PUBLIC_PROGRAM)
    utils.click_by_png(config.YES)
    while utils.search_symbol(config.SAVING_PROGRAM):
        time.sleep(1)
    time.sleep(1)
    # 修改元件，切换元件，是，保存，手动勾选
    for _ in range(6):
        pyautogui.press('down')
        time.sleep(0.5)
    logger.error(2)
    utils.click_component()
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(3)
    utils.click_by_png(config.SAVE)
    time.sleep(1)
    utils.click_by_png(config.EXPORT_PUBLIC_PROGRAM)
    time.sleep(1)
    pyautogui.press("enter")
    # 修改元件，返回 是 保存 勾选
    for _ in range(6):
        pyautogui.press('down')
        time.sleep(0.5)
    logger.error(3)
    utils.click_by_png(config.EDIT_DARK)
    utils.click_by_png(config.EDIT_BACK)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(3)
    utils.click_by_png(config.SAVE)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    utils.click_by_png(config.TOOL_DARK)
    time.sleep(1)
    # 傻逼用例描述
    utils.click_by_png(config.SYNC_TO_PUBLIC_LIBS)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    if utils.check_new_data(config.SHARE_LIB_PATH):
        logger.info("共享元件库文件夹内有新数据生成")
    else:
        raise Exception("共享元件库文件夹内没有新数据生成")
    utils.close_aoi()



# 勾共享元件库路径
@utils.screenshot_error_to_excel()
def yjk_001_49():
    utils.check_and_launch_aoi()
    utils.check_share_lib_path(True)
    # 打开任一job,同步至公共元件库
    utils.open_program()
    pyautogui.press('enter')
    time.sleep(5)
    if utils.search_symbol(config.TOOL_DARK, 5):
        utils.click_by_png(config.TOOL_DARK)
    utils.click_by_png(config.SYNC_TO_PUBLIC_LIBS)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    pyautogui.press("enter")
    # 打开更早编辑的程式
    for i in range(2):
        utils.click_by_png(config.OPEN_PROGRAM)
        utils.click_by_png(config.OPEN_PROGRAM_RECENT)
        if i == 0:
            pyautogui.press('tab',6)
        if i == 1:
            pyautogui.press('tab',8)
        utils.click_by_png(config.OPEN_PROGRAM_CHOSED)
        utils.click_by_png(config.OPEN_PROGRAM_LOAD_1)
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
        utils.click_by_png(config.YES)
        logger.error(i)
        # 否，检测是否生成新数据
        utils.click_by_png(config.QUESTION_MARK)
        if i == 0:
            pyautogui.press("left")
            pyautogui.press("enter")
            logger.error(2)
            while utils.search_symbol(config.PROGRAM_LOADING):
                time.sleep(5)
            if not utils.check_new_data(config.SHARE_LIB_PATH):
                logger.info("共享元件库文件夹内没有新数据生成")
            else:
                raise Exception("共享元件库文件夹内有新数据生成")

        if i == 1:
            logger.error(3)
            pyautogui.press("enter")
            while utils.search_symbol(config.PROGRAM_LOADING):
                time.sleep(5)
            if utils.check_new_data(config.SHARE_LIB_PATH):
                logger.info("共享元件库文件夹内有新数据生成")
            else:
                raise Exception("共享元件库文件夹内没有新数据生成")
            utils.close_aoi()


@utils.screenshot_error_to_excel()
def yjk_001_50():
    utils.check_and_launch_aoi()
    utils.check_share_lib_path(True)
    # 先打开任一job，同步到公共元件库
    utils.ensure_in_edit_mode()
    utils.click_by_png(config.TOOL)
    utils.click_by_png(config.SYNC_TO_PUBLIC_LIBS)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    pyautogui.press("enter")
    # 再打开最近编辑的程式
    utils.click_by_png(config.OPEN_PROGRAM)
    pyautogui.press('enter')
    utils.click_by_png(config.OPEN_PROGRAM_RECENT)
    time.sleep(1)
    pyautogui.press('tab',4)
    utils.click_by_png(config.OPEN_PROGRAM_CHOSED)
    utils.click_by_png(config.OPEN_PROGRAM_LOAD_1, 2)
    utils.click_by_png(config.YES)
    # 检测是否生成新数据
    if utils.search_symbol(config.QUESTION_MARK):
        raise Exception("有弹框")
    else:
        logger.info("没有弹框")
    time.sleep(1)
    pyautogui.press("enter")
    if utils.check_new_data(config.SHARE_LIB_PATH):
        logger.info("共享元件库文件夹内有新数据生成")
    else:
        raise Exception("共享元件库文件夹内没有新数据生成")
    utils.close_aoi()


@utils.screenshot_error_to_excel()
def yjk_001_51():
    utils.check_and_launch_aoi()
    utils.check_share_lib_path(True)
    utils.ensure_in_edit_mode()
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.IMPORT_ALL_PN)
    time.sleep(3)
    pyautogui.click((945, 525))
    utils.click_by_png(config.PUBLIC_ELEMENTS)
    pyautogui.press('enter')
    utils.search_symbol_erroring(config.IMPORTING_ELEMENTS)
    utils.close_aoi()


# 测试=============================
# # TODO 需要在线版才可以
# @utils.screenshot_error_to_excel()
# def yjk_001_52():
#     pass
