import re
import os
import shutil
import pyautogui

try:
    # 读取 yjk.py 并提取所有函数名及其系列编号
    with open('scripts/yjk.py', 'r', encoding='utf-8') as file:
        content = file.read()

    # 使用正则表达式提取函数名和系列编号
    # 匹配函数定义，同时捕获前面可能存在的空白字符和注释符号
    functions = re.findall(r'(?m)^(?:\s*#)?\s*def (yjk_(\d{3})_(\d{2}))\(', content)
    series_dict = {}
    for func, series, sub_series in functions:
        # 检查是否被注释
        match = re.search(r'(?m)^(.*)def ' + re.escape(func) + r'\(', content)
        if match and '#' in match.group(1):
            continue  # 如果函数前有注释符号，则跳过

        series_key = f"{series}_{sub_series[0]}"  # 使用系列号和子系列的第一个数字作为键
        if series_key not in series_dict:
            series_dict[series_key] = []
        series_dict[series_key].append(func)

    # 主执行文件模板
    main_template = """
from scripts import yjk
from utils import setup_logger, logger
import pyautogui
import keyboard  # 导入keyboard库用于监听键盘事件
import os

def stop_program():
    print("程序即将停止...")
    os._exit(0)  # 使用os._exit(0)来立即终止程序

if __name__ == '__main__':
    setup_logger()
    {function_calls}
    keyboard.add_hotkey('ctrl+w', stop_program)  # 设置当按下Ctrl+W时调用stop_program函数
    keyboard.wait('esc')  # 使用esc键作为程序运行的终止条件
"""

    output_path = "D:\\work\\output_bbb"
    build_path = "D:\\work\\build"
    temp_path = "D:\\work\\temp"

    # 确保输出目录和临时目录存在
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)

    # 创建最终_internal文件夹的路径
    final_internal_path = os.path.join(output_path, '_internal')

    # 为每个系列生成一个主执行文件并编译
    for series_key, funcs in series_dict.items():
        function_calls = "\n    ".join([f"logger.info(f'目前执行到 {func} 方法'); pyautogui.alert(f'目前执行到 {func} 方法', timeout=3000); yjk.{func}()" for func in funcs])
        main_content = main_template.format(function_calls=function_calls)
        main_filename = f'main_{series_key}.py'
        with open(main_filename, 'w', encoding='utf-8') as f:
            f.write(main_content)

        # 使用 PyInstaller 编译主执行文件
        os.system(f'pyinstaller --onedir --clean --noconsole --add-data "images;images" --hidden-import=cv2 --distpath "{temp_path}" --workpath "{build_path}" {main_filename}')
        os.remove(main_filename)

        # 移动生成的 .exe 文件到 output 目录，并重命名为 yjk_001_0x.exe 格式
        exe_source_path = os.path.join(temp_path, f'main_{series_key}', f'main_{series_key}.exe')
        exe_dest_path = os.path.join(output_path, f'yjk_{series_key}.exe')
        shutil.move(exe_source_path, exe_dest_path)

        # 合并新的 _internal 文件夹内容到最终的 _internal 文件夹
        temp_internal_path = os.path.join(temp_path, f'main_{series_key}', '_internal')
        if os.path.exists(temp_internal_path):
            if not os.path.exists(final_internal_path):
                shutil.copytree(temp_internal_path, final_internal_path)
            else:
                # 合并文件夹内容
                for item in os.listdir(temp_internal_path):
                    s = os.path.join(temp_internal_path, item)
                    d = os.path.join(final_internal_path, item)
                    if os.path.isdir(s):
                        if os.path.exists(d):
                            shutil.rmtree(d)
                        shutil.copytree(s, d)
                    else:
                        shutil.copy2(s, d)

        # 删除临时生成的文件夹
        shutil.rmtree(os.path.join(temp_path, f'main_{series_key}'))

    # 删除临时目录
    shutil.rmtree(temp_path)

    # 删除当前项目下所有.spec文件
    for spec_file in os.listdir('.'):
        if spec_file.endswith('.spec'):
            os.remove(spec_file)

    # 显示完成弹框
    pyautogui.alert('所有系列已编译为可执行文件，并共享一个_internal文件夹。', title='编译完成')

except Exception as e:
    print(f"发生错误：{e}")

print("所有系列已编译为可执行文件，并共享一个_internal文件夹。")




