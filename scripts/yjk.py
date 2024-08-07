import utils
import config
import pyautogui
import time
from loguru import logger

# 不勾共享元件库路径
@utils.screenshot_error_to_excel
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
        raise Exception("共享元件库文件夹内有新数据生成")
# 不勾共享元件库路径
@utils.screenshot_error_to_excel
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

# 勾共享元件库路径
@utils.screenshot_error_to_excel
def yjk_001_45():
    utils.check_and_launch_aoi()
    utils.check_share_lib_path(True)
    utils.ensure_in_edit_mode()
    # 公共文件库默认一样的，删除库内所有数据
    utils.delete_documents(config.SHARE_LIB_PATH)
    # 修改元件，左侧列表切换元件，弹框点击是(有数据生成)
    utils.modify_component()
    utils.click_by_png(config.SAVE)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    utils.click_by_png(config.EXPORT_PUBLIC_PROGRAM)
    time.sleep(1)
    pyautogui.press("enter")
    utils.modify_component()
    utils.click_component()
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(2)
    if utils.check_new_data(config.SHARE_LIB_PATH):
        logger.info("共享元件库文件夹内有新数据生成")
    else:
        raise Exception("共享元件库文件夹内没有新数据生成")
    # 修改元件，点击返回，弹框点击是(有数据生成)
    utils.modify_component()
    utils.click_by_png(config.EDIT_BACK)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(2)
    if utils.check_new_data(config.SHARE_LIB_PATH):
        logger.info("共享元件库文件夹内有新数据生成")
    else:
        raise Exception("共享元件库文件夹内没有新数据生成")
    # 查看共享元件库路径【设置】-【硬件设置】-【数据导出配置】-【共享元件库路径】
    # 看文件夹干嘛 又没任何作用 也没写任何期待结果 放着了
    # 查看共享元件库文件夹


# 勾共享元件库路径
@utils.screenshot_error_to_excel
def yjk_001_46():
    utils.check_and_launch_aoi()
    utils.check_share_lib_path(True)
    utils.ensure_in_edit_mode()
    utils.delete_documents(config.SHARE_LIB_PATH)
    # 修改元件，点击左上角保存按钮，点击否或叉(没有数据生成)
    utils.modify_component()
    utils.click_by_png(config.SAVE)
    pyautogui.press("left")
    pyautogui.press("enter")
    if not utils.check_new_data(config.SHARE_LIB_PATH):
        logger.info("共享元件库文件夹内没有新数据生成")
    else:
        raise Exception("共享元件库文件夹内有新数据生成")
    # 修改元件，左侧列表切换元件，（是否修改此元件）弹框点击否或叉 (没有数据生成)
    utils.modify_component()
    utils.click_component()
    pyautogui.press("left")
    pyautogui.press("enter")
    if not utils.check_new_data(config.SHARE_LIB_PATH):
        logger.info("共享元件库文件夹内没有新数据生成")
    else:
        raise Exception("共享元件库文件夹内有新数据生成")
    # 修改元件，点击返回，（是否修改此元件）弹框点击否 (没有数据生成)
    utils.modify_component()
    utils.click_by_png(config.EDIT_BACK)
    pyautogui.press("left")
    pyautogui.press("enter")
    if not utils.check_new_data(config.SHARE_LIB_PATH):
        logger.info("共享元件库文件夹内没有新数据生成")
    else:
        raise Exception("共享元件库文件夹内有新数据生成")
    # 查看共享元件库路径【设置】-【硬件设置】-【数据导出配置】-【共享元件库路径】
    # 没啥鸟用 不开发
    # 打开共享元件库文件夹

# 勾共享元件库路径-更早之前编辑的样式       （需要打开程式-最近编辑至少有一个程式）
@utils.screenshot_error_to_excel
def yjk_001_47():
    utils.check_and_launch_aoi()
    utils.check_share_lib_path(True)
    start = utils.check_data_amount(config.SHARE_LIB_PATH)
    for i in range(2):
        # 打开任一job,同步至公共元件库
        utils.open_program()
        pyautogui.press('enter')
        time.sleep(5)
        utils.search_symbol(config.TOOL)
        utils.click_by_png(config.TOOL)
        utils.search_symbol(config.SYNC_TO_PUBLIC_LIBS)
        utils.click_by_png(config.SYNC_TO_PUBLIC_LIBS)
        # 选中和非选中时的确认按钮样式不同，需要换个方式
        utils.click_by_png(config.UI_SHOW_MESSAGE)
        pyautogui.press('tab')
        pyautogui.press('enter')
        # 打开更早编辑的程式
        utils.click_by_png(config.OPEN_PROGRAM)
        pyautogui.press('enter')
        utils.click_by_png(config.OPEN_PROGRAM_RECENT)
        pyautogui.press('tab',4)
        utils.click_by_png(config.OPEN_PROGRAM_LOAD)
        utils.click_by_png(config.OPEN_PROGRAM_YES)
        # 弹框选否
        if i == 0:
            if utils.search_symbol_erroring(config.IF_SYNC_PART_NO):
                pyautogui.press("left")
                pyautogui.press("enter")
                now = utils.check_data_amount(config.SHARE_LIB_PATH)
                if now == start:
                    logger.info("共享元件库文件夹内没有新数据生成")
                if now != start:
                    logger.error("共享元件库文件夹内有新数据生成")
                    raise Exception("共享元件库文件夹内有新数据生成")
        if i == 1:
             if utils.search_symbol_erroring(config.IF_SYNC_PART_NO):
                pyautogui.press("enter")
                now = utils.check_data_amount(config.SHARE_LIB_PATH)
                if now != start:
                    logger.info("共享元件库文件夹内有新数据生成")
                if now == start:
                    logger.error("共享元件库文件夹内没有新数据生成")
                    raise Exception("共享元件库文件夹内没有新数据生成")

# 勾共享元件库路径-最近编辑的样式
@utils.screenshot_error_to_excel
def yjk_001_48():
    utils.check_and_launch_aoi()
    utils.check_share_lib_path(True)
    start = utils.check_data_amount()
    utils.open_program()
    utils.click_by_png(config.TOOL)
    utils.click_by_png(config.SYNC_TO_PUBLIC_LIBS)
    utils.click_by_png(config.UI_SHOW_MESSAGE)
    pyautogui.press('tab')
    pyautogui.press('enter')
    utils.click_by_png(config.OPEN_PROGRAM)
    utils.click_by_png(config.OPEN_PROGRAM_RECENT)
    # 最近编辑的至少有俩
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    utils.click_by_png(config.OPEN_PROGRAM_LOAD)
    utils.click_by_png(config.OPEN_PROGRAM_YES)
    if utils.search_symbol(config.IF_SYNC_PART_NO):
        raise Exception("有不希望看到的弹框生成")
    now = utils.check_amount_content()
    if now != start:
        logger.info("共享元件库文件夹内有新数据生成")
    if now == start:
        logger.error("共享元件库文件夹内没有新数据生成")
        raise Exception("共享元件库文件夹内没有新数据生成")



# 勾共享元件库路径
@utils.screenshot_error_to_excel
def yjk_001_49():
    utils.check_and_launch_aoi()
    # 打开任一job，任选一元件，进入离线编辑界面             
    utils.open_program()
    utils.ensure_in_edit_mode()
    # 菜单栏-【元件库】，点击【导入当前料号】或【导入所有】   
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.ELEMENTS_IMPORT_ALL)
    # 下拉框选第一个共享元件库，点击是         
    # TODO 有显示 共享元件库     相同料号，从共享元件库导入job(识别加载进度条上方的数字吗？个/十/百的数字坐标都不同，有哪个地方可以看导入了多少元件)
    utils.click_by_png(config.ELEMENTS_DEFAULT)
    utils.click_by_png(config.PUBLIC_ELEMENTS)
    pyautogui.press("enter")

