# 打开批量编辑
import time

import pyautogui
from main import JOB_PATH, batch_djb_edit, check_and_launch_aoi, click_button, click_open_label, input_path, open_and_output_file, skip_warning

# 等到无算法提示的出现，点击确认，否则要等十秒
def skip_warning(image_path):
    warning = None
    timeout = 50  # 最多等待10秒
    start_time = time.time()

    while warning is None and (time.time() - start_time) < timeout:
        try:
            warning = pyautogui.locateOnScreen(image_path)
            if warning is not None:
                print("找到按钮" + image_path)
                click(warning)
                print("操作成功")
                break
        except:
            print("未找到" + image_path)
        time.sleep(1)  # 每次检查间隔1秒
    if warning is None:
        sys.exit("在指定时间内未找到图片" + image_path)

# 模拟键盘操作，打开djb批量编辑界面
def batch_djb_edit():
    print("按键")
    pyautogui.hotkey('ctrl', 'shift', 'p')
    time.sleep(1)
    pyautogui.press('enter')
    print("进入djb批量编辑界面")

# 点击打开DJB文件文本框
def click_open_label():
    pyautogui.click(180, 210)


def input_path(content):
    print("输入路径")
    pyautogui.typewrite(content)  # 输入文本
    print("输入完毕")



# 把带有hardware.png的一个一个点击，会有一个成功的提示，表示已导出，点击确定。然后复制一份文件夹，开始下一份文件夹的复制
def open_and_output_file():
    click('open.png')

    # 等待加载
    loading = None
    timeout = 30
    start_time = time.time()

    # 确认加载完成
    while loading is None and (time.time() - start_time) < timeout:
        try:
            loading = pyautogui.locateOnScreen('hardware.png')
            if loading is not None:
                print("加载完,准备djb处理")
                break
        except:
            print("加载中———")
        time.sleep(1)  # 每次检查间隔1秒
    if loading is None:
        sys.exit("在指定时间内未找到hardware.png,可能加载失败")

    # 加载完成后再导出
    # 不重复依次点击所有的hardware.png按钮，并导出，确保导出成功后点击导出成功的提示按钮，再进行下一个hardware的导出
    seen_buttons = set()  # 用于存储已点击的按钮位置
    hardware_buttons = list(pyautogui.locateAllOnScreen('hardware.png'))
    for hardware_button in hardware_buttons:
        button_position = pyautogui.center(hardware_button)
        if button_position not in seen_buttons:
            print("点击芯片")
            x, y = button_position
            pyautogui.click(x, y)
            print(f"点击位置: ({x}, {y})")
            print("点击导出")
            click_button('export.png')
            time.sleep(2)

            # 加载成功，关闭提示
            export_success = None
            start_time = time.time()
            timeout = 3
            while export_success is None and (time.time() - start_time) < timeout:
                print("查找导出成功提示")
                export_success = locateOnScreen('export_success.png')
                if export_success:
                    pyautogui.click(export_success)
                    print("导出成功，点击确认")
                    seen_buttons.add(button_position)
            if export_success is None:
                print("未找到导出成功提示")


def aoi_batch_djb_edit():
    # 打开aoi
    check_and_launch_aoi()
    skip_warning("images/login/done.png")
    print("等待5秒界面刷新")
    time.sleep(5)
    # 开始djb批量编辑
    batch_djb_edit()
    time.sleep(3)
    click_open_label()
    input_path(JOB_PATH)
    # 导入文件夹，一个一个导出djb
    open_and_output_file()
    click_button('export.png')
