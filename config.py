import sys
import os


def resource_path(relative_path):
    """ 获取资源的绝对路径，用于访问打包后的资源文件 """
    try:
        # PyInstaller创建的临时文件夹
        base_path = sys._MEIPASS
    except Exception:
        # 如果没有使用PyInstaller打包，使用当前文件夹
        base_path = os.path.abspath(".")

        # 构建完整的文件路径
    full_path = os.path.join(base_path, relative_path)

    # 获取文件所在的目录路径
    directory = os.path.dirname(full_path)

    # 如果目录不存在，则创建它
    if not os.path.exists(directory):
        os.makedirs(directory)

    return full_path


# AOI路径
AOI_EXE_PATH = r'D:\EYAOI\Bin\AOI.exe'
# SPC路径
SPC_EXE_PATH = r'D:\EYAOI\AOI_SPC\SPCViewMain.exe'
# RV路径
RV_EXE_PATH = r'D:\EYAOI\AOI_RV\DVPro.UI.exe'
# job路径
JOB_PATH = r'D:\EYAOI\JOB\djb'
# SPC用户名
SPC_USER_NAME = "sinictek"
# SPC密码
SPC_PASSWORD, RV_PASSWORD_TEXT = "000", "000"

SPC_TOPIC = resource_path('images/spc/topic.png')
SPC_TASKBAR = resource_path('images/spc/taskbar.png')
SPC_PROGRAM_VIEW = resource_path('images/spc/system/program_view.png')
SPC_DEFECT_STATISTICS = resource_path('images/spc/system/defect_statistics.png')
SPC_YIELD_ANALYSIS = resource_path('images/spc/system/yield_analysis.png')
SPC_DATA_EXPORT = resource_path('images/spc/system/data_export.png')
SPC_SYSTEM_SETTING = resource_path('images/spc/system/system_setting.png')
SPC_QUERY = resource_path('images/spc/data_filtering/query.png')
SPC_ONE_HOUR = resource_path('images/spc/data_filtering/one_hour.png')
SPC_EIGHT_HOURS = resource_path('images/spc/data_filtering/eight_hours.png')
SPC_ONE_DAY = resource_path('images/spc/data_filtering/one_day.png')
SPC_ONE_WEEK = resource_path('images/spc/data_filtering/one_week.png')
SPC_ONE_MONTH = resource_path('images/spc/data_filtering/one_month.png')
SPC_EXPORT = resource_path('images/spc/data_filtering/export.png')
SPC_CPK_ANALYSIS = resource_path('images/spc/cpk_analysis.png')
SPC_GRR_ANALYSIS = resource_path('images/spc/grr_analysis.png')
SPC_LOGIN_USERNAME_CHINESE = resource_path('images/spc/login_name_chinese.png')
SPC_LOGIN_USERNAME_ENGLISH = resource_path('images/spc/login_name_english.png')
SPC_LOGIN_PASSWORD_CHINESE = resource_path('images/spc/login_password_chinese.png')
SPC_LOGIN_PASSWORD_ENGLISH = resource_path('images/spc/login_password_english.png')
SPC_USER_ADMIN = resource_path('images/spc/user_admin.png')
SPC_LOGIN_CHINESE = resource_path('images/spc/login_chinese.png')
SPC_LOGIN_ENGLISH = resource_path('images/spc/login_english.png')
SPC_PCB_VIEW = resource_path('images/spc/pcb_view.png')

PROGRAM_COMPONENT_LIGHT = resource_path('images/whole_board/program_component_light.png')
PROGRAM_COMPONENT_DARK = resource_path('images/whole_board/program_component_dark.png')
WHOLE_BOARD_DARK = resource_path('images/whole_board/board_dark.png')
WHOLE_BOARD_LIGHT = resource_path('images/whole_board/board_light.png')
# 整版-硬件图标
BOARD_HARDWARE_ICON = resource_path('images/whole_board/hardware_icon.png')
PART_CHOSED = resource_path('images/whole_board/part_chosed.png')
PASS_COMPONENT = resource_path('images/whole_board/job/pass_component.png')
NO_PASS_COMPONENT = resource_path('images/whole_board/job/no_pass_component.png')
NO_CHECKED_COMPONENT = resource_path('images/whole_board/job/no_checked_component.png')
CHECKED_COMPONENT = resource_path('images/whole_board/job/checked_component.png')
WHOLE_BOARD_IMAGE_LIGHT = resource_path('images/whole_board/image_light.png')
WHOLE_BOARD_IMAGE_DARK = resource_path('images/whole_board/image_dark.png')
# 元件窗口
CW_SQUARE_POSITIONING = resource_path('images/whole_board/component_window/alg/square_positioning.png')
CW_IMAGE_MATCHING = resource_path('images/whole_board/component_window/alg/image_matching.png')
CW_COLOR_AREA = resource_path('images/whole_board/component_window/alg/color_area.png')
CW_BODY_CHECK = resource_path('images/whole_board/component_window/alg/body_check.png')
CW_COLOR_MATCHING = resource_path('images/whole_board/component_window/alg/color_matching.png')
CW_COLOR_ANALYSISING = resource_path('images/whole_board/component_window/alg/color_analysising.png')
CW_PIN_SIMILARITY_MATCHING = resource_path('images/whole_board/component_window/alg/pin_similarity_matching.png')
CW_REFERENCE_PLANE_3D = resource_path('images/whole_board/component_window/alg/reference_plane_3d.png')
CW_COPLANARITY_3D = resource_path('images/whole_board/component_window/alg/coplanarity_3d.png')

CHIP_TYPE = resource_path('images/whole_board/chip_type.png')
MARK_POINT = resource_path('images/whole_board/mark_point.png')
BOARD_EYE = resource_path('images/whole_board/eye.png')
REFRESH = resource_path('images/whole_board/refresh.png')
BOARD_PACKAGE_TEST = resource_path('images/whole_board/package_test.png')
FOV_EDIT = resource_path('images/whole_board/fov/fov_edit.png')
MAGNIFIER = resource_path('images/whole_board/magnifier.png')
BOARD_BOARD = resource_path('images/whole_board/board_board.png')
BOARD_ENLARGE = resource_path('images/whole_board/enlarge.png')
BOARD_REDUCE = resource_path('images/whole_board/reduce.png')

OPEN_PROGRAM_PLUS = resource_path('images/open_program/plus.png')
OPEN_PROGRAM_CURSOR = resource_path('images/open_program/cursor.png')
OPEN_PROGRAM_REMOVE = resource_path('images/open_program/remove.png')
OPEN_PROGRAM_LOAD_1 = resource_path('images/open_program/load_1.png')
OPEN_PROGRAM_RECENT = resource_path('images/open_program/recent.png')
REMOVE_PROGRAM = resource_path('images/open_program/remove.png')
OPEN_PROGRAM_ALL_ALGS = resource_path('images/open_program/all_algs.png')
OPEN_PROGRAM_TOPIC = resource_path('images/open_program/topic.png')

ALG2D = resource_path('images/alg_param/alg2d.png')
ALG2D_LIGHT = resource_path('images/alg_param/alg2d_light.png')
ALG_RESULT_0 = resource_path('images/alg_param/result_0.png')
# 影响参数类型-权重
ALG_IMAGE_TYPE_WEIGHT = resource_path('images/alg_param/image_type_weight.png')
# 影响参数类型-颜色空间
ALG_IMAGE_TYPE_COLOR_SPACE = resource_path('images/alg_param/image_type_color_space.png')
# 影响参数类型-下拉框-权重
ALG_IMAGE_TYPE_CHOOSE_WEIGHT = resource_path('images/alg_param/image_type_choose_weight.png')
ALG2D_LIGHT_MEDIUM = resource_path('images/alg_param/alg2d_light_medium.png')
ALG2D_LIGHT_UNIFORM = resource_path('images/alg_param/alg2d_light_uniform.png')

ADD_WINDOW = resource_path('images/click_menu/add_window.png')
CLICK_AUTO_LINK = resource_path('images/click_menu/auto_link.png')
CLICK_MENU_RELATE = resource_path('images/click_menu/relate.png')
EDIT_THIS_COMPONENT = resource_path('images/click_menu/edit_this_component.png')
CLICK_CANCEL_RELATE = resource_path('images/click_menu/cancel_relate.png')
ADD_OBJECT = resource_path('images/click_menu/add_object.png')
BAD_BOARD_MARK = resource_path('images/click_menu/bad_board_mark.png')
ADD_SAME_CHECK_WINDOW = resource_path('images/click_menu/add_same_check_window.png')
EXPORT_COMPONENT_OK = resource_path('images/click_menu/export_component_ok.png')
EXPORT_PART_OK = resource_path('images/click_menu/export_part_ok.png')
EXPORT_ALL_OK = resource_path('images/click_menu/export_all_ok.png')
COMPONENT_INFORMATION = resource_path('images/click_menu/component_information.png')
ADD_REFERENCE_POINT = resource_path('images/click_menu/add_reference_point.png')
BOARD_COLOR_DRAWING = resource_path('images/click_menu/board_color_drawing.png')
PASTE_TO_COMPONENT = resource_path('images/click_menu/paste_to_component.png')

DEVELOPER_OPTIONS_SAVE_3D_DATA_YES = resource_path('images/developer_options/save_3d_data_yes.png')
DEVELOPER_OPTIONS_SAVE_3D_DATA_NO = resource_path('images/developer_options/save_3d_data_no.png')
DEVELOPER_OPTIONS_SAVE_CHECK_DATA_YES = resource_path('images/developer_options/save_check_data_yes.png')
DEVELOPER_OPTIONS_SAVE_CHECK_DATA_NO = resource_path('images/developer_options/save_check_data_no.png')


YES = resource_path('images/prompt_box/yes.png')
SELECT_FOLDER = resource_path('images/prompt_box/select_folder.png')
DEVELOPER_OPTIONS_YES = resource_path('images/prompt_box/developer_options_yes.png')
YES_BLUE = resource_path('images/prompt_box/yes_blue.png')
CHOOSED_YES = resource_path('images/prompt_box/choosed_yes.png')
QUESTION_MARK = resource_path('images/prompt_box/question_mark.png')
OPEN_PROGRAM_CANCEL = resource_path('images/prompt_box/cancel.png')
ADD_IMAGE_CLOSE = resource_path('images/prompt_box/add_image_close.png')
NO = resource_path('images/prompt_box/no.png')
PROGRAM_LOADING = resource_path('images/prompt_box/program_loading.png')
APPLY = resource_path('images/prompt_box/apply.png')
UI_SHOW_MESSAGE_YES = resource_path('images/prompt_box/ui_show_message_yes.png')
PROGRAM_ATTRIBUTE_CLOSE = resource_path('images/prompt_box/program_attribute_close.png')
CLOSE = resource_path('images/prompt_box/close.png')
IMAGE_CLOSE = resource_path('images/prompt_box/image_close.png')
EXPORT_PUBLIC_PROGRAM_CHECKED = resource_path('images/prompt_box/export_public_program_checked.png')
EXPORT_PUBLIC_PROGRAM_GRAY = resource_path('images/prompt_box/export_public_program_gray.png')
EXPORT_PUBLIC_PROGRAM = resource_path('images/prompt_box/export_public_program.png')
EXPORTING_DJB = resource_path('images/prompt_box/exporting_djb.png')
PLEASE_OPEN_PUBLIC_LIBS = resource_path('images/prompt_box/please_open_public_libs.png')
WARNING = resource_path('images/prompt_box/warning.png')
IF_EXPORT_PART_OK = resource_path('images/prompt_box/if_export_part_ok.png')
IF_EXPORT_ALL_OK = resource_path('images/prompt_box/if_export_all_ok.png')
IF_DELETE_BOARD = resource_path('images/prompt_box/if_delete_board.png')
IF_DELETE_BOARD_WARNING = resource_path('images/prompt_box/if_delete_board_warning.png')
TESTING_COMPONENT = resource_path('images/prompt_box/testing_component.png')
EXPORTING_OK = resource_path('images/prompt_box/exporting_ok.png')
OCV_EDIT_APPLY = resource_path('images/prompt_box/ocv_edit_apply.png')
SAVING_PROGRAM = resource_path('images/prompt_box/saving_program.png')
CLOSE_BUTTON = resource_path('images/prompt_box/close_button.png')
OK_COLLECTION = resource_path('images/prompt_box/ok_collection.png')
LOADING_ELEMENTS = resource_path('images/prompt_box/loading_elements.png')
INVALID_PASSWORD = resource_path('images/prompt_box/invalid_password.png')
LOGINING = resource_path('images/prompt_box/logining.png')
WINDOW_SAVE = resource_path('images/prompt_box/window_save.png')
WINDOW_CANCEL = resource_path('images/prompt_box/window_cancel.png')
WINDOW_DROP_LIST = resource_path('images/prompt_box/window_drop_list.png')
DELETE_LOG_SUCCESS = resource_path('images/prompt_box/delete_log_success.png')
EXPORTING_ELEMENTS = resource_path('images/prompt_box/exporting_elements.png')
ALL = resource_path('images/prompt_box/all.png')
CANCEL = resource_path('images/prompt_box/cancel.png')

PIN_ANGLE = resource_path('images/add_check_window/pin_angle.png')
ADD_CHECKED_TOPIC = resource_path('images/add_check_window/topic.png')
ADD_CHECKED_TYPE_SELF = resource_path('images/add_check_window/type_self.png')
ADD_CHECKED_TYPE_PIN = resource_path('images/add_check_window/type_pin.png')
ADD_CHECKED_SENIOR = resource_path('images/add_check_window/check_type/senior.png')
COLOR_MATCHING = resource_path('images/add_check_window/check_type/senior/color_matching.png')
PIN_CHECKING = resource_path('images/add_check_window/check_type/senior/pin_checking.png')
IMAGE_MATCHING = resource_path('images/add_check_window/check_type/senior/image_matching.png')
SQUARE_POSITIONING = resource_path('images/add_check_window/check_type/common/square_positioning.png')
REFERENCE_PLANE_3D = resource_path('images/add_check_window/check_type/common/3d_reference_plane.png')
COPLANARITY_3D = resource_path('images/add_check_window/check_type/common/coplanarity_3d.png')
# 板弯补偿
PLATE_BENDING_COMPENSATION = resource_path('images/add_check_window/check_type/plate_bending_compensation.png')
ADD_CHECKED_OCV = resource_path('images/add_check_window/check_type/common/ocv.png')
PIN_SIMILARITY_MATCHING = resource_path('images/add_check_window/check_type/common/pin_similarity_matching.png')
COLOR_AREA = resource_path('images/add_check_window/check_type/common/color_area.png')
X_OFFSET = resource_path('images/add_check_window/drawback/ontology/x_offset.png')
Y_OFFSET = resource_path('images/add_check_window/drawback/ontology/y_offset.png')
DEFAULT = resource_path('images/add_check_window/drawback/ontology/default.png')

IMAGE_PROCESS_TOPIC = resource_path('images/image_process/topic.png')

ALG_W_ = resource_path('images/alg_area/w_.png')
ALG_W_0 = resource_path('images/alg_area/w_0.png')
ALG_W_1 = resource_path('images/alg_area/w_1.png')
ALG_OCV = resource_path('images/alg_area/ocv.png')
ALG_CHECK_MODE_LEGEND = resource_path('images/alg_area/check_mode_legend.png')
ALG_CHECK_MODE_STANDARD = resource_path('images/alg_area/check_mode_standard.png')
ALG_SQUARE_POSITIONING = resource_path('images/alg_area/square_positioning.png')
ALG_LETTERFORM_CRAFTWORK_DEFAULT = resource_path('images/alg_area/letterform_craftwork_default.png')
ALG_SICK_SCREEN = resource_path('images/alg_area/sick_screen.png')
ALG_LATTICE = resource_path('images/alg_area/lattice.png')
ALG_TRANSISTOR = resource_path('images/alg_area/transistor.png')
ALG_CHECK_MODE_PARAMETER = resource_path('images/alg_area/check_mode_parameter.png')

ADD_STANDARD_IMAGE = resource_path('images/palette/add_standard_image.png')
DISPLAY_FILTERED_IMAGE = resource_path('images/palette/display_filtered_image.png')
WAIT_MATERIAL_EMPTY = resource_path('images/palette/wait_material_empty.png')
WAIT_MATERIAL_ALL_EMPTY = resource_path('images/palette/wait_material_all_empty.png')

PARAM_SETTING_TOPIC = resource_path('images/param_setting/topic.png')
PARAM_HARDWARE_SETTING = resource_path('images/param_setting/hardware_setting/topic.png')
PARAM_PROCESS_SETTING = resource_path('images/param_setting/process_setting/topic.png')
PARAM_DV_MODE_NO = resource_path('images/param_setting/process_setting/dv_mode_no.png')
PARAM_DV_MODE_YES = resource_path('images/param_setting/process_setting/dv_mode_yes.png')
PARAM_DV_AUTO_CHECK_NO = resource_path('images/param_setting/process_setting/dv_auto_check_no.png')
PARAM_DV_AUTO_CHECK_YES = resource_path('images/param_setting/process_setting/dv_auto_check_yes.png')
PARAM_DATA_EXPORT_SETTING = resource_path('images/param_setting/data_export_setting/topic.png')
PARAM_KEEP_THE_LAST_PCB_NUMBER = resource_path('images/param_setting/data_export_setting/keep_the_last_pcb_number.png')
PARAM_TRACK_1 = resource_path('images/param_setting/data_export_setting/track_1.png')
PARAM_TRACK_2 = resource_path('images/param_setting/data_export_setting/track_2.png')
PARAM_ONLINE_ALL_YES = resource_path('images/param_setting/data_export_setting/online_all_yes.png')
PARAM_ONLINE_ALL_NO = resource_path('images/param_setting/data_export_setting/online_all_no.png')

PARAM_GOOD_COMPONENT_LIMIT = resource_path('images/param_setting/data_export_setting/good_component_limit.png')
PARAM_NG_COMPONENT_LIMIT = resource_path('images/param_setting/data_export_setting/ng_component_limit.png')
PARAM_AMOUNT_LIMIT_ALL_YES = resource_path('images/param_setting/data_export_setting/amount_limit_all_yes.png')
PARAM_AMOUNT_LIMIT_ALL_NO = resource_path('images/param_setting/data_export_setting/amount_limit_all_no.png')
PARAM_UI_SETTING = resource_path('images/param_setting/ui_setting/topic.png')
PARAM_ALGORITHM_SETTING = resource_path('images/param_setting/algorithm_setting/topic.png')
PARAM_SHORTCUT_KEY_SETTING = resource_path('images/param_setting/shortcut_key_setting/topic.png')
PARAM_ONLINE_PARAMETER_DISPLAY_SYNC_PACKAGE = resource_path('images/param_setting/shortcut_key_setting/online_parameter_tuning_display_sync_package.png')
PARAM_ALGORITHM_DEVELOPER_OPTIONS = resource_path('images/param_setting/algorithm_setting/developer_options.png')

FOV_BAD_MARK_FOV_FIRST_NO = resource_path('images/fov/bad_mark_fov_first_no.png')

SAVE = resource_path('images/gui/save.png')
PLAY = resource_path('images/gui/play.png')
SAVE_AS_JOB = resource_path('images/gui/save_as_job.png')
AOI_TOPIC = resource_path('images/gui/topic.png')
SYSTEM_DARK = resource_path('images/gui/system/system_dark.png')
RENAME_PROGRAM = resource_path('images/gui/system/rename_program.png')
RUN_DARK = resource_path('images/gui/run/run_dark.png')
RUN_LIGHT = resource_path('images/gui/run/run_light.png')
CHANGE_PARAM_ONLINE = resource_path('images/gui/run/change_param_online.png')
CHANGE_PARAM_ONLINE_OPENED = resource_path('images/gui/run/change_param_online_opened.png')
CHANGE_PARAM_ONLINE_CLOSED = resource_path('images/gui/run/change_param_online_closed.png')
GUI_LOGIN = resource_path('images/gui/run/login.png')
STOP = resource_path('images/gui/run/stop.png')
TOOL = resource_path('images/gui/tools/tool.png')
TOOL_DARK = resource_path('images/gui/tools/tool_dark.png')
PACKAGE_TYPE_MANAGE = resource_path('images/gui/tools/package_type_manage.png')
SYNC_TO_PUBLIC_LIBS = resource_path('images/gui/tools/library/sync_to_public_libs.png')
OPEN_PROGRAM = resource_path('images/gui/open_program.png')
FOV = resource_path('images/gui/board/fov.png')
BOARD_AUTO = resource_path('images/gui/board/auto.png')
BOARD_LIGHT = resource_path('images/gui/board/light.png')
BOARD_DARK = resource_path('images/gui/board/dark.png')
BOARD_SPLICING_OPERATION = resource_path('images/gui/board/splicing_operation.png')
BOARD_DELETE_IMPOSITION = resource_path('images/gui/board/delete_imposition.png')
ELEMENTS = resource_path('images/gui/elements/elements.png')
MANUAL_SELECT = resource_path('images/gui/elements/manual_select.png')
IMPORT_CURRENT_PN = resource_path('images/gui/elements/import_current_part_no.png')
EXPORT_CURRENT_PN = resource_path('images/gui/elements/export_current_part_no.png')
EXPORT_ALL_PN = resource_path('images/gui/elements/export_all_part_no.png')
IMPORT_ALL_PN = resource_path('images/gui/elements/import_all_part_no.png')
ELEMENTS_STANDARD_LIBRARY = resource_path('images/gui/elements/standard_library.png')
PUBLIC_ELEMENTS = resource_path('images/gui/elements/public_elements.png')
ELEMENTS_DEFAULT = resource_path('images/gui/elements/default.png')
IMPORTING_ELEMENTS = resource_path('images/gui/elements/importing_elements.png')
EDIT_BACK = resource_path('images/gui/edit/back.png')
GUI_EDIT_LIGHT = resource_path('images/gui/edit/light.png')
COMPONENT_3D_IMAGE = resource_path('images/gui/edit/component_3d_image.png')
GUI_EDIT_LIGHT_MENU = resource_path('images/gui/edit/light_menu.png')
SEARCH_RANGE = resource_path('images/gui/edit/search_range.png')
GUI_EDIT_DELETE = resource_path('images/gui/edit/delete.png')
TEST_WINDOW = resource_path('images/gui/edit/test_window.png')
RELATE_WINDOW = resource_path('images/gui/edit/relate.png')
CANCEL_RELATE_WINDOW = resource_path('images/gui/edit/cancel_relate.png')
EDIT_LIGHT = resource_path('images/gui/edit/edit_light.png')
EDIT_DARK = resource_path('images/gui/edit/edit_dark.png')
TEST_COMPONENT = resource_path('images/gui/edit/test_component.png')
TEST_GROUP = resource_path('images/gui/edit/test_group.png')
TEST_BOARD = resource_path('images/gui/edit/test_board.png')
SETTING_DARK = resource_path('images/gui/setting/setting.png')
SETTING_LIGHT = resource_path('images/gui/setting/setting_light.png')
HARDWARE_SETTING = resource_path('images/gui/setting/hardware/hardware_setting.png')

PYQT_ICON = resource_path('gui/resources/sinic_tek.jpg')
BLACK = resource_path('images/hodgepodge/black.png')
CHANGE_PARAM_ONLINE_TASKBAR = resource_path('images/gui/run/change_param_online_taskbar.png')
EDIT_PACKAGE_TYPE = resource_path('images/hodgepodge/edit_package_type.png')
CLEAR_PACKAGE_TYPE = resource_path('images/hodgepodge/clear_package_type.png')
COPY_PACKAGE_TYPE_NAME = resource_path('images/hodgepodge/copy_package_type_name.png')
COPY_PART_NO_NAME = resource_path('images/hodgepodge/copy_part_no_name.png')
TYPE_NAME_DEFAULT = resource_path('images/hodgepodge/type_name_default.png')
TYPE_NAME_C = resource_path('images/hodgepodge/type_name_c.png')
TEST_PACKAGE_NAME = resource_path('images/hodgepodge/test_package_name.png')
ELEMENTS_TYPE_NAME = resource_path('images/hodgepodge/elements_type_name.png')
ELEMENTS_INFORMATION = resource_path('images/hodgepodge/elements_information.png')
ELEMENTS_VIEW_ABC = resource_path('images/hodgepodge/elements_view_abc.png')
ELEMENTS_VIEW_TEST = resource_path('images/hodgepodge/elements_view_test.png')
ELEMENTS_VIEW_SEARCH = resource_path('images/hodgepodge/elements_view_search.png')
ELEMENTS_VIEW_CANCEL = resource_path('images/hodgepodge/elements_view_cancel.png')
PALETTE_EMPTY = resource_path('images/hodgepodge/palette_empty.png')
ELEMENTS_VIEW_PN_EMPTY = resource_path('images/hodgepodge/elements_view_pn_empty.png')
ELEMENTS_VIEW_PT_EMPTY = resource_path('images/hodgepodge/elements_view_pt_empty.png')
ALG_PARAM_EMPTY = resource_path('images/hodgepodge/alg_param_empty.png')
SAVE_AS_TOPIC = resource_path('images/hodgepodge/save_as_topic.png')
OPEN_DJB_TOPIC = resource_path('images/hodgepodge/open_djb_topic.png')
LOG_SAVE_SUCCESS = resource_path('images/hodgepodge/log_save_success.png')
# 点击运行后的测试界面
TESTING_INTERFACE_INFORMATION = resource_path('images/testing_interface/information.png')
TESTING_INTERFACE_GOOD = resource_path('images/testing_interface/good.png')
TESTING_INTERFACE_CIRCLE_1 = resource_path('images/testing_interface/circle_1.png')
TESTING_INTERFACE_CIRCLE_20 = resource_path('images/testing_interface/circle_20.png')
TESTING_INTERFACE_PERCENT_100 = resource_path('images/testing_interface/percent_100.png')
TESTING_INTERFACE_STOP = resource_path('images/testing_interface/stop.png')
TESTING_INTERFACE_IGNORE = resource_path('images/testing_interface/ignore.png')
TESTING_INTERFACE_ENTER_DETAIL_INTERFACE = resource_path('images/testing_interface/enter_detail_interface.png')
# 参数配置-ui配置
# 自动加载程式
SETTING_UI_AUTO_LOAD_PROGRAM_YES = resource_path('images/setting/ui/auto_load_program_yes.png')
SETTING_UI_AUTO_LOAD_PROGRAM_NO = resource_path('images/setting/ui/auto_load_program_no.png')
SETTING_UI_EXPORT_ALL_OK_YES = resource_path('images/setting/ui/export_all_ok_yes.png')
SETTING_UI_EXPORT_ALL_OK_NO = resource_path('images/setting/ui/export_all_ok_no.png')
SETTING_UI_EXPORT_OK_YES = resource_path('images/setting/ui/export_ok_yes.png')
SETTING_UI_EXPORT_OK_NO = resource_path('images/setting/ui/export_ok_no.png')
# 演算法配置-保存DJB文件
SETTING_ALGORITHM_SAVE_DJB_YES = resource_path('images/setting/algorithm/save_djb_yes.png')
SETTING_ALGORITHM_SAVE_DJB_NO = resource_path('images/setting/algorithm/save_djb_no.png')
SETTING_ALGORITHM_MARK_MATCHING_YES = resource_path('images/setting/algorithm/mark_matching_yes.png')
SETTING_ALGORITHM_MARK_MATCHING_NO = resource_path('images/setting/algorithm/mark_matching_no.png')
SETTING_ALGORITHM_BARCODE_DETECTION_YES = resource_path('images/setting/algorithm/barcode_detection_yes.png')
SETTING_ALGORITHM_BARCODE_DETECTION_NO = resource_path('images/setting/algorithm/barcode_detection_no.png')
SETTING_ALGORITHM_COLOR_ANALYSE_YES = resource_path('images/setting/algorithm/color_analyse_yes.png')
SETTING_ALGORITHM_COLOR_ANALYSE_NO = resource_path('images/setting/algorithm/color_analyse_no.png')


# 演算法配置-勾选所有算法
SETTING_ALGORITHM_ALL_ALGS_YES = resource_path('images/setting/algorithm/all_algs_yes.png')
SETTING_ALGORITHM_ALL_ALGS_NO = resource_path('images/setting/algorithm/all_algs_no.png')


# 文件夹-左
OFFSET_LEFT_1 = resource_path('images/offset/left_1.png')
OUTPUT_DELAY_TIME = resource_path('images/offset/output_delay_time.png')

# 元件库视图-上图为空
ELEMENTS_VIEW_PICTURE_EMPTY_UP = resource_path('images/hodgepodge/elements_view_picture_empty_up.png')
# 元件库视图-下图为空
ELEMENTS_VIEW_PICTURE_EMPTY_DOWN = resource_path('images/hodgepodge/elements_view_picture_empty_down.png')
ELEMENTS_VIEW_REFRESH = resource_path('images/hodgepodge/elements_view_refresh.png')
QUERY = resource_path('images/hodgepodge/query.png')
OPEN_PROGRAM_CHOSED = resource_path('images/hodgepodge/open_program_chosed.png')
UI_SHOW_MESSAGE = resource_path('images/hodgepodge/ui_show_message.png')
TEST = resource_path('images/hodgepodge/test.png')
RULER = resource_path('images/hodgepodge/ruler.png')
FRM_FILL_COLOR = resource_path('images/hodgepodge/frm_fill_color.png')
IF_SYNC_SAME_PACKAGE_NO = resource_path('images/hodgepodge/if_sync_same_package_no.png')
IF_SYNC_SAME_PACKAGE_YES = resource_path('images/hodgepodge/if_sync_same_package_yes.png')
IF_EXPORT_ALL_PN = resource_path('images/hodgepodge/if_export_all_pn.png')
BOARD_COLOR_FILTER = resource_path('images/hodgepodge/board_color_filter.png')
BOARD_COLOR_FILTER_CLOSE = resource_path('images/hodgepodge/board_color_filter_close.png')
OPEN_PROGRAM_SINGLE_BOARD = resource_path('images/hodgepodge/open_program_single_board.png')
OPEN_PROGRAM_EMPTY = resource_path('images/hodgepodge/open_program_empty.png')
USER_LOGIN_LIGHT = resource_path('images/hodgepodge/user_login_light.png')
USER_LOGIN_DARK = resource_path('images/hodgepodge/user_login_dark.png')
USER_LOGIN_CHINESE_DARK = resource_path('images/hodgepodge/user_login_chinese_dark.png')
USER_LOGIN_CHINESE_LIGHT = resource_path('images/hodgepodge/user_login_chinese_light.png')

FRM_TOPIC = resource_path('images/frm/topic.png')
FRM_COLOR_DRAWING = resource_path('images/frm/color_drawing.png')
FRM_APPLY = resource_path('images/frm/apply.png')
FRM_OK = resource_path('images/frm/ok.png')

ROTATION_ANGLE = resource_path('images/component_attribute/rotation_angle.png')

PCB_VIEW_BLACK_MEDIUM = resource_path('images/pcb_view/black_medium.png')
PCB_VIEW_TOPIC = resource_path('images/pcb_view/topic.png')
PCB_VIEW_BOARD_DISCRET = resource_path('images/pcb_view/board_discret.png')

# 在线调参界面












# ======================================坐标========================================
SHARE_LIB_PATH_COORDINATE = (1185, 295)
UI_SHOW_MESSAGE_COORDINATE = (515, 370)
FOV_FOV_COORDINATE = (701, 694)
W_0_COORDINATE = (100, 690)
W_1_COORDINATE = (100, 710)
RV_DATA_POINT = (100, 215)
FOV_FOD = (701, 694)
FOV_FOREIGN_CHECK_COORDINATE = (723, 717)
FOV_INSIDE_CHECK_COORDINATE = (723, 738)
FOV_SENIOR_COORDINATE = (78, 526)
FOV_EXPAND_COORDINATE = (195, 633)
CENTRE = (935, 446)
PART_POSITION_NO = (180, 210)
RESERVE_COMPONENT_COORDINATE = (885, 524)
RESERVE_BENCHMARK_COORDINATE = (885, 549)
# 选择料号导出库的修改日期坐标
SELECT_PN_EXPORT_LIB_POINTS_DATES = [
    {"date": (1000, 360), "checkbox": ((1112, 352), (1124, 364))},
    {"date": (1000, 380), "checkbox": ((1112, 375), (1124, 387))},
    {"date": (1000, 405), "checkbox": ((1112, 398), (1124, 410))},
    {"date": (1000, 430), "checkbox": ((1112, 421), (1124, 433))},    
]
LIGHT_VIEWS_POINTS = [(550, 315), (685, 315), (820, 315),
               (550, 455), (685, 455), (820, 455),
               (550, 580), (685, 580), (820, 580),
               (550, 710), (685, 710)]
SQUARE_POSITIONING_POINTS = [(1720, 398), (1720, 418), (1720, 440), (1720, 460), (1720, 480), (1720, 500), (1720, 630),
                    (1720, 650),
                    (1720, 690), (1720, 715), (1720, 735), (1720, 775), (1720, 840), (1720, 860)]
IMAGE_PARAM_POINTS = [(1720, 355), (1720, 375), (1720, 545), (1720, 565)]


CW_COLOR_MATCHING_POINTS = [(1720, 355), (1720, 525), (1720, 545), (1720, 652)]
CW_COLOR_ANALYSISING_POINTS = [(1720, 460), (1720, 480)]
CW_COLOR_AREA_POINTS = [(1720, 460), (1720, 480)]
CW_IMAGE_MATCHING_POINTS = [(1720, 355), (1720, 375), (1720, 545), (1720, 565)]
CW_SQUARE_POSITIONING_POINTS = [(1720, 398), (1720, 418), (1720, 440), (1720, 460), (1720, 480), (1720, 500), (1720, 630),
                    (1720, 650),
                    (1720, 690), (1720, 715), (1720, 735), (1720, 775), (1720, 840), (1720, 860)]
CW_PIN_SIMILARITY_MATCHING_POINTS = [(1720, 440), (1720, 460), (1720, 500)]
PCB_COMPONENT_LIST_POINTS = [(1545, 375), (1545, 400), (1545, 420), (1545, 440), (1545, 460), (1545, 480), 
                             (1545, 500), (1545, 525), (1545, 545), (1545, 565), (1545, 585)]
# ======================================区域========================================
# 使用pyautogui时，将坐标（左上角AX,左上角AY,右下角BX,右下角BY）转为pyautogui的region的格式 用到pyautogui的才用该函数
def convert_region(region):
    left, top, right_bottom_x, right_bottom_y = region
    width = right_bottom_x - left
    height = right_bottom_y - top
    return (left, top, width, height)
# PCB列表区域
PCB_LIST_REGION = convert_region((0, 80, 235, 1010))
# PCB上边区域(首页的上部分)
PCB_UP_REGION = convert_region((240, 80, 1500, 545))
# PCB元件列表区域
PCB_COMPONENT_LIST_REGION = convert_region((1509, 318, 1525, 605))
# 屏幕坐标附近区域
CENTRE_REGION = convert_region((888, 400, 1020, 510))
# 检测结果区域
CHECK_RESULT_REGION = convert_region((765, 150, 1135, 190))
# 左下日志区域
LOG_REGION = convert_region((4, 859, 359, 1008))
# 元件库视图
ELEMENTS_VIEW_REGION = convert_region((362, 149, 796, 758))
# 芯片板区域
BOARD_REGION = convert_region((712, 152, 1535, 962))
# 元件编辑区域
COMPONENT_REGION = convert_region((545, 190, 1507, 740))
# 快捷键设置-元件编辑区域
SHORTCUT_KEY_COMPONENT_EDIT_REGION = convert_region((380, 250, 1521, 1004))
# 调色板区域
PALETTE_REGION = convert_region((362, 765, 1521, 1004))
# 编辑界面封装类型区域
PACKAGE_TYPE_REGION = convert_region((1380, 165, 1505, 180))
# 料号导入库分类下拉框
PN_IMPORT_DROPDOWN_BOX_REGION = convert_region((888, 536, 1085, 649))
# 算法参数区域
ALG_PARAM_REGION = convert_region((1530, 193, 1895, 620))
# 料号区域
PACKAGE_PART_NO_REGION = convert_region((958, 354, 1170, 680))
# 被选程式列表区域
SELECTED_PROGRAM_REGION = convert_region((994, 239, 1383, 556))
# 程式列表区域
PROGRAM_LIST_REGION = convert_region((458, 238, 923, 558))
# 单个料号
SINGLE_PART_NO_REGION = convert_region((958, 354, 1095, 366))
# 整板信息区域
BOARD_INFORMATION_REGION = convert_region((45, 170, 360, 1010))
# 板内各元件区域
BOARD_COMPONENTS_REGION = convert_region((45, 252, 352, 604))
# 元件窗口区域
COMPONENT_WINDOW_REGION = convert_region((45, 640, 350, 850))
COMPONENT_NUM_REGION = convert_region((82, 253, 232, 271))
# 元件操作区域（屏幕中央区域）
COMPONENT_OPERATION_REGION = convert_region((555, 190, 1300, 710))
# ocv编辑 识别文字区域
OCR_RESULT_REGION = convert_region((695, 365, 1100, 770))
# 程式信息区域
PROGRAM_INFORMATION_REGION = convert_region((994, 586, 1381, 828))
# 元件库视图搜索下拉框
ELEMENTS_VIEW_DROPDOWN_BOX_REGION = convert_region((372, 244, 572, 312))
# 芯片区域(用的是bbox。不是pyautogui，不需要转换)
CHIP_SCROLLBAR_REGION = (777, 230, 792, 648)
# 整版区域的滚动条
BOARD_SCROLLBAR_REGION = convert_region((333, 253, 350, 603))
# 元件库视图的元件图片
ELEMENTS_VIEW_IMAGE_REGION = convert_region((569, 243, 748, 417))
# 元件库视图的元件编辑界面
ELEMENTS_VIEW_COMPONENT_REGION = convert_region((560, 150, 1450, 738))

# rv的pcb列表区域
RV_PCB_LIST_REGION = convert_region((5, 140, 211, 985))
# rv的元件列表区域
RV_COMPONENT_LIST_REGION = convert_region((1510, 320, 1825, 605))
# rv的元件标准图区域
RV_STANDARD_IMAGE_REGION = convert_region((240, 80, 655, 540))

# ======================================绝对路径========================================
# 参数配置-数据导出配置-共享元件库路径
SHARE_LIB_PATH = r'D:\EYAOI\PublicCompLibrary'
# 参数配置-数据导出配置-元件库路径
ELEMENTS_LIB_PATH = r'D:\EYAOI\CompLibrary'

# ===================================RV-AI复判========================================
RV_AI_TOPIC = resource_path('images/rv_ai_test/topic.png')
RV_AI_TOPIC_DARK = resource_path('images/rv_ai_test/dark_topic.png')
RV_AI_SIMULATE_TO_TRAIN = resource_path('images/rv_ai_test/simulate_to_train.png')
RV_AI_SIMULATE_TO_EVAL = resource_path('images/rv_ai_test/simulate_to_eval.png')
RV_AI_TRAIN_SUCCESS = resource_path('images/rv_ai_test/train_success.png')
RV_AI_EVAL_SUCCESS = resource_path('images/rv_ai_test/eval_success.png')
RV_AI_TRAIN_EVAL_YES = resource_path('images/rv_ai_test/train_eval_yes.png')
RV_AI_MISSION_MANAGE = resource_path('images/rv_ai_test/mission_manage.png')
RV_AI_CLOSE_MISSION_MANAGE = resource_path('images/rv_ai_test/close_mission_manage.png')
RV_AI_JOB_NAME = resource_path('images/rv_ai_test/job_name.png')
RV_AI_TRAIN_STATUS = resource_path('images/rv_ai_test/train_status.png')
RV_AI_REFRESH_JOB = resource_path('images/rv_ai_test/refresh_job.png')
RV_AI_DELETE_JOB = resource_path('images/rv_ai_test/delete_job.png')
RV_AI_CLICK_RESTART_EVAL = resource_path('images/rv_ai_test/click_restart_eval.png')
RV_AI_MANUAL_FILTER = resource_path('images/rv_ai_test/manual_filter.png')
RV_AI_FILTER_TOPIC = resource_path('images/rv_ai_test/filter_topic.png')
RV_AI_IMAGE_ZERO = resource_path('images/rv_ai_test/image_zero.png')
RV_AI_PASS = resource_path('images/rv_ai_test/pass.png')
RV_AI_NG = resource_path('images/rv_ai_test/ng.png')
RV_AI_CURRENT_CLOSE = resource_path('images/rv_ai_test/current_close.png')

# RV
RV_PASSWORD = resource_path('images/rv/password.png')
RV_ICON = resource_path('images/rv/icon.png')
RV_ALL_PASS = resource_path('images/rv/all_pass.png')
RV_PASS = resource_path('images/rv/pass.png')
RV_NG = resource_path('images/rv/ng.png')
RV_ALL_NG = resource_path('images/rv/all_ng.png')
RV_CONFIRM = resource_path('images/rv/confirm.png')
RV_PCB_LIST_EMPTY = resource_path('images/rv/pcb_list_empty.png')
RV_TASKBAR = resource_path('images/rv/taskbar.png')

