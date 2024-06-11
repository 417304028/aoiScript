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

    return os.path.join(base_path, relative_path)

AOI_EXE_PATH = r'D:\EYAOI\Bin\AOI.exe'
JOB_PATH = r'D:\EYAOI\JOB\djb'

PROGRAM_COMPONENT = resource_path('images/whole_board/program_component.png')
PROGRAM_COMPONENT_DARK = resource_path('images/whole_board/program_component_dark.png')

NO_CHECKED_COMPONENT = resource_path('images/whole_board/job/no_checked_component.png')
CHECKED_COMPONENT = resource_path('images/whole_board/job/checked_component.png')
WHOLE_BOARD_LIGHT = resource_path('images/whole_board/whole_board_image_light.png')

OPEN_PROGRAM_PLUS = resource_path('images/open_program/plus.png')
OPEN_PROGRAM_CURSOR = resource_path('images/open_program/cursor.png')
LOAD_PROGRAM = resource_path('images/open_program/load.png')
REMOVE_PROGRAM = resource_path('images/open_program/remove.png')
OPEN_PROGRAM_TOPIC = resource_path('images/open_program/topic.png')

ALG2D = resource_path('images/alg_param/alg2d.png')
OPEN_PROGRAM_YES = resource_path('images/prompt_box/open_program_yes.png')
OPEN_PROGRAM_CANCEL = resource_path('images/prompt_box/open_program_cancel.png')
ADD_CHECKED_YES = resource_path('images/prompt_box/add_check_yes.png')
PROGRAM_LOADING = resource_path('images/prompt_box/program_loading.png')
ADD_WINDOW = resource_path('images/click_menu/add_window.png')

SQUARE_POSITIONING = resource_path('images/add_check_window/check_type/common/square_positioning.png')
X_OFFSET = resource_path('images/add_check_window/drawback/ontology/x_offset.png')
Y_OFFSET = resource_path('images/add_check_window/drawback/ontology/y_offset.png')
DEFAULT = resource_path('images/add_check_window/drawback/ontology/default.png')

AOI_TOPIC = resource_path('images/gui/topic.png')
OPEN_PROGRAM = resource_path('images/gui/open_program.png')
BOARD_BOARD = resource_path('images/gui/board/auto.png')
EDIT_BACK_BUTTON = resource_path('images/gui/edit/back.png')
GUI_EDIT_LIGHT = resource_path('images/gui/edit/light.png')
GUI_EDIT_LIGHT_MENU = resource_path('images/gui/edit/light_menu.png')
TEST_WINDOW = resource_path('images/gui/edit/test_window.png')
TEST_COMPONENT = resource_path('images/gui/edit/test_component.png')

PYQT_ICON = resource_path('gui/resources/sinic_tek.jpg')
