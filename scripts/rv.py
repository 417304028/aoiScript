import pyperclip
import utils
import config
import re
from pywinauto import Application,Desktop
from loguru import logger
# ai复判 传入json（可能一组json 有大概七八个参数），传出json（海建给的）
def rv_ai_test(path):
    status = 1
    # 训练所在文件夹的路径加入剪切板
    pyperclip.copy(path)
    # 前置程序（假定程序已打开）
    windows = Desktop(backend="uia").windows()
    window_found = False
    pattern = re.compile(r".*Sinictek-训练.*")  # 正则表达式匹配包含 "Sinictek-训练" 的标题
    sinictek_amount = 0
    for w in windows:
        if pattern.match(w.window_text()):
            window_properties = w.get_properties()
            logger.info(f"'Sinictek-训练'窗口存在,详细信息：{window_properties}")
            window_found = True
            sinictek_amount += 1
    logger.info(f"'Sinictek-训练'窗口数量: {sinictek_amount}")
    if window_found:
        app = Application().connect(title_re=".*Sinictek-训练.*")
        main_window = app.window(title_re="Sinictek-训练")
        if main_window.exists(timeout=10):
            logger.info("成功连接到窗口")
            main_window.wait('ready', timeout=10)
            main_window.set_focus()
            main_window.wait('ready', timeout=10)
        else:
            status = -1
            logger.error("未找到窗口")
            raise Exception("未找到窗口")
    else:
        status = -1
        logger.error("未找到程序")
        raise Exception("未找到程序")
    # 点击程序里的训练
    if utils.search_symbol_erroring(config.RV_TOPIC):
        logger.info("识别到窗口标题")
    # 点击训练按钮
    utils.click_by_png(config.RV_SIMULATE_TO_TRAIN)
    # 训练完查看训练状态，删除选中元件，再进行下批训练，推理也同样 生成结果都在同个文件夹
    utils.
    

    utils.click_by_png(config.RV_SIMULATE_TO_TRAIN)
    return status
