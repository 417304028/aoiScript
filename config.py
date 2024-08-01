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


AOI_EXE_PATH = r'D:\EYAOI\Bin\AOI.exe'
JOB_PATH = r'D:\EYAOI\JOB\djb'

PROGRAM_COMPONENT_LIGHT = resource_path('images/whole_board/program_component_light.png')
PROGRAM_COMPONENT_DARK = resource_path('images/whole_board/program_component_dark.png')
WHOLE_BOARD_DARK = resource_path('images/whole_board/board_dark.png')
WHOLE_BOARD_LIGHT = resource_path('images/whole_board/board_light.png')
PASS_COMPONENT = resource_path('images/whole_board/job/pass_component.png')
NO_PASS_COMPONENT = resource_path('images/whole_board/job/no_pass_component.png')
NO_CHECKED_COMPONENT = resource_path('images/whole_board/job/no_checked_component.png')
CHECKED_COMPONENT = resource_path('images/whole_board/job/checked_component.png')
WHOLE_BOARD_IMAGE_LIGHT = resource_path('images/whole_board/image_light.png')
WHOLE_BOARD_IMAGE_DARK = resource_path('images/whole_board/image_dark.png')
FOV_EDIT = resource_path('images/whole_board/fov/fov_edit.png')
MAGNIFIER = resource_path('images/whole_board/magnifier.png')
BOARD_BOARD = resource_path('images/whole_board/board_board.png')
BOARD_ENLARGE = resource_path('images/whole_board/enlarge.png')
BOARD_REDUCE = resource_path('images/whole_board/reduce.png')

OPEN_PROGRAM_PLUS = resource_path('images/open_program/plus.png')
OPEN_PROGRAM_CURSOR = resource_path('images/open_program/cursor.png')
OPEN_PROGRAM_LOAD = resource_path('images/open_program/load.png')
OPEN_PROGRAM_RECENT = resource_path('images/open_program/recent.png')
REMOVE_PROGRAM = resource_path('images/open_program/remove.png')
OPEN_PROGRAM_TOPIC = resource_path('images/open_program/topic.png')

ALG2D = resource_path('images/alg_param/alg2d.png')
ALG2D_LIGHT = resource_path('images/alg_param/alg2d_light.png')
ALG2D_LIGHT_MEDIUM = resource_path('images/alg_param/alg2d_light_medium.png')
ADD_WINDOW = resource_path('images/click_menu/add_window.png')
CLICK_AUTO_LINK = resource_path('images/click_menu/auto_link.png')
CLICK_RELATE = resource_path('images/click_menu/relate.png')
CLICK_CANCEL_RELATE = resource_path('images/click_menu/cancel_relate.png')
EXPORT_COMPONENT_OK = resource_path('images/click_menu/export_component_ok.png')
EXPORT_PART_OK = resource_path('images/click_menu/export_part_ok.png')
EXPORT_ALL_OK = resource_path('images/click_menu/export_all_ok.png')
ADD_REFERENCE_POINT = resource_path('images/click_menu/add_reference_point.png')
BOARD_COLOR_DRAWING = resource_path('images/click_menu/board_color_drawing.png')

OPEN_PROGRAM_YES = resource_path('images/prompt_box/open_program_yes.png')
OPEN_PROGRAM_CANCEL = resource_path('images/prompt_box/open_program_cancel.png')
ADD_CHECKED_YES = resource_path('images/prompt_box/add_check_yes.png')
PROGRAM_LOADING = resource_path('images/prompt_box/program_loading.png')
IMAGE_PROCESS_YES = resource_path('images/prompt_box/image_process_yes.png')
PARAM_SETTING_YES = resource_path('images/prompt_box/param_setting_yes.png')
UI_SHOW_MESSAGE_YES = resource_path('images/prompt_box/ui_show_message_yes.png')
CLOSE = resource_path('images/prompt_box/close.png')
EXPORT_PUBLIC_PROGRAM_GRAY = resource_path('images/prompt_box/export_public_program_gray.png')
EXPORT_PUBLIC_PROGRAM = resource_path('images/prompt_box/export_public_program.png')
PLEASE_OPEN_PUBLIC_LIBS = resource_path('images/prompt_box/please_open_public_libs.png')
EXPORT_COMPONENT_SUCCESS = resource_path('images/prompt_box/export_component_success.png')
IF_EXPORT_PART_OK = resource_path('images/prompt_box/if_export_part_ok.png')
IF_EXPORT_ALL_OK = resource_path('images/prompt_box/if_export_all_ok.png')
IF_DELETE_BOARD = resource_path('images/prompt_box/if_delete_board.png')
IF_DELETE_BOARD_WARNING = resource_path('images/prompt_box/if_delete_board_warning.png')
EXPORTING_OK = resource_path('images/prompt_box/exporting_ok.png')
OCV_EDIT_APPLY = resource_path('images/prompt_box/ocv_edit_apply.png')
OK_COLLECTION = resource_path('images/prompt_box/ok_collection.png')

ADD_CHECKED_TOPIC = resource_path('images/add_check_window/topic.png')
ADD_CHECKED_SENIOR = resource_path('images/add_check_window/check_type/senior.png')
COLOR_MATCHING = resource_path('images/add_check_window/check_type/senior/color_matching.png')
PIN_CHECKING = resource_path('images/add_check_window/check_type/senior/pin_checking.png')
IMAGE_MATCHING = resource_path('images/add_check_window/check_type/senior/image_matching.png')
SQUARE_POSITIONING = resource_path('images/add_check_window/check_type/common/square_positioning.png')
ADD_CHECKED_OCV = resource_path('images/add_check_window/check_type/common/ocv.png')
PIN_SIMILARITY_MATCHING = resource_path('images/add_check_window/check_type/common/pin_similarity_matching.png')
COLOR_AREA = resource_path('images/add_check_window/check_type/common/color_area.png')
X_OFFSET = resource_path('images/add_check_window/drawback/ontology/x_offset.png')
Y_OFFSET = resource_path('images/add_check_window/drawback/ontology/y_offset.png')
DEFAULT = resource_path('images/add_check_window/drawback/ontology/default.png')

IMAGE_PROCESS_TOPIC = resource_path('images/image_process/topic.png')

ALG_W_0 = resource_path('images/alg_area/w_0.png')
ALG_W_1 = resource_path('images/alg_area/w_1.png')
ALG_RESULT_0 = resource_path('images/alg_area/result_0.png')
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

PARAM_SETTING_TOPIC = resource_path('images/param_setting/topic.png')
PARAM_HARDWARE_SETTING = resource_path('images/param_setting/hardware_setting/topic.png')
PARAM_DATA_EXPORT_SETTING = resource_path('images/param_setting/data_export_setting/topic.png')
PARAM_UI_SETTING = resource_path('images/param_setting/ui_setting/topic.png')
PARAM_ALGORITHM_SETTING = resource_path('images/param_setting/algorithm_setting/topic.png')

SAVE = resource_path('images/gui/save.png')
AOI_TOPIC = resource_path('images/gui/topic.png')
RUN = resource_path('images/gui/run/run.png')
TOOL = resource_path('images/gui/tools/tool.png')
PACKAGE_TYPE_MANAGE = resource_path('images/gui/tools/package_type_manage.png')
SYNC_TO_PUBLIC_LIBS = resource_path('images/gui/tools/library/sync_to_public_libs.png')
OPEN_PROGRAM = resource_path('images/gui/open_program.png')
FOV = resource_path('images/gui/board/fov.png')
BOARD_AUTO = resource_path('images/gui/board/auto.png')
BOARD_LIGHT = resource_path('images/gui/board/light.png')
BOARD_SPLICING_OPERATION = resource_path('images/gui/board/splicing_operation.png')
BOARD_DELETE_IMPOSITION = resource_path('images/gui/board/delete_imposition.png')
ELEMENTS = resource_path('images/gui/elements/elements.png')
IMPORT_CURRENT_PART_NO = resource_path('images/gui/elements/import_current_part_no.png')
EXPORT_CURRENT_PART_NO = resource_path('images/gui/elements/export_current_part_no.png')
ELEMENTS_IMPORT_ALL = resource_path('images/gui/elements/import_all.png')
ELEMENTS_STANDARD_LIBRARY = resource_path('images/gui/elements/standard_library.png')
PUBLIC_ELEMENTS = resource_path('images/gui/elements/public_elements.png')
ELEMENTS_DEFAULT = resource_path('images/gui/elements/default.png')
EDIT_BACK = resource_path('images/gui/edit/back.png')
GUI_EDIT_LIGHT = resource_path('images/gui/edit/light.png')
GUI_EDIT_LIGHT_MENU = resource_path('images/gui/edit/light_menu.png')
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
EDIT_PACKAGE_TYPE = resource_path('images/hodgepodge/edit_package_type.png')
CLEAR_PACKAGE_TYPE = resource_path('images/hodgepodge/clear_package_type.png')
COPY_PACKAGE_TYPE_NAME = resource_path('images/hodgepodge/copy_package_type_name.png')
COPY_PART_NO_NAME = resource_path('images/hodgepodge/copy_part_no_name.png')
QUERY = resource_path('images/hodgepodge/query.png')
UI_SHOW_MESSAGE = resource_path('images/hodgepodge/ui_show_message.png')
IF_SYNC_PART_NO = resource_path('images/hodgepodge/if_sync_part_no.png')
TEST = resource_path('images/hodgepodge/test.png')
IF_SYNC_SAME_PACKAGE_NO = resource_path('images/hodgepodge/if_sync_same_package_no.png')
IF_SYNC_SAME_PACKAGE_YES = resource_path('images/hodgepodge/if_sync_same_package_yes.png')
ADD_IMAGE_CLOSE = resource_path('images/hodgepodge/add_checked_close.png')

FRM_TOPIC = resource_path('images/frm/topic.png')
FRM_COLOR_DRAWING = resource_path('images/frm/color_drawing.png')
FRM_APPLY = resource_path('images/frm/apply.png')
FRM_OK = resource_path('images/frm/ok.png')

# ======================================坐标========================================
SHARE_LIB_PATH_COORDINATE = (1185,295)
UI_SHOW_MESSAGE_COORDINATE = (515,370)
FOV_FOV_COORDINATE = (701,694)
FOV_FOREIGN_CHECK_COORDINATE = (723,717)
FOV_INSIDE_CHECK_COORDINATE = (723,738)
FOV_SENIOR_COORDINATE = (78,526)
FOV_EXPAND_COORDINATE = (200,613)
CENTRE = (935,446)
PART_POSITION_NO = (180,210)
RESERVE_COMPONENT_COORDINATE = (885,524)
RESERVE_BENCHMARK_COORDINATE = (885,549)
# ======================================区域========================================
# 编辑区域
EDIT_REGION = (545, 190, 1715, 940)
BOARD_INFORMATION_REGION = (46, 199, 350, 848)
COMPONENT_NUM_REGION = (82, 253, 232, 271)



# ======================================绝对路径========================================
# 参数配置-数据导出配置-共享元件库路径
SHARE_LIB_PATH = r'D:\EYAOI\PublicCompLibrary'



# ===================================RV-AI复判========================================
RV_TOPIC = resource_path('images/rv_ai_test/topic.png')
RV_TOPIC_DARK = resource_path('images/rv_ai_test/dark_topic.png')
RV_SIMULATE_TO_TRAIN = resource_path('images/rv_ai_test/simulate_to_train.png')
RV_SIMULATE_TO_EVAL = resource_path('images/rv_ai_test/simulate_to_eval.png')
RV_TRAIN_SUCCESS = resource_path('images/rv_ai_test/train_success.png')
RV_EVAL_SUCCESS = resource_path('images/rv_ai_test/eval_success.png')
RV_TRAIN_EVAL_YES = resource_path('images/rv_ai_test/train_eval_yes.png')
RV_MISSION_MANAGE = resource_path('images/rv_ai_test/mission_manage.png')
RV_CLOSE_MISSION_MANAGE = resource_path('images/rv_ai_test/close_mission_manage.png')
RV_JOB_NAME = resource_path('images/rv_ai_test/job_name.png')
RV_TRAIN_STATUS = resource_path('images/rv_ai_test/train_status.png')
RV_REFRESH_JOB = resource_path('images/rv_ai_test/refresh_job.png')
RV_DELETE_JOB = resource_path('images/rv_ai_test/delete_job.png')
RV_CLICK_RESTART_EVAL = resource_path('images/rv_ai_test/click_restart_eval.png')

