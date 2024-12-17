import shutil
import tkinter as tk
from tkinter import ttk
from loguru import logger
from scripts import yjk, lxbj, jbgn, kjj, spc, tccs, sjdc
from utils import setup_logger
import sys
import win32event
import win32api
import winerror
import csv
import os
import threading
import ctypes
import time
import inspect
from threading import Thread
import pyautogui

# 在文件的开头定义全局变量
global thread, csv_created, execution_lock, current_thread, is_running, CSV_FILE_PATH
thread = None
current_thread = None
is_running = False  # 初始化is_running变量
test_case_status = {}
# 定义一个全局变量来标记CSV文件是否新创建
csv_created = False 

# 定义一个全局锁，确保同一时间只能执行一个方法
execution_lock = threading.Lock()

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

def initialize_csv_file_path():
    global CSV_FILE_PATH
    CSV_FILE_PATH = f"operation_results_{time.strftime('%Y-%m-%d-%H-%M')}.csv"

def create_or_read_csv():
    """
    创建或读取CSV文件。如果文件不存在，则创建一个新的文件并插入模块和方法名。
    """
    global csv_created
    logger.debug(f"Checking if CSV file exists at: {CSV_FILE_PATH}")
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
                "调参测试": tccs
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

def update_csv(module_name, method_name, operation="", result="", error_step="", execution_time="", remarks="", lock=None, device_type="", execution_system=""):
    """
    更新CSV文件，修改已有的测试结果记录。
    """
    if not method_name:
        logger.error("方法名不能为空")
        return

    if lock:
        lock.acquire()

    try:
        rows = []
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

        with open(CSV_FILE_PATH, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=CSV_COLUMNS)
            writer.writeheader()
            writer.writerows(rows)
        logger.info(f"已更新CSV文件：模块 '{module_name}' 的方法 '{method_name}'。")
    except FileNotFoundError:
        logger.error(f"CSV文件未找到：{CSV_FILE_PATH}")
        # 记录CSV文件夹下所有文件的名称
        csv_folder = os.path.dirname(CSV_FILE_PATH)
        if os.path.exists(csv_folder):
            files = os.listdir(csv_folder)
            logger.info(f"CSV文件夹 '{csv_folder}' 下的文件：{files}")
        else:
            logger.error(f"CSV文件夹 '{csv_folder}' 不存在")
    except Exception as e:
        logger.error(f"更新CSV文件时发生错误：{e}")
    finally:
        if lock:
            lock.release()

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
        self.pack()
        self.create_widgets()

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
        self.label.pack(pady=20)

        self.icon_frame = tk.Frame(self)
        self.icon_frame.pack(pady=20)

        self.aoi_icon = ttk.Button(
            self.icon_frame, text="AOI", command=self.toggle_aoi, style="Selected.TButton"
        )
        self.aoi_icon.pack(padx=10, pady=10)

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(pady=20)

        self.confirm_button = ttk.Button(self.button_frame, text="确认", command=self.open_aoi_detail)
        self.confirm_button.pack(side="left", padx=10)

        self.exit_button = ttk.Button(self.button_frame, text="退出", command=self.master.quit)
        self.exit_button.pack(side="right", padx=10)

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

    def open_aoi_detail(self):
        """
        打开AOI详情界面，并在必要时启动加载模块的线程。
        """
        if self.selected_icon.get() == "AOI":
            self.master.switch_frame(AOIDetailScreen)
            logger.info("切换至AOI详情界面。")
            # 如果CSV文件是新创建的，则启动加载模块的线程
            if csv_created:
                threading.Thread(target=self.load_modules_in_background).start()

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

        # 初始化配置状态
        self.config_state = {
            "replace_aoi": True,  # 默认值
            "replace_rv": True    # 默认值
        }

        # 默认加载"基本功能"模块的用例
        self.load_test_cases("基本功能")

    def load_csv(self):
        """
        加载CSV文件内容，如果文件不存在则创建新的CSV文件。
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
            "数据导出": sjdc
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

        # 配置按钮
        self.config_button = ttk.Button(self, text="配置", style="TButton", width=10, command=lambda: self.show_config_window())
        self.config_button.grid(row=7, column=0, padx=10, pady=10, sticky="w")

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
                    logger.warning("已有一个用例脚本在运行，请等待其结束后再启动新的用例脚本")
                    return
            except NameError:
                thread = None
            self.running_event.set()
            test_case_status.clear()  # 清理状态
            self.master.iconify()
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
                logger.info(f"准备执行模块 '{module_name}' 中选中的方法：{selected_methods}。")

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
                self.master.after(5000, self.create_prompt_box, "选中的方法执行完毕")
                global is_running
                is_running = False
                # 更新所有方法的状态
                self.master.after(1000, lambda: self.update_status_list([test_case_status.get(method_name, '未执行') for method_name in method_names]))
                # 将界面置前
                self.master.focus_force()

        def execute_method(method, index):
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
                        self.master.after(5000, self.create_prompt_box, f"{method.__name__} 方法执行完毕")

                        # 确保状态更新完成后再执行下一个方法
                        self.master.after(10000, lambda: run_method(index + 1))  # 增加时间以确保任务状态更新完毕
                except SystemExit:
                    logger.info(f"{method.__name__} 方法被终止")
                except Exception as e:
                    logger.error(f"{method.__name__} 方法执行出错: {e}")
                    test_case_status[method.__name__] = "失败"
                    
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


    def create_prompt_box(self, status):
        """
        更新界面状态信息。
        """
        status_window = tk.Toplevel(self)
        status_window.title("状态")
        status_label = tk.Label(status_window, text=status, font=("Segoe UI", 12))
        status_label.pack(padx=20, pady=20)
        
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
        self.create_prompt_box("脚本已终止")
        is_running = False

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
            logger.debug(f"Children count: {len(children)}, Results count: {len(results)}")
            logger.debug(f"Results keys: {list(results.keys())}")  # 列出结果中的键
            for i, result in enumerate(results):
                if i < len(children):  # 确保索引不超出范围
                    self.table.set(children[i], column="状态", value=result)
                else:
                    logger.critical(f"索引 {i} 超出范围，跳过更新状态")
                    continue  # 跳过不存在的索引
            self.update_idletasks()  # 确保每次更新后界面能即时反映出变化
            logger.debug(f"已更新用例状态为 '{result}'。")
        except Exception as e:
            logger.error(f"更新用例状态时发生错误: {e}")
            logger.error(f"Exception details: {e.__class__.__name__}, {e.args}")


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

    def show_config_window(self):
        """
        显示配置窗口。
        """
        config_window = tk.Toplevel(self)
        config_window.title("配置选项")
        config_window.geometry("300x200")
        config_window.transient(self)
        config_window.grab_set()

        # 使用已保存的配置状态初始化勾选框
        self.aoi_var = tk.BooleanVar(value=self.config_state.get("replace_aoi", True))
        aoi_check = ttk.Checkbutton(config_window, text="替换aoi流程配置及切换程式配置", variable=self.aoi_var)
        aoi_check.pack(pady=10)

        self.rv_var = tk.BooleanVar(value=self.config_state.get("replace_rv", True))
        rv_check = ttk.Checkbutton(config_window, text="替换rv视图配置", variable=self.rv_var)
        rv_check.pack(pady=10)

        # 确认按钮
        confirm_button = ttk.Button(config_window, text="确认", command=lambda: self.save_config(config_window))
        confirm_button.pack(pady=20)

    def save_config(self, config_window):
        """
        保存配置状态。
        """
        self.config_state = {
            "replace_aoi": self.aoi_var.get(),
            "replace_rv": self.rv_var.get()
        }
        config_window.destroy()
        logger.info(f"配置已保存: {self.config_state}")

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("自动化测试")
        self.geometry("533x400")  # 调整窗口大小为原来的三分之二
        self.center_window()
        self.current_frame = None
        self.switch_frame(HomeScreen)  # 先进入HomeScreen
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # 绑定窗口关闭事件

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

    def switch_frame(self, frame_class):
        """
        切换当前显示的帧。
        """
        new_frame = frame_class(self)
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        if isinstance(new_frame, AOIDetailScreen):
            self.geometry("550x600")  # Detail界面大小，增加下方留白
        else:
            self.geometry("400x400")  # Home界面大小，适当调整

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
        self.destroy()

if __name__ == "__main__":
    setup_logger()
    app = Application()
    app.mainloop()

