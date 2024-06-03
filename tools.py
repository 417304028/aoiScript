
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