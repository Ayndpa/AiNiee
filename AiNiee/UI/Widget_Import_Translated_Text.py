from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QGroupBox, QHBoxLayout, QLabel, QVBoxLayout
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import PushButton, PrimaryPushButton


class Widget_Import_Translated_Text(QFrame):  #  导入子界面
    def __init__(self, text: str, parent=None):  # 解释器会自动调用这个函数
        super().__init__(parent=parent)  # 调用父类的构造函数
        self.setObjectName(
            text.replace(" ", "-")
        )  # 设置对象名，作用是在NavigationInterface中的addItem中的routeKey参数中使用
        # 设置各个控件-----------------------------------------------------------------------------------------

        # -----创建第1个组，添加多个组件-----
        box_input = QGroupBox()
        box_input.setStyleSheet(
            """ QGroupBox {border: 1px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout_input = QHBoxLayout()

        # 设置“输入文件夹”标签
        label4 = QLabel(flags=Qt.WindowFlags())
        label4.setStyleSheet("font-family: 'Microsoft YaHei'; font-size: 17px")
        label4.setText("输入文件夹")

        # 设置“输入文件夹”显示
        self.label_input_path = QLabel(parent=self, flags=Qt.WindowFlags())
        self.label_input_path.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 11px"
        )
        self.label_input_path.setText("(请选择原文文件所在的文件夹，不要混杂其他文件)")

        # 设置打开文件按钮
        self.pushButton_input = PushButton("选择文件夹", self, FIF.FOLDER)
        # self.pushButton_input.clicked.connect(File_Reader.Select_project_folder) #按钮绑定槽函数

        layout_input.addWidget(label4)
        layout_input.addWidget(self.label_input_path)
        layout_input.addStretch(1)  # 添加伸缩项
        layout_input.addWidget(self.pushButton_input)
        box_input.setLayout(layout_input)

        # -----创建第2个组，添加多个组件-----
        box_output = QGroupBox()
        box_output.setStyleSheet(
            """ QGroupBox {border: 1px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout_output = QHBoxLayout()

        # 设置“输出文件夹”标签
        label6 = QLabel(parent=self, flags=Qt.WindowFlags())
        label6.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 17px;  color: black"
        )
        label6.setText("输出文件夹")

        # 设置“输出文件夹”显示
        self.label_output_path = QLabel(parent=self, flags=Qt.WindowFlags())
        self.label_output_path.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 11px;  color: black"
        )
        self.label_output_path.setText("(请选择翻译文件存放的文件夹)")

        # 设置输出文件夹按钮
        self.pushButton_output = PushButton("选择文件夹", self, FIF.FOLDER)
        # self.pushButton_output.clicked.connect(File_Reader.Select_output_folder) #按钮绑定槽函数

        layout_output.addWidget(label6)
        layout_output.addWidget(self.label_output_path)
        layout_output.addStretch(1)  # 添加伸缩项
        layout_output.addWidget(self.pushButton_output)
        box_output.setLayout(layout_output)

        # -----创建第x个组，添加多个组件-----
        box_start_import = QGroupBox()
        box_start_import.setStyleSheet(
            """ QGroupBox {border: 0px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout_start_import = QHBoxLayout()

        # 设置“开始翻译”的按钮
        self.primaryButton_start_import = PrimaryPushButton(
            "开始导入", self, FIF.UPDATE
        )
        # self.primaryButton_start_import.clicked.connect(self.Start_import_mtool) #按钮绑定槽函数

        layout_start_import.addStretch(1)  # 添加伸缩项
        layout_start_import.addWidget(self.primaryButton_start_import)
        layout_start_import.addStretch(1)  # 添加伸缩项
        box_start_import.setLayout(layout_start_import)

        # 最外层的垂直布局
        container = QVBoxLayout()

        # 把内容添加到容器中
        container.addStretch(1)  # 添加伸缩项
        container.addWidget(box_input)
        container.addWidget(box_output)
        container.addWidget(box_start_import)
        container.addStretch(1)  # 添加伸缩项

        # 设置窗口显示的内容是最外层容器
        self.setLayout(container)
        container.setSpacing(28)  # 设置布局内控件的间距为28
        container.setContentsMargins(
            20, 10, 20, 20
        )  # 设置布局的边距, 也就是外边框距离，分别为左、上、右、下
