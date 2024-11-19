import ctypes
import config, time
import utils
from utils import logger, setup_logger, check_and_launch_rv
from pywinauto import Application
import win32gui
import win32con
import re

class WindowMgr:
    """Encapsulates some calls to the winapi for window management"""
    def __init__(self):
        """Constructor"""
        self._handle = None

    def find_window_wildcard(self, wildcard):
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def _window_enum_callback(self, hwnd, wildcard):
        '''Pass to win32gui.EnumWindows() to check all the opened windows'''
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
            self._handle = hwnd

    def set_foreground(self):
        """put the window in the foreground"""
        if self._handle > 0:
            win32gui.SendMessage(self._handle, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
            win32gui.SetForegroundWindow(self._handle)
            return True
        return False

if __name__ == "__main__":
    setup_logger()
    utils.check_checkbox_status_before_text("打开左右循环")
    # # 检测D:\\work\\aoi_output目录是否存在并清空其内部所有文件
    # output_dir = "D:\\work\\aoi_output"
    # if os.path.exists(output_dir):
    #     for filename in os.listdir(output_dir):
    #         file_path = os.path.join(output_dir, filename)
    #         try:
    #             if os.path.isfile(file_path) or os.path.islink(file_path):
    #                 os.unlink(file_path)
    #             elif os.path.isdir(file_path):
    #                 shutil.rmtree(file_path)
    #         except Exception as e:
    #             logger.error(f"无法删除文件 {file_path}: {e}")
    # else:
    #     os.makedirs(output_dir)

    # # 执行pyinstaller命令
    # command = [
    #     "pyinstaller", "--onedir", "--clean", "--noconsole",
    #     "--add-data", "images;images", "--distpath", output_dir,
    #     "--workpath", "D:\\work\\build", "script_controller.py", "--noconfirm"
    # ]
    # subprocess.run(command, check=True)

    # # 打包为zip文件
    # zip_filename = "D:\\work\\aoi_output\\script_controller.zip"
    # shutil.make_archive(zip_filename.replace('.zip', ''), 'zip', output_dir)

    # logger.info("end")
