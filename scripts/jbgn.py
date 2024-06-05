import config
import utils
import time
import pyautogui
import pytesseract
from PIL import ImageGrab

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
        pyautogui.click(544,292)
        program_bbox = (535, 300, 920, 555)
        program_loaded_bbox = (1000, 280, 1380, 550)
        # 程式列表-主目录程式下任选一个，确保右边空的才双击
        plus_program = config.OPEN_PROGRAM_PLUS
        cursor_program = config.OPEN_PROGRAM_CURSOR
        plus_exist = utils.check_load_program(plus_program, program_bbox, program_loaded_bbox)
        cursor_exist = utils.check_load_program(cursor_program, program_bbox, program_loaded_bbox)
        if not plus_exist and not cursor_exist:
            raise Exception("程式都不存在，怎么个事")
        # 重复步骤 打开——至——取消 三次后 点击确定按钮
        if i < 2:
            # 确定弹窗存在
            utils.search_symbol(config.OPEN_PROGRAM_TOPIC, 5)
            # 点击取消
            utils.click_button(config.OPEN_PROGRAM_NO, 1)
            # 确定返回之前的整版视图
            utils.search_symbol(config.WHOLE_BOARD_LIGHT, 10)
        else:
            utils.click_button(config.OPEN_PROGRAM_YES, 1)
            # 有进度条提示
            utils.search_symbol(config.PROGRAM_LOADING, 30)
            # 确定加载后
            utils.search_symbol(config.PROGRAM_COMPONENT_DARK, 5)
            # 无闪退
            utils.search_symbol(config.AOI_TOPIC, 5)

@utils.screenshot_error_to_excel
def jbgn_001_02():
    utils.check_and_launch_aoi()
    utils.click_button(config.OPEN_PROGRAM, 1)
    directory = r"D:\EYAOI\JOB"
    bbox = (640, 190, 719, 203)
    utils.text_in_bbox(directory, bbox)


    utils.click_button(config.OPEN_PROGRAM_YES)


@utils.screenshot_error_to_excel
def jbgn_001_03():
    utils.check_and_launch_aoi()
    utils.click_button(config.OPEN_PROGRAM, 1)
    directory = r"D:\EYAOI\JOB"
    bbox = (640, 190, 719, 203)
    utils.text_in_bbox(directory, bbox)
    


    utils.click_button(config.OPEN_PROGRAM_YES)

@utils.screenshot_error_to_excel
def jbgn_001_04():
    utils.check_and_launch_aoi()
    utils.click_button(config.OPEN_PROGRAM, 1)
    directory = r"D:\EYAOI\JOB"
    bbox = (640, 190, 719, 203)
    program_loaded_bbox = (1000, 280, 1380, 550)
    utils.text_in_bbox(directory, bbox)
    cursor_exist = utils.search_symbol(config.OPEN_PROGRAM_CURSOR)
    if cursor_exist:
        utils.click_button(config.OPEN_PROGRAM_CURSOR, 2)
        load_success = utils.search_symbol(config.OPEN_PROGRAM_CURSOR, None, program_loaded_bbox)
        if not load_success:
            raise Exception("指针程式没加载成功")
        utils.click_button(config.REMOVE_PROGRAM)
          
    plus_exist = utils.search_symbol(config.OPEN_PROGRAM_PLUS)
    if plus_exist:
        utils.click_button(config.OPEN_PROGRAM_PLUS, 2)
        load_success = utils.search_symbol(config.OPEN_PROGRAM_PLUS, None, program_loaded_bbox)
        if not load_success:
            raise Exception("指针程式没加载成功")
    if not plus_exist and not cursor_exist:
        raise Exception("程式都不存在，怎么个事")  
    
