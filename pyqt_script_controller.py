import sys
import os
import traceback
from datetime import datetime
from multiprocessing import Process, Queue
import subprocess

from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QDateEdit, QLabel, QMessageBox, QCheckBox, QGroupBox, QLineEdit
)
from PyQt5.QtCore import QDate, QThread, pyqtSignal, QTimer, Qt
from utils import setup_logger
import test
import platform
import tkinter as tk
from tkinter import filedialog
from PyQt5.QtWidgets import QFileDialog

# 使用子进程打开文件对话框
def open_file_dialog(queue):
    try:
        # 使用系统文件对话框
        import tkinter as tk
        from tkinter import filedialog
        
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        folder_path = filedialog.askdirectory()
        queue.put(folder_path)
    except Exception as e:
        queue.put(f"ERROR: {str(e)}")

# Excel生成线程
class ExcelGeneratorThread(QThread):
    task_completed = pyqtSignal(list, list)  # 成功和失败的模式列表
    progress_update = pyqtSignal(str)  # 进度更新
    
    def __init__(self, folder, date_str, selected_modes, parent=None):
        super().__init__(parent)
        self.folder = folder
        self.date_str = date_str
        self.selected_modes = selected_modes
        
    def find_log_file(self, log_type):
        """在选择的文件夹中查找指定类型和日期的日志文件"""
        try:
            print(f"查找日志文件: {log_type}_{self.date_str}.log 在文件夹 {self.folder}")
            
            if log_type == "AlgInspection":
                # AlgInspection日志文件格式特殊，需要查找包含Idx的文件
                matching_files = []
                for file in os.listdir(self.folder):
                    if "AlgInspection" in file and self.date_str in file and file.endswith(".log"):
                        matching_files.append(os.path.join(self.folder, file))
                
                if matching_files:
                    print(f"找到匹配的AlgInspection文件: {matching_files[0]}")
                    return matching_files[0]  # 返回第一个匹配的文件
                else:
                    print(f"未找到匹配的AlgInspection文件，尝试查找任何日期的文件")
                    # 如果找不到指定日期的文件，尝试查找任何日期的文件
                    for file in os.listdir(self.folder):
                        if "AlgInspection" in file and file.endswith(".log"):
                            matching_files.append(os.path.join(self.folder, file))
                    
                    if matching_files:
                        print(f"找到任意日期的AlgInspection文件: {matching_files[0]}")
                        return matching_files[0]
                    else:
                        print(f"未找到任何AlgInspection文件")
            else:
                # 其他类型的日志文件
                file_name = f"{log_type}_{self.date_str}.log"
                file_path = os.path.join(self.folder, file_name)
                
                if os.path.exists(file_path):
                    print(f"找到日志文件: {file_path}")
                    return file_path
                else:
                    print(f"日志文件不存在: {file_path}，尝试查找任何日期的文件")
                    # 如果找不到指定日期的文件，尝试查找任何日期的文件
                    matching_files = []
                    for file in os.listdir(self.folder):
                        if file.startswith(f"{log_type}_") and file.endswith(".log"):
                            matching_files.append(os.path.join(self.folder, file))
                    
                    if matching_files:
                        print(f"找到任意日期的{log_type}文件: {matching_files[0]}")
                        return matching_files[0]
            
            self.progress_update.emit(f"找不到日志文件: {log_type}_{self.date_str}.log")
            return None
        except Exception as e:
            print(f"查找日志文件时出错: {str(e)}")
            traceback.print_exc()
            self.progress_update.emit(f"查找日志文件时出错: {str(e)}")
            return None
    
    def run(self):
        try:
            success_modes = []
            failed_modes = []
            
            # 处理窗口级矫正
            if "algInspection" in self.selected_modes:
                self.progress_update.emit("正在处理AlgInspection-窗口级...")
                log_file = self.find_log_file("AlgInspection")
                if log_file:
                    try:
                        test.solve_algInspection(log_file)
                        success_modes.append("AlgInspection-窗口级")
                    except Exception as e:
                        failed_modes.append(f"AlgInspection-窗口级 (错误: {str(e)})")
                        print(f"处理AlgInspection时出错: {str(e)}")
                        traceback.print_exc()
                else:
                    failed_modes.append("AlgInspection-窗口级 (找不到日志文件)")
            
            # 处理元件级矫正
            if "alg3DCrr" in self.selected_modes:
                self.progress_update.emit("正在处理ALG3DCrr-元件级矫正...")
                log_file = self.find_log_file("ALG3DCrr")
                if log_file:
                    try:
                        test.solve_alg3DCrr(log_file)
                        success_modes.append("ALG3DCrr-元件级矫正")
                    except Exception as e:
                        failed_modes.append(f"ALG3DCrr-元件级矫正 (错误: {str(e)})")
                        print(f"处理ALG3DCrr时出错: {str(e)}")
                        traceback.print_exc()
            
            # 处理整板级
            if "simpCalTime" in self.selected_modes:
                self.progress_update.emit("正在处理AlgSimpCalTime-整板级...")
                simp_log_file = self.find_log_file("AlgSimpCalTime")
                thread_log_file = self.find_log_file("AlgThreadTimeStats")
                
                if simp_log_file and thread_log_file:
                    try:
                        test.solve_simpCalTime(simp_log_file, thread_log_file)
                        success_modes.append("AlgSimpCalTime-整板级")
                    except Exception as e:
                        failed_modes.append(f"AlgSimpCalTime-整板级 (错误: {str(e)})")
                        print(f"处理AlgSimpCalTime时出错: {str(e)}")
                        traceback.print_exc()
            
            # 处理线程时间统计
            if "ThreadTimeStats" in self.selected_modes:
                self.progress_update.emit("正在处理AlgThreadTimeStats-整板级...")
                log_file = self.find_log_file("AlgThreadTimeStats")
                simp_log_file = self.find_log_file("AlgSimpCalTime")
                
                if log_file and simp_log_file:
                    try:
                        test.solve_ThreadTimeStats(log_file, simp_log_file)
                        success_modes.append("AlgThreadTimeStats-整板级")
                    except Exception as e:
                        failed_modes.append(f"AlgThreadTimeStats-整板级 (错误: {str(e)})")
                        print(f"处理AlgThreadTimeStats时出错: {str(e)}")
                        traceback.print_exc()
            
            self.task_completed.emit(success_modes, failed_modes)
        except Exception as e:
            print(f"Excel生成线程出错: {str(e)}")
            traceback.print_exc()
            self.task_completed.emit([], [f"Excel生成过程中出错: {str(e)}"])

# 创建主窗口
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Excel 生成器")
        self.setGeometry(100, 100, 500, 400)
        self.selected_folder = ""
        self.folder_queue = Queue()
        self.folder_process = None
        self.init_ui()
        
    def init_ui(self):
        main_layout = QVBoxLayout()

        # 添加文件夹输入框
        folder_layout = QHBoxLayout()
        folder_label = QLabel("日志文件夹:")
        self.folder_path_edit = QLineEdit()
        browse_button = QPushButton("浏览...")
        browse_button.clicked.connect(self.browse_folder)
        folder_layout.addWidget(folder_label)
        folder_layout.addWidget(self.folder_path_edit)
        folder_layout.addWidget(browse_button)
        main_layout.addLayout(folder_layout)

        # 添加日期选择控件
        date_layout = QHBoxLayout()
        date_label = QLabel("选择日期:")
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())  # 默认为当前日期
        self.date_edit.setCalendarPopup(True)  # 允许弹出日历选择
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.date_edit)
        main_layout.addLayout(date_layout)

        # 添加模式选择组
        mode_group = QGroupBox("选择处理模式")
        mode_layout = QVBoxLayout()
        
        # 添加复选框
        self.mode_checkboxes = {}
        modes = [
            ("AlgInspection-窗口级", "algInspection"),
            ("ALG3DCrr-元件级矫正", "alg3DCrr"),
            ("AlgSimpCalTime-整板级", "simpCalTime"),
            ("AlgThreadTimeStats-整板级", "ThreadTimeStats")
        ]
        
        for label, mode in modes:
            checkbox = QCheckBox(label)
            self.mode_checkboxes[mode] = checkbox
            mode_layout.addWidget(checkbox)
        
        # 添加全选复选框
        self.select_all_checkbox = QCheckBox("全选")
        self.select_all_checkbox.stateChanged.connect(self.toggle_all_modes)
        mode_layout.addWidget(self.select_all_checkbox)
        
        mode_group.setLayout(mode_layout)
        main_layout.addWidget(mode_group)

        # 添加状态标签
        self.status_label = QLabel("就绪")
        main_layout.addWidget(self.status_label)

        # 创建生成按钮
        generate_button = QPushButton("生成Excel")
        generate_button.clicked.connect(self.generate_excel)
        generate_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;")
        main_layout.addWidget(generate_button)

        self.setLayout(main_layout)
        
        # 设置定时器检查文件夹选择结果
        self.folder_timer = QTimer()
        self.folder_timer.timeout.connect(self.check_folder_result)
        
    def browse_folder(self):
        """选择日志文件夹"""
        self.status_label.setText("正在打开文件夹选择对话框...")
        
        # 方法1：使用subprocess直接调用系统文件选择器
        try:

            system = platform.system()
            
            if system == "Windows":
                # Windows系统使用PowerShell命令
                import tempfile
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
                temp_file.close()
                
                powershell_command = f"""
                Add-Type -AssemblyName System.Windows.Forms
                $folderBrowser = New-Object System.Windows.Forms.FolderBrowserDialog
                $folderBrowser.Description = "选择日志文件夹"
                $folderBrowser.RootFolder = 'MyComputer'
                if($folderBrowser.ShowDialog() -eq 'OK') {{
                    $folderBrowser.SelectedPath | Out-File -FilePath "{temp_file.name}" -Encoding utf8
                }}
                """
                
                # 执行PowerShell命令
                subprocess.run(["powershell", "-Command", powershell_command], 
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                # 读取选择的文件夹路径，使用UTF-8编码
                if os.path.exists(temp_file.name) and os.path.getsize(temp_file.name) > 0:
                    try:
                        with open(temp_file.name, 'r', encoding='utf-8') as f:
                            folder_path = f.read().strip()
                        
                        # 清理路径中的不可见字符
                        folder_path = folder_path.replace('\ufeff', '')  # 移除BOM标记
                        folder_path = ''.join(c for c in folder_path if ord(c) >= 32 or ord(c) == 9)  # 只保留可打印字符和制表符
                        
                        if folder_path:
                            self.folder_path_edit.setText(folder_path)
                            self.selected_folder = folder_path
                            self.status_label.setText(f"已选择文件夹: {folder_path}")
                            os.unlink(temp_file.name)
                            return
                    except Exception as e:
                        print(f"读取临时文件失败: {str(e)}")
                
                try:
                    os.unlink(temp_file.name)
                except:
                    pass
                
            elif system == "Darwin":  # macOS
                # 使用AppleScript
                script = 'tell application "Finder" to return POSIX path of (choose folder with prompt "选择日志文件夹")'
                result = subprocess.run(["osascript", "-e", script], 
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                
                if result.stdout.strip():
                    folder_path = result.stdout.strip()
                    self.folder_path_edit.setText(folder_path)
                    self.selected_folder = folder_path
                    self.status_label.setText(f"已选择文件夹: {folder_path}")
                    return
                
            elif system == "Linux":
                # 使用zenity
                result = subprocess.run(["zenity", "--file-selection", "--directory", "--title=选择日志文件夹"], 
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                
                if result.stdout.strip():
                    folder_path = result.stdout.strip()
                    self.folder_path_edit.setText(folder_path)
                    self.selected_folder = folder_path
                    self.status_label.setText(f"已选择文件夹: {folder_path}")
                    return
        
        except Exception as e:
            print(f"方法1失败: {str(e)}")
            traceback.print_exc()
        
        # 方法2：使用tkinter（在主线程中）
        try:
            
            root = tk.Tk()
            root.withdraw()  # 隐藏主窗口
            root.attributes('-topmost', True)  # 确保对话框在最前面
            
            folder_path = filedialog.askdirectory(title="选择日志文件夹")
            
            if folder_path:
                self.folder_path_edit.setText(folder_path)
                self.selected_folder = folder_path
                self.status_label.setText(f"已选择文件夹: {folder_path}")
                return
        
        except Exception as e:
            print(f"方法2失败: {str(e)}")
            traceback.print_exc()
        
        # 方法3：使用PyQt的对话框，但设置为非模态
        try:

            
            dialog = QFileDialog()
            dialog.setFileMode(QFileDialog.Directory)
            dialog.setOption(QFileDialog.DontUseNativeDialog, True)
            dialog.setWindowTitle("选择日志文件夹")
            dialog.setWindowFlags(Qt.WindowStaysOnTopHint)
            
            if dialog.exec_():
                folder_path = dialog.selectedFiles()[0]
                self.folder_path_edit.setText(folder_path)
                self.selected_folder = folder_path
                self.status_label.setText(f"已选择文件夹: {folder_path}")
                return
        
        except Exception as e:
            print(f"方法3失败: {str(e)}")
            traceback.print_exc()
        
        # 所有方法都失败，提示用户手动输入
        self.status_label.setText("无法打开文件夹选择对话框，请手动输入文件夹路径")
        QMessageBox.warning(self, "提示", "无法打开文件夹选择对话框，请手动在输入框中输入文件夹的完整路径")
    
    def check_folder_result(self):
        """检查文件夹选择结果"""
        if not self.folder_queue.empty():
            result = self.folder_queue.get()
            self.folder_timer.stop()
            
            if result.startswith("ERROR:"):
                self.status_label.setText(f"选择文件夹出错: {result[6:]}")
                print(f"选择文件夹出错: {result[6:]}")
            elif result:
                self.folder_path_edit.setText(result)
                self.selected_folder = result
                self.status_label.setText(f"已选择文件夹: {result}")
            else:
                self.status_label.setText("未选择文件夹")
    
    def toggle_all_modes(self, state):
        """全选或取消全选所有模式"""
        for checkbox in self.mode_checkboxes.values():
            checkbox.setChecked(state)
    
    def get_selected_date(self):
        """获取选择的日期，格式为YYYY-MM-DD"""
        return self.date_edit.date().toString("yyyy-MM-dd")
    
    def generate_excel(self):
        """根据选择的模式生成Excel"""
        # 获取文件夹路径
        folder_path = self.folder_path_edit.text().strip()
        if not folder_path:
            QMessageBox.warning(self, "未选择文件夹", "请先选择或输入日志文件夹路径")
            return
        
        # 移除BOM标记和其他不可见字符
        folder_path = folder_path.replace('\ufeff', '')  # 移除BOM标记
        folder_path = ''.join(c for c in folder_path if ord(c) >= 32 or ord(c) == 9)  # 只保留可打印字符和制表符
        
        # 打印调试信息
        print(f"清理后的文件夹路径: '{folder_path}'")
        print(f"路径长度: {len(folder_path)}")
        print(f"路径字符编码: {[ord(c) for c in folder_path]}")
        
        # 规范化路径
        try:
            normalized_path = os.path.normpath(folder_path)
            print(f"规范化后的路径: '{normalized_path}'")
            
            # 检查文件夹是否存在
            exists = os.path.exists(normalized_path)
            print(f"路径是否存在: {exists}")
            
            if not exists:
                # 尝试创建文件夹
                try:
                    os.makedirs(normalized_path, exist_ok=True)
                    print(f"已创建文件夹: {normalized_path}")
                    exists = True
                except Exception as e:
                    print(f"创建文件夹失败: {str(e)}")
            
            if not exists:
                QMessageBox.warning(self, "无效文件夹", f"指定的路径不存在，且无法创建: {normalized_path}")
                return
            
            is_dir = os.path.isdir(normalized_path)
            print(f"路径是否为文件夹: {is_dir}")
            
            if not is_dir:
                QMessageBox.warning(self, "无效文件夹", f"指定的路径不是文件夹: {normalized_path}")
                return
            
            # 测试文件夹权限
            test_file = os.path.join(normalized_path, "test_permission.tmp")
            try:
                with open(test_file, 'w') as f:
                    f.write("test")
                os.remove(test_file)
                print(f"文件夹权限测试通过")
            except Exception as e:
                print(f"文件夹权限测试失败: {str(e)}")
                QMessageBox.warning(self, "文件夹权限问题", f"无法在选择的文件夹中写入文件: {str(e)}")
                return
            
            # 如果一切正常，使用规范化的路径
            self.selected_folder = normalized_path
            print(f"已确认文件夹有效: {normalized_path}")
            
        except Exception as e:
            print(f"文件夹检查错误: {str(e)}")
            traceback.print_exc()
            QMessageBox.warning(self, "文件夹检查错误", f"检查文件夹时出错: {str(e)}")
            return
        
        selected_modes = [mode for mode, checkbox in self.mode_checkboxes.items() if checkbox.isChecked()]
        
        if not selected_modes:
            QMessageBox.warning(self, "未选择模式", "请至少选择一种处理模式")
            return
        
        # 禁用生成按钮，防止重复点击
        for widget in self.findChildren(QPushButton):
            if widget.text() == "生成Excel":
                widget.setEnabled(False)
        
        # 更新状态
        self.status_label.setText("正在生成Excel...")
        
        # 创建并启动Excel生成线程
        self.excel_thread = ExcelGeneratorThread(
            self.selected_folder, 
            self.get_selected_date(), 
            selected_modes
        )
        self.excel_thread.progress_update.connect(self.update_status)
        self.excel_thread.task_completed.connect(self.on_excel_generated)
        self.excel_thread.start()
    
    def update_status(self, message):
        """更新状态标签"""
        self.status_label.setText(message)
    
    def on_excel_generated(self, success_modes, failed_modes):
        """Excel生成完成后的回调"""
        # 重新启用生成按钮
        for widget in self.findChildren(QPushButton):
            if widget.text() == "生成Excel":
                widget.setEnabled(True)
        
        # 显示处理结果
        result_message = ""
        if success_modes:
            result_message += f"成功处理: {', '.join(success_modes)}\n\n"
        
        if failed_modes:
            result_message += f"处理失败: {', '.join(failed_modes)}"
        
        if success_modes:
            # 创建一个置顶的消息框
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("处理完成")
            msg_box.setText(result_message)
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowFlags(msg_box.windowFlags() | Qt.WindowStaysOnTopHint)
            msg_box.exec_()
            self.status_label.setText("处理完成")
        else:
            # 创建一个置顶的错误消息框
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("处理失败")
            msg_box.setText(result_message)
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setWindowFlags(msg_box.windowFlags() | Qt.WindowStaysOnTopHint)
            msg_box.exec_()
            self.status_label.setText("处理失败")

if __name__ == "__main__":
    setup_logger()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
