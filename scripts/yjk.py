import utils
import config
import pyautogui
import os
import time
from loguru import logger

# 不勾共享元件库路径
@utils.screenshot_to_excel
def yjk_001_43():
    # 先打开并前置aoi
    utils.check_and_launch_aoi()
    # 选任一元件，双击进入编辑界面（确保在编辑界面）
    utils.ensure_in_edit_mode()
    # 查看共享元件库路径【设置】-【硬件设置】-【数据导出配置】-【共享元件库路径】路径基本不变，因此我路径先用绝对路径了
    # utils.read_text(config.SHARE_LIB_PATH_COORDINATE)
    # 不勾选
    utils.check_share_lib_path(False)
    # 修改元件
    utils.modify_component()
    # 点击保存按钮，查看弹窗是否隐藏（导出到公共元件库）
    utils.click_by_png(config.SAVE)
    pyautogui.press("enter")
    # 检查是否置灰
    if_grey = utils.search_symbol(config.EXPORT_PUBLIC_PROGRAM)
    if if_grey:
        pyautogui.press("enter")
        logger.info("置灰")
    else:
        pyautogui.press("enter")
        raise Exception("共享元件库未置灰")
    # 确保共享文件库文件夹内没有新数据生成
    if not utils.check_new_data(config.SHARE_LIB_PATH):
        raise Exception("共享元件库文件夹内有新数据生成")
# 不勾共享元件库路径
@utils.screenshot_to_excel
def yjk_001_44():
    utils.check_and_launch_aoi()
    utils.check_share_lib_path(False)
    utils.ensure_in_edit_mode()
    # 点击菜单栏-工具-同步到公共元件库
    utils.click_by_png(config.TOOL)
    utils.click_by_png(config.SYNC_TO_PUBLIC_LIBS)
    # 检测到提示框
    utils.search_symbol_erroring(config.PLEASE_OPEN_PUBLIC_LIBS)
    pyautogui.press("enter")

# 勾共享元件库路径
@utils.screenshot_to_excel
def yjk_001_45():
    utils.check_and_launch_aoi()
    utils.check_share_lib_path(True)
    utils.ensure_in_edit_mode()
    # 公共文件库默认一样的，删除库内所有数据
    utils.delete_documents(config.SHARE_LIB_PATH)
    # 修改元件，左侧列表切换元件，弹框点击是(有数据生成)
    utils.modify_component()
    utils.click_component()
    pyautogui.press("enter")
    if utils.check_new_data(config.SHARE_LIB_PATH):
        logger.info("共享元件库文件夹内有新数据生成")
    else:
        raise Exception("共享元件库文件夹内没有新数据生成")
    # 修改元件，点击返回，弹框点击是(有数据生成)
    utils.modify_component()
    utils.click_by_png(config.EDIT_BACK_BUTTON)
    pyautogui.press("enter")
    if utils.check_new_data(config.SHARE_LIB_PATH):
        logger.info("共享元件库文件夹内有新数据生成")
    else:
        raise Exception("共享元件库文件夹内没有新数据生成")
    # 查看共享元件库路径【设置】-【硬件设置】-【数据导出配置】-【共享元件库路径】
    # 看文件夹干嘛 又没任何作用 也没写任何期待结果 放着了
    # 查看共享元件库文件夹


# 勾共享元件库路径
@utils.screenshot_to_excel
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
    utils.click_by_png(config.EDIT_BACK_BUTTON)
    pyautogui.press("left")
    pyautogui.press("enter")
    if not utils.check_new_data(config.SHARE_LIB_PATH):
        logger.info("共享元件库文件夹内没有新数据生成")
    else:
        raise Exception("共享元件库文件夹内有新数据生成")
    # 查看共享元件库路径【设置】-【硬件设置】-【数据导出配置】-【共享元件库路径】
    # 没啥鸟用 不开发
    # 打开共享元件库文件夹

# TODO 勾共享元件库路径  注意得和48 49顺序运行
@utils.screenshot_to_excel
def yjk_001_47():
    utils.check_and_launch_aoi()
    utils.check_share_lib_path(True)
    # 打开一个最近编辑过的程式。逻辑：把获取到的程式坐标存起来，取最上面的一个坐标，点击
    utils.click_by_png(config.OPEN_PROGRAM)
    topest = utils.get_topest_program()
    pyautogui.doubleClick(topest)
    utils.click_by_png(config.OPEN_PROGRAM_YES)
    # 打开共享元件库文件夹，全选删除数据
    utils.delete_documents(config.SHARE_LIB_PATH)
    # 点击菜单栏-【工具】-【同步到公共元件库】，弹框点否，查看共享元件库文件夹（没有数据生成）
    utils.click_by_png(config.TOOL)
    utils.click_by_png(config.SYNC_TO_PUBLIC_LIBS)
    pyautogui.press("left")
    pyautogui.press("enter")
    if not utils.check_new_data(config.SHARE_LIB_PATH):
        logger.info("共享元件库文件夹内没有新数据生成")
    else:
        raise Exception("共享元件库文件夹内有新数据生成")
    # 点击菜单栏-【工具】-【同步到公共元件库】，弹框点是
    utils.click_by_png(config.SYNC_TO_PUBLIC_LIBS)
    pyautogui.press("enter")
    # 弹出UI显示消息，点击确定，查看共享元件库文件夹，弹框和文件夹 对比料号数量和是否一致（弹ui显示消息，且一致）
    

# TODO 勾共享元件库路径
@utils.screenshot_to_excel
def yjk_001_48():
    utils.check_and_launch_aoi()
    utils.check_share_lib_path(True)
    # 打开一个更早之前编辑的程式
    utils.click_by_png(config.OPEN_PROGRAM)
    topest = utils.get_topest_program()
    pyautogui.click(topest)
    pyautogui.press('down')
    utils.click_by_png(config.OPEN_PROGRAM_YES)
    # 弹出是否要从公共元件库中同步如下料号，点否或叉

    # 弹出是否要从公共元件库中同步如下料号，点是

    # 再次打开刚刚的job     （不会弹出 是否要从公共元件库中同步的提示框）

    # 打开更新编辑过的job   （不会弹出 是否要从公共元件库中同步的提示框）



# TODO 勾共享元件库路径
@utils.screenshot_to_excel
def yjk_001_49():
    utils.check_and_launch_aoi()
    # 打开任一job，任选一元件，进入离线编辑界面             有显示 共享元件库
    utils.open_program()
    utils.ensure_in_edit_mode()
    utils.search_symbol(config.SHARE_LIB_PATH)
    # 菜单栏-【元件库】，点击【导入当前料号】或【导入所有】    相同料号，从共享元件库导入job
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.ELEMENTS_IMPORT_ALL)
    # TODO 下拉框选第一个共享元件库，点击是
    utils.click_by_png(config.ELEMENTS_STANDARD_LIBRARY)
    pyautogui.press("enter")

