import datetime
import difflib
import sys
from tkinter import filedialog
sys.coinit_flags = 2
import shutil
import subprocess
import zipfile
import tkinter as tk
from tkinter import messagebox
import cv2, easyocr
import numpy as np
import psutil
import utils, config
from loguru import logger
import pyautogui
import os,time
from PIL import Image as PILImage
import win32gui, win32con
import threading

def build_script_controller():
    utils.setup_logger()
    # 检测D:\\work\\aoi_output目录是否存在并清空其内部所有文件
    output_dir = r"D:\work\aoi_output"

    if os.path.exists(output_dir):
        for filename in os.listdir(output_dir):
            file_path = os.path.join(output_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path, ignore_errors=True)  # 强制删除文件夹及其内容
            except Exception as e:
                logger.error(f"无法删除文件 {file_path}: {e}")
    else:
        os.makedirs(output_dir)

    # 如果zip文件存在，先删除
    zip_filename = r"D:\work\aoi_output\script_controller_" + datetime.datetime.now().strftime('%Y%m%d') + ".zip"
    if os.path.exists(zip_filename):
        try:
            os.remove(zip_filename)
        except Exception as e:
            logger.error(f"无法删除zip文件 {zip_filename}: {e}")
    aoi_script_dir = r"D:\work\aoiScript"
    if os.path.exists(aoi_script_dir):
        for file in os.listdir(aoi_script_dir):
            if file.endswith(".csv") or file.endswith(".spec"):
                os.remove(os.path.join(aoi_script_dir, file))


    # 执行pyinstaller命令
    command = [
        "pyinstaller", "--onedir", "--clean", "--noconsole",
        "--add-data", "images;images", 
        "--add-data", "C:\\Users\\Sinictek\\.EasyOCR\\model;model",
        "--add-data", "aoi_config;aoi_config", 
        "--add-data", "rv_config;rv_config",
        "--distpath", "D:\\work\\aoi_output", "--workpath", "D:\\work\\build", "script_controller.py", "--noconfirm"
    ]
    subprocess.run(command, check=True)

    # 确保编译完成后再打包为zip文件
    if os.path.exists(output_dir):
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(output_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    # 跳过已经存在的ZIP文件
                    if file_path == zip_filename:
                        continue
                    arcname = os.path.relpath(file_path, output_dir)
                    zipf.write(file_path, arcname)
    root = tk.Tk()
    root.attributes('-topmost', True)  # 置顶窗口
    messagebox.showinfo("通知", "zip文件已创建", master=root)
    root.after(5000, root.destroy)  # 5秒后自动关闭弹窗

    # 删除指定路径下的zip文件
    target_dir = "//192.168.201.215/bk/install/AOI软件/自动化测试/版本更新"
    target_zip_path = os.path.join(target_dir, f"script_controller_{datetime.datetime.now().strftime('%Y%m%d')}.zip")

    if os.path.exists(target_zip_path):
        try:
            os.remove(target_zip_path)
        except Exception as e:
            logger.error(f"无法删除目标路径下的zip文件 {target_zip_path}: {e}")

    # 五分钟内不停传输 直到复制完成
    start_time = time.time()
    while time.time() - start_time < 300:
        logger.info("开始尝试传输文件至215")
        try:
            shutil.copy(zip_filename, target_zip_path)
            logger.info("文件复制成功")
            break
        except Exception as e:
            logger.error(f"无法复制zip文件到目标路径 {target_zip_path}: {e}")
            time.sleep(3)  # 等待3秒后重试

    if time.time() - start_time >= 300:
        logger.error("五分钟内未能成功发送文件")
    logger.info("发送文件完成")
    root = tk.Tk()
    root.attributes('-topmost', True)  # 置顶窗口
    messagebox.showinfo("通知", "编译完成", master=root)
    root.after(5000, root.destroy)  # 5秒后自动关闭弹窗

# import ctypes
# def hide_taskbar():
#     try:
#         taskbar_hwnd = win32gui.FindWindow("Shell_TrayWnd", None)
#         if taskbar_hwnd:
#             win32gui.ShowWindow(taskbar_hwnd, win32con.SW_HIDE)
#             logger.info("任务栏已隐藏")
#         else:
#             logger.error("未找到任务栏窗口")
#     except Exception as e:
#         logger.error(f"隐藏任务栏时发生错误: {e}")
# def show_taskbar():
#     try:
#         taskbar_hwnd = win32gui.FindWindow("Shell_TrayWnd", None)
#         if taskbar_hwnd:
#             win32gui.ShowWindow(taskbar_hwnd, win32con.SW_SHOW)
#             logger.info("任务栏已显示")
#         else:
#             logger.error("未找到任务栏窗口")
#     except Exception as e:
#         logger.error(f"显示任务栏时发生错误: {e}")



if __name__ == "__main__":
    utils.setup_logger()
    build_script_controller()


