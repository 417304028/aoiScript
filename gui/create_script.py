from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog


class CreateScriptWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('创建脚本')
        self.setGeometry(400, 400, 600, 400)

        main_layout = QVBoxLayout()

        # 脚本路径
        path_layout = QHBoxLayout()
        self.script_path_label = QLabel('保存路径:', self)
        path_layout.addWidget(self.script_path_label)
        self.script_path_input = QLineEdit(self)
        path_layout.addWidget(self.script_path_input)
        self.browse_button = QPushButton('选择文件', self)
        self.browse_button.clicked.connect(self.browse_files)
        path_layout.addWidget(self.browse_button)
        main_layout.addLayout(path_layout)

        # 各个任务的步骤
        self.steps_label = QLabel('各个任务的步骤（等待）', self)
        main_layout.addWidget(self.steps_label)

        # 当前已创建的流程
        self.current_process_label = QLabel('当前已创建的流程', self)
        main_layout.addWidget(self.current_process_label)

        # 分别表示移动与删除
        button_layout = QHBoxLayout()
        self.move_button = QPushButton('移动', self)
        button_layout.addWidget(self.move_button)
        self.delete_button = QPushButton('删除', self)
        button_layout.addWidget(self.delete_button)
        main_layout.addLayout(button_layout)

        # 创建脚本按钮
        self.create_button = QPushButton('创建脚本', self)
        self.create_button.clicked.connect(self.create_script)
        main_layout.addWidget(self.create_button)

        self.setLayout(main_layout)

    def browse_files(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "选择文件", "", "All Files (*);;Python Files (*.py)",
                                                   options=options)
        if file_name:
            self.script_path_input.setText(file_name)

    def create_script(self):
        script_path = self.script_path_input.text()
        # 在这里添加创建脚本的逻辑
        print(f"创建脚本: {script_path}")
        self.accept()
