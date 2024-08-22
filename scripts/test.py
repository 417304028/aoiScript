import random
import utils
import config
import pyautogui
import time
from loguru import logger

# monkey test 遍历程式以及元件，测试aoi会不会出问题
@utils.screenshot_error_to_excel
def test_aoi():
    utils.check_and_launch_aoi()
    utils.delete_documents(config.SHARE_LIB_PATH)
    while True:
        # 随机点开程式
        utils.random_open_program()
        time.sleep(5)
        # 打开程式时会有个加载框，检测加载框是否存在，框没了再找程式元件栏
        while True:
            if not utils.search_symbol(config.PROGRAM_LOADING, 10, tolerance=0.8):
                break
            time.sleep(3)
        if utils.search_symbol(config.PROGRAM_COMPONENT_DARK, 30, tolerance=0.8):
            utils.click_by_png(config.PROGRAM_COMPONENT_DARK, tolerance=0.8)
        time.sleep(5)

        # 遍历所有元件，点完五个component并修改参数后滑轮下滑
        component_count = 0
        while True:
            a = pyautogui.screenshot(region=config.BOARD_SCROLLBAR_REGION) 
            if not utils.click_component():
                raise Exception("程式元件面板无程式元件")
            if utils.search_symbol(config.IF_MODIFY_COMPONENT_NO, 4):
                utils.click_by_png(config.IF_MODIFY_COMPONENT_NO, tolerance=0.9)
            # 随机修改参数
            param = random.choice([1, 2, 3, 4])
            utils.random_change_param(param)
            # if param != 4:
            # 下滑并确认是否到达底部
            component_count += 1
            if component_count >= 5:
                # 滚轮下滚
                pyautogui.moveTo(60, 300)
                pyautogui.click()
                time.sleep(3)
                pyautogui.scroll(-200)
                b = pyautogui.screenshot(region=config.BOARD_SCROLLBAR_REGION)
                if a == b:
                    logger.error("滚元件列表时，疑似到底了，开始打开下一个程式")
                    break
                component_count = 0  # 重置计数器，继续处理下一批五个元件
            # else:
            #     # 测试的是整版，因为识别问题，直接打开下一个程式
            #     break
