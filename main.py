import datetime
import difflib
import random
import sys
from tkinter import filedialog
sys.coinit_flags = 2
import shutil
import subprocess
import zipfile
import tkinter as tk
from tkinter import messagebox
import cv2
import numpy as np
import psutil
import utils, config
from loguru import logger
import pyautogui
import os, time
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
            if file.endswith(".spec"):
                os.remove(os.path.join(aoi_script_dir, file))
        
        # 删除csv_files文件夹
        csv_files_dir = os.path.join(aoi_script_dir, "csv_files")
        if os.path.exists(csv_files_dir):
            shutil.rmtree(csv_files_dir, ignore_errors=True)
        
        # 删除__pycache__文件夹
        pycache_dir = os.path.join(aoi_script_dir, "__pycache__")
        if os.path.exists(pycache_dir):
            shutil.rmtree(pycache_dir, ignore_errors=True)

    # 执行pyinstaller命令
    command = [
        "pyinstaller", "--onedir", "--clean", "--noconsole",
        # "pyinstaller", "--onedir", "--console",
        "--add-data", "images;images",
        "--add-data", "aoi_config;aoi_config",
        "--add-data", "rv_config;rv_config",
        "--add-data", "D:\\environment\\Miniconda3\\Lib\\site-packages\\paddleocr;./paddleocr",
        "--add-data", "D:\\work\\models;./models",
        "--add-binary", "D:\\environment\\Miniconda3\\Lib\\site-packages\\paddle\\libs\\*;paddle/libs",
        "--hidden-import=paddle",
        "--hidden-import=paddle.fluid.core",
        "--hidden-import=paddleocr",
        "--hidden-import=paddleocr.tools",
        "--hidden-import=paddleocr.tools.infer",
        "--hidden-import=shapely",
        "--hidden-import=pyclipper",
        "--hidden-import=numpy",
        "--hidden-import=cv2",
        "--hidden-import=scipy",
        "--hidden-import=PIL",
        "--hidden-import=skimage.morphology",
        "--hidden-import=yaml",
        "--hidden-import=skimage",
        "--hidden-import=imgaug",
        "--hidden-import=albumentations",
        "--hidden-import=docx",
        "--distpath", "D:\\work\\aoi_output",
        "--workpath", "D:\\work\\build",
        "script_controller.py",
        "--noconfirm",
        "--debug=all"
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
    root.withdraw()  # 隐藏主窗口
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
            logger.info("文件传输成功")
            break
        except Exception as e:
            logger.error(f"无法复制zip文件到目标路径 {target_zip_path}: {e}")
            time.sleep(3)  # 等待3秒后重试

    if time.time() - start_time >= 300:
        logger.error("五分钟内未能成功发送文件")
    root = tk.Tk()
    # root.withdraw()  # 隐藏主窗口
    root.attributes('-topmost', True)  # 置顶窗口
    messagebox.showinfo("通知", "编译完成", master=root)
    root.after(5000, root.destroy)  # 5秒后自动关闭弹窗

if __name__ == "__main__":
    utils.setup_logger()
    build_script_controller()