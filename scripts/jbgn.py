import utils
import time
import pyautogui
import config

@utils.screenshot_error_to_excel
# 3D AOI软件--基本功能测试用例
def jbgn_001_01():
    for i in range(3):
        # 确保aoi打开
        utils.check_and_launch_aoi()
        # 打开程式
        utils.click_button(config.OPEN_PROGRAM, 1)

        directory = r"D:\EYAOI\JOB"
        bbox = (640, 190, 719, 203)
        utils.text_in_bbox(directory, bbox)

        time.sleep(0.2)
        # 把最近打开程式收起来
        pyautogui.click(544, 292)
        program_bbox = (535, 300, 920, 555)
        program_loaded_bbox = (1000, 280, 1380, 550)
        # 双击任意程式
        cursor_exist = utils.check_load_program(config.OPEN_PROGRAM_CURSOR, program_bbox, program_loaded_bbox)
        if not cursor_exist:
            plus_exist = utils.check_load_program(config.OPEN_PROGRAM_PLUS, program_bbox, program_loaded_bbox)
            if not plus_exist:
                raise Exception("程式都不存在，可能文件夹下无可识别的程式")

        # 重复步骤 打开——至——取消 三次后 点击确定按钮
        if i < 2:
            # 确定弹窗存在
            utils.search_symbol_erroring(config.OPEN_PROGRAM_TOPIC, 5)
            # 点击取消
            utils.click_button(config.OPEN_PROGRAM_CANCEL, 1)
            time.sleep(0.2)
            print("开始确定无闪退")
            # 确定返回之前的整版视图
            utils.click_button(config.WHOLE_BOARD_LIGHT, 1)
            print("已确定无闪退")
            time.sleep(0.2)
        else:
            utils.click_button(config.OPEN_PROGRAM_YES, 1)
            # 有进度条提示
            utils.search_symbol_erroring(config.PROGRAM_LOADING, 30)
            # 确定加载后
            utils.search_symbol_erroring(config.PROGRAM_COMPONENT_DARK, 5)
            # 无闪退
            utils.search_symbol_erroring(config.AOI_TOPIC, 5)


@utils.screenshot_error_to_excel
def jbgn_001_02():
    utils.check_and_launch_aoi()
    utils.click_button(config.OPEN_PROGRAM, 1)
    directory = r"D:\EYAOI\JOB"
    bbox = (640, 190, 719, 203)
    utils.text_in_bbox(directory, bbox)

    time.sleep(0.2)
    # 把最近打开程式收起来
    pyautogui.click(544, 292)
    program_bbox = (535, 300, 920, 555)
    program_loaded_bbox = (1000, 280, 1380, 550)
    # 双击任意程式
    cursor_exist = utils.check_load_program(config.OPEN_PROGRAM_CURSOR, program_bbox, program_loaded_bbox)
    if not cursor_exist:
        plus_exist = utils.check_load_program(config.OPEN_PROGRAM_PLUS, program_bbox, program_loaded_bbox)
        if not plus_exist:
            raise Exception("程式都不存在，可能文件夹下无可识别的程式")
    utils.click_button(config.OPEN_PROGRAM_YES, 1)
    # 有进度条提示
    utils.search_symbol_erroring(config.PROGRAM_LOADING, 30)
    # 确定加载后
    utils.search_symbol_erroring(config.PROGRAM_COMPONENT_DARK, 5)
    # 无闪退
    utils.search_symbol_erroring(config.AOI_TOPIC, 5)


@utils.screenshot_error_to_excel
def jbgn_001_03():
    utils.check_and_launch_aoi()
    utils.click_button(config.OPEN_PROGRAM, 1)
    directory = r"D:\EYAOI\JOB"
    bbox = (640, 190, 719, 203)
    utils.text_in_bbox(directory, bbox)
    time.sleep(0.2)
    # 把最近打开程式收起来
    pyautogui.click(544, 292)
    program_bbox = (535, 300, 920, 555)
    program_loaded_bbox = (1000, 280, 1380, 550)
    # 找到左侧所有程式图标
    program_list = []
    exist_cursor = utils.search_symbol(config.OPEN_PROGRAM_CURSOR, None, program_bbox)
    exist_plus = utils.search_symbol(config.OPEN_PROGRAM_PLUS, None,program_bbox)
    if exist_cursor:
        program_list += list(pyautogui.locateAllOnScreen(config.OPEN_PROGRAM_CURSOR, region=program_bbox))
    if exist_plus:
        program_list += list(pyautogui.locateAllOnScreen(config.OPEN_PROGRAM_PLUS, region=program_bbox))
    if not program_list:
        raise Exception("疑似程式文件夹/程式文件未加载")
    for program in program_list:
        time.sleep(0.5)
        # 双击程式图标
        pyautogui.doubleClick(program)
        time.sleep(2)  # 等待加载
        # 检查右侧是否加载了相应的程式, 找不到自然会报错
        if exist_cursor:
            pyautogui.locateOnScreen(config.OPEN_PROGRAM_PLUS, region=program_loaded_bbox)
        if exist_plus:
            pyautogui.locateOnScreen(config.OPEN_PROGRAM_PLUS, region=program_loaded_bbox)
    utils.click_button(config.OPEN_PROGRAM_YES, 1)
    # 有进度条提示
    utils.search_symbol_erroring(config.PROGRAM_LOADING, 30)
    # 确定加载后
    utils.search_symbol_erroring(config.PROGRAM_COMPONENT_DARK, 5)
    # 无闪退
    utils.search_symbol_erroring(config.AOI_TOPIC, 5)


@utils.screenshot_error_to_excel
def jbgn_001_04():
    utils.check_and_launch_aoi()
    utils.click_button(config.OPEN_PROGRAM, 1)
    directory = r"D:\EYAOI\JOB"
    bbox = (640, 190, 719, 203)
    program_loaded_bbox = (1000, 280, 1380, 550)
    utils.text_in_bbox(directory, bbox)
    time.sleep(0.2)
    # 把最近打开程式收起来
    pyautogui.click(544, 292)
    program_bbox = (535, 300, 920, 555)
    program_loaded_bbox = (1000, 280, 1380, 550)
    # 双击任一指针程式，确保在右边之后，点击右边的程式，点击移除
    cursor_load = utils.check_load_program(config.OPEN_PROGRAM_CURSOR, program_bbox, program_loaded_bbox)
    if cursor_load:
        loaded_cursor = pyautogui.locateCenterOnScreen(config.OPEN_PROGRAM_CURSOR, region=program_loaded_bbox)
        pyautogui.click(loaded_cursor)
        utils.click_button(config.REMOVE_PROGRAM, 1)
        if utils.search_symbol(config.OPEN_PROGRAM_CURSOR, None, program_loaded_bbox):
            raise Exception("指针程式移除失败")
        else:
            print("移除指针程式成功")
    # 左边没指针程式，尝试处理＋号程式
    elif not cursor_load:
        cursor_load = utils.check_load_program(config.OPEN_PROGRAM_PLUS, program_bbox, program_loaded_bbox)
        if cursor_load:
            loaded_plus = pyautogui.locateCenterOnScreen(config.OPEN_PROGRAM_PLUS, region=program_loaded_bbox)
            pyautogui.click(loaded_plus)
            utils.click_button(config.REMOVE_PROGRAM, 1)
            if utils.search_symbol(config.OPEN_PROGRAM_PLUS, None, program_loaded_bbox):
                raise Exception("＋号程式移除失败")
            else:
                print("移除＋号程式成功")
        else:
            raise Exception("左边没有任何程式")
    else:
        raise Exception("程式都不存在，可能文件夹下无可识别的程式")

