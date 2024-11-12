import datetime
import os
import shutil
from loguru import logger
import psutil
import utils
import time
import pyautogui
import config

# @utils.screenshot_error_to_excel()
# 新建单板程式
# def jbgn_001_01():
    # 1、新建程式文件：选择保存目录，选择单板CAD文件，输入【程式名称】，【是】
    # 2、点击进版
    # 3、待页面上方绿色方块到中间位置，点击【移到板边】，将版右下角位置移到屏幕中心十字线，点击【右下角标记位】
    # 4、点击操作镜头的字母让其变成EG再点击左上箭头
    # 5、将版左上角移动到屏幕中心十字线，点击【左上角标记位】
    # 6、点击【扫描整版】
    # 7、点击【是】
    # 8、确认基板颜色提示框，根据实际情况点击【是】或【否】
    # 9、弹出导入库提示框，选择【Default】后点击是
    # 10、选中MARK点附近的空元件：Designator，右键选择【标记点操作】--【转换为标记点】--【是】
    # 11、选中标记点--右键选择【标记点操作】--【根据标记点矫正元件】


    # pass



# @utils.screenshot_error_to_excel()
# 新建单板程式后测试RV复判并在SPC确认数据
# def jbgn_001_02():
    # 1、接上条用例，新建JOB后
    # 2、点击【运行】开始测试
    # 3、点击【是】按钮
    # 4、检查FOV，元件数
    # 5、检测过程，观察界面右上角【测试状态】--【FOVs】和【元件】的进度条
    # 6、测试完成后打开RV确认
    # 7、在RV对当前测试数据进行复判
    # 8、到SPC查看RV复判的数据





# @utils.screenshot_error_to_excel()
# def jbgn_001_03():



@utils.screenshot_error_to_excel()
def jbgn_001_04():
    for i in range (2):
        # 1、打开AOI软件，软件点击左上角【打开程式】按钮
        utils.check_and_launch_aoi()
        screen_before = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
        while not utils.search_symbol(config.OPEN_PROGRAM_TOPIC, 2):
            time.sleep(1)
            utils.click_by_png(config.OPEN_PROGRAM)
        time.sleep(2)
        # 2、在弹窗中的【程式主目录】，选择程式的目录或输入程式目录，例：D:\EYAOI\JOB，回车
        directory = r"D:\EYAOI\JOB"
        pyautogui.press("enter")
        pyautogui.write(directory)
        time.sleep(0.5)
        utils.click_by_png(config.SELECT_FOLDER)
        utils.click_by_png(config.OFFSET_LEFT_1,tolerance=0.98, type="left")
        time.sleep(2)
        symbols = [config.OPEN_PROGRAM_PLUS, config.OPEN_PROGRAM_CURSOR]
        found = False
        program_count = 0
        for symbol in symbols:
            try:
                located_symbols = list(pyautogui.locateAllOnScreen(symbol, region=config.PROGRAM_LIST_REGION))
                program_count += len(located_symbols)
                logger.info(f"找到 {len(located_symbols)} 个 {symbol} 符号")
            except Exception:
                logger.warning(f"未找到 {symbol} 符号")
                continue

        if program_count == 0:
            raise Exception("未发现任何程式")
        # 计算D:\EYAOI\JOB内，往下一级的第一级路径含有.tjb文件的文件夹个数
        folder_count = len([name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name)) and any(f.endswith('.tjb') for f in os.listdir(os.path.join(directory, name)))])
        # 比较数量是否相同
        if program_count != folder_count:
            logger.warning(f"未能显示目录下所有程式，实际程式数量: {program_count}，期望程式数量: {folder_count}")
            raise Exception("未能显示目录下所有程式")
        # 3、在【程式列表】--【主目录程式】，双击任一准备测试的程式
        for symbol in symbols:
            if utils.search_symbol(symbol, 3,region=config.PROGRAM_LIST_REGION):
                utils.click_by_png(symbol, 2,region=config.PROGRAM_LIST_REGION)
                if not utils.search_symbol(symbol, 3,region=config.SELECTED_PROGRAM_REGION):
                    raise Exception("双击后程式未出现在被选程式列表中")
                found = True
                break
            else:
                raise Exception("打开程式-程式列表内未发现程式")
        if not found:
            raise Exception("找不到程式")
        if i == 0:
            # 4、点击【取消】按钮
            utils.click_by_png(config.CANCEL)
            time.sleep(1)
            if utils.search_symbol(config.OPEN_PROGRAM_TOPIC):
                raise Exception("关闭打开程式弹窗失败")
            utils.search_symbol_erroring(config.AOI_TOPIC, 3)
            screen_after = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
            if screen_after != screen_before:
                raise Exception("点击取消后，疑似未回到整版视图界面")
            utils.close_aoi()
        elif i == 1:
            # 5、重复步骤1-3，点击【是】按钮
            utils.click_by_png(config.YES)
            time.sleep(1)
            if not utils.search_symbol(config.PROGRAM_LOADING, 5):
                raise Exception("未发现正在打开程式进度条")
            while utils.search_symbol(config.PROGRAM_LOADING, 5):
                time.sleep(5)
            if utils.search_symbol(config.OPEN_PROGRAM_TOPIC, 2):
                raise Exception("打开程式后还存在打开程式弹窗")
            time.sleep(3)
            if not utils.search_symbol(config.BOARD_AUTO,tolerance=0.75):
                raise Exception("点击是后，疑似未进入整版视图界面")
            time.sleep(3)
            utils.caton_or_flashback()
            utils.close_aoi()        
@utils.screenshot_error_to_excel()
def jbgn_001_05():
    # 1、打开AOI软件，点击左上角【打开程式】按钮
    utils.check_and_launch_aoi()
    while not utils.search_symbol(config.OPEN_PROGRAM_TOPIC, 2):
        time.sleep(1)
        utils.click_by_png(config.OPEN_PROGRAM)
    time.sleep(2)
    # 2、在弹窗中的【程式主目录】，选择程式的目录或输入程式目录，例：D:\EYAOI\JOB，回车
    directory = r"D:\EYAOI\JOB"
    pyautogui.press("enter")
    pyautogui.write(directory)
    time.sleep(0.5)
    utils.click_by_png(config.SELECT_FOLDER)
    utils.click_by_png(config.OFFSET_LEFT_1,tolerance=0.98, type="left")
    time.sleep(2)
    symbols = [config.OPEN_PROGRAM_PLUS, config.OPEN_PROGRAM_CURSOR]
    found = False
    program_count = 0
    for symbol in symbols:
        try:
            located_symbols = list(pyautogui.locateAllOnScreen(symbol, region=config.PROGRAM_LIST_REGION))
            program_count += len(located_symbols)
            logger.info(f"找到 {len(located_symbols)} 个 {symbol} 符号")
        except Exception:
            logger.warning(f"未找到 {symbol} 符号")
            continue

    if program_count == 0:
        raise Exception("未发现任何程式")
    # 计算D:\EYAOI\JOB内，往下一级的第一级路径含有.tjb文件的文件夹个数
    folder_count = len([name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name)) and any(f.endswith('.tjb') for f in os.listdir(os.path.join(directory, name)))])
    # 比较数量是否相同
    if program_count != folder_count:
        raise Exception("未能显示目录下所有程式")

    # 3、在【程式列表】--【主目录程式】，选中任一程式(压缩的程式图标变成带有箭头)，点击【轨1】（如果是双轨机台在轨2打开，显示【轨2】）
    symbols = [config.OPEN_PROGRAM_PLUS, config.OPEN_PROGRAM_CURSOR]
    found = False
    for symbol in symbols:
        if utils.search_symbol(symbol, 3,region=config.PROGRAM_LIST_REGION):
            utils.click_by_png(symbol, 2,region=config.PROGRAM_LIST_REGION)
            if not utils.search_symbol(symbol, 3,region=config.SELECTED_PROGRAM_REGION):
                raise Exception("双击后程式未出现在被选程式列表中")
            found = True
            break
        else:
            raise Exception("打开程式-程式列表内未发现程式")
    if not found:
        raise Exception("找不到程式")
    # 4、点击【是】按钮
    utils.click_by_png(config.YES)
    utils.search_symbol_erroring(config.PROGRAM_LOADING, 5)
    while utils.search_symbol(config.PROGRAM_LOADING, 5):
        time.sleep(5)
    if utils.search_symbol(config.OPEN_PROGRAM_TOPIC, 2):
        raise Exception("打开程式后还存在打开程式弹窗")
    utils.search_symbol_erroring(config.AOI_TOPIC, 3)
    utils.caton_or_flashback()
    utils.close_aoi()  
@utils.screenshot_error_to_excel()  
def jbgn_001_06():
    # 1、打开AOI软件，点击左上角【打开程式】按钮
    utils.check_and_launch_aoi()
    while not utils.search_symbol(config.OPEN_PROGRAM_TOPIC, 2):
        time.sleep(1)
        utils.click_by_png(config.OPEN_PROGRAM)
    time.sleep(2)
    # 2、在弹窗中的【程式主目录】，选择程式的目录或输入程式目录，例：D:\EYAOI\JOB，回车
    directory = r"D:\EYAOI\JOB"
    pyautogui.press("enter")
    pyautogui.write(directory)
    utils.click_by_png(config.SELECT_FOLDER)
    time.sleep(0.5)
    # 3、在【程式列表】--【主目录程式】，选中某一程式，点击【轨1】（如果是双轨机台在轨2打开，显示【轨2】）。按此操作，多次选择不同程式。
    # 先识别总共有多少个程式
    symbols = [config.OPEN_PROGRAM_PLUS, config.OPEN_PROGRAM_CURSOR]
    initial_count = 0
    utils.click_by_png(config.OFFSET_LEFT_1,tolerance=0.98, type="left")
    time.sleep(2)
    for symbol in symbols:
        try:
            located_symbols = list(pyautogui.locateAllOnScreen(symbol, region=config.PROGRAM_LIST_REGION))
            initial_count += len(located_symbols)
            logger.info(f"找到 {len(located_symbols)} 个 {symbol} 符号")
        except Exception:
            logger.warning(f"未找到 {symbol} 符号")
            continue
    logger.info(f"初始找到的程式数量: {initial_count}")
    if initial_count == 0:
        raise Exception("未发现任何程式")
    # 一个个去点加载
    for symbol in symbols:
        try:
            locations = list(pyautogui.locateAllOnScreen(symbol, region=config.PROGRAM_LIST_REGION))
            for location in locations:
                logger.info(f"点击 {symbol} 符号")
                utils.click_by_png(symbol, region=config.PROGRAM_LIST_REGION)
                utils.click_by_png(config.OPEN_PROGRAM_LOAD_1)
                time.sleep(1)
        except Exception:
            logger.warning(f"未找到 {symbol} 符号")
            continue
    logger.info("所有程式加载完成")

    final_count = 0
    for symbol in symbols:
        try:
            final_count += len(list(pyautogui.locateAllOnScreen(symbol, region=config.SELECTED_PROGRAM_REGION)))
        except Exception:
            logger.warning(f"未找到 {symbol} 符号")
            continue
    if initial_count != final_count:
        raise Exception("程式未完全出现再被选程式列表中")
    # 4、点击【是】按钮
    utils.click_by_png(config.YES)
    utils.search_symbol_erroring(config.PROGRAM_LOADING, 5)
    while utils.search_symbol(config.PROGRAM_LOADING, 5):
        time.sleep(5)
    if utils.search_symbol(config.OPEN_PROGRAM_TOPIC, 2):
        raise Exception("打开程式后还存在打开程式弹窗")
    utils.search_symbol_erroring(config.AOI_TOPIC, 3)
    utils.caton_or_flashback()
    utils.close_aoi()    
@utils.screenshot_error_to_excel()
def jbgn_001_07():
    # 1、打开AOI软件，点击左上角【打开程式】按钮
    utils.check_and_launch_aoi()
    while not utils.search_symbol(config.OPEN_PROGRAM_TOPIC, 2):
        time.sleep(1)
        utils.click_by_png(config.OPEN_PROGRAM)
    time.sleep(2)
    # 2、在弹窗中的【程式主目录】，选择程式的目录或输入程式目录，例：D:\EYAOI\JOB，回车
    directory = r"D:\EYAOI\JOB"
    # 进入打开程式界面之后会默认选中打开程式的按钮 所以直接回车
    pyautogui.press("enter")
    pyautogui.write(directory)
    utils.click_by_png(config.SELECT_FOLDER)
    time.sleep(0.5)
    utils.click_by_png(config.OFFSET_LEFT_1,tolerance=0.98, type="left")
    time.sleep(2)
    # 3、在【程式列表】--【主目录程式】，选中任一程式，点击【轨1】（如果是双轨机台在轨2打开，显示【轨2】）
    symbols = [config.OPEN_PROGRAM_PLUS, config.OPEN_PROGRAM_CURSOR]
    found = False
    temp = None
    for symbol in symbols:
        if utils.search_symbol(symbol, 3):
            temp = symbol
            utils.click_by_png(symbol, 2)
            utils.search_symbol_erroring(symbol, 3,region=config.SELECTED_PROGRAM_REGION)
            found = True
            break
    if not found:
        raise Exception("找不到程式")
    # 4、选中【被选程式列表】--【轨一被选程式】列表中的程式后，点击【移除】
    utils.click_by_png(temp, region=config.SELECTED_PROGRAM_REGION)
    utils.click_by_png(config.OPEN_PROGRAM_REMOVE)
    if utils.search_symbol(temp, 3, region=config.SELECTED_PROGRAM_REGION):
        raise Exception("移除程式失败")
    utils.close_aoi()
# @utils.screenshot_error_to_excel()
# def jbgn_001_08():
#     # 1、打开AOI软件，点击左上角【打开程式】按钮
#     utils.check_and_launch_aoi()
#     utils.check_auto_load_program(False)
#     while not utils.search_symbol(config.OPEN_PROGRAM_TOPIC, 2):
    #     time.sleep(1)
    #     utils.click_by_png(config.OPEN_PROGRAM)
    # time.sleep(2)
#     # 2、在弹窗中的【程式主目录】，选择程式的目录：D:\EYAOI\JOB\AAA测试专用，回车
#     # 进入打开程式界面之后会默认选中打开程式的按钮 所以直接回车
#     pyautogui.press("enter")
#     if not os.path.exists(r"D:\EYAOI\JOB\AAA测试专用\全算法（仅测试，勿修改）"):
#         pyautogui.alert(text='D:\\EYAOI\\JOB\\AAA测试专用\\全算法（仅测试，勿修改）不存在', title='错误', button='OK')
#         raise Exception("D:\\EYAOI\\JOB\\AAA测试专用\\全算法（仅测试，勿修改）不存在")

#     directory = r"D:\EYAOI\JOB\AAA测试专用"
#     pyautogui.write(directory)
#     pyautogui.press("enter")
#     symbols = [config.OPEN_PROGRAM_PLUS, config.OPEN_PROGRAM_CURSOR]
#     program_count = 0
#     for symbol in symbols:
#         try:
#             located_symbols = list(pyautogui.locateAllOnScreen(symbol, region=config.PROGRAM_LIST_REGION))
#             program_count += len(located_symbols)
#             logger.info(f"找到 {len(located_symbols)} 个 {symbol} 符号")
#         except Exception:
#             logger.warning(f"未找到 {symbol} 符号")
#             continue
#     if program_count == 0:
#         raise Exception("未发现任何程式")
        # 计算D:\EYAOI\JOB内，往下一级的第一级路径含有.tjb文件的文件夹个数
        # folder_count = len([name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name)) and any(f.endswith('.tjb') for f in os.listdir(os.path.join(directory, name)))])

#     # 比较数量是否相同
#     if program_count != folder_count:
#         raise Exception("未能显示目录下所有程式")
#     # 3、在【程式列表】--【主目录程式】，选中程式：【全算法（仅测试，勿修改）】，点击【轨1】（如果是双轨机台在轨2打开，显示【轨2】）
#     utils.click_by_png(config.OPEN_PROGRAM_ALL_ALGS, 2, tolerance=0.75)
#     memory_before = 0
#     for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
#         if 'Sinic-Tek AOI UI' in proc.info['name']:
#             memory_before = proc.info['memory_info'].rss
#             break
#     logger.info(f"打开程式前Sinic-Tek AOI UI进程的内存大小: {memory_before} bytes")

#     # 4、点击【是】按钮
#     utils.click_by_png(config.YES)
#     while utils.search_symbol(config.PROGRAM_LOADING, 5):
#         time.sleep(5)
#     # 5、查看打开时间：打开最近日志D:\EYAOI\Logger\Lane_0\UI_JOB_SAVE_OPEN_XX.log(XX--代表当前日期),在日志文本Open Job Calcu Time段落，查看End finally值
#     log_directory = r"D:\EYAOI\Logger\Lane_0"
#     log_file = max([os.path.join(log_directory, f) for f in os.listdir(log_directory) if f.startswith("UI_JOB_SAVE_OPEN_")], key=os.path.getctime)
    
#     with open(log_file, 'r', encoding='utf-8') as file:
#         lines = file.readlines()
    
#     end_finally_value = None
#     open_job_calcu_time_section = False
    
#     for line in lines:
#         if "============Open Job Calcu Time========" in line:
#             open_job_calcu_time_section = True
#         elif "=============================" in line and open_job_calcu_time_section:
#             break
#         elif open_job_calcu_time_section and "End finally:" in line:
#             end_finally_value = line.split(":")[1].strip()
#             break
    
#     if end_finally_value is None:
#         raise Exception("未找到End finally值")
    
#     logger.info(f"End finally值: {end_finally_value}")
#     # TODO End finally为多少时报错？


#     # 6、通过Windows任务管理器查看程式占用内存大小：启动AOI未打开程式时Sinic-Tek AOI UI(轨一)进程的内存大小，对比打开该程式后的内存大小，前后内存的差值--即该程式占用的内存
#     memory_after = 0
#     for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
#         if 'Sinic-Tek AOI UI' in proc.info['name']:
#             memory_after = proc.info['memory_info'].rss
#             break
#     logger.info(f"打开程式后Sinic-Tek AOI UI进程的内存大小: {memory_after} bytes")
#     occupied_memory = memory_after - memory_before
#     logger.info(f"程式占用内存大小: {occupied_memory} bytes")
#     # TODO 内存差值为多少时报错？



#     utils.close_aoi()

@utils.screenshot_error_to_excel()
def jbgn_001_09():
    # 1、打开AOI软件，点击左上角【打开程式】按钮
    utils.check_and_launch_aoi()
    while not utils.search_symbol(config.OPEN_PROGRAM_TOPIC, 2):
        time.sleep(1)
        utils.click_by_png(config.OPEN_PROGRAM)
    time.sleep(2)
    # 2、在弹窗中的【程式主目录】，选择程式的目录：D:\EYAOI\JOB\专用job，回车
    # directory = r"D:\EYAOI\JOB\专用job"
    # utils.write_text((660,195),directory)
    pyautogui.press("enter")
    # 3、在【程式列表】--【主目录程式】，选中程式：【Badmark测试-Mark8Barcode1】，点击【轨1】
    program_name = "Badmark测试-Mark8Barcode1"
    # utils.select_program(program_name)
    # 4、点击【是】按钮
    utils.click_by_png(config.YES)
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def jbgn_001_10():
    # 1、打开AOI软件，点击左上角【打开程式】按钮
    utils.check_and_launch_aoi()
    while not utils.search_symbol(config.OPEN_PROGRAM_TOPIC, 2):
        time.sleep(1)
        utils.click_by_png(config.OPEN_PROGRAM)
    time.sleep(2)
    # 2、在弹窗中的【程式主目录】，选择程式的目录：D:\EYAOI\JOB\专用job，回车
    directory = r"D:\EYAOI\JOB\专用job"
    utils.write_text((660,195),directory)
    pyautogui.press("enter")
    # 3、在【程式列表】--【主目录程式】，选中程式：【Badmark测试-Mark2Barcode4】，点击【轨1】
    program_name = "Badmark测试-Mark2Barcode4"
    # utils.select_program(program_name)
    # 4、点击【是】按钮
    utils.click_by_png(config.YES)
    while utils.search_symbol(config.PROGRAM_LOADING, 5):
        time.sleep(5)
    utils.close_aoi()
@utils.screenshot_error_to_excel()
def jbgn_001_11():
    # 1、打开AOI软件，点击左上角【打开程式】按钮
    utils.check_and_launch_aoi()
    # 2、在弹窗中的【程式主目录】，选择程式的目录：任意选择一个JOB
    # 3、点击【是】按钮
    utils.open_program()
    # 4、点击左上角【save to Job File】
    utils.click_by_png(config.SAVE)
    if utils.search_symbol(config.QUESTION_MARK):
        pyautogui.press("enter")
    while utils.search_symbol(config.SAVING_PROGRAM):
        time.sleep(3)
    latest_folder = max([os.path.join(r"D:\EYAOI\JOB", d) for d in os.listdir(r"D:\EYAOI\JOB")], key=os.path.getmtime)
    time_difference = time.time() - os.path.getmtime(latest_folder)
    logger.info(f"保存时间差距: {time_difference} 秒")
    if time_difference > 60:
        raise Exception("非当前保存时间")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def jbgn_001_12():
    # 1、打开AOI软件，点击左上角【打开程式】按钮
    utils.check_and_launch_aoi()
    # 2、在弹窗中的【程式主目录】，选择程式的目录：任意选择一个JOB
    # 3、点击【是】按钮
    utils.open_program()
    # 4、点击左上角【save As To Job File】
    utils.click_by_png(config.SAVE_AS_JOB)
    time.sleep(1)
    if os.path.exists(r"D:\EYAOI\JOB\save_test"):
        shutil.rmtree(r"D:\EYAOI\JOB\save_test")
    # 5、选择文件夹并重新命名程式名称后点击【是】
    utils.write_text((815,480),"D:\EYAOI\JOB")
    utils.write_text((815,540),"save_test")
    utils.click_by_png(config.YES)
    while utils.search_symbol(config.SAVING_PROGRAM):
        time.sleep(3)
    if not os.path.exists(r"D:\EYAOI\JOB\save_test"):
        raise Exception("未发现另存为的程式名")
    utils.close_aoi()
# @utils.screenshot_error_to_excel()
# def jbgn_001_13():
#     # 1、点击左上角【运行】按钮
#     utils.click_by_png(config.RUN)
#     # 2、点击【是】按钮
#     pyautogui.press("enter")
#     # 3、检查FOV，元件数
#     utils.check_fov_and_component_count()
#     # 4、检测过程，观察界面右上角【测试状态】--【FOVs】和【元件】的进度条
#     utils.observe_test_status()
#     # 5、检查【BarCode】条码信息
#     utils.check_barcode_info()
#     # 6、检查整板2个Mark点检测状态
#     utils.check_mark_points()

# @utils.screenshot_error_to_excel()
# def jbgn_001_14():
#     # 1、检查FOV拍照时间，通过查看日志D:\EYAOI\Logger\Lane_0\AlgThreadTimeStats_XX.log（XX--代表当前日期）字段End Cap FOV的值
#     utils.check_fov_photo_time()
#     # 2、检查元件计算时间(取第2次运行的时间)，通过查看日志AlgThreadTimeStats_XX.log中字段Total(BIn/ThdS)值
#     utils.check_component_calculation_time()
#     # 3、检查导出数据时间，通过日志D:\EYAOI\Logger\IL\StateLog\UI\L1\UI-L1-STATE-XX.log（XX-代表测试日期）查看字段【开始二次导出数据】、【计算完成】的时间
#     utils.check_data_export_time()

# @utils.screenshot_error_to_excel()
# def jbgn_001_15():
#     # 1、程式运行结束后，打开RV界面
#     utils.open_rv_interface()
#     # 2、双击该条数据，检查RV界面右上角【条码】中的内容
#     utils.check_rv_barcode_content()
#     # 3、检查【元件列表】，不选【全部】筛选条件时，【全部】数量
#     utils.check_component_list_without_filter()
#     # 4、检查【元件列表】，选中【全部】筛选条件时，【全部】数量
#     utils.check_component_list_with_filter()
#     # 5、【元件列表】是否存在特殊元件
#     utils.check_special_components()

# @utils.screenshot_error_to_excel()
# def jbgn_001_16():
#     # 1、检查RV中每个元件的3D图显示
#     utils.check_rv_3d_images()
#     # 2、无3D图的元件，在该元件【不良窗口】筛选【全部】，检查是否无3D算法
#     utils.check_no_3d_algorithm()
#     # 3、无3D图的元件，返回UI，点击【停止】--【进入细调界面】，查看该元件算法是否启用【3D模式】
#     utils.check_3d_mode_in_ui()
#     # 4、RV中元件的3D图存在凹陷、不平滑等异常现象，返回UI，点击【停止】--【进入细调界面】，对比该元件的3D图
#     utils.compare_3d_images()
#     # 5、检查每个元件的所有不良窗口在【缺陷组件】图中的算法结果
#     utils.check_defect_component_algorithm_results()
#     # 6、检查每个元件【标准图像】、【缺陷组件】、【3D图像】是否一致，【Board View】和【FOV View】显示的元件位置一致
#     utils.check_image_consistency()

# @utils.screenshot_error_to_excel()
# def jbgn_001_17():
#     # 1、在RV判定元件的检测结果，选择【通过】或【不良】后，【确认】。注：保证【通过】、【不良】二种数据都要选
#     utils.judge_rv_component_results()

# @utils.screenshot_error_to_excel()
# def jbgn_001_18():
#     # 1、打开SPC软件，点击程序视图，在查询条件选择【1小时】后，点击【查询】
#     utils.open_spc_and_query()
#     # 2、在搜索结果中找到对应的Job，双击进入【明细】页面，检查列表中最新1条记录每列的数据
#     utils.check_spc_details()
#     # 3、双击该记录进入PCB明细页面，分别筛选【不良】、【通过】、【良好】条件，在筛选结果列表中抽测3-5个元件的【标准图像】、【不良图像】、【3D图像】、【整板图像】、【FOV View】、【窗口数据】
#     utils.check_pcb_details()

# @utils.screenshot_error_to_excel()
# def jbgn_001_19():
#     # 1、在UI界面右侧【良率视图】分别选择【板】、【拼板】、【元件】查看数据是否有变化
#     utils.check_yield_view()

# @utils.screenshot_error_to_excel()
# def jbgn_001_20():
#     # 1、检查料号47UF_6.3*7.7mm在【元器件编辑】界面的显示
#     utils.check_component_display()
#     # 2、检查料号47UF_6.3*7.7mm在RV的缺陷组件图、3D图
#     utils.check_defect_and_3d_images()

# @utils.screenshot_error_to_excel()
# def jbgn_001_21():
#     # 1、检查元件LVC1在【元器件编辑】界面是否显示抽测元件
#     utils.check_sampled_component_display()
#     # 2、【运行】程式3次，每次运行停止后，检查元件LVC1在UI运行界面上的检测标识
#     utils.run_program_and_check_component()
#     # 3、检查最近的3条RV记录
#     utils.check_recent_rv_records()

# @utils.screenshot_error_to_excel()
# def jbgn_001_22():
#     # 1、检查元件epcos1、epcos2在【元器件编辑】界面显示【抽测元件】
#     utils.check_sampled_components_display()
#     # 2、检查元件epcos1、epcos2在【元器件编辑】界面中【颜色匹配】的窗口标题
#     utils.check_color_matching_titles()
#     # 3、运行程式3次，检查元件epcos1、epcos2在最近3条RV数据中的窗口
#     utils.run_program_and_check_rv_windows()

# @utils.screenshot_error_to_excel()
# def jbgn_001_23():
#     # 1、检查元件G6K-2F-Y(J3,J2)在【元器件编辑】界面的显示
#     utils.check_component_display_g6k()
#     # 2、打开机台查看FOV拍照过程，检查相机是否有升高拍照
#     utils.check_camera_elevation()

# @utils.screenshot_error_to_excel()
# def jbgn_001_24():
#     # 1、检查料号7343TAN-100uf在【元器件编辑】界面的显示
#     utils.check_component_display_7343tan()
#     # 2、检查RV【元件列表】中
#     utils.check_rv_component_list()

# @utils.screenshot_error_to_excel()
# def jbgn_001_25():
#     # 1、手动设置UI：参数配置--演算法配置--输出调试数据：选择【保存DJB文件】、一片最多【0】、最大数量【500】、有效期至【...】(选择晚于测试日期）
#     utils.set_ui_save_djb()
#     # 2、运行程式后，查看地D:\EYUI\BIN\DebugDBJFileExport\XX目录(XX代表运行时间)
#     utils.run_program_and_check_djb()

# @utils.screenshot_error_to_excel()
# def jbgn_001_26():
#     # 1、在料号R6322-2512-470E的【元件器编辑】界面，修改【方形定位】窗口参数X偏移的值，修改的值超出100-500范围
#     utils.modify_square_positioning_x_offset()

# @utils.screenshot_error_to_excel()
# def jbgn_001_27():
#     # 1、设置UI：参数配置--演算法配置--强制操作：选择【定位元件不良继续矫正】；
#     utils.set_ui_force_operation()
#     # 2、整体轻微移动元件Designator3、R60、R58、R56、R54的位置，运行程式后，查看元件R60 R58 R56 R54在RV的检测结果
#     utils.move_components_and_check_rv()
#     # 3、设置UI：参数配置--演算法配置--强制操作：不选【定位元件不良继续矫正】；
#     utils.unset_ui_force_operation()
#     # 4、整体轻微移动元件Designator3、R60、R58、R56、R54的位置，运行程式后，查看元件R60 R58 R56 R54在RV的检测结果
#     utils.move_components_and_check_rv_again()

# @utils.screenshot_error_to_excel()
# def jbgn_001_28():
#     # 1、在RV检查大元件con1的不同角度的3D图形
#     utils.check_large_component_3d_images()

# @utils.screenshot_error_to_excel()
# def jbgn_001_29():
#     # 1、在UI整板信息【量测】Tab页检查是否选择【123】
#     utils.check_measurement_tab()
#     # 2、在RV【元件列表】检查是否存在元件【123】
#     utils.check_rv_component_list_123()

# @utils.screenshot_error_to_excel()
# def jbgn_001_30():
#     # 1、检查UI整板信息是否存在【整板异物】Tab页
#     utils.check_board_anomaly_tab()
#     # 2、检查RV【元件列表】是否存在元件BoardAnomaly(异物)
#     utils.check_rv_board_anomaly()

# @utils.screenshot_error_to_excel()
# def jbgn_001_31():
#     # 1、检查RV【元件列表】是否存在BoardDiscret元件
#     utils.check_rv_board_discret()
#     # 2、对比RV右上角显示BoardView【总数高】的值与UI【整板离散度】Tab页中【总数高】的值
#     utils.compare_board_discret_values()

# @utils.screenshot_error_to_excel()
# def jbgn_001_32():
#     # 1、点击左上角【运行】按钮
#     utils.click_by_png(config.RUN)
#     # 2、点击【是】按钮
#     pyautogui.press("enter")
#     # 3、检查【BarCode】条码信息
#     utils.check_barcode_info()
#     # 4、检查整板2个Mark点检测状态
#     utils.check_mark_points()

# @utils.screenshot_error_to_excel()
# def jbgn_001_33():
#     # 1、检查RV右上角【Job信息】中的条码
#     utils.check_rv_job_barcode()
#     # 2、检查RV的Borard View界面信息
#     utils.check_rv_board_view()
#     # 3、在RV【元件列表】筛选【全部】条件，检查列表中【全部】的个数
#     utils.check_rv_component_list_all()
#     # 4、在【元件列表】选择不同拼板的元件
#     utils.check_rv_different_panels()

# @utils.screenshot_error_to_excel()
# def jbgn_001_34():
#     # 1、打开SPC软件，点击程序视图，在查询条件选择【1小时】后，点击【查询】
#     utils.open_spc_and_query()
#     # 2、在搜索结果中找到对应的Job，双击进入【明细】页面，检查列表中最新1条记录每列的数据
#     utils.check_spc_details()
#     # 3、打开SPC软件，找到记录进入PCB明细页面，选择【不良】、【通过】、【良好】筛选条件，检查列表中的元件
#     utils.check_pcb_details()
#     # 4、检查【整板图像】的元件检测标识
#     utils.check_board_image_component_marks()

# @utils.screenshot_error_to_excel()
# def jbgn_001_35():
#     # 检查良率视图：
#     # 1、【板】数据
#     utils.check_yield_view_board()
#     # 2、【拼板】数据
#     utils.check_yield_view_panel()
#     # 3、【元件】数据
#     utils.check_yield_view_component()

# @utils.screenshot_error_to_excel()
# def jbgn_001_36():
#     # 1、点击左上角【运行】按钮
#     utils.click_by_png(config.RUN)
#     # 2、点击【是】按钮
#     pyautogui.press("enter")
#     # 3、检查【BarCode】条码信息
#     utils.check_barcode_info()
#     # 4、检查整板4个Mark点检测状态
#     utils.check_mark_points_4()

# @utils.screenshot_error_to_excel()
# def jbgn_001_37():
#     # 1、检查RV右上角【Job信息】中的条码
#     utils.check_rv_job_barcode()
#     # 2、检查RV的Borard View界面信息
#     utils.check_rv_board_view()
#     # 3、在RV【元件列表】筛选【全部】条件，检查列表中【全部】的个数
#     utils.check_rv_component_list_all()

# @utils.screenshot_error_to_excel()
# def jbgn_001_38():
#     # 1、打开SPC软件，找到记录进入PCB明细页面，选择【不良】、【通过】、【良好】筛选条件，检查列表中的元件
#     utils.check_spc_pcb_details()
#     # 2、检查【整板图像】的元件检测标识
#     utils.check_board_image_component_marks()

# @utils.screenshot_error_to_excel()
# def jbgn_001_39():
#     # 检查良率视图：
#     # 1、【板】数据
#     utils.check_yield_view_board()
#     # 2、【拼板】数据
#     utils.check_yield_view_panel()
#     # 3、【元件】数据
#     utils.check_yield_view_component()

@utils.screenshot_error_to_excel()
def jbgn_001_40():
    utils.check_and_launch_aoi()
    utils.check_all_algs()
    utils.open_program()
    utils.click_by_png(config.PROGRAM_COMPONENT_DARK)
    utils.is_checked((66,255),(78,267),True)
    utils.click_by_png(config.PLAY)
    for _ in range (2):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,20)
    while utils.search_symbol(config.TESTING_INTERFACE_CIRCLE_1,tolerance=0.95):
        time.sleep(3)
    utils.click_by_png(config.STOP)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_STOP)
    utils.click_by_png(config.TESTING_INTERFACE_ENTER_DETAIL_INTERFACE)
    time.sleep(5)
    # 1、点击【进入细调界面】，在【元件窗口】选择所有红色NG的窗口，查看算法参数值
    utils.click_by_png(config.NO_PASS_COMPONENT,2)
    utils.click_color(1,config.COMPONENT_WINDOW_REGION,(255,0,0))
    time.sleep(5)
    # 2、点击【测试当前窗口】按钮，查看算法参数值，对比点击【测试当前窗口】前的算法参数值
    screen_before = pyautogui.screenshot(region=config.ALG_PARAM_REGION)
    utils.click_by_png(config.TEST_WINDOW)
    time.sleep(5)
    screen_later = pyautogui.screenshot(region=config.ALG_PARAM_REGION)
    if screen_before != screen_later:
        raise Exception("算法参数值发生变化")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def jbgn_001_41():
    utils.check_and_launch_aoi()
    utils.check_all_algs()
    utils.open_program()
    utils.click_by_png(config.PROGRAM_COMPONENT_DARK)
    utils.is_checked((66,255),(78,267),True)
    utils.click_by_png(config.PLAY)
    for _ in range (2):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,20)
    while utils.search_symbol(config.TESTING_INTERFACE_CIRCLE_1,tolerance=0.95):
        time.sleep(3)
    utils.click_by_png(config.STOP)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_STOP)
    utils.click_by_png(config.TESTING_INTERFACE_ENTER_DETAIL_INTERFACE)
    time.sleep(5)
    # 1、点击【进入细调界面】，在【不良元件】Tab页，快速点击不同料号、位号的元件（包括大元件）
    start_time = datetime.datetime.now()
    while (datetime.datetime.now() - start_time).seconds < 600:
        ng_components = []  # 初始化为一个空列表
        try:
            ng_components = list(pyautogui.locateAllOnScreen(config.NO_PASS_COMPONENT, confidence=0.9, region=config.BOARD_COMPONENTS_REGION))
        except Exception as e:
            logger.error(f"该页未找到不良元件，继续下滚: {e}")
        for ng_component in ng_components:
            reference = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
            pyautogui.doubleClick(ng_component)
            for _ in range(10):
                time.sleep(0.1)
                current_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
                if current_screenshot != reference:
                    reference = current_screenshot
                    break
                else:
                    continue
        for _ in range(7):
            utils.scroll_down((200, 380), config.BOARD_COMPONENTS_REGION, "-100")
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def jbgn_001_42():
    utils.check_and_launch_aoi()
    utils.check_all_algs()
    utils.open_program()
    utils.click_by_png(config.PROGRAM_COMPONENT_DARK)
    utils.is_checked((66,255),(78,267),True)
    utils.click_by_png(config.PLAY)
    for _ in range (2):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,20)
    while utils.search_symbol(config.TESTING_INTERFACE_CIRCLE_1,tolerance=0.95):
        time.sleep(3)
    utils.click_by_png(config.STOP)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_STOP)
    utils.click_by_png(config.TESTING_INTERFACE_ENTER_DETAIL_INTERFACE)
    time.sleep(5)
    # 1、点击【进入细调界面】，在【元件窗口】中选择含有搜索范围的算法，如：方形定位
    utils.click_by_png(config.NO_PASS_COMPONENT,2)
    time.sleep(3)
    utils.add_window()
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    time.sleep(7)
    # 看下3d图啥样
    utils.click_by_png(config.COMPONENT_3D_IMAGE)
    time.sleep(3)
    before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    utils.click_by_png(config.COMPONENT_3D_IMAGE)
    # 2、点击【搜索范围】按钮，在界面上设定元件不同的搜索范围
    utils.click_by_png(config.SEARCH_RANGE)
    utils.add_window(None)
    time.sleep(3)
    # 3、点击【元件3D图】，查看3D图的变化
    utils.click_by_png(config.COMPONENT_3D_IMAGE)
    after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if before_screenshot == after_screenshot:
        raise Exception("3D图未发生变化")

@utils.screenshot_error_to_excel()
def jbgn_001_43():
    utils.check_and_launch_aoi()
    utils.check_all_algs()
    utils.open_program()
    utils.click_by_png(config.PROGRAM_COMPONENT_DARK)
    utils.is_checked((66,255),(78,267),True)
    utils.click_by_png(config.PLAY)
    for _ in range (2):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,20)
    while utils.search_symbol(config.TESTING_INTERFACE_CIRCLE_1,tolerance=0.95):
        time.sleep(3)
    utils.click_by_png(config.STOP)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_STOP)
    utils.click_by_png(config.TESTING_INTERFACE_ENTER_DETAIL_INTERFACE)
    time.sleep(5)
    # 1、点击【进入细调界面】，在【元件窗口】中选择含有搜索范围的算法，如：方形定位
    utils.click_by_png(config.NO_PASS_COMPONENT,2)
    time.sleep(3)
    utils.add_window()
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    time.sleep(7)
    # 看下3d图啥样
    utils.click_by_png(config.COMPONENT_3D_IMAGE)
    time.sleep(3)
    before_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    utils.click_by_png(config.COMPONENT_3D_IMAGE)
    # 2、将算法的检测框拉大、缩小，点击【元件3D图】
    utils.expand_choose_box()
    time.sleep(3)
    utils.click_by_png(config.COMPONENT_3D_IMAGE)
    after_screenshot = pyautogui.screenshot(region=config.COMPONENT_OPERATION_REGION)
    if before_screenshot == after_screenshot:
        raise Exception("3D图未发生变化")

@utils.screenshot_error_to_excel()
def jbgn_001_44():
    utils.check_and_launch_aoi()
    utils.check_all_algs()
    utils.open_program()
    utils.click_by_png(config.PROGRAM_COMPONENT_DARK)
    utils.is_checked((66,255),(78,267),True)
    # 1、点击【运行】按钮，【运行】按钮置灰进入检测状态
    utils.click_by_png(config.PLAY)
    for _ in range (2):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,20)
    # 2、点击【停止】按钮，查看UI界面在1秒内显示的状态
    utils.click_by_png(config.STOP)
    if not utils.search_symbol(config.TESTING_INTERFACE_STOP,1,config.ALG_PARAM_REGION,tolerance=0.75):
        raise Exception("未识别到停止，疑似UI界面在1秒内未显示【停止】状态")

@utils.screenshot_error_to_excel()
def jbgn_001_45():
    utils.check_and_launch_aoi()
    utils.check_all_algs()
    utils.open_program()
    utils.click_by_png(config.PROGRAM_COMPONENT_DARK)
    utils.is_checked((66,255),(78,267),True)
    # 1、点击【运行】按钮，查看运行各阶段的界面显示状态与实际轨道上板的位置
    utils.click_by_png(config.PLAY)
    for _ in range (2):
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
    utils.search_symbol_erroring(config.TESTING_INTERFACE_INFORMATION,20)
    # 2、至少循环测试20片
    utils.search_symbol_erroring(config.TESTING_INTERFACE_CIRCLE_20,1200)

# @utils.screenshot_error_to_excel()
# def jbgn_001_46():
#     # 1、点击【运行】按钮，运行完成后
#     utils.click_run_and_complete()
#     # 2、RV在【未复判】列表中双击准备复判的数据，然后点击【全部通过】--【确认】进行复判
#     utils.review_and_confirm()
#     # 3、在SPC点击【程序视图】--【1小时】--【查询】，在搜索结果中选择相应的数据， 点击【PCB视图】
#     utils.query_spc_and_check_pcb_view()

# @utils.screenshot_error_to_excel()
# def jbgn_001_47():
#     # 1、点击【运行】按钮，运行完成后
#     utils.click_run_and_complete()
#     # 2、在DV界面，点击【全部通过】--【确认完成】按钮
#     utils.confirm_in_dv()
#     # 3、在SPC点击【程序视图】--【1小时】--【查询】，在搜索结果中选择相应的数据， 点击【PCB视图】
#     utils.query_spc_and_check_pcb_view()
# @utils.screenshot_error_to_excel()
# def jbgn_001_48():
#     # 1、点击【运行】按钮，运行完成后
#     utils.click_run_and_complete()
#     # 2、在SPC点击【程序视图】--【1小时】--【查询】，在搜索结果中选择相应的数据， 点击【PCB视图】
#     utils.query_spc_and_check_pcb_view()

# @utils.screenshot_error_to_excel()
# def jbgn_001_49():
#     # 1、在元器件编辑界面，右击--【导出所有元件OK图】
#     utils.export_all_ok_images()
#     # 2、在RV检查所有元件的标准图
#     utils.check_standard_images_in_rv()

# @utils.screenshot_error_to_excel()
# def jbgn_001_50():
#     # 1、接案例JBGN-001-01，做好job并矫正
#     utils.prepare_job_and_correct()
#     # 2、选择任一元件，双击进入离线编辑界面
#     utils.double_click_component_to_offline_edit()
#     # 3、修改任一算法参数，切换到同料号其它元件，弹框选择【是】
#     utils.modify_algorithm_and_switch_component(confirm=True)
#     # 4、调整任一算法窗口，切换到同料号其它元件，弹框选择【是】
#     utils.adjust_algorithm_window_and_switch_component(confirm=True)

# @utils.screenshot_error_to_excel()
# def jbgn_001_51():
#     # 1、接案例JBGN-001-01，做好job并矫正
#     utils.prepare_job_and_correct()
#     # 2、点【测试】按钮开始测试，测试完成后，点【停止】按钮，点击右下角【进入细调界面】
#     utils.click_test_and_enter_fine_tuning()
#     # 3、选择任一元件，修改任一算法参数，切换到同料号其它元件，弹框选择【是】
#     utils.modify_algorithm_and_switch_component(confirm=True)
#     # 4、调整任一算法窗口，切换到同料号其它元件，弹框选择【是】
#     utils.adjust_algorithm_window_and_switch_component(confirm=True)

# # @utils.screenshot_error_to_excel()
# # def jbgn_001_52():
# #     # 1.打开这个名为量测的job
# #     utils.open_job_named_measurement()
# #     # 2.检查板--整板信息--量测-点对点量测是否为勾上状态
# #     utils.check_point_to_point_measurement()
# #     # 3.点击左上角运行
# #     utils.click_run()

@utils.screenshot_error_to_excel()
def jbgn_001_53():
    utils.check_and_launch_aoi()
    utils.check_open_developer_options(type="save_3d_data_yes")
    # 任意打开一个job进入元件查看3D图
    utils.ensure_in_edit_mode()
    # 删除D:\EYAOI\BIN\Debug下后缀为.dat的文件（如果存在的话）
    debug_dir = r"D:\EYAOI\BIN\Debug"
    for file_name in os.listdir(debug_dir):
        if file_name.endswith(".dat"):
            file_path = os.path.join(debug_dir, file_name)
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"已删除文件: {file_path}")
    utils.click_by_png(config.COMPONENT_3D_IMAGE)
    if not utils.search_symbol(config.TESTING_INTERFACE_INFORMATION):
        raise Exception("未能进入测试板界面")
    # 检测debug_dir下是否有新的.dat文件生成
    new_dat_files = [file for file in os.listdir(debug_dir) if file.endswith(".dat")]
    if not new_dat_files:
        raise Exception("在D:\EYAOI\BIN\Debug下未生成.dat文件")
    else:
        logger.info(f"生成的.dat文件: {new_dat_files}")
    utils.close_aoi()
@utils.screenshot_error_to_excel()
def jbgn_001_54():
    utils.check_and_launch_aoi()
    utils.check_open_developer_options(type="save_check_data_yes")
    utils.open_program()
    # 任意测试一个job
    debug_dir = r"D:\EYAOI\BIN\Debug"
    for file_name in os.listdir(debug_dir):
        if file_name.endswith(".dat"):
            file_path = os.path.join(debug_dir, file_name)
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"已删除文件: {file_path}")
    utils.is_checked((66,255),(78,267),True)
    utils.click_by_png(config.PLAY)
    for _ in range(2):
        if utils.search_symbol(config.QUESTION_MARK):
            pyautogui.press("enter")
            time.sleep(3)
    if not utils.search_symbol(config.TESTING_INTERFACE_INFORMATION):
        raise Exception("未能进入测试板界面")
    # 检测debug_dir下是否有新的.insp文件生成
    new_insp_files = [file for file in os.listdir(debug_dir) if file.endswith(".insp")]
    if not new_insp_files:
        raise Exception("在D:\EYAOI\BIN\Debug下未生成.dat文件")
    else:
        logger.info(f"生成的.insp文件: {new_insp_files}")

    utils.close_aoi()

@utils.screenshot_error_to_excel()
def jbgn_001_55():
    utils.check_and_launch_aoi()
    # 任意在线测试一个JOB
    utils.check_save_djb(True)
    utils.open_program()
    utils.is_checked((66,255),(78,267),True)
    utils.click_by_png(config.PLAY)
    for _ in range(2):
        if utils.search_symbol(config.QUESTION_MARK):
            pyautogui.press("enter")
            time.sleep(3)
    if not utils.search_symbol(config.TESTING_INTERFACE_INFORMATION):
        raise Exception("未能进入测试板界面")
    debug_djb_dir = r"D:\EYAOI\BIN\DebugDBJFileExport"
    current_time = time.time()
    new_djb_files = [file for file in os.listdir(debug_djb_dir) if file.endswith(".djb") and (current_time - os.path.getmtime(os.path.join(debug_djb_dir, file))) < 180]
    if not new_djb_files:
        raise Exception("三分钟内无.djb文件生成")
    else:
        latest_djb_file = max(new_djb_files, key=lambda file: os.path.getmtime(os.path.join(debug_djb_dir, file)))
        latest_djb_time = os.path.getmtime(os.path.join(debug_djb_dir, latest_djb_file))
        logger.info(f"最近生成的.djb文件: {latest_djb_file}, 生成时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(latest_djb_time))}")

    utils.close_aoi()

@utils.screenshot_error_to_excel()
def jbgn_001_56():
    utils.check_and_launch_aoi()
    # 任意测试一个job
    utils.check_all_algs()
    utils.open_program()
    utils.is_checked((66,255),(78,267),True)
    utils.click_by_png(config.PLAY)
    for _ in range(2):
        if utils.search_symbol(config.QUESTION_MARK):
            pyautogui.press("enter")
            time.sleep(3)
    if not utils.search_symbol(config.TESTING_INTERFACE_INFORMATION, 20):
        raise Exception("未能进入测试板界面")
    # 测试结果良好
    if not utils.search_symbol(config.TESTING_INTERFACE_GOOD, 20):
        raise Exception("未检测到：良好")

@utils.screenshot_error_to_excel()
def jbgn_001_57():
    utils.check_and_launch_aoi() 
    utils.check_all_algs()
    utils.open_program()   
    # 测试一个忽略板
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.ADD_OBJECT)
    utils.click_by_png(config.BAD_BOARD_MARK)
    time.sleep(3)
    utils.add_window()
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(3)
    utils.write_text((825,950),"0")
    utils.write_text((825,975),"0")
    pyautogui.press("enter")
    time.sleep(3)
    if not utils.check_color_in_region((255,0,0),region=config.CHECK_RESULT_REGION):
        raise Exception("标记坏板失败：调整调色板后未检测到坏板结果")
    utils.click_by_png(config.PLAY)
    for _ in range(5):
        if utils.search_symbol(config.QUESTION_MARK):
            pyautogui.press("enter")
    if not utils.search_symbol(config.TESTING_INTERFACE_INFORMATION):
        raise Exception("未能进入测试板界面")
    if not utils.search_symbol(config.TESTING_INTERFACE_IGNORE):
        raise Exception("未检测到结果：忽略")
    # TODO 没写完
    utils.check_and_launch_spc()



    utils.close_aoi()

# @utils.screenshot_error_to_excel()
# def jbgn_001_58():  
#     utils.check_and_launch_aoi()
#     # 1.打开任意一个job，运行测试
#     utils.open_any_job_and_run_test()
#     # 2.计算完成后--查看rv
#     utils.check_rv_after_calculation()
#     # 3.按快捷键进行复判--提交
#     utils.review_and_submit_with_shortcut()
#     utils.close_aoi()
