import random
import time
from loguru import logger
import pyautogui
import pyperclip
import config
import utils
import shutil
import os

# TODO 需要在线版aoi
# @utils.screenshot_error_to_excel()
# # 复制元件
# def lxbj_001_01():
    # utils.check_and_launch_aoi()
    # utils.check_cross_component_copy()
    # # 新建程式元件 选择保存目录 指定导入文件 输入程式名称，是   
    # utils.click_by_png(config.NEW_PROGRAM_COMPONENT)
    # # 在整板影像界面，完成扫描整板（弹窗提示是否导入默认元件库）

    # # 否 不导入默认元件库(存在弹框提示)

    # # 不同类型元件手动添加检测窗口，须添加所有算法窗口

    # # 元件复制，黏贴在同一类型的元件

    # # 导出所有元件OK图
    # utils.click_by_png(config.EXPORT_COMPONENT_OK)
    # # 运行 程式(不闪退)
    # utils.click_by_png(config.RUN)
    # pass


# 查看RV，SRC上元件窗口，结果值 正常显示
@utils.screenshot_error_to_excel()
# 添加待料
def lxbj_002_01():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    utils.add_window()
    time.sleep(1)
    # 选择含有待料的窗口 如图像匹配
    utils.click_by_png(config.ADD_CHECKED_SENIOR)
    utils.click_by_png(config.IMAGE_MATCHING)
    utils.click_by_png(config.YES)
    time.sleep(3)
    # 图像处理框
    # utils.click_by_png(config.YES)
    # utils.click_by_png(config.IMAGE_CLOSE)
    # 添加标准影像
    # 加五种随机不同光源的待料 需确认添加成功
    for _ in range(5):
        if utils.search_symbol(config.ADD_STANDARD_IMAGE):
            utils.click_by_png(config.ADD_STANDARD_IMAGE)
        utils.random_choose_light()
        if utils.search_symbol(config.YES):
            utils.click_by_png(config.YES)
        if utils.search_symbol(config.IMAGE_CLOSE):
            utils.click_by_png(config.IMAGE_CLOSE)
    utils.random_change_image_param()
    if utils.search_symbol(config.PALETTE_EMPTY):
        raise Exception("添加标准影像失败")
    utils.click_by_png(config.TEST_WINDOW)
    time.sleep(3)
    # 设置超时时间（单位：秒）
    timeout_seconds = 600  # 可以根据需要调整超时时间

    # 点击TEST_COMPONENT并等待TESTING_COMPONENT消失或超时
    utils.click_by_png(config.TEST_COMPONENT)
    start_time = time.time()  # 记录开始时间
    while utils.search_symbol(config.TESTING_COMPONENT):
        if time.time() - start_time > timeout_seconds:
            raise Exception("测试元件等待超时")
            break  # 超时后跳出循环
        time.sleep(1)

    time.sleep(1)

    # 点击TEST_GROUP并等待TESTING_COMPONENT消失或超时
    utils.click_by_png(config.TEST_GROUP)
    start_time = time.time()  # 重新记录开始时间
    while utils.search_symbol(config.TESTING_COMPONENT):
        if time.time() - start_time > timeout_seconds:
            raise Exception("测试组等待超时")
            break  # 超时后跳出循环
        time.sleep(1)

    time.sleep(1)

    # 点击TEST_BOARD并等待TESTING_COMPONENT消失或超时
    utils.click_by_png(config.TEST_BOARD)
    start_time = time.time()  # 重新记录开始时间
    while utils.search_symbol(config.TESTING_COMPONENT):
        if time.time() - start_time > timeout_seconds:
            raise Exception("测试板等待超时")
            break  # 超时后跳出循环
        time.sleep(1)

    time.sleep(1)

    # 调用卡顿或闪退检测函数
    utils.caton_or_flashback("AOI.exe")
    utils.close_aoi()

# # TODO 可以识别出提示，但是没办法跟缺陷名对应
# # 不良窗口/元件
# @utils.screenshot_error_to_excel()
# def lxbj_003_01():
#     utils.check_and_launch_aoi()
#     utils.ensure_in_edit_mode()
#     time.sleep(2)
#     pyautogui.press('b')
#     # 不良窗口，红字提示：检测窗口 缺陷名称（左侧窗口的缺陷名，如果左侧窗口的缺陷名是默认，取算法参数界面首个不良结果对应的缺陷名）
#     utils.click_by_png(config.TEST_WINDOW)
#     time.sleep(3)
#     # 不良元件，红字提示：元件 首个不良窗口的缺陷名称（左侧窗口的缺陷名，如果左侧窗口的缺陷名是默认，取算法参数界面首个不良结果对应的缺陷名）
#     utils.click_by_png(config.TEST_COMPONENT)
#     time.sleep(3)
#     utils.close_aoi()

# 返回不修改
@utils.screenshot_error_to_excel()
def lxbj_004_01():
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(False, False)
    utils.ensure_in_edit_mode()
    utils.add_window()
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    time.sleep(3)
    utils.random_change_param()
    utils.click_by_png(config.EDIT_BACK)
    utils.search_symbol_erroring(config.QUESTION_MARK)
    # 在提示框，不选【同步到相同的封装类型】，点击【否】
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO, 1):
        utils.click_by_png(config.NO)
    else:
        if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_YES, 1):
            utils.click_by_png(config.IF_SYNC_SAME_PACKAGE_YES)
            utils.click_by_png(config.NO)
        else:
            raise Exception("未发现提示框")
    utils.search_symbol_erroring(config.BOARD_AUTO, 10)
    utils.close_aoi()


# 不同步封装
@utils.screenshot_error_to_excel()
def lxbj_004_02():
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(False, False)
    utils.ensure_in_edit_mode()
    utils.add_window()
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    time.sleep(3)
    utils.random_change_param()
    utils.click_by_png(config.EDIT_BACK)
    utils.search_symbol_erroring(config.QUESTION_MARK)
    # 在提示框，不选【同步到相同的封装类型】，点击【是】
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO, 1):
        pyautogui.press('enter')
    else:
        if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_YES, 1):
            utils.click_by_png(config.IF_SYNC_SAME_PACKAGE_YES)
            pyautogui.press('enter')
        else:
            raise Exception("未发现提示框")
    # 相同封装的其他料号的元件窗口参数都相同
    utils.check_same_package_same_param(True)
    utils.close_aoi()


# 同步封装
@utils.screenshot_error_to_excel()
def lxbj_004_03():
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(False, False)
    utils.ensure_in_edit_mode()
    utils.add_window()
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    time.sleep(3)
    utils.random_change_param()
    utils.click_by_png(config.EDIT_BACK)
    utils.search_symbol_erroring(config.QUESTION_MARK)
    # 在提示框，选择【同步到相同的封装类型】，点击【是】
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_YES, 1):
        pyautogui.press('enter')
    else:
        if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO, 1):
            utils.click_by_png(config.IF_SYNC_SAME_PACKAGE_NO)
            pyautogui.press('enter')
        else:
            raise Exception("未发现提示框")
    utils.check_same_package_same_param(True)
    utils.close_aoi()


# 不同步封装 
@utils.screenshot_error_to_excel()
def lxbj_004_04():
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(True, False)
    utils.ensure_in_edit_mode()
    utils.add_window()
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    time.sleep(3)
    utils.random_change_param()
    utils.click_by_png(config.EDIT_BACK)
    utils.search_symbol_erroring(config.QUESTION_MARK)
    # 在提示框，点击【是】
    pyautogui.press('enter')
    utils.check_same_package_same_param(False)
    utils.close_aoi()


# 不同步封装
@utils.screenshot_error_to_excel()
def lxbj_004_05():
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(True, True)
    utils.ensure_in_edit_mode()
    utils.add_window()
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    time.sleep(3)
    utils.random_change_param()
    utils.click_by_png(config.EDIT_BACK)
    utils.search_symbol_erroring(config.QUESTION_MARK)
    # 在提示框，点击【是】
    pyautogui.press('enter')
    utils.check_same_package_same_param(False)
    utils.close_aoi()


# 同步封装
@utils.screenshot_error_to_excel()
def lxbj_004_06():
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(False, True)
    utils.ensure_in_edit_mode()
    utils.add_window()
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    time.sleep(3)
    utils.random_change_param()
    utils.click_by_png(config.EDIT_BACK)
    utils.search_symbol_erroring(config.QUESTION_MARK)
    # 在提示框，点击【是】
    # 弹框提示不勾默认选择【同步到相同的封装类型】
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_YES, 1):
        pyautogui.press('enter')
    else:
        if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO, 1):
            utils.click_by_png(config.IF_SYNC_SAME_PACKAGE_NO)
            pyautogui.press('enter')
        else:
            raise Exception("未发现提示框")
    pyautogui.press('enter')
    # 要确定相同封装其他料号的元件窗口算法参数未更新
    utils.check_same_package_same_param(False)
    utils.close_aoi()
    


# 导出元件ok图
@utils.screenshot_error_to_excel()
def lxbj_005_01():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 1、UI：参数配置--UI配置-程序设置：不选【导出元件OK图】、选择【导出所有元件OK图】
    utils.check_export_ok(True, False)
    utils.click_by_png(config.RUN_DARK)
    program_name = utils.read_text(110, 70)

    # 删除目录D:\EYAOI\JOB\Job名\Job名.oki
    oki_path = f"D:\\EYAOI\\JOB\\{program_name}\\{program_name}.oki"
    if os.path.exists(oki_path):
        shutil.rmtree(oki_path, ignore_errors=True)
    # 删除目录F:\DataExport\Job名\OKImage
    ok_image_path = f"F:\\DataExport\\{program_name}\\OKImage"
    if os.path.exists(ok_image_path):
        shutil.rmtree(ok_image_path, ignore_errors=True)
    # 在某一元件【元器件编辑】界面，右击--【导出元件OK图】
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.EXPORT_COMPONENT_OK)
    # 在提示框，点击【确定】
    utils.search_symbol_erroring(config.WARNING)
    pyautogui.press("enter")
    # 弹框提示：生成ok图完成，并可以在F:\DataExport\Job名\OKImage下发现
    ok_image_path = f"F:\\DataExport\\{program_name}\\OKImage"
    if os.path.exists(ok_image_path):
        recent_files = [f for f in os.listdir(ok_image_path) if
                        os.path.getctime(os.path.join(ok_image_path, f)) > time.time() - 10]
        if not recent_files:
            raise Exception("在指定目录下未找到最近10秒内生成的OK图数据")
    utils.close_aoi()


@utils.screenshot_error_to_excel()
def lxbj_005_02():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 1、UI：参数配置--UI配置-程序设置：不选【导出元件OK图】、选择【导出所有元件OK图】
    utils.check_export_ok(False, True)
    utils.click_by_png(config.RUN_DARK)
    program_name = utils.read_text(110, 70)
    # 删除目录D:\EYAOI\JOB\Job名\Job名.oki
    oki_path = f"D:\\EYAOI\\JOB\\{program_name}\\{program_name}.oki"
    if os.path.exists(oki_path):
        shutil.rmtree(oki_path, ignore_errors=True)
    # 删除目录F:\DataExport\Job名\OKImage
    ok_image_path = f"F:\\DataExport\\{program_name}\\OKImage"
    if os.path.exists(ok_image_path):
        shutil.rmtree(ok_image_path, ignore_errors=True)
    # 在某一元件【元器件编辑】界面，右击--【导出元件OK图】
    point = (935, 445)
    pyautogui.rightClick(point)
    utils.click_by_png(config.EXPORT_COMPONENT_OK)
    # 在提示框，点击【确定】
    utils.search_symbol_erroring(config.WARNING, timeout=5)
    pyautogui.press("enter")
    # 弹框提示：生成ok图完成，并可以在F:\DataExport\Job名\OKImage下发现
    ok_image_path = f"F:\\DataExport\\{program_name}\\OKImage"
    if os.path.exists(ok_image_path):
        recent_files = [f for f in os.listdir(ok_image_path) if
                        os.path.getctime(os.path.join(ok_image_path, f)) > time.time() - 10]
        if not recent_files:
            raise Exception("在指定目录下未找到最近10秒内生成的OK图数据")
    utils.close_aoi()


@utils.screenshot_error_to_excel()
def lxbj_005_03():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    utils.check_export_ok(True, False)
    utils.click_by_png(config.RUN_DARK)
    program_name = utils.read_text(110, 70)
    # 删除目录D:\EYAOI\JOB\Job名\Job名.oki
    shutil.rmtree(f"D:\\EYAOI\\JOB\\{program_name}\\{program_name}.oki", ignore_errors=True)
    # 删除目录F:\DataExport\Job名\OKImage
    shutil.rmtree(f"F:\\DataExport\\{program_name}\\OKImage", ignore_errors=True)
    # 在某一元件【元器件编辑】界面，右击--【导出元件OK图】
    point = (935, 445)
    pyautogui.rightClick(point)
    utils.click_by_png(config.EXPORT_PART_OK)
    if not utils.search_symbol_erroring(config.QUESTION_MARK, 5):
        raise Exception("未发现提示框")
    else:
        pyautogui.press('enter')
        while utils.search_symbol(config.EXPORTING_OK, 2):
            time.sleep(2)
        utils.search_symbol_erroring(config.OK_COLLECTION, 60)
        pyautogui.press('enter')
    # 弹框提示：生成ok图完成，并可以在F:\DataExport\Job名\OKImage下发现
    ok_image_path = f"F:\\DataExport\\{program_name}\\OKImage"
    if os.path.exists(ok_image_path):
        recent_files = [f for f in os.listdir(ok_image_path) if
                        os.path.getctime(os.path.join(ok_image_path, f)) > time.time() - 10]
        if not recent_files:
            raise Exception("在指定目录下未找到最近10秒内生成的OK图数据")
    utils.close_aoi()


@utils.screenshot_error_to_excel()
def lxbj_005_04():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    utils.check_export_ok(False, True)
    utils.click_by_png(config.RUN_DARK)
    program_name = utils.read_text(110, 70)
    # 删除目录D:\EYAOI\JOB\Job名\Job名.oki
    shutil.rmtree(f"D:\\EYAOI\\JOB\\{program_name}\\{program_name}.oki", ignore_errors=True)
    # 删除目录F:\DataExport\Job名\OKImage
    shutil.rmtree(f"F:\\DataExport\\{program_name}\\OKImage", ignore_errors=True)
    # 在某一元件【元器件编辑】界面，右击--【导出元件OK图】
    point = (935, 445)
    pyautogui.rightClick(point)
    utils.click_by_png(config.EXPORT_PART_OK)
    if not utils.search_symbol_erroring(config.WARNING, 5):
        raise Exception("未发现提示框")
    else:
        pyautogui.press('enter')
        while utils.search_symbol(config.EXPORTING_OK, 2):
            time.sleep(2)
        utils.search_symbol_erroring(config.OK_COLLECTION, 60)
        pyautogui.press('enter')
    # 弹框提示：生成ok图完成，并可以在F:\DataExport\Job名\OKImage下发现
    ok_image_path = f"F:\\DataExport\\{program_name}\\OKImage"
    if os.path.exists(ok_image_path):
        recent_files = [f for f in os.listdir(ok_image_path) if
                        os.path.getctime(os.path.join(ok_image_path, f)) > time.time() - 10]
        if not recent_files:
            raise Exception("在指定目录下未找到最近10秒内生成的OK图数据")
    utils.close_aoi()


@utils.screenshot_error_to_excel()
def lxbj_006_01():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    utils.click_by_png(config.SYSTEM_DARK)
    utils.click_by_png(config.RENAME_PROGRAM)
    utils.search_symbol_erroring(config.OK_COLLECTION)
    program_name = utils.read_text(900, 525)
    pyautogui.click((1098, 451))
    # 删除目录D:\EYAOI\JOB\Job名\Job名.oki
    shutil.rmtree(f"D:\\EYAOI\\JOB\\{program_name}\\{program_name}.oki", ignore_errors=True)
    # 删除目录F:\DataExport\Job名\OKImage
    shutil.rmtree(f"F:\\DataExport\\{program_name}\\OKImage", ignore_errors=True)
    # 在某一元件【元器件编辑】界面，右击--【导出元件OK图】
    point = (935, 445)
    pyautogui.rightClick(point)
    utils.click_by_png(config.EXPORT_ALL_OK)
    if not utils.search_symbol_erroring(config.QUESTION_MARK, 5):
        raise Exception("未发现提示框")
    else:
        pyautogui.press('enter')
        while utils.search_symbol(config.EXPORTING_OK, 2):
            time.sleep(2)
        utils.search_symbol_erroring(config.OK_COLLECTION, 60)
        pyautogui.press('enter')
    # 弹框提示：生成ok图完成，并可以在F:\DataExport\Job名\OKImage下发现   TODO 6-1 和6-2没找到地方去读取program_name
    ok_image_path = f"F:\\DataExport\\{program_name}\\OKImage"
    if os.path.exists(ok_image_path):
        recent_files = [f for f in os.listdir(ok_image_path) if
                        os.path.getctime(os.path.join(ok_image_path, f)) > time.time() - 10]
        if not recent_files:
            raise Exception("在指定目录下未找到最近10秒内生成的OK图数据")
    utils.close_aoi()


@utils.screenshot_error_to_excel()
def lxbj_006_02():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    utils.check_export_ok(False, True)
    utils.click_by_png(config.SYSTEM_DARK)
    utils.click_by_png(config.RENAME_PROGRAM)
    utils.search_symbol_erroring(config.OK_COLLECTION)
    program_name = utils.read_text(900, 525)
    pyautogui.click((1098, 451))
    # 删除目录D:\EYAOI\JOB\Job名\Job名.oki
    shutil.rmtree(f"D:\\EYAOI\\JOB\\{program_name}\\{program_name}.oki", ignore_errors=True)
    # 删除目录F:\DataExport\Job名\OKImage
    shutil.rmtree(f"F:\\DataExport\\{program_name}\\OKImage", ignore_errors=True)
    # 在某一元件【元器件编辑】界面，右击--【导出元件OK图】
    point = (935, 445)
    pyautogui.rightClick(point)
    utils.click_by_png(config.EXPORT_ALL_OK)
    if not utils.search_symbol_erroring(config.IF_EXPORT_ALL_OK, 5):
        raise Exception("未发现提示框")
    else:
        pyautogui.press('enter')
        while utils.search_symbol(config.EXPORTING_OK, 2):
            time.sleep(2)
        utils.search_symbol_erroring(config.OK_COLLECTION, 60)
        pyautogui.press('enter')
    # 弹框提示：生成ok图完成，并可以在F:\DataExport\Job名\OKImage下发现
    ok_image_path = f"F:\\DataExport\\{program_name}\\OKImage"
    if os.path.exists(ok_image_path):
        recent_files = [f for f in os.listdir(ok_image_path) if
                        os.path.getctime(os.path.join(ok_image_path, f)) > time.time() - 10]
        if not recent_files:
            raise Exception("在指定目录下未找到最近10秒内生成的OK图数据")
    utils.close_aoi()


# 参数配置--演算法配置--关联子框检测模式：选择【父框检测NG不计算】
@utils.screenshot_error_to_excel()
def lxbj_007_01():
    utils.check_and_launch_aoi()
    utils.check_patent_not_NG(1)
    # 1、在某一元件的【元器件编辑】界面，点击上方【检测窗口】添加父、子框，如父框：方形定位、子框：颜色面积
    utils.ensure_in_edit_mode()
    # 遍历所有元件类型 获取父框，子框进行操作
    components = [config.NO_CHECKED_COMPONENT, config.CHECKED_COMPONENT, config.PASS_COMPONENT, config.NO_PASS_COMPONENT]
    
    def find_frames():
        timeout = 600  # 设置超时时间为6.0秒
        start_time = time.time()
        while time.time() - start_time < timeout:
            for component in components:
                logger.debug(f"查找元件类型: {component}")
                logger.debug(f"区域: {config.BOARD_INFORMATION_REGION}")
                try:
                    component_positions = list(pyautogui.locateAllOnScreen(component, region=config.BOARD_INFORMATION_REGION))
                except Exception as e:
                    logger.warning(f"查找元件类型 {component} 时出错: {e}")
                    continue
                if not component_positions:
                    continue
                for pos in component_positions:
                    logger.debug(f"双击元件: {pos}")
                    pyautogui.doubleClick(pos)
                    time.sleep(20)  # 等待界面响应

                    # 获取父框，子框
                    try:
                        w_positions = list(pyautogui.locateAllOnScreen(config.ALG_W_, region=config.COMPONENT_WINDOW_REGION))
                        logger.info(f"算法框数量: {len(w_positions)}")
                        if len(w_positions) < 2:
                            logger.warning("算法框少于两个，跳到下一个元件")
                            continue
                        father_frame = None
                        child_frame = None
                        for w_pos in w_positions:
                            x, y = pyautogui.center(w_pos)
                            logger.debug(f"点击位置: ({x}, {y})")
                            pyautogui.click(x, y)
                            time.sleep(10)
                            # 检测父框良好
                            utils.click_by_png(config.TEST_WINDOW)
                            time.sleep(10)
                            try:
                                good_frame = utils.check_color_in_region((0,128,0), (x, y))
                            except Exception as e:
                                logger.error(f"检测父框良好时出现错误: {e}")
                                continue
                            if good_frame:
                                father_frame = (x, y)
                                break
                        if father_frame:
                            for w_pos in w_positions:
                                x, y = pyautogui.center(w_pos)
                                if (x, y) != father_frame:
                                    child_frame = (x, y)
                                    break
                        if father_frame and child_frame:
                            return father_frame, child_frame
                    except Exception as e:
                        logger.warning(f"获取父框，子框时出现错误： {e}")
                        continue
        raise Exception("超时：未能找到合适的父框和子框")

    father_frame, child_frame = find_frames()
    time.sleep(10)
    while not father_frame or not child_frame:
        utils.scroll_down((200, 410), region=config.BOARD_COMPONENTS_REGION)
        father_frame, child_frame = find_frames()

    if not father_frame or not child_frame:
        raise Exception("遍历所有元件后未能找到合适的父框和子框")

    # 获取到了，开始后续处理
    pyautogui.keyDown('ctrl')
    pyautogui.click(father_frame)
    time.sleep(10)
    pyautogui.click(child_frame)
    pyautogui.keyUp('ctrl')
    time.sleep(5)
    # 2、父、子框同时选中后，点击上方【关联】
    utils.click_by_png(config.RELATE_WINDOW)
    result = utils.check_color_in_region()
    if not result:
        raise Exception("未检测到红色连接线")
    # 3、选中父框，如向上移动，使之测试结果变成NG 
    pyautogui.click(father_frame)
    time.sleep(5)
    pyautogui.press('up', presses=20, interval=0.25)
    # 4、选择子框后，点击【测试当前窗口】
    pyautogui.click(child_frame)
    time.sleep(5)
    utils.click_by_png(config.TEST_WINDOW)
    time.sleep(5)
    alg_result_positions = list(pyautogui.locateAllOnScreen(config.ALG_RESULT_0, region=config.ALG_PARAM_REGION))
    if len(alg_result_positions) < 3:
        raise Exception("疑似算法参数结果不为0")
    # 5、点击【测试当前元件】
    utils.click_by_png(config.TEST_COMPONENT)
    timeout = 60  # 设置超时时间为60秒
    start_time = time.time()
    while utils.search_symbol(config.TESTING_COMPONENT):
        if time.time() - start_time > timeout:
            raise Exception("测试元件等待超时")
        time.sleep(2)
    time.sleep(1)
    alg_result_positions = list(pyautogui.locateAllOnScreen(config.ALG_RESULT_0, region=config.ALG_PARAM_REGION))
    if len(alg_result_positions) < 3:
        raise Exception("疑似算法参数结果不为0")
    # 6、点击【测试当前分组】
    utils.click_by_png(config.TEST_GROUP)
    start_time = time.time()
    while utils.search_symbol(config.TESTING_COMPONENT):
        if time.time() - start_time > timeout:
            raise Exception("测试元件等待超时")
        time.sleep(2)    
    time.sleep(1)
    alg_result_positions = list(pyautogui.locateAllOnScreen(config.ALG_RESULT_0, region=config.ALG_PARAM_REGION))
    if len(alg_result_positions) < 3:
        raise Exception("疑似算法参数结果不为0")
    # TODO 位置是矫正后的位置，与父框移动的方向相反。
    utils.close_aoi()

# 1、参数配置--演算法配置--关联子框检测模式：选择【父框检测NG不计算】
# 2、父框检测结果是良好
@utils.screenshot_error_to_excel()
def lxbj_007_02():
    utils.check_and_launch_aoi()
    utils.check_patent_not_NG(1)
    # 1、在某一元件的【元器件编辑】界面，点击上方【检测窗口】添加父、子框，如父框：方形定位、子框：颜色面积
    utils.ensure_in_edit_mode()
    # 遍历所有元件类型 获取父框，子框进行操作
    components = [config.NO_CHECKED_COMPONENT, config.CHECKED_COMPONENT, config.PASS_COMPONENT, config.NO_PASS_COMPONENT]
    
    def find_frames():
        for component in components:
            logger.debug(f"查找元件类型: {component}")
            logger.debug(f"区域: {config.BOARD_INFORMATION_REGION}")
            try:
                component_positions = list(pyautogui.locateAllOnScreen(component, region=config.BOARD_INFORMATION_REGION))
            except Exception as e:
                logger.warning(f"查找元件类型 {component} 时出错: {e}")
                continue
            if not component_positions:
                continue
            for pos in component_positions:
                logger.debug(f"双击元件: {pos}")
                pyautogui.doubleClick(pos)
                time.sleep(20)  # 等待界面响应

                # 获取父框，子框
                try:
                    w_positions = list(pyautogui.locateAllOnScreen(config.ALG_W_, region=config.COMPONENT_WINDOW_REGION))
                    logger.info(f"算法框数量: {len(w_positions)}")
                    if len(w_positions) < 2:
                        logger.warning("算法框少于两个，跳到下一个元件")
                        continue
                    father_frame = None
                    child_frame = None
                    for w_pos in w_positions:
                        x, y = pyautogui.center(w_pos)
                        logger.debug(f"点击位置: ({x}, {y})")
                        pyautogui.click(x, y)
                        time.sleep(10)
                        # 检测父框良好
                        utils.click_by_png(config.TEST_WINDOW)
                        time.sleep(10)
                        try:
                            good_frame = utils.check_color_in_region((0,128,0), (x, y))
                        except Exception as e:
                            logger.error(f"检测父框良好时出现错误: {e}")
                            continue
                        if good_frame:
                            father_frame = (x, y)
                            break
                    if father_frame:
                        for w_pos in w_positions:
                            x, y = pyautogui.center(w_pos)
                            if (x, y) != father_frame:
                                child_frame = (x, y)
                                break
                    if father_frame and child_frame:
                        return father_frame, child_frame
                except Exception as e:
                    logger.warning(f"获取父框，子框时出现错误： {e}")
                    continue
        return None, None

    father_frame, child_frame = find_frames()
    time.sleep(10)
    while not father_frame or not child_frame:
        utils.scroll_down((200, 410), region=config.BOARD_COMPONENTS_REGION)
        father_frame, child_frame = find_frames()

    if not father_frame or not child_frame:
        raise Exception("遍历所有元件后未能找到合适的父框和子框")

    # 获取到了，开始后续处理
    pyautogui.keyDown('ctrl')
    pyautogui.click(father_frame)
    time.sleep(10)
    pyautogui.click(child_frame)
    pyautogui.keyUp('ctrl')
    time.sleep(5)
    
    # 2、父、子框同时选中后，点击上方【关联】
    utils.click_by_png(config.RELATE_WINDOW)
    result = utils.check_color_in_region()
    if not result:
        raise Exception("未检测到红色连接线")
    # 4、选择子框后，点击【测试当前窗口】
    time.sleep(1)
    pyautogui.click(child_frame)
    time.sleep(5)
    utils.click_by_png(config.TEST_WINDOW)
    time.sleep(5)
    alg_result_positions = list(pyautogui.locateAllOnScreen(config.ALG_RESULT_0, region=config.ALG_PARAM_REGION))
    if len(alg_result_positions) > 3:
        raise Exception("疑似算法参数结果为0")
    # 5、点击【测试当前元件】
    utils.click_by_png(config.TEST_COMPONENT)
    while utils.search_symbol(config.TESTING_COMPONENT):
        time.sleep(2)
    time.sleep(1)
    alg_result_positions = list(pyautogui.locateAllOnScreen(config.ALG_RESULT_0, region=config.ALG_PARAM_REGION))
    if len(alg_result_positions) > 3:
        raise Exception("疑似算法参数结果为0")
    # 6、点击【测试当前分组】
    utils.click_by_png(config.TEST_GROUP)
    time.sleep(5)
    alg_result_positions = list(pyautogui.locateAllOnScreen(config.ALG_RESULT_0, region=config.ALG_PARAM_REGION))
    if len(alg_result_positions) > 3:
        raise Exception("疑似算法参数结果为0")
    # TODO 位置不变
    utils.close_aoi()

# 参数配置--演算法配置--关联子框检测模式：选择【父框检测NG继续计算】
@utils.screenshot_error_to_excel()
def lxbj_008_01():
    utils.check_and_launch_aoi()
    utils.check_patent_not_NG(2)
    # 1、在某一元件的【元器件编辑】界面，点击上方【检测窗口】添加父、子框，如父框：方形定位、子框：颜色面积
    utils.ensure_in_edit_mode()
    # 遍历所有元件类型 获取父框，子框进行操作
    components = [config.NO_CHECKED_COMPONENT, config.CHECKED_COMPONENT, config.PASS_COMPONENT, config.NO_PASS_COMPONENT]
    
    def find_frames():
        for component in components:
            logger.debug(f"查找元件类型: {component}")
            logger.debug(f"区域: {config.BOARD_INFORMATION_REGION}")
            try:
                component_positions = list(pyautogui.locateAllOnScreen(component, region=config.BOARD_INFORMATION_REGION))
            except Exception as e:
                logger.warning(f"查找元件类型 {component} 时出错: {e}")
                continue
            if not component_positions:
                continue
            for pos in component_positions:
                logger.debug(f"双击元件: {pos}")
                pyautogui.doubleClick(pos)
                time.sleep(20)  # 等待界面响应

                # 获取父框，子框
                try:
                    w_positions = list(pyautogui.locateAllOnScreen(config.ALG_W_, region=config.COMPONENT_WINDOW_REGION))
                    logger.info(f"算法框数量: {len(w_positions)}")
                    if len(w_positions) < 2:
                        logger.warning("算法框少于两个，跳到下一个元件")
                        continue
                    father_frame = None
                    child_frame = None
                    for w_pos in w_positions:
                        x, y = pyautogui.center(w_pos)
                        logger.debug(f"点击位置: ({x}, {y})")
                        pyautogui.click(x, y)
                        time.sleep(10)
                        # 检测父框良好
                        utils.click_by_png(config.TEST_WINDOW)
                        time.sleep(10)
                        try:
                            good_frame = utils.check_color_in_region((0,128,0), (x, y))
                        except Exception as e:
                            logger.error(f"检测父框良好时出现错误: {e}")
                            continue
                        if good_frame:
                            father_frame = (x, y)
                            break
                    if father_frame:
                        for w_pos in w_positions:
                            x, y = pyautogui.center(w_pos)
                            if (x, y) != father_frame:
                                child_frame = (x, y)
                                break
                    if father_frame and child_frame:
                        return father_frame, child_frame
                except Exception as e:
                    logger.warning(f"获取父框，子框时出现错误： {e}")
                    continue
        return None, None

    father_frame, child_frame = find_frames()
    time.sleep(10)
    while not father_frame or not child_frame:
        utils.scroll_down((200, 410), region=config.BOARD_COMPONENTS_REGION)
        father_frame, child_frame = find_frames()

    if not father_frame or not child_frame:
        raise Exception("遍历所有元件后未能找到合适的父框和子框")

    # 获取到了，开始后续处理
    pyautogui.keyDown('ctrl')
    pyautogui.click(father_frame)
    time.sleep(10)
    pyautogui.click(child_frame)
    pyautogui.keyUp('ctrl')
    time.sleep(5)
    # 2、父、子框同时选中后，点击上方【关联】
    utils.click_by_png(config.RELATE_WINDOW)
    result = utils.check_color_in_region()
    if not result:
        raise Exception("未检测到红色连接线")
    # 3、选中父框，如向上移动，使之测试结果变成NG
    pyautogui.click(father_frame)
    time.sleep(5)
    pyautogui.press('up', presses=20, interval=0.45)
    # 4、选择子框后，点击【测试当前窗口】
    pyautogui.click(child_frame)
    time.sleep(5)
    utils.click_by_png(config.TEST_WINDOW)
    time.sleep(5)
    alg_result_positions = list(pyautogui.locateAllOnScreen(config.ALG_RESULT_0, region=config.ALG_PARAM_REGION))
    if len(alg_result_positions) > 3:
        raise Exception("疑似算法参数结果为0")
    # 5、点击【测试当前元件】
    utils.click_by_png(config.TEST_COMPONENT)
    while utils.search_symbol(config.TESTING_COMPONENT):
        time.sleep(2)
    time.sleep(1)
    alg_result_positions = list(pyautogui.locateAllOnScreen(config.ALG_RESULT_0, region=config.ALG_PARAM_REGION))
    if len(alg_result_positions) > 3:
        raise Exception("疑似算法参数结果为0")
    # 6、点击【测试当前分组】
    utils.click_by_png(config.TEST_GROUP)
    while utils.search_symbol(config.TESTING_COMPONENT):
        time.sleep(2)
    time.sleep(1)
    alg_result_positions = list(pyautogui.locateAllOnScreen(config.ALG_RESULT_0, region=config.ALG_PARAM_REGION))
    if len(alg_result_positions) > 3:
        raise Exception("疑似算法参数结果为0")
    # TODO 位置是矫正后的位置，与父框移动的方向相反。
    utils.close_aoi()

# 1、参数配置--演算法配置--关联子框检测模式：选择【父框检测NG继续计算】
# 2、父框检测结果是良好
@utils.screenshot_error_to_excel()
def lxbj_008_02():
    utils.check_and_launch_aoi()
    utils.check_patent_not_NG(2)
    # 1、在某一元件的【元器件编辑】界面，点击上方【检测窗口】添加父、子框，如父框：方形定位、子框：颜色面积
    utils.ensure_in_edit_mode()
    # 遍历所有元件类型 获取父框，子框进行操作
    components = [config.NO_CHECKED_COMPONENT, config.CHECKED_COMPONENT, config.PASS_COMPONENT, config.NO_PASS_COMPONENT]
    
    def find_frames():
        for component in components:
            logger.debug(f"查找元件类型: {component}")
            logger.debug(f"区域: {config.BOARD_INFORMATION_REGION}")
            try:
                component_positions = list(pyautogui.locateAllOnScreen(component, region=config.BOARD_INFORMATION_REGION))
            except Exception as e:
                logger.warning(f"查找元件类型 {component} 时出错: {e}")
                continue
            if not component_positions:
                continue
            for pos in component_positions:
                logger.debug(f"双击元件: {pos}")
                pyautogui.doubleClick(pos)
                time.sleep(20)  # 等待界面响应

                # 获取父框，子框
                try:
                    w_positions = list(pyautogui.locateAllOnScreen(config.ALG_W_, region=config.COMPONENT_WINDOW_REGION))
                    logger.info(f"算法框数量: {len(w_positions)}")
                    if len(w_positions) < 2:
                        logger.warning("算法框少于两个，跳到下一个元件")
                        continue
                    father_frame = None
                    child_frame = None
                    for w_pos in w_positions:
                        x, y = pyautogui.center(w_pos)
                        logger.debug(f"点击位置: ({x}, {y})")
                        pyautogui.click(x, y)
                        time.sleep(10)
                        # 检测父框良好
                        utils.click_by_png(config.TEST_WINDOW)
                        time.sleep(10)
                        try:
                            good_frame = utils.check_color_in_region((0,128,0), (x, y))
                        except Exception as e:
                            logger.error(f"检测父框良好时出现错误: {e}")
                            continue
                        if good_frame:
                            father_frame = (x, y)
                            break
                    if father_frame:
                        for w_pos in w_positions:
                            x, y = pyautogui.center(w_pos)
                            if (x, y) != father_frame:
                                child_frame = (x, y)
                                break
                    if father_frame and child_frame:
                        return father_frame, child_frame
                except Exception as e:
                    logger.warning(f"获取父框，子框时出现错误： {e}")
                    continue
        return None, None

    father_frame, child_frame = find_frames()
    time.sleep(10)
    while not father_frame or not child_frame:
        utils.scroll_down((200, 410), region=config.BOARD_COMPONENTS_REGION)
        father_frame, child_frame = find_frames()

    if not father_frame or not child_frame:
        raise Exception("遍历所有元件后未能找到合适的父框和子框")

    # 获取到了，开始后续处理
    pyautogui.keyDown('ctrl')
    pyautogui.click(father_frame)
    time.sleep(10)
    pyautogui.click(child_frame)
    pyautogui.keyUp('ctrl')
    time.sleep(5)
    # 2、父、子框同时选中后，点击上方【关联】
    utils.click_by_png(config.RELATE_WINDOW)
    result = utils.check_color_in_region()
    if not result:
        raise Exception("未检测到红色连接线")
    # 4、选择子框后，点击【测试当前窗口】
    pyautogui.click(child_frame)
    time.sleep(5)
    utils.click_by_png(config.TEST_WINDOW)
    time.sleep(5)
    alg_result_positions = list(pyautogui.locateAllOnScreen(config.ALG_RESULT_0, region=config.ALG_PARAM_REGION))
    if len(alg_result_positions) > 3:
        raise Exception("疑似算法参数结果为0")
    # 5、点击【测试当前元件】
    utils.click_by_png(config.TEST_COMPONENT)
    while utils.search_symbol(config.TESTING_COMPONENT):
        time.sleep(2)
    time.sleep(1)
    alg_result_positions = list(pyautogui.locateAllOnScreen(config.ALG_RESULT_0, region=config.ALG_PARAM_REGION))
    if len(alg_result_positions) > 3:
        raise Exception("疑似算法参数结果为0")
    # 6、点击【测试当前分组】
    utils.click_by_png(config.TEST_GROUP)
    while utils.search_symbol(config.TESTING_COMPONENT):
        time.sleep(2)
    time.sleep(1)
    alg_result_positions = list(pyautogui.locateAllOnScreen(config.ALG_RESULT_0, region=config.ALG_PARAM_REGION))
    if len(alg_result_positions) > 3:
        raise Exception("疑似算法参数结果为0")
    # TODO 位置不变
    utils.close_aoi()

# 参数配置--演算法配置--关联子框检测模式：选择【父框检测NG继续关联】
@utils.screenshot_error_to_excel()
def lxbj_009_01():
    utils.check_and_launch_aoi()
    utils.check_patent_not_NG(3)
    # 1、在某一元件的【元器件编辑】界面，点击上方【检测窗口】添加父、子框，如父框：方形定位、子框：颜色面积
    utils.ensure_in_edit_mode()
    # 遍历所有元件类型 获取父框，子框进行操作
    components = [config.NO_CHECKED_COMPONENT, config.CHECKED_COMPONENT, config.PASS_COMPONENT, config.NO_PASS_COMPONENT]
    
    def find_frames():
        for component in components:
            logger.debug(f"查找元件类型: {component}")
            logger.debug(f"区域: {config.BOARD_INFORMATION_REGION}")
            try:
                component_positions = list(pyautogui.locateAllOnScreen(component, region=config.BOARD_INFORMATION_REGION))
            except Exception as e:
                logger.warning(f"查找元件类型 {component} 时出错: {e}")
                continue
            if not component_positions:
                continue
            for pos in component_positions:
                logger.debug(f"双击元件: {pos}")
                pyautogui.doubleClick(pos)
                time.sleep(20)  # 等待界面响应

                # 获取父框，子框
                try:
                    w_positions = list(pyautogui.locateAllOnScreen(config.ALG_W_, region=config.COMPONENT_WINDOW_REGION))
                    logger.info(f"算法框数量: {len(w_positions)}")
                    if len(w_positions) < 2:
                        logger.warning("算法框少于两个，跳到下一个元件")
                        continue
                    father_frame = None
                    child_frame = None
                    for w_pos in w_positions:
                        x, y = pyautogui.center(w_pos)
                        logger.debug(f"点击位置: ({x}, {y})")
                        pyautogui.click(x, y)
                        time.sleep(10)
                        # 检测父框良好
                        utils.click_by_png(config.TEST_WINDOW)
                        time.sleep(10)
                        try:
                            good_frame = utils.check_color_in_region((0,128,0), (x, y))
                        except Exception as e:
                            logger.error(f"检测父框良好时出现错误: {e}")
                            continue
                        if good_frame:
                            father_frame = (x, y)
                            break
                    if father_frame:
                        for w_pos in w_positions:
                            x, y = pyautogui.center(w_pos)
                            if (x, y) != father_frame:
                                child_frame = (x, y)
                                break
                    if father_frame and child_frame:
                        return father_frame, child_frame
                except Exception as e:
                    logger.warning(f"获取父框，子框时出现错误： {e}")
                    continue
        return None, None

    father_frame, child_frame = find_frames()
    time.sleep(10)
    while not father_frame or not child_frame:
        utils.scroll_down((200, 410), region=config.BOARD_COMPONENTS_REGION)
        father_frame, child_frame = find_frames()

    if not father_frame or not child_frame:
        raise Exception("遍历所有元件后未能找到合适的父框和子框")

    # 获取到了，开始后续处理
    pyautogui.keyDown('ctrl')
    pyautogui.click(father_frame)
    time.sleep(10)
    pyautogui.click(child_frame)
    pyautogui.keyUp('ctrl')
    time.sleep(5)
    # 2、父、子框同时选中后，点击上方【关联】
    utils.click_by_png(config.RELATE_WINDOW)
    result = utils.check_color_in_region()
    if not result:
        raise Exception("未检测到红色连接线")
    # 3、选中父框，如向上移动，使之测试结果变成NG 
    pyautogui.click(father_frame)
    time.sleep(5)
    pyautogui.press('up', presses=20, interval=0.45)
    # 4、选择子框后，点击【测试当前窗口】
    pyautogui.click(child_frame)
    time.sleep(5)
    utils.click_by_png(config.TEST_WINDOW)
    time.sleep(5)
    alg_result_positions = list(pyautogui.locateAllOnScreen(config.ALG_RESULT_0, region=config.ALG_PARAM_REGION))
    if len(alg_result_positions) > 3:
        raise Exception("疑似算法参数结果为0")
    # 5、点击【测试当前元件】
    utils.click_by_png(config.TEST_COMPONENT)
    while utils.search_symbol(config.TESTING_COMPONENT):
        time.sleep(2)
    time.sleep(1)
    alg_result_positions = list(pyautogui.locateAllOnScreen(config.ALG_RESULT_0, region=config.ALG_PARAM_REGION))
    if len(alg_result_positions) > 3:
        raise Exception("疑似算法参数结果为0")
    # 6、点击【测试当前分组】
    utils.click_by_png(config.TEST_GROUP)
    while utils.search_symbol(config.TESTING_COMPONENT):
        time.sleep(2)
    time.sleep(1)
    alg_result_positions = list(pyautogui.locateAllOnScreen(config.ALG_RESULT_0, region=config.ALG_PARAM_REGION))
    if len(alg_result_positions) > 3:
        raise Exception("疑似算法参数结果为0")
    # TODO 位置是矫正后的位置，与父框移动的方向相反。
    utils.close_aoi()

# 1、参数配置--演算法配置--关联子框检测模式：选择【父框检测NG继续关联】
# 2、父框检测结果是良好
@utils.screenshot_error_to_excel()
def lxbj_009_02():
    utils.check_and_launch_aoi()
    utils.check_patent_not_NG(3)
    # 1、在某一元件的【元器件编辑】界面，点击上方【检测窗口】添加父、子框，如父框：方形定位、子框：颜色面积
    utils.ensure_in_edit_mode()
    # 遍历所有元件类型 获取父框，子框进行操作
    components = [config.NO_CHECKED_COMPONENT, config.CHECKED_COMPONENT, config.PASS_COMPONENT, config.NO_PASS_COMPONENT]
    
    def find_frames():
        for component in components:
            logger.debug(f"查找元件类型: {component}")
            logger.debug(f"区域: {config.BOARD_INFORMATION_REGION}")
            try:
                component_positions = list(pyautogui.locateAllOnScreen(component, region=config.BOARD_INFORMATION_REGION))
            except Exception as e:
                logger.warning(f"查找元件类型 {component} 时出错: {e}")
                continue
            if not component_positions:
                continue
            for pos in component_positions:
                logger.debug(f"双击元件: {pos}")
                pyautogui.doubleClick(pos)
                time.sleep(20)  # 等待界面响应

                # 获取父框，子框
                try:
                    w_positions = list(pyautogui.locateAllOnScreen(config.ALG_W_, region=config.COMPONENT_WINDOW_REGION))
                    logger.info(f"算法框数量: {len(w_positions)}")
                    if len(w_positions) < 2:
                        logger.warning("算法框少于两个，跳到下一个元件")
                        continue
                    father_frame = None
                    child_frame = None
                    for w_pos in w_positions:
                        x, y = pyautogui.center(w_pos)
                        logger.debug(f"点击位置: ({x}, {y})")
                        pyautogui.click(x, y)
                        time.sleep(10)
                        # 检测父框良好
                        utils.click_by_png(config.TEST_WINDOW)
                        time.sleep(10)
                        try:
                            good_frame = utils.check_color_in_region((0,128,0), (x, y))
                        except Exception as e:
                            logger.error(f"检测父框良好时出现错误: {e}")
                            continue
                        if good_frame:
                            father_frame = (x, y)
                            break
                    if father_frame:
                        for w_pos in w_positions:
                            x, y = pyautogui.center(w_pos)
                            if (x, y) != father_frame:
                                child_frame = (x, y)
                                break
                    if father_frame and child_frame:
                        return father_frame, child_frame
                except Exception as e:
                    logger.warning(f"获取父框，子框时出现错误： {e}")
                    continue
        return None, None

    father_frame, child_frame = find_frames()
    time.sleep(10)
    while not father_frame or not child_frame:
        utils.scroll_down((200, 410), region=config.BOARD_COMPONENTS_REGION)
        father_frame, child_frame = find_frames()

    if not father_frame or not child_frame:
        raise Exception("遍历所有元件后未能找到合适的父框和子框")

    # 获取到了，开始后续处理
    pyautogui.keyDown('ctrl')
    pyautogui.click(father_frame)
    time.sleep(10)
    pyautogui.click(child_frame)
    pyautogui.keyUp('ctrl')
    time.sleep(5)
    # 2、父、子框同时选中后，点击上方【关联】
    utils.click_by_png(config.RELATE_WINDOW)
    result = utils.check_color_in_region()
    if not result:
        raise Exception("未检测到红色连接线")
    # 4、选择子框后，点击【测试当前窗口】
    pyautogui.click(child_frame)
    time.sleep(5)
    utils.click_by_png(config.TEST_WINDOW)
    time.sleep(5)
    alg_result_positions = list(pyautogui.locateAllOnScreen(config.ALG_RESULT_0, region=config.ALG_PARAM_REGION))
    if len(alg_result_positions) > 3:
        raise Exception("疑似算法参数结果为0")
    # 5、点击【测试当前元件】
    utils.click_by_png(config.TEST_COMPONENT)
    time.sleep(5)
    alg_result_positions = list(pyautogui.locateAllOnScreen(config.ALG_RESULT_0, region=config.ALG_PARAM_REGION))
    if len(alg_result_positions) > 3:
        raise Exception("疑似算法参数结果为0")
    # 6、点击【测试当前分组】
    utils.click_by_png(config.TEST_GROUP)
    time.sleep(5)
    alg_result_positions = list(pyautogui.locateAllOnScreen(config.ALG_RESULT_0, region=config.ALG_PARAM_REGION))
    if len(alg_result_positions) > 3:
        raise Exception("疑似算法参数结果为0")
    # TODO 位置不变
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_010_01():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 1、点击【工具】--【封装类型管理】
    if utils.search_symbol(config.TOOL_DARK):
        utils.click_by_png(config.TOOL_DARK)
    else:
        utils.click_by_png(config.TOOL)
    utils.click_by_png(config.PACKAGE_TYPE_MANAGE)
    # 2、在弹窗左侧选择1个封装类型，点击【编辑封装类型】，输入新的封装类型名称，点击【是】
    time.sleep(1)
    old_part_no = pyautogui.screenshot(region=config.PACKAGE_PART_NO_REGION)
    utils.click_by_png(config.EDIT_PACKAGE_TYPE)
    time.sleep(0.5)
    pyautogui.write('test')
    pyautogui.press('enter')
    # 编辑完后 在封装类型处输入剪切板的内容 点击查询
    pyautogui.click((840, 290))
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.write('test')
    utils.click_by_png(config.QUERY)
    # 检测剪切板内容是否为test 不是的行报错
    utils.click_by_png(config.COPY_PACKAGE_TYPE_NAME)
    clipboard_content = pyperclip.paste()
    if clipboard_content != 'test':
        raise Exception("剪切板内容不是'test'")
    time.sleep(1)
    # 截图（955，351）至（1211，690）区域为new 对比old和new看是否一致，不一致则报错
    new_part_no = pyautogui.screenshot(region= config.PACKAGE_PART_NO_REGION)
    if old_part_no != new_part_no:
        raise Exception("料号不一致")
    utils.click_by_png(config.CLEAR_PACKAGE_TYPE)
    pyautogui.press('enter')
    utils.click_by_png(config.CLOSE_BUTTON)
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_010_02():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 1、点击【工具】--【封装类型管理】
    if utils.search_symbol(config.TOOL_DARK):
        utils.click_by_png(config.TOOL_DARK)
    utils.click_by_png(config.TOOL)
    utils.click_by_png(config.PACKAGE_TYPE_MANAGE)
    time.sleep(2)
    # 2、在弹窗左侧选择多个封装类型，点击【编辑封装类型】，输入新的封装类型名称，点击【是】
    a = (730,360)
    pyautogui.click(a)
    a_content = utils.read_text_ocr((955, 351), (1211, 690)).strip()
    b = (730,375)
    pyautogui.click(b)
    b_content = utils.read_text_ocr((955, 351), (1211, 690)).strip()
    c = (730,388)
    pyautogui.click(c)
    c_content = utils.read_text_ocr((955, 351), (1211, 690)).strip()
    # 分别点击几个封装类型，截图料号
    pyautogui.keyDown('ctrl')
    pyautogui.click(a)
    pyautogui.click(b)
    pyautogui.keyUp('ctrl')
    # 新的封装类型包含所有料号
    utils.click_by_png(config.EDIT_PACKAGE_TYPE)
    pyautogui.write('test')
    utils.click_by_png(config.YES)
    pyautogui.click((840, 290))
    pyautogui.write('test')
    utils.click_by_png(config.QUERY)
    time.sleep(1)
    all_content = utils.read_text_ocr((955, 351), (1211, 690)).strip()
    if utils.contains(a_content, all_content) and utils.contains(b_content, all_content) and utils.contains(c_content, all_content):
        logger.info("新的封装类型包含所有料号")
    else:
        raise Exception("新的封装类型不包含所有料号")
    utils.click_by_png(config.CLEAR_PACKAGE_TYPE)
    time.sleep(1)
    pyautogui.press('enter')
    utils.click_by_png(config.CLOSE_BUTTON)
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_010_03():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    time.sleep(3)
    # 1、点击【工具】--【封装类型管理】
    if utils.search_symbol(config.TOOL_DARK):
        utils.click_by_png(config.TOOL_DARK)
    else:
        utils.click_by_png(config.TOOL)
    utils.click_by_png(config.PACKAGE_TYPE_MANAGE)
    # 2、选择一个封装，点击清除
    utils.click_by_png(config.COPY_PACKAGE_TYPE_NAME, tolerance=0.9)
    old_content = pyperclip.paste()
    utils.click_by_png(config.CLEAR_PACKAGE_TYPE, tolerance=0.9)
    utils.search_symbol_erroring(config.QUESTION_MARK, tolerance=0.9)
    pyautogui.press('enter')
    # 编辑完后 在封装类型处输入剪切板的内容 点击查询
    pyautogui.click((840, 290))
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'v')
    utils.click_by_png(config.QUERY)
    # 检测剪切板内容是否为test 不是的行报错
    utils.click_by_png(config.COPY_PACKAGE_TYPE_NAME, tolerance=0.9)
    new_content = pyperclip.paste()
    logger.debug(old_content)
    logger.debug(new_content)
    if new_content == old_content:
        raise Exception("封装类型删除失败")
    utils.click_by_png(config.CLOSE_BUTTON)
    utils.close_aoi()


@utils.screenshot_error_to_excel()
def lxbj_010_04():
    # 点击两个封装，复制存入a和b，再清除a，b，点复制（c） c与a，b对比
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 1、点击【工具】--【封装类型管理】
    if utils.search_symbol(config.TOOL_DARK):
        utils.click_by_png(config.TOOL_DARK)
    else:
        utils.click_by_png(config.TOOL)
    utils.click_by_png(config.PACKAGE_TYPE_MANAGE)
    # 2、在弹窗左侧选择多个封装类型，点击【清除封装类型】
    a = (730,360)
    b = (730,375)
    pyautogui.click(a)
    utils.click_by_png(config.COPY_PACKAGE_TYPE_NAME, tolerance=0.9)
    content_a = pyperclip.paste()
    pyautogui.click(b)
    utils.click_by_png(config.COPY_PACKAGE_TYPE_NAME, tolerance=0.9)
    content_b = pyperclip.paste()
    pyautogui.keyDown('ctrl')
    pyautogui.click(a)
    pyautogui.keyUp('ctrl')
    utils.click_by_png(config.CLEAR_PACKAGE_TYPE, tolerance=0.9)
    pyautogui.press('enter')
    time.sleep(1)
    utils.click_by_png(config.COPY_PACKAGE_TYPE_NAME, tolerance=0.9)
    content_c = pyperclip.paste()
    if content_a != content_c and content_b != content_c:
        logger.info("删除成功")
    else:
        raise Exception("删除失败")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_011_01():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    utils.click_by_png(config.EDIT_BACK)
    time.sleep(3)
    pyautogui.press('enter')
    time.sleep(3)
    pyautogui.press('enter')
    time.sleep(3)
    # 1、在整板视图，点击左上方【板】-【FOV】
    utils.click_by_png(config.FOV)
    # 2、在弹窗【FOV检测】-【异物】：选择所有子选项，其中【类型】选择【元件遮罩】，点击【是】关闭弹窗。
    time.sleep(1)
    if not utils.if_checked((695, 688), (707, 700)):
        pyautogui.click(config.FOV_FOD)
    if not utils.if_checked((717, 711), (729, 723)):
        pyautogui.click(config.FOV_FOREIGN_CHECK_COORDINATE)
    if not utils.if_checked((717, 732), (729, 744)):
        pyautogui.click(config.FOV_INSIDE_CHECK_COORDINATE)
    time.sleep(1)
    # 3、【确定】关闭弹框
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('enter')
    # 4、在整板视图界面中，右击，选择【整板抽色】，在【Frm_BoardColorFilter】弹窗中完成整板抽色操作。
    if not utils.search_symbol(config.FRM_TOPIC, 8):
        pyautogui.rightClick((1120, 500))
        utils.click_by_png(config.BOARD_COLOR_DRAWING)
    utils.click_by_png(config.FRM_COLOR_DRAWING)
    # 左键按住（1100,160)拖至(1111,150)，松开鼠标
    pyautogui.moveTo(1100, 160)
    pyautogui.dragTo(1111, 150, button='left', duration=1)
    utils.click_by_png(config.FRM_APPLY)
    utils.click_by_png(config.FRM_OK)
    time.sleep(2)
    # 5、在整板视图界面中，点击【整板异物】Tab页，【高级】--【扩展(um)】栏，修改扩展值，如将默认的150改为3000
    utils.is_checked((72,541), (84,553), True)
    time.sleep(2)
    utils.write_text(config.FOV_EXPAND_COORDINATE, "3000")
    # 6、在【整板异物】Tab页，点击【整板遮罩编辑】，查看元件的遮罩
    utils.click_by_png(config.FOV_EDIT)
    # 元件遮罩（粉红色）变大
    utils.search_symbol_erroring(config.FRM_FILL_COLOR)
    time.sleep(2)
    if not utils.check_color_expand():
        raise Exception("元件遮罩（粉红色）未变大")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_012_01():
    # 1、在某一元件【元器件编辑】界面，选择元件【图像匹配】窗口
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    utils.add_window()
    utils.click_by_png(config.ADD_CHECKED_SENIOR)
    utils.click_by_png(config.IMAGE_MATCHING)
    utils.click_by_png(config.YES)
    # 2、在调色板中，修改不同代料的RGB值(红、绿、蓝、限的值)
    if utils.search_symbol(config.IMAGE_PROCESS_TOPIC, 10):
        utils.click_by_png(config.YES)
    if utils.search_symbol(config.IMAGE_CLOSE, 10):
        utils.click_by_png(config.IMAGE_CLOSE)
    time.sleep(5)
    # 添加待料
    utils.add_waiting_material()
    utils.random_change_rgb()
    # 3、查看不同代料的RGB值
    # 截图(820,817)至(849,984) 调下一个待料 再截图(820,817)至(849,984) 对比 
    initial_screenshot = pyautogui.screenshot(region=(820, 817, 29, 167))
    pyautogui.click(1180, 910)  # 调下一个待料
    time.sleep(2)  # 等待待料调整完成
    final_screenshot = pyautogui.screenshot(region=(820, 817, 29, 167))
    if initial_screenshot == final_screenshot:
        logger.error("RGB相互影响了")
    else:
        logger.info("RGB不相互影响")
    utils.close_aoi()

# 1、元件包含【颜色匹配】窗口
# 2、【颜色匹配】窗口包含多个代料
@utils.screenshot_error_to_excel()
def lxbj_012_02():
    # 1、在某一元件【元器件编辑】界面，选择元件【颜色匹配】窗口
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    utils.add_window()
    utils.click_by_png(config.ADD_CHECKED_SENIOR)
    utils.click_by_png(config.COLOR_MATCHING)
    utils.click_by_png(config.YES)
    # 2、在调色板中，修改不同代料的RGB值(红、绿、蓝、限的值)
    if utils.search_symbol(config.IMAGE_PROCESS_TOPIC, 10):
        utils.click_by_png(config.YES)
    if utils.search_symbol(config.IMAGE_CLOSE, 10):
        utils.click_by_png(config.IMAGE_CLOSE)
    time.sleep(5)
    # 添加待料
    utils.add_waiting_material()
    utils.random_change_rgb()
    # 3、查看不同代料的RGB值
    # 截图(820,817)至(849,984) 调下一个待料 再截图(820,817)至(849,984) 对比 
    initial_screenshot = pyautogui.screenshot(region=(820, 817, 29, 167))
    pyautogui.click(1180, 910)  # 调下一个待料
    time.sleep(2)  # 等待待料调整完成
    final_screenshot = pyautogui.screenshot(region=(820, 817, 29, 167))
    if initial_screenshot == final_screenshot:
        logger.error("RGB相互影响了")
    else:
        logger.info("RGB不相互影响")
    utils.close_aoi()

# 1、元件包含【引脚相似度匹配】窗口
# 2、【引脚相似度匹配】窗口包含多个代料
@utils.screenshot_error_to_excel()
def lxbj_012_03():
    # 1、在某一元件【元器件编辑】界面，选择元件【引脚相似度匹配】窗口
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    for _ in range(2):
        utils.add_window("q")
        time.sleep(1)
        pyautogui.press('enter')
    utils.add_window()
    utils.click_by_png(config.PIN_SIMILARITY_MATCHING)
    utils.click_by_png(config.YES)
    # 2、在调色板中，修改不同代料的RGB值(红、绿、蓝、限的值)
    utils.click_by_png(config.YES)
    # 添加待料
    utils.add_waiting_material()
    utils.random_change_rgb()
    # 3、查看不同代料的RGB值
    # 截图(820,817)至(849,984) 调下一个待料 再截图(820,817)至(849,984) 对比 
    initial_screenshot = pyautogui.screenshot(region=(820, 817, 29, 167))
    pyautogui.click(1180, 910)  # 调下一个待料
    time.sleep(5)  # 等待待料调整完成
    final_screenshot = pyautogui.screenshot(region=(820, 817, 29, 167))
    if initial_screenshot == final_screenshot:
        logger.error("RGB相互影响了")
    else:
        logger.info("RGB不相互影响")
    utils.close_aoi()

# 1、元件包含【引脚检测】窗口
# 2、【引脚检测】窗口包含多个代料
@utils.screenshot_error_to_excel()
def lxbj_012_04():
    # 1、在某一元件【元器件编辑】界面，选择元件【引脚检测】窗口
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    for _ in range(2):
        utils.add_window("q")
        time.sleep(1)
        pyautogui.press('enter')
    utils.add_window()
    utils.click_by_png(config.ADD_CHECKED_SENIOR)
    utils.click_by_png(config.PIN_CHECKING)
    utils.click_by_png(config.YES)
    # 2、在调色板中，修改不同代料的RGB值(红、绿、蓝、限的值)
    if utils.search_symbol(config.IMAGE_PROCESS_TOPIC, 10):
        utils.click_by_png(config.YES)
    if utils.search_symbol(config.IMAGE_CLOSE, 10):
        utils.click_by_png(config.IMAGE_CLOSE)
    time.sleep(5)
    # 添加待料
    utils.add_waiting_material()
    utils.random_change_rgb()
    # 3、查看不同代料的RGB值
    # 截图(820,817)至(849,984) 调下一个待料 再截图(820,817)至(849,984) 对比 
    initial_screenshot = pyautogui.screenshot(region=(820, 817, 29, 167))
    pyautogui.click(1180, 910)  # 调下一个待料
    time.sleep(2)  # 等待待料调整完成
    final_screenshot = pyautogui.screenshot(region=(820, 817, 29, 167))
    if initial_screenshot == final_screenshot:
        logger.error("RGB相互影响了")
        raise Exception("RGB相互影响了")
    else:
        logger.info("RGB不相互影响")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_013_01():
    utils.check_and_launch_aoi()
    # 1、使用快捷键，打开某一包含多个检测窗口的djb文件
    utils.ensure_in_edit_mode()
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    for _ in range(2):
        utils.add_window()
        time.sleep(1)
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
        time.sleep(3)
    # 2、在【窗口列表】第一个窗口设置为不勾选，即第1个窗口不检测
    utils.is_checked((68, 684), (80, 696), False, times=3)
    # 3、点击【编辑】--【返回】
    utils.click_by_png(config.EDIT_BACK)
    time.sleep(1)
    # 4、【是】保存修改
    pyautogui.press('enter')
    utils.search_symbol_erroring(config.BOARD_AUTO, 5)
    # 5、双击该元件，查看该元件窗口列表
    region = (170, 290, 161, 314)
    utils.click_by_png(config.TEST, 2, region=region)
    if utils.if_checked((68, 684), (80, 696)):
        raise Exception("打勾框已打勾")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_013_02():
    utils.check_and_launch_aoi()
    # 1、使用快捷键，打开某一包含多个检测窗口的djb文件
    utils.ensure_in_edit_mode()
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    for _ in range(2):
        utils.add_window()
        time.sleep(1)
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
        time.sleep(3)
    # 2、在【窗口列表】第一个窗口设置为不勾选，即第1个窗口不检测
    utils.is_checked((68, 684), (80, 696), False, times=3)
    # 3、点击导出当前料号
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.EXPORT_CURRENT_PN)
    time.sleep(3)
    pyautogui.press('enter')
    time.sleep(1)
    # 勾选第一个窗口
    utils.is_checked((68, 684), (80, 696), True, times=2)
    utils.click_by_png(config.IMPORT_CURRENT_PN)
    pyautogui.press('enter')
    time.sleep(3)
    if utils.if_checked((68, 684), (80, 696)):
        raise Exception("打勾框打勾")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_013_03():
    utils.check_and_launch_aoi()
    # 1、使用快捷键，打开某一包含多个检测窗口的djb文件
    utils.ensure_in_edit_mode()
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    for _ in range(2):
        utils.add_window()
        time.sleep(1)
        utils.click_by_png(config.SQUARE_POSITIONING)
        utils.click_by_png(config.YES)
        time.sleep(0.5)
    # 2、在【窗口列表】第一个窗口设置为勾选，即第1个窗口不检测
    utils.is_checked((68, 684), (80, 696), True, times=3)
    # 3、点击导出当前料号
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.EXPORT_CURRENT_PN)
    pyautogui.press('enter')
    time.sleep(1)
    # 勾选第一个窗口
    utils.is_checked((68, 684), (80, 696), False, times=2)
    utils.click_by_png(config.IMPORT_CURRENT_PN)
    pyautogui.press('enter')

    if not utils.if_checked((68, 684), (80, 696)):
        raise Exception("打勾框未打勾")
    utils.close_aoi()

# 14开头的前置条件：元件带有字符检测窗口
@utils.screenshot_error_to_excel()
def lxbj_014_01():
    utils.check_and_launch_aoi()
    # 1、某一元件的【元器件编辑】界面
    utils.ensure_in_edit_mode()
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    utils.add_window()
    utils.click_by_png(config.ADD_CHECKED_OCV)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
    utils.write_text((812, 268),"1")
    time.sleep(0.5)
    utils.write_text((812, 302),"1")
    utils.click_by_png(config.OCV_EDIT_APPLY)
    # 2、在左侧【元件窗口】列表中，双击【字符检测】窗口
    utils.click_by_png(config.ALG_OCV, 2)
    time.sleep(0.5)
    # 3、在右侧【算法参数】栏中，【检测模式】选择：标准，【字体工艺】选择：默认
    if not utils.search_symbol(config.ALG_CHECK_MODE_STANDARD):
        pyautogui.click((1720, 503))
        pyautogui.click((1720, 525))
    if not utils.search_symbol(config.ALG_LETTERFORM_CRAFTWORK_DEFAULT):
        pyautogui.click((1725, 523))
        pyautogui.click((1725, 545))
    # 4、点击上方【测试当前窗口】
    utils.click_by_png(config.TEST_WINDOW)
    utils.caton_or_flashback("AOI.exe")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_014_02():
    utils.check_and_launch_aoi()
    # 1、某一元件的【元器件编辑】界面
    utils.ensure_in_edit_mode()
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    utils.add_window()
    utils.click_by_png(config.ADD_CHECKED_OCV)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
    utils.write_text((812, 268),"1")
    time.sleep(0.5)
    utils.write_text((812, 302),"1")
    utils.click_by_png(config.OCV_EDIT_APPLY)
    time.sleep(0.5)
    # 2、在左侧【元件窗口】列表中，双击【字符检测】窗口
    utils.click_by_png(config.ALG_OCV, 2)
    # 3、在右侧【算法参数】栏中，【检测模式】选择：标准，【字体工艺】选择：点阵
    if not utils.search_symbol(config.ALG_CHECK_MODE_STANDARD):
        pyautogui.click((1725, 503))
        pyautogui.click((1725, 525))
    if not utils.search_symbol(config.ALG_LATTICE):
        pyautogui.click((1725, 523))
        pyautogui.click((1725, 575))
    # 4、点击上方【测试当前窗口】
    utils.click_by_png(config.TEST_WINDOW)
    utils.caton_or_flashback("AOI.exe")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_014_03():
    utils.check_and_launch_aoi()
    # 1、某一元件的【元器件编辑】界面
    utils.ensure_in_edit_mode()
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    utils.add_window()
    utils.click_by_png(config.ADD_CHECKED_OCV)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
    utils.write_text((812, 268),"1")
    time.sleep(0.5)
    utils.write_text((812, 302),"1")
    utils.click_by_png(config.OCV_EDIT_APPLY)
    time.sleep(0.5)
    # 2、在左侧【元件窗口】列表中，双击【字符检测】窗口
    utils.click_by_png(config.ALG_OCV, 2)
    # 3、在右侧【算法参数】栏中，【检测模式】选择：标准，【字体工艺】选择：晶体管
    if not utils.search_symbol(config.ALG_CHECK_MODE_STANDARD):
        pyautogui.click((1720, 503))
        pyautogui.click((1720, 525))
    if not utils.search_symbol(config.ALG_TRANSISTOR):
        pyautogui.click((1725, 523))
        pyautogui.click((1725, 595))
    # 4、点击上方【测试当前窗口】
    utils.click_by_png(config.TEST_WINDOW)
    utils.caton_or_flashback("AOI.exe")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_014_04():
    utils.check_and_launch_aoi()
    # 1、某一元件的【元器件编辑】界面
    utils.ensure_in_edit_mode()
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    utils.add_window()
    utils.click_by_png(config.ADD_CHECKED_OCV)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
    utils.write_text((812, 268),"1")
    time.sleep(0.5)
    utils.write_text((812, 302),"1")
    utils.click_by_png(config.OCV_EDIT_APPLY)
    time.sleep(0.5)
    # 2、在左侧【元件窗口】列表中，双击【字符检测】窗口
    utils.click_by_png(config.ALG_OCV, 2)
    # 3、在右侧【算法参数】栏中，【检测模式】选择：图例，【字体工艺】选择：默认
    if not utils.search_symbol(config.ALG_CHECK_MODE_LEGEND):
        pyautogui.click((1720, 505))
        pyautogui.click((1720, 540))
    if not utils.search_symbol(config.ALG_LETTERFORM_CRAFTWORK_DEFAULT):
        pyautogui.click((1725, 525))
        pyautogui.click((1725, 545))
    # 4、点击上方【测试当前窗口】
    utils.click_by_png(config.TEST_WINDOW)
    utils.caton_or_flashback("AOI.exe")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_014_05():
    utils.check_and_launch_aoi()
    # 1、某一元件的【元器件编辑】界面
    utils.ensure_in_edit_mode()
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    utils.add_window()
    utils.click_by_png(config.ADD_CHECKED_OCV)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
    utils.write_text((812, 268),"1")
    time.sleep(0.5)
    utils.write_text((812, 302),"1")
    utils.click_by_png(config.OCV_EDIT_APPLY)
    time.sleep(0.5)
    # 2、在左侧【元件窗口】列表中，双击【字符检测】窗口
    utils.click_by_png(config.ALG_OCV, 2)
    # 3、在右侧【算法参数】栏中，【检测模式】选择：图例，【字体工艺】选择：默认
    if not utils.search_symbol(config.ALG_CHECK_MODE_LEGEND):
        pyautogui.click((1720, 503))
        pyautogui.click((1720, 540))
    if not utils.search_symbol(config.ALG_LETTERFORM_CRAFTWORK_DEFAULT):
        pyautogui.click((1725, 523))
        pyautogui.click((1725, 545))
    # 4、点击上方【测试当前窗口】
    utils.click_by_png(config.TEST_WINDOW)
    utils.caton_or_flashback("AOI.exe")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_014_06():
    utils.check_and_launch_aoi()
    # 1、某一元件的【元器件编辑】界面
    utils.ensure_in_edit_mode()
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    utils.add_window()
    utils.click_by_png(config.ADD_CHECKED_OCV)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
    utils.write_text((812, 268),"1")
    time.sleep(0.5)
    utils.write_text((812, 302),"1")
    utils.click_by_png(config.OCV_EDIT_APPLY)
    time.sleep(0.5)
    # 2、在左侧【元件窗口】列表中，双击【字符检测】窗口
    utils.click_by_png(config.ALG_OCV, 2)
    # 3、在右侧【算法参数】栏中，【检测模式】选择：图例，【字体工艺】选择：丝印
    if not utils.search_symbol(config.ALG_CHECK_MODE_LEGEND):
        pyautogui.click((1720, 505))
        pyautogui.click((1720, 540))
    if not utils.search_symbol(config.ALG_TRANSISTOR):
        pyautogui.click((1725, 523))
        pyautogui.click((1725, 560))
    # 4、点击上方【测试当前窗口】
    utils.click_by_png(config.TEST_WINDOW)
    utils.caton_or_flashback("AOI.exe")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_014_07():
    utils.check_and_launch_aoi()
    # 1、某一元件的【元器件编辑】界面
    utils.ensure_in_edit_mode()
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    utils.add_window()
    utils.click_by_png(config.ADD_CHECKED_OCV)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
    utils.write_text((812, 268),"1")
    time.sleep(0.5)
    utils.write_text((812, 302),"1")
    utils.click_by_png(config.OCV_EDIT_APPLY)
    time.sleep(0.5)
    # 2、在左侧【元件窗口】列表中，双击【字符检测】窗口
    utils.click_by_png(config.ALG_OCV, 2)
    # 3、在右侧【算法参数】栏中，【检测模式】选择：图例，【字体工艺】选择：点阵
    if not utils.search_symbol(config.ALG_CHECK_MODE_LEGEND):
        pyautogui.click((1720, 505))
        pyautogui.click((1720, 540))
    if not utils.search_symbol(config.ALG_LATTICE):
        pyautogui.click((1725, 523))
        pyautogui.click((1725, 575))
    # 4、点击上方【测试当前窗口】
    utils.click_by_png(config.TEST_WINDOW)
    utils.caton_or_flashback("AOI.exe")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_014_08():
    utils.check_and_launch_aoi()
    # 1、某一元件的【元器件编辑】界面
    utils.ensure_in_edit_mode()
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    utils.add_window()
    utils.click_by_png(config.ADD_CHECKED_OCV)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
    utils.write_text((812, 268),"1")
    time.sleep(0.5)
    utils.write_text((812, 302),"1")
    utils.click_by_png(config.OCV_EDIT_APPLY)
    time.sleep(0.5)
    # 2、在左侧【元件窗口】列表中，双击【字符检测】窗口
    utils.click_by_png(config.ALG_OCV, 2)
    # 3、在右侧【算法参数】栏中，【检测模式】选择：图例，【字体工艺】选择：晶体管
    if not utils.search_symbol(config.ALG_CHECK_MODE_LEGEND):
        pyautogui.click((1720, 505))
        pyautogui.click((1720, 540))
    if not utils.search_symbol(config.ALG_TRANSISTOR):
        pyautogui.click((1725, 523))
        pyautogui.click((1725, 590))
    # 4、点击上方【测试当前窗口】
    utils.click_by_png(config.TEST_WINDOW)
    utils.caton_or_flashback("AOI.exe")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_014_09():
    utils.check_and_launch_aoi()
    # 1、某一元件的【元器件编辑】界面
    utils.ensure_in_edit_mode()
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    utils.add_window()
    utils.click_by_png(config.ADD_CHECKED_OCV)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
    utils.write_text((812, 268),"1")
    time.sleep(0.5)
    utils.write_text((812, 302),"1")
    utils.click_by_png(config.OCV_EDIT_APPLY)
    time.sleep(0.5)
    # 2、在左侧【元件窗口】列表中，双击【字符检测】窗口
    utils.click_by_png(config.ALG_OCV, 2)
    # 3、在右侧【算法参数】栏中，【检测模式】选择：参数，【字体工艺】选择：默认
    if not utils.search_symbol(config.ALG_CHECK_MODE_PARAMETER):
        pyautogui.click((1720, 505))
        pyautogui.click((1720, 555))
    if not utils.search_symbol(config.ALG_LETTERFORM_CRAFTWORK_DEFAULT):
        pyautogui.click((1725, 523))
        pyautogui.click((1725, 545))
    # 4、点击上方【测试当前窗口】
    utils.click_by_png(config.TEST_WINDOW)
    utils.caton_or_flashback("AOI.exe")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_014_10():
    utils.check_and_launch_aoi()
    # 1、某一元件的【元器件编辑】界面
    utils.ensure_in_edit_mode()
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    utils.add_window()
    utils.click_by_png(config.ADD_CHECKED_OCV)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
    utils.write_text((812, 268),"1")
    time.sleep(0.5)
    utils.write_text((812, 302),"1")
    utils.click_by_png(config.OCV_EDIT_APPLY)
    time.sleep(0.5)
    # 2、在左侧【元件窗口】列表中，双击【字符检测】窗口
    utils.click_by_png(config.ALG_OCV, 2)
    # 3、在右侧【算法参数】栏中，【检测模式】选择：参数，【字体工艺】选择：丝印
    if not utils.search_symbol(config.ALG_CHECK_MODE_PARAMETER):
        pyautogui.click((1720, 505))
        pyautogui.click((1720, 555))
    if not utils.search_symbol(config.ALG_LETTERFORM_CRAFTWORK_DEFAULT):
        pyautogui.click((1725, 525))
        pyautogui.click((1725, 560))
    # 4、点击上方【测试当前窗口】
    utils.click_by_png(config.TEST_WINDOW)
    utils.caton_or_flashback("AOI.exe")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_014_11():
    utils.check_and_launch_aoi()
    # 1、某一元件的【元器件编辑】界面
    utils.ensure_in_edit_mode()
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    utils.add_window()
    utils.click_by_png(config.ADD_CHECKED_OCV)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
    utils.write_text((812, 268),"1")
    time.sleep(0.5)
    utils.write_text((812, 302),"1")
    utils.click_by_png(config.OCV_EDIT_APPLY)
    time.sleep(0.5)
    # 2、在左侧【元件窗口】列表中，双击【字符检测】窗口
    utils.click_by_png(config.ALG_OCV, 2)
    # 3、在右侧【算法参数】栏中，【检测模式】选择：参数，【字体工艺】选择：点阵
    if not utils.search_symbol(config.ALG_CHECK_MODE_PARAMETER):
        pyautogui.click((1720, 505))
        pyautogui.click((1720, 555))
    if not utils.search_symbol(config.ALG_LATTICE):
        pyautogui.click((1725, 523))
        pyautogui.click((1725, 575))
    # 4、点击上方【测试当前窗口】
    utils.click_by_png(config.TEST_WINDOW)
    utils.caton_or_flashback("AOI.exe")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_014_12():
    utils.check_and_launch_aoi()
    # 1、某一元件的【元器件编辑】界面
    utils.ensure_in_edit_mode()
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    utils.add_window()
    utils.click_by_png(config.ADD_CHECKED_OCV)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
    utils.write_text((812, 268),"1")
    time.sleep(0.5)
    utils.write_text((812, 302),"1")
    utils.click_by_png(config.OCV_EDIT_APPLY)
    time.sleep(0.5)
    # 2、在左侧【元件窗口】列表中，双击【字符检测】窗口
    utils.click_by_png(config.ALG_OCV, 2)
    # 3、在右侧【算法参数】栏中，【检测模式】选择：参数，【字体工艺】选择：晶体管
    if not utils.search_symbol(config.ALG_CHECK_MODE_PARAMETER):
        pyautogui.click((1720, 505))
        pyautogui.click((1720, 555))
    if not utils.search_symbol(config.ALG_TRANSISTOR):
        pyautogui.click((1725, 525))
        pyautogui.click((1725, 590))
    # 4、点击上方【测试当前窗口】
    utils.click_by_png(config.TEST_WINDOW)
    utils.caton_or_flashback("AOI.exe")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_015_01():
    utils.check_and_launch_aoi()
    # 1、某一元器件编辑界面，在上方【编辑】--【光源】选择不同光源，如中角度（不选均匀光）；
    utils.ensure_in_edit_mode()
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    utils.click_by_png(config.GUI_EDIT_LIGHT)
    time.sleep(1)
    pyautogui.press('down', 2)
    time.sleep(1)
    pyautogui.press('enter')
    # 2、添加方形定位检测窗口，查看右侧【算法参数】--【2D光源】
    utils.add_window()
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    time.sleep(3)
    utils.search_symbol_erroring(config.ALG2D_LIGHT_UNIFORM)
    time.sleep(1)
    # 3、返回修改该元件；
    utils.modify_component()
    # 4、再次进入该元器件编辑界面，查看方形定位窗口的【算法参数】--【2D光源】
    utils.click_by_png(config.TEST, 2, region=(46, 252, 334, 604))
    pyautogui.press('enter')
    utils.click_by_png(config.ALG_SQUARE_POSITIONING)
    utils.search_symbol_erroring(config.ALG2D_LIGHT_UNIFORM)
    utils.close_aoi()

# 元件添加参考点关联所有检测框
@utils.screenshot_error_to_excel()
def lxbj_016_01():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    utils.click_by_png(config.EDIT_BACK)
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(3)
    # 右键元件直到搜索到添加参考点的框
    utils.board_component_process(config.ADD_REFERENCE_POINT)
    while utils.click_color(1, config.COMPONENT_REGION, (255, 0, 255), 1):
        if utils.search_symbol(config.EDIT_THIS_COMPONENT):
            utils.click_by_png(config.EDIT_THIS_COMPONENT)
            break
        else:
            pyautogui.click((400, 5))
    time.sleep(10)
    # 先加一个方形检测
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    utils.add_window()
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    time.sleep(5)
    # 再加一个颜色面积检测
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(5)
    pyautogui.hotkey('ctrl', 'a')
    utils.click_by_png(config.RELATE_WINDOW)
    if not utils.check_color_in_region():
        raise Exception('子框与父框未连接')
    utils.click_by_png(config.CANCEL_RELATE_WINDOW)
    if utils.check_color_in_region():
        raise Exception('检测框取消关联失败')
    utils.close_aoi()

# 元件添加参考点关联所有检测框
@utils.screenshot_error_to_excel()
def lxbj_016_02():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    utils.click_by_png(config.EDIT_BACK)
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(3)
    utils.board_component_process(config.ADD_REFERENCE_POINT)
    while utils.click_color(1, config.COMPONENT_REGION, (255, 0, 255), 1):
        if utils.search_symbol(config.EDIT_THIS_COMPONENT,tolerance=0.98):
            time.sleep(0.5)
            utils.click_by_png(config.EDIT_THIS_COMPONENT,tolerance=0.98)
            break
        else:
            pyautogui.click((400, 5))
            time.sleep(0.5)
    time.sleep(10)
    # 先加一个方形检测
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    utils.add_window()
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    time.sleep(10)
    # 再加一个颜色面积检测
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(10)
    pyautogui.hotkey("ctrl", "a")
    while utils.click_color(1, config.COMPONENT_REGION,(0,0,255),1):
        time.sleep(0.5)
        if utils.search_symbol(config.CLICK_MENU_RELATE, tolerance=0.99,timeout=3):
            utils.click_by_png(config.CLICK_MENU_RELATE, tolerance=0.99,timeout=3)
            break
        else:
            pyautogui.click((400, 5))
            time.sleep(0.5)
    if not utils.check_color_in_region(region=config.COMPONENT_REGION):
        raise Exception('子框与父框未连接')
    while utils.click_color(1, config.COMPONENT_REGION,(0,0,255),1):
        time.sleep(0.5)
        if utils.search_symbol(config.CLICK_CANCEL_RELATE, tolerance=0.99,timeout=3):
            utils.click_by_png(config.CLICK_CANCEL_RELATE, tolerance=0.99,timeout=3)
            break
        else:
            pyautogui.click((400, 5))
            time.sleep(0.5)
    time.sleep(3)
    if utils.check_color_in_region(region=config.COMPONENT_REGION):
        raise Exception('检测框取消关联失败')
    utils.close_aoi()

# 元件添加参考点关联所有检测框
@utils.screenshot_error_to_excel()
def lxbj_016_03():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    utils.click_by_png(config.EDIT_BACK)
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(3)
    utils.board_component_process(config.ADD_REFERENCE_POINT)
    while utils.click_color(1, config.COMPONENT_REGION, (255, 0, 255), 1):
        if utils.search_symbol(config.EDIT_THIS_COMPONENT,tolerance=0.98):
            time.sleep(0.5)
            utils.click_by_png(config.EDIT_THIS_COMPONENT,tolerance=0.98)
            break
        else:
            pyautogui.click((400, 5))
            time.sleep(0.5)
    time.sleep(10)
    # 先加一个方形检测
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    utils.add_window()
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    time.sleep(10)
    # 再加一个颜色面积检测
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(10)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('F5')
    if not utils.check_color_in_region():
        raise Exception('子框与父框未连接')
    utils.close_aoi()

# 元件添加参考点关联所有检测框
@utils.screenshot_error_to_excel()
def lxbj_016_04():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    utils.click_by_png(config.EDIT_BACK)
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(3)
    utils.board_component_process(config.ADD_REFERENCE_POINT)
    while utils.click_color(1, config.COMPONENT_REGION, (255, 0, 255), 1):
        if utils.search_symbol(config.EDIT_THIS_COMPONENT,tolerance=0.98):
            time.sleep(0.5)
            utils.click_by_png(config.EDIT_THIS_COMPONENT,tolerance=0.98)
            break
        else:
            pyautogui.click((400, 5))
            time.sleep(0.5)
    time.sleep(10)
    # 先加一个方形检测
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    utils.add_window()
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    time.sleep(10)
    # 再加一个颜色面积检测
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(10)
    pyautogui.hotkey('ctrl', 'a')
    while utils.click_color(1, config.COMPONENT_REGION,(0,0,255),1):
        time.sleep(0.5)
        if utils.search_symbol(config.CLICK_AUTO_LINK, tolerance=0.99,timeout=3):
            utils.click_by_png(config.CLICK_AUTO_LINK, tolerance=0.99,timeout=3)
            break
        else:
            pyautogui.click((400, 5))
            time.sleep(0.5)
    if not utils.check_color_in_region():
        raise Exception('子框与父框未连接')
    utils.close_aoi()

#元件添加参考点关联所有检测框
@utils.screenshot_error_to_excel()
def lxbj_016_05():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    utils.click_by_png(config.EDIT_BACK)
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(3)
    utils.board_component_process(config.ADD_REFERENCE_POINT)
    while utils.click_color(1, config.COMPONENT_REGION, (255, 0, 255), 1):
        if utils.search_symbol(config.EDIT_THIS_COMPONENT,tolerance=0.98):
            time.sleep(0.5)
            utils.click_by_png(config.EDIT_THIS_COMPONENT,tolerance=0.98)
            break
        else:
            pyautogui.click((400, 5))
            time.sleep(0.5)
    time.sleep(10)
    # 先加一个方形检测
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    utils.add_window()
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    time.sleep(10)
    # 再加一个颜色面积检测
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(10)
    pyautogui.hotkey("ctrl", "a")
    utils.click_by_png(config.RELATE_WINDOW)
    time.sleep(1)
    if not utils.check_color_in_region():
        raise Exception('子框与父框未连接')
    utils.click_by_png(config.CANCEL_RELATE_WINDOW)
    time.sleep(1)
    if utils.check_color_in_region():
        raise Exception('检测框取消关联失败')
    utils.close_aoi()

# 客户JOB名称和地址：H898_E1_256G+8G_V1.2_TOP_A2（\\192.168.201.215\f\AOI-JOB\泰衡诺科技）
# TODO 做个屁 弄不到那边的job
@utils.screenshot_error_to_excel()
def lxbj_017_01():
    # utils.check_and_launch_aoi()
    # utils.ensure_in_edit_mode()
    # # 1，【程式元件】--【料/位号】：输入C2745，点击放大镜图标查找
    # pyautogui.click(config.PART_POSITION_NO)
    # pyautogui.typewrite('C2745')
    # utils.click_by_png(config.MAGNIFIER)
    # # 2，双轨元件进入元件编辑界面
    # # 3，测试当前窗口
    # utils.click_by_png(config.TEST_WINDOW)
    # # 4，其他三个元件也要测试
    pass


@utils.screenshot_error_to_excel()
def lxbj_018_01():
    utils.check_and_launch_aoi()
    # 1、打开一个编辑过的有多个拼版的job
    utils.ensure_multiple_collages()
    while utils.search_symbol(config.PROGRAM_LOADING):
        time.sleep(5)
    utils.click_by_png(config.PROGRAM_COMPONENT_DARK)
    time.sleep(2)
    # 元件数量
    before_num_region = pyautogui.screenshot(region=config.COMPONENT_NUM_REGION)
    utils.click_by_png(config.WHOLE_BOARD_DARK)
    time.sleep(0.5)
    utils.click_by_png(config.BOARD_REDUCE)
    before_edit_region = pyautogui.screenshot(region=config.COMPONENT_REGION)
    time.sleep(3)
    # 2、左侧选择板--选择一个拼版右键--删除拼版
    utils.click_by_png(config.BOARD_BOARD)
    time.sleep(0.5)
    pyautogui.rightClick()
    time.sleep(1)
    pyautogui.press('up')
    pyautogui.press('enter')
    # 3、点击【是】
    utils.search_symbol_erroring(config.IF_DELETE_BOARD)
    pyautogui.press('enter')
    utils.search_symbol_erroring(config.IF_DELETE_BOARD_WARNING)
    # 4、勾选保留此拼板下的元件
    pyautogui.click(config.RESERVE_COMPONENT_COORDINATE)
    # 5、点击【是】
    pyautogui.press('enter')
    time.sleep(5)
    # 点击缩小按钮之后截图已确认板数量
    now_edit_region = pyautogui.screenshot(region=config.COMPONENT_REGION)
    utils.click_by_png(config.PROGRAM_COMPONENT_DARK)
    utils.click_by_png(config.BOARD_REDUCE)
    now_num_region = pyautogui.screenshot(region=config.COMPONENT_NUM_REGION)
    a = before_num_region == now_num_region
    b = before_edit_region != now_edit_region
    logger.info(f'{a},{b}')
    if before_num_region == now_num_region and before_edit_region != now_edit_region:
        logger.info('拼版被删除且元件保留')
    else:
        logger.error('元件未被保留/拼版未被删除')
        raise Exception('元件未被保留/拼版未被删除')
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_018_02():
    utils.check_and_launch_aoi()
    # 1、打开一个编辑过的有多个拼版的job
    utils.ensure_multiple_collages()
    while utils.search_symbol(config.PROGRAM_LOADING):
        time.sleep(5)
    utils.click_by_png(config.PROGRAM_COMPONENT_DARK)
    time.sleep(2)
    before_num_region = pyautogui.screenshot(region=config.COMPONENT_NUM_REGION)
    utils.click_by_png(config.WHOLE_BOARD_DARK)
    utils.click_by_png(config.BOARD_REDUCE)
    before_edit_region = pyautogui.screenshot(region=config.COMPONENT_REGION)
    time.sleep(3)
    # 2、点击拼版操作 再点击删除拼版
    utils.click_by_png(config.BOARD_SPLICING_OPERATION)
    utils.click_by_png(config.BOARD_BOARD,tolerance=0.95)
    utils.click_by_png(config.BOARD_DELETE_IMPOSITION)
    # 3、点击【是】
    utils.search_symbol_erroring(config.IF_DELETE_BOARD_WARNING)
    # 4、勾选保留此拼板下的元件
    pyautogui.click(config.RESERVE_COMPONENT_COORDINATE)
    # 5、点击【是】
    pyautogui.press('enter')
    time.sleep(5)
    now_edit_region = pyautogui.screenshot(region=config.COMPONENT_REGION)
    utils.click_by_png(config.PROGRAM_COMPONENT_DARK)
    utils.click_by_png(config.BOARD_REDUCE)
    now_num_region = pyautogui.screenshot(region=config.COMPONENT_NUM_REGION)
    a = before_num_region == now_num_region
    b = before_edit_region != now_edit_region
    logger.info(f'{a},{b}')
    if before_num_region == now_num_region and before_edit_region != now_edit_region:
        logger.info('拼版被删除且元件保留')
    else:
        logger.error('元件未被保留/拼版未被删除')
        raise Exception('元件未被保留/拼版未被删除')
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_018_03():
    utils.check_and_launch_aoi()
    # 1、打开一个编辑过的有多个拼版的job
    utils.ensure_multiple_collages()
    while utils.search_symbol(config.PROGRAM_LOADING):
        time.sleep(5)
    utils.click_by_png(config.BOARD_REDUCE)
    # 统计板数量
    board_num_before = utils.count_symbol_on_region(config.BOARD_BOARD)
    logger.info(f'板数量: {board_num_before}')
    # 统计基准点数量
    utils.click_by_png(config.BOARD_ENLARGE)
    utils.scroll_down((200, 400),config.BOARD_INFORMATION_REGION)
    mark_point_num_before = utils.count_symbol_on_region(config.MARK_POINT)
    logger.info(f'基准点数量: {mark_point_num_before}')
    # 2、左侧选择板--选择一个拼版右键--删除拼版
    utils.click_by_png(config.BOARD_BOARD)
    time.sleep(0.5)
    pyautogui.rightClick()
    time.sleep(1)
    pyautogui.press('up')
    pyautogui.press('enter')
    # 3、点击【是】
    utils.search_symbol_erroring(config.IF_DELETE_BOARD)
    pyautogui.press('enter')
    utils.search_symbol_erroring(config.IF_DELETE_BOARD_WARNING)
    # 4、勾选保留基准点
    pyautogui.click(config.RESERVE_BENCHMARK_COORDINATE)
    # 5、点击【是】
    pyautogui.press('enter')
    time.sleep(5)
    # 统计基准点数量
    mark_point_num_after = utils.count_symbol_on_region(config.MARK_POINT)
    logger.info(f'基准点数量: {mark_point_num_after}')
    utils.click_by_png(config.BOARD_REDUCE)
    board_num_after = utils.count_symbol_on_region(config.BOARD_BOARD)
    if board_num_before == board_num_after and mark_point_num_before != mark_point_num_after:
        logger.info('拼版被删除且基准点被保留')
    else:
        logger.error('基准点未被保留/拼版未被删除')
        raise Exception('基准点未被保留/拼版未被删除')
    utils.close_aoi()

# 选择一个拼版删除并保留基准点
@utils.screenshot_error_to_excel()
def lxbj_018_04():
    utils.check_and_launch_aoi()
    # 1、打开一个编辑过的有多个拼版的job
    utils.ensure_multiple_collages()
    while utils.search_symbol(config.PROGRAM_LOADING):
        time.sleep(5)
    utils.click_by_png(config.BOARD_REDUCE)
    # 统计板数量
    board_num_before = utils.count_symbol_on_region(config.BOARD_BOARD)
    logger.info(f'板数量: {board_num_before}')
    # 统计基准点数量
    utils.click_by_png(config.BOARD_ENLARGE)
    utils.scroll_down((200, 400),config.BOARD_INFORMATION_REGION)
    mark_point_num_before = utils.count_symbol_on_region(config.MARK_POINT)
    logger.info(f'基准点数量: {mark_point_num_before}')
    # 2、点击拼版操作 再点击删除拼版
    utils.click_by_png(config.BOARD_SPLICING_OPERATION)
    utils.click_by_png(config.BOARD_BOARD)
    utils.click_by_png(config.BOARD_DELETE_IMPOSITION)
    # 4、勾选保留基准点
    pyautogui.click(config.RESERVE_BENCHMARK_COORDINATE)
    # 5、点击【是】
    utils.search_symbol_erroring(config.IF_DELETE_BOARD_WARNING)
    pyautogui.press('enter')
    time.sleep(5)
    # 统计基准点数量
    mark_point_num_after = utils.count_symbol_on_region(config.MARK_POINT)
    logger.info(f'基准点数量: {mark_point_num_after}')
    utils.click_by_png(config.BOARD_REDUCE)
    board_num_after = utils.count_symbol_on_region(config.BOARD_BOARD)
    if board_num_before == board_num_after and mark_point_num_before != mark_point_num_after:
        logger.info('拼版被删除且基准点被保留')
    else:
        logger.error('基准点未被保留/拼版未被删除')
        raise Exception('基准点未被保留/拼版未被删除')
    utils.close_aoi()
# @utils.screenshot_error_to_excel()
# def lxbj_019_01():
#     utils.check_and_launch_aoi()
#     utils.check_xy_max_extension()
#     # 1、打开任一编辑过的job
#     # 2、双击元件，进入元件编辑界面
#     utils.ensure_in_edit_mode()
#     # 3、新增3d共面性算法，查看是否有搜索范围
#     utils.add_window()
#     utils.click_by_png(config.COPLANARITY_3D)
#     utils.click_by_png(config.YES)
#     time.sleep(10)
#     # 4、删除元件所有窗口，导入元件库/标准库，查看是否有搜索范围
#     pyautogui.hotkey("ctrl", "a")
#     pyautogui.press("delete")
#     time.sleep(1)
#     pyautogui.press("enter")
#     # 5、重复3、4操作，不同算法


@utils.screenshot_error_to_excel()
def lxbj_020_01():
    # 1、打开编辑过job，任选一个元件，双击，进入元件编辑界面
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 2、整板图上，右键点击元件信息，改变元件角度为0°
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)
    utils.write_text_textbox(config.ROTATION_ANGLE, write_content="0.0")
    utils.click_by_png(config.PROGRAM_ATTRIBUTE_CLOSE)
    time.sleep(1)
    reference_frame_points_list = utils.get_frame_points(config.COMPONENT_REGION, (0, 0, 255))
    # 3、点击本体cad或本体上的算法，右键点击新增对象，新增相同大小检测框，或手动添加算法
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.ADD_OBJECT)
    utils.click_by_png(config.ADD_SAME_CHECK_WINDOW)
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    # 4、查看检测框方向大小 是否与步骤3的参照框一致
    time.sleep(5)
    check_frame_points_list = utils.get_frame_points(config.COMPONENT_REGION, (0, 0, 255))
    if utils.points_are_similar(reference_frame_points_list, check_frame_points_list):
        logger.info("检测框方向大小与参照框一致")
    else:
        logger.error("检测框方向大小与参照框不一致")
        raise Exception("检测框方向大小与参照框不一致")

@utils.screenshot_error_to_excel()
def lxbj_020_02():
    # 1、打开编辑过job，任选一个元件，双击，进入元件编辑界面
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 2、整板图上，右键点击元件信息，改变元件角度为45°
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)
    utils.write_text_textbox(config.ROTATION_ANGLE, write_content="45.0")
    utils.click_by_png(config.PROGRAM_ATTRIBUTE_CLOSE)
    time.sleep(1)
    reference_frame_points_list = utils.get_frame_points(config.COMPONENT_REGION, (0, 0, 255))
    # 3、点击本体cad或本体上的算法，右键点击新增对象，新增相同大小检测框，或手动添加算法
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.ADD_OBJECT)
    utils.click_by_png(config.ADD_SAME_CHECK_WINDOW)
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    # 4、查看检测框方向大小 是否与步骤3的参照框一致
    time.sleep(5)
    check_frame_points_list = utils.get_frame_points(config.COMPONENT_REGION, (0, 0, 255))
    if utils.points_are_similar(reference_frame_points_list, check_frame_points_list):
        logger.info("检测框方向大小与参照框一致")
    else:
        logger.error("检测框方向大小与参照框不一致")
        raise Exception("检测框方向大小与参照框不一致")
@utils.screenshot_error_to_excel()
def lxbj_020_03():
    # 1、打开编辑过job，任选一个元件，双击，进入元件编辑界面
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 2、整板图上，右键点击元件信息，改变元件角度为90°
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)
    utils.write_text_textbox(config.ROTATION_ANGLE, write_content="90")
    utils.click_by_png(config.PROGRAM_ATTRIBUTE_CLOSE)
    time.sleep(1)
    reference_frame_points_list = utils.get_frame_points(config.COMPONENT_REGION, (0, 0, 255))
    # 3、点击本体cad或本体上的算法，右键点击新增对象，新增相同大小检测框，或手动添加算法
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.ADD_OBJECT)
    utils.click_by_png(config.ADD_SAME_CHECK_WINDOW)
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    # 4、查看检测框方向大小 是否与步骤3的参照框一致
    time.sleep(5)
    check_frame_points_list = utils.get_frame_points(config.COMPONENT_REGION, (0, 0, 255))
    if utils.points_are_similar(reference_frame_points_list, check_frame_points_list):
        logger.info("检测框方向大小与参照框一致")
    else:
        logger.error("检测框方向大小与参照框不一致")
        raise Exception("检测框方向大小与参照框不一致")
@utils.screenshot_error_to_excel()
def lxbj_020_04():
    # 1、打开编辑过job，任选一个元件，双击，进入元件编辑界面
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 2、整板图上，右键点击元件信息，改变元件角度为135°
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)
    utils.write_text_textbox(config.ROTATION_ANGLE, write_content="135")
    utils.click_by_png(config.PROGRAM_ATTRIBUTE_CLOSE)
    time.sleep(1)
    reference_frame_points_list = utils.get_frame_points(config.COMPONENT_REGION, (0, 0, 255))
    # 3、点击本体cad或本体上的算法，右键点击新增对象，新增相同大小检测框，或手动添加算法
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.ADD_OBJECT)
    utils.click_by_png(config.ADD_SAME_CHECK_WINDOW)
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    # 4、查看检测框方向大小 是否与步骤3的参照框一致
    time.sleep(5)
    check_frame_points_list = utils.get_frame_points(config.COMPONENT_REGION, (0, 0, 255))
    if utils.points_are_similar(reference_frame_points_list, check_frame_points_list):
        logger.info("检测框方向大小与参照框一致")
    else:
        logger.error("检测框方向大小与参照框不一致")
        raise Exception("检测框方向大小与参照框不一致")
@utils.screenshot_error_to_excel()
def lxbj_020_05():
    # 1、打开编辑过job，任选一个元件，双击，进入元件编辑界面
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 2、整板图上，右键点击元件信息，改变元件角度为180°
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)
    utils.write_text_textbox(config.ROTATION_ANGLE, write_content="180")
    utils.click_by_png(config.PROGRAM_ATTRIBUTE_CLOSE)
    time.sleep(1)
    reference_frame_points_list = utils.get_frame_points(config.COMPONENT_REGION, (0, 0, 255))
    # 3、点击本体cad或本体上的算法，右键点击新增对象，新增相同大小检测框，或手动添加算法
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.ADD_OBJECT)
    utils.click_by_png(config.ADD_SAME_CHECK_WINDOW)
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    # 4、查看检测框方向大小 是否与步骤3的参照框一致
    time.sleep(5)
    check_frame_points_list = utils.get_frame_points(config.COMPONENT_REGION, (0, 0, 255))
    if utils.points_are_similar(reference_frame_points_list, check_frame_points_list):
        logger.info("检测框方向大小与参照框一致")
    else:
        logger.error("检测框方向大小与参照框不一致")
        raise Exception("检测框方向大小与参照框不一致")
@utils.screenshot_error_to_excel()
def lxbj_020_06():
    # 1、打开编辑过job，任选一个元件，双击，进入元件编辑界面
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 2、整板图上，右键点击元件信息，改变元件角度为225°
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)
    utils.write_text_textbox(config.ROTATION_ANGLE, write_content="225")
    utils.click_by_png(config.PROGRAM_ATTRIBUTE_CLOSE)
    time.sleep(1)
    reference_frame_points_list = utils.get_frame_points(config.COMPONENT_REGION, (0, 0, 255))
    # 3、点击本体cad或本体上的算法，右键点击新增对象，新增相同大小检测框，或手动添加算法
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.ADD_OBJECT)
    utils.click_by_png(config.ADD_SAME_CHECK_WINDOW)
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    # 4、查看检测框方向大小 是否与步骤3的参照框一致
    time.sleep(5)
    check_frame_points_list = utils.get_frame_points(config.COMPONENT_REGION, (0, 0, 255))
    if utils.points_are_similar(reference_frame_points_list, check_frame_points_list):
        logger.info("检测框方向大小与参照框一致")
    else:
        logger.error("检测框方向大小与参照框不一致")
        raise Exception("检测框方向大小与参照框不一致")
@utils.screenshot_error_to_excel()
def lxbj_020_07():
    # 1、打开编辑过job，任选一个元件，双击，进入元件编辑界面
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 2、整板图上，右键点击元件信息，改变元件角度为270°
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)
    utils.write_text_textbox(config.ROTATION_ANGLE, write_content="270")
    utils.click_by_png(config.PROGRAM_ATTRIBUTE_CLOSE)
    time.sleep(1)
    reference_frame_points_list = utils.get_frame_points(config.COMPONENT_REGION, (0, 0, 255))
    # 3、点击本体cad或本体上的算法，右键点击新增对象，新增相同大小检测框，或手动添加算法
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.ADD_OBJECT)
    utils.click_by_png(config.ADD_SAME_CHECK_WINDOW)
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    # 4、查看检测框方向大小 是否与步骤3的参照框一致
    time.sleep(5)
    check_frame_points_list = utils.get_frame_points(config.COMPONENT_REGION, (0, 0, 255))
    if utils.points_are_similar(reference_frame_points_list, check_frame_points_list):
        logger.info("检测框方向大小与参照框一致")
    else:
        logger.error("检测框方向大小与参照框不一致")
        raise Exception("检测框方向大小与参照框不一致")
@utils.screenshot_error_to_excel()
def lxbj_020_08():
    # 1、打开编辑过job，任选一个元件，双击，进入元件编辑界面
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 2、整板图上，右键点击元件信息，改变元件角度为315°
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)
    utils.write_text_textbox(config.ROTATION_ANGLE, write_content="315")
    utils.click_by_png(config.PROGRAM_ATTRIBUTE_CLOSE)
    time.sleep(1)
    reference_frame_points_list = utils.get_frame_points(config.COMPONENT_REGION, (0, 0, 255))
    # 3、点击本体cad或本体上的算法，右键点击新增对象，新增相同大小检测框，或手动添加算法
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.ADD_OBJECT)
    utils.click_by_png(config.ADD_SAME_CHECK_WINDOW)
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    # 4、查看检测框方向大小 是否与步骤3的参照框一致
    time.sleep(5)
    check_frame_points_list = utils.get_frame_points(config.COMPONENT_REGION, (0, 0, 255))
    if utils.points_are_similar(reference_frame_points_list, check_frame_points_list):
        logger.info("检测框方向大小与参照框一致")
    else:
        logger.error("检测框方向大小与参照框不一致")
        raise Exception("检测框方向大小与参照框不一致")
@utils.screenshot_error_to_excel()
def lxbj_020_09():
    # 1、打开编辑过job，任选一个元件，双击，进入元件编辑界面
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 2、整板图上，右键点击元件信息，改变元件角度为0°-45°范围任一角度
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)  
    random_angle = str(random.uniform(0, 45))
    utils.write_text_textbox(config.ROTATION_ANGLE, write_content=random_angle)
    utils.click_by_png(config.PROGRAM_ATTRIBUTE_CLOSE)
    time.sleep(1)
    reference_frame_points_list = utils.get_frame_points(config.COMPONENT_REGION, (0, 0, 255))  
    # 3、点击本体cad或本体上的算法，右键点击新增对象，新增相同大小检测框，或手动添加算法
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.ADD_OBJECT)
    utils.click_by_png(config.ADD_SAME_CHECK_WINDOW)
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    # 4、查看检测框方向大小 是否与步骤3的参照框一致
    time.sleep(5)
    check_frame_points_list = utils.get_frame_points(config.COMPONENT_REGION, (0, 0, 255))
    if utils.points_are_similar(reference_frame_points_list, check_frame_points_list):
        logger.info("检测框方向大小与参照框一致")
    else:
        logger.error("检测框方向大小与参照框不一致")
        raise Exception("检测框方向大小与参照框不一致")

@utils.screenshot_error_to_excel()
def lxbj_020_10():
    # 1、打开编辑过job，任选一个元件，双击，进入元件编辑界面
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 2、整板图上，右键点击元件信息，改变元件角度为45°-90°范围任一角度
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)  
    random_angle = str(random.uniform(45, 90))
    utils.write_text_textbox(config.ROTATION_ANGLE, write_content=random_angle)
    utils.click_by_png(config.PROGRAM_ATTRIBUTE_CLOSE)
    time.sleep(1)
    reference_frame_points_list = utils.get_frame_points(config.COMPONENT_REGION, (0, 0, 255))  
    # 3、点击本体cad或本体上的算法，右键点击新增对象，新增相同大小检测框，或手动添加算法
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.ADD_OBJECT)
    utils.click_by_png(config.ADD_SAME_CHECK_WINDOW)
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    # 4、查看检测框方向大小 是否与步骤3的参照框一致
    time.sleep(5)
    check_frame_points_list = utils.get_frame_points(config.COMPONENT_REGION, (0, 0, 255))
    if utils.points_are_similar(reference_frame_points_list, check_frame_points_list):
        logger.info("检测框方向大小与参照框一致")
    else:
        logger.error("检测框方向大小与参照框不一致")
        raise Exception("检测框方向大小与参照框不一致")
@utils.screenshot_error_to_excel()
def lxbj_020_11():
    # 1、打开编辑过job，任选一个元件，双击，进入元件编辑界面
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 2、整板图上，右键点击元件信息，改变元件角度为90°-135°范围任一角度
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)  
    random_angle = str(random.uniform(90, 135))
    utils.write_text_textbox(config.ROTATION_ANGLE, write_content=random_angle)
    utils.click_by_png(config.PROGRAM_ATTRIBUTE_CLOSE)
    time.sleep(1)
    reference_frame_points_list = utils.get_frame_points(config.COMPONENT_REGION, (0, 0, 255))  
    # 3、点击本体cad或本体上的算法，右键点击新增对象，新增相同大小检测框，或手动添加算法
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.ADD_OBJECT)
    utils.click_by_png(config.ADD_SAME_CHECK_WINDOW)
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    # 4、查看检测框方向大小 是否与步骤3的参照框一致
    time.sleep(5)
    check_frame_points_list = utils.get_frame_points(config.COMPONENT_REGION, (0, 0, 255))
    if utils.points_are_similar(reference_frame_points_list, check_frame_points_list):
        logger.info("检测框方向大小与参照框一致")
    else:
        logger.error("检测框方向大小与参照框不一致")
        raise Exception("检测框方向大小与参照框不一致")
@utils.screenshot_error_to_excel()
def lxbj_020_12():
    # 1、打开编辑过job，任选一个元件，双击，进入元件编辑界面
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 2、整板图上，右键点击元件信息，改变元件角度为135°-180°范围任一角度
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)  
    random_angle = str(random.uniform(135, 180))
    utils.write_text_textbox(config.ROTATION_ANGLE, write_content=random_angle)
    utils.click_by_png(config.PROGRAM_ATTRIBUTE_CLOSE)
    time.sleep(1)
    reference_frame_points_list = utils.get_frame_points(config.COMPONENT_REGION, (0, 0, 255))  
    # 3、点击本体cad或本体上的算法，右键点击新增对象，新增相同大小检测框，或手动添加算法
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.ADD_OBJECT)
    utils.click_by_png(config.ADD_SAME_CHECK_WINDOW)
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    # 4、查看检测框方向大小 是否与步骤3的参照框一致
    time.sleep(5)
    check_frame_points_list = utils.get_frame_points(config.COMPONENT_REGION, (0, 0, 255))
    if utils.points_are_similar(reference_frame_points_list, check_frame_points_list):
        logger.info("检测框方向大小与参照框一致")
    else:
        logger.error("检测框方向大小与参照框不一致")
        raise Exception("检测框方向大小与参照框不一致")
@utils.screenshot_error_to_excel()
def lxbj_020_13():
    # 1、打开编辑过job，任选一个元件，双击，进入元件编辑界面
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 2、整板图上，右键点击元件信息，改变元件角度为180°-225°范围任一角度
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)  
    random_angle = str(random.uniform(180, 225))
    utils.write_text_textbox(config.ROTATION_ANGLE, random_angle)
    utils.click_by_png(config.PROGRAM_ATTRIBUTE_CLOSE)
    time.sleep(1)
    reference_frame_points_list = utils.get_frame_points(config.COMPONENT_REGION, (0, 0, 255))  
    # 3、点击本体cad或本体上的算法，右键点击新增对象，新增相同大小检测框，或手动添加算法
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.ADD_OBJECT)
    utils.click_by_png(config.ADD_SAME_CHECK_WINDOW)
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    # 4、查看检测框方向大小 是否与步骤3的参照框一致
    time.sleep(5)
    check_frame_points_list = utils.get_frame_points(config.COMPONENT_REGION, (0, 0, 255))
    if utils.points_are_similar(reference_frame_points_list, check_frame_points_list):
        logger.info("检测框方向大小与参照框一致")
    else:
        logger.error("检测框方向大小与参照框不一致")
        raise Exception("检测框方向大小与参照框不一致")
@utils.screenshot_error_to_excel()
def lxbj_020_14():
    # 1、打开编辑过job，任选一个元件，双击，进入元件编辑界面
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 2、整板图上，右键点击元件信息，改变元件角度为225°-270°范围任一角度
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)  
    random_angle = str(random.uniform(225, 270))
    utils.write_text_textbox(config.ROTATION_ANGLE, write_content=random_angle)
    utils.click_by_png(config.PROGRAM_ATTRIBUTE_CLOSE)
    time.sleep(1)
    reference_frame_points_list = utils.get_frame_points(config.COMPONENT_REGION, (0, 0, 255))  
    # 3、点击本体cad或本体上的算法，右键点击新增对象，新增相同大小检测框，或手动添加算法
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.ADD_OBJECT)
    utils.click_by_png(config.ADD_SAME_CHECK_WINDOW)
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    # 4、查看检测框方向大小 是否与步骤3的参照框一致
    time.sleep(5)
    check_frame_points_list = utils.get_frame_points(config.COMPONENT_REGION, (0, 0, 255))
    if utils.points_are_similar(reference_frame_points_list, check_frame_points_list):
        logger.info("检测框方向大小与参照框一致")
    else:
        logger.error("检测框方向大小与参照框不一致")
        raise Exception("检测框方向大小与参照框不一致")
@utils.screenshot_error_to_excel()
def lxbj_020_15():
    # 1、打开编辑过job，任选一个元件，双击，进入元件编辑界面
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 2、整板图上，右键点击元件信息，改变元件角度为270°-315°范围任一角度
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)  
    random_angle = str(random.uniform(270, 315))
    utils.write_text_textbox(config.ROTATION_ANGLE, random_angle)
    utils.click_by_png(config.PROGRAM_ATTRIBUTE_CLOSE)
    time.sleep(1)
    reference_frame_points_list = utils.get_frame_points(config.COMPONENT_REGION, (0, 0, 255))  
    # 3、点击本体cad或本体上的算法，右键点击新增对象，新增相同大小检测框，或手动添加算法
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.ADD_OBJECT)
    utils.click_by_png(config.ADD_SAME_CHECK_WINDOW)
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    # 4、查看检测框方向大小 是否与步骤3的参照框一致
    time.sleep(5)
    check_frame_points_list = utils.get_frame_points(config.COMPONENT_REGION, (0, 0, 255))
    if utils.points_are_similar(reference_frame_points_list, check_frame_points_list):
        logger.info("检测框方向大小与参照框一致")
    else:
        logger.error("检测框方向大小与参照框不一致")
        raise Exception("检测框方向大小与参照框不一致")
@utils.screenshot_error_to_excel()
def lxbj_020_16():
    # 1、打开编辑过job，任选一个元件，双击，进入元件编辑界面
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 2、整板图上，右键点击元件信息，改变元件角度为315°-0°范围任一角度
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)  
    random_angle = str(random.uniform(315, 360))
    utils.write_text_textbox(config.ROTATION_ANGLE, write_content=random_angle)
    utils.click_by_png(config.PROGRAM_ATTRIBUTE_CLOSE)
    time.sleep(1)
    reference_frame_points_list = utils.get_frame_points(config.COMPONENT_REGION, (0, 0, 255))  
    # 3、点击本体cad或本体上的算法，右键点击新增对象，新增相同大小检测框，或手动添加算法
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.ADD_OBJECT)
    utils.click_by_png(config.ADD_SAME_CHECK_WINDOW)
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    # 4、查看检测框方向大小 是否与步骤3的参照框一致
    time.sleep(5)
    check_frame_points_list = utils.get_frame_points(config.COMPONENT_REGION, (0, 0, 255))
    if utils.points_are_similar(reference_frame_points_list, check_frame_points_list):
        logger.info("检测框方向大小与参照框一致")
    else:
        logger.error("检测框方向大小与参照框不一致")
        raise Exception("检测框方向大小与参照框不一致")
# @utils.screenshot_error_to_excel()
# def lxbj_020_17():
#     # 1、打开编辑过job，任选一个有引脚元件，双击，进入元件编辑界面
#     utils.check_and_launch_aoi()
#     utils.ensure_in_edit_mode()
#     # 2、整板图上，右键点击元件信息，改变元件角度为0°
#     # 3、点击引脚或引脚上的算法，右键点击新增对象，新增相同大小检测框，或手动添加算法
#     # 4、查看检测框方向大小 是否与步骤3的参照框一致

# @utils.screenshot_error_to_excel()
# def lxbj_020_18():
#     # 1、打开编辑过job，任选一个元件，双击，进入元件编辑界面
#     utils.check_and_launch_aoi()
#     utils.ensure_in_edit_mode()
#     # 2、整板图上，右键点击元件信息，改变元件角度为45°
#     # 3、点击引脚或引脚上的算法，右键点击新增对象，新增相同大小检测框，或手动添加算法
#     # 4、查看检测框方向大小 是否与步骤3的参照框一致

# @utils.screenshot_error_to_excel()
# def lxbj_020_19():
#     # 1、打开编辑过job，任选一个元件，双击，进入元件编辑界面
#     utils.check_and_launch_aoi()
#     utils.ensure_in_edit_mode()
#     # 2、整板图上，右键点击元件信息，改变元件角度为90°
#     # 3、点击引脚或引脚上的算法，右键点击新增对象，新增相同大小检测框，或手动添加算法
#     # 4、查看检测框方向大小 是否与步骤3的参照框一致

# @utils.screenshot_error_to_excel()
# def lxbj_020_20():
#     # 1、打开编辑过job，任选一个元件，双击，进入元件编辑界面
#     utils.check_and_launch_aoi()
#     utils.ensure_in_edit_mode()
#     # 2、整板图上，右键点击元件信息，改变元件角度为135°
#     # 3、点击引脚或引脚上的算法，右键点击新增对象，新增相同大小检测框，或手动添加算法
#     # 4、查看检测框方向大小 是否与步骤3的参照框一致
# @utils.screenshot_error_to_excel()
# def lxbj_020_21():
#     # 1、打开编辑过job，任选一个元件，双击，进入元件编辑界面
#     utils.check_and_launch_aoi()
#     utils.ensure_in_edit_mode()
#     # 2、整板图上，右键点击元件信息，改变引脚角度为180°
#     # 3、点击引脚或引脚上的算法，右键点击新增对象，新增相同大小检测框，或手动添加算法
#     # 4、查看检测框方向大小 是否与步骤3的参照框一致
# @utils.screenshot_error_to_excel()
# def lxbj_020_22():
#     # 1、打开编辑过job，任选一个元件，双击，进入元件编辑界面
#     utils.check_and_launch_aoi()
#     utils.ensure_in_edit_mode()
#     # 2、整板图上，右键点击元件信息，改变元件角度为225°
#     # 3、点击引脚或引脚上的算法，右键点击新增对象，新增相同大小检测框，添加算法
#     # 4、查看检测框方向大小 是否与步骤3的参照框一致
# @utils.screenshot_error_to_excel()
# def lxbj_020_23():
#     # 1、打开编辑过job，任选一个元件，双击，进入元件编辑界面
#     utils.check_and_launch_aoi()
#     utils.ensure_in_edit_mode()
#     # 2、整板图上，右键点击元件信息，改变元件角度为270°
#     # 3、点击引脚或引脚上的算法，右键点击新增对象，新增相同大小检测框，或手动添加算法
#     # 4、查看检测框方向大小 是否与步骤3的参照框一致
# @utils.screenshot_error_to_excel()
# def lxbj_020_24():
#     # 1、打开编辑过job，任选一个元件，双击，进入元件编辑界面
#     utils.check_and_launch_aoi()
#     utils.ensure_in_edit_mode()
#     # 2、整板图上，右键点击元件信息，改变元件角度为315°
#     # 3、点击引脚或引脚上的算法，右键点击新增对象，新增相同大小检测框，或手动添加算法
#     # 4、查看检测框方向大小 是否与步骤3的参照框一致
# @utils.screenshot_error_to_excel()
# def lxbj_020_25():
#     # 1、打开编辑过job，任选一个元件，双击，进入元件编辑界面
#     utils.check_and_launch_aoi()
#     utils.ensure_in_edit_mode()
#     # 2、整板图上，右键点击元件信息，改变引脚角度为0°-45°范围任一角度
#     # 3、点击引脚或引脚上的算法，右键点击新增对象，新增相同大小检测框，或手动添加算法
#     # 4、查看检测框方向大小 是否与步骤3的参照框一致
# @utils.screenshot_error_to_excel()
# def lxbj_020_26():
#     # 1、打开编辑过job，任选一个元件，双击，进入元件编辑界面
#     utils.check_and_launch_aoi()
#     utils.ensure_in_edit_mode()
#     # 2、整板图上，右键点击元件信息，改变元件角度为45°-90°范围任一角度
#     # 3、点击引脚或引脚上的算法，右键点击新增对象，新增相同大小检测框，或手动添加算法
#     # 4、查看检测框方向大小 是否与步骤3的参照框一致
# @utils.screenshot_error_to_excel()
# def lxbj_020_27():
#     # 1、打开编辑过job，任选一个元件，双击，进入元件编辑界面
#     utils.check_and_launch_aoi()
#     utils.ensure_in_edit_mode()
#     # 2、整板图上，右键点击元件信息，改变元件角度为90°-135°范围任一角度
#     # 3、点击引脚或引脚上的算法，右键点击新增对象，新增相同大小检测框，或手动添加算法
#     # 4、查看检测框方向大小 是否与步骤3的参照框一致
# @utils.screenshot_error_to_excel()
# def lxbj_020_28():
#     # 1、打开编辑过job，任选一个元件，双击，进入元件编辑界面
#     utils.check_and_launch_aoi()
#     utils.ensure_in_edit_mode()
#     # 2、整板图上，右键点击元件信息，改变元件角度为135°-180°范围任一角度
#     # 3、点击本体cad或本体上的算法，右键点击新增对象，新增相同大小检测框，或手动添加算法
#     # 4、查看检测框方向大小 是否与步骤3的参照框一致
# @utils.screenshot_error_to_excel()
# def lxbj_020_29():
#     # 1、打开编辑过job，任选一个元件，双击，进入元件编辑界面
#     utils.check_and_launch_aoi()
#     utils.ensure_in_edit_mode()
#     # 2、整板图上，右键点击元件信息，改变元件角度为180°-225°范围任一角度
#     # 3、点击引脚或引脚上的算法，右键点击新增对象，新增相同大小检测框，或手动添加算法
#     # 4、查看检测框方向大小 是否与步骤3的参照框一致
# @utils.screenshot_error_to_excel()
# def lxbj_020_30():
#     # 1、打开编辑过job，任选一个元件，双击，进入元件编辑界面
#     utils.check_and_launch_aoi()
#     utils.ensure_in_edit_mode()
#     # 2、整板图上，右键点击元件信息，改变元件角度为225°-270°范围任一角度
#     # 3、点击引脚或引脚上的算法，右键点击新增对象，新增相同大小检测框，或手动添加算法
#     # 4、查看检测框方向大小 是否与步骤3的参照框一致
# @utils.screenshot_error_to_excel()
# def lxbj_020_31():
#     # 1、打开编辑过job，任选一个元件，双击，进入元件编辑界面
#     utils.check_and_launch_aoi()
#     utils.ensure_in_edit_mode()
#     # 2、整板图上，右键点击元件信息，改变元件角度为270°-315°范围任一角度
#     # 3、点击引脚或引脚上的算法，右键点击新增对象，新增相同大小检测框，或手动添加算法
#     # 4、查看检测框方向大小 是否与步骤3的参照框一致
# @utils.screenshot_error_to_excel()
# def lxbj_020_32():
#     # 1、打开编辑过job，任选一个元件，双击，进入元件编辑界面
#     utils.check_and_launch_aoi()
#     utils.ensure_in_edit_mode()
#     # 2、整板图上，右键点击元件信息，改变元件角度为315°-0°范围任一角度
#     # 3、点击引脚或引脚上的算法，右键点击新增对象，新增相同大小检测框，或手动添加算法
#     # 4、查看检测框方向大小 是否与步骤3的参照框一致

@utils.screenshot_error_to_excel()
def lxbj_021_01():
    # 1.【设置】-【硬件设置】-【UI配置】-【程序设置】-勾选不允许同步相同的封装
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_package(True)
    utils.ensure_in_edit_mode()

    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的参数--返回-选是
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    time.sleep(7)

    # 修改元件参数
    pyautogui.hotkey("ctrl", "a")
    time.sleep(3)
    pyautogui.press("delete")
    time.sleep(3)
    pyautogui.press("enter")
    time.sleep(3)
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(7)
    pyautogui.press("escape")
    time.sleep(3)

    utils.click_by_png(config.EDIT_BACK)
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，仍出现可选项")
    time.sleep(1)
    pyautogui.press("enter")
    if not utils.search_symbol(config.BOARD_AUTO,tolerance=0.75):
        raise Exception("疑似未返回整版界面")
    time.sleep(3)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数未同步修改")
   
    # 封装下其他料号元件未修改
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_02():
    # 1.【设置】-【硬件设置】-【UI配置】-【程序设置】-勾选不允许同步相同的封装
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_package(True)
    utils.ensure_in_edit_mode()
    
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的算法框的大小--返回-选是
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    if utils.search_symbol(config.QUESTION_MARK, 5):
        pyautogui.press("enter")
    time.sleep(7)
    # 修改框大小
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)

    pyautogui.hotkey("ctrl", "tab")
    time.sleep(3)
    utils.expand_choose_box()
    pyautogui.press("escape")
    time.sleep(3)

    utils.click_by_png(config.EDIT_BACK)
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，仍出现可选项")
    pyautogui.press("enter")
    if not utils.search_symbol(config.BOARD_AUTO,tolerance=0.75):
        raise Exception("疑似未返回整版界面")
    time.sleep(3)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，仍出现可选项")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(5)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数未同步修改")
   
    # 封装下其他料号元件未修改
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_03():
    # 1.【设置】-【硬件设置】-【UI配置】-【程序设置】-勾选不允许同步相同的封装
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_package(True)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的参数--切换元件-选是
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    time.sleep(7)

    # 修改元件参数
    pyautogui.hotkey("ctrl", "a")
    time.sleep(3)
    pyautogui.press("delete")
    time.sleep(3)
    pyautogui.press("enter")
    time.sleep(3)
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(7)
    pyautogui.press("escape")
    time.sleep(3)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，仍出现可选项")
    pyautogui.press("enter")
    time.sleep(5)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数未同步修改")
    
    # 封装下其他料号元件未修改
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_04():
    # 1.【设置】-【硬件设置】-【UI配置】-【程序设置】-勾选不允许同步相同的封装
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_package(True)
    utils.ensure_in_edit_mode()

    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的算法框的大小--切换元件-选是
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    if utils.search_symbol(config.QUESTION_MARK, 5):
        pyautogui.press("enter")
    time.sleep(7)

    # 修改框大小
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)

    pyautogui.hotkey("ctrl", "tab")
    time.sleep(3)
    utils.expand_choose_box()
    pyautogui.press("escape")
    time.sleep(3)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，仍出现可选项")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(5)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数未同步修改")
   
    # 封装下其他料号元件未修改
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 400)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_05():
    # 1.【设置】-【硬件设置】-【UI配置】-【程序设置】-勾选不允许同步相同的封装
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_package(True)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的参数--测试当前分组--切换到同料号下其他元件
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    if utils.search_symbol(config.QUESTION_MARK, 5):
        pyautogui.press("enter")
    time.sleep(7)

    # 修改元件参数
    pyautogui.hotkey("ctrl", "a")
    time.sleep(3)
    pyautogui.press("delete")
    time.sleep(3)
    pyautogui.press("enter")
    time.sleep(3)
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(7)
    pyautogui.press("escape")
    time.sleep(3)

    # 测试当前分组
    utils.is_checked((66,255),(78,267), True)
    utils.click_by_png(config.TEST_GROUP)
    while utils.search_symbol(config.TESTING_COMPONENT):
        time.sleep(3)
    time.sleep(7)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    if utils.search_symbol(config.QUESTION_MARK):
        raise Exception("不应出现弹框")    
    time.sleep(7)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)    
    if utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数未同步修改")
   
    # 封装下其他料号元件未修改
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_06():
    # 1.【设置】-【硬件设置】-【UI配置】-【程序设置】-勾选不允许同步相同的封装
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_package(True)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的算法框的大小--测试当前分组--切换到同料号下其他元件
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    if utils.search_symbol(config.QUESTION_MARK, 5):
        pyautogui.press("enter")
    time.sleep(7)

    # 修改框大小
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)

    pyautogui.hotkey("ctrl", "tab")
    time.sleep(3)
    utils.expand_choose_box()
    pyautogui.press("escape")
    time.sleep(3)    

    # 测试当前分组
    utils.is_checked((66,255),(78,267), True)
    utils.click_by_png(config.TEST_GROUP)
    while utils.search_symbol(config.TESTING_COMPONENT):
        time.sleep(3)
    time.sleep(7)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        time.sleep(1)
        pyautogui.press("enter")
    time.sleep(5)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数未同步修改")
   
    # 封装下其他料号元件未修改
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_07():
    # 1.【设置】-【硬件设置】-【UI配置】-【程序设置】-勾选不允许同步相同的封装
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_package(True)
    utils.ensure_in_edit_mode()

    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的参数--测试当前整板--切换到同料号下其他元件
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    if utils.search_symbol(config.QUESTION_MARK, 5):
        pyautogui.press("enter")
    time.sleep(7)

    # 修改元件参数
    pyautogui.hotkey("ctrl", "a")
    time.sleep(3)
    pyautogui.press("delete")
    time.sleep(3)
    pyautogui.press("enter")
    time.sleep(3)
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(7)
    pyautogui.press("escape")
    time.sleep(3)

    # 测试当前整版
    utils.is_checked((66,255),(78,267), True)
    utils.click_by_png(config.TEST_BOARD)
    while utils.search_symbol(config.TESTING_COMPONENT):
        time.sleep(3)
    time.sleep(7)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    if utils.search_symbol(config.QUESTION_MARK):
        raise Exception("不应出现弹框")    
    time.sleep(7)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数未同步修改")
   
    # 封装下其他料号元件未修改
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_08():
    # 1.【设置】-【硬件设置】-【UI配置】-【程序设置】-勾选不允许同步相同的封装
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_package(True)
    utils.ensure_in_edit_mode()

    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的算法框的大小--测试当前整板--切换到同料号下其他元件
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    if utils.search_symbol(config.QUESTION_MARK, 5):
        pyautogui.press("enter")
    time.sleep(7)

    # 修改框大小
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)

    pyautogui.hotkey("ctrl", "tab")
    time.sleep(3)
    utils.expand_choose_box()
    pyautogui.press("escape")
    time.sleep(3)   

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    if utils.search_symbol(config.QUESTION_MARK):
        pyautogui.press("enter")
        time.sleep(7)    
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数未同步修改")
   
    # 封装下其他料号元件未修改
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_09():
    # 1.【设置】-【硬件设置】-【UI配置】-【程序设置】-勾选不允许同步相同的封装
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_package(True)
    utils.ensure_in_edit_mode()

    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的参数--返回
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    time.sleep(7)

    # 修改元件参数
    pyautogui.hotkey("ctrl", "a")
    time.sleep(3)
    pyautogui.press("delete")
    time.sleep(3)
    pyautogui.press("enter")
    time.sleep(3)
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(7)
    pyautogui.press("escape")
    time.sleep(3)

    utils.click_by_png(config.EDIT_BACK)
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，仍出现可选项")
    # 3.选否
    utils.click_by_png(config.NO)
    if not utils.search_symbol(config.BOARD_AUTO,tolerance=0.75):
        raise Exception("疑似未返回整版界面")
    time.sleep(3)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数被同步修改")
   
    # 4.再次进入元件编辑界面，查看此元件参数
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_10():
    # 1.【设置】-【硬件设置】-【UI配置】-【程序设置】-勾选不允许同步相同的封装
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_package(True)
    utils.ensure_in_edit_mode()

    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的算法框的大小--返回
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    time.sleep(7)

    # 修改框大小
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)

    pyautogui.hotkey("ctrl", "tab")
    time.sleep(3)
    utils.expand_choose_box()
    pyautogui.press("escape")
    time.sleep(3)   

    utils.click_by_png(config.EDIT_BACK)
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，仍出现可选项")
    # 3.选否
    utils.click_by_png(config.NO)
    if not utils.search_symbol(config.BOARD_AUTO,tolerance=0.75):
        raise Exception("疑似未返回整版界面")
    time.sleep(3)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    
    if not utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数被同步修改")
   
    # 4.再次进入元件编辑界面，查看此元件算法框
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_11():
    # 1.【设置】-【硬件设置】-【UI配置】-【程序设置】-勾选不允许同步相同的封装
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_package(True)
    utils.ensure_in_edit_mode()

    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的参数--左侧列表选择某个元件切换
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    time.sleep(7)

    # 修改元件参数
    pyautogui.hotkey("ctrl", "a")
    time.sleep(3)
    pyautogui.press("delete")
    time.sleep(3)
    pyautogui.press("enter")
    time.sleep(3)
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(7)
    pyautogui.press("escape")
    time.sleep(3)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    if not utils.search_symbol(config.QUESTION_MARK):
        raise Exception("出现未知错误，未出现弹框")
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，仍出现可选项")
    # 3.选否
    utils.click_by_png(config.NO)
    time.sleep(5)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数被同步修改")

    # 4.再次回到修改那个元件
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_12():
    # 1.【设置】-【硬件设置】-【UI配置】-【程序设置】-勾选不允许同步相同的封装
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_package(True)
    utils.ensure_in_edit_mode()

    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的算法框的大小--左侧列表选择某个元件切换
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    if utils.search_symbol(config.QUESTION_MARK, 5):
        pyautogui.press("enter")
    time.sleep(7)

    # 修改框大小
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)

    pyautogui.hotkey("ctrl", "tab")
    time.sleep(3)
    utils.expand_choose_box()
    pyautogui.press("escape")
    time.sleep(3)   

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    if not utils.search_symbol(config.QUESTION_MARK):
        raise Exception("出现未知错误，未出现弹框")
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，仍出现可选项")
    # 3.选否
    utils.click_by_png(config.NO)
    time.sleep(5)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if not utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数被同步修改")
   
    # 封装下其他料号元件未修改
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_13():
    # 1.【设置】-【硬件设置】-【UI配置】-【程序设置】-勾选不允许同步相同的封装+勾选默认同步封装
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(True,True)
    utils.ensure_in_edit_mode()
    
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的参数--返回-选是
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    time.sleep(7)

    # 修改元件参数
    pyautogui.hotkey("ctrl", "a")
    time.sleep(3)
    pyautogui.press("delete")
    time.sleep(3)
    pyautogui.press("enter")
    time.sleep(3)
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(7)
    pyautogui.press("escape")
    time.sleep(3)

    utils.click_by_png(config.EDIT_BACK)
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，仍出现可选项")
    time.sleep(1)
    pyautogui.press("enter")
    if not utils.search_symbol(config.BOARD_AUTO,tolerance=0.75):
        raise Exception("疑似未返回整版界面")
    time.sleep(3)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数未同步修改")
   
    # 封装下其他料号元件未修改
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_14():
    # 1.【设置】-【硬件设置】-【UI配置】-【程序设置】-勾选不允许同步相同的封装+勾选默认同步封装
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(True,True)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的算法框的大小--返回-选是
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    if utils.search_symbol(config.QUESTION_MARK, 5):
        pyautogui.press("enter")
    time.sleep(7)
    # 修改框大小
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)

    pyautogui.hotkey("ctrl", "tab")
    time.sleep(3)
    utils.expand_choose_box()
    pyautogui.press("escape")
    time.sleep(3)

    utils.click_by_png(config.EDIT_BACK)
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，仍出现可选项")
    time.sleep(1)
    pyautogui.press("enter")
    if not utils.search_symbol(config.BOARD_AUTO,tolerance=0.75):
        raise Exception("疑似未返回整版界面")
    time.sleep(3)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，仍出现可选项")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(5)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数未同步修改")
   
    # 封装下其他料号元件未修改
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_15():
    # 1.【设置】-【硬件设置】-【UI配置】-【程序设置】-勾选不允许同步相同的封装+勾选默认同步封装
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(True,True)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的算法框的大小--切换元件-选是
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    if utils.search_symbol(config.QUESTION_MARK, 5):
        pyautogui.press("enter")
    time.sleep(7)

    # 修改框大小
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)

    pyautogui.hotkey("ctrl", "tab")
    time.sleep(3)
    utils.expand_choose_box()
    pyautogui.press("escape")
    time.sleep(3)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，仍出现可选项")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(5)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数未同步修改")
   
    # 封装下其他料号元件未修改
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_16():
    # 1.【设置】-【硬件设置】-【UI配置】-【程序设置】-勾选不允许同步相同的封装+勾选默认同步封装
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(True,True)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的算法框的大小--切换元件-选是
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    if utils.search_symbol(config.QUESTION_MARK, 5):
        pyautogui.press("enter")
    time.sleep(7)

    # 修改框大小
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)

    pyautogui.hotkey("ctrl", "tab")
    time.sleep(3)
    utils.expand_choose_box()
    pyautogui.press("escape")
    time.sleep(3)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，仍出现可选项")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(5)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数未同步修改")
   
    # 封装下其他料号元件未修改
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_17():
    # 1.【设置】-【硬件设置】-【UI配置】-【程序设置】-勾选不允许同步相同的封装+勾选默认同步封装
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(True,True)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的参数--测试当前分组--切换到同料号下其他元件
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    if utils.search_symbol(config.QUESTION_MARK, 5):
        pyautogui.press("enter")
    time.sleep(7)

    # 修改元件参数
    pyautogui.hotkey("ctrl", "a")
    time.sleep(3)
    pyautogui.press("delete")
    time.sleep(3)
    pyautogui.press("enter")
    time.sleep(3)
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(7)
    pyautogui.press("escape")
    time.sleep(3)

    # 测试当前分组
    utils.is_checked((66,255),(78,267), True)
    utils.click_by_png(config.TEST_GROUP)
    while utils.search_symbol(config.TESTING_COMPONENT):
        time.sleep(3)
    time.sleep(7)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    if utils.search_symbol(config.QUESTION_MARK):
        raise Exception("不应出现弹框")      
    time.sleep(7)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)    
    if utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数未同步修改")
   
    # 封装下其他料号元件未修改
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_18():
    # 1.【设置】-【硬件设置】-【UI配置】-【程序设置】-勾选不允许同步相同的封装+勾选默认同步封装
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(True,True)
    utils.ensure_in_edit_mode()

    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的算法框的大小--测试当前分组--切换到同料号下其他元件
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    if utils.search_symbol(config.QUESTION_MARK, 5):
        pyautogui.press("enter")
    time.sleep(7)

    # 修改框大小
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)

    pyautogui.hotkey("ctrl", "tab")
    time.sleep(3)
    utils.expand_choose_box()
    pyautogui.press("escape")
    time.sleep(3)    

    # 测试当前分组
    utils.is_checked((66,255),(78,267), True)
    utils.click_by_png(config.TEST_GROUP)
    while utils.search_symbol(config.TESTING_COMPONENT):
        time.sleep(3)
    time.sleep(7)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    if utils.search_symbol(config.QUESTION_MARK):
        raise Exception("不应出现弹框")   
    time.sleep(7)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数未同步修改")
   
    # 3.切换到同封装下其他元件
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()


@utils.screenshot_error_to_excel()
def lxbj_021_19():
    # 1.【设置】-【硬件设置】-【UI配置】-【程序设置】-勾选不允许同步相同的封装+勾选默认同步封装
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(True,True)
    utils.ensure_in_edit_mode()

    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的参数--测试当前整板--切换到同料号下其他元件
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    if utils.search_symbol(config.QUESTION_MARK, 5):
        pyautogui.press("enter")
    time.sleep(7)

    # 修改元件参数
    pyautogui.hotkey("ctrl", "a")
    time.sleep(3)
    pyautogui.press("delete")
    time.sleep(3)
    pyautogui.press("enter")
    time.sleep(3)
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(7)
    pyautogui.press("escape")
    time.sleep(3)

    # 测试当前整版
    utils.is_checked((66,255),(78,267), True)
    utils.click_by_png(config.TEST_BOARD)
    while utils.search_symbol(config.TESTING_COMPONENT):
        time.sleep(3)
    time.sleep(7)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    if utils.search_symbol(config.QUESTION_MARK):
        raise Exception("不应出现弹框")    
    time.sleep(7)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)    
    if utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数未同步修改")
   
    # 3.切换到同封装下其他料号元件
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_20():
    # 1.【设置】-【硬件设置】-【UI配置】-【程序设置】-勾选不允许同步相同的封装+勾选默认同步封装
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(True,True)
    utils.ensure_in_edit_mode()

    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的算法框的大小--测试当前整板--切换到同料号下其他元件
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    if utils.search_symbol(config.QUESTION_MARK, 5):
        pyautogui.press("enter")
    time.sleep(7)

    # 修改框大小
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)

    pyautogui.hotkey("ctrl", "tab")
    time.sleep(3)
    utils.expand_choose_box()
    pyautogui.press("escape")
    time.sleep(3)   

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    if utils.search_symbol(config.QUESTION_MARK):
        raise Exception("不应出现弹框") 
    time.sleep(7)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数未同步修改")
   
    # 3.切换到同封装下其他元件
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_21():
    # 1.【设置】-【硬件设置】-【UI配置】-【程序设置】-勾选不允许同步相同的封装+勾选默认同步封装
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(True,True)
    utils.ensure_in_edit_mode()

    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的参数--返回
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    time.sleep(7)

    # 修改元件参数
    pyautogui.hotkey("ctrl", "a")
    time.sleep(3)
    pyautogui.press("delete")
    time.sleep(3)
    pyautogui.press("enter")
    time.sleep(3)
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(7)
    pyautogui.press("escape")
    time.sleep(3)

    utils.click_by_png(config.EDIT_BACK)
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，仍出现可选项")
    # 3.选否
    utils.click_by_png(config.NO)
    if not utils.search_symbol(config.BOARD_AUTO,tolerance=0.75):
        raise Exception("疑似未返回整版界面")
    time.sleep(3)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数被同步修改")
   
    # 4.再次进入元件编辑界面，查看此元件参数
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()
 
@utils.screenshot_error_to_excel()
def lxbj_021_22():
    # 1.【设置】-【硬件设置】-【UI配置】-【程序设置】-勾选不允许同步相同的封装+勾选默认同步封装
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(True,True)
    utils.ensure_in_edit_mode()

    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的算法框的大小--返回
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    time.sleep(7)

    # 修改元件参数
    pyautogui.hotkey("ctrl", "a")
    time.sleep(3)
    pyautogui.press("delete")
    time.sleep(3)
    pyautogui.press("enter")
    time.sleep(3)
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(7)
    pyautogui.press("escape")
    time.sleep(3)

    utils.click_by_png(config.EDIT_BACK)
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，仍出现可选项")
    # 3.选否
    utils.click_by_png(config.NO)
    if not utils.search_symbol(config.BOARD_AUTO,tolerance=0.75):
        raise Exception("疑似未返回整版界面")
    time.sleep(3)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    
    if not utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数被同步修改")
   
    # 4.再次进入元件编辑界面，查看此元件参数
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_23():
    # 1.【设置】-【硬件设置】-【UI配置】-【程序设置】-勾选不允许同步相同的封装+勾选默认同步封装
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(True,True)
    utils.ensure_in_edit_mode()

    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的参数--左侧列表选择某个元件切换
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    time.sleep(7)

    # 修改元件参数
    pyautogui.hotkey("ctrl", "a")
    time.sleep(3)
    pyautogui.press("delete")
    time.sleep(3)
    pyautogui.press("enter")
    time.sleep(3)
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(7)
    pyautogui.press("escape")
    time.sleep(3)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    if not utils.search_symbol(config.QUESTION_MARK):
        raise Exception("出现未知错误，未出现弹框")
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，仍出现可选项")
    # 3.选否
    utils.click_by_png(config.NO)
    time.sleep(5)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数被同步修改")

    # 4.再次回到修改那个元件
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()
    # 3.选否
    utils.select_no()
    # 4.再次回到修改那个元件
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_24():
    # 1.【设置】-【硬件设置】-【UI配置】-【程序设置】-勾选不允许同步相同的封装+勾选默认同步封装
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(True,True)
    utils.ensure_in_edit_mode()

    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的算法框的大小--左侧列表选择某个元件切换
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    if utils.search_symbol(config.QUESTION_MARK, 5):
        pyautogui.press("enter")
    time.sleep(7)

    # 修改框大小
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)

    pyautogui.hotkey("ctrl", "tab")
    time.sleep(3)
    utils.expand_choose_box()
    pyautogui.press("escape")
    time.sleep(3)   

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    if not utils.search_symbol(config.QUESTION_MARK):
        raise Exception("出现未知错误，未出现弹框")
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，仍出现可选项")
    # 3.选否
    utils.click_by_png(config.NO)
    time.sleep(5)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if not utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数被同步修改")
   
    # 4.再次进入修改元件
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_25():
    # 1.【设置】-【硬件设置】-【UI配置】-【程序设置】-不勾不允许同步相同的封装+不勾选默认同步封装
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(False,False)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的参数--返回
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    time.sleep(7)

    # 修改元件参数
    pyautogui.hotkey("ctrl", "a")
    time.sleep(3)
    pyautogui.press("delete")
    time.sleep(3)
    pyautogui.press("enter")
    time.sleep(3)
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(7)
    pyautogui.press("escape")
    time.sleep(3)

    utils.click_by_png(config.EDIT_BACK)
    if not utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，未出现可选项")
    # 3.不勾选可选项，弹框选是
    pyautogui.press("enter")
    if not utils.search_symbol(config.BOARD_AUTO,tolerance=0.75):
        raise Exception("疑似未返回整版界面")
    time.sleep(3)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    
    if utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数未被同步修改")
   
    # 封装下其他料号元件未修改
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()


@utils.screenshot_error_to_excel()
def lxbj_021_26():
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(False,False)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的算法框的大小--返回
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    time.sleep(7)

    # 修改框大小
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)

    pyautogui.hotkey("ctrl", "tab")
    time.sleep(3)
    utils.expand_choose_box()
    pyautogui.press("escape")
    time.sleep(3)   

    utils.click_by_png(config.EDIT_BACK)
    if not utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，未出现可选项")
    # 3.不勾选可选项，弹框选是
    pyautogui.press("enter")
    if not utils.search_symbol(config.BOARD_AUTO,tolerance=0.75):
        raise Exception("疑似未返回整版界面")
    time.sleep(3)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    
    if utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数未被同步修改")
   
    # 封装下其他料号元件未修改
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_27():
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(False,False)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的参数--返回
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    time.sleep(7)

    # 修改元件参数
    pyautogui.hotkey("ctrl", "a")
    time.sleep(3)
    pyautogui.press("delete")
    time.sleep(3)
    pyautogui.press("enter")
    time.sleep(3)
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(7)
    pyautogui.press("escape")
    time.sleep(3)

    utils.click_by_png(config.EDIT_BACK)
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，仍出现可选项")
    # 3.勾选可选项，弹框选是
    utils.click_by_png(config.IF_SYNC_SAME_PACKAGE_NO)
    pyautogui.press("enter")
    if not utils.search_symbol(config.BOARD_AUTO,tolerance=0.75):
        raise Exception("疑似未返回整版界面")
    time.sleep(3)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    
    if utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数未被同步修改")
   
    # 4.再次进入元件编辑界面，查看此元件参数
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件未被同步修改")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_28():
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(False,False)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的算法框的大小--返回
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    time.sleep(7)

    # 修改框大小
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)

    pyautogui.hotkey("ctrl", "tab")
    time.sleep(3)
    utils.expand_choose_box()
    pyautogui.press("escape")
    time.sleep(3)   

    utils.click_by_png(config.EDIT_BACK)
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，仍出现可选项")
    # 3.勾选可选项，弹框选是
    utils.click_by_png(config.IF_SYNC_SAME_PACKAGE_NO)
    pyautogui.press("enter")
    if not utils.search_symbol(config.BOARD_AUTO,tolerance=0.75):
        raise Exception("疑似未返回整版界面")
    time.sleep(3)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    
    if utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数未被同步修改")
   
    # 4.再次进入元件编辑界面，查看此元件参数
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件未被同步修改")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_29():
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(False,False)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的参数--切换元件
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    time.sleep(7)

    # 修改元件参数
    pyautogui.hotkey("ctrl", "a")
    time.sleep(3)
    pyautogui.press("delete")
    time.sleep(3)
    pyautogui.press("enter")
    time.sleep(3)
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(7)
    pyautogui.press("escape")
    time.sleep(3)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    if not utils.search_symbol(config.QUESTION_MARK):
        raise Exception("出现未知错误，未出现弹框")
    if not utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，未出现可选项")
    # 3.不勾选可选项-选是
    pyautogui.press("enter")
    time.sleep(5)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数被同步修改")

    # 4.再次回到修改那个元件
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_30():
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(False,False)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的算法框的大小--切换元件
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    if utils.search_symbol(config.QUESTION_MARK, 5):
        pyautogui.press("enter")
    time.sleep(7)

    # 修改框大小
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)

    pyautogui.hotkey("ctrl", "tab")
    time.sleep(3)
    utils.expand_choose_box()
    pyautogui.press("escape")
    time.sleep(3)   

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    if not utils.search_symbol(config.QUESTION_MARK):
        raise Exception("出现未知错误，未出现弹框")
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，仍出现可选项")
    # 3.不勾选可选项-选是
    pyautogui.press("enter")
    time.sleep(5)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数未被同步修改")

    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件未被同步修改")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_31():
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(False,False)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的参数--切换元件
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    time.sleep(7)

    # 修改元件参数
    pyautogui.hotkey("ctrl", "a")
    time.sleep(3)
    pyautogui.press("delete")
    time.sleep(3)
    pyautogui.press("enter")
    time.sleep(3)
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(7)
    pyautogui.press("escape")
    time.sleep(3)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    if not utils.search_symbol(config.QUESTION_MARK):
        raise Exception("出现未知错误，未出现弹框")
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，仍出现可选项")
    # 3.勾选可选项-选是
    utils.click_by_png(config.IF_SYNC_SAME_PACKAGE_NO)
    pyautogui.press("enter")
    time.sleep(5)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数未被同步修改")

    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件未被同步修改")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_32():
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(False,False)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的算法框的大小--切换元件
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    if utils.search_symbol(config.QUESTION_MARK, 5):
        pyautogui.press("enter")
    time.sleep(7)

    # 修改框大小
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)

    pyautogui.hotkey("ctrl", "tab")
    time.sleep(3)
    utils.expand_choose_box()
    pyautogui.press("escape")
    time.sleep(3)   

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    if not utils.search_symbol(config.QUESTION_MARK):
        raise Exception("出现未知错误，未出现弹框")
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，仍出现可选项")

    # 3.勾选可选项-选是
    utils.click_by_png(config.IF_SYNC_SAME_PACKAGE_NO)
    pyautogui.press("enter")
    time.sleep(5)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数未被同步修改")

    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件未被同步修改")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_33():
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(False,False)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的参数--测试当前分组--切换到同料号下其他元件
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    if utils.search_symbol(config.QUESTION_MARK, 5):
        pyautogui.press("enter")
    time.sleep(7)

    # 修改元件参数
    pyautogui.hotkey("ctrl", "a")
    time.sleep(3)
    pyautogui.press("delete")
    time.sleep(3)
    pyautogui.press("enter")
    time.sleep(3)
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(7)
    pyautogui.press("escape")
    time.sleep(3)

    # 测试当前分组
    utils.is_checked((66,255),(78,267), True)
    utils.click_by_png(config.TEST_GROUP)
    while utils.search_symbol(config.TESTING_COMPONENT):
        time.sleep(3)
    time.sleep(7)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    if utils.search_symbol(config.QUESTION_MARK):
        raise Exception("不应出现弹框")    
    time.sleep(7)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)    
    if utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数未同步修改")
   
    # 封装下其他料号元件未修改
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_34():
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(False,False)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的算法框的大小--测试当前分组--切换到同料号下其他元件
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    if utils.search_symbol(config.QUESTION_MARK, 5):
        pyautogui.press("enter")
    time.sleep(7)

    # 修改框大小
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)

    pyautogui.hotkey("ctrl", "tab")
    time.sleep(3)
    utils.expand_choose_box()
    pyautogui.press("escape")
    time.sleep(3)    

    # 测试当前分组
    utils.is_checked((66,255),(78,267), True)
    utils.click_by_png(config.TEST_GROUP)
    while utils.search_symbol(config.TESTING_COMPONENT):
        time.sleep(3)
    time.sleep(7)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    if utils.search_symbol(config.QUESTION_MARK):
        raise Exception("不应出现弹框")
    time.sleep(5)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数未同步修改")
   
    # 3.切换到同封装下其他元件
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_35():
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(False,False)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的参数--测试当前整板--切换到同料号下其他元件
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    if utils.search_symbol(config.QUESTION_MARK, 5):
        pyautogui.press("enter")
    time.sleep(7)

    # 修改元件参数
    pyautogui.hotkey("ctrl", "a")
    time.sleep(3)
    pyautogui.press("delete")
    time.sleep(3)
    pyautogui.press("enter")
    time.sleep(3)
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(7)
    pyautogui.press("escape")
    time.sleep(3)

    # 测试当前整版
    utils.is_checked((66,255),(78,267), True)
    utils.click_by_png(config.TEST_BOARD)
    while utils.search_symbol(config.TESTING_COMPONENT):
        time.sleep(3)
    time.sleep(7)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    if utils.search_symbol(config.QUESTION_MARK):
        raise Exception("不应出现弹框")    
    time.sleep(7)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)    
    if utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数未同步修改")
   
    # 3.切换到同封装下其他料号元件
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()
   

@utils.screenshot_error_to_excel()
def lxbj_021_36():
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(False,False)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的算法框的大小--测试当前整板--切换到同料号下其他元件
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    if utils.search_symbol(config.QUESTION_MARK, 5):
        pyautogui.press("enter")
    time.sleep(7)

    # 修改框大小
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)

    pyautogui.hotkey("ctrl", "tab")
    time.sleep(3)
    utils.expand_choose_box()
    pyautogui.press("escape")
    time.sleep(3)   

    # 测试当前整版
    utils.is_checked((66,255),(78,267), True)
    utils.click_by_png(config.TEST_BOARD)
    while utils.search_symbol(config.TESTING_COMPONENT):
        time.sleep(3)
    time.sleep(7)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    if utils.search_symbol(config.QUESTION_MARK):
        raise Exception("不应出现弹框")
    time.sleep(7)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数未同步修改")
   
    # 3.切换到同封装下其他元件
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_37():
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(False,False)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的参数--返回
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    time.sleep(7)

    # 修改元件参数
    pyautogui.hotkey("ctrl", "a")
    time.sleep(3)
    pyautogui.press("delete")
    time.sleep(3)
    pyautogui.press("enter")
    time.sleep(3)
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(7)
    pyautogui.press("escape")
    time.sleep(3)

    utils.click_by_png(config.EDIT_BACK)
    if not utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，未出现可选项")
    # 3.不勾选可选项-选否
    utils.click_by_png(config.NO)
    if not utils.search_symbol(config.BOARD_AUTO,tolerance=0.75):
        raise Exception("疑似未返回整版界面")
    time.sleep(3)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数被同步修改")
   
    # 4.再次进入元件编辑界面，查看此元件参数
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_38():
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(False,False)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的算法框的大小--返回
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    time.sleep(7)

    # 修改框大小
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)

    pyautogui.hotkey("ctrl", "tab")
    time.sleep(3)
    utils.expand_choose_box()
    pyautogui.press("escape")
    time.sleep(3)   

    utils.click_by_png(config.EDIT_BACK)
    if not utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，未出现可选项")
    # 3.不勾选可选项-选否
    utils.click_by_png(config.NO)
    if not utils.search_symbol(config.BOARD_AUTO,tolerance=0.75):
        raise Exception("疑似未返回整版界面")
    time.sleep(3)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if not utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数被同步修改")
    # 4.再次进入元件编辑界面，查看此元件算法框
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_39():
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(False,False)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的参数--返回
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    time.sleep(7)

    # 修改元件参数
    pyautogui.hotkey("ctrl", "a")
    time.sleep(3)
    pyautogui.press("delete")
    time.sleep(3)
    pyautogui.press("enter")
    time.sleep(3)
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(7)
    pyautogui.press("escape")
    time.sleep(3)

    utils.click_by_png(config.EDIT_BACK)
    if not utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，未出现可选项")
    # 3.勾选可选项-选否
    utils.click_by_png(config.IF_SYNC_SAME_PACKAGE_NO)
    utils.click_by_png(config.NO)
    if not utils.search_symbol(config.BOARD_AUTO,tolerance=0.75):
        raise Exception("疑似未返回整版界面")
    time.sleep(3)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数被同步修改")
   
    # 4.再次进入元件编辑界面，查看此元件参数
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_40():
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(False,False)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的算法框的大小--返回
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    time.sleep(7)

    # 修改框大小
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)

    pyautogui.hotkey("ctrl", "tab")
    time.sleep(3)
    utils.expand_choose_box()
    pyautogui.press("escape")
    time.sleep(3)   

    utils.click_by_png(config.EDIT_BACK)
    if not utils.search_symbol(config.QUESTION_MARK):
        raise Exception("出现未知错误，未出现弹框")
    if not utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，未出现可选项")
    # 3.勾选可选项--选否
    utils.click_by_png(config.IF_SYNC_SAME_PACKAGE_NO)
    utils.click_by_png(config.NO)
    if not utils.search_symbol(config.BOARD_AUTO,tolerance=0.75):
        raise Exception("疑似未返回整版界面")
    time.sleep(3)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if not utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数被同步修改")
    
    # 4.再次进入元件编辑界面，查看此元件算法框
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_41():
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(False,False)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的参数--左侧列表选择某个元件切换
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    time.sleep(7)

    # 修改元件参数
    pyautogui.hotkey("ctrl", "a")
    time.sleep(3)
    pyautogui.press("delete")
    time.sleep(3)
    pyautogui.press("enter")
    time.sleep(3)
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(7)
    pyautogui.press("escape")
    time.sleep(3)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    if not utils.search_symbol(config.QUESTION_MARK):
        raise Exception("出现未知错误，未出现弹框")
    if not utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，未出现可选项")
    # 3.不勾选可选项-选否
    utils.click_by_png(config.NO)
    time.sleep(7)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数被同步修改")

    # 4.再次回到修改那个元件
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_42():
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(False,False)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的算法框的大小--左侧列表选择某个元件切换
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    if utils.search_symbol(config.QUESTION_MARK, 5):
        pyautogui.press("enter")
    time.sleep(7)

    # 修改框大小
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)

    pyautogui.hotkey("ctrl", "tab")
    time.sleep(3)
    utils.expand_choose_box()
    pyautogui.press("escape")
    time.sleep(3)   

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    if not utils.search_symbol(config.QUESTION_MARK):
        raise Exception("出现未知错误，未出现弹框")
    if not utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，未出现可选项")
    # 3.不勾选可选项-选否
    utils.click_by_png(config.NO)
    time.sleep(7)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if not utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数被同步修改")
   
    # 封装下其他料号元件未修改
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()


@utils.screenshot_error_to_excel()
def lxbj_021_43():
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(False,False)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的参数--左侧列表选择某个元件切换
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    time.sleep(7)

    # 修改元件参数
    pyautogui.hotkey("ctrl", "a")
    time.sleep(3)
    pyautogui.press("delete")
    time.sleep(3)
    pyautogui.press("enter")
    time.sleep(3)
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(7)
    pyautogui.press("escape")
    time.sleep(3)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    if not utils.search_symbol(config.QUESTION_MARK):
        raise Exception("出现未知错误，未出现弹框")
    if not utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，未出现可选项")

    # 3.勾选可选项--选否
    utils.click_by_png(config.IF_SYNC_SAME_PACKAGE_NO)
    utils.click_by_png(config.NO)
    time.sleep(7)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数被同步修改")
    # 4.再次回到修改元件
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_44():
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(False,False)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的算法框的大小--左侧列表选择某个元件切换
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    if utils.search_symbol(config.QUESTION_MARK, 5):
        pyautogui.press("enter")
    time.sleep(7)
    # 修改框大小
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)

    pyautogui.hotkey("ctrl", "tab")
    time.sleep(3)
    utils.expand_choose_box()
    pyautogui.press("escape")
    time.sleep(3)   

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    if not utils.search_symbol(config.QUESTION_MARK):
        raise Exception("出现未知错误，未出现弹框")
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，仍出现可选项")
    # 3.勾选可选项--选否
    utils.click_by_png(config.IF_SYNC_SAME_PACKAGE_NO)
    utils.click_by_png(config.NO)
    time.sleep(5)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if not utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数被同步修改")
   
    # 封装下其他料号元件未修改
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_45():
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(False,False)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的参数--返回
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    time.sleep(7)

    # 修改元件参数
    pyautogui.hotkey("ctrl", "a")
    time.sleep(3)
    pyautogui.press("delete")
    time.sleep(3)
    pyautogui.press("enter")
    time.sleep(3)
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(7)
    pyautogui.press("escape")
    time.sleep(3)

    utils.click_by_png(config.EDIT_BACK)
    if not utils.search_symbol(config.QUESTION_MARK):
        raise Exception("出现未知错误，未出现弹框")
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，仍出现可选项")
    # 3.取消勾选可选项，弹框选是
    pyautogui.press("enter")
    if not utils.search_symbol(config.BOARD_AUTO,tolerance=0.75):
        raise Exception("疑似未返回整版界面")
    time.sleep(3)
    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数未被同步修改")
   
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_46():
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(False,False)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的算法框的大小--返回
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    time.sleep(7)

    # 修改框大小
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)

    pyautogui.hotkey("ctrl", "tab")
    time.sleep(3)
    utils.expand_choose_box()
    pyautogui.press("escape")
    time.sleep(3)   

    utils.click_by_png(config.EDIT_BACK)
    if not utils.search_symbol(config.QUESTION_MARK):
        raise Exception("出现未知错误，未出现弹框")
    if not utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，未出现可选项")
    # 3.取消勾选可选项，弹框选是
    pyautogui.press("enter")
    if not utils.search_symbol(config.BOARD_AUTO,tolerance=0.75):
        raise Exception("疑似未返回整版界面")
    time.sleep(3)
    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数未被同步修改")
   
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_47():
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(False,False)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的参数--返回
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    time.sleep(7)

    # 修改元件参数
    pyautogui.hotkey("ctrl", "a")
    time.sleep(3)
    pyautogui.press("delete")
    time.sleep(3)
    pyautogui.press("enter")
    time.sleep(3)
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(7)
    pyautogui.press("escape")
    time.sleep(3)

    utils.click_by_png(config.EDIT_BACK)
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，仍出现可选项")
    # 3.选否
    utils.click_by_png(config.NO)
    if not utils.search_symbol(config.BOARD_AUTO,tolerance=0.75):
        raise Exception("疑似未返回整版界面")
    time.sleep(3)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    
    if not utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数被同步修改")
   
    # 4.再次进入元件编辑界面，查看此元件参数
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()
    # 3.可选项勾选状态，弹框选是
    utils.click_by_png(config.IF_SYNC_SAME_PACKAGE_NO)
    pyautogui.press("enter")
    time.sleep(5)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数未被同步修改")

    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件未被同步修改")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_48():
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(False,False)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的算法框的大小--返回
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    time.sleep(7)

    # 修改框大小
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)

    pyautogui.hotkey("ctrl", "tab")
    time.sleep(3)
    utils.expand_choose_box()
    pyautogui.press("escape")
    time.sleep(3)   

    utils.click_by_png(config.EDIT_BACK)
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，仍出现可选项")
    # 3.可选项勾选状态，弹框选是
    utils.click_by_png(config.IF_SYNC_SAME_PACKAGE_NO)
    pyautogui.press("enter")
    time.sleep(5)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数未被同步修改")

    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件未被同步修改")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_49():
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(False,False)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的参数--切换元件
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    time.sleep(7)

    # 修改元件参数
    pyautogui.hotkey("ctrl", "a")
    time.sleep(3)
    pyautogui.press("delete")
    time.sleep(3)
    pyautogui.press("enter")
    time.sleep(3)
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(7)
    pyautogui.press("escape")
    time.sleep(3)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    if not utils.search_symbol(config.QUESTION_MARK):
        raise Exception("出现未知错误，未出现弹框")
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，仍出现可选项")
    # 3.选否
    utils.click_by_png(config.NO)
    time.sleep(5)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数被同步修改")

    # 4.再次回到修改那个元件
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()
    # 3.取消勾选可选项-选是
    utils.uncheck_optional_item()
    utils.confirm_popup("是")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_50():
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(False,False)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的算法框的大小--切换元件
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    if utils.search_symbol(config.QUESTION_MARK, 5):
        pyautogui.press("enter")
    time.sleep(7)

    # 修改框大小
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)

    pyautogui.hotkey("ctrl", "tab")
    time.sleep(3)
    utils.expand_choose_box()
    pyautogui.press("escape")
    time.sleep(3)   

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    if not utils.search_symbol(config.QUESTION_MARK):
        raise Exception("出现未知错误，未出现弹框")
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，仍出现可选项")
    # 3.选否
    utils.click_by_png(config.NO)
    time.sleep(5)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数被同步修改")
   
    # 封装下其他料号元件未修改
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()
    # 3.取消勾选可选项-选是
    utils.uncheck_optional_item()
    utils.confirm_popup("是")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_51():
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(False,False)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的参数--切换元件
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    time.sleep(7)

    # 修改元件参数
    pyautogui.hotkey("ctrl", "a")
    time.sleep(3)
    pyautogui.press("delete")
    time.sleep(3)
    pyautogui.press("enter")
    time.sleep(3)
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(7)
    pyautogui.press("escape")
    time.sleep(3)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    if not utils.search_symbol(config.QUESTION_MARK):
        raise Exception("出现未知错误，未出现弹框")
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，仍出现可选项")
    # 3.选否
    utils.click_by_png(config.NO)
    time.sleep(5)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数被同步修改")

    # 4.再次回到修改那个元件
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()
    # 3.选是
    utils.confirm_popup("是")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_52():
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(False,False)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的算法框的大小--切换元件
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    if utils.search_symbol(config.QUESTION_MARK, 5):
        pyautogui.press("enter")
    time.sleep(7)

    # 修改框大小
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)

    pyautogui.hotkey("ctrl", "tab")
    time.sleep(3)
    utils.expand_choose_box()
    pyautogui.press("escape")
    time.sleep(3)   

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    if not utils.search_symbol(config.QUESTION_MARK):
        raise Exception("出现未知错误，未出现弹框")
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，仍出现可选项")
    # 3.选否
    utils.click_by_png(config.NO)
    time.sleep(5)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数被同步修改")
   
    # 封装下其他料号元件未修改
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()
    # 3.选是
    utils.confirm_popup("是")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_53():
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(False,False)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的参数--测试当前分组--切换到同料号下其他元件
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    if utils.search_symbol(config.QUESTION_MARK, 5):
        pyautogui.press("enter")
    time.sleep(7)

    # 修改元件参数
    pyautogui.hotkey("ctrl", "a")
    time.sleep(3)
    pyautogui.press("delete")
    time.sleep(3)
    pyautogui.press("enter")
    time.sleep(3)
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(7)
    pyautogui.press("escape")
    time.sleep(3)

    # 测试当前分组
    utils.is_checked((66,255),(78,267), True)
    utils.click_by_png(config.TEST_GROUP)
    while utils.search_symbol(config.TESTING_COMPONENT):
        time.sleep(3)
    time.sleep(7)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    if utils.search_symbol(config.QUESTION_MARK):
        raise Exception("不应出现弹框")    
    time.sleep(7)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)    
    if utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数未同步修改")
   
    # 封装下其他料号元件未修改
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()
    # 3.切换到同封装下其他料号元件
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_54():
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(False,False)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的算法框的大小--测试当前分组--切换到同料号下其他元件
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    if utils.search_symbol(config.QUESTION_MARK, 5):
        pyautogui.press("enter")
    time.sleep(7)

    # 修改框大小
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)

    pyautogui.hotkey("ctrl", "tab")
    time.sleep(3)
    utils.expand_choose_box()
    pyautogui.press("escape")
    time.sleep(3)    

    # 测试当前分组
    utils.is_checked((66,255),(78,267), True)
    utils.click_by_png(config.TEST_GROUP)
    while utils.search_symbol(config.TESTING_COMPONENT):
        time.sleep(3)
    time.sleep(7)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        time.sleep(1)
        pyautogui.press("enter")
    time.sleep(5)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数未同步修改")
   
    # 封装下其他料号元件未修改
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()
    utils.open_job_with_multiple_parts()
    utils.modify_algorithm_box_size()
    utils.test_current_group()
    utils.switch_to_other_component_in_same_part()
    # 3.切换到同封装下其他元件
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_55():
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(False,False)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的参数--测试当前整板--切换到同料号下其他元件
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    if utils.search_symbol(config.QUESTION_MARK, 5):
        pyautogui.press("enter")
    time.sleep(7)

    # 修改元件参数
    pyautogui.hotkey("ctrl", "a")
    time.sleep(3)
    pyautogui.press("delete")
    time.sleep(3)
    pyautogui.press("enter")
    time.sleep(3)
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(7)
    pyautogui.press("escape")
    time.sleep(3)

    # 测试当前分组
    utils.is_checked((66,255),(78,267), True)
    utils.click_by_png(config.TEST_GROUP)
    while utils.search_symbol(config.TESTING_COMPONENT):
        time.sleep(3)
    time.sleep(7)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    if utils.search_symbol(config.QUESTION_MARK):
        raise Exception("不应出现弹框")    
    time.sleep(7)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)    
    if utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数未同步修改")
   
    # 封装下其他料号元件未修改
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()
    # 3.切换到同封装下其他料号元件
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_56():
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(False,False)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的算法框的大小--测试当前整板--切换到同料号下其他元件
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    if utils.search_symbol(config.QUESTION_MARK, 5):
        pyautogui.press("enter")
    time.sleep(7)

    # 修改框大小
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)

    pyautogui.hotkey("ctrl", "tab")
    time.sleep(3)
    utils.expand_choose_box()
    pyautogui.press("escape")
    time.sleep(3)   


    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    if utils.search_symbol(config.QUESTION_MARK):
        pyautogui.press("enter")
        time.sleep(7)    
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数未同步修改")
   
    # 封装下其他料号元件未修改
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()
    # 3.切换到同封装下其他元件
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_57():
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(False,False)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的参数--返回
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    time.sleep(7)

    # 修改元件参数
    pyautogui.hotkey("ctrl", "a")
    time.sleep(3)
    pyautogui.press("delete")
    time.sleep(3)
    pyautogui.press("enter")
    time.sleep(3)
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(7)
    pyautogui.press("escape")
    time.sleep(3)

    utils.click_by_png(config.EDIT_BACK)
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，仍出现可选项")
    # 3.选否
    utils.click_by_png(config.NO)
    if not utils.search_symbol(config.BOARD_AUTO,tolerance=0.75):
        raise Exception("疑似未返回整版界面")
    time.sleep(3)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    
    if not utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数被同步修改")
   
    # 4.再次进入元件编辑界面，查看此元件参数
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()
    utils.click_by_png(config.NO)
    if not utils.search_symbol(config.BOARD_AUTO,tolerance=0.75):
        raise Exception("疑似未返回整版界面")
    time.sleep(3)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数被同步修改")
    # 4.再次进入元件编辑界面，查看此元件参数
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_58():
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(False,False)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的算法框的大小--返回
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    time.sleep(7)

    # 修改框大小
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)

    pyautogui.hotkey("ctrl", "tab")
    time.sleep(3)
    utils.expand_choose_box()
    pyautogui.press("escape")
    time.sleep(3)   

    utils.click_by_png(config.EDIT_BACK)
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，仍出现可选项")
    # 3.取消勾选可选项--选否
    utils.uncheck_optional_item()
    utils.confirm_popup("否")
    # 4.再次进入元件编辑界面，查看此元件算法框
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_59():
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(False,False)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的参数--返回
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    time.sleep(7)

    # 修改元件参数
    pyautogui.hotkey("ctrl", "a")
    time.sleep(3)
    pyautogui.press("delete")
    time.sleep(3)
    pyautogui.press("enter")
    time.sleep(3)
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(7)
    pyautogui.press("escape")
    time.sleep(3)

    utils.click_by_png(config.EDIT_BACK)
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，仍出现可选项")
    # 3.选否
    utils.click_by_png(config.NO)
    if not utils.search_symbol(config.BOARD_AUTO,tolerance=0.75):
        raise Exception("疑似未返回整版界面")
    time.sleep(3)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    
    if not utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数被同步修改")
   
    # 4.再次进入元件编辑界面，查看此元件参数
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()
    # 3.可选项勾选状态-选否
    utils.check_optional_item()
    utils.confirm_popup("否")
    # 4.再次进入元件编辑界面，查看此元件参数
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_60():
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(False,False)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的算法框的大小--返回
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    time.sleep(7)

    # 修改框大小
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)

    pyautogui.hotkey("ctrl", "tab")
    time.sleep(3)
    utils.expand_choose_box()
    pyautogui.press("escape")
    time.sleep(3)   

    utils.click_by_png(config.EDIT_BACK)
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，仍出现可选项")
    # 3.可选项勾选状态--选否
    utils.check_optional_item()
    utils.confirm_popup("否")
    # 4.再次进入元件编辑界面，查看此元件算法框
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_61():
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(False,False)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的参数--左侧列表选择某个元件切换
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    time.sleep(7)

    # 修改元件参数
    pyautogui.hotkey("ctrl", "a")
    time.sleep(3)
    pyautogui.press("delete")
    time.sleep(3)
    pyautogui.press("enter")
    time.sleep(3)
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(7)
    pyautogui.press("escape")
    time.sleep(3)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    if not utils.search_symbol(config.QUESTION_MARK):
        raise Exception("出现未知错误，未出现弹框")
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，仍出现可选项")
    # 3.选否
    utils.click_by_png(config.NO)
    time.sleep(5)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数被同步修改")

    # 4.再次回到修改那个元件
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()
    # 3.取消勾选可选项--选否
    utils.uncheck_optional_item()
    utils.confirm_popup("否")
    # 4.再次回到修改那个元件
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_62():
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(False,False)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的算法框的大小--左侧列表选择某个元件切换
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    if utils.search_symbol(config.QUESTION_MARK, 5):
        pyautogui.press("enter")
    time.sleep(7)

    # 修改框大小
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)

    pyautogui.hotkey("ctrl", "tab")
    time.sleep(3)
    utils.expand_choose_box()
    pyautogui.press("escape")
    time.sleep(3)   

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    if not utils.search_symbol(config.QUESTION_MARK):
        raise Exception("出现未知错误，未出现弹框")
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，仍出现可选项")
    # 3.选否
    utils.click_by_png(config.NO)
    time.sleep(5)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数被同步修改")
   
    # 封装下其他料号元件未修改
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()
    # 3.取消勾选可选项--选否
    utils.uncheck_optional_item()
    utils.confirm_popup("否")
    # 4.再次进入修改元件
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_63():
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(False,False)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的参数--左侧列表选择某个元件切换
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    time.sleep(7)

    # 修改元件参数
    pyautogui.hotkey("ctrl", "a")
    time.sleep(3)
    pyautogui.press("delete")
    time.sleep(3)
    pyautogui.press("enter")
    time.sleep(3)
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(7)
    pyautogui.press("escape")
    time.sleep(3)

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    if not utils.search_symbol(config.QUESTION_MARK):
        raise Exception("出现未知错误，未出现弹框")
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，仍出现可选项")
    # 3.选否
    utils.click_by_png(config.NO)
    time.sleep(5)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数被同步修改")

    # 4.再次回到修改那个元件
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()
    # 3.可选项勾选状态--选否
    utils.check_optional_item()
    utils.confirm_popup("否")
    # 4.再次回到修改那个元件
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def lxbj_021_64():
    utils.check_and_launch_aoi()
    utils.check_not_sync_same_and_default_package(False,False)
    utils.ensure_in_edit_mode()
    # 2.打开一个job(一个封装下有多料号的)--修改其中一个料号的元件的算法框的大小--左侧列表选择某个元件切换
    # 自己制造封装
    package_a,package_b = utils.make_package()
    logger.info(f"封装a: {package_a}, 封装b: {package_b}")
    if utils.search_symbol(config.BOARD_EYE, 2, region=config.BOARD_INFORMATION_REGION):
        utils.click_by_png(config.BOARD_EYE, region=config.BOARD_INFORMATION_REGION)
    # 操作封装a 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_a)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的首个料号 截取原图 用于确保封装下其他料号修改情况
    utils.write_text((135,210),package_b)
    utils.click_component(click_index=1)
    time.sleep(7)
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)
    package_b1_before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    # 操作封装b的第二个料号 用于确保同料号下其他元件修改情况
    utils.click_component(click_index=2)
    if utils.search_symbol(config.QUESTION_MARK, 5):
        pyautogui.press("enter")
    time.sleep(7)

    # 修改框大小
    if not utils.search_symbol(config.ALG_W_0, 5, region=config.COMPONENT_WINDOW_REGION):
        utils.add_window()
        utils.click_by_png(config.COLOR_AREA)
        utils.click_by_png(config.YES)
        time.sleep(7)
        pyautogui.press("escape")
        time.sleep(3)

    pyautogui.hotkey("ctrl", "tab")
    time.sleep(3)
    utils.expand_choose_box()
    pyautogui.press("escape")
    time.sleep(3)   

    # 回到封装b的第一个料号
    utils.click_component(click_index=1)
    if not utils.search_symbol(config.QUESTION_MARK):
        raise Exception("出现未知错误，未出现弹框")
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO):
        raise Exception("设置疑似失效，仍出现可选项")
    # 3.选否
    utils.click_by_png(config.NO)
    time.sleep(5)
    package_b1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_b1_after_screenshot, package_b1_before_screenshot):
        raise Exception("同料号下其他元件参数被同步修改")
   
    # 封装下其他料号元件未修改
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()
    # 3.可选项勾选状态--选否
    utils.check_optional_item()
    utils.confirm_popup("否")
    # 4.再次进入修改元件
    utils.write_text((135,210),package_a)
    utils.scroll_down((200,380),config.BOARD_COMPONENTS_REGION, 800)
    utils.click_component(click_index=1)
    time.sleep(7)
    package_a1_after_screenshot = pyautogui.screenshot(region=config.COMPONENT_WINDOW_REGION)
    if not utils.compare_images(package_a1_after_screenshot, package_a1_before_screenshot):
        raise Exception("封装下其他料号元件也被同步修改了")
    utils.close_aoi()
