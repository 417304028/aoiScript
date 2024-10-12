import os
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
    # 1、打开AOI软件，软件点击左上角【打开程式】按钮
    utils.check_and_launch_aoi()
    utils.click_by_png(config.OPEN_PROGRAM)
    # 2、在弹窗中的【程式主目录】，选择程式的目录或输入程式目录，例：D:\EYAOI\JOB，回车
    directory = r"D:\EYAOI\JOB"
    utils.write_text((660,195),directory)
    pyautogui.press("enter")
    # 3、在【程式列表】--【主目录程式】，双击任一准备测试的程式
    symbols = [config.OPEN_PROGRAM_PLUS, config.OPEN_PROGRAM_CURSOR]
    found = False
    for symbol in symbols:
        if utils.search_symbol(symbol, 3):
            utils.click_by_png(symbol, 2)
            utils.search_symbol_erroring(symbol, 3,region=config.SELECTED_PROGRAM_REGION)
            found = True
            break
    if not found:
        raise Exception("找不到程式")

    # 4、点击【取消】按钮
    utils.click_by_png(config.CANCEL)
    time.sleep(1)
    if utils.search_symbol(config.OPEN_PROGRAM_TOPIC):
        raise Exception("关闭打开程式弹窗失败")
    utils.search_symbol_erroring(config.AOI_TOPIC, 3)
    utils.close_aoi()
    time.sleep(5)
    # 5、重复步骤1-3，点击【是】按钮
    utils.check_and_launch_aoi()
    utils.click_by_png(config.OPEN_PROGRAM)
    directory = r"D:\EYAOI\JOB"
    utils.write_text((660,195),directory)  
    pyautogui.press("enter")
    symbols = [config.OPEN_PROGRAM_PLUS, config.OPEN_PROGRAM_CURSOR]
    found = False
    for symbol in symbols:
        if utils.search_symbol(symbol, 3):
            utils.click_by_png(symbol, 2)
            found = True
            break
    if not found:
        raise Exception("找不到程式")
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
def jbgn_001_05():
    # 1、打开AOI软件，点击左上角【打开程式】按钮
    utils.check_and_launch_aoi()
    utils.click_by_png(config.OPEN_PROGRAM)
    # 2、在弹窗中的【程式主目录】，选择程式的目录或输入程式目录，例：D:\EYAOI\JOB，回车
    directory = r"D:\EYAOI\JOB"
    utils.write_text((660,195),directory)
    pyautogui.press("enter")

    program_count = 0
    for symbol in symbols:
        try:
            program_count += len(list(pyautogui.locateAllOnScreen(symbol, region=config.SELECTED_PROGRAM_REGION)))
        except pyautogui.ImageNotFoundException:
            continue

    if program_count == 0:
        raise Exception("未发现任何程式")
    # 计算D:\EYAOI\JOB内文件夹个数
    directory = r"D:\EYAOI\JOB"
    folder_count = len([name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))])

    # 比较数量是否相同
    if program_count != folder_count:
        raise Exception("未能显示目录下所有程式")

    # 3、在【程式列表】--【主目录程式】，选中任一程式(压缩的程式图标变成带有箭头)，点击【轨1】（如果是双轨机台在轨2打开，显示【轨2】）
    symbols = [config.OPEN_PROGRAM_PLUS, config.OPEN_PROGRAM_CURSOR]
    found = False
    for symbol in symbols:
        if utils.search_symbol(symbol, 3):
            utils.click_by_png(symbol, 2)
            utils.search_symbol_erroring(symbol, 3,region=config.SELECTED_PROGRAM_REGION)
            found = True
            break
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
    utils.click_by_png(config.OPEN_PROGRAM)
    # 2、在弹窗中的【程式主目录】，选择程式的目录或输入程式目录，例：D:\EYAOI\JOB，回车
    directory = r"D:\EYAOI\JOB"
    utils.write_text((660,195),directory)
    pyautogui.press("enter")
    # 3、在【程式列表】--【主目录程式】，选中某一程式，点击【轨1】（如果是双轨机台在轨2打开，显示【轨2】）。按此操作，多次选择不同程式。
    # 先识别总共有多少个程式
    symbols = [config.OPEN_PROGRAM_PLUS, config.OPEN_PROGRAM_CURSOR]
    initial_count = 0
    for symbol in symbols:
        try:
            initial_count += len(list(pyautogui.locateAllOnScreen(symbol, region=config.SELECTED_PROGRAM_REGION)))
        except pyautogui.ImageNotFoundException:
            continue
    if initial_count == 0:
        raise Exception("未发现任何程式")
    # 一个个去点加载
    for symbol in symbols:
        try:
            locations = list(pyautogui.locateAllOnScreen(symbol, region=config.SELECTED_PROGRAM_REGION))
            for location in locations:
                utils.click_by_png(symbol)
                utils.click_by_png(config.OPEN_PROGRAM_LOAD_1)
                time.sleep(1)
        except pyautogui.ImageNotFoundException:
            continue

    final_count = 0
    for symbol in symbols:
        final_count += len(list(pyautogui.locateAllOnScreen(symbol, region=config.SELECTED_PROGRAM_REGION)))
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
    utils.click_by_png(config.OPEN_PROGRAM)
    # 2、在弹窗中的【程式主目录】，选择程式的目录或输入程式目录，例：D:\EYAOI\JOB，回车
    directory = r"D:\EYAOI\JOB"
    utils.write_text((660,195),directory)
    pyautogui.press("enter")
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
# def jbgn_001_08():
#     pass
# def jbgn_001_09():
#     pass
# def jbgn_001_10():
#     pass
@utils.screenshot_error_to_excel()
def jbgn_001_11():
    # 1、打开AOI软件，点击左上角【打开程式】按钮
    utils.check_and_launch_aoi()
    # 2、在弹窗中的【程式主目录】，选择程式的目录：任意选择一个JOB
    # 3、点击【是】按钮
    utils.open_program()
    # 4、点击左上角【save to Job File】
    utils.click_by_png(config.SAVE_AS_JOB)
    time.sleep(1)
    pyautogui.press("enter")
    while utils.search_symbol(config.SAVING_PROGRAM):
        time.sleep(3)
    latest_folder = max([os.path.join(r"D:\EYAOI\JOB", d) for d in os.listdir(r"D:\EYAOI\JOB")], key=os.path.getmtime)
    if time.time() - os.path.getmtime(latest_folder) > 60:
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
    # 5、选择文件夹并重新命名程式名称后点击【是】
    utils.write_text((815,480),"save_test")
    utils.click_by_png(config.YES)

    while utils.search_symbol(config.SAVING_PROGRAM):
        time.sleep(3)
    if not os.path.exists(r"D:\EYAOI\JOB\save_test"):
        raise Exception("未发现另存为的程式名")
    utils.close_aoi()
# def jbgn_001_13():
#     pass
# def jbgn_001_14():
#     pass
# def jbgn_001_15():
#     pass
# def jbgn_001_16():
#     pass
# def jbgn_001_17():
#     pass
# def jbgn_001_18():
#     pass
# def jbgn_001_19():
#     pass
# def jbgn_001_20():
#     pass
# def jbgn_001_21():
#     pass
# def jbgn_001_22():
#     pass
# def jbgn_001_23():
#     pass
# def jbgn_001_24():
#     pass
# def jbgn_001_25():
#     pass
# # 参数控制限定
# def jbgn_001_26():
#     pass
# # 定位元件
# def jbgn_001_27():
#     pass
# # 大元件测试
# def jbgn_001_28():
#     pass
# # 整板量测
# def jbgn_001_29():
#     pass
# # 整板异物检测
# def jbgn_001_30():
    
#     pass
# # 整板离散度
# def jbgn_001_31():
#     pass
# # 运行坏板程式
# def jbgn_001_32():
#     pass
# # 坏板RV信息
# def jbgn_001_33():

#     pass
# # 坏板SPC信息
# def jbgn_001_34():

#     pass
# # 坏板良率信息
# def jbgn_001_35():


#     pass
# # 运行坏板程式
# def jbgn_001_36():
#     pass
# # 坏板RV信息
# def jbgn_001_37():
#     pass
# # 坏板SPC信息
# def jbgn_001_38():
#     pass
# # 坏板良率信息
# def jbgn_001_39():


#     pass
# # 检查细调算法
def jbgn_001_40():
    pass
# 细调元件切换
def jbgn_001_41():
    pass
# 搜索范围变化
def jbgn_001_42():
    pass
# 调整检测框
def jbgn_001_43():
    pass
# 停止响应
def jbgn_001_44():
    pass
# 状态稳定性
def jbgn_001_45():
    pass
# SPC数据保存
def jbgn_001_46():
    pass
# SPC数据保存
def jbgn_001_47():
    pass
# SPC数据保存
def jbgn_001_48():
    # 1、参数配置--硬件设置--流程配置--缺陷视图:勾选【DV自动确认】
    # 2、RV：手工确认
    pass
# 导出所有ok图
def jbgn_001_49():
    # 1、UI：参数配置--UI配置-程序设置：选择【导出所有元件OK图】
    # 2、删除目录D:\EYAOI\JOB\Job名\Job名.oki
    # 3、删除目录F:\DataExport\Job名\OKImage
    pass
# # 离线调整参数
# def jbgn_001_50():
#     #1、接案例JBGN-001-01，做好job并矫正
#     #2、选择任一元件，双金进入离线编辑界面
#     # 3、修改任一算法参数，切换到同料号其它元件，弹框选择【是】 参数已修改，窗口位置不会变
#     # 4、调整任一算法窗口，切换到同料号其它元件，弹框选择【是】 窗口位置已修改，其它窗口位置不会变
#     pass

# # 细调调整参数
# def jbgn_001_51():
#     # 1、接案例JBGN-001-01，做好job并矫正
#     # 2、点【测试】按钮开始测试，测试完成后，点【停止】按钮，点击右下角【进入细调界面】
#     # 3、选择任一元件，修改任一算法参数，切换到同料号其它元件，弹框选择【是】   参数已修改，窗口位置不会变

#     # 4、调整任一算法窗口，切换到同料号其它元件，弹框选择【是】     窗口位置已修改，其它窗口位置不会变
#     pass

# # 量测测试
# def jbgn_001_52():
#     # 1.打开这个名为量测的job
#     # 2.检查板--整板信息--量测-点对点量测是否为勾上状态
#     # 3.点击左上角运行  不出错
#     pass
