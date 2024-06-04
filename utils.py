import os
import sys
import time
import psutil
import win32gui
import win32com
import win32con
import pythoncom
import pyautogui
import config

# from pyautogui import locateOnScreen, click
# import easyocr
# import win32com.client


def check_and_launch_aoi():
    aoi_running = any("AOI.exe" == p.name() for p in psutil.process_iter())
    if not aoi_running:
        print("AOI程序未运行,正在启动...")
        os.startfile(config.AOI_EXE_PATH)
        print("等待AOI程序启动...")
        wait_for_symbol(config.TOPIC_PATH, 60)
    else:
        print("AOI已启动，正在恢复正常窗口")
        hwnd_list = []
        pythoncom.CoInitialize()
        shell = win32com.client.Dispatch('WScript.Shell')
        shell.SendKeys('%')

        def enum_windows_proc(hwnd, lParam):
            window_text = win32gui.GetWindowText(hwnd)
            parent_hwnd = win32gui.GetParent(hwnd)
            # ！！！！！！！！！版本变动后这边可能要改！！！！！！！！！！
            if 'Sinic-Tek 3D AOI' in win32gui.GetWindowText(hwnd) and win32gui.GetClassName(
                    hwnd) == 'WindowsForms10.Window.8.app.0.27829a8_r8_ad1' and parent_hwnd == 0:
                class_name = win32gui.GetClassName(hwnd)
                print(f"窗口标题: '{window_text}'，类名: '{class_name}'")
                hwnd_list.append(hwnd)

        win32gui.EnumWindows(enum_windows_proc, None)

        # 检查窗口状态并适当调整
        for hwnd in hwnd_list:
            # 获取窗口状态 这几行会导致窗口大小异常！！！！！！！！
            window_placement = win32gui.GetWindowPlacement(hwnd)
            print(hwnd)
            # 确保窗口是正常大小
            # win32gui.MoveWindow(hwnd, 0, 0, 1920, 1040, True)
            # win32gui.ShowWindow(hwnd, win32con.SW_SHOWNA) #打不开
            # win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  #窗口异常
            # win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL) #窗口异常
            win32gui.ShowWindow(hwnd, win32con.SW_SHOWMAXIMIZED)
            win32gui.ShowWindow(hwnd, win32con.SW_SHOWNOACTIVATE)
            win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
        wait_for_symbol(config.TOPIC_PATH, 20)


def wait_for_symbol(symbol, timeout):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            if pyautogui.locateOnScreen(symbol) is not None:
                print("已确认" + symbol + "存在")
                # click_button(symbol)
                return True
        except pyautogui.ImageNotFoundException:
            print("正在识别" + symbol)
        except Exception as e:
            sys.exit(f"发生异常: {e}")
    return False


# 5s内尝试识别并点击按钮
def click_button(image_path, num):
    print("寻找按钮并点击..." + image_path)
    start_time = time.time()
    while time.time() - start_time < 5:
        try:
            if num == 1:
                pyautogui.click(image_path)
                print("点击" + image_path + "成功")
                break
            elif num == 2:
                pyautogui.doubleClick(image_path)
                print("双击" + image_path + "成功")
                break
        except Exception as e:
            print(f"尝试点击{image_path}时报错: 错误信息: {e}")
            time.sleep(1)
