import os
import random
import pyperclip
import utils
import time
import pyautogui
import config
from loguru import logger

# @utils.screenshot_error_to_excel()
# def zxtc_001_01():
#     utils.check_and_launch_aoi()
#     # 1、打开二轨【运行】Tab页，打开【在线调参】开关
#     utils.open_tab(config.TAB_RUN, track=2)
#     utils.toggle_switch(config.ONLINE_TUNING_SWITCH, track=2)
#     # 2、二轨运行测试一次
#     utils.run_test(track=2)

# @utils.screenshot_error_to_excel()
# def zxtc_002_01():
#     utils.check_and_launch_aoi()
#     # 1、打开一轨、二轨【运行】Tab页，分别打开【在线调参】开关
#     utils.open_tab(config.TAB_RUN, track=1)
#     utils.toggle_switch(config.ONLINE_TUNING_SWITCH, track=1)
#     utils.open_tab(config.TAB_RUN, track=2)
#     utils.toggle_switch(config.ONLINE_TUNING_SWITCH, track=2)
#     # 2、一轨、二轨分别运行测试一次
#     utils.run_test(track=1)
#     utils.run_test(track=2)
#     # 3、打开一轨【运行】Tab页--【在线调参】
#     utils.open_tab(config.TAB_RUN, track=1)
#     utils.open_online_tuning(track=1)
#     # 4、在【ONLINE PROGARMING】在线调参界面，同时打开一轨、二轨测试的job
#     utils.open_job_in_online_tuning(track=1)
#     utils.open_job_in_online_tuning(track=2)

# @utils.screenshot_error_to_excel()
# def zxtc_002_02():
#     utils.check_and_launch_aoi()
#     # 1、打开一轨、二轨【运行】Tab页，分别打开【在线调参】开关
#     utils.open_tab(config.TAB_RUN, track=1)
#     utils.toggle_switch(config.ONLINE_TUNING_SWITCH, track=1)
#     utils.open_tab(config.TAB_RUN, track=2)
#     utils.toggle_switch(config.ONLINE_TUNING_SWITCH, track=2)
#     # 2、打开一轨【运行】Tab页--【在线调参】
#     utils.open_tab(config.TAB_RUN, track=1)
#     utils.open_online_tuning(track=1)
#     # 3、在【ONLINE PROGARMING】在线调参界面，同时打开一轨、二轨测试的job
#     utils.open_job_in_online_tuning(track=1)
#     utils.open_job_in_online_tuning(track=2)
#     # 4、一轨、二轨运行测试一次，等待导出数据完成
#     utils.run_test(track=1)
#     utils.run_test(track=2)
#     utils.wait_for_data_export()
#     # 5、在线调参界面点击【整板信息】中的“下载“图标
#     utils.click_download_icon_in_board_info()

# @utils.screenshot_error_to_excel()
# def zxtc_003_01():
#     utils.check_and_launch_aoi()
#     # 1、参考ZXTC-002案例，左侧列表已经加载了元件
#     utils.load_components_list()
#     # 2、选中任一元件，双击元件
#     utils.select_and_double_click_component()
#     # 3、修改算法参数、调整检测框位置等，切换同一料号元件
#     utils.modify_algorithm_parameters()
#     utils.adjust_detection_box()
#     utils.switch_to_same_package_component()

# @utils.screenshot_error_to_excel()
# def zxtc_004_01():
#     utils.check_and_launch_aoi()
#     # 1、参考ZXTC-003-01案例，元件参数已经修改
#     utils.modify_component_parameters()
#     # 2、点击【整板信息】中的“上传“图标，弹出【确认同步到运行的程式？】
#     utils.click_upload_icon_in_board_info()
#     # 3、点击【否】
#     utils.click_no_in_confirmation_dialog()
#     # 4、点击【是】
#     utils.click_yes_in_confirmation_dialog()

# @utils.screenshot_error_to_excel()
# def zxtc_004_02():
#     utils.check_and_launch_aoi()
#     # 1、参考ZXTC-003-01案例，任意修改元件参数
#     utils.modify_component_parameters()
#     # 2、点击【整板信息】中的“上传“图标，弹出【确认同步到运行的程式？】，并点击【是】
#     utils.click_upload_icon_in_board_info()
#     utils.click_yes_in_confirmation_dialog()
#     # 3、开Ngbuffer或手动将板抽出，再放入进板口
#     utils.open_ngbuffer_or_manual_board_removal()
#     # 4、在线调参界面点击【整板信息】中的“下载“图标
#     utils.click_download_icon_in_board_info()
#     # 5、找到刚刚修改的料号元件，查看刚刚修改的参数，查看3D算法
#     utils.find_and_check_modified_component_parameters()
#     utils.check_3d_algorithm()
#     # 6、测试窗口、元件
#     utils.test_window_and_component()

# @utils.screenshot_error_to_excel()
# def zxtc_004_03():
#     utils.check_and_launch_aoi()
#     # 1、参考ZXTC-003-01案例，元件参数已经修改
#     utils.modify_component_parameters()
#     # 2、点击【整板信息】中的“上传“图标，弹出【确认同步到运行的程式？】
#     utils.click_upload_icon_in_board_info()
#     # 3、点击【是】
#     utils.click_yes_in_confirmation_dialog()
#     # 4、确认UI从【正在同步程式】到拍mark点的时间要多久
#     utils.confirm_ui_sync_time()

# @utils.screenshot_error_to_excel()
# def zxtc_005_01():
#     utils.check_and_launch_aoi()
#     # 1、参考ZXTC-002案例，左侧列表已经加载了元件
#     utils.load_components_list()
#     # 2、按快捷键打开DJB
#     utils.open_djb_with_shortcut()
#     # 3、点击【整板信息】中的“下载“图标
#     utils.click_download_icon_in_board_info()

# @utils.screenshot_error_to_excel()
# def zxtc_005_02():
#     utils.check_and_launch_aoi()
#     # 1、在操作ZXTC-001~ZXTC-004的案例时，正常测试，切换元件，修改参数，移动位置等
#     utils.perform_normal_test_and_modify_parameters()

@utils.screenshot_error_to_excel()
def zxtc_005_03():
    utils.check_and_launch_aoi()
    utils.shortcut_key_online_parameter_display_sync_package()
    # 1、接ZXTC-005-02，对料号A任一元件修改参数或移动位置后，按快捷键K
    utils.modify_component_parameters_or_move_position()
    utils.press_shortcut_key_k()
    # 2、点击【是】
    utils.click_yes_in_confirmation_dialog()
    # 3、切换到另一料号B
    utils.switch_to_another_package_b()

# @utils.screenshot_error_to_excel()
# def zxtc_006_01():
#     utils.check_and_launch_aoi()
#     # 1、在操作ZXTC-001~ZXTC-005的案例时，正常测试，切换元件，修改参数，移动位置、打开djb等
#     utils.perform_normal_test_and_modify_parameters()
#     # 2、快捷键快速切换元件、窗口等
#     utils.quick_switch_components_and_windows_with_shortcut()

# @utils.screenshot_error_to_excel()
# def zxtc_007_01():
#     utils.check_and_launch_aoi()
#     # 1、参考ZXTC-001或ZXTC-002案列，测试数据后，在在线调参界面加载出来
#     utils.load_test_data_in_online_tuning()
#     # 2、切换不同元件不同窗口，测试窗口
#     utils.switch_and_test_different_components_and_windows()

# @utils.screenshot_error_to_excel()
# def zxtc_008_01():
    # utils.check_and_launch_aoi()
    # utils.param_keep_the_last_pcb_number()
#     # 1、参数设置--数据导出配置--在线调参，只勾选【允许循环覆盖】
#     utils.set_data_export_configuration(allow_loop_overwrite=True)
#     # 2、循环运行job
#     utils.loop_run_job()
#     # 3、在【ONLINE PROGARMING】在线调参界面，打开刚刚运行过的job
#     utils.open_recently_run_job_in_online_tuning()
#     # 4、循环运行job
#     utils.loop_run_job()

# @utils.screenshot_error_to_excel()
# def zxtc_008_02():
#     utils.check_and_launch_aoi()
    # utils.param_keep_the_last_pcb_number()
#     # 1、参数设置--数据导出配置--在线调参，不勾选【允许循环覆盖】
#     utils.set_data_export_configuration(allow_loop_overwrite=False)
#     # 2、循环运行job
#     utils.loop_run_job()
#     # 3、在【ONLINE PROGARMING】在线调参界面，打开刚刚运行过的job
#     utils.open_recently_run_job_in_online_tuning()
#     # 4、循环运行job
#     utils.loop_run_job()

# @utils.screenshot_error_to_excel()
# def zxtc_008_03():
#     utils.check_and_launch_aoi()
    # utils.param_keep_the_last_pcb_number()
#     # 1、勾选【在线编辑时不导出】
#     utils.set_online_edit_not_export(True)
#     # 2、运行测试
#     utils.run_test()

# @utils.screenshot_error_to_excel()
# def zxtc_008_04():
#     utils.check_and_launch_aoi()
    # utils.param_keep_the_last_pcb_number()
#     # 1、不勾选【在线编辑时不导出】
#     utils.set_online_edit_not_export(False)
#     # 2、运行测试
#     utils.run_test()

# @utils.screenshot_error_to_excel()
# def zxtc_009_01():
#     utils.check_and_launch_aoi()
#     utils.param_good_and_ng_component_limits(3, 3)
#     # 1、对【Good元件】、【NG元件】对应的【数量限制】输入X、Y
#     # 2、运行测试
#     utils.run_test()

# @utils.screenshot_error_to_excel()
# def zxtc_009_02():
#     utils.check_and_launch_aoi()
#     # 1、对【Good元件】、【NG元件】对应的【数量限制】勾选【所有】TODO
    # utils.param_good_and_ng_component_limits()
#     # 2、运行测试
#     utils.run_test()

# @utils.screenshot_error_to_excel()
# def zxtc_009_03():
#     utils.check_and_launch_aoi()
#     # 1、在【ONLINE PROGARMING】在线调参界面，打开已运行过的job
#     utils.open_recently_run_job_in_online_tuning()
#     # 2、通过右上角关闭【ONLINE PROGARMING】在线调参界面
#     utils.close_online_tuning_interface()

@utils.screenshot_error_to_excel()
def zxtc_010_01():
    utils.check_and_launch_aoi()
    utils.open_program()
    utils.click_by_png(config.FOV)
    if utils.search_symbol(config.FOV_BAD_MARK_FOV_FIRST_NO,2):
        utils.click_by_png(config.FOV_BAD_MARK_FOV_FIRST_NO,timeout=2)
    utils.click_by_png(config.YES)
    # 1、对【Good元件】、【NG元件】对应的【数量限制】输入X、Y
    utils.set_good_and_ng_component_limits(x, y)
    # 2、运行测试
    utils.run_test()
    # 3、有badmark的拼板忽略，查看job目录下【OffProgData】中的djb数量
    utils.check_djb_count(ignore_badmark=True)

@utils.screenshot_error_to_excel()
def zxtc_010_02():
    utils.check_and_launch_aoi()
    utils.open_program()
    utils.click_by_png(config.FOV)
    if utils.search_symbol(config.FOV_BAD_MARK_FOV_FIRST_YES,2):
        utils.click_by_png(config.FOV_BAD_MARK_FOV_FIRST_YES,timeout=2)
    utils.click_by_png(config.YES)
    # 1、对【Good元件】、【NG元件】对应的【数量限制】输入X、Y
    utils.set_good_and_ng_component_limits(x, y)
    # 2、运行测试
    utils.run_test()
    # 3、有badmark的拼板忽略，查看job目录下【OffProgData】中的djb数量
    utils.check_djb_count(ignore_badmark=True)

@utils.screenshot_error_to_excel()
def zxtc_010_03():
    utils.check_and_launch_aoi()
    utils.open_program()
    utils.click_by_png(config.FOV)
    if utils.search_symbol(config.FOV_BAD_MARK_FOV_FIRST_NO,2):
        utils.click_by_png(config.FOV_BAD_MARK_FOV_FIRST_NO,timeout=2)
    utils.click_by_png(config.YES)
    # 1、对【Good元件】、【NG元件】对应的【数量限制】输入X、Y
    utils.set_good_and_ng_component_limits(x, y)
    # 2、运行测试
    utils.run_test()
    # 3、有设置元件缺陷坏板标记的拼板忽略，查看job目录下【OffProgData】中的djb数量
    utils.check_djb_count(ignore_defect_badmark=True)

@utils.screenshot_error_to_excel()
def zxtc_010_04():
    utils.check_and_launch_aoi()
    utils.open_program()
    utils.click_by_png(config.FOV)
    if utils.search_symbol(config.FOV_BAD_MARK_FOV_FIRST_YES,2):
        utils.click_by_png(config.FOV_BAD_MARK_FOV_FIRST_YES,timeout=2)
    utils.click_by_png(config.YES)
    # 1、对【Good元件】、【NG元件】对应的【数量限制】输入X、Y
    utils.set_good_and_ng_component_limits(x, y)
    # 2、运行测试
    utils.run_test()
    # 3、有设置元件缺陷坏板标记的拼板忽略，查看job目录下【OffProgData】中的djb数量
    utils.check_djb_count(ignore_defect_badmark=True)

# @utils.screenshot_error_to_excel()
# def zxtc_011_01():
#     utils.check_and_launch_aoi()
#     # 1、在线调参界面，下载数据
#     utils.download_data_in_online_tuning()
#     # 2、双击任一元件，点击上传，弹框点是
#     utils.double_click_component_and_upload(confirm=True)
#     # 3、查看列表数据 和job目录下【OffProgData】中下载的数据
#     utils.check_list_data_and_offprogdata()

# @utils.screenshot_error_to_excel()
# def zxtc_011_02():
#     utils.check_and_launch_aoi()
#     # 1、在线调参界面，下载数据
#     utils.download_data_in_online_tuning()
#     # 2、双击任一元件，修改元件，点击上传，弹框点是
#     utils.double_click_component_modify_and_upload(confirm=True)
#     # 3、查看列表数据 和job目录下【OffProgData】中下载的数据
#     utils.check_list_data_and_offprogdata()

# @utils.screenshot_error_to_excel()
# def zxtc_011_03():
#     utils.check_and_launch_aoi()
#     # 1、在线调参界面，下载数据
#     utils.download_data_in_online_tuning()
#     # 2、点击界面的删除按钮
#     utils.click_delete_button()
#     # 3、查看列表数据 和job目录下【OffProgData】中下载的数据
#     utils.check_list_data_and_offprogdata()

# @utils.screenshot_error_to_excel()
# def zxtc_011_04():
#     utils.check_and_launch_aoi()
#     # 1、在线调参界面，下载数据
#     utils.download_data_in_online_tuning()
#     # 2、选中任一元件，双击元件
#     utils.double_click_component()
#     # 3、修改算法参数，点击测试分组
#     utils.modify_algorithm_parameters_and_test_group()
#     # 4、点击【整板信息】中的“上传“图标，弹出【确认同步到运行的程式？】
#     utils.click_upload_icon_in_board_info()
#     # 5、点击【是】
#     utils.confirm_sync_to_running_program()
#     # 6、在线测试一笔
#     utils.run_online_test()
#     # 7、在线调参界面，下载数据，查看步骤2的元件是否已修改
#     utils.download_data_in_online_tuning()
#     utils.check_component_modification()