import pyautogui

import config
import utils


# @utils.screenshot_error_to_excel()
# def spc_001_01():
#     utils.check_and_launch_spc()
    # 1.点【程序视图】--在左侧选择时间【1小时】
#     utils.click_by_png(config.SPC_PROGRAM_VIEW)
#     utils.click_by_png(config.SPC_ONE_HOUR)
#     # 2.点击【查询】
#     utils.click_by_png(config.SPC_QUERY)
#     utils.close_spc()

# @utils.screenshot_error_to_excel()
# def spc_001_02():
#     utils.check_and_launch_spc()
    # 1.点【程序视图】--在左侧选择时间【8小时】
#     utils.click_by_png(config.SPC_PROGRAM_VIEW)
#     utils.click_by_png(config.SPC_EIGHT_HOURS)
#     # 2.点击【查询】
#     utils.click_by_png(config.SPC_QUERY)
#     utils.close_spc()

# @utils.screenshot_error_to_excel()
# def spc_001_03():
#     utils.check_and_launch_spc()
    # 1.点【程序视图】--在左侧选择时间【一天】
#     utils.click_by_png(config.SPC_PROGRAM_VIEW)
#     utils.click_by_png(config.SPC_ONE_DAY)
#     # 2.点击【查询】
#     utils.click_by_png(config.SPC_QUERY)
#     utils.close_spc()

# @utils.screenshot_error_to_excel()
# def spc_001_04():
#     utils.check_and_launch_spc()
    # 1.点【程序视图】--在左侧选择时间【一星期】
#     utils.click_by_png(config.SPC_PROGRAM_VIEW)
#     utils.click_by_png(config.SPC_ONE_WEEK)
#     # 2.点击【查询】
#     utils.click_by_png(config.SPC_QUERY)
#     utils.close_spc()

# @utils.screenshot_error_to_excel()
# def spc_001_05():
#     utils.check_and_launch_spc()
    # 1.点【程序视图】--在左侧选择时间【一个月】
#     utils.click_by_png(config.SPC_PROGRAM_VIEW)
#     utils.click_by_png(config.SPC_ONE_MONTH)
#     # 2.点击【查询】
#     utils.click_by_png(config.SPC_QUERY)
#     utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_002_01():
    utils.check_and_launch_spc()
    # 1.点【程序视图】--在左侧选择时间--【查询】，在中间找到对应job名字，双击进入明细
    utils.click_by_png(config.SPC_PROGRAM_VIEW)
    # 2.双击对应时间的PCB数据
    # 3.查看数据中的列表窗口和元件数据窗口的数据
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_003_01():
    utils.check_and_launch_spc()
    # 1.点【缺陷统计】--在左侧选择时间
    utils.click_by_png(config.SPC_DEFECT_STATISTICS)
    # 2.【其他选项】--【判定结果】--选择【NG】；【其他选项】--【类型】--选择【元件】；在输入框中输入想要查询的前__个元件

    # 3.点击【查询】
    utils.click_by_png(config.SPC_QUERY)
    # 4.点击【导出】
    utils.click_by_png(config.SPC_EXPORT)
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_003_02():
    utils.check_and_launch_spc()
    # 1.点【缺陷统计】--在左侧选择时间
    utils.click_by_png(config.SPC_DEFECT_STATISTICS)
    # 2.【其他选项】--【判定结果】--选择【NG】；【其他选项】--【类型】--选择【缺陷类型】；在输入框中输入想要查询的前__个缺陷类型
    # 3.点击【查询】
    utils.click_by_png(config.SPC_QUERY)
    # 4.点击【导出】
    utils.click_by_png(config.SPC_EXPORT)
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_003_03():
    utils.check_and_launch_spc()
    # 1.点【缺陷统计】--在左侧选择时间
    utils.click_by_png(config.SPC_DEFECT_STATISTICS)
    # 2.【其他选项】--【判定结果】--选择【NG】；【其他选项】--【类型】--选择【算法】；在输入框中输入想要查询的前__个算法
    # 3.点击【查询】
    utils.click_by_png(config.SPC_QUERY)
    # 4.点击【导出】
    utils.click_by_png(config.SPC_EXPORT)
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_003_04():
    utils.check_and_launch_spc()
    # 1.点【缺陷统计】--在左侧选择时间
    utils.click_by_png(config.SPC_DEFECT_STATISTICS)
    # 2.【其他选项】--【判定结果】--选择【NG】；【其他选项】--【类型】--选择【料号】；在输入框中输入想要查询的前__个算法
    # 3.点击【查询】
    utils.click_by_png(config.SPC_QUERY)
    # 4.点击【导出】
    utils.click_by_png(config.SPC_EXPORT)
    utils.close_spc()
    pass

@utils.screenshot_error_to_excel()
def spc_003_05():
    utils.check_and_launch_spc()
    # 1.点【缺陷统计】--在左侧选择时间
    utils.click_by_png(config.SPC_DEFECT_STATISTICS)
    # 2.【其他选项】--【判定结果】--选择【NG】；【其他选项】--【类型】--选择【封装类型】；在输入框中输入想要查询的前__个算法
    # 3.点击【查询】
    utils.click_by_png(config.SPC_QUERY)
    # 4.点击【导出】
    utils.click_by_png(config.SPC_EXPORT)
    utils.close_spc()
    pass

@utils.screenshot_error_to_excel()
def spc_003_06():
    utils.check_and_launch_spc()
    # 1.点【缺陷统计】--在左侧选择时间
    utils.click_by_png(config.SPC_DEFECT_STATISTICS)
    # 2.【其他选项】--【判定结果】--选择【pass】；【其他选项】--【类型】--选择【元件】；在输入框中输入想要查询的前__个元件
    # 3.点击【查询】
    utils.click_by_png(config.SPC_QUERY)
    # 4.点击【导出】
    utils.click_by_png(config.SPC_EXPORT)
    utils.close_spc()
    pass

@utils.screenshot_error_to_excel()
def spc_003_07():
    utils.check_and_launch_spc()
    # 1.点【缺陷统计】--在左侧选择时间
    utils.click_by_png(config.SPC_DEFECT_STATISTICS)
    # 2.【其他选项】--【判定结果】--选择【pass】；【其他选项】--【类型】--选择【缺陷类型】；在输入框中输入想要查询的前__个缺陷类型
    # 3.点击【查询】
    utils.click_by_png(config.SPC_QUERY)
    # 4.点击【导出】
    utils.click_by_png(config.SPC_EXPORT)
    utils.close_spc()
    pass

@utils.screenshot_error_to_excel()
def spc_003_08():
    utils.check_and_launch_spc()
    # 1.点【缺陷统计】--在左侧选择时间
    utils.click_by_png(config.SPC_DEFECT_STATISTICS)
    # 2.【其他选项】--【判定结果】--选择【pass】；【其他选项】--【类型】--选择【算法】；在输入框中输入想要查询的前__个算法
    # 3.点击【查询】
    utils.click_by_png(config.SPC_QUERY)
    # 4.点击【导出】
    utils.click_by_png(config.SPC_EXPORT)
    utils.close_spc()
    pass

@utils.screenshot_error_to_excel()
def spc_003_09():
    utils.check_and_launch_spc()
    # 1.点【缺陷统计】--在左侧选择时间
    utils.click_by_png(config.SPC_DEFECT_STATISTICS)
    # 2.【其他选项】--【判定结果】--选择【pass】；【其他选项】--【类型】--选择【料号】；在输入框中输入想要查询的前__个算法
    # 3.点击【查询】
    utils.click_by_png(config.SPC_QUERY)
    # 4.点击【导出】
    utils.click_by_png(config.SPC_EXPORT)
    utils.close_spc()
    pass

@utils.screenshot_error_to_excel()
def spc_003_10():
    utils.check_and_launch_spc()
    # 1.点【缺陷统计】--在左侧选择时间
    utils.click_by_png(config.SPC_DEFECT_STATISTICS)
    # 2.【其他选项】--【判定结果】--选择【pass】；【其他选项】--【类型】--选择【封装类型】；在输入框中输入想要查询的前__个算法
    # 3.点击【查询】
    utils.click_by_png(config.SPC_QUERY)
    # 4.点击【导出】
    utils.click_by_png(config.SPC_EXPORT)
    utils.close_spc()
    pass

@utils.screenshot_error_to_excel()
def spc_004_01():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.点【良率分析】--在左侧选择时间--在【程序名称】中选择对应job名字--在左侧【其他选项】中选择【整板】
    utils.click_by_png(config.SPC_YIELD_ANALYSIS)
    # 2.点击【查询】
    utils.click_by_png(config.SPC_QUERY)
    # 3.点击【导出】
    utils.click_by_png(config.SPC_EXPORT)
    utils.close_spc()
    pass

@utils.screenshot_error_to_excel()
def spc_004_02():
    utils.check_and_launch_spc()
    # 1.点【良率分析】--在左侧选择时间--在【程序名称】中选择对应job名字--在左侧【其他选项】中选择【拼板】
    utils.click_by_png(config.SPC_YIELD_ANALYSIS)
    # 2.点击【查询】
    utils.click_by_png(config.SPC_QUERY)
    # 3.点击【导出】
    utils.click_by_png(config.SPC_EXPORT)
    utils.close_spc()
    pass

@utils.screenshot_error_to_excel()
def spc_004_03():
    utils.check_and_launch_spc()
    # 1.点【良率分析】--在左侧选择时间--在【程序名称】中选择对应job名字--在左侧【其他选项】中选择【元件】
    utils.click_by_png(config.SPC_YIELD_ANALYSIS)
    # 2.点击【查询】
    utils.click_by_png(config.SPC_QUERY)
    # 3.点击【导出】
    utils.click_by_png(config.SPC_EXPORT)
    utils.close_spc()
    pass

@utils.screenshot_error_to_excel()
def spc_004_04():
    utils.check_and_launch_spc()
    # 1.点【良率分析】--在左侧选择时间--在【程序名称】中选择对应job名字--在左侧【其他选项】中改变【天】和【小时】前的值
    utils.click_by_png(config.SPC_YIELD_ANALYSIS)
    # 2.点击【查询】
    utils.click_by_png(config.SPC_QUERY)
    utils.close_spc()
    pass

@utils.screenshot_error_to_excel()
def spc_005_01():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.点【数据导出】--选择时间--点击【加载】
    utils.click_by_png(config.SPC_DATA_EXPORT)
    # 2.勾选要导出【job名称】
    # 3.在【导出选项】中更改图片数量限制，在【元件数据筛选】中勾选需要导出数据和图片的数据类型（通过、不良、良好）
    # 4.点击【导出】--选择保存路径
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_005_02():
    utils.check_and_launch_spc()
    # 1.点击左侧导航栏可以正常在页面中进行定位
    # 2.查看报表中的数据
    # 3.在【Component Detail Report】下查看详细数据报表，查看以下信息是否正确：
    utils.check_and_launch_spc()
    # 1）导出报表时间
    # 2）导出的数据基本信息
    # 3）图表最上方NG/Pass/Good进行切换
    # 4）除【pcbbarcode】之外其他均为下拉选择框，下拉选择框中的数据，【pcbbarcode】输入框可以输入条码
    # 5）选择并输入查询条件--【查询】
    # 6）对比表中数据与spc中数据
    # 7）查看表最右侧2D图片，点击图片
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_006_01():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.【系统设置】选择指定光源和算法，点【>】键
    utils.click_by_png(config.SPC_SYSTEM_SETTINGS)
    # 2.点保存
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_007_01():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.【系统设置】--【图像缩放】--更改【放大比例】的数值
    utils.click_by_png(config.SPC_SYSTEM_SETTINGS)
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_008_01():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.【系统设置】--【图像缩放】--勾选【显示实时整版图】
    utils.click_by_png(config.SPC_SYSTEM_SETTINGS)
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_008_02():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.【系统设置】--【图像缩放】--不勾选【显示实时整版图】
    utils.click_by_png(config.SPC_SYSTEM_SETTINGS)
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_009_01():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.【系统设置】--【图像视图】--勾选【整板图像】
    utils.click_by_png(config.SPC_SYSTEM_SETTINGS)
    utils.close_spc()
@utils.screenshot_error_to_excel()
def spc_009_02():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.【系统设置】--【图像视图】--不勾选【整板图像】
    utils.click_by_png(config.SPC_SYSTEM_SETTINGS)
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_009_03():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.【系统设置】--【图像视图】--勾选【FOV图像】
    utils.click_by_png(config.SPC_SYSTEM_SETTINGS)
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_009_04():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.【系统设置】--【图像视图】--不勾选【FOV图像】
    utils.click_by_png(config.SPC_SYSTEM_SETTINGS)
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_009_05():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.【系统设置】--【图像视图】--勾选【标准图像】
    utils.click_by_png(config.SPC_SYSTEM_SETTINGS)
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_009_06():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.【系统设置】--【图像视图】--不勾选【标准图像】
    utils.click_by_png(config.SPC_SYSTEM_SETTINGS)
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_009_07():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.【系统设置】--【图像视图】--勾选【不良图像】
    utils.click_by_png(config.SPC_SYSTEM_SETTINGS)
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_009_08():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.【系统设置】--【图像视图】--不勾选【不良图像】
    utils.click_by_png(config.SPC_SYSTEM_SETTINGS)
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_009_09():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.【系统设置】--【图像视图】--勾选【3D图像】
    utils.click_by_png(config.SPC_SYSTEM_SETTINGS)
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_009_10():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.【系统设置】--【图像视图】--不勾选【3D图像】
    utils.click_by_png(config.SPC_SYSTEM_SETTINGS)
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_009_11():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.【系统设置】--【图像视图】--勾选【窗口数据】
    utils.click_by_png(config.SPC_SYSTEM_SETTINGS)
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_009_12():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.【系统设置】--【图像视图】--不勾选【窗口数据】
    utils.click_by_png(config.SPC_SYSTEM_SETTINGS)
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_010_01():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.【系统设置】--【其他设置】--【检测结果统计】--勾选【包含其他（NG、Good、Pass之外）】
    utils.click_by_png(config.SPC_SYSTEM_SETTINGS)
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_010_02():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.【系统设置】--【其他设置】--【检测结果统计】--不勾选【包含其他（NG、Good、Pass之外）】
    utils.click_by_png(config.SPC_SYSTEM_SETTINGS)
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_010_03():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.【系统设置】--【其他设置】--【检测结果统计】--勾选【Pass数据显示】
    utils.click_by_png(config.SPC_SYSTEM_SETTINGS)
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_010_04():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.【系统设置】--【其他设置】--【检测结果统计】--不勾选【Pass数据显示】
    utils.click_by_png(config.SPC_SYSTEM_SETTINGS)
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_011_01():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.【系统设置】--【其他设置】--【单位类型】--勾选【UM】
    utils.click_by_png(config.SPC_SYSTEM_SETTINGS)
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_011_02():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.【系统设置】--【其他设置】--【单位类型】--勾选【MM】
    utils.click_by_png(config.SPC_SYSTEM_SETTINGS)
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_012_01():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.【系统设置】--【其他设置】--【单位类型】--【不允许最大化】
    utils.click_by_png(config.SPC_SYSTEM_SETTINGS)
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_012_02():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.【系统设置】--【其他设置】--【单位类型】--【允许最大化】
    utils.click_by_png(config.SPC_SYSTEM_SETTINGS)
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_013_01():
    utils.check_and_launch_spc()
    # 1.点击【重新加载】
    pass

@utils.screenshot_error_to_excel()
def spc_014_01():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.点【程序视图】--在左侧选择时间--【查询】，在中间找到对应job名字，双击进入明细
    utils.click_by_png(config.SPC_PROGRAM_VIEW)
    # 2.双击任意一条PCB数据
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_014_02():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.点【程序视图】--在左侧选择时间--【查询】，在中间找到对应job名字，双击进入明细
    utils.click_by_png(config.SPC_PROGRAM_VIEW)
    # 2.选择任意一条PCB数据，点击【PCB视图】
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_014_03():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.点【程序视图】--在左侧选择时间--【查询】，在中间找到对应job名字，双击进入明细
    utils.click_by_png(config.SPC_PROGRAM_VIEW)
    # 2.选择任意一条PCB数据，【右键】--【PCB视图】
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_015_01():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.点【程序视图】--在左侧选择时间--【查询】，在中间找到对应job名字，双击进入明细
    utils.click_by_png(config.SPC_PROGRAM_VIEW)
    # 2.选择多条数据
    # 3.【右键】--【PCB视图】
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_015_02():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.点【程序视图】--在左侧选择时间--【查询】，在中间找到对应job名字，双击进入明细
    utils.click_by_png(config.SPC_PROGRAM_VIEW)
    # 2.选择多条数据
    # 3.点击【PCB视图】
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_016_01():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.点【程序视图】--在左侧选择时间--【查询】，在中间找到对应job名字，双击进入明细
    utils.click_by_png(config.SPC_PROGRAM_VIEW)
    # 2.选中一笔数据--右键--【TOP缺陷元件】
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_016_02():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.点【程序视图】--在左侧选择时间--【查询】，在中间找到对应job名字，双击进入明细
    utils.click_by_png(config.SPC_PROGRAM_VIEW)
    # 2.选中一笔数据--右键--【TOP缺陷类型】
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_016_03():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.点【程序视图】--在左侧选择时间--【查询】，在中间找到对应job名字，双击进入明细
    utils.click_by_png(config.SPC_PROGRAM_VIEW)
    # 2.选中一笔数据--右键--【TOP缺陷算法】
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_016_04():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.点【程序视图】--在左侧选择时间--【查询】，在中间找到对应job名字，双击进入明细
    utils.click_by_png(config.SPC_PROGRAM_VIEW)
    # 2.选中一笔数据--右键--【TOP料号】
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_016_05():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.点【程序视图】--在左侧选择时间--【查询】，在中间找到对应job名字，双击进入明细
    utils.click_by_png(config.SPC_PROGRAM_VIEW)
    # 2.选中一笔数据--右键--【TOP封装类型】
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_016_06():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.点【程序视图】--在左侧选择时间--【查询】，在中间找到对应job名字，双击进入明细
    utils.click_by_png(config.SPC_PROGRAM_VIEW)
    # 2.右键--【导出】
    # 3.选择【样式一】--【确定】
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_016_07():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.点【程序视图】--在左侧选择时间--【查询】，在中间找到对应job名字，双击进入明细
    utils.click_by_png(config.SPC_PROGRAM_VIEW)
    # 2.右键--【导出】
    # 3.选择【样式二】--【确定】
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_016_08():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.点【程序视图】--在左侧选择时间--【查询】，在中间找到对应job名字，双击进入明细
    utils.click_by_png(config.SPC_PROGRAM_VIEW)
    # 2.右键--【导出】
    # 3.选择【PCB列表数据】--勾选【判定结果】中需要导出的结果（良好、不良、通过）--【确定】
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_016_09():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.点【程序视图】--在左侧选择时间--【查询】，在中间找到对应job名字，双击进入明细
    utils.click_by_png(config.SPC_PROGRAM_VIEW)
    # 2.右键--【导出】
    # 3.选择【元件检测结果】--勾选【元件】中需要导出的元件位号--勾选【缺陷类型】中需要导出的类型--【确定】
    # 4.设置是否导出标准图，设置导出的图片数量，设置导出的图片光源
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_016_10():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.点【程序视图】--在左侧选择时间--【查询】，在中间找到对应job名字，双击进入明细
    utils.click_by_png(config.SPC_PROGRAM_VIEW)
    # 2.右键--【导出】
    # 3.选择【窗口检测项结果】--勾选【算法】中需要导出的算法
    # 4.设置是否都出其他检测项
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_016_11():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.点【程序视图】--在左侧选择时间--【查询】，在中间找到对应job名名，双击进入明细
    utils.click_by_png(config.SPC_PROGRAM_VIEW)
    # 2.右键--【导出】
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_016_12():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.点【程序视图】--在左侧选择时间--【查询】，在中间找到对应job名名，双击进入明细
    utils.click_by_png(config.SPC_PROGRAM_VIEW)
    # 2.选择一个检测结果为【样板】的数据，右键--【修改结果】--【通过】
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_016_13():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.点【程序视图】--在左侧选择时间--【查询】，在中间找到对应job名名，双击进入明细
    utils.click_by_png(config.SPC_PROGRAM_VIEW)
    # 2.选择一个检测结果为【通过】的数据，右键--【修改结果】--【样板】
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_017_01():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.点【程序视图】--在左侧选择时间--【查询】，在中间找到对应job名名，双击进入明细，选择一条数据双击进入PCB视图
    utils.click_by_png(config.SPC_PROGRAM_VIEW)
    # 2.查看PCB视图中列表的窗口和元件数据
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_017_02():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.按快捷键【Alt+F12】
    pyautogui.hotkey('alt', 'f12')
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_018_01():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.点【CPK分析】
    utils.click_by_png(config.SPC_CPK_ANALYSIS)
    # 2.选择【时间范围】--【1天】，选择【数据筛选】下拉框中的程式/元件，选择【其他选项】--【检测项】下拉框中的检测项
    # 3.点击【查询】
    utils.click_by_png(config.SPC_QUERY)
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_018_02():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.点【CPK分析】
    utils.click_by_png(config.SPC_CPK_ANALYSIS)
    # 2.选择【时间范围】--【1天】，选择【数据筛选】下拉框中的程式/元件，选择【其他选项】--【检测项】下拉框中的检测项
    # 3.点击【导出】
    utils.click_by_png(config.SPC_EXPORT)
    utils.close_spc()
@utils.screenshot_error_to_excel()
def spc_018_03():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.点【CPK分析】
    utils.click_by_png(config.SPC_CPK_ANALYSIS)
    # 2.选择【时间范围】--【1星期】，选择【数据筛选】下拉框中的程式/元件，选择【其他选项】--【检测项】下拉框中的检测项
    # 3.点击【查询】
    utils.click_by_png(config.SPC_QUERY)
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_018_04():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.点【CPK分析】
    utils.click_by_png(config.SPC_CPK_ANALYSIS)
    # 2.选择【时间范围】--【1星期】，选择【数据筛选】下拉框中的程式/元件，选择【其他选项】--【检测项】下拉框中的检测项
    # 3.点击【导出】
    utils.click_by_png(config.SPC_EXPORT)
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_018_05():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.点【CPK分析】
    utils.click_by_png(config.SPC_CPK_ANALYSIS)
    # 2.选择【时间范围】--【1个月】，选择【数据筛选】下拉框中的程式/元件，选择【其他选项】--【检测项】下拉框中的检测项
    # 3.点击【查询】
    utils.click_by_png(config.SPC_QUERY)
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_018_06():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.点【CPK分析】
    utils.click_by_png(config.SPC_CPK_ANALYSIS)
    # 2.选择【时间范围】--【1个月】，选择【数据筛选】下拉框中的程式/元件，选择【其他选项】--【检测项】下拉框中的检测项
    # 3.点击【导出】
    utils.click_by_png(config.SPC_EXPORT)
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_019_01():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.点【GRR分析】
    utils.click_by_png(config.SPC_GRR_ANALYSIS)
    # 2.选择【时间范围】--【1天】，选择【数据筛选】下拉框中的程式/元件，选择【其他选项】--【检测项】下拉框中的检测项
    # 3.点击【查询】
    utils.click_by_png(config.SPC_QUERY)
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_019_02():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.点【GRR分析】
    utils.click_by_png(config.SPC_GRR_ANALYSIS)
    # 2.选择【时间范围】--【1天】，选择【数据筛选】下拉框中的程式/元件，选择【其他选项】--【检测项】下拉框中的检测项
    # 3.点击【导出】
    utils.click_by_png(config.SPC_EXPORT)
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_019_03():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.点【GRR分析】
    utils.click_by_png(config.SPC_GRR_ANALYSIS)
    # 2.选择【时间范围】--【1星期】，选择【数据筛选】下拉框中的程式/元件，选择【其他选项】--【检测项】下拉框中的检测项
    # 3.点击【查询】
    utils.click_by_png(config.SPC_QUERY)
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_019_04():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.点【GRR分析】
    utils.click_by_png(config.SPC_GRR_ANALYSIS)
    # 2.选择【时间范围】--【1星期】，选择【数据筛选】下拉框中的程式/元件，选择【其他选项】--【检测项】下拉框中的检测项
    # 3.点击【导出】
    utils.click_by_png(config.SPC_EXPORT)
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_019_05():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.点【GRR分析】
    utils.click_by_png(config.SPC_GRR_ANALYSIS)
    # 2.选择【时间范围】--【1个月】，选择【数据筛选】下拉框中的程式/元件，选择【其他选项】--【检测项】下拉框中的检测项
    # 3.点击【查询】
    utils.click_by_png(config.SPC_QUERY)
    utils.close_spc()

@utils.screenshot_error_to_excel()
def spc_019_06():
    utils.check_and_launch_spc()
    utils.check_and_launch_spc()
    # 1.点【GRR分析】
    utils.click_by_png(config.SPC_GRR_ANALYSIS)
    # 2.选择【时间范围】--【1个月】，选择【数据筛选】下拉框中的程式/元件，选择【其他选项】--【检测项】下拉框中的检测项
    # 3.点击【导出】
    utils.click_by_png(config.SPC_EXPORT)
    utils.close_spc()
