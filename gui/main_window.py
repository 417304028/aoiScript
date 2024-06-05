from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QLabel, QLineEdit, QFileDialog, QScrollArea, QStyle, \
    QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSettings, QSize, Qt
import sys, os, subprocess
# import gui.create_script as cs
from gui.create_script import CreateScriptWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.statusBar()
    def initUI(self):
        # 窗口设置
        self.setWindowTitle('AOI关联脚本')
        self.setGeometry(300, 300, 600, 400)
        self.setWindowIcon(QIcon('gui/resources/sinictek.jpg'))  # 设置窗口图标

        # 路径输入文本框
        self.script_path_label = QLabel('脚本/脚本文件夹', self)
        self.script_path_label.move(50, 50)
        self.script_path_input = QLineEdit(self)
        self.script_path_input.setGeometry(150, 50, 250, 30)
        # 选择脚本按钮
        self.browse_file_button = QPushButton(self)
        self.browse_file_button.setGeometry(410, 50, 30, 30)
        self.browse_file_button.setIcon(self.style().standardIcon(QStyle.SP_FileDialogNewFolder))
        self.browse_file_button.setToolTip('选择脚本')
        self.browse_file_button.setIconSize(QSize(20, 20))
        self.browse_file_button.clicked.connect(self.browse_file)
        # 选择脚本文件夹按钮
        self.browse_folder_button = QPushButton(self)
        self.browse_folder_button.setGeometry(440, 50, 30, 30)
        self.browse_folder_button.setIcon(self.style().standardIcon(QStyle.SP_DialogOpenButton))
        self.browse_folder_button.setToolTip('选择脚本文件夹')
        self.browse_folder_button.setIconSize(QSize(20, 20))
        self.browse_folder_button.clicked.connect(self.browse_folder)
        # 准备运行的脚本文字
        self.target_script_label = QLabel('准备运行的脚本', self)
        self.target_script_label.move(50, 100)
        # 滚动的显示准备运行的脚本
        self.script_label = QLabel('', self)
        self.script_label.setWordWrap(True)
        self.script_label.setAlignment(Qt.AlignTop)  # 设置为居上对齐
        # 组合形成可以滚动的一片区域
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setGeometry(150, 100, 250, 100)
        self.scroll_area.setWidget(self.script_label)
        self.scroll_area.setWidgetResizable(True)
        # 执行脚本按钮
        self.execute_button = QPushButton(self)
        self.execute_button.setGeometry(410, 100, 30, 30)  # 调整按钮大小
        self.execute_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.execute_button.setToolTip('执行脚本')
        self.execute_button.setIconSize(QSize(24, 24))  # 调整图标大小
        self.execute_button.clicked.connect(self.execute_script)
        # 创建脚本按钮
        self.create_script_button = QPushButton('创建脚本', self)
        self.create_script_button.setGeometry(350, 300, 100, 40)
        self.create_script_button.clicked.connect(self.open_create_window)
        # 加载默认路径
        self.load_default_path()

    # 拼接/换行文件名
    def process_name(self, path, is_folder=False):
        if is_folder:
            files = [f for f in os.listdir(path) if f.endswith('.py') or f.endswith('.exe')]
            display_text = "\n".join(files)
        else:
            if isinstance(path, list):
                display_text = "\n".join([os.path.basename(p) for p in path])
            else:
                display_text = os.path.basename(path)

        self.script_label.setText(display_text)

    # 浏览文件
    def browse_file(self):
        options = QFileDialog.Options()
        file_names, _ = QFileDialog.getOpenFileNames(self, "选择文件", "/", "Python Files (*.py);;All Files (*)",
                                                     options=options)
        if file_names:
            self.script_path_input.setText("; ".join(file_names))
            self.process_name(file_names)
            self.save_default_path(file_names)

    # 浏览文件夹
    def browse_folder(self):
        options = QFileDialog.Options()
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹", "/", options=options)
        if folder_path:
            self.script_path_input.setText(folder_path)
            self.process_name(folder_path, is_folder=True)
            self.save_default_path([folder_path])
            # 执行脚本

    def execute_script(self):
        script_path = self.script_path_input.text()
        target_script = self.script_label.text()
        self.statusBar().showMessage("脚本执行已开始，请稍候...")
        try:
            # 如果是单个文件的话执行单个文件
            if os.path.isfile(script_path) and script_path.endswith('.exe'):
                self.showMinimized()
                subprocess.run([script_path], check=True)
            # 如果是多个文件的话，按顺序一个一个执行
            elif isinstance(script_path, list):
                self.showMinimized()
                for path in script_path:
                    if path.endswith('.exe'):
                        subprocess.run([path], check=True)
            # 如果是文件夹的话执行该文件夹下所有文件
            elif os.path.isdir(script_path):
                self.showMinimized()
                for file in os.listdir(script_path):
                    if file.endswith('.exe'):
                        full_path = os.path.join(script_path, file)
                        subprocess.run([full_path], check=True)
            print(f"执行脚本: {script_path} 目标: {target_script}")
        except Exception as e:
            self.statusBar().showMessage(f"发生错误: {e}")
        else:
            self.statusBar().showMessage("脚本开始执行，请稍后")

    # 打开创建脚本窗口
    def open_create_window(self):
        self.create_script_window = CreateScriptWindow()
        self.create_script_window.exec_()

    # 存为默认路径分别下次打开时使用
    def save_default_path(self, paths):
        settings = QSettings('Sinic-Tek', 'AOI')
        if isinstance(paths, list):
            # 如果是路径列表，将它们连接成一个字符串
            path_string = "; ".join(paths)
        else:
            # 如果不是列表（即单个路径），直接使用
            path_string = paths
        settings.setValue('default_script_path', path_string)

    # 加载上次的路径
    def load_default_path(self):
        settings = QSettings('Sinic-Tek', 'AOI')
        default_path = settings.value('default_script_path', '')
        if default_path:
            self.script_path_input.setText(default_path)
            self.script_label.setText(default_path)


def start_gui():
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
