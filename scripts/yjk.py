import utils
import config
import pyautogui
import time
from loguru import logger

@utils.screenshot_error_to_excel()
def yjk_001_01():
    # 1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 2、点击【菜单栏】--【元件库】--【导出当前料号】
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.EXPORT_CURRENT_PN)
    # 3、弹框 设置默认，点击是。
    utils.search_symbol_erroring(config.ELEMENTS_DEFAULT)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(5)
    # 4、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】，
    utils.click_by_png(config.MANUAL_SELECT)
    # 1）下拉框查找所选的元件库
    # 2）点击所选的元件库 扩展 （元件库->芯片类型->封装类型->料号）
    # 3）点击图片
    # 4）查看下面信息与导出的料号信息（元件上右键--【元件信息】）对比。
    # 5、所选的元件库文件夹（元件库路径：【设置】--【数据导出配置】--【元件库设置】--【元件库路径】），查看是否有导出，分类名称、芯片类型、料号、封装类型是否与导出的料号信息对应
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def yjk_001_02():
    # 1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 2、点击【菜单栏】--【元件库】--【导出当前料号】
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.EXPORT_CURRENT_PN)
    # 3、弹框 设置默认，点击取消。
    utils.search_symbol_erroring(config.ELEMENTS_DEFAULT)
    time.sleep(1)
    pyautogui.press("left")
    pyautogui.press("enter")
    # 4、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】和元件库路径，查看是否有导出
    utils.close_aoi()


@utils.screenshot_error_to_excel()
def yjk_001_03():
utils.check_and_launch_aoi()
    # 1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 2、点击【菜单栏】--【元件库】--【导出当前料号】
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.EXPORT_CURRENT_PN)
    # 3、弹框 切换分类名称、修改芯片类型、修改封装类型，点击是
    # 4、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】，
    # 1）下拉框查找切换的元件库
    # 2）点击所切换的元件库 扩展 （元件库->芯片类型->封装类型->料号）
    # 3）点击图片
    # 4）查看下面信息与导出的料号信息（元件上右键--【元件信息】）对比。
    # 5、所选的元件库文件夹（元件库路径：【设置】--【数据导出配置】--【元件库设置】--【元件库路径】），查看是否有导出，分类名称、芯片类型、料号、封装类型是否与导出的料号信息对应
    utils.close_aoi()
@utils.screenshot_error_to_excel()
def yjk_001_04():
utils.check_and_launch_aoi()
    # 1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    # 2、点击【菜单栏】--【元件库】--【导出当前料号】
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.EXPORT_CURRENT_PN)
    # 3、弹框 新增分类名称、修改芯片类型、修改封装类型，点击是
    # 4、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】，
    # 1）下拉框查找新增的元件库
    # 2）点击所新增的元件库 扩展 （元件库->芯片类型->封装类型->料号）
    # 3）点击图片
    # 4）查看下面信息与导出的料号信息（元件上右键--【元件信息】）对比。
    # 5、新增的元件库文件夹（元件库路径：【设置】--【数据导出配置】--【元件库设置】--【元件库路径】），查看是否有导出，分类名称、芯片类型、料号、封装类型是否与导出的料号信息对应
    utils.close_aoi()
@utils.screenshot_error_to_excel()
def yjk_001_05():
    # 跳
utils.check_and_launch_aoi()
    # 1、选任一元件，双击进入【编辑界面】
    # 2、点击【菜单栏】--【元件库】--【导入当前料号】
    # 3、选有此料号的元件库名称，点击是
    # 4、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】，找到导入的是哪个元件库 哪个料号（点击ABC 标志），元件信息、元件窗口，进行对比
    utils.close_aoi()
@utils.screenshot_error_to_excel()
def yjk_001_06():
    # 跳
utils.check_and_launch_aoi()
    # 1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
    # 2、点击【菜单栏】--【元件库】--【导出当前料号】
    # 3、弹框 设置默认，点击是。
    # 4、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】，
    # 1）下拉框查找所选的元件库
    # 2）点击所选的元件库 扩展 （元件库->芯片类型->封装类型->料号）
    # 3）查看整板上的料号是否都有导到此元件库
    # 4）查看下面信息与导出的料号信息（元件上右键--【元件信息】）对比。
    # 5、所选的元件库文件夹（元件库路径：【设置】--【数据导出配置】--【元件库设置】--【元件库路径】），查看整板上的料号是否都有导到此元件库此元件库；分类名称、芯片类型、料号、封装类型是否与导出的料号信息对应
    utils.close_aoi()
    pass

@utils.screenshot_error_to_excel()
def yjk_001_07():
    utils.check_and_launch_aoi()
    # 1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
    utils.ensure_in_edit_mode()
    # 2、点击【菜单栏】--【元件库】--【导出所有】
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.EXPORT_ALL_PN)
    # 3、弹框 设置默认，点击取消。
    # 4、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】和元件库路径，查看是否有导出
    utils.close_aoi()


@utils.screenshot_error_to_excel()
def yjk_001_08():
utils.check_and_launch_aoi()
    # 1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
    # 2、点击【菜单栏】--【元件库】--【导出所有】
    # 3、弹框 任选一个已有的元件库，点击是。
    # 4、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】，
    # 1）下拉框查找所选的元件库
    # 2）点击所选的元件库 扩展 （元件库->芯片类型->封装类型->料号）
    # 3）查看整板上的料号是否都有导到此元件库
    # 4）查看下面信息与导出的料号信息（元件上右键--【元件信息】）对比。
    # 5、所选的元件库文件夹（元件库路径：【设置】--【数据导出配置】--【元件库设置】--【元件库路径】），查看整板上的料号是否都有导到此元件库此元件库；分类名称、芯片类型、料号、封装类型是否与导出的料号信息对应
    utils.close_aoi()


@utils.screenshot_error_to_excel()
def yjk_001_09():
utils.check_and_launch_aoi()
#     1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
# 2、点击【菜单栏】--【元件库】--【导出所有】
# 3、弹框 新增元件库分类名称，点击是。
# 4、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】，
# 1）下拉框查找所选的元件库
# 2）点击所选的元件库 扩展 （元件库->芯片类型->封装类型->料号）
# 3）查看整板上的料号是否都有导到此元件库
# 4）查看下面信息与导出的料号信息（元件上右键--【元件信息】）对比。
# 5、所选的元件库文件夹（元件库路径：【设置】--【数据导出配置】--【元件库设置】--【元件库路径】），查看整板上的料号是否都有导到此元件库此元件库；分类名称、芯片类型、料号、封装类型是否与导出的料号信息对应
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def yjk_001_10():
utils.check_and_launch_aoi()
#     1、选任一元件，双击进入【编辑界面】
    utils.ensure_in_edit_mode()
# 2、点击【菜单栏】--【元件库】--【导入所有】
# 3、选有 多个料号的元件库名称，点击是
# 4、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】，找到导入的是哪个元件库 哪个料号（点击ABC 标志），元件信息、元件窗口，进行对比
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def yjk_001_11():
utils.check_and_launch_aoi()
#     1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
# 2、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】
# 3、点击ABC
    utils.close_aoi()
@utils.screenshot_error_to_excel()
def yjk_001_12():
utils.check_and_launch_aoi()
#     1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
# 2、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】
# 3、PN栏输入 当前元件的料号，点击查询标志
# 4、点击撤销标志
    utils.close_aoi()
@utils.screenshot_error_to_excel()
def yjk_001_13():
    # 跳
utils.check_and_launch_aoi()
#     1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
# 2、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】
# 3、PT栏输入 当前元件的料号，点击查询标志
# 4、点击撤销标志
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def yjk_001_14():
utils.check_and_launch_aoi()
#     1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
# 2、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】
# 3、点击下拉框勾选某些元件库，点击OK
# 4、再次点击下拉框，勾选Select All
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def yjk_001_15():
utils.check_and_launch_aoi()
#     1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
# 2、点击【菜单栏】--【元件库】--【导出所有】/【导出当前料号】
# 3、弹框新增元件库分类名称，点击是
# 4、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】
# ，点击刷新（循环标志）
# 5、点击最上方的元件库 扩展 （元件库->芯片类型->封装类型->料号），查看导出的元件库料号，是否都显示
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def yjk_001_16():
utils.check_and_launch_aoi()
    utils.check_refresh_tree(False)
#     1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
# 2、点击【菜单栏】--【元件库】--【导出所有】/【导出当前料号】
# 3、弹框新增元件库分类名称，点击是
# 4、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】
# 5、点击最上方的元件库 扩展 （元件库->芯片类型->封装类型->料号），查看导出的元件库料号，是否都显示
    utils.close_aoi()
    pass
@utils.screenshot_error_to_excel()
def yjk_001_17():
utils.check_and_launch_aoi()
    utils.check_export_image_libs(False)
#     1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
# 2、点击【菜单栏】--【元件库】--【导出所有】/【导出当前料号】
# 3、弹框新增元件库分类名称，点击是
# 4、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】
# 5、找到刚刚导出的元件库，扩展，双击料号，查看第一张图片
    utils.close_aoi()
    pass
@utils.screenshot_error_to_excel()
def yjk_001_18():
utils.check_and_launch_aoi()
    utils.check_export_image_libs(True)
#     1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
# 2、点击【菜单栏】--【元件库】--【导出所有】/【导出当前料号】
# 3、弹框新增元件库分类名称，点击是
# 4、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】
# 5、找到刚刚导出的元件库，扩展，双击料号，查看第一张图片
    utils.close_aoi()
    pass
@utils.screenshot_error_to_excel()
def yjk_001_19():
utils.check_and_launch_aoi()
    utils.check_export_pn_add_sn(False)
#     1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
# 2、点击【菜单栏】--【元件库】--【导出所有】
# 3、弹框新增元件库分类名称，点击是
# 4、编辑界面，点击【菜单栏】--【编辑】--【检测窗口】，多个元件，新增窗口
# 5、再次重复步骤2
# 6、弹框下拉框选步骤3 的分类名称，点击是
# 7、弹出是否覆盖弹框，点击所有
# 8、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】
# 9、找到刚刚导出的元件库，扩展，双击料号
# 10、查看第一张图片
# 1）导出时间是否是刚刚时间
# 2）下面的窗口 是否有刚刚新增的窗口
    utils.close_aoi()
    pass

@utils.screenshot_error_to_excel()
def yjk_001_20():
utils.check_and_launch_aoi()
    utils.check_export_pn_add_sn(False)
#     1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
# 2、点击【菜单栏】--【元件库】--【导出当前料号】
# 3、弹框新增元件库分类名称，点击是
# 4、编辑界面，点击【菜单栏】--【编辑】--【检测窗口】，任选一个元件新增窗口
# 5、再次重复步骤2
# 6、弹框下拉框选步骤3 的分类名称，点击是
# 7、是否覆盖弹框，点击是
# 8、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】
# 9、找到刚刚导出的元件库，扩展，双击料号
# 10、查看第一张图片
# 1）导出时间是否是刚刚时间
# 2）下面的窗口 是否有刚刚新增的窗口
    utils.close_aoi()
    pass

@utils.screenshot_error_to_excel()
def yjk_001_21():
utils.check_and_launch_aoi()
    utils.check_export_pn_add_sn(False)
#     1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
# 2、点击【菜单栏】--【元件库】--【导入所有】/【导出当前料号】
# 3、弹框新增元件库分类名称，点击是
# 4、编辑界面，点击【菜单栏】--【编辑】--【检测窗口】，新增窗口
# 5、再次重复步骤2
# 6、弹框下拉框选步骤3 的分类名称，点击是
# 7、是否弹出覆盖弹框
# 8、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】
# 9、找到刚刚导出的元件库，扩展，双击料号
# 10、查看第一张图片
# 1）导出时间是否是刚刚时间
# 2）下面的窗口 是否有刚刚新增的窗口
    utils.close_aoi()
    pass
@utils.screenshot_error_to_excel()
def yjk_001_22():
utils.check_and_launch_aoi()
    utils.check_export_pn_add_sn(True)
#     1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
# 2、点击【菜单栏】--【元件库】--【导出所有】
# 3、弹框新增元件库分类名称，点击是
# 4、编辑界面，点击【菜单栏】--【编辑】--【检测窗口】，多选几个元件新增窗口
# 5、再次重复步骤2
# 6、弹框下拉框选步骤3 的分类名称，点击是
# 7、是否弹出覆盖弹框
# 8、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】
# 9、找到刚刚导出的元件库，扩展，双击料号
# 10、查看第一张图片
# 1）导出时间是否是刚刚时间
# 2）下面的窗口 是否有刚刚新增的窗口
    utils.close_aoi()
    pass
@utils.screenshot_error_to_excel()
def yjk_001_23():
utils.check_and_launch_aoi()
    utils.check_export_pn_add_sn(True)
#     1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
# 2、点击【菜单栏】--【元件库】--【导出当前料号】
# 3、弹框新增元件库分类名称，点击是
# 4、编辑界面，点击【菜单栏】--【编辑】--【检测窗口】，任选一个元件 新增窗口
# 5、再次重复步骤2
# 6、弹框下拉框选步骤3 的分类名称，点击是
# 7、是否弹出覆盖弹框
# 8、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】
# 9、找到刚刚导出的元件库，扩展，双击料号
# 10、查看第一张图片
# 1）导出时间是否是刚刚时间
# 2）下面的窗口 是否有刚刚新增的窗口
    utils.close_aoi()
    pass
@utils.screenshot_error_to_excel()
def yjk_001_24():
utils.check_and_launch_aoi()
    utils.check_allow_preview(False)
#     1、主界面整板上，任选一个元件，双击元件进入【编辑界面】
# 2、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】
# 3、任选一个料号，点击图片
    utils.close_aoi()
    pass
@utils.screenshot_error_to_excel()
def yjk_001_25():
utils.check_and_launch_aoi()
    utils.check_allow_preview(True)
#     1、主界面整板上，任选一个元件，双击元件进入【编辑界面】
# 2、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】
# 3、任选一个料号，点击图片
    utils.close_aoi()
    pass

@utils.screenshot_error_to_excel()
def yjk_001_26():
utils.check_and_launch_aoi()
    utils.check_import_sync_package(False)
#     1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
# 2、右键 点击元件信息，修改封装类型成NULL
# 3、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】
# ，任意选一个料号 封装类型不是NONE，双击图片
# 4、右键 点击元件信息，查看封装类型
    utils.close_aoi()
    pass

@utils.screenshot_error_to_excel()
def yjk_001_27():
utils.check_and_launch_aoi()
    utils.check_import_sync_package(False)
#     1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
# 2、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】
# ，任意选一个料号 封装类型跟此元件不一样，双击图片
# 3、右键 点击元件信息，查看封装类型
    utils.close_aoi()
    pass
@utils.screenshot_error_to_excel()
def yjk_001_28():
utils.check_and_launch_aoi()
    utils.check_import_sync_package(True)
#     1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
# 2、上方菜单栏点击【元件库】--【手动选择】--【元件库视图】
# ，任意选一个料号 封装类型跟此元件不一样，双击图片
# 3、右键 点击元件信息，查看封装类型
    utils.close_aoi()
    pass
@utils.screenshot_error_to_excel()
def yjk_001_29():
utils.check_and_launch_aoi()
    utils.check_pn_1_day(True)
#     1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
# 2、编辑界面，点击【菜单栏】--【编辑】--【检测窗口】，任选一个元件 新增窗口
# 3、点击【菜单栏】--【元件库】--【导出所有】
# 4、弹框新增元件库类型，点击是，弹出可选择导出的料号
# 5、勾选所有，点击导出
    utils.close_aoi()
    pass
@utils.screenshot_error_to_excel()
def yjk_001_30():
utils.check_and_launch_aoi()
    utils.check_pn_1_day(True)
#     1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
# 2、编辑界面，点击【菜单栏】--【编辑】--【检测窗口】，任选一个元件 新增需要添加代料的窗口，添加2个代料
# 3、点击【菜单栏】--【元件库】--【导出当前料号】
# 4、弹框新增元件库类型，点击是
# 5、点击【菜单栏】--【元件库】--【导入当前料号】
# 6、查看步骤2添加的窗口代料是否是1
    utils.close_aoi()
    pass
@utils.screenshot_error_to_excel()
def yjk_001_31():
utils.check_and_launch_aoi()
    utils.check_pn_1_day(True)
#     1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
# 2、编辑界面，点击【菜单栏】--【编辑】--【检测窗口】，任选一个元件 新增需要添加代料的窗口，添加3个代料
# 3、点击【菜单栏】--【元件库】--【导出当前料号】
# 4、弹框新增元件库类型，点击是
# 5、点击【菜单栏】--【元件库】--【导入当前料号】
# 6、查看步骤2添加的窗口代料是否是3
    utils.close_aoi()
    pass
@utils.screenshot_error_to_excel()
def yjk_001_32():
utils.check_and_launch_aoi()
    utils.check_import_delete_ocv_wm(True)
#     1、主界面整板上，任选一个有字符检测待料的元件，双击进入元件编辑界面
# 2、菜单栏点击【导出当前料号】，弹框 新增分类名称，点击是
# 3、双击其他料号的元件，进入元件编辑界面
# 4、点击菜单栏--【元件库】--【手动选择】
# 5、查询步骤2 导出的料号，双击图片
# 6、查看字符检测待料图 是否有删除
    utils.close_aoi()
    pass
@utils.screenshot_error_to_excel()
def yjk_001_33():
utils.check_and_launch_aoi()
# 1、主界面整板上，任选一个有算法（编辑界面 左侧有元件窗口）的元件，双击元件进入【编辑界面】
# 2、右键点击【元件信息】--【标准】，修改xyh值
# 3、上方菜单栏点击【导出当前料号】/【导出所有】
# 4、弹框新增元件库类型，点击确认
# 5、上方菜单栏点击【手动选择】--【元件库视图】
# 6、找到导出的是哪个料号，点击图片，查看元件xyh值，进行对比
    utils.close_aoi()






    pass
@utils.screenshot_error_to_excel()
def yjk_001_34():
utils.check_and_launch_aoi()
    utils.check_allow_cad_teach(False)
    utils.check_import_update_height(True)
#     1、主界面整板上，任选一个没有方形定位算法的元件，双击元件进入【编辑界面】
# 2、点击【菜单栏】--【元件库】--【导出当前料号】
# 3、弹框新增元件库类型，点击确认
# 4、右键点击【元件信息】--【标准】，修改h值
# 5、导入 刚刚导出的料号，对比h值
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def yjk_001_35():
utils.check_and_launch_aoi()
    utils.check_allow_cad_teach(False)
    utils.check_import_update_height(False)
# 1、主界面整板上，任选一个没有方形定位算法的元件，双击元件进入【编辑界面】
# 2、点击【菜单栏】--【元件库】--【导出当前料号】
# 3、弹框新增元件库类型，点击确认
# 4、右键点击【元件信息】--【标准】，修改h值
# 5、点击【菜单栏】--【元件库】--【导出当前料号】，弹框选步骤3的元件库类型，对比h值
    utils.close_aoi()


@utils.screenshot_error_to_excel()
def yjk_001_36():
utils.check_and_launch_aoi()
    utils.check_allow_cad_teach(False)
    # 不管这边选啥 都对结果没影响。也就是说要验证两次h值
    # utils.check_import_update_height(False)
#     1、主界面整板上，任选一个有方形定位算法的元件，双击元件进入【编辑界面】
# 2、点击【菜单栏】--【元件库】--【导出当前料号】
# 3、弹框新增元件库类型，点击确认
# 4、右键点击【元件信息】--【标准】，修改h值
# 5、点击【菜单栏】--【元件库】--【导出当前料号】，弹框选步骤3的元件库类型，对比h值
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def yjk_001_37():
utils.check_and_launch_aoi()
    utils.check_allow_cad_teach(False)
    utils.check_import_component_xy(False)
    utils.check_standard_xyh(False)
#     1、主界面整板上，任选一个没有方形定位算法的元件，双击元件进入【编辑界面】
# 2、点击【菜单栏】--【元件库】--【导出当前料号】
# 3、弹框新增元件库类型，点击确认
# 4、右键点击【元件信息】--【标准】，修改xy值
# 5、点击【菜单栏】--【元件库】--【导出当前料号】，弹框选步骤3的元件库类型
# 6、右键点击元件信息，查看标准xy
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def yjk_001_38():
    utils.check_and_launch_aoi()
    utils.ensure_in_edit_mode()
    utils.check_allow_cad_teach(False)
    time.sleep(3)
    utils.check_import_component_xy(True)
    time.sleep(3)
    utils.check_standard_xyh(False)
    time.sleep(3)
#     1、主界面整板上，任选一个没有方形定位算法的元件，双击元件进入【编辑界面】
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
# 2、点击【菜单栏】--【元件库】--【导出当前料号】
# 3、弹框新增元件库类型，点击确认
# 4、右键点击【元件信息】--【标准】，修改xy值
# 5、点击【菜单栏】--【元件库】--【导出当前料号】，弹框选步骤3的元件库类型
# 6、右键点击元件信息，查看标准xy
    utils.close_aoi()


@utils.screenshot_error_to_excel()
def yjk_001_39():
    utils.check_and_launch_aoi()
    utils.check_standard_xyh(True)
    utils.check_allow_cad_teach(False)
    utils.check_import_component_xy(True)
    utils.check_import_update_height(True)
    # 1、主界面整板上，任选一个有算法的元件，双击元件进入【编辑界面】
    utils.ensure_in_edit_mode()
    # 2、点击【菜单栏】--【元件库】--【导出当前料号】
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.EXPORT_CURRENT_PN)
    # 3、弹框新增元件库类型，点击确认
    # 4、右键点击【元件信息】--【标准】，修改xyh值
    pyautogui.rightClick(config.CENTRE)
    utils.click_by_png(config.COMPONENT_INFORMATION)

    # 5、点击【菜单栏】--【元件库】--【导入当前料号】，弹框选步骤3的元件库类型
    # 6、右键点击元件信息，查看标准xyh
    utils.close_aoi()

@utils.screenshot_error_to_excel()
def yjk_001_40():
    utils.check_and_launch_aoi()
    utils.filter_auxiliary_window(True)
    # 1、选任一元件，双击进入【编辑界面】
    utils.ensure_in_edit_mode()
    # 2、新增3d基准面、板弯补偿算法，导出此料号
    utils.add_window()
    utils.click_by_png(config.REFERENCE_PLANE_3D)
    utils.click_by_png(config.YES)
    time.sleep(5)
    utils.add_window()
    utils.click_by_png(config.PLATE_BENDING_COMPENSATION)
    utils.click_by_png(config.SQUARE_POSITIONING)
    utils.click_by_png(config.YES)
    time.sleep(5)
    # 导出当前料号
    utils.search_symbol_erroring(config.ELEMENTS)
    utils.click_by_png(config.EXPORT_CURRENT_PN)
    utils.click_by_png(config.YES)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    # 3、清空算法，导入 刚导出的料号
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(2)
    utils.click_by_png(config.IMPORT_CURRENT_PN)
    # 4、删除重添加或编辑 3d基准面、板弯补偿算法，导入 刚导出的料号

    # 5、删除3d基准面、板弯补偿算法，导入 刚导出的料号

    utils.close_aoi()
# # TODO 需要在线aoi
# @utils.screenshot_error_to_excel()
# def yjk_001_41():
    # 1、新建job，弹出 是否导入默认库弹框，点击是
    # 2、查看主界面导入的元件 是否是所选的元件库
    # 3、重新改变 下拉框选择任一元件库【设置】--【数据导出配置】--【元件库设置】--【默认】
    # 4、选任一元件，双击进入【编辑界面】
    # utils.ensure_in_edit_mode()
    # 5、点击菜单栏-【元件库】-【导出当前料号】/【导出所有】/【导入当前料号】/【导入所有】，弹出的框 ，显示的元件库名称 是步骤3所选择的
    # pass
# @utils.screenshot_error_to_excel()
# def yjk_001_42():
#     # 1、输入百分比值【设置】--【硬件设置】--【数据导出配置】--【元件库】--【导入筛选限制】
#     utils.check_and_launch_aoi()
#     utils.check_import_filtering_restriction("80")
#     # 2、主界面整板上，任选一个元件，双击元件进入【编辑界面】
#     utils.ensure_in_edit_mode()
#     time.sleep(2)
#     # 3、点击菜单栏【元件库】--【手动选择】，宽度高度是当前元件的xy尺寸
#     utils.click_by_png(config.ELEMENTS)
#     utils.click_by_png(config.MANUAL_SELECT)
#     time.sleep(2)
#     # 4、随机点击芯片类型
#     utils.click_by_png(config.CHIP_TYPE, 2, instance=2)
#     time.sleep(2)
#     a = utils.check_chip_coverage((203,203,203), config.CHIP_SCROLLBAR_REGION)
#     # 5、重复步骤1、步骤4 TODO 一个看不出来 要遍历
#     utils.check_import_filtering_restriction("20")
#     utils.click_by_png(config.CHIP_TYPE, 2, instance=2)
#     time.sleep(2)
#     b = utils.check_chip_coverage((203,203,203), config.CHIP_SCROLLBAR_REGION)
#     if a > b:
#         logger.info("百分比值越小，限制越多")
#     else:
#         raise Exception("不符合：百分比值越小，限制越多")
#     utils.close_aoi()

# 不勾共享元件库路径
@utils.screenshot_error_to_excel()
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
    utils.close_aoi()
# 不勾共享元件库路径
@utils.screenshot_error_to_excel()
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
    utils.close_aoi()

# 勾共享元件库路径
@utils.screenshot_error_to_excel()
def yjk_001_45():
    utils.check_and_launch_aoi()
    utils.check_share_lib_path(True)
    utils.check_default_export_auto_save(True, False)
    utils.ensure_in_edit_mode()
    # 公共文件库默认一样的，删除库内所有数据
    utils.delete_documents(config.SHARE_LIB_PATH)
    # 修改元件，左侧列表切换元件，弹框点击是
    utils.modify_component()
    utils.click_by_png(config.SAVE)
    time.sleep(1)
    logger.error("第一次检测勾选框")
    utils.search_symbol_erroring(config.EXPORT_PUBLIC_PROGRAM_CHECKED)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(5)
    utils.modify_component()
    utils.click_component()
    time.sleep(1)
    pyautogui.press("enter")
    utils.click_by_png(config.SAVE)
    # 再次确认默认勾选（切换元件后点击保存）
    logger.error("第二次检测勾选框")
    utils.search_symbol_erroring(config.EXPORT_PUBLIC_PROGRAM_CHECKED)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(5)
    # 最后确认默认勾选（点击返回）
    utils.modify_component()
    if utils.search_symbol(config.EDIT_DARK, 3):
        utils.click_by_png(config.EDIT_DARK)
    else:
        utils.search_symbol_erroring(config.EDIT_LIGHT)
    utils.click_by_png(config.EDIT_BACK)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(3)
    utils.click_by_png(config.SAVE)
    logger.error("第三次检测勾选框")
    utils.search_symbol_erroring(config.EXPORT_PUBLIC_PROGRAM_CHECKED)
    time.sleep(1)
    pyautogui.press("enter")
    if utils.check_new_data(config.SHARE_LIB_PATH):
        logger.info("共享元件库文件夹内有新数据生成")
    else:
        raise Exception("共享元件库文件夹内没有新数据生成")
    utils.close_aoi()


# 勾共享元件库路径
@utils.screenshot_error_to_excel()
def yjk_001_46():
    utils.check_and_launch_aoi()
    utils.check_share_lib_path(True)
    utils.check_default_export_auto_save(False, False)
    utils.delete_documents(config.SHARE_LIB_PATH)
    utils.ensure_in_edit_mode()
    # 修改元件
    time.sleep(8)
    # 第一次进入会直接选中，不需要按b了
    for _ in range(6):
        pyautogui.press('down')
        time.sleep(0.5)
    # utils.modify_component()
    utils.click_by_png(config.SAVE)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    logger.info("第一次检测未勾选框")
    utils.search_symbol_erroring(config.EXPORT_PUBLIC_PROGRAM_GRAY)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(8)
    # 修改元件，左侧列表切换元件，再次确定
    for _ in range(6):
        pyautogui.press('down')
        time.sleep(0.5)
    utils.click_component()
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(8)
    utils.click_by_png(config.SAVE)
    logger.info("第二次检测未勾选框")
    time.sleep(1)
    utils.search_symbol_erroring(config.EXPORT_PUBLIC_PROGRAM_GRAY)
    pyautogui.press("enter")
    time.sleep(8)
    # 修改元件，点击返回
    for _ in range(6):
        pyautogui.press('down')
        time.sleep(0.5)
    utils.click_by_png(config.EDIT_BACK)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    utils.click_by_png(config.SAVE)
    time.sleep(1)
    logger.info("第三次检测未勾选框")
    utils.search_symbol_erroring(config.EXPORT_PUBLIC_PROGRAM_GRAY)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(5)
    # 傻逼用例描述 他妈的明明都是置灰无法勾选
    utils.click_by_png(config.TOOL_DARK)
    utils.click_by_png(config.SYNC_TO_PUBLIC_LIBS)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    if utils.check_new_data(config.SHARE_LIB_PATH):
        logger.info("共享元件库文件夹内有新数据生成")
    else:
        raise Exception("共享元件库文件夹内没有新数据生成")
    utils.close_aoi()


@utils.screenshot_error_to_excel()
def yjk_001_47():
    utils.check_and_launch_aoi()
    utils.check_share_lib_path(True)
    utils.check_default_export_auto_save(True, True)
    utils.ensure_in_edit_mode()
    utils.delete_documents(config.SHARE_LIB_PATH)
    # 修改元件 保存 是
    utils.modify_component()
    utils.click_by_png(config.SAVE)
    time.sleep(1)
    pyautogui.press("enter")
    # 修改元件 返回 是 保存 是
    time.sleep(3)
    utils.modify_component()
    utils.click_by_png(config.EDIT_BACK)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(3)
    utils.click_by_png(config.SAVE)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    # 傻逼用例描述
    utils.click_by_png(config.TOOL_DARK)
    utils.click_by_png(config.SYNC_TO_PUBLIC_LIBS)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    if utils.check_new_data(config.SHARE_LIB_PATH):
        logger.info("共享元件库文件夹内有新数据生成")
    else:
        raise Exception("共享元件库文件夹内没有新数据生成")
    utils.close_aoi()


# 勾共享元件库路径-最近编辑的样式
@utils.screenshot_error_to_excel()
def yjk_001_48():
    utils.check_and_launch_aoi()
    utils.check_share_lib_path(True)
    utils.check_default_export_auto_save(False, True)
    utils.delete_documents(config.SHARE_LIB_PATH)
    utils.ensure_in_edit_mode()
    # 修改元件，点击保存，手动勾选导出到公共元件库
    for _ in range(6):
        pyautogui.press('down')
        time.sleep(0.5)
    utils.click_by_png(config.SAVE)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    utils.click_by_png(config.TOOL_DARK)
    time.sleep(1)
    utils.click_by_png(config.SYNC_TO_PUBLIC_LIBS)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(3)
    # 修改元件，切换元件，是，保存，手动勾选
    for _ in range(6):
        pyautogui.press('down')
        time.sleep(0.5)
    logger.error(2)
    utils.click_component()
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(3)
    utils.click_by_png(config.SAVE)
    time.sleep(1)
    utils.click_by_png(config.EXPORT_PUBLIC_PROGRAM)
    time.sleep(1)
    pyautogui.press("enter")
    # 修改元件，返回 是 保存 勾选
    for _ in range(6):
        pyautogui.press('down')
        time.sleep(0.5)
    logger.error(3)
    utils.click_by_png(config.EDIT_DARK)
    utils.click_by_png(config.EDIT_BACK)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(3)
    utils.click_by_png(config.SAVE)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    utils.click_by_png(config.TOOL_DARK)
    time.sleep(1)
    # 傻逼用例描述
    utils.click_by_png(config.SYNC_TO_PUBLIC_LIBS)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    if utils.check_new_data(config.SHARE_LIB_PATH):
        logger.info("共享元件库文件夹内有新数据生成")
    else:
        raise Exception("共享元件库文件夹内没有新数据生成")
    utils.close_aoi()



# 勾共享元件库路径
@utils.screenshot_error_to_excel()
def yjk_001_49():
    utils.check_and_launch_aoi()
    utils.check_share_lib_path(True)
    utils.delete_documents(config.SHARE_LIB_PATH)
    # 打开任一job,同步至公共元件库
    utils.open_program()
    pyautogui.press('enter')
    time.sleep(5)
    if utils.search_symbol(config.TOOL_DARK, 5):
        utils.click_by_png(config.TOOL_DARK)
    utils.click_by_png(config.SYNC_TO_PUBLIC_LIBS)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    pyautogui.press("enter")
    # 打开更早编辑的程式
    for i in range(2):
        utils.click_by_png(config.OPEN_PROGRAM)
        utils.click_by_png(config.OPEN_PROGRAM_RECENT)
        if i == 0:
            pyautogui.press('tab',6)
        if i == 1:
            pyautogui.press('tab',8)
        utils.click_by_png(config.OPEN_PROGRAM_CHOSED)
        utils.click_by_png(config.OPEN_PROGRAM_LOAD)
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
        utils.click_by_png(config.YES)
        logger.error(i)
        # 否，检测是否生成新数据
        utils.click_by_png(config.IF_SYNC_PART_NO)
        if i == 0:
            pyautogui.press("left")
            pyautogui.press("enter")
            logger.error(2)
            while utils.search_symbol(config.PROGRAM_LOADING):
                time.sleep(5)
            if not utils.check_new_data(config.SHARE_LIB_PATH):
                logger.info("共享元件库文件夹内没有新数据生成")
            else:
                raise Exception("共享元件库文件夹内有新数据生成")

        if i == 1:
            logger.error(3)
            pyautogui.press("enter")
            while utils.search_symbol(config.PROGRAM_LOADING):
                time.sleep(5)
            if utils.check_new_data(config.SHARE_LIB_PATH):
                logger.info("共享元件库文件夹内有新数据生成")
            else:
                raise Exception("共享元件库文件夹内没有新数据生成")
            utils.close_aoi()


@utils.screenshot_error_to_excel()
def yjk_001_50():
    utils.check_and_launch_aoi()
    utils.check_share_lib_path(True)
    utils.delete_documents(config.SHARE_LIB_PATH)
    # 先打开任一job，同步到公共元件库
    utils.ensure_in_edit_mode()
    utils.click_by_png(config.TOOL)
    utils.click_by_png(config.SYNC_TO_PUBLIC_LIBS)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    pyautogui.press("enter")
    # 再打开最近编辑的程式
    utils.click_by_png(config.OPEN_PROGRAM)
    pyautogui.press('enter')
    utils.click_by_png(config.OPEN_PROGRAM_RECENT)
    time.sleep(1)
    pyautogui.press('tab',4)
    utils.click_by_png(config.OPEN_PROGRAM_CHOSED)
    utils.click_by_png(config.OPEN_PROGRAM_LOAD, 2)
    utils.click_by_png(config.YES)
    # 检测是否生成新数据
    if utils.search_symbol(config.IF_SYNC_PART_NO):
        logger.info("有弹框")
    else:
        raise Exception("没有弹框")
    time.sleep(1)
    pyautogui.press("enter")
    if utils.check_new_data(config.SHARE_LIB_PATH):
        logger.info("共享元件库文件夹内有新数据生成")
    else:
        raise Exception("共享元件库文件夹内没有新数据生成")
    utils.close_aoi()


@utils.screenshot_error_to_excel()
def yjk_001_51():
    utils.check_and_launch_aoi()
    utils.check_share_lib_path(True)
    utils.delete_documents(config.SHARE_LIB_PATH)
    utils.ensure_in_edit_mode()
    utils.click_by_png(config.ELEMENTS)
    utils.click_by_png(config.ELEMENTS_IMPORT_ALL)
    time.sleep(3)
    pyautogui.click((945, 525))
    utils.click_by_png(config.PUBLIC_ELEMENTS)
    pyautogui.press('enter')
    utils.search_symbol_erroring(config.IMPORTING_ELEMENTS)
    utils.close_aoi()


# 测试=============================
# # TODO 需要在线版才可以
# @utils.screenshot_error_to_excel()
# def yjk_001_52():
#     pass
