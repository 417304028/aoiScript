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
    utils.click_by_png(config.YES)
    utils.click_by_png(config.IMAGE_CLOSE)
    # 添加标准影像
    # 加五种随机不同光源的待料 需确认添加成功
    for _ in range(5):
        utils.click_by_png(config.ADD_STANDARD_IMAGE)
        utils.random_choose_light()
        utils.click_by_png(config.YES)
        utils.click_by_png(config.IMAGE_CLOSE)
    utils.random_change_image_param()
    utils.click_by_png(config.TEST_WINDOW)
    time.sleep(3)
    # TODO 要加个超时时间
    utils.click_by_png(config.TEST_COMPONENT)
    while utils.search_symbol(config.TESTING_COMPONENT):
        time.sleep(1)
    time.sleep(1)
    utils.click_by_png(config.TEST_GROUP)
    while utils.search_symbol(config.TESTING_COMPONENT):
        time.sleep(1)
    time.sleep(1)
    utils.click_by_png(config.TEST_BOARD)
    while utils.search_symbol(config.TESTING_COMPONENT):
        time.sleep(1)
    time.sleep(1)
    utils.caton_or_flashback()

# TODO 可以识别出提示，但是没办法跟缺陷名对应
# 不良窗口/元件
@utils.screenshot_error_to_excel()
def lxbj_003_01():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    time.sleep(2)
    pyautogui.press('b')
    # 不良窗口，红字提示：检测窗口 缺陷名称（左侧窗口的缺陷名，如果左侧窗口的缺陷名是默认，取算法参数界面首个不良结果对应的缺陷名）
    utils.click_by_png(config.TEST_WINDOW)
    time.sleep(3)
    # 不良元件，红字提示：元件 首个不良窗口的缺陷名称（左侧窗口的缺陷名，如果左侧窗口的缺陷名是默认，取算法参数界面首个不良结果对应的缺陷名）
    utils.click_by_png(config.TEST_COMPONENT)
    time.sleep(3)

# 返回不修改
@utils.screenshot_error_to_excel()
def lxbj_004_01():
    utils.check_and_launch_aoi()
    utils.check_sync_package(False, False)
    utils.ensure_in_edit_mode()
    utils.add_window()
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    time.sleep(3)
    utils.random_change_param()
    utils.click_by_png(config.EDIT_BACK)
    time.sleep(2)
    # 在提示框，不选【同步到相同的封装类型】，点击【否】
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO, 1):
        pyautogui.press('right')
        pyautogui.press('enter')
    else:
        if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_YES, 1):
            utils.click_by_png(config.IF_SYNC_SAME_PACKAGE_YES)
            pyautogui.press('right')
            pyautogui.press('enter')
        else:
            raise Exception
    utils.search_symbol_erroring(config.BOARD_AUTO, 10)


# 不同步封装
@utils.screenshot_error_to_excel()
def lxbj_004_02():
    utils.check_and_launch_aoi()
    utils.check_sync_package(False, False)
    utils.ensure_in_edit_mode()
    utils.add_window()
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    time.sleep(3)
    utils.random_change_param()
    utils.click_by_png(config.EDIT_BACK)
    # 在提示框，不选【同步到相同的封装类型】，点击【是】
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO, 1):
        pyautogui.press('enter')
    else:
        if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_YES, 1):
            utils.click_by_png(config.IF_SYNC_SAME_PACKAGE_YES)
            pyautogui.press('enter')
        else:
            raise Exception
    # 相同封装的其他料号的元件窗口参数都相同
    utils.check_package_same_param(True)


# 同步封装
@utils.screenshot_error_to_excel()
def lxbj_004_03():
    utils.check_and_launch_aoi()
    utils.check_sync_package(False, False)
    utils.ensure_in_edit_mode()
    utils.add_window()
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    time.sleep(3)
    utils.random_change_param()
    utils.click_by_png(config.EDIT_BACK)
    # 在提示框，选择【同步到相同的封装类型】，点击【是】
    if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_YES, 1):
        pyautogui.press('enter')
    else:
        if utils.search_symbol(config.IF_SYNC_SAME_PACKAGE_NO, 1):
            utils.click_by_png(config.IF_SYNC_SAME_PACKAGE_NO)
            pyautogui.press('enter')
        else:
            raise Exception
    utils.check_package_same_param(False)


# 不同步封装 
@utils.screenshot_error_to_excel()
def lxbj_004_04():
    utils.check_and_launch_aoi()
    utils.check_sync_package(True, False)
    utils.ensure_in_edit_mode()
    utils.add_window()
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    time.sleep(3)
    utils.random_change_param()
    utils.click_by_png(config.EDIT_BACK)
    # 在提示框，点击【是】
    pyautogui.press('enter')
    utils.check_package_same_param(False)


# 不同步封装
@utils.screenshot_error_to_excel()
def lxbj_004_05():
    utils.check_and_launch_aoi()
    utils.check_sync_package(True, True)
    utils.ensure_in_edit_mode()
    utils.add_window()
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    time.sleep(3)
    utils.random_change_param()
    utils.click_by_png(config.EDIT_BACK)
    # 在提示框，点击【是】
    pyautogui.press('enter')
    utils.check_package_same_param(False)


# 同步封装
@utils.screenshot_error_to_excel()
def lxbj_004_06():
    utils.check_and_launch_aoi()
    utils.check_sync_package(False, True)
    utils.ensure_in_edit_mode()
    utils.add_window()
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    time.sleep(3)
    utils.random_change_param()
    utils.click_by_png(config.EDIT_BACK)
    # 在提示框，点击【是】
    # 弹框提示不勾默认选择【同步到相同的封装类型】
    utils.search_symbol_erroring(config.IF_SYNC_SAME_PACKAGE_YES, 5)
    pyautogui.press('enter')
    utils.check_package_same_param(False)
    # TODO 要确定相同封装其他料号的元件窗口算法参数未更新


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
    shutil.rmtree(f"D:\\EYAOI\\JOB\\{program_name}\\{program_name}.oki", ignore_errors=True)
    # 删除目录F:\DataExport\Job名\OKImage
    shutil.rmtree(f"F:\\DataExport\\{program_name}\\OKImage", ignore_errors=True)
    # 在某一元件【元器件编辑】界面，右击--【导出元件OK图】
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.EXPORT_COMPONENT_OK)
    # 在提示框，点击【确定】
    utils.click_by_png(config.EXPORT_COMPONENT_SUCCESS, timeout=20)
    # 弹框提示：生成ok图完成，并可以在F:\DataExport\Job名\OKImage下发现
    ok_image_path = f"F:\\DataExport\\{program_name}\\OKImage"
    recent_files = [f for f in os.listdir(ok_image_path) if
                    os.path.getctime(os.path.join(ok_image_path, f)) > time.time() - 10]
    if not recent_files:
        raise Exception("在指定目录下未找到最近10秒内生成的OK图数据")


@utils.screenshot_error_to_excel()
def lxbj_005_02():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 1、UI：参数配置--UI配置-程序设置：不选【导出元件OK图】、选择【导出所有元件OK图】
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
    utils.click_by_png(config.EXPORT_COMPONENT_OK)
    # 在提示框，点击【确定】
    utils.click_by_png(config.EXPORT_COMPONENT_SUCCESS, timeout=5)
    # 弹框提示：生成ok图完成，并可以在F:\DataExport\Job名\OKImage下发现
    ok_image_path = f"F:\\DataExport\\{program_name}\\OKImage"
    recent_files = [f for f in os.listdir(ok_image_path) if
                    os.path.getctime(os.path.join(ok_image_path, f)) > time.time() - 10]
    if not recent_files:
        raise Exception("在指定目录下未找到最近10秒内生成的OK图数据")


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
    if not utils.search_symbol_erroring(config.IF_EXPORT_PART_OK, 5):
        raise Exception("未发现提示框")
    else:
        pyautogui.press('enter')
        utils.search_symbol_erroring(config.EXPORTING_OK, 5)
        utils.search_symbol_erroring(config.OK_COLLECTION, 5)
        pyautogui.press('enter')
    # 弹框提示：生成ok图完成，并可以在F:\DataExport\Job名\OKImage下发现
    ok_image_path = f"F:\\DataExport\\{program_name}\\OKImage"
    recent_files = [f for f in os.listdir(ok_image_path) if
                    os.path.getctime(os.path.join(ok_image_path, f)) > time.time() - 10]
    if not recent_files:
        raise Exception("在指定目录下未找到最近10秒内生成的OK图数据")


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
    if not utils.search_symbol_erroring(config.IF_EXPORT_PART_OK, 5):
        raise Exception("未发现提示框")
    else:
        pyautogui.press('enter')
        utils.search_symbol_erroring(config.EXPORTING_OK, 5)
        utils.search_symbol_erroring(config.OK_COLLECTION, 5)
        pyautogui.press('enter')
    # 弹框提示：生成ok图完成，并可以在F:\DataExport\Job名\OKImage下发现
    ok_image_path = f"F:\\DataExport\\{program_name}\\OKImage"
    recent_files = [f for f in os.listdir(ok_image_path) if
                    os.path.getctime(os.path.join(ok_image_path, f)) > time.time() - 10]
    if not recent_files:
        raise Exception("在指定目录下未找到最近10秒内生成的OK图数据")


@utils.screenshot_error_to_excel()
def lxbj_006_01():
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
    utils.click_by_png(config.EXPORT_ALL_OK)
    if not utils.search_symbol_erroring(config.IF_EXPORT_ALL_OK, 5):
        raise Exception("未发现提示框")
    else:
        pyautogui.press('enter')
        utils.search_symbol_erroring(config.EXPORTING_OK, 5)
        utils.search_symbol_erroring(config.OK_COLLECTION, 5)
        pyautogui.press('enter')
    # 弹框提示：生成ok图完成，并可以在F:\DataExport\Job名\OKImage下发现
    ok_image_path = f"F:\\DataExport\\{program_name}\\OKImage"
    recent_files = [f for f in os.listdir(ok_image_path) if
                    os.path.getctime(os.path.join(ok_image_path, f)) > time.time() - 10]
    if not recent_files:
        raise Exception("在指定目录下未找到最近10秒内生成的OK图数据")


@utils.screenshot_error_to_excel()
def lxbj_006_02():
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
    utils.click_by_png(config.EXPORT_ALL_OK)
    if not utils.search_symbol_erroring(config.IF_EXPORT_ALL_OK, 5):
        raise Exception("未发现提示框")
    else:
        pyautogui.press('enter')
        utils.search_symbol_erroring(config.EXPORTING_OK, 5)
        utils.search_symbol_erroring(config.OK_COLLECTION, 60)
        pyautogui.press('enter')
    # 弹框提示：生成ok图完成，并可以在F:\DataExport\Job名\OKImage下发现
    ok_image_path = f"F:\\DataExport\\{program_name}\\OKImage"
    recent_files = [f for f in os.listdir(ok_image_path) if
                    os.path.getctime(os.path.join(ok_image_path, f)) > time.time() - 10]
    if not recent_files:
        raise Exception("在指定目录下未找到最近10秒内生成的OK图数据")


# 参数配置--演算法配置--关联子框检测模式：选择【父框检测NG不计算】
@utils.screenshot_error_to_excel()
def lxbj_007_01():
    utils.check_and_launch_aoi()
    utils.check_patent_not_NG(1)
    # 1、在某一元件的【元器件编辑】界面，点击上方【检测窗口】添加父、子框，如父框：方形定位、子框：颜色面积
    utils.ensure_in_edit_mode()
    # 先检测左下角有没有窗口,有的话删除 
    pyautogui.hotkey('ctrl', 'a')
    utils.click_by_png(config.GUI_EDIT_DELETE)
    pyautogui.press('enter')
    utils.add_window()
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    time.sleep(5)
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(5)
    # 2、父、子框同时选中后，点击上方【关联】
    pyautogui.hotkey('ctrl', 'a')
    utils.click_by_png(config.RELATE_WINDOW)
    result = utils.check_color_in_region()
    if not result:
        raise Exception("未检测到红色连接线")
    # 3、选中父框，如向上移动，使之测试结果变成NG 
    pyautogui.click(config.W_0_COORDINATE)
    time.sleep(3)
    pyautogui.press('up', presses=20, interval=0.25)
    # 4、选择子框后，点击【测试当前窗口】
    pyautogui.click(config.W_1_COORDINATE)
    time.sleep(1)
    utils.click_by_png(config.TEST_WINDOW)
    time.sleep(3)
    utils.search_symbol_erroring(config.ALG_RESULT_0, 5)
    # 5、点击【测试当前元件】
    utils.click_by_png(config.TEST_COMPONENT)
    time.sleep(5)
    utils.search_symbol_erroring(config.ALG_RESULT_0, 5)
    # 6、点击【测试当前分组】
    utils.click_by_png(config.TEST_GROUP)
    time.sleep(5)
    utils.search_symbol_erroring(config.ALG_RESULT_0, 20)
    # TODO 位置是矫正后的位置，与父框移动的方向相反。


# 1、参数配置--演算法配置--关联子框检测模式：选择【父框检测NG不计算】
# 2、父框检测结果是良好
@utils.screenshot_error_to_excel()
def lxbj_007_02():
    utils.check_and_launch_aoi()
    utils.check_patent_not_NG(1)
    # 1、在某一元件的【元器件编辑】界面，点击上方【检测窗口】添加父、子框，如父框：方形定位、子框：颜色面积
    utils.ensure_in_edit_mode()
    # 先检测左下角有没有窗口,有的话删除 
    pyautogui.hotkey('ctrl', 'a')
    utils.click_by_png(config.GUI_EDIT_DELETE)
    pyautogui.press('enter')
    utils.add_window()
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    time.sleep(5)
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(5)
    # 2、父、子框同时选中后，点击上方【关联】
    pyautogui.hotkey('ctrl', 'a')
    utils.click_by_png(config.RELATE_WINDOW)
    result = utils.check_color_in_region()
    if not result:
        raise Exception("未检测到红色连接线")
    # 4、选择子框后，点击【测试当前窗口】
    time.sleep(1)
    pyautogui.click(config.W_1_COORDINATE)
    time.sleep(2)
    utils.click_by_png(config.TEST_WINDOW)
    time.sleep(3)
    # if utils.search_symbol(config.ALG_RESULT_0, 5):
    #     raise Exception("算法结果为零")
    # 5、点击【测试当前元件】
    utils.click_by_png(config.TEST_COMPONENT)
    time.sleep(5)
    # if utils.search_symbol(config.ALG_RESULT_0, 5):
    #     raise Exception("算法结果为零")
    # 6、点击【测试当前分组】
    utils.click_by_png(config.TEST_GROUP)
    time.sleep(5)
    # if utils.search_symbol(config.ALG_RESULT_0, 20):
    #     raise Exception("算法结果为零")
    # TODO 位置不变


# 参数配置--演算法配置--关联子框检测模式：选择【父框检测NG继续计算】
@utils.screenshot_error_to_excel()
def lxbj_008_01():
    utils.check_and_launch_aoi()
    utils.check_patent_not_NG(2)
    # 1、在某一元件的【元器件编辑】界面，点击上方【检测窗口】添加父、子框，如父框：方形定位、子框：颜色面积
    utils.ensure_in_edit_mode()
    # 先检测左下角有没有窗口,有的话删除 
    pyautogui.hotkey('ctrl', 'a')
    utils.click_by_png(config.GUI_EDIT_DELETE)
    pyautogui.press('enter')
    utils.add_window()
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    time.sleep(5)
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(5)
    # 2、父、子框同时选中后，点击上方【关联】
    pyautogui.hotkey('ctrl', 'a')
    utils.click_by_png(config.RELATE_WINDOW)
    result = utils.check_color_in_region()
    if not result:
        raise Exception("未检测到红色连接线")
    # 3、选中父框，如向上移动，使之测试结果变成NG
    pyautogui.click(config.W_0_COORDINATE)
    time.sleep(3)
    pyautogui.press('up', presses=20, interval=0.45)
    # 4、选择子框后，点击【测试当前窗口】
    pyautogui.click(config.W_1_COORDINATE)
    time.sleep(3)
    utils.click_by_png(config.TEST_WINDOW)
    time.sleep(3)
    # if utils.search_symbol(config.ALG_RESULT_0, 5):
    #     raise Exception("算法结果为零")
    # 5、点击【测试当前元件】
    utils.click_by_png(config.TEST_COMPONENT)
    time.sleep(5)
    # if utils.search_symbol(config.ALG_RESULT_0, 5):
    #     raise Exception("算法结果为零")
    # 6、点击【测试当前分组】
    utils.click_by_png(config.TEST_GROUP)
    time.sleep(5)
    # if utils.search_symbol(config.ALG_RESULT_0, 20):
    #     raise Exception("算法结果为零")
    # TODO 位置是矫正后的位置，与父框移动的方向相反。


# 1、参数配置--演算法配置--关联子框检测模式：选择【父框检测NG继续计算】
# 2、父框检测结果是良好
@utils.screenshot_error_to_excel()
def lxbj_008_02():
    utils.check_and_launch_aoi()
    utils.check_patent_not_NG(2)
    # 1、在某一元件的【元器件编辑】界面，点击上方【检测窗口】添加父、子框，如父框：方形定位、子框：颜色面积
    utils.ensure_in_edit_mode()
    # 先检测左下角有没有窗口,有的话删除 
    pyautogui.hotkey('ctrl', 'a')
    utils.click_by_png(config.GUI_EDIT_DELETE)
    pyautogui.press('enter')
    utils.add_window()
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    time.sleep(5)
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(5)
    # 2、父、子框同时选中后，点击上方【关联】
    pyautogui.hotkey('ctrl', 'a')
    utils.click_by_png(config.RELATE_WINDOW)
    time.sleep(1)
    result = utils.check_color_in_region()
    if not result:
        raise Exception("未检测到红色连接线")
    # 4、选择子框后，点击【测试当前窗口】
    pyautogui.click(config.W_1_COORDINATE)
    time.sleep(1)
    utils.click_by_png(config.TEST_WINDOW)
    time.sleep(3)
    # if utils.search_symbol(config.ALG_RESULT_0, 5):
    #     raise Exception("算法结果为零")
    # 5、点击【测试当前元件】
    utils.click_by_png(config.TEST_COMPONENT)
    time.sleep(5)
    # if utils.search_symbol(config.ALG_RESULT_0, 5):
    #     raise Exception("算法结果为零")
    # 6、点击【测试当前分组】
    utils.click_by_png(config.TEST_GROUP)
    time.sleep(5)
    # if utils.search_symbol(config.ALG_RESULT_0, 20):
    #     raise Exception("算法结果为零")
    # TODO 位置不变


# 参数配置--演算法配置--关联子框检测模式：选择【父框检测NG继续关联】
@utils.screenshot_error_to_excel()
def lxbj_009_01():
    utils.check_and_launch_aoi()
    utils.check_patent_not_NG(3)
    # 1、在某一元件的【元器件编辑】界面，点击上方【检测窗口】添加父、子框，如父框：方形定位、子框：颜色面积
    utils.ensure_in_edit_mode()
    # 先检测左下角有没有窗口,有的话删除 
    pyautogui.hotkey('ctrl', 'a')
    utils.click_by_png(config.GUI_EDIT_DELETE)
    pyautogui.press('enter')
    utils.add_window()
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    time.sleep(5)
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(5)
    # 2、父、子框同时选中后，点击上方【关联】
    pyautogui.hotkey('ctrl', 'a')
    utils.click_by_png(config.RELATE_WINDOW)
    result = utils.check_color_in_region()
    if not result:
        raise Exception("未检测到红色连接线")
    # 3、选中父框，如向上移动，使之测试结果变成NG 
    pyautogui.click(config.W_0_COORDINATE)
    time.sleep(1)
    pyautogui.press('up', presses=20, interval=0.45)
    # 4、选择子框后，点击【测试当前窗口】
    pyautogui.click(config.W_1_COORDINATE)
    time.sleep(1)
    utils.click_by_png(config.TEST_WINDOW)
    time.sleep(3)
    # if utils.search_symbol(config.ALG_RESULT_0, 5):
    #     raise Exception("算法结果为零")
    # 5、点击【测试当前元件】
    utils.click_by_png(config.TEST_COMPONENT)
    time.sleep(5)
    # if utils.search_symbol(config.ALG_RESULT_0, 5):
    #     raise Exception("算法结果为零")
    # 6、点击【测试当前分组】
    utils.click_by_png(config.TEST_GROUP)
    time.sleep(5)
    # if utils.search_symbol(config.ALG_RESULT_0, 20):
    #     raise Exception("算法结果为零")
    # TODO 位置是矫正后的位置，与父框移动的方向相反。


# 1、参数配置--演算法配置--关联子框检测模式：选择【父框检测NG继续关联】
# 2、父框检测结果是良好
@utils.screenshot_error_to_excel()
def lxbj_009_02():
    utils.check_and_launch_aoi()
    utils.check_patent_not_NG(3)
    # 1、在某一元件的【元器件编辑】界面，点击上方【检测窗口】添加父、子框，如父框：方形定位、子框：颜色面积
    utils.ensure_in_edit_mode()
    # 先检测左下角有没有窗口,有的话删除 
    pyautogui.hotkey('ctrl', 'a')
    utils.click_by_png(config.GUI_EDIT_DELETE)
    pyautogui.press('enter')
    utils.add_window()
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    time.sleep(5)
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    time.sleep(5)
    # 2、父、子框同时选中后，点击上方【关联】
    pyautogui.hotkey('ctrl', 'a')
    utils.click_by_png(config.RELATE_WINDOW)
    result = utils.check_color_in_region()
    if not result:
        raise Exception("未检测到红色连接线")
    # 4、选择子框后，点击【测试当前窗口】
    pyautogui.click(config.W_1_COORDINATE)
    time.sleep(1)
    utils.click_by_png(config.TEST_WINDOW)
    time.sleep(3)
    # if utils.search_symbol(config.ALG_RESULT_0, 5):
    #     raise Exception("算法结果为零")
    # 5、点击【测试当前元件】
    utils.click_by_png(config.TEST_COMPONENT)
    time.sleep(5)
    # if utils.search_symbol(config.ALG_RESULT_0, 5):
    #     raise Exception("算法结果为零")
    # 6、点击【测试当前分组】
    utils.click_by_png(config.TEST_GROUP)
    time.sleep(5)
    # if utils.search_symbol(config.ALG_RESULT_0, 20):
    #     raise Exception("算法结果为零")
    # TODO 位置不变


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
    utils.click_by_png(config.PACKAGE_CLOSE)


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
    b = (730,375)
    pyautogui.click(a)
    time.sleep(1)
    part_no_a = pyautogui.screenshot(region= config.SINGLE_PART_NO_REGION)
    pyautogui.click(b)
    time.sleep(1)
    part_no_b = pyautogui.screenshot(region= config.SINGLE_PART_NO_REGION)
    # 分别点击几个封装类型，截图料号
    pyautogui.keyDown('ctrl')
    pyautogui.click(a)
    pyautogui.click(b)
    pyautogui.keyUp('ctrl')
    # TODO 新的封装类型包含所有料号
    utils.click_by_png(config.EDIT_PACKAGE_TYPE)
    pyautogui.write('test')
    pyautogui.press('enter')
    if utils.search_symbol(part_no_a, 3) and utils.search_symbol(part_no_b, 3):
        logger.info("新的封装类型包含所有料号")
    else:
        raise Exception("新的封装类型不包含所有料号")

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
    utils.click_by_png(config.COPY_PACKAGE_TYPE_NAME)
    old_content = pyperclip.paste()
    utils.click_by_png(config.CLEAR_PACKAGE_TYPE)
    pyautogui.press('enter')
    # 编辑完后 在封装类型处输入剪切板的内容 点击查询
    pyautogui.click((840, 290))
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'v')
    utils.click_by_png(config.QUERY)
    # 检测剪切板内容是否为test 不是的行报错
    utils.click_by_png(config.COPY_PACKAGE_TYPE_NAME)
    new_content = pyperclip.paste()
    if new_content == old_content:
        raise Exception("封装类型删除失败")
    utils.click_by_png(config.PACKAGE_CLOSE)



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
    utils.click_by_png(config.COPY_PACKAGE_TYPE_NAME)
    content_a = pyperclip.paste()
    pyautogui.click(b)
    utils.click_by_png(config.COPY_PACKAGE_TYPE_NAME)
    content_b = pyperclip.paste()
    pyautogui.keyDown('ctrl')
    pyautogui.click(a)
    pyautogui.click(b)
    pyautogui.keyUp('ctrl')
    utils.click_by_png(config.CLEAR_PACKAGE_TYPE)
    pyautogui.press('enter')
    time.sleep(2)
    utils.click_by_png(config.COPY_PACKAGE_TYPE_NAME)
    content_c = pyperclip.paste()
    if content_a != content_c and content_b != content_c:
        logger.info("删除成功")
    else:
        raise Exception("删除失败")


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
    pyautogui.click(config.FOV_SENIOR_COORDINATE)
    time.sleep(2)
    utils.write_text(config.FOV_EXPAND_COORDINATE, "3000")
    # 6、在【整板异物】Tab页，点击【整板遮罩编辑】，查看元件的遮罩
    utils.click_by_png(config.FOV_EDIT)
    # 元件遮罩（粉红色）变大
    utils.search_symbol_erroring(config.BOARD_COLOR_FILTER)
    time.sleep(3)
    if not utils.check_color_expand():
        raise Exception("元件遮罩（粉红色）未变大")
    utils.click_by_png(config.BOARD_COLOR_FILTER_CLOSE)

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
    if utils.search_symbol(config.IMAGE_PROCESS_TOPIC, 5):
        utils.click_by_png(config.YES)
    if utils.search_symbol(config.ADD_IMAGE_CLOSE, 5):
        utils.click_by_png(config.ADD_IMAGE_CLOSE)
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
    if utils.search_symbol(config.IMAGE_PROCESS_TOPIC, 5):
        utils.click_by_png(config.YES)
    if utils.search_symbol(config.ADD_IMAGE_CLOSE, 5):
        utils.click_by_png(config.ADD_IMAGE_CLOSE)
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
    time.sleep(2)  # 等待待料调整完成
    final_screenshot = pyautogui.screenshot(region=(820, 817, 29, 167))
    if initial_screenshot == final_screenshot:
        logger.error("RGB相互影响了")
    else:
        logger.info("RGB不相互影响")

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
    if utils.search_symbol(config.IMAGE_PROCESS_TOPIC, 5):
        utils.click_by_png(config.YES)
    if utils.search_symbol(config.ADD_IMAGE_CLOSE, 5):
        utils.click_by_png(config.ADD_IMAGE_CLOSE)
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


@utils.screenshot_error_to_excel()
def lxbj_013_01():
    utils.check_and_launch_aoi()
    # 1、使用快捷键，打开某一包含多个检测窗口的djb文件
    utils.ensure_in_edit_mode()
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


@utils.screenshot_error_to_excel()
def lxbj_013_02():
    utils.check_and_launch_aoi()
    # 1、使用快捷键，打开某一包含多个检测窗口的djb文件
    utils.ensure_in_edit_mode()
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


@utils.screenshot_error_to_excel()
def lxbj_013_03():
    utils.check_and_launch_aoi()
    # 1、使用快捷键，打开某一包含多个检测窗口的djb文件
    utils.ensure_in_edit_mode()
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


# 14开头的前置条件：元件带有字符检测窗口
@utils.screenshot_error_to_excel()
def lxbj_014_01():
    utils.check_and_launch_aoi()
    # 1、某一元件的【元器件编辑】界面
    utils.ensure_in_edit_mode()
    utils.add_window()
    utils.click_by_png(config.ADD_CHECKED_OCV)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
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
    utils.caton_or_flashback()


@utils.screenshot_error_to_excel()
def lxbj_014_02():
    utils.check_and_launch_aoi()
    # 1、某一元件的【元器件编辑】界面
    utils.ensure_in_edit_mode()
    utils.add_window()
    utils.click_by_png(config.ADD_CHECKED_OCV)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
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
    utils.caton_or_flashback()


@utils.screenshot_error_to_excel()
def lxbj_014_03():
    utils.check_and_launch_aoi()
    # 1、某一元件的【元器件编辑】界面
    utils.ensure_in_edit_mode()
    utils.add_window()
    utils.click_by_png(config.ADD_CHECKED_OCV)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
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
    utils.caton_or_flashback()


@utils.screenshot_error_to_excel()
def lxbj_014_04():
    utils.check_and_launch_aoi()
    # 1、某一元件的【元器件编辑】界面
    utils.ensure_in_edit_mode()
    utils.add_window()
    utils.click_by_png(config.ADD_CHECKED_OCV)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
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
    utils.caton_or_flashback()


@utils.screenshot_error_to_excel()
def lxbj_014_05():
    utils.check_and_launch_aoi()
    # 1、某一元件的【元器件编辑】界面
    utils.ensure_in_edit_mode()
    utils.add_window()
    utils.click_by_png(config.ADD_CHECKED_OCV)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
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
    utils.caton_or_flashback()


@utils.screenshot_error_to_excel()
def lxbj_014_06():
    utils.check_and_launch_aoi()
    # 1、某一元件的【元器件编辑】界面
    utils.ensure_in_edit_mode()
    utils.add_window()
    utils.click_by_png(config.ADD_CHECKED_OCV)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
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
    utils.caton_or_flashback()


@utils.screenshot_error_to_excel()
def lxbj_014_07():
    utils.check_and_launch_aoi()
    # 1、某一元件的【元器件编辑】界面
    utils.ensure_in_edit_mode()
    utils.add_window()
    utils.click_by_png(config.ADD_CHECKED_OCV)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
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
    utils.caton_or_flashback()


@utils.screenshot_error_to_excel()
def lxbj_014_08():
    utils.check_and_launch_aoi()
    # 1、某一元件的【元器件编辑】界面
    utils.ensure_in_edit_mode()
    utils.add_window()
    utils.click_by_png(config.ADD_CHECKED_OCV)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
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
    utils.caton_or_flashback()


@utils.screenshot_error_to_excel()
def lxbj_014_09():
    utils.check_and_launch_aoi()
    # 1、某一元件的【元器件编辑】界面
    utils.ensure_in_edit_mode()
    utils.add_window()
    utils.click_by_png(config.ADD_CHECKED_OCV)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
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
    utils.caton_or_flashback()


@utils.screenshot_error_to_excel()
def lxbj_014_10():
    utils.check_and_launch_aoi()
    # 1、某一元件的【元器件编辑】界面
    utils.ensure_in_edit_mode()
    utils.add_window()
    utils.click_by_png(config.ADD_CHECKED_OCV)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
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
    utils.caton_or_flashback()


@utils.screenshot_error_to_excel()
def lxbj_014_11():
    utils.check_and_launch_aoi()
    # 1、某一元件的【元器件编辑】界面
    utils.ensure_in_edit_mode()
    utils.add_window()
    utils.click_by_png(config.ADD_CHECKED_OCV)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
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
    utils.caton_or_flashback()


@utils.screenshot_error_to_excel()
def lxbj_014_12():
    utils.check_and_launch_aoi()
    # 1、某一元件的【元器件编辑】界面
    utils.ensure_in_edit_mode()
    utils.add_window()
    utils.click_by_png(config.ADD_CHECKED_OCV)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
    utils.click_by_png(config.YES)
    time.sleep(1)
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
    utils.caton_or_flashback()


@utils.screenshot_error_to_excel()
def lxbj_015_01():
    utils.check_and_launch_aoi()
    # 1、某一元器件编辑界面，在上方【编辑】--【光源】选择不同光源，如中角度（不选均匀光）；
    utils.ensure_in_edit_mode()
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


# 元件添加参考点关联所有检测框
@utils.screenshot_error_to_excel()
def lxbj_016_01():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    utils.click_by_png(config.EDIT_BACK)
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(3)
    # 右键直到搜索到添加参考点的框
    found = False
    attempts = 0
    while not found and attempts < 3:
        for y in range(config.COMPONENT_REGION[1], config.COMPONENT_REGION[1] + config.COMPONENT_REGION[3], 20):
            for x in range(config.COMPONENT_REGION[0] + config.COMPONENT_REGION[2] - 10, config.COMPONENT_REGION[0], -20):
                pyautogui.rightClick(x, y)
                time.sleep(0.2)
                if utils.search_symbol(config.ADD_REFERENCE_POINT, timeout=3,region=config.COMPONENT_REGION):
                    utils.click_by_png(config.ADD_REFERENCE_POINT, timeout=3,region=config.COMPONENT_REGION)
                    time.sleep(5)
                    found = True
                    break
            if found:
                break
        attempts += 1
        if not found:
            pyautogui.moveTo(config.COMPONENT_REGION[0] + config.COMPONENT_REGION[2] - 20 * attempts, config.COMPONENT_REGION[1])
    utils.click_chosed_component(2,config.BOARD_INFORMATION_REGION)
    time.sleep(3)
    # 先加一个方形检测
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


# 元件添加参考点关联所有检测框
@utils.screenshot_error_to_excel()
def lxbj_016_02():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    utils.click_by_png(config.EDIT_BACK)
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(3)
    # 右键直到搜索到添加参考点的框
    found = False
    attempts = 0
    while not found and attempts < 3:
        for y in range(config.COMPONENT_REGION[1], config.COMPONENT_REGION[1] + config.COMPONENT_REGION[3], 20):
            for x in range(config.COMPONENT_REGION[0] + config.COMPONENT_REGION[2] - 10, config.COMPONENT_REGION[0], -20):
                pyautogui.rightClick(x, y)
                time.sleep(0.2)
                if utils.search_symbol(config.ADD_REFERENCE_POINT, timeout=3,region=config.COMPONENT_REGION):
                    utils.click_by_png(config.ADD_REFERENCE_POINT, timeout=3,region=config.COMPONENT_REGION)
                    time.sleep(5)
                    found = True
                    break
            if found:
                break
        attempts += 1
        if not found:
            pyautogui.moveTo(config.COMPONENT_REGION[0] + config.COMPONENT_REGION[2] - 20 * attempts, config.COMPONENT_REGION[1])
    utils.click_chosed_component(2,config.BOARD_INFORMATION_REGION)
    time.sleep(3)
    # 先加一个方形检测
    utils.add_window()
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    # 再加一个颜色面积检测
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.CLICK_RELATE)
    if not utils.check_color_in_region():
        raise Exception('子框与父框未连接')
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.CLICK_CANCEL_RELATE)
    if utils.check_color_in_region():
        raise Exception('检测框取消关联失败')


# 元件添加参考点关联所有检测框
@utils.screenshot_error_to_excel()
def lxbj_016_03():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    utils.click_by_png(config.EDIT_BACK)
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(3)
    # 右键直到搜索到添加参考点的框
    found = False
    attempts = 0
    while not found and attempts < 3:
        for y in range(config.COMPONENT_REGION[1], config.COMPONENT_REGION[1] + config.COMPONENT_REGION[3], 20):
            for x in range(config.COMPONENT_REGION[0] + config.COMPONENT_REGION[2] - 10, config.COMPONENT_REGION[0], -20):
                pyautogui.rightClick(x, y)
                time.sleep(0.2)
                if utils.search_symbol(config.ADD_REFERENCE_POINT, timeout=3,region=config.COMPONENT_REGION):
                    utils.click_by_png(config.ADD_REFERENCE_POINT, timeout=3,region=config.COMPONENT_REGION)
                    time.sleep(5)
                    found = True
                    break
            if found:
                break
        attempts += 1
        if not found:
            pyautogui.moveTo(config.COMPONENT_REGION[0] + config.COMPONENT_REGION[2] - 20 * attempts, config.COMPONENT_REGION[1])
    utils.click_chosed_component(2,config.BOARD_INFORMATION_REGION)
    time.sleep(3)
    # 先加一个方形检测
    utils.add_window()
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    # 再加一个颜色面积检测
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('F5')
    if not utils.check_color_in_region():
        raise Exception('子框与父框未连接')


# 元件添加参考点关联所有检测框
@utils.screenshot_error_to_excel()
def lxbj_016_04():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    utils.click_by_png(config.EDIT_BACK)
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(3)
    # 右键直到搜索到添加参考点的框
    found = False
    attempts = 0
    while not found and attempts < 3:
        for y in range(config.COMPONENT_REGION[1], config.COMPONENT_REGION[1] + config.COMPONENT_REGION[3], 20):
            for x in range(config.COMPONENT_REGION[0] + config.COMPONENT_REGION[2] - 10, config.COMPONENT_REGION[0], -20):
                pyautogui.rightClick(x, y)
                time.sleep(0.2)
                if utils.search_symbol(config.ADD_REFERENCE_POINT, timeout=3,region=config.COMPONENT_REGION):
                    utils.click_by_png(config.ADD_REFERENCE_POINT, timeout=3,region=config.COMPONENT_REGION)
                    time.sleep(5)
                    found = True
                    break
            if found:
                break
        attempts += 1
        if not found:
            pyautogui.moveTo(config.COMPONENT_REGION[0] + config.COMPONENT_REGION[2] - 20 * attempts, config.COMPONENT_REGION[1])
    utils.click_chosed_component(2,config.BOARD_INFORMATION_REGION)
    time.sleep(3)
    # 先加一个方形检测
    utils.add_window()
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    # 再加一个颜色面积检测
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.click(config.CENTRE)
    utils.click_by_png(config.CLICK_AUTO_LINK)
    if not utils.check_color_in_region():
        raise Exception('子框与父框未连接')


#元件添加参考点关联所有检测框
@utils.screenshot_error_to_excel()
def lxbj_016_05():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    utils.click_by_png(config.EDIT_BACK)
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(3)
    # 右键直到搜索到添加参考点的框
    found = False
    attempts = 0
    while not found and attempts < 3:
        for y in range(config.COMPONENT_REGION[1], config.COMPONENT_REGION[1] + config.COMPONENT_REGION[3], 20):
            for x in range(config.COMPONENT_REGION[0] + config.COMPONENT_REGION[2] - 10, config.COMPONENT_REGION[0], -20):
                pyautogui.rightClick(x, y)
                time.sleep(0.2)
                if utils.search_symbol(config.ADD_REFERENCE_POINT, timeout=3,region=config.COMPONENT_REGION):
                    utils.click_by_png(config.ADD_REFERENCE_POINT, timeout=3,region=config.COMPONENT_REGION)
                    time.sleep(5)
                    found = True
                    break
            if found:
                break
        attempts += 1
        if not found:
            pyautogui.moveTo(config.COMPONENT_REGION[0] + config.COMPONENT_REGION[2] - 20 * attempts, config.COMPONENT_REGION[1])
    utils.click_chosed_component(2,config.BOARD_INFORMATION_REGION)
    time.sleep(3)
    # 先加一个方形检测
    utils.add_window()
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    # 再加一个颜色面积检测
    utils.add_window()
    utils.click_by_png(config.COLOR_AREA)
    utils.click_by_png(config.YES)
    pyautogui.hotkey('ctrl', 'a')
    utils.click_by_png(config.RELATE_WINDOW)
    if not utils.check_color_in_region():
        raise Exception('子框与父框未连接')
    utils.click_by_png(config.CANCEL_RELATE_WINDOW)
    if utils.check_color_in_region():
        raise Exception('检测框取消关联失败')


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
    time.sleep(20)
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


@utils.screenshot_error_to_excel()
def lxbj_018_02():
    utils.check_and_launch_aoi()
    # 1、打开一个编辑过的有多个拼版的job
    utils.ensure_multiple_collages()
    time.sleep(20)
    utils.click_by_png(config.PROGRAM_COMPONENT_DARK)
    time.sleep(2)
    before_num_region = pyautogui.screenshot(region=config.COMPONENT_NUM_REGION)
    utils.click_by_png(config.WHOLE_BOARD_DARK)
    time.sleep(0.5)
    utils.click_by_png(config.BOARD_REDUCE)
    before_edit_region = pyautogui.screenshot(region=config.COMPONENT_REGION)
    time.sleep(3)
    # 2、点击拼版操作 再点击删除拼版
    utils.click_by_png(config.BOARD_BOARD)
    utils.click_by_png(config.BOARD_SPLICING_OPERATION)
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

# TODO 保留基准点
@utils.screenshot_error_to_excel()
def lxbj_018_03():
    utils.check_and_launch_aoi()
    # 1、打开一个编辑过的有多个拼版的job
    utils.ensure_multiple_collages()
    time.sleep(20)
    utils.click_by_png(config.PROGRAM_COMPONENT_DARK)
    time.sleep(2)
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
    # 4、勾选保留基准点
    pyautogui.click(config.RESERVE_BENCHMARK_COORDINATE)
    # 5、点击【是】
    pyautogui.press('enter')
    time.sleep(5)
    now_edit_region = pyautogui.screenshot(region=config.COMPONENT_REGION)
    utils.click_by_png(config.PROGRAM_COMPONENT_DARK)
    utils.click_by_png(config.BOARD_REDUCE)
    now_num_region = pyautogui.screenshot(region=config.COMPONENT_NUM_REGION)
    if before_num_region == now_num_region and before_edit_region != now_edit_region:
        logger.info('拼版被删除且元件保留')
    else:
        logger.error('元件未被保留/拼版未被删除')
        raise Exception('元件未被保留/拼版未被删除')


# 选择一个拼版删除并保留基准点
@utils.screenshot_error_to_excel()
def lxbj_018_04():
    utils.check_and_launch_aoi()
    # 1、打开一个编辑过的有多个拼版的job
    utils.ensure_multiple_collages()
    time.sleep(20)
    utils.click_by_png(config.PROGRAM_COMPONENT_DARK)
    time.sleep(2)
    before_num_region = pyautogui.screenshot(region=config.COMPONENT_NUM_REGION)
    utils.click_by_png(config.WHOLE_BOARD_DARK)
    time.sleep(0.5)
    utils.click_by_png(config.BOARD_REDUCE)
    before_edit_region = pyautogui.screenshot(region=config.COMPONENT_REGION)
    time.sleep(3)
    # 2、点击拼版操作 再点击删除拼版
    utils.click_by_png(config.BOARD_BOARD)
    utils.click_by_png(config.BOARD_SPLICING_OPERATION)
    utils.click_by_png(config.BOARD_DELETE_IMPOSITION)
    # 4、勾选保留基准点
    pyautogui.click(config.RESERVE_BENCHMARK_COORDINATE)
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
