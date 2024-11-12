import config, cv2, time
from utils import logger, write_text_textbox, setup_logger, get_color_in_region, scroll_down, click_by_png, expand_choose_box
from scripts import yjk
from scripts import test
import importlib
import pyautogui

if __name__ == "__main__":
    setup_logger()
    write_text_textbox(config.PARAM_ONLINE_PARAMETER_DISPLAY_SYNC_PACKAGE, "K", if_select_all=False)
    logger.info("end")