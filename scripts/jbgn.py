import utils
import time
import pyautogui
import config

@utils.screenshot_error_to_excel()
# 新建单板程式
def jbgn_001_01():
    # 新建程式文件：选择保存目录，选择单板CAD文件，输入【程式名称】，【是】         进入整版影像页面
    # 点击进版
    # 待页面上方绿色方块到中间位置，点击【移到板边】，将版右下角位置移到屏幕中心十字线，点击【右下角标记位】
    # 将版左上角移动到屏幕中心十字线，点击【左上角标记位】
    # 点击【扫描整版】          出现扫版参数提示框
    # 点击【是】                开始扫描整版，有等待FOV数据保存完成提示框，整版扫描完成后弹出：确认基板颜色提示框
    # 确认基板颜色提示框，根据实际情况点击【是】或【否】    出现导入默认库提示框
    # 弹出导入库提示框，选择【Default】后点击是             
    # 选中MARK点附近的空元件：Designator，右键选择【标记点操作】--【转换为标记点】--【是】
    # 选中标记点--右键选择【标记点操作】--【根据标记点矫正元件】    正常矫正整板坐标，无报错
    pass



@utils.screenshot_error_to_excel()
# 新建单板程式后测试RV复判并在SPC确认数据
def jbgn_001_02():
1、使用Job对应的PCB板
2、Ctrl+Shift+L删除日志
3、UI:参数配置--应用配置--硬件配置：不选【打开左右循环】、选择【左进左出】
4、UI:参数配置--流程配置：
（1）缺陷视图：不选【打开DV复判模式】、不选【DV自动确认】按钮
（2）数据流向：选择【允许中间层转发数据】
5、UI:参数配置--演算法配置：
（1）强制操作：不选【基准点NG继续矫正位置】、
（2）算法日志：只选【计算时间】
6、UI:参数配置--数据导出配置：
（1）不选【使用Good/NG分开传输】、不选【只导出NG】
（2）FOV影像输出：选择【所有】
（3）元件输出影像：选择【所有】，Good/Pass/NG元件数量限制：选择【所有】
（4）RV输出：选择【输出检测数据到RV】
7、UI:参数配置--条码--条码读取设定：选择【允许填充条码时间戳】
8、RV:手动确认























































    utils.check_and_launch_aoi()
    utils.click_by_controls(config.OPEN_PROGRAM, 1)
    directory = r"D:\EYAOI\JOB"
    bbox = (640, 190, 719, 203)
    time.sleep(0.2)
    utils.text_in_bbox(directory, bbox)
    time.sleep(0.2)
    # 把最近打开程式收起来
    pyautogui.click(544, 292)
    program_bbox = (535, 300, 920, 555)
    program_loaded_bbox = (1000, 280, 1380, 550)
    # 双击任意程式
    cursor_exist = utils.check_load_program(config.OPEN_PROGRAM_CURSOR, program_bbox, program_loaded_bbox)
    if not cursor_exist:
        plus_exist = utils.check_load_program(config.OPEN_PROGRAM_PLUS, program_bbox, program_loaded_bbox)
        if not plus_exist:
            raise Exception("程式都不存在，可能文件夹下无可识别的程式")
    utils.click_by_controls(config.YES, 1)
    # 有进度条提示
    utils.search_symbol_erroring(config.PROGRAM_LOADING, 30)
    # 确定加载后
    utils.search_symbol_erroring(config.PROGRAM_COMPONENT_DARK, 5)
    # 无闪退
    utils.search_symbol_erroring(config.AOI_TOPIC, 5)


@utils.screenshot_error_to_excel()
def jbgn_001_03():
    准备4块拼版的CAD文件


















    utils.check_and_launch_aoi()
    utils.click_by_controls(config.OPEN_PROGRAM, 1)
    directory = r"D:\EYAOI\JOB"
    bbox = (640, 190, 719, 203)
    time.sleep(0.2)
    utils.text_in_bbox(directory, bbox)
    time.sleep(0.2)
    # 把最近打开程式收起来
    pyautogui.click(544, 292)
    program_bbox = (535, 300, 920, 555)
    program_loaded_bbox = (1000, 280, 1380, 550)
    # 找到左侧所有程式图标
    program_list = []
    exist_cursor = utils.search_symbol(config.OPEN_PROGRAM_CURSOR, None, program_bbox)
    exist_plus = utils.search_symbol(config.OPEN_PROGRAM_PLUS, None,program_bbox)
    if exist_cursor:
        program_list += list(pyautogui.locateAllOnScreen(config.OPEN_PROGRAM_CURSOR, region=program_bbox))
    if exist_plus:
        program_list += list(pyautogui.locateAllOnScreen(config.OPEN_PROGRAM_PLUS, region=program_bbox))
    if not program_list:
        raise Exception("疑似程式文件夹/程式文件未加载")
    for program in program_list:
        time.sleep(0.5)
        # 双击程式图标
        pyautogui.doubleClick(program)
        time.sleep(2)  # 等待加载
        # 检查右侧是否加载了相应的程式, 找不到自然会报错
        if exist_cursor:
            pyautogui.locateOnScreen(config.OPEN_PROGRAM_PLUS, region=program_loaded_bbox)
        if exist_plus:
            pyautogui.locateOnScreen(config.OPEN_PROGRAM_PLUS, region=program_loaded_bbox)
    utils.click_by_controls(config.YES, 1)
    # 有进度条提示
    utils.search_symbol_erroring(config.PROGRAM_LOADING, 30)
    # 确定加载后
    utils.search_symbol_erroring(config.PROGRAM_COMPONENT_DARK, 5)
    # 无闪退
    utils.search_symbol_erroring(config.AOI_TOPIC, 5)


@utils.screenshot_error_to_excel()
def jbgn_001_04():
    for i in range(3):
        # 确保aoi打开
        utils.check_and_launch_aoi()
        # 打开程式
        utils.click_by_controls(config.OPEN_PROGRAM, 1)
        directory = r"D:\EYAOI\JOB"
        bbox = (640, 190, 719, 203)
        time.sleep(0.2)
        utils.text_in_bbox(directory, bbox)
        time.sleep(0.2)
        # 把最近打开程式收起来
        pyautogui.click(544, 292)
        program_bbox = (535, 300, 920, 555)
        program_loaded_bbox = (1000, 280, 1380, 550)
        # 双击任意程式
        cursor_exist = utils.check_load_program(config.OPEN_PROGRAM_CURSOR, program_bbox, program_loaded_bbox)
        if not cursor_exist:
            plus_exist = utils.check_load_program(config.OPEN_PROGRAM_PLUS, program_bbox, program_loaded_bbox)
            if not plus_exist:
                raise Exception("程式都不存在，可能文件夹下无可识别的程式")

        # 重复步骤 打开——至——取消 三次后 点击确定按钮
        if i < 2:
            # 确定弹窗存在
            utils.search_symbol_erroring(config.OPEN_PROGRAM_TOPIC, 5)
            # 点击取消
            utils.click_by_controls(config.OPEN_PROGRAM_CANCEL, 1)
            time.sleep(0.2)
            print("开始确定无闪退")
            # 确定返回之前的整版视图
            utils.click_by_controls(config.WHOLE_BOARD_LIGHT, 1)
            print("已确定无闪退")
            time.sleep(0.2)
        else:
            utils.click_by_controls(config.YES, 1)
            # 有进度条提示
            utils.search_symbol_erroring(config.PROGRAM_LOADING, 30)
            # 确定加载后
            utils.search_symbol_erroring(config.PROGRAM_COMPONENT_DARK, 5)
            # 无闪退
            utils.search_symbol_erroring(config.AOI_TOPIC, 5)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    utils.check_and_launch_aoi()
    utils.click_by_controls(config.OPEN_PROGRAM, 1)
    directory = r"D:\EYAOI\JOB"
    bbox = (640, 190, 719, 203)
    program_loaded_bbox = (1000, 280, 1380, 550)
    time.sleep(0.2)
    utils.text_in_bbox(directory, bbox)
    time.sleep(0.2)
    # 把最近打开程式收起来
    pyautogui.click(544, 292)
    program_bbox = (535, 300, 920, 555)
    program_loaded_bbox = (1000, 280, 1380, 550)
    # 双击任一指针程式，确保在右边之后，点击右边的程式，点击移除
    cursor_load = utils.check_load_program(config.OPEN_PROGRAM_CURSOR, program_bbox, program_loaded_bbox)
    if cursor_load:
        loaded_cursor = pyautogui.locateCenterOnScreen(config.OPEN_PROGRAM_CURSOR, region=program_loaded_bbox)
        pyautogui.click(loaded_cursor)
        utils.click_by_controls(config.REMOVE_PROGRAM, 1)
        if utils.search_symbol(config.OPEN_PROGRAM_CURSOR, None, program_loaded_bbox):
            raise Exception("指针程式移除失败")
        else:
            print("移除指针程式成功")
    # 左边没指针程式，尝试处理＋号程式
    elif not cursor_load:
        cursor_load = utils.check_load_program(config.OPEN_PROGRAM_PLUS, program_bbox, program_loaded_bbox)
        if cursor_load:
            loaded_plus = pyautogui.locateCenterOnScreen(config.OPEN_PROGRAM_PLUS, region=program_loaded_bbox)
            pyautogui.click(loaded_plus)
            utils.click_by_controls(config.REMOVE_PROGRAM, 1)
            if utils.search_symbol(config.OPEN_PROGRAM_PLUS, None, program_loaded_bbox):
                raise Exception("＋号程式移除失败")
            else:
                print("移除＋号程式成功")
        else:
            raise Exception("左边没有任何程式")
    else:
        raise Exception("程式都不存在，可能文件夹下无可识别的程式")
打开任一程式
def jbgn_001_05():
    pass
打开多个程式
def jbgn_001_06():
    pass
移除程式
def jbgn_001_07():
    pass
打开指定程式
def jbgn_001_08():
    1、参数配置--UI配置--软件界面：不选【自动加载程式】
    pass
打开指定程式
def jbgn_001_09():
    pass
打开指定程式
def jbgn_001_10():
    pass
保存程式
def jbgn_001_11():
    pass
另存程式
def jbgn_001_12():
    pass
运行指定程式
def jbgn_001_13():
    1、使用Job对应的PCB板
2、Ctrl+Shift+L删除日志
3、UI:参数配置--应用配置--硬件配置：不选【打开左右循环】
4、UI:参数配置--流程配置：
（1）缺陷视图：不选【打开DV复判模式】、不选【DV自动确认】按钮
（2）数据流向：选择【允许中间层转发数据】
5、UI:参数配置--演算法配置：
（1）强制操作：不选【基准点NG继续矫正位置】、
（2）算法日志：只选【计算时间】
6、UI:参数配置--数据导出配置：
（1）不选【使用Good/NG分开传输】、不选【只导出NG】
（2）FOV影像输出：选择【所有】
（3）元件输出影像：选择【所有】，Good/Pass/NG元件数量限制：选择【所有】
（4）RV输出：选择【输出检测数据到RV】
7、UI:参数配置--条码--条码读取设定：选择【允许填充条码时间戳】
8、RV:手动确认


    pass
检查运行相关时间
def jbgn_001_14():
    1、程式运行结束
    pass
检查RV概览数据
def jbgn_001_15():
    
1、UI整板视图左上方【板】-【FOV】-【FOV检测】-【异物】：选择所有选项
2、程式运行结束
    pass
检查RV算法数据
def jbgn_001_16():
    1、程式运行结束
    pass
RV确认
def jbgn_001_17():
    1、程式运行结束
2、检查RV算法数据结束
    pass
检查SPC数据
def jbgn_001_18():
    1、UI:参数配置--流程配置--缺陷视图：不选【打开DV复判模式】、不选【DV自动确认】按钮
2、UI:参数配置--数据导出配置：
（1）不选【使用Good/NG分开传输】、不选【只导出NG】
（2）FOV影像输出：选择【所有】
（3）元件输出影像：选择【所有】，Good/Pass/NG元件数量限制：选择【所有】
3、RV:复判后
    pass
良率更新
def jbgn_001_19():
    1、程式运行结束
2、RV复判后
    pass
元件拍照类型
def jbgn_001_20():
    1、程式已设置：料号47UF_6.3*7.7mm拍照类型设置Quad12mm
    pass
抽测元件
def jbgn_001_21():
    1、程式已设置：元件LVC1设置抽测元件：1/3测试
    pass
抽测窗口1/3
def jbgn_001_22():
    1、程式已设置：抽测窗口1/3忽略， 元件：epcos1、epcos2，窗口： 颜色匹配
    pass
拍照高度设置
def jbgn_001_23():
    1、程式已设置：元件G6K-2F-Y(J3,J2)拍照高度设置10mm
    pass
元件缺陷锁定
def jbgn_001_24():
    1、程式已设置：元件缺陷锁定：7343TAN-100uf
2、UI不启用单料号模式，须将D:\EYUI\BIN\config\SinglePartNo.cfg重命名
    pass
强制导出DJB
def jbgn_001_25():
    1、程式已设置：强制导出料号4D03-100R
    pass
# 参数控制限定
def jbgn_001_26():
    1、程式已设置：料号R6322-2512-470E的X偏移：100-500
    pass
# 定位元件
def jbgn_001_27():
    1、程式已设置：定位元件： Designator3+r60 r58 r56 r54

    pass
# 大元件测试
def jbgn_001_28():
    1、程式运行结束
    pass
# 整板量测
def jbgn_001_29():
    1、程式已设置：整板量测【123】
    pass
# 整板异物检测
def jbgn_001_30():
    
1、UI整板视图左上方【板】-【FOV】-【FOV检测】-【异物】：选择所有选项
2、程式运行结束
    pass
# 整板离散度
def jbgn_001_31():
    1、整板离散度--半径：100mm
    pass
# 运行坏板程式
def jbgn_001_32():
    1、使用Job对应的PCB板，坏的拼板放在左上角位置
    pass
# 坏板RV信息
def jbgn_001_33():
    1、使用Job对应的PCB板，坏的拼板放在左上角位置
2、程式运行停止后


    pass
# 坏板SPC信息
def jbgn_001_34():
    1、使用Job对应的PCB板，坏的拼板放在左上角位置
2、RV复判后


    pass
# 坏板良率信息
def jbgn_001_35():
    1、使用Job对应的PCB板，坏的拼板放在左上角位置
2、程式运行、复判后


    pass
# 运行坏板程式
def jbgn_001_36():
    1、使用Job对应的PCB板，坏的拼板放在左上角位置
    pass
# 坏板RV信息
def jbgn_001_37():
    1、使用Job对应的PCB板，坏的拼板放在左上角位置
2、程式运行停止后
    pass
# 坏板SPC信息
def jbgn_001_38():
    1、使用Job对应的PCB板，坏的拼板放在左上角位置
2、RV复判后
    pass
# 坏板良率信息
def jbgn_001_39():
    1、使用Job对应的PCB板，坏的拼板放在左上角位置
2、RV复判后


    pass
# 检查细调算法
def jbgn_001_40():
    1、程式运行停止后
    pass
# 细调元件切换
def jbgn_001_41():
    1、程式运行停止后
    pass
# 搜索范围变化
def jbgn_001_42():
    1、程式运行停止后
    pass
# 调整检测框
def jbgn_001_43():
    1、程式运行停止后
    pass
# 停止响应
def jbgn_001_44():
    pass
# 状态稳定性
def jbgn_001_45():
    pass
# SPC数据保存
def jbgn_001_46():
    1、参数配置--流程配置--缺陷视图：不勾选【打开DV复判模式】、不勾选【DV自动确认】按钮
2、RV：手工确认
    pass
# SPC数据保存
def jbgn_001_47():
    1、参数配置--流程配置--缺陷视图:勾选【打开DV复判模式】
2、RV：手工确认
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
# 离线调整参数
def jbgn_001_50():
    #1、接案例JBGN-001-01，做好job并矫正
    #2、选择任一元件，双金进入离线编辑界面
    # 3、修改任一算法参数，切换到同料号其它元件，弹框选择【是】 参数已修改，窗口位置不会变
    # 4、调整任一算法窗口，切换到同料号其它元件，弹框选择【是】 窗口位置已修改，其它窗口位置不会变
    pass

# 细调调整参数
def jbgn_001_51():
    # 1、接案例JBGN-001-01，做好job并矫正
    # 2、点【测试】按钮开始测试，测试完成后，点【停止】按钮，点击右下角【进入细调界面】
    # 3、选择任一元件，修改任一算法参数，切换到同料号其它元件，弹框选择【是】   参数已修改，窗口位置不会变

    # 4、调整任一算法窗口，切换到同料号其它元件，弹框选择【是】     窗口位置已修改，其它窗口位置不会变
    pass

# 量测测试
def jbgn_001_52():
    # 1.打开这个名为量测的job
    # 2.检查板--整板信息--量测-点对点量测是否为勾上状态
    # 3.点击左上角运行  不出错
    pass
