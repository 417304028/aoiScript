from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QListWidget, QListWidgetItem, QInputDialog
import gui.create_script as cs

class CreateScriptWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('创建脚本')
        self.setGeometry(400, 400, 600, 400)

        main_layout = QHBoxLayout()

        # 左侧布局
        left_layout = QVBoxLayout()

        # 脚本路径
        path_layout = QHBoxLayout()
        self.script_path_label = QLabel('保存路径:', self)
        path_layout.addWidget(self.script_path_label)
        self.script_path_input = QLineEdit(self)
        path_layout.addWidget(self.script_path_input)
        self.browse_button = QPushButton('选择路径', self)
        self.browse_button.clicked.connect(self.browse_files)
        path_layout.addWidget(self.browse_button)
        left_layout.addLayout(path_layout)

        # 脚本列表
        self.script_list_label = QLabel('脚本列表', self)
        left_layout.addWidget(self.script_list_label)
        self.script_list = QListWidget(self)
        left_layout.addWidget(self.script_list)

        # 增加步骤按钮
        self.add_step_button = QPushButton('增加步骤', self)
        self.add_step_button.clicked.connect(self.add_step)
        left_layout.addWidget(self.add_step_button)

        main_layout.addLayout(left_layout)

        # 右侧布局
        right_layout = QVBoxLayout()

        # 当前已创建的流程
        self.current_process_label = QLabel('当前已创建的流程', self)
        right_layout.addWidget(self.current_process_label)
        self.process_list = QListWidget(self)
        self.process_list.setDragDropMode(QListWidget.InternalMove)
        right_layout.addWidget(self.process_list)

        # 分别表示移动与删除
        button_layout = QHBoxLayout()
        self.delete_button = QPushButton('删除', self)
        self.delete_button.clicked.connect(self.delete_step)
        button_layout.addWidget(self.delete_button)
        right_layout.addLayout(button_layout)

        # 创建脚本按钮
        self.create_button = QPushButton('创建脚本', self)
        self.create_button.clicked.connect(self.create_script)
        right_layout.addWidget(self.create_button)

        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)

    def browse_files(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "选择文件", "", "All Files (*);;Python Files (*.py)",
                                                   options=options)
        if file_name:
            self.script_path_input.setText(file_name)

    def add_step(self):
        # 添加步骤的逻辑
        step_name, ok = QInputDialog.getText(self, '增加步骤', '输入步骤名称:')
        if ok and step_name:
            self.process_list.addItem(QListWidgetItem(step_name))

    def delete_step(self):
        # 删除步骤的逻辑
        current_row = self.process_list.currentRow()
        if current_row >= 0:
            self.process_list.takeItem(current_row)

    def create_script(self):
        script_path = self.script_path_input.text()
        # 在这里添加创建脚本的逻辑
        print(f"创建脚本: {script_path}")
        self.accept()