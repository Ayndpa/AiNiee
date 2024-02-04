from PyQt5.QtWidgets import (
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QFileDialog,
)
from PyQt5.QtCore import Qt
from qfluentwidgets import CheckBox, PushButton, FluentIcon as FIF
from ..Basic_Logic.File_Outputter import File_Outputter

from ..Global import Global


class Widget_Start_Translation_B(QFrame):  #  开始翻译子界面
    def __init__(self, text: str, parent=None):  # 解释器会自动调用这个函数
        super().__init__(parent=parent)  # 调用父类的构造函数
        self.setObjectName(
            text.replace(" ", "-")
        )  # 设置对象名，作用是在NavigationInterface中的addItem中的routeKey参数中使用
        # 设置各个控件-----------------------------------------------------------------------------------------

        # -----创建第1个组，添加多个组件-----
        box_switch = QGroupBox()
        box_switch.setStyleSheet(
            """ QGroupBox {border: 1px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout_switch = QHBoxLayout()

        label1 = QLabel(flags=Qt.WindowFlags())
        label1.setStyleSheet("font-family: 'Microsoft YaHei'; font-size: 17px;")
        label1.setText("自动备份缓存文件到输出文件夹")

        self.checkBox_switch = CheckBox("启用功能")
        self.checkBox_switch.stateChanged.connect(self.checkBoxChanged1)

        layout_switch.addWidget(label1)
        layout_switch.addStretch(1)  # 添加伸缩项
        layout_switch.addWidget(self.checkBox_switch)
        box_switch.setLayout(layout_switch)

        # -----创建第1个组，添加多个组件-----
        box_export_cache_file_path = QGroupBox()
        box_export_cache_file_path.setStyleSheet(
            """ QGroupBox {border: 1px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout_export_cache_file_path = QHBoxLayout()

        # 设置“导出当前任务的缓存文件”标签
        label4 = QLabel(flags=Qt.WindowFlags())
        label4.setStyleSheet("font-family: 'Microsoft YaHei'; font-size: 17px")
        label4.setText("导出当前任务的缓存文件")

        # 设置导出当前任务的缓存文件按钮
        self.pushButton_export_cache_file_path = PushButton(
            "选择文件夹", self, FIF.FOLDER
        )
        self.pushButton_export_cache_file_path.clicked.connect(
            self.output_cachedata
        )  # 按钮绑定槽函数

        layout_export_cache_file_path.addWidget(label4)
        layout_export_cache_file_path.addStretch(1)  # 添加伸缩项
        layout_export_cache_file_path.addWidget(self.pushButton_export_cache_file_path)
        box_export_cache_file_path.setLayout(layout_export_cache_file_path)

        # -----创建第2个组，添加多个组件-----
        box_export_translated_file_path = QGroupBox()
        box_export_translated_file_path.setStyleSheet(
            """ QGroupBox {border: 1px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout_export_translated_file_path = QHBoxLayout()

        # 设置“导出当前任务的已翻译文本”标签
        label6 = QLabel(parent=self, flags=Qt.WindowFlags())
        label6.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 17px;  color: black"
        )
        label6.setText("导出当前任务的已翻译文本")

        # 设置导出当前任务的已翻译文本按钮
        self.pushButton_export_translated_file_path = PushButton(
            "选择文件夹", self, FIF.FOLDER
        )
        self.pushButton_export_translated_file_path.clicked.connect(
            self.output_data
        )  # 按钮绑定槽函数

        layout_export_translated_file_path.addWidget(label6)
        layout_export_translated_file_path.addStretch(1)  # 添加伸缩项
        layout_export_translated_file_path.addWidget(
            self.pushButton_export_translated_file_path
        )
        box_export_translated_file_path.setLayout(layout_export_translated_file_path)

        # -----最外层容器设置垂直布局-----
        container = QVBoxLayout()

        # 设置窗口显示的内容是最外层容器
        self.setLayout(container)
        container.setSpacing(28)  # 设置布局内控件的间距为28
        container.setContentsMargins(
            20, 10, 20, 20
        )  # 设置布局的边距, 也就是外边框距离，分别为左、上、右、下

        # 把各个组添加到容器中
        container.addStretch(1)  # 添加伸缩项
        container.addWidget(box_switch)
        container.addWidget(box_export_cache_file_path)
        container.addWidget(box_export_translated_file_path)
        container.addStretch(1)  # 添加伸缩项

    # 提示函数
    def checkBoxChanged1(self, isChecked: bool):
        if isChecked:
            Global.user_interface_prompter.createSuccessInfoBar("已开启自动备份功能")

    # 缓存文件输出
    def output_cachedata(self):
        Output_Folder = QFileDialog.getExistingDirectory(
            None, "Select Directory", ""
        )  # 调用QFileDialog类里的函数来选择文件目录
        if Output_Folder:
            print("[INFO]  已选择输出文件夹:", Output_Folder)

            if len(Global.cache_list) >= 3:
                File_Outputter.output_cache_file(self, Global.cache_list, Output_Folder)
                Global.user_interface_prompter.createSuccessInfoBar("已输出缓存文件")
                print("[INFO]  已输出缓存文件")
            else:
                print("[INFO]  未存在缓存文件")
                return  # 直接返回，不执行后续操作
        else:
            print("[INFO]  未选择文件夹")
            return  # 直接返回，不执行后续操作

    # 缓存文件输出
    def output_data(self):
        Output_Folder = QFileDialog.getExistingDirectory(
            None, "Select Directory", ""
        )  # 调用QFileDialog类里的函数来选择文件目录
        if Output_Folder:
            print("[INFO]  已选择输出文件夹:", Output_Folder)

            if len(Global.cache_list) >= 3:
                File_Outputter.output_translated_content(
                    self, Global.cache_list, Output_Folder
                )
                Global.user_interface_prompter.createSuccessInfoBar("已输出已翻译文件")
                print("[INFO]  已输出已翻译文件")
            else:
                print("[INFO]  未存在缓存文件")
                return  # 直接返回，不执行后续操作
        else:
            print("[INFO]  未选择文件夹")
            return  # 直接返回，不执行后续操作
