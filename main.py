import config, cv2, time
from utils import logger, search_symbol, setup_logger, click_color, count_color_in_range, read_text_ocr, get_frame_points
from scripts import yjk
from scripts import test
import importlib
import pyautogui


def main():
    # 创建一个函数列表
    # lxbj_functions = [
    #     lxbj.lxbj_001_01, lxbj.lxbj_002_01, lxbj.lxbj_003_01, lxbj.lxbj_004_04, lxbj.lxbj_004_05, lxbj.lxbj_004_06,
    #     lxbj.lxbj_005_01, lxbj.lxbj_005_02, lxbj.lxbj_005_03, lxbj.lxbj_005_04,
    #     lxbj.lxbj_007_01, lxbj.lxbj_007_02, lxbj.lxbj_008_01, lxbj.lxbj_008_02,
    #     lxbj.lxbj_010_01, lxbj.lxbj_010_02, lxbj.lxbj_010_03, lxbj.lxbj_010_04, lxbj.lxbj_011_01,
    #     lxbj.lxbj_012_03, lxbj.lxbj_012_04, lxbj.lxbj_013_01, lxbj.lxbj_013_02, lxbj.lxbj_013_03,
    #     lxbj.lxbj_014_01, lxbj.lxbj_014_02, lxbj.lxbj_014_03, lxbj.lxbj_014_04, lxbj.lxbj_014_05,
    #     lxbj.lxbj_014_06, lxbj.lxbj_014_07, lxbj.lxbj_014_08, lxbj.lxbj_014_09, lxbj.lxbj_014_10,
    #     lxbj.lxbj_014_11, lxbj.lxbj_014_12, lxbj.lxbj_015_01, 
    #     lxbj.lxbj_016_01, lxbj.lxbj_016_02, lxbj.lxbj_016_03, lxbj.lxbj_016_04, lxbj.lxbj_016_05,
    #     lxbj.lxbj_017_01, lxbj.lxbj_018_01, lxbj.lxbj_018_02, lxbj.lxbj_018_03, lxbj.lxbj_018_04,
    # ]



    yjk_module = importlib.import_module('scripts.yjk')
    yjk_functions = [getattr(yjk_module, func) for func in dir(yjk_module) if callable(getattr(yjk_module, func)) and func.startswith('yjk_')]
    
    # 依次执行每个函数
    for func in yjk_functions:
        try:
            logger.info(f"目前执行到 {func.__name__} 方法")
            pyautogui.alert(f"目前执行到 {func.__name__} 方法", timeout=3000)
            func()
        except Exception as e:
            logger.error(f"执行 {func.__name__} 时遇到错误: {e}")


if __name__ == "__main__":
    setup_logger()

    pyautogui.click(config.CENTRE)
    pyautogui.hotkey("ctrl", "a")
    a = count_color_in_range(config.CENTRE, 100, (0,0,255))
    pyautogui.hotkey("ctrl", "b")
    time.sleep(1)
    b = count_color_in_range(config.CENTRE, 100, (0,0,255))
    if b == a:
        raise Exception("切换本体(引脚)/窗口快捷键疑似无效")
    # black_pixel_count = 0
    # total_pixels = 0
    # screenshot = pyautogui.screenshot(region=config.COMPONENT_REGION)
    # for x in range(screenshot.width):
    #     for y in range(screenshot.height):
    #         if screenshot.getpixel((x, y)) == (0, 0, 0):
    #             black_pixel_count += 1
    #         total_pixels += 1
    # if total_pixels > 0:
    #     black_pixel_ratio = black_pixel_count / total_pixels * 100
    #     if black_pixel_ratio < 40:
    #         raise Exception("config.component_region内颜色为（0，0，0）的比例低于30%")
    #     else:
    #         logger.info(f"config.component_region内颜色为（0，0，0）的比例为{black_pixel_ratio}%")