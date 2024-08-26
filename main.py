import config, cv2, time
from utils import logger, check_chip_coverage, setup_logger, click_by_png, if_checked
from scripts import yjk
from scripts import test

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
    yjk_functions = [
        # yjk.yjk_001_42,
        # yjk.yjk_001_43,
        # yjk.yjk_001_44,
        # yjk.yjk_001_45,
        # yjk.yjk_001_46,
        # yjk.yjk_001_47,
        # yjk.yjk_001_48,
        # yjk.yjk_001_49,
        # yjk.yjk_001_50,
        yjk.yjk_001_51,
    ]
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
    main()
    # test.test_aoi()