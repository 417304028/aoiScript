import tkinter as tk
from tkinter import ttk
from threading import Thread, current_thread
from loguru import logger
import importlib
from scripts import yjk, lxbj, jbgn, kjj, spc, tccs
from utils import running_event, test_case_status
import ctypes
import inspect
from utils import setup_logger
import sys
import win32event
import win32api
import winerror

# 创建一个全局的命名互斥体，确保同一时间只能有一个脚本控制器窗口打开
mutex = win32event.CreateMutex(None, False, "Global\\ScriptControllerMutex")
if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    logger.error("脚本控制器窗口已经在运行，不能同时打开多个实例。")
    sys.exit(0)

module_names = {
    "scripts.yjk": "元件库用例",
    "scripts.lxbj": "离线编辑用例",
    "scripts.jbgn": "基本功能用例",
    "scripts.kjj": "快捷键用例",
    "scripts.spc": "SPC用例",
    "scripts.tccs": "调参测试用例",
    "scripts.zxtc": "在线调参用例"
}

def _async_raise(tid, exctype):
    """Raises an exception in the threads with id tid"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)

def update_method_status(method_name):
    status = test_case_status.get(method_name, "unknown")
    for i in range(method_listbox.size()):
        if method_listbox.get(i) == method_name:
            method_listbox.selection_clear(i)  # 取消选中
            if status == "success":
                method_listbox.itemconfig(i, {'bg':'green'})
            elif status == "failed":
                method_listbox.itemconfig(i, {'bg':'red'})
            else:
                method_listbox.itemconfig(i, {'bg':'white'})

def run_all():
    selected_module_key = next(key for key, value in module_names.items() if value == module_var.get())
    module = importlib.import_module(selected_module_key)
    methods = [getattr(module, func) for func in dir(module) if callable(getattr(module, func)) and func.startswith(selected_module_key.split('.')[-1])]
    
    def run_method(index):
        if index < len(methods) and running_event.is_set():
            method = methods[index]
            current_method_var.set(method.__name__)
            root.after(3000, lambda: execute_method(method, index))
        else:
            root.after(0, update_status, "所有方法执行完毕")
            root.after(10000, lambda: update_status(""))
            current_method_var.set("")
    
    def execute_method(method, index):
        def run_in_thread():
            try:
                result, error = method()
                if running_event.is_set():
                    root.after(0, update_status, f"{method.__name__} 方法执行完毕")
                    root.after(10000, lambda: update_status(""))
                    root.after(0, update_method_status, method.__name__)
                    root.after(3000, lambda: run_method(index + 1))
            except SystemExit:
                logger.info(f"{method.__name__} 方法被终止")
            except Exception as e:
                logger.error(f"{method.__name__} 方法执行出错: {e}")
        global current_thread
        current_thread = Thread(target=run_in_thread)
        current_thread.start()

    run_method(0)

def run_selected(method_names):
    selected_module_key = next(key for key, value in module_names.items() if value == module_var.get())
    module = importlib.import_module(selected_module_key)
    
    def run_method(index):
        if index < len(method_names) and running_event.is_set():
            method_name = method_names[index]
            method = getattr(module, method_name)
            current_method_var.set(method.__name__)
            root.after(3000, lambda: execute_method(method, index))
        else:
            root.after(0, update_status, "选中的方法执行完毕")
            root.after(5000, lambda: update_status(""))
    
    def execute_method(method, index):
        def run_in_thread():
            try:
                result, error = method()
                if running_event.is_set():
                    root.after(0, update_status, f"{method.__name__} 方法执行完毕")
                    root.after(10000, lambda: update_status(""))
                    root.after(0, update_method_status, method.__name__)
                    root.after(3000, lambda: run_method(index + 1))
            except SystemExit:
                logger.info(f"{method.__name__} 方法被终止")
            except Exception as e:
                logger.error(f"{method.__name__} 方法执行出错: {e}")
        global current_thread
        current_thread = Thread(target=run_in_thread)
        current_thread.start()

    run_method(0)

def start_all():
    global thread
    try:
        if thread and thread.is_alive():
            logger.warning("已有一个用例脚本在运行，请等待其结束后再启动新的用例脚本")
            return
    except NameError:
        thread = None
    running_event.set()
    test_case_status.clear()  # 清理状态
    root.iconify()
    thread = Thread(target=run_all)
    thread.start()

def start_selected():
    global thread
    try:
        if thread and thread.is_alive():
            logger.warning("已有一个用例脚本在运行，请等待其结束后再启动新的用例脚本")
            return
    except NameError:
        thread = None
    running_event.set()
    test_case_status.clear()  # 清理状态
    root.iconify()
    selected_indices = method_listbox.curselection()
    selected_methods = [method_listbox.get(i) for i in selected_indices]
    thread = Thread(target=lambda: run_selected(selected_methods))
    thread.start()

def terminate_execution():
    global thread, current_thread
    running_event.clear()
    if current_thread and current_thread.is_alive():
        logger.info("正在终止当前运行的用例函数")
        stop_thread(current_thread)  # 强制终止当前线程
    if thread and thread.is_alive():
        thread.join(timeout=5)  # 等待线程结束，设置超时时间为5秒
        if thread.is_alive():
            logger.error("线程未能在预期时间内结束")
            stop_thread(thread)  # 强制终止线程
    update_status("脚本已终止")

def update_status(message):
    status_var.set(message)
    root.update()

def on_closing():
    """Handle the window closing event to ensure all threads are terminated."""
    terminate_execution()  # Terminate all running threads
    # 确保释放所有资源
    # 例如，关闭所有打开的文件句柄或其他资源
    root.quit()  # 退出主循环
    root.destroy()  # 关闭Tkinter窗口

# 创建主窗口
root = tk.Tk()
root.title("脚本控制器")
root.geometry("510x555")  # 调整窗口大小以确保完全显示

# 捕获窗口关闭事件
root.protocol("WM_DELETE_WINDOW", on_closing)

# 配置样式
style = ttk.Style()
style.theme_use('clam')
style.configure('.', font=('Helvetica', 10))
style.configure('TButton', font=('Helvetica', 10), padding=10, relief='raised', borderwidth=2)
style.configure('TLabel', font=('Helvetica', 10), padding=6)
style.configure('TEntry', font=('Helvetica', 10), padding=6)

# 状态和方法执行信息显示区域
info_frame = ttk.Frame(root)
info_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

status_var = tk.StringVar()
status_label = ttk.Label(info_frame, textvariable=status_var, style='TLabel')
status_label.grid(row=0, column=0, columnspan=2, sticky="ew")

current_method_var = tk.StringVar()
current_method_label = ttk.Label(info_frame, text="目前执行：")
current_method_label.grid(row=1, column=0, sticky="w")
current_method_entry = ttk.Entry(info_frame, textvariable=current_method_var, state='readonly')
current_method_entry.grid(row=1, column=1, sticky="ew")

# 下拉框选择模块
module_var = tk.StringVar(root)
default_module = "scripts.yjk"
module_var.set(module_names[default_module])

module_dropdown = ttk.OptionMenu(root, module_var, module_names[default_module], *module_names.values())
module_dropdown.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

# 方法列表区域
list_frame = ttk.Frame(root)
list_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsw")

method_listbox = tk.Listbox(list_frame, height=20, selectmode='multiple', width=50)  # 调整列表框大小
method_listbox.grid(row=0, column=0, sticky="nsw")

# 按钮区域
button_frame = ttk.Frame(root)
button_frame.grid(row=3, column=1, padx=10, pady=10, sticky="nse")

run_all_button = ttk.Button(button_frame, text="执行全部", command=start_all)
run_all_button.grid(row=0, column=0, padx=5, pady=5)

run_selected_button = ttk.Button(button_frame, text="执行选中", command=start_selected)
run_selected_button.grid(row=1, column=0, padx=5, pady=5)

stop_button = ttk.Button(button_frame, text="终止执行", command=terminate_execution)
stop_button.grid(row=2, column=0, padx=5, pady=5)

def update_methods():
    method_listbox.delete(0, tk.END)
    friendly_name = module_var.get()
    selected_module = next(key for key, value in module_names.items() if value == friendly_name)
    module = importlib.import_module(selected_module)
    method_names = [getattr(module, func) for func in dir(module) if callable(getattr(module, func)) and func.startswith(selected_module.split('.')[-1])]
    for method_name in method_names:
        method_listbox.insert(tk.END, method_name.__name__)

# 当下拉框选择改变时更新方法列表
module_var.trace('w', lambda *args: update_methods())

# 初始化方法列表
update_methods()

setup_logger()

root.mainloop()