import shutil
import sys
import tkinter as tk
from tkinter import ttk

from loguru import logger

sys.coinit_flags = 2
from scripts import yjk, lxbj, jbgn, kjj, spc, tccs, sjdc, kfzy
from utils import setup_logger,loop
import win32event
import win32api
import win32gui
import win32con
import winerror
import csv
import os
import threading
import ctypes
import time
import inspect
from threading import Thread
from tkinter import messagebox
from tkinter import filedialog
import json
import concurrent.futures
import queue
import sys


# 在文件的开头定义全局变量
global thread, csv_created, current_thread, is_running, CSV_FILE_PATH, config_window_instance, active_path, active_job_name
thread = None
current_thread = None
is_running = False  # 初始化is_running变量
test_case_status = {}
# 定义一个全局变量来标记CSV文件是否新创建
csv_created = False 
active_loop = True
# 定义一个全局锁，确保同一时间只能执行一个方法
execution_lock = threading.Lock()
# 定义一个全局变量来标记配置窗口实例
config_window_instance = None
loop_config_window_instance = None
active_path = None
active_job_name = None
gui_queue = queue.Queue()

# 创建一个全局的命名互斥体，确保同一时间只能有一个脚本控制器窗口打开
mutex = win32event.CreateMutex(None, False, "Global\\ScriptControllerMutex")
if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    logger.error("无法启动脚本控制器：已有一个实例在运行，已阻止打开多个窗口。")
    sys.exit(0)

# 定义列名
CSV_COLUMNS = [
    "设备类型", "执行系统", "用例模块", "用例编号", "执行操作",
    "执行结果", "预期结果", "执行时间", "备注"
]
def thread_it(func, *args):
    t = threading.Thread(target=func, args=args)
    t.setDaemon(True)
    t.start()
    
def initialize_csv_file_path():
    global CSV_FILE_PATH
    # 确保路径包含有效的目录
    directory = os.path.join(os.getcwd(), "csv_files")
    if not os.path.exists(directory):
        os.makedirs(directory)
    CSV_FILE_PATH = os.path.join(directory, f"operation_results_{time.strftime('%Y-%m-%d-%H-%M')}.csv")
    logger.debug(f"初始化的 CSV_FILE_PATH: {CSV_FILE_PATH}")

def create_or_read_csv():
    """
    创建或读取CSV文件。如果文件不存在，则创建一个新的文件并插入模块和方法名。
    """
    global csv_created, CSV_FILE_PATH
    logger.debug(f"Checking if CSV file exists at: {CSV_FILE_PATH}")

    def create_csv():
        if not os.path.exists(CSV_FILE_PATH):
            logger.debug("CSV file does not exist, creating a new one.")
            with open(CSV_FILE_PATH, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(CSV_COLUMNS)
                # 插入模块和方法名
                modules = {
                    "离线编辑": lxbj,
                    "元件库": yjk,
                    "基本功能": jbgn,
                    "快捷键": kjj,
                    "数据导出": sjdc,
                    "SPC": spc,
                    "调参测试": tccs,
                    "开发专用": kfzy
                }
                for module_name, module in modules.items():
                    methods = [func for func in dir(module) if callable(getattr(module, func)) and not func.startswith("__")]
                    for method in methods:
                        writer.writerow([
                            "AOI",
                            "",  # 先不管
                            module_name,
                            method,
                            "",  # 先不管
                            "",  # 先不管
                            "",  # 先不管
                            "",  # 先不管
                            ""   # 先不管
                        ])
            logger.info("成功创建新的CSV文件，并添加模块及相应的方法名称。")
            csv_created = True
        else:
            logger.info("CSV文件已存在，跳过创建和模块方法加载。")
            csv_created = False

    # 在后台线程中执行创建 CSV 的操作
    threading.Thread(target=create_csv).start()

def update_csv(module_name, method_name, operation="", result="", error_step="", execution_time="", remarks="", lock=None, device_type="", execution_system=""):
    """
    更新CSV文件，修改已有的测试结果记录。
    """
    global CSV_FILE_PATH

    if not method_name:
        logger.error("方法名不能为空")
        return

    if lock:
        lock.acquire()

    try:
        rows = []
        logger.debug(f"打开csv路径: {CSV_FILE_PATH}")
        
        with open(CSV_FILE_PATH, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            found = False
            for row in reader:
                # 当模块名为'全部'时，只根据用例编号进行匹配
                if (module_name == "全部" and row["用例编号"] == method_name) or (row["用例编号"] == method_name and row["用例模块"] == module_name):
                    found = True
                    if device_type:
                        row["设备类型"] = device_type
                    if execution_system:
                        row["执行系统"] = execution_system
                    if operation:
                        row["执行操作"] = operation
                    if result:
                        row["执行结果"] = result
                    if execution_time:
                        row["执行时间"] = execution_time
                    if remarks:
                        row["备注"] = remarks
                rows.append(row)
            
            if not found:
                raise Exception("未找到对应用例")

        logger.debug(f"准备写入CSV文件: {CSV_FILE_PATH}")
        with open(CSV_FILE_PATH, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=CSV_COLUMNS)
            writer.writeheader()
            writer.writerows(rows)
        logger.info(f"已更新CSV文件：模块 '{module_name}' 的方法 '{method_name}'。")

    except FileNotFoundError:
        logger.error(f"CSV文件未找到：{CSV_FILE_PATH}")
        handle_csv_not_found()
    except Exception as e:
        logger.error(f"更新CSV文件时发生错误：{e}，时间：{time.strftime('%Y-%m-%d %H:%M:%S')}，CSV文件的绝对路径：{os.path.abspath(CSV_FILE_PATH)}")
        handle_csv_not_found()
    finally:
        if lock:
            lock.release()

def handle_csv_not_found():
    global CSV_FILE_PATH
    csv_folder = os.path.dirname(CSV_FILE_PATH)
    logger.debug(f"CSV folder path: {csv_folder}")
    if os.path.exists(csv_folder):
        files = os.listdir(csv_folder)
        logger.info(f"CSV文件夹 '{csv_folder}' 下的文件：{files}")
        csv_files = [f for f in files if f.endswith('.csv')]
        if csv_files:
            latest_csv = max(csv_files, key=lambda f: os.path.getctime(os.path.join(csv_folder, f)))
            CSV_FILE_PATH = os.path.join(csv_folder, latest_csv)
            logger.info(f"更新CSV_FILE_PATH为最新的CSV文件：{latest_csv}")
            logger.info(f"CSV文件的绝对路径：{os.path.abspath(CSV_FILE_PATH)}")
    else:
        logger.error(f"CSV文件夹 '{csv_folder}' 不存在")

# 在程序启动时调用
initialize_csv_file_path()
create_or_read_csv()

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
class HomeScreen(tk.Frame):
    def __init__(self, master=None):
        """
        初始化HomeScreen类，创建主界面。
        """
        super().__init__(master)
        self.master = master

        # 设置窗口的尺寸
        self.master.geometry("420x410") 

        self.pack()
        self.create_widgets()

        # 在打开UI时保存AOI和RV的原有配置
        self.backup_aoi_rv_configs()

    def create_widgets(self):
        """
        创建主界面的所有控件。
        """
        self.selected_icon = tk.StringVar(value="AOI")

        style = ttk.Style()
        style.configure("TButton", font=("Segoe UI", 12), padding=10)
        style.configure("Selected.TButton", background="darkblue", foreground="white", borderwidth=2, relief="solid")
        style.configure("Unselected.TButton", background="lightgray", foreground="black", borderwidth=2, relief="ridge")

        self.label = tk.Label(self, text="自动化测试", font=("Segoe UI", 18))
        self.label.grid(row=0, column=0, columnspan=2, pady=20)

        self.icon_frame = tk.Frame(self)
        self.icon_frame.grid(row=1, column=0, columnspan=2, pady=20)

        self.aoi_icon = ttk.Button(
            self.icon_frame, text="AOI", command=self.toggle_aoi, style="Selected.TButton"
        )
        self.aoi_icon.grid(row=0, column=0, padx=20, pady=10)

        # 添加离线重复测试按钮
        self.offline_repeat_test_icon = ttk.Button(
            self.icon_frame, text="离线重复测试", command=self.toggle_offline_repeat_test, style="Unselected.TButton"
        )
        self.offline_repeat_test_icon.grid(row=0, column=1, padx=20, pady=10)

        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=2, column=0, columnspan=2, pady=20)

        self.confirm_button = ttk.Button(self.button_frame, text="确认", command=self.open_aoi_detail)
        self.confirm_button.grid(row=0, column=0, padx=20, pady=10)

        self.exit_button = ttk.Button(self.button_frame, text="退出", command=self.master.quit)
        self.exit_button.grid(row=0, column=1, padx=20, pady=10)

        # 配置按钮
        self.config_button = ttk.Button(self, text="配置", style="TButton", width=10, command=self.show_config_window)
        self.config_button.grid(row=3, column=0, columnspan=2, pady=20)

    def toggle_aoi(self):
        """
        切换AOI按钮的选中状态。
        """
        if self.selected_icon.get() == "AOI":
            self.selected_icon.set("")
            self.aoi_icon.configure(style="Unselected.TButton")
        else:
            self.selected_icon.set("AOI")
            self.aoi_icon.configure(style="Selected.TButton")
            self.offline_repeat_test_icon.configure(style="Unselected.TButton")

    def toggle_offline_repeat_test(self):
        """
        切换离线重复测试按钮的选中状态。
        """
        if self.selected_icon.get() == "离线重复测试":
            self.selected_icon.set("")
            self.offline_repeat_test_icon.configure(style="Unselected.TButton")
        else:
            self.selected_icon.set("离线重复测试")
            self.offline_repeat_test_icon.configure(style="Selected.TButton")
            self.aoi_icon.configure(style="Unselected.TButton")

    def open_aoi_detail(self):
        """
        打开AOI详情界面，并在必要时启动加载模块的线程。
        """
        if self.selected_icon.get() == "AOI":
            # 销毁当前界面
            for widget in self.master.winfo_children():
                widget.destroy()

            # 创建并显示AOIDetailScreen界面
            aoi_detail_screen = AOIDetailScreen(master=self.master)
            aoi_detail_screen.pack(fill=tk.BOTH, expand=True)

            logger.info("切换至AOI详情界面。")

            # 如果CSV文件是新创建的，则启动加载模块的线程
            if csv_created:
                threading.Thread(target=self.load_modules_in_background).start()

            # 使用全局变量获取路径信息
            logger.info(f"使用全局变量获取路径信息: path={active_path}, job_name={active_job_name}")

        elif self.selected_icon.get() == "离线重复测试":
            # 销毁当前界面
            for widget in self.master.winfo_children():
                widget.destroy()

            # 创建并显示OfflineRepeatTestScreen界面
            offline_repeat_test_screen = OfflineRepeatTestScreen(master=self.master)
            offline_repeat_test_screen.pack(fill=tk.BOTH, expand=True)

            logger.info("切换至离线重复测试界面。")

    def load_modules_in_background(self):
        """
        在后台加载所有模块的方法，并插入到CSV文件中。
        """
        try:
            total_methods = sum([len([func for func in dir(module) if callable(getattr(module, func)) and not func.startswith("__")]) for module in self.master.current_frame.modules.values()])
            loaded_methods = 0
            
            # 循环加载所有模块的方法
            for module_name, module in self.master.current_frame.modules.items():
                methods = [func for func in dir(module) if callable(getattr(module, func)) and not func.startswith("__")]
                for method in methods:
                    # 每加载一个方法
                    loaded_methods += 1
                    
                    # 插入方法到CSV
                    lock = threading.Lock()
                    t = threading.Thread(target=update_csv, args=(module_name, method, "", "", "", "", "", lock))
                    t.start()
                    t.join()
                    logger.debug(f"已加载方法 '{method}' 至模块 '{module_name}'。当前已加载 {loaded_methods}/{total_methods} 个方法。")

        except Exception as e:
            logger.error(f"在加载模块时发生异常：{e}")

    # 点开配置后的窗口
    def show_config_window(self):
        """
        显示配置窗口。
        """
        global config_window_instance
        if config_window_instance is not None and config_window_instance.winfo_exists():
            config_window_instance.lift()
            return

        try:
            config_window_instance = tk.Toplevel(self)
            config_window_instance.title("配置选项")
            config_window_instance.geometry("400x300")
            config_window_instance.transient(self)
            config_window_instance.grab_set()

            # 创建标题
            title_label = tk.Label(config_window_instance, text="执行软件", font=("Arial", 12, "bold"))
            title_label.pack(anchor="nw", padx=10, pady=10)

            # 创建按钮并绑定事件
            button_frame = tk.Frame(config_window_instance)
            button_frame.pack(anchor="nw", padx=10, pady=10)

            button1 = ttk.Button(button_frame, text="登录密码", command=self.handle_login_password)
            button1.pack(side=tk.LEFT, padx=5)

            button2 = ttk.Button(button_frame, text="循环测试", command=self.handle_loop_test)
            button2.pack(side=tk.LEFT, padx=5)

            button3 = ttk.Button(button_frame, text="覆盖设置", command=self.handle_override_settings)
            button3.pack(side=tk.LEFT, padx=5)

        except Exception as e:
            logger.error(f"创建配置窗口时发生错误: {e}")

    def handle_login_password(self):
        """
        处理登录密码按钮事件。
        """
        logger.info("登录密码按钮被点击")
        self.master.switch_frame(LoginPasswordWindow)

    def handle_loop_test(self):
        """
        处理循环测试按钮事件。
        """
        logger.info("循环测试配置按钮被点击")
        try:
            # 确保在点击循环测试按钮时，正确实例化并显示 LoopTestWindow
            LoopTestWindow(self.master)
        except Exception as e:
            logger.error(f"在循环配置按钮事件中发生错误: {e}")

    def handle_override_settings(self):
        """
        处理覆盖设置按钮事件，显示现有的配置选项。
        """
        global loop_config_window_instance
        try:
            if loop_config_window_instance is not None and loop_config_window_instance.winfo_exists():
                loop_config_window_instance.lift()
                logger.info("配置窗口已存在。")

            logger.info("创建新的配置窗口。")
            loop_config_window_instance = tk.Toplevel(self)
            loop_config_window_instance.title("覆盖设置")
            loop_config_window_instance.geometry("300x200")
            loop_config_window_instance.transient(self)
            loop_config_window_instance.grab_set()

            # # 在窗口关闭时重置 config_window_instance
            # def on_close():
            #     global config_window_instance
            #     config_window_instance = None
            #     config_window_instance.destroy()

            # config_window_instance.protocol("WM_DELETE_WINDOW", on_close)

            # 获取屏幕的宽度和高度
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()

            # 计算新窗口的居中位置
            window_width = 450
            window_height = 200
            position_right = (screen_width // 2) - (window_width // 2)
            position_down = (screen_height // 2) - (window_height // 2)

            # 设置新窗口的位置
            loop_config_window_instance.geometry(f"+{position_right}+{position_down}")

            # 使用已保存的配置状态初始化勾选框
            self.aoi_var = tk.BooleanVar(value=self.master.config_state.get("replace_aoi", True))
            aoi_check = ttk.Checkbutton(loop_config_window_instance, text="替换aoi流程配置及切换程式配置", variable=self.aoi_var)
            aoi_check.pack(anchor="w", pady=10, padx=10)

            self.rv_var = tk.BooleanVar(value=self.master.config_state.get("replace_rv", True))
            rv_check = ttk.Checkbutton(loop_config_window_instance, text="替换rv视图配置", variable=self.rv_var)
            rv_check.pack(anchor="w", pady=10, padx=10)

            # 确认按钮
            confirm_button = ttk.Button(loop_config_window_instance, text="确认", command=lambda: self.save_config(config_window_instance))
            confirm_button.pack(anchor="w", pady=20, padx=10)

        except Exception as e:
            logger.error(f"创建配置窗口时发生错误: {e}")

    def save_config(self, config_window):
        """
        保存配置状态。
        """
        self.master.config_state = {
            "replace_aoi": self.aoi_var.get(),
            "replace_rv": self.rv_var.get()
        }
        config_window.destroy()
        logger.info(f"配置已保存: {self.master.config_state}")

    def backup_aoi_rv_configs(self):
        """
        备份AOI和RV的原有配置。
        """
        try:
            # utils.close_aoi()
            # utils.close_rv()
            bin_dir = "d:\\EYAOI\\Bin"
            script_aoi_config_folder = os.path.join(os.path.dirname(sys.executable), "_internal/aoi_config")
            script_rv_config_folder = os.path.join(os.path.dirname(sys.executable), "_internal/rv_config")

            # 备份AOI配置
            aoi_config_folder = None
            if os.path.exists(os.path.join(bin_dir, "config")):
                aoi_config_folder = os.path.join(bin_dir, "config")
            elif os.path.exists(os.path.join(bin_dir, "Config")):
                aoi_config_folder = os.path.join(bin_dir, "Config")
            else:
                for d in os.listdir(bin_dir):
                    if os.path.isdir(os.path.join(bin_dir, d)) and d.lower().startswith("config"):
                        aoi_config_folder = os.path.join(bin_dir, d)
                        break

            if aoi_config_folder and os.path.exists(script_aoi_config_folder):
                aoi_backup_folder = os.path.join(bin_dir, "aoi", "copy")
                if not os.path.exists(aoi_backup_folder):
                    os.makedirs(aoi_backup_folder)
                for file_name in os.listdir(script_aoi_config_folder):
                    if file_name.endswith(".bin"):
                        src_file = os.path.join(script_aoi_config_folder, file_name)
                        dst_file = os.path.join(aoi_backup_folder, file_name)
                        try:
                            shutil.copy2(src_file, dst_file)
                            logger.info(f"已备份AOI配置文件 {file_name} 到 {aoi_backup_folder}")
                        except Exception as e:
                            logger.error(f"无法备份AOI文件: {src_file},错误内容为：{e}")

            # 备份RV配置
            rv_config_folder = None
            if os.path.exists(os.path.join(bin_dir, "config", "RV")):
                rv_config_folder = os.path.join(bin_dir, "config", "RV")
            elif os.path.exists(os.path.join(bin_dir, "Config", "RV")):
                rv_config_folder = os.path.join(bin_dir, "Config", "RV")

            if rv_config_folder and os.path.exists(script_rv_config_folder):
                rv_backup_folder = os.path.join(rv_config_folder, "copy")
                if not os.path.exists(rv_backup_folder):
                    os.makedirs(rv_backup_folder)
                for file_name in os.listdir(script_rv_config_folder):
                    src_file = os.path.join(rv_config_folder, file_name)
                    dst_file = os.path.join(rv_backup_folder, file_name)
                    if os.path.exists(src_file):
                        try:
                            shutil.copy2(src_file, dst_file)
                            logger.info(f"已备份RV配置文件 {file_name} 到 {rv_backup_folder}")
                        except Exception as e:
                            logger.error(f"无法备份RV文件: {src_file},错误：{e}")

        except Exception as e:
            logger.error(f"备份AOI和RV配置时发生错误: {e}")

class AOIDetailScreen(tk.Frame):
    def __init__(self, master=None):
        """
        初始化AOIDetailScreen类，创建详细界面。
        """
        super().__init__(master)
        self.master = master
        self.current_method_var = tk.StringVar()  # 初始化 current_method_var
        self.csv_path = CSV_FILE_PATH
        self.results = self.load_csv()
        self.displayed_rows = 20  # 初始显示的行数
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
        self.running_event = threading.Event()
        self.running_event.set()
        self.active_path = None
        self.active_job_name = None

        # 初始化配置状态
        self.config_state = {
            "replace_aoi": True,  # 默认值
            "replace_rv": True    # 默认值
        }

        # 默认加载"基本功能"模块的用例
        self.load_test_cases("基本功能")

        # 设置窗口的尺寸
        self.master.geometry("520x600")

    def load_csv(self):
        """
        加载CSV文件内容，如果文件不存在，则创建新的CSV文件。
        """
        if not os.path.exists(self.csv_path):
            with open(self.csv_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(CSV_COLUMNS)
            logger.info("CSV文件不存在，已成功创建新的CSV文件。")
            return {}
        
        results = {}
        with open(self.csv_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                module_name = row["用例模块"]
                if module_name not in results:
                    results[module_name] = []
                results[module_name].append(row)
        logger.info("成功加载CSV文件内容。")
        return results

    def save_to_csv(self, data, module_name):
        """
        保存数据到CSV文件中。
        """
        lock = threading.Lock()
        t = threading.Thread(target=update_csv, args=(module_name, data[3], data[4], data[5], data[4], data[7], data[8], lock))
        t.start()
        t.join()

    def create_widgets(self):
        """
        创建详细界面的所有控件。
        """
        style = ttk.Style()
        style.configure("TButton", font=("Segoe UI", 10), padding=(5, 10), background="#f0f0f0", foreground="#333", borderwidth=1, relief="solid")
        style.map("TButton",
                  background=[("active", "#e0e0e0"), ("disabled", "#f0f0f0")],
                  foreground=[("active", "#000"), ("disabled", "#999")])

        style.configure("Treeview", rowheight=30)  # 调整行高
        style.configure("Treeview.Heading", background="#d3d3d3", font=("Segoe UI", 10))  # 设置表头背景色和字体加粗
        style.configure("Treeview", borderwidth=1, relief="solid")  # 为表格添加边框
        style.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])  # 移除默认的边框

        # UI控件位置和大小配置
        # 系统标签
        self.system_label = ttk.Label(self, text="系统:")
        self.system_label.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="e")
        # 系统选择框
        self.system_combobox = ttk.Combobox(self, values=["全部", "UI", "中间层", "MES", "SPC", "RV"], width=15)
        self.system_combobox.current(0)  # 默认选中"全部"
        self.system_combobox.grid(row=0, column=1, padx=(5, 10), pady=10, sticky="w")

        # 用例模块字典
        self.modules = {
            "离线编辑": lxbj,
            "元件库": yjk,
            "基本功能": jbgn,
            "快捷键": kjj,
            "SPC": spc,
            "调参测试": tccs,
            "数据导出": sjdc,
            "开发专用": kfzy
        }
        # 用例标签
        self.case_label = ttk.Label(self, text="用例:")
        self.case_label.grid(row=0, column=2, padx=(10, 5), pady=10, sticky="e")
        # 用例选择框
        self.case_combobox = ttk.Combobox(self, values=["全部"] + list(self.results.keys()), width=15)
        self.case_combobox.set("基本功能")  # 默认选中基本功能
        self.case_combobox.bind("<<ComboboxSelected>>", self.on_module_selected)
        self.case_combobox.grid(row=0, column=3, padx=(5, 10), pady=10, sticky="w")

        # 搜索框
        self.search_frame = tk.Frame(self)
        self.search_frame.grid(row=1, column=0, columnspan=4, pady=15, padx=25, sticky="w")

        # 搜索框输入框
        self.search_entry = ttk.Entry(self.search_frame, width=20, foreground="gray")
        self.search_entry.insert(0, "输入用例编码搜索")
        self.search_entry.bind("<FocusIn>", self.clear_placeholder)
        self.search_entry.bind("<FocusOut>", self.add_placeholder)
        self.search_entry.bind("<KeyRelease>", self.on_search)  # 绑定实时搜索事件
        self.search_entry.grid(row=0, column=0, padx=5, ipady=6, sticky="w")

        # 搜索按钮（可选，如果实时搜索，可以移除按钮）
        self.search_button = ttk.Button(self.search_frame, text="搜索", style="TButton", width=5, command=self.search_methods)
        self.search_button.grid(row=0, column=1, padx=10, ipady=0)  # 通过ipady增加高度

        # 开始执行按钮
        self.start_button = ttk.Button(self.search_frame, text="开始执行", style="TButton", width=10, command=self.start_selected)
        self.start_button.grid(row=0, column=2, padx=10, ipady=0)  # 通过ipady增加高度

        # 停止执行按钮
        self.stop_button = ttk.Button(self.search_frame, text="停止执行", style="TButton", width=10, command=self.terminate_execution)
        self.stop_button.grid(row=0, column=3, padx=10, ipady=0)  # 通过ipady增加高度

        # 表格
        self.table = ttk.Treeview(self, columns=("编码", "状态"), show="headings", height=20, selectmode="none")
        self.table.heading("编码", text="编码")
        self.table.heading("状态", text="状态")
        self.table.grid(row=2, column=0, columnspan=4, rowspan=4, padx=10, pady=10, sticky="nsew")
        # 表格列宽
        self.table.column("编码", anchor="center", width=50)
        self.table.column("状态", anchor="center", width=50)

        # 添加垂直滚动条
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.table.yview)
        self.table.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=2, column=4, rowspan=4, sticky='ns')

        # 加载更多用例标签
        self.more_label = tk.Label(self, text="点击查询更多...", fg="blue", cursor="hand2")
        self.more_label.grid(row=6, column=0, columnspan=4, pady=15)
        self.more_label.bind("<Button-1>", self.more_info)

        # 配置行列权重，使表格扩展
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(1, minsize=100, weight=1)
        self.grid_columnconfigure(3, weight=1)

        # 加载所有模块的方法到CSV
        if csv_created:
            self.load_all_modules_to_csv()

        # 绑定单击事件以实现多选
        self.table.bind("<Button-1>", self.on_click)

        # 显示当前执行方法的标签
        current_method_label = ttk.Label(self, text="当前执行方法：")
        current_method_label.grid(row=7, column=2, padx=10, pady=10, sticky="e")
        current_method_entry = ttk.Entry(self, textvariable=self.current_method_var, state='readonly')
        current_method_entry.grid(row=7, column=3, padx=10, pady=10, sticky="w")

        # 显示所有方法已执行完毕的标签
        self.execution_complete_label = tk.Label(self, text="", fg="green", font=("Segoe UI", 12))
        self.execution_complete_label.grid(row=8, column=0, columnspan=4, pady=10)

    def on_click(self, event):
        """
        单击事件处理函数，用于实现多选。
        """
        region = self.table.identify("region", event.x, event.y)
        if region == "cell":
            item = self.table.identify_row(event.y)
            if item in self.table.selection():
                self.table.selection_remove(item)
            else:
                self.table.selection_add(item)

    def load_all_modules_to_csv(self):
        """
        加载所有模块的方法到CSV文件中。
        """
        lock = threading.Lock()
        total_methods = sum([len([func for func in dir(module) if callable(getattr(module, func)) and not func.startswith("__")]) for module in self.modules.values()])
        loaded_methods = 0

        for module_name, module in self.modules.items():
            methods = [func for func in dir(module) if callable(getattr(module, func)) and not func.startswith("__")]
            for method in methods:
                t = threading.Thread(target=update_csv, args=(module_name, method, "", "", "", "", "", lock))
                t.start()
                t.join()
                loaded_methods += 1
                logger.debug(f"已将方法 '{method}' 添加到CSV文件中，所属模块：'{module_name}'。已处理 {loaded_methods}/{total_methods} 个方法。")

        logger.info("所有模块的方法已成功加载并记录到CSV文件中。")

    def update_table(self):
        """在主线程中更新表格内容"""
        def update_table_content():
            module_name = self.case_combobox.get()
            if module_name in self.results:
                self.table.delete(*self.table.get_children())
                for result in self.results[module_name]:
                    self.table.insert("", "end", values=(result["用例编号"], result["执行结果"]))
                    logger.info(f"加载用例编号: '{result['用例编号']}'，执行结果: '{result['执行结果']}'。")
                logger.info(f"已更新表格，当前显示模块：'{module_name}'。")

        # 确保在主线程中调用更新
        self.master.after(0, update_table_content)

    def start_selected(self):
        """
        执行选中的多个方法。如果没有选择任何方法，则执行当前模块的所有方法。
        """
        def run_selected_methods():
            global thread, is_running
            if is_running:
                self.show_running_message()
                logger.warning("已有一个用例脚本在运行，请等待其结束后再启动新的用例脚本")
                return
            is_running = True
            try:
                if thread and thread.is_alive():
                    self.show_running_message()
                    logger.warning("已有一个用例脚本在运行，请等待其结束后再动新的用例脚本")
                    return
            except NameError:
                thread = None
            self.running_event.set()
            test_case_status.clear()  # 清理状态
            # self.master.iconify()
            selected_items = self.table.selection()
            selected_methods = [self.table.item(item, "values")[0] for item in selected_items]
            module_name = self.case_combobox.get()

            if module_name == "全部":
                modules = self.modules.values()
            else:
                modules = [self.modules.get(module_name)]

            if not modules:
                logger.error(f"无法执行方法：模块 '{module_name}' 未找到。")
                return

            # 如果没有选择任何方法，则执行当前模块的所有方法
            if not selected_methods:
                selected_methods = [func for module in modules for func in dir(module) if callable(getattr(module, func)) and not func.startswith("__")]
                logger.info(f"没有选择特定方法，准备执行模块 '{module_name}' 中的所有方法。")
            else:
                logger.info(f"准备执行模块 '{module_name}' 中的方法：{selected_methods}。")

            # 清除底部的执行完毕文本
            self.execution_complete_label.config(text="")

            thread = Thread(target=lambda: self.run_selected(selected_methods, modules))
            thread.start()

        # 在新线程中启动方法执行
        Thread(target=run_selected_methods).start()


    def run_selected(self, method_names, modules):
        """
        在单独的线程中顺序执行方法。
        """
        selected_module_name = self.case_combobox.get().strip()
        logger.debug(f"Combobox 选择的模块名称: {selected_module_name}")
        logger.debug(f"模块字典内容: {self.modules}")

        def run_method(index):
            if index < len(method_names) and self.running_event.is_set():
                method_name = method_names[index]
                for module in modules:
                    if hasattr(module, method_name):
                        method = getattr(module, method_name)
                        self.current_method_var.set(method.__name__)
                        self.master.after(3000, lambda: execute_method(method, index))
                        break
            else:
                # 所有方法执行完毕后，如果循环生效，就调用 loop
                self.master.after(0, self.create_prompt_box, "选中的方法执行完毕", active_loop)
                if active_loop:
                    global active_path, active_job_name
                    if active_path and active_job_name:
                        logger.info(f"调用 loop 函数，job_path: {active_path}, job_name: {active_job_name}")
                        loop(job_path=active_path, job_name=active_job_name)
                    else:
                        logger.warning("未找到生效中的路径信息，无法调用 loop。")
                else:
                    logger.warning(
                        f"未发现生效的循环job路径，无法调用 loop。active_loop:{active_loop}, active_path:{active_path}, active_job_name:{active_job_name}")
                self.execution_complete_label.config(text="所有方法已执行完毕")
                global is_running
                is_running = False
                # 更新所有方法的状态
                self.master.after(1000, lambda: self.update_status_list([test_case_status.get(method_name, '未执行') for method_name in method_names]))
                # 将界面置前
                self.master.focus_force()

                # 在方法执行完毕后恢复AOI和RV的配置
                self.restore_aoi_rv_configs()

        def execute_method(method, index):
            """
            执行单个用例方法。
            """
            def run_in_thread():
                try:
                    # 记录当前的配置状态
                    logger.info(f"当前配置状态: replace_aoi={self.config_state.get('replace_aoi', True)}, replace_rv={self.config_state.get('replace_rv', True)}")

                    # 在每次执行方法时进行配置替换
                    if self.config_state.get("replace_aoi", True):
                        logger.info("正在替换 AOI 配置")
                        # 替换aoi配置的代码
                        exe_dir = os.path.dirname(sys.executable)
                        script_aoi_config_folder = os.path.join(exe_dir, "_internal/aoi_config")
                        bin_dir = "d:\\EYAOI\\Bin"
                        aoi_config_folder = None
                        if os.path.exists(os.path.join(bin_dir, "config")):
                            aoi_config_folder = os.path.join(bin_dir, "config")
                        elif os.path.exists(os.path.join(bin_dir, "Config")):
                            aoi_config_folder = os.path.join(bin_dir, "Config")
                        else:
                            for d in os.listdir(bin_dir):
                                if os.path.isdir(os.path.join(bin_dir, d)) and d.lower().startswith("config"):
                                    aoi_config_folder = os.path.join(bin_dir, d)
                                    break
                        if aoi_config_folder and os.path.exists(script_aoi_config_folder):
                            for file_name in os.listdir(script_aoi_config_folder):
                                script_config_path = os.path.join(script_aoi_config_folder, file_name)
                                aoi_config_path = os.path.join(aoi_config_folder, file_name)
                                if os.path.isfile(aoi_config_path):
                                    os.remove(aoi_config_path)
                                shutil.copy2(script_config_path, aoi_config_path)
                                logger.info(f"已将 {file_name} 从 {script_aoi_config_folder} 替换到 {aoi_config_folder}")

                    if self.config_state.get("replace_rv", True):
                        logger.info("正在替换 RV 配置")
                        # 替换rv配置的代码
                        script_rv_config_folder = os.path.join(exe_dir, "_internal/rv_config")
                        rv_config_folder = "d:\\EYAOI\\Bin\\config\\RV"
                        if os.path.exists(script_rv_config_folder):
                            if not os.path.exists(rv_config_folder):
                                raise Exception(f"未找到RV配置文件夹{rv_config_folder}")
                            for file_name in os.listdir(script_rv_config_folder):
                                script_config_path = os.path.join(script_rv_config_folder, file_name)
                                rv_config_path = os.path.join(rv_config_folder, file_name)
                                if os.path.isfile(rv_config_path):
                                    os.remove(rv_config_path)
                                shutil.copy2(script_config_path, rv_config_path)
                                logger.info(f"已将 {file_name} 从 {script_rv_config_folder} 替换到 {rv_config_folder}")

                    # 调用方法并处理可能的无返回值情况
                    result, error = method() or (None, None)
                    if self.running_event.is_set():
                        test_case_status[method.__name__] = "成功" if not error else "失败"
                        update_csv(module_name=self.case_combobox.get(), method_name=method.__name__, result=test_case_status[method.__name__], remarks=str(error) if error else "")
                        self.master.after(0, lambda: self.update_status_list([test_case_status.get(method_name, '未执行') for method_name in method_names]))
                        self.master.after(5000, self.create_prompt_box, f"{method.__name__} 方法执行完毕", True)

                        # 确保状态更新完成后再执行下一个方法
                        self.master.after(10000, lambda: run_method(index + 1))  # 增加时间以确保任务状态更新完毕
                except SystemExit:
                    logger.info(f"{method.__name__} 方法被终止")
                except Exception as e:
                    logger.error(f"{method.__name__} 方法执行出错: {e}，CSV文件的绝对路径：{os.path.abspath(CSV_FILE_PATH)}")
                    test_case_status[method.__name__] = "失败"
                    csv_folder = os.path.dirname(CSV_FILE_PATH)
                    if os.path.exists(csv_folder):
                        files = os.listdir(csv_folder)
                        csv_files = [f for f in files if f.endswith('.csv')]
                        logger.info(f"CSV文件夹 '{csv_folder}' 下的文件：{csv_files}")
                    else:
                        logger.error(f"CSV文件夹 '{csv_folder}' 不存在")
                    
                    # 调用 update_status_list 更新表格状态
                    self.master.after(0, lambda: self.update_status_list([test_case_status.get(method_name, '未执行') for method_name in method_names]))
                    update_csv(module_name=self.case_combobox.get(), method_name=method.__name__, result=test_case_status[method.__name__], remarks=str(e))
                finally:
                    # 方法执行完毕后停止线程
                    stop_thread(current_thread)
                    self.results = self.load_csv()
                    # 更新表格状态
                    self.master.after(0, lambda: self.update_status_list([test_case_status.get(method_name, '未执行') for method_name in method_names]))

            global current_thread
            current_thread = Thread(target=run_in_thread)
            current_thread.start()

        run_method(0)
    def show_running_message(self):
        """
        显示正在执行中的提示框，三秒后消失。
        """
        running_message = tk.Toplevel(self)
        running_message.title("提示")
        message_label = tk.Label(running_message, text="正在执行中，请先停止执行", font=("Segoe UI", 12))
        message_label.pack(padx=20, pady=20)

        # 获取主窗口的位置和大小
        master_x = self.master.winfo_x()
        master_y = self.master.winfo_y()
        master_width = self.master.winfo_width()
        master_height = self.master.winfo_height()

        # 计算提示框的位置，使其居中显示
        running_message.update_idletasks()  # 更新提示框的大小信息
        message_width = running_message.winfo_width()
        message_height = running_message.winfo_height()
        x = master_x + (master_width // 2) - (message_width // 2)
        y = master_y + (master_height // 2) - (message_height // 2)
        running_message.geometry(f"+{x}+{y}")

        self.master.after(3000, running_message.destroy)


    def create_prompt_box(self, status, auto_close):
        """
        更新界面状态信息。
        """
        if active_loop and "选中的方法执行完毕" in status:
            # 如果循环生效，自动关闭提示框
            auto_close = True

        status_window = tk.Toplevel(self)
        status_window.title("状态")
        status_label = tk.Label(status_window, text=status, font=("Segoe UI", 12))
        status_label.pack(padx=20, pady=20)
        
        if auto_close:
            self.master.after(5000, status_window.destroy)  # 显示五秒后关闭

    def terminate_execution(self):
        """
        终止当前执行的用例函数。
        """
        global thread, current_thread, is_running
        self.running_event.clear()
        if current_thread and current_thread.is_alive():
            logger.info("正在终止当前运行的用例函数")
            stop_thread(current_thread)  # 强制终止当前线程
        if thread and thread.is_alive():
            thread.join(timeout=5)  # 等待线程结束，设置超时时间为5秒
            if thread.is_alive():
                logger.error("线程未能在预期时间内结束")
                stop_thread(thread)  # 强制终止线程
        self.create_prompt_box("脚本已终止", True)
        is_running = False

        # 恢复AOI和RV的配置
        self.restore_aoi_rv_configs()

    def on_search(self, event):
        """
        搜索框输入事件处理函数。
        """
        self.search_methods()

    def search_methods(self):
        """
        根据输入内容搜索用例编码，并更新表格显示。
        """
        search_text = self.search_entry.get().strip()

        # 确保占位符不参与搜索
        if search_text == "输入用例编码搜索":
            search_text = ""

        logger.debug(f"用户尝试搜索用例编码，搜索内容：'{search_text}'。")
        
        # 如果搜索框为空，加载初始用例列表
        if not search_text:
            self.load_test_cases(self.case_combobox.get())
            return

        # 获取当前模块的用例列表
        module_name = self.case_combobox.get()
        test_cases = []
        results_list = []

        if module_name == "全部":
            # 遍历所有模块的用例
            for mod_name, cases in self.results.items():
                for row in cases:
                    test_cases.append(row["用例编号"])
                    results_list.append(row["执行结果"])
        else:
            # 仅遍历选定模块的用例
            if module_name in self.results:
                for row in self.results[module_name]:
                    test_cases.append(row["用例编号"])
                    results_list.append(row["执行结果"])

        # 进行模糊搜索，匹配包含搜索关键字的用例编码
        filtered_cases = []
        filtered_results = []
        for i, test_case in enumerate(test_cases):
            if search_text.lower() in test_case.lower():
                filtered_cases.append(test_case)
                filtered_results.append(results_list[i])

        # 更新表格显示匹配的用例
        self.update_test_case_list(filtered_cases)
        self.update_status_list(filtered_results)

    def clear_placeholder(self, event):
        """
        清除搜索框中的占位符。
        """
        if self.search_entry.get() == "输入用例编码搜索":
            self.search_entry.delete(0, tk.END)
            self.search_entry.configure(foreground="black")

    def add_placeholder(self, event):
        """
        如果搜索框为空，则添加占位符。
        """
        if not self.search_entry.get():
            self.search_entry.insert(0, "输入用例编码搜索")
            self.search_entry.configure(foreground="gray")

    def more_info(self, event=None):
        """
        加载更多用例。
        """
        self.displayed_rows += 20  # 每次增加20行
        logger.info(f"加载更多用例，当前显示行数增加到 {self.displayed_rows} 行。")
        
        # 从CSV文件中重新加载数据
        self.results = self.load_csv()
        
        # 加载当前模块的用例
        self.load_test_cases(self.case_combobox.get())
        self.update_idletasks()  # 确保表格更新完成
        while self.table.bbox(self.table.get_children()[-1]) is None:
            self.update_idletasks()  # 确保表格更新完成
            time.sleep(0.2)  # 添加短暂延迟

    def load_test_cases(self, module_name):
        """
        加载指定模块的所有用例到表格中，并为每个用例添加按钮。
        """
        search_text = self.search_entry.get().strip()
        
        # 确保占位符不参与搜索
        if search_text == "输入用例编码搜索":
            search_text = ""

        test_cases = []
        results_list = []

        if module_name == "全部":
            for module_name, module in self.modules.items():
                # 使用模块名称（中文）作为键来获取数据
                for row in self.results.get(module_name, []):
                    test_case_id = row["用例编号"]
                    result = row["执行结果"]
                    if search_text == "" or search_text.lower() in test_case_id.lower():
                        test_cases.append(test_case_id)
                        results_list.append(result)
        else:
            if module_name in self.results:
                for row in self.results[module_name]:
                    test_case_id = row["用例编号"]
                    result = row["执行结果"]
                    if search_text == "" or search_text.lower() in test_case_id.lower():
                        test_cases.append(test_case_id)
                        results_list.append(result)

        self.update_test_case_list(test_cases[:self.displayed_rows])
        self.update_status_list(results_list[:self.displayed_rows])
        logger.info(f"已加载并显示模块 '{module_name}' 的前 {self.displayed_rows} 个用例。")

    def update_test_case_list(self, test_cases):
        """
        更新表格中的用例列表。
        """
        try:
            self.table.delete(*self.table.get_children())
            for test_case in test_cases:
                self.table.insert("", "end", values=(test_case, ""))
            logger.debug(f"已添加用例编码 '{test_case}' 到表格。")
        except Exception as e:
            logger.error(f"更新用例列表时发生错误: {e}")

    def update_status_list(self, results):
        """
        更新表格中用例的执行状态，并确保表格完全更新完成。
        """
        try:
            children = self.table.get_children()
            for child in children:
                test_case_id = self.table.item(child, "values")[0]  # 获取用例编号
                # 从 test_case_status 获取执行结果
                result = test_case_status.get(test_case_id, '未执行')
                self.table.set(child, column="状态", value=result)
                logger.debug(f"更新用例编号 {test_case_id} 的状态为 {result}")
            self.update_idletasks()  # 确保每次更新后界面能即时反映出变化
            logger.debug("已更新用例状态。")
        except Exception as e:
            logger.error(f"更新用例状态时发生错误: {e}")
            logger.error(f"异常详情: {e.__class__.__name__}, {e.args}")

    def on_module_selected(self, event):
        """
        当选择不同模块时，加载相应的用例。
        """
        selected_module = self.case_combobox.get()
        logger.info(f"用户选择了模块 '{selected_module}'，开始加载对应的用例。")
        
        # 检查模块是否在结果中
        if selected_module not in self.results and selected_module != "全部":
            logger.error(f"模块 '{selected_module}' 的数据未找到。")
        else:
            logger.info(f"模块 '{selected_module}' 的数据已找到，准备加载。")
        
        self.load_test_cases(selected_module)

    def on_search(self, event=None):
        """
        搜索框输入事件处理函数。
        """
        self.load_test_cases(self.case_combobox.get())

    def restore_aoi_rv_configs(self):
        """
        恢复AOI和RV的配置。
        """
        try:
            bin_dir = "d:\\EYAOI\\Bin"
            rv_config_folder = "d:\\EYAOI\\Bin\\config\\RV"

            # 恢复AOI配置
            aoi_backup_folder = os.path.join(bin_dir, "copy")
            aoi_config_folder = None
            if os.path.exists(os.path.join(bin_dir, "config")):
                aoi_config_folder = os.path.join(bin_dir, "config")
            elif os.path.exists(os.path.join(bin_dir, "Config")):
                aoi_config_folder = os.path.join(bin_dir, "Config")
            else:
                for d in os.listdir(bin_dir):
                    if os.path.isdir(os.path.join(bin_dir, d)) and d.lower().startswith("config"):
                        aoi_config_folder = os.path.join(bin_dir, d)
                        break

            if aoi_config_folder and os.path.exists(aoi_backup_folder):
                for file_name in os.listdir(aoi_backup_folder):
                    backup_file = os.path.join(aoi_backup_folder, file_name)
                    config_file = os.path.join(aoi_config_folder, file_name)
                    if os.path.isfile(config_file):
                        os.remove(config_file)
                    shutil.copy2(backup_file, config_file)
                    logger.info(f"已将 {file_name} 从 {aoi_backup_folder} 恢复到 {aoi_config_folder}")

            # 恢复RV配置
            rv_backup_folder = os.path.join(rv_config_folder, "copy")
            if os.path.exists(rv_backup_folder):
                for file_name in os.listdir(rv_backup_folder):
                    backup_file = os.path.join(rv_backup_folder, file_name)
                    config_file = os.path.join(rv_config_folder, file_name)
                    if os.path.isfile(config_file):
                        os.remove(config_file)
                    shutil.copy2(backup_file, config_file)
                    logger.info(f"已将 {file_name} 从 {rv_backup_folder} 恢复到 {rv_config_folder}")

        except Exception as e:
            logger.error(f"恢复AOI和RV配置时发生错误: {e}")
class OfflineRepeatTestScreen(tk.Frame):
    def __init__(self, master=None):
        """
        初始化OfflineRepeatTestScreen类，创建离线重复测试界面。
        """
        super().__init__(master)
        self.master = master
        self.master.geometry("750x360")
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
        self.running_event = threading.Event()
        self.current_task = None
        self.selected_button = None
        self.current_thread = None
        self.process_queue()

    def create_widgets(self):
        style = ttk.Style()
        style.configure("TButton", font=("Segoe UI", 12), padding=10)

        self.label = tk.Label(self, text="离线重复测试", font=("Segoe UI", 18))
        self.label.pack(pady=20)

        self.button_frame = tk.Frame(self, width=690, height=100)
        self.button_frame.pack_propagate(False)
        self.button_frame.pack(pady=10)

        self.test_current_window_button = ttk.Button(
            self.button_frame, text="测试当前窗口", command=lambda: self.select_task(self.test_current_window, self.test_current_window_button)
        )
        self.test_current_window_button.pack(side="left", padx=10)

        self.test_current_component_button = ttk.Button(
            self.button_frame, text="测试当前元件", command=lambda: self.select_task(self.test_current_component, self.test_current_component_button)
        )
        self.test_current_component_button.pack(side="left", padx=10)

        self.test_current_group_button = ttk.Button(
            self.button_frame, text="测试当前分组", command=lambda: self.select_task(self.test_current_group, self.test_current_group_button)
        )
        self.test_current_group_button.pack(side="left", padx=10)

        self.test_current_board_button = ttk.Button(
            self.button_frame, text="测试当前整版", command=lambda: self.select_task(self.test_current_board, self.test_current_board_button)
        )
        self.test_current_board_button.pack(side="left", padx=10)

        # 将运行按钮放在返回和停止按钮的左边
        self.button_frame_bottom = tk.Frame(self)
        self.button_frame_bottom.pack(pady=10)

        self.run_button = ttk.Button(self.button_frame_bottom, text="运行", command=self.run_task)
        self.run_button.pack(side="left", padx=10)

        self.back_button = ttk.Button(self.button_frame_bottom, text="返回", command=self.go_back)
        self.back_button.pack(side="left", padx=10)

        self.stop_button = ttk.Button(self.button_frame_bottom, text="停止", command=self.terminate_execution)
        self.stop_button.pack(side="left", padx=10)

    def select_task(self, task, button):
        """
        选择任务并更新按钮状态。
        """
        if self.selected_button:
            self.selected_button.state(["!pressed"])
        self.current_task = task
        self.selected_button = button
        self.selected_button.state(["pressed"])
        self.update_label(f"已选择任务: {task.__name__}")

    def go_back(self):
        """
        返回上级界面。
        """
        for widget in self.master.winfo_children():
            widget.destroy()
        home_screen = HomeScreen(master=self.master)
        home_screen.pack(fill=tk.BOTH, expand=True)

    def run_task(self):
        """
        运行当前选中的任务。
        """
        if self.current_task:
            self.current_thread = threading.Thread(target=self.execute_task, daemon=True)
            self.current_thread.start()

    def execute_task(self):
        """
        执行任务的线程。在开始任务前先将顶级窗口最小化（通过发送最小化命令），等待1秒以确保窗口已完全最小化，
        然后将任务放入队列中执行。
        """
        # # 通过当前组件获取顶级窗口
        # top = self.winfo_toplevel()
        # hwnd = top.winfo_id()
        # try:
        #     # 发送 WM_SYSCOMMAND 消息，命令值为 SC_MINIMIZE，使窗口最小化
        #     win32gui.PostMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_MINIMIZE, 0)
        # except Exception as e:
        #     logger.error("通过Win32API发送最小化消息失败: " + str(e))
        # # 等待1秒，确保窗口完全最小化
        # time.sleep(1)
        gui_queue.put(self.current_task)
        self.update_label(f"正在运行: {self.current_task.__name__}")

    def test_current_window(self):
        """
        测试当前窗口的事件处理。
        """
        threading.Thread(target=kfzy.test_current_window, daemon=True).start()

    def test_current_component(self):
        """
        测试当前元件的事件处理。
        """
        threading.Thread(target=kfzy.test_current_component, daemon=True).start()

    def test_current_group(self):
        """
        测试当前分组的事件处理。
        """
        threading.Thread(target=kfzy.test_current_group, daemon=True).start()

    def test_current_board(self):
        """
        测试当前整版的事件处理。
        """
        threading.Thread(target=kfzy.test_current_board, daemon=True).start()

    def terminate_execution(self):
        """
        终止当前执行的用例函数。
        """
        self.running_event.clear()
        if self.current_thread and self.current_thread.is_alive():
            self._stop_thread(self.current_thread)
            logger.info("正在终止当前运行的用例函数")
            self.current_task = None
            self.update_label("任务已终止")

    def _stop_thread(self, thread):
        """强行终止线程"""
        if not thread.is_alive():
            return
        exc = ctypes.py_object(SystemExit)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread.ident), exc)
        if res == 0:
            raise ValueError("线程不存在")
        elif res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
            raise SystemError("线程终止失败")

    def update_label(self, text):
        self.label.config(text=text)

    def process_queue(self):
        try:
            while True:
                # 从队列中获取并执行操作
                task = gui_queue.get_nowait()
                self.running_event.set()
                task()
                self.running_event.clear()
        except queue.Empty:
            pass
        # 定期检查队列
        self.master.after(100, self.process_queue)

class LoopTestWindow(tk.Toplevel):
    def __init__(self, master):
        """
        初始化循环测试窗口。
        """
        super().__init__(master)
        self.master = master
        self.title("循环测试配置")
        self.geometry("800x600")
        self.transient(master)
        self.grab_set()

        # 加载路径数据
        self.load_paths()

        # 定义颜色常量
        SELECTED_COLOR = "#169bd5"
        DEFAULT_COLOR = "#f0f0f0"
        ACTIVE_COLOR = "#d9001b"

        # 左上角标题
        header_label = tk.Label(self, text="路径", font=("SimHei", 16, "bold"), anchor="nw")
        header_label.grid(row=0, column=0, columnspan=20, sticky="w", padx=10, pady=10)

        # 左侧系统框
        system_frame = tk.Frame(self, borderwidth=2, relief="groove", padx=10, pady=10)
        system_frame.grid(row=1, column=0, rowspan=20, columnspan=5, sticky="nsew", padx=10, pady=10)

        # 系统标题
        system_label = tk.Label(system_frame, text="系统", font=("Arial", 12, "bold"))
        system_label.pack(pady=5)

        systems = ["AOI", "MES"]
        for idx, system in enumerate(systems):
            btn = tk.Button(system_frame, text=system, bg=DEFAULT_COLOR, command=lambda s=system: self.switch_system(s), width=15)
            btn.pack(fill="x", pady=2)

        # 新增系统按钮
        add_system_button = tk.Button(system_frame, text="新增", command=lambda: print("新增系统"), bg=SELECTED_COLOR, fg="white")
        add_system_button.pack(side="left", pady=5, padx=5, fill="x", expand=True)

        # 删除系统按钮
        delete_system_button = tk.Button(system_frame, text="删除", command=lambda: print("删除系统"))
        delete_system_button.pack(side="right", pady=5, padx=5, fill="x", expand=True)

        # 路径列表框架
        self.path_frame = tk.Frame(self, borderwidth=2, relief="groove", padx=10, pady=10)
        self.path_frame.grid(row=1, column=5, rowspan=20, columnspan=15, sticky="nsew", padx=10, pady=10)

        # 路径列表标题
        path_label = tk.Label(self.path_frame, text="路径", font=("Arial", 12, "bold"), anchor="nw")
        path_label.grid(row=0, column=0, columnspan=4, pady=5, sticky="w")

        # 表格列标题
        columns = ["选择", "文件夹路径", "JOB名称", "状态"]
        for col_idx, col_name in enumerate(columns):
            tk.Label(self.path_frame, text=col_name, font=("Arial", 12, "bold")).grid(row=1, column=col_idx, padx=5, pady=5)

        self.selected_path = 0  # 默认选中第一条路径
        self.selected_path_var = tk.IntVar(value=self.selected_path)

        # 按钮框架
        button_frame = tk.Frame(self.path_frame)
        button_frame.grid(row=0, column=1, columnspan=4, sticky="ew")

        buttons = [
            ("生效", self.take_loop_path_effect, ACTIVE_COLOR),
            ("失效", self.make_loop_path_ineffective, None),
            ("编辑", self.edit_path, None),
            ("测试", lambda: None, None),
            ("新增", self.add_path, SELECTED_COLOR),
            ("删除", lambda: None, None),
        ]

        for idx, (text, command, color) in enumerate(buttons):
            fg_color = "white" if color else "black"
            tk.Button(button_frame, text=text, command=command, bg=color or DEFAULT_COLOR, fg=fg_color, width=8).grid(row=0, column=idx, padx=5)

        # 初始加载路径数据
        self.refresh_path_list()

        # 确保初始状态下没有任何一个路径是生效的
        for path in self.path_data:
            path["状态"] = ""

        # 调整窗口布局留白
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(5, weight=1)

    def switch_system(self, system):
        """
        切换系统。
        """
        self.current_system = system
        print(f"当前系统切换到: {system}")

    def select_path(self, idx):
        """
        选择路径。
        """
        self.selected_path = idx
        print(f"选择了路径: {self.path_data[idx]['文件夹路径']}")

    def take_loop_path_effect(self):
        """
        让路径生效。
        """
        global active_loop, active_path, active_job_name
        if self.selected_path is not None:
            for path in self.path_data:
                path["状态"] = ""
            self.path_data[self.selected_path]["状态"] = "生效中"
            active_loop = True
            self.refresh_path_list()
            self.save_paths()

            # 更新全局变量
            selected_path = self.path_data[self.selected_path]
            active_path = selected_path["文件夹路径"]
            active_job_name = selected_path["JOB名称"]
            logger.info(f"更新全局变量: active_path={active_path}, active_job_name={active_job_name}")

    def make_loop_path_ineffective(self):
        """
        让路径失效。
        """
        global active_loop, active_path, active_job_name
        if self.selected_path is not None:
            if self.path_data[self.selected_path]["状态"] == "生效中":
                self.path_data[self.selected_path]["状态"] = ""
            active_loop = False
            self.refresh_path_list()
            self.save_paths()

            # 更新全局变量
            active_path = None
            active_job_name = None
            logger.info("路径已失效，清除全局变量: active_path 和 active_job_name")

    def refresh_path_list(self):
        """
        刷新路径列表。
        """
        for widget in self.path_frame.winfo_children():
            if widget.grid_info()["row"] > 1:  # 保留标题行
                widget.destroy()

        for row_idx, entry in enumerate(self.path_data, start=2):
            rbutton = tk.Radiobutton(
                self.path_frame,
                variable=self.selected_path_var,
                value=row_idx - 2,
                command=lambda idx=row_idx - 2: self.select_path(idx),
            )
            rbutton.grid(row=row_idx, column=0, padx=5, pady=5)
            tk.Label(self.path_frame, text=entry["文件夹路径"]).grid(row=row_idx, column=1, padx=5, pady=5)
            tk.Label(self.path_frame, text=entry["JOB名称"]).grid(row=row_idx, column=2, padx=5, pady=5)
            status_color = "green" if entry["状态"] == "生效中" else "black"
            tk.Label(self.path_frame, text=entry["状态"], fg=status_color).grid(row=row_idx, column=3, padx=5, pady=5)

    def load_paths(self):
        """
        从文件加载路径信息。
        """
        try:
            with open("path_data.json", "r", encoding="utf-8") as f:
                self.path_data = json.load(f)
        except FileNotFoundError:
            # 添加几条示例路径
            self.path_data = [
                {"文件夹路径": "D:\\EYAOI\\JOB\\全算法", "JOB名称": "全算法", "状态": ""},
                {"文件夹路径": "D:\\EYAOI\\JOB\\测试1", "JOB名称": "测试1", "状态": ""},
                {"文件夹路径": "D:\\EYAOI\\JOB\\测试2", "JOB名称": "测试2", "状态": ""}
            ]

    def save_paths(self):
        """
        保存路径信息到文件。
        """
        with open("path_data.json", "w", encoding="utf-8") as f:
            json.dump(self.path_data, f, ensure_ascii=False, indent=4)

    def add_path(self):
        """
        弹出窗口以添加新路径。
        """
        def save_path():
            folder_path = path_entry.get().strip()
            job_name = job_entry.get().strip()

            # 前置条件校验
            if not folder_path:
                messagebox.showwarning("警告", "请输入文件夹路径")
                return
            if not job_name:
                messagebox.showwarning("警告", "请输入JOB名称")
                return
            if any(entry["JOB名称"] == job_name for entry in self.path_data):
                messagebox.showwarning("警告", "当前JOB已存在不允许重复添加")
                return

            self.path_data.append({"文件夹路径": folder_path, "JOB名称": job_name, "状态": ""})
            self.refresh_path_list()
            self.save_paths()
            add_window.destroy()

        def select_folder():
            folder_selected = filedialog.askdirectory(parent=add_window)
            if folder_selected:
                folder_selected = folder_selected.replace("/", "\\")
                path_entry.delete(0, tk.END)
                path_entry.insert(0, folder_selected)
                job_entry.delete(0, tk.END)
                job_entry.insert(0, os.path.basename(folder_selected))

        add_window = tk.Toplevel(self)
        add_window.title("新增路径")
        add_window.geometry("450x200")
        add_window.transient(self)
        add_window.grab_set()

        tk.Label(add_window, text="文件夹路径:").grid(row=0, column=0, padx=10, pady=10)
        path_entry = tk.Entry(add_window, width=40)
        path_entry.grid(row=0, column=1, padx=10, pady=10)
        tk.Button(add_window, text="选择", command=select_folder).grid(row=0, column=2, padx=5)

        tk.Label(add_window, text="JOB名称:").grid(row=1, column=0, padx=10, pady=10)
        job_entry = tk.Entry(add_window, width=40)
        job_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(add_window, text="取消", command=add_window.destroy).grid(row=2, column=0, pady=10)
        tk.Button(add_window, text="保存", command=save_path, bg="#169bd5", fg="white").grid(row=2, column=1, pady=10)

    def edit_path(self):
        """
        编辑所选路径。
        """
        if self.selected_path is None:
            messagebox.showwarning("警告", "请先选择一个路径！")
            return

        selected_entry = self.path_data[self.selected_path]

        def save_edit_changes():
            selected_entry["文件夹路径"] = path_entry.get()
            selected_entry["JOB名称"] = job_entry.get()
            self.refresh_path_list()
            self.save_paths()
            edit_window.destroy()

        def select_folder():
            folder_selected = filedialog.askdirectory(parent=edit_window)
            if folder_selected:
                folder_selected = folder_selected.replace("/", "\\")
                path_entry.delete(0, tk.END)
                path_entry.insert(0, folder_selected)
                job_entry.delete(0, tk.END)
                job_entry.insert(0, os.path.basename(folder_selected))

        edit_window = tk.Toplevel(self)
        edit_window.title("编辑路径")
        edit_window.geometry("450x200")
        edit_window.transient(self)
        edit_window.grab_set()

        tk.Label(edit_window, text="文件夹路径:").grid(row=0, column=0, padx=10, pady=10)
        path_entry = tk.Entry(edit_window, width=40)
        path_entry.grid(row=0, column=1, padx=10, pady=10)
        path_entry.insert(0, selected_entry["文件夹路径"])
        tk.Button(edit_window, text="选择", command=select_folder).grid(row=0, column=2, padx=5)

        tk.Label(edit_window, text="JOB名称:").grid(row=1, column=0, padx=10, pady=10)
        job_entry = tk.Entry(edit_window, width=40)
        job_entry.grid(row=1, column=1, padx=10, pady=10)
        job_entry.insert(0, selected_entry["JOB名称"])

        tk.Button(edit_window, text="取消", command=edit_window.destroy).grid(row=2, column=0, pady=10)
        tk.Button(edit_window, text="保存", command=save_edit_changes, bg="#169bd5", fg="white").grid(row=2, column=1, pady=10)

class LoginPasswordWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("登录密码")
        self.geometry("800x600")
        self.account_data = [
            {"账号": "admin", "密码": "admin123", "状态": "生效中"},
            {"账号": "op2", "密码": "op2pass", "状态": "失效"},
        ]
        self.current_system = "AOI"
        self.selected_account = None
        self.create_widgets()

    def create_widgets(self):
        # 定义颜色常量
        SELECTED_COLOR = "#169bd5"
        DEFAULT_COLOR = "#f0f0f0"
        ACTIVE_COLOR = "#d9001b"
        TEXT_ACTIVE_COLOR = "#9fce56"

        # 左上角标题
        header_label = tk.Label(self, text="登录密码", font=("Arial", 16, "bold"), anchor="w")
        header_label.grid(row=0, column=0, columnspan=20, sticky="w", padx=10, pady=10)

        # 刷新账号密码列表
        def refresh_account_list():
            for widget in account_frame.winfo_children():
                if widget.grid_info()["row"] > 1:  # 保留标题行
                    widget.destroy()

            for row_idx, entry in enumerate(self.account_data, start=2):
                rbutton = tk.Radiobutton(
                    account_frame,
                    variable=selected_account_var,
                    value=row_idx - 2,
                    command=lambda idx=row_idx - 2: select_account(idx),
                )
                rbutton.grid(row=row_idx, column=0, padx=5, pady=5)
                tk.Label(account_frame, text=entry["账号"]).grid(row=row_idx, column=1, padx=5, pady=5)
                tk.Label(account_frame, text="******").grid(row=row_idx, column=2, padx=5, pady=5)
                status_color = TEXT_ACTIVE_COLOR if entry["状态"] == "生效中" else "black"
                tk.Label(account_frame, text=entry["状态"], fg=status_color).grid(row=row_idx, column=3, padx=5, pady=5)

        # 切换系统
        def switch_system(system):
            self.current_system = system
            print(f"当前系统切换到: {system}")
            refresh_account_list()

        # 左侧系统框
        system_frame = tk.Frame(self, borderwidth=2, relief="groove", padx=10, pady=10)
        system_frame.grid(row=1, column=0, rowspan=20, columnspan=5, sticky="nsew", padx=10, pady=10)

        # 系统标题
        system_label = tk.Label(system_frame, text="系统", font=("Arial", 12, "bold"))
        system_label.pack(pady=5)

        systems = ["AOI", "MES"]
        for idx, system in enumerate(systems):
            btn = tk.Button(system_frame, text=system, bg=DEFAULT_COLOR, command=lambda s=system: switch_system(s), width=15)
            btn.pack(fill="x", pady=2)

        # 新增系统按钮
        add_system_button = tk.Button(system_frame, text="新增", command=lambda: print("新增系统"), bg=SELECTED_COLOR, fg="white")
        add_system_button.pack(side="left", pady=5, padx=5, fill="x", expand=True)

        # 删除系统按钮
        delete_system_button = tk.Button(system_frame, text="删除", command=lambda: print("删除系统"))
        delete_system_button.pack(side="right", pady=5, padx=5, fill="x", expand=True)

        # 账号密码框架
        account_frame = tk.Frame(self, borderwidth=2, relief="groove", padx=10, pady=10)
        account_frame.grid(row=1, column=5, rowspan=20, columnspan=15, sticky="nsew", padx=10, pady=10)

        # 账号密码标题
        account_label = tk.Label(account_frame, text="账号密码", font=("Arial", 12, "bold"))
        account_label.grid(row=0, column=0, columnspan=4, pady=5)

        # 表格列标题
        columns = ["选择", "账号", "密码", "状态"]
        for col_idx, col_name in enumerate(columns):
            tk.Label(account_frame, text=col_name, font=("Arial", 12, "bold")).grid(row=1, column=col_idx, padx=5, pady=5)

        selected_account_var = tk.IntVar(value=-1)

        # 选择账号
        def select_account(idx):
            self.selected_account = idx
            print(f"选择了账号: {self.account_data[idx]['账号']}")

        # 编辑账号
        def edit_account():
            if self.selected_account is None:
                messagebox.showwarning("警告", "请先选择一个账号！")
                return

            account = self.account_data[self.selected_account]

            def save_changes():
                account["账号"] = account_entry.get()
                account["密码"] = password_entry.get() if password_entry.get() != "******" else account["密码"]
                refresh_account_list()
                edit_window.destroy()

            edit_window = tk.Toplevel(self)
            edit_window.title("编辑账号")
            edit_window.geometry("300x200")

            tk.Label(edit_window, text="账号:").grid(row=0, column=0, padx=10, pady=10)
            account_entry = tk.Entry(edit_window)
            account_entry.grid(row=0, column=1, padx=10, pady=10)
            account_entry.insert(0, account["账号"])

            tk.Label(edit_window, text="密码:").grid(row=1, column=0, padx=10, pady=10)
            password_entry = tk.Entry(edit_window, show="*")
            password_entry.grid(row=1, column=1, padx=10, pady=10)
            password_entry.insert(0, "******")

            tk.Button(edit_window, text="保存", command=save_changes).grid(row=2, column=0, columnspan=2, pady=10)

        # 新增账号
        def add_account():
            def save_new_account():
                self.account_data.append({"账号": account_entry.get(), "密码": password_entry.get(), "状态": "失效"})
                refresh_account_list()
                add_window.destroy()

            add_window = tk.Toplevel(self)
            add_window.title("新增账号")
            add_window.geometry("300x200")

            tk.Label(add_window, text="账号:").grid(row=0, column=0, padx=10, pady=10)
            account_entry = tk.Entry(add_window)
            account_entry.grid(row=0, column=1, padx=10, pady=10)

            tk.Label(add_window, text="密码:").grid(row=1, column=0, padx=10, pady=10)
            password_entry = tk.Entry(add_window, show="*")
            password_entry.grid(row=1, column=1, padx=10, pady=10)

            tk.Button(add_window, text="保存", command=save_new_account).grid(row=2, column=0, columnspan=2, pady=10)

        # 删除账号
        def delete_account():
            if self.selected_account is None:
                messagebox.showwarning("警告", "请先选择一个账号！")
                return
            if messagebox.askyesno("确认删除", f"确定要删除账号 {self.account_data[self.selected_account]['账号']} 吗？"):
                self.account_data.pop(self.selected_account)
                self.selected_account = None
                refresh_account_list()

        # 生效按钮
        def activate_account():
            if self.selected_account is None:
                messagebox.showwarning("警告", "请先选择一个账号！")
                return

            for account in self.account_data:
                account["状态"] = "失效"
            self.account_data[self.selected_account]["状态"] = "生效中"
            refresh_account_list()

        # 失效按钮
        def deactivate_account():
            if self.selected_account is None:
                messagebox.showwarning("警告", "请先选择一个账号！")
                return

            self.account_data[self.selected_account]["状态"] = "失效"
            refresh_account_list()

        # 测试按钮
        def test_account():
            if self.selected_account is None:
                messagebox.showwarning("警告", "请先选择一个账号！")
                return

            messagebox.showinfo("测试", f"测试账号 {self.account_data[self.selected_account]['账号']}")

        # 按钮框架
        button_frame = tk.Frame(account_frame)
        button_frame.grid(row=0, column=1, columnspan=4, sticky="ew")

        buttons = [
            ("生效", activate_account, ACTIVE_COLOR),
            ("失效", deactivate_account, None),
            ("编辑", edit_account, None),
            ("测试", test_account, None),
            ("新增", add_account, SELECTED_COLOR),
            ("删除", delete_account, None),
        ]

        for idx, (text, command, color) in enumerate(buttons):
            fg_color = "white" if color else "black"
            tk.Button(button_frame, text=text, command=command, bg=color or DEFAULT_COLOR, fg=fg_color, width=8).grid(row=0, column=idx, padx=5)

        # 初始加载账号数据
        refresh_account_list()

        # 调整窗口布局留白
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(5, weight=1)

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("自动化测试")
        self.geometry("533x400")
        self.center_window()
        self.current_frame = None  # 用于跟踪当前的框架
        self.loop_test_window = None
        self.config_state = {
            "replace_aoi": True,
            "replace_rv": True
        }
        self.switch_frame(HomeScreen)

    def switch_frame(self, frame_class):
        # 销毁当前的 frame
        if self.current_frame is not None:
            self.current_frame.destroy()

        # 创建新的 frame
        if issubclass(frame_class, tk.Toplevel):
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(frame_class, self)
                new_frame = future.result()
                new_frame.grab_set()
                if isinstance(new_frame, LoopTestWindow):
                    self.loop_test_window = new_frame
        else:
            new_frame = frame_class(self)
            self.current_frame = new_frame  # 更新当前的框架
            self.current_frame.pack(fill=tk.BOTH, expand=True)

    def center_window(self):
        """
        将窗口居中显示。
        """
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def on_closing(self):
        """
        当界面被关闭时，结束所有资源占用。
        """
        global thread, current_thread, is_running
        if current_thread and current_thread.is_alive():
            logger.info("正在终止当前运行的用例函数")
            stop_thread(current_thread)  # 强制终止当前线程
        if thread and thread.is_alive():
            thread.join(timeout=5)  # 等待线程结束，设置超时时间为5秒
            if thread.is_alive():
                logger.error("线程未能在预期时间内结束")
                stop_thread(thread)  # 强制终止线程
        # 释放互斥体
        if mutex:
            win32api.CloseHandle(mutex)
        self.destroy()


if __name__ == "__main__":
    setup_logger()
    app = Application()
    app.mainloop()

