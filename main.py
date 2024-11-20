import ctypes
import subprocess
import config, time
import utils
from utils import logger, setup_logger, check_and_launch_rv
from pywinauto import Application
import win32gui
import win32con
import re

if __name__ == "__main__":
    setup_logger()
    # 使用subprocess启动程序
    try:
        subprocess.run([config.SPC_EXE_PATH], check=True)
        logger.info("SPC程序已启动")
    except subprocess.CalledProcessError as e:
        logger.error(f"启动SPC程序时发生错误: {e}")
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
