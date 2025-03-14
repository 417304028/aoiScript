import config
import utils


@utils.screenshot_error_to_excel()
def zdbj_001_01():
    utils.check_and_launch_aoi()
    # 1、打开任一未压缩的job
    # 2、job内含有cad
    utils.open_program(1)
    # 3、点击【板】--【自动编程】
    if utils.search_symbol(config.BOARD_DARK):
        utils.click_by_png(config.BOARD_DARK)
    else:
        utils.click_by_png(config.BOARD_LIGHT)
    utils.click_by_png(config.BOARD_AUTO)
    # 4、点击【是】
    # 5、弹出【是否要自动导入默认元件库？】，点击【是】
@utils.screenshot_error_to_excel()    
def zdbj_001_02():
    utils.check_and_launch_aoi()
    # 1、打开任一未压缩的job
    # 2、job内含有cad
    # 3、点击【板】--【自动编程】
    if utils.search_symbol(config.BOARD_DARK):
        utils.click_by_png(config.BOARD_DARK)
    else:
        utils.click_by_png(config.BOARD_LIGHT)
    utils.click_by_png(config.BOARD_AUTO)
    # 4、点击【是】
    # 5、弹出【是否要自动导入默认元件库？】，点击【否】
@utils.screenshot_error_to_excel()
def zdbj_001_03():
    utils.check_and_launch_aoi()
    # 1、打开任一未压缩的job
    # 2、job内含有cad
    # 3、点击【板】--【自动编程】
    if utils.search_symbol(config.BOARD_DARK):
        utils.click_by_png(config.BOARD_DARK)
    else:
        utils.click_by_png(config.BOARD_LIGHT)
    utils.click_by_png(config.BOARD_AUTO)
    # 4、弹出【是否开始自动编程】，点击【是】
    # 5、点击【取消】
@utils.screenshot_error_to_excel()
def zdbj_001_04():
    utils.check_and_launch_aoi()
    # 1.【打开】任一job
    # 2.【设置】--【硬件设置】--【快捷键设置】，查看缺陷试图界面的快捷键
    # 3.【运行】该程式
    # 4.弹出dv复判界面，在dv复判界面，使用快捷键