from utils import logger
from scripts import lxbj, yjk
from utils import if_checked
import pyautogui

def main():
    # 创建一个函数列表
    lxbj_functions = [
        # lxbj.lxbj_001_01, lxbj.lxbj_002_01, lxbj.lxbj_003_01, lxbj.lxbj_004_04, lxbj.lxbj_004_05, lxbj.lxbj_004_06,
        # lxbj.lxbj_005_01, lxbj.lxbj_005_02, lxbj.lxbj_005_03, lxbj.lxbj_005_04,
        # lxbj.lxbj_007_01, lxbj.lxbj_007_02, lxbj.lxbj_008_01, lxbj.lxbj_008_02,
        # lxbj.lxbj_010_01, lxbj.lxbj_010_02, lxbj.lxbj_010_03, lxbj.lxbj_010_04, lxbj.lxbj_011_01,
        # lxbj.lxbj_012_03, lxbj.lxbj_012_04, lxbj.lxbj_013_01, lxbj.lxbj_013_02, lxbj.lxbj_013_03
        lxbj.lxbj_007_01, lxbj.lxbj_007_02, lxbj.lxbj_008_01, lxbj.lxbj_008_02,
        lxbj.lxbj_010_01, lxbj.lxbj_010_02, lxbj.lxbj_010_03, lxbj.lxbj_010_04, lxbj.lxbj_011_01,
        lxbj.lxbj_012_03, lxbj.lxbj_012_04, lxbj.lxbj_013_01, lxbj.lxbj_013_02, lxbj.lxbj_013_03
    ]
    # yjk_functions = [
    #     yjk.yjk_001_43, yjk.yjk_001_44, yjk.yjk_001_45, yjk.yjk_001_46, yjk.yjk_001_47, yjk.yjk_001_48, yjk.yjk_001_49
    # ]
    # yjk_functions = [
    #     yjk.yjk_001_47, yjk.yjk_001_48, yjk.yjk_001_49
    # ]
    # 依次执行每个函数
    for func in lxbj_functions:
        try:
            logger.info(f"目前执行到 {func.__name__} 方法")
            pyautogui.alert(f"目前执行到 {func.__name__} 方法", timeout=3000)
            func()
        except Exception as e:
            logger.error(f"执行 {func.__name__} 时遇到错误: {e}")

if __name__ == "__main__":
    main()