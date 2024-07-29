from utils import logger
import config
import pyautogui
import utils

if __name__ == '__main__':
    utils.setup_logger()
    logger.info("程序开始运行")
    try:
        region = (170, 290, 161, 314)

        position = pyautogui.locateOnScreen(config.TEST, region=region)
        if position:
            # 点击图片中心
            center_x, center_y = position.left + position.width // 2, position.top + position.height // 2
            pyautogui.click(center_x, center_y)
            logger.info(f"找到图片并点击中心点: (X: {center_x}, Y: {center_y})")
        else:
            logger.info("在指定区域未找到任何图片")
    except Exception as e:
        logger.error(f"在指定区域搜索图片时发生错误: {e}")
