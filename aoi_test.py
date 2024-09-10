import tkinter as tk
from tkinter import ttk  # 导入ttk模块
from threading import Thread
from loguru import logger
import time
import importlib
from scripts import yjk, lxbj
from utils import auto_close_msgbox

module_names = {
    "scripts.yjk": "元件库用例",
    "scripts.lxbj": "离线编辑用例"
}

def run_all():
    global running
    running = True
    selected_module = module_var.get()
    module = importlib.import_module(selected_module)
    methods = [getattr(module, func) for func in dir(module) if callable(getattr(module, func)) and func.startswith(selected_module.split('.')[-1])]
    for method in methods:
        if not running:  # 检查是否应该停止执行
            break
        current_method_var.set(method.__name__)
        auto_close_msgbox(root, f"即将执行: {method.__name__}", "方法执行", 3000)
        time.sleep(3)
        method()
        root.after(0, update_status, f"{method.__name__} 方法执行完毕")
        root.after(10000, lambda: update_status(""))
        time.sleep(3)
    root.after(0, update_status, "所有方法执行完毕")
    root.after(10000, lambda: update_status(""))
    current_method_var.set("")

def run_selected(method_names):
    global running
    running = True
    selected_module = module_var.get()
    module = importlib.import_module(selected_module)
    for method_name in method_names:
        if not running:
            break
        method = getattr(module, method_name)
        current_method_var.set(method.__name__)
        auto_close_msgbox(root, f"即将执行: {method.__name__}", "方法执行", 3000)
        time.sleep(3)
        method()
        root.after(0, update_status, f"{method.__name__} 方法执行完毕")
        root.after(5000, lambda: update_status(""))
        time.sleep(3)
    root.after(0, update_status, "选中的方法执行完毕")
    root.after(5000, lambda: update_status(""))

def start_all():
    global thread
    root.iconify()  # 缩小窗口
    thread = Thread(target=run_all)
    thread.start()

def start_selected():
    global thread
    root.iconify()  # 缩小窗口
    selected_indices = method_listbox.curselection()
    selected_methods = [method_listbox.get(i) for i in selected_indices]
    thread = Thread(target=lambda: run_selected(selected_methods))
    thread.start()

def terminate_execution():
    global running, thread
    running = False  # 设置运行标志为False，通知所有方法停止执行
    if thread.is_alive():
        thread.join()  # 等待线程自然结束
        if thread.is_alive():
            logger.error("线程未能在预期时间内结束")
    update_status("脚本已终止")  # 更新状态显示脚本已终止

def update_status(message):
    status_var.set(message)
    root.update()

# 创建主窗口
root = tk.Tk()
root.title("脚本控制器")
root.geometry("300x350")  # 调整窗口大小

# 配置样式
style = ttk.Style()
style.theme_use('clam')  # 使用clam主题

# 设置整体样式
style.configure('.', font=('Helvetica', 8))
style.configure('TButton', font=('Helvetica', 10), padding=6, relief='raised', borderwidth=1)
style.configure('TEntry', font=('Helvetica', 8), padding=6, relief='flat', borderwidth=0)
style.configure('TLabel', font=('Helvetica', 8), padding=6)
style.configure('TMenubutton', font=('Helvetica', 12))

# 状态和方法执行信息显示区域
info_frame = ttk.Frame(root, style='TFrame')
info_frame.pack(side=tk.TOP, fill=tk.X)

status_var = tk.StringVar()
status_label = ttk.Label(info_frame, textvariable=status_var, style='TLabel')
status_label.pack(side=tk.LEFT, fill=tk.X)

# 添加标签和Entry显示当前执行的方法名
current_method_var = tk.StringVar()
current_method_label = ttk.Label(info_frame, text="目前执行：", style='TLabel', font=('Helvetica', 10))  # 调整字体大小
current_method_label.pack(side=tk.LEFT)
current_method_entry = ttk.Entry(info_frame, textvariable=current_method_var, style='TEntry', state='readonly')
current_method_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

# 下拉框选择模块
module_var = tk.StringVar(root)
default_module = "scripts.yjk"  # 默认模块
module_var.set(module_names[default_module])  # 设置默认显示的用户友好名称

# 创建下拉菜单，使用映射后的友好名称
module_dropdown = ttk.OptionMenu(root, module_var, module_names[default_module], *module_names.values(), style='TMenubutton')
module_dropdown.pack(side=tk.TOP, fill=tk.X)

# 方法列表区域
list_frame = ttk.Frame(root, style='TFrame')
list_frame.pack(side=tk.LEFT, fill=tk.Y)

method_listbox = tk.Listbox(list_frame, height=20, selectmode='multiple', width=20, borderwidth=0, highlightthickness=0)
method_listbox.pack(padx=5, pady=5)

def update_methods():
    method_listbox.delete(0, tk.END)
    friendly_name = module_var.get()
    # 反向查找模块名
    selected_module = next(key for key, value in module_names.items() if value == friendly_name)
    module = importlib.import_module(selected_module)
    method_names = [getattr(module, func) for func in dir(module) if callable(getattr(module, func)) and func.startswith(selected_module.split('.')[-1])]
    for method_name in method_names:
        method_listbox.insert(tk.END, method_name.__name__)

# 当下拉框选择改变时更新方法列表
module_var.trace('w', lambda *args: update_methods())

# 按钮区域
button_frame = ttk.Frame(root, style='TFrame')
button_frame.pack(side=tk.RIGHT, fill=tk.Y)

run_all_button = ttk.Button(button_frame, text="执行全部", command=start_all, style='TButton')
run_all_button.pack(pady=5)

run_selected_button = ttk.Button(button_frame, text="执行选中", command=start_selected, style='TButton')
run_selected_button.pack(pady=5)

stop_button = ttk.Button(button_frame, text="终止执行", command=terminate_execution, style='TButton')
stop_button.pack(pady=5)

root.mainloop()

