from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QListWidget, \
    QListWidgetItem, QInputDialog, QFormLayout, QComboBox, QWidget, QStatusBar, QSpacerItem, QSizePolicy

import config


class CreateScriptWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('创建脚本')
        self.setGeometry(400, 400, 800, 600)
        self.setWindowIcon(QIcon(config.PYQT_ICON))

        main_layout = QHBoxLayout()

        # 控制按钮
        control_layout = QVBoxLayout()
        self.add_step_button = QPushButton('增加步骤', self)
        self.add_step_button.clicked.connect(self.add_step)
        self.delete_step_button = QPushButton('删除步骤', self)
        self.delete_step_button.clicked.connect(self.delete_step)
        control_layout.addWidget(self.add_step_button)
        control_layout.addWidget(self.delete_step_button)
        control_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        main_layout.addLayout(control_layout)

        # 步骤库
        self.step_library_label = QLabel('步骤库', self)
        self.step_library = QListWidget(self)
        self.step_library.addItems(['步骤1', '步骤2', '步骤3'])  # 示例步骤
        self.step_library.itemClicked.connect(self.add_step_from_library)

        # 步骤种类
        self.step_category_label = QLabel('步骤种类', self)
        self.step_category = QComboBox(self)
        self.step_category.addItems(['检测类', '点击类', '拖动类', '其他类'])  # 示例种类
        self.step_category.activated[str].connect(self.change_step_category)

        library_layout = QVBoxLayout()
        library_layout.addWidget(self.step_category_label)
        library_layout.addWidget(self.step_category)
        library_layout.addWidget(self.step_library_label)
        library_layout.addWidget(self.step_library)
        main_layout.addLayout(library_layout)

        # 当前流程
        self.current_process_label = QLabel('当前流程', self)
        self.process_list = QListWidget(self)
        self.process_list.setFixedWidth(200)  # 调整宽度
        self.process_list.setDragDropMode(QListWidget.InternalMove)
        self.process_list.itemClicked.connect(self.show_step_parameters)

        process_layout = QVBoxLayout()
        process_layout.addWidget(self.current_process_label)
        process_layout.addWidget(self.process_list)
        main_layout.addLayout(process_layout)

        # 步骤参数配置
        self.step_parameters_label = QLabel('步骤参数配置', self)
        self.step_parameters_form = QFormLayout()
        self.step_parameters_widget = QWidget()
        self.step_parameters_widget.setLayout(self.step_parameters_form)

        parameters_layout = QVBoxLayout()
        parameters_layout.addWidget(self.step_parameters_label)
        parameters_layout.addWidget(self.step_parameters_widget)
        main_layout.addLayout(parameters_layout)

        # 右侧按钮
        right_layout = QVBoxLayout()
        self.save_process_button = QPushButton('保存流程', self)
        self.load_process_button = QPushButton('加载流程', self)
        self.run_process_button = QPushButton('运行流程', self)
        self.create_script_button = QPushButton('创建脚本', self)
        self.run_process_button.clicked.connect(self.run_process)
        self.create_script_button.clicked.connect(self.create_script)

        right_layout.addWidget(self.save_process_button)
        right_layout.addWidget(self.load_process_button)
        right_layout.addWidget(self.run_process_button)
        right_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        right_layout.addWidget(self.create_script_button)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)

        # 初始化状态栏
        self.status_bar = QStatusBar(self)
        main_layout.addWidget(self.status_bar)

    def add_step_from_library(self, item):
        self.process_list.addItem(QListWidgetItem(item.text()))

    def change_step_category(self, category):
        # 根据选择的步骤种类更新步骤库
        steps = {
            '检测类': ['检测步骤1', '检测步骤2'],
            '点击类': ['点击步骤1', '点击步骤2'],
            '拖动类': ['拖动步骤1', '拖动步骤2'],
            '其他类': ['其他步骤1', '其他步骤2']
        }
        self.step_library.clear()
        self.step_library.addItems(steps.get(category, []))

    def add_step(self):
        selected_items = self.step_library.currentItem()
        if selected_items:
            self.process_list.addItem(QListWidgetItem(selected_items.text()))
        else:
            step_name, ok = QInputDialog.getText(self, '增加步骤', '输入步骤名称:')
            if ok and step_name:
                self.process_list.addItem(QListWidgetItem(step_name))

    def delete_step(self):
        current_row = self.process_list.currentRow()
        if current_row >= 0:
            self.process_list.takeItem(current_row)

    def show_step_parameters(self, item):
        # 清空当前参数配置
        for i in reversed(range(self.step_parameters_form.count())):
            self.step_parameters_form.removeRow(i)
        # 示例参数配置
        self.step_parameters_form.addRow('参数1:', QLineEdit())
        self.step_parameters_form.addRow('参数2:', QComboBox())

    def run_process(self):
        # 运行流程的逻辑
        for i in range(self.process_list.count()):
            step_item = self.process_list.item(i)
            print(f"执行步骤: {step_item.text()}")
        self.status_bar.showMessage("流程执行完毕")
        QTimer.singleShot(5000, self.clear_status_message)

    def clear_status_message(self):
        self.status_bar.clearMessage()

    def create_script(self):
        script_code = ""
        for i in range(self.process_list.count()):
            step_item = self.process_list.item(i)
            step_code = self.generate_step_code(step_item.text())
            script_code += step_code + "\n"
        
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "保存脚本", "", "Python Files (*.py);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'w') as file:
                file.write(script_code)
            self.status_bar.showMessage("脚本已创建")
            QTimer.singleShot(5000, self.clear_status_message)

    def generate_step_code(self, step_name):
        # 根据步骤名称生成对应的代码
        step_code_map = {
            '步骤1': 'print("执行步骤1")',
            '步骤2': 'print("执行步骤2")',
            '步骤3': 'print("执行步骤3")',
            '检测步骤1': 'print("执行检测步骤1")',
            '检测步骤2': 'print("执行检测步骤2")',
            '点击步骤1': 'print("执行点击步骤1")',
            '点击步骤2': 'print("执行点击步骤2")',
            '拖动步骤1': 'print("执行拖动步骤1")',
            '拖动步骤2': 'print("执行拖动步骤2")',
            '其他步骤1': 'print("执行其他步骤1")',
            '其他步骤2': 'print("执行其他步骤2")'
        }
        return step_code_map.get(step_name, f'# 未知步骤: {step_name}')