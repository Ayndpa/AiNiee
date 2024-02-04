from PyQt5.QtWidgets import (
    QFrame,
    QGroupBox,
    QGridLayout,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
)
from PyQt5.QtCore import Qt
from qfluentwidgets import ComboBox, PushButton, FluentIcon as FIF
from ..Basic_Logic.File_Reader import File_Reader

from ..Global import Global


class Widget_Translation_Settings_A(QFrame):  #  基础设置子界面
    def __init__(self, text: str, parent=None):  # 解释器会自动调用这个函数
        super().__init__(parent=parent)  # 调用父类的构造函数
        self.setObjectName(
            text.replace(" ", "-")
        )  # 设置对象名，作用是在NavigationInterface中的addItem中的routeKey参数中使用
        # 设置各个控件-----------------------------------------------------------------------------------------

        # -----创建第1个组，添加多个组件-----
        box_translation_platform = QGroupBox()
        box_translation_platform.setStyleSheet(
            """ QGroupBox {border: 1px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout_translation_platform = QGridLayout()

        # 设置“翻译平台”标签
        self.labelx = QLabel(flags=Qt.WindowFlags())
        self.labelx.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 17px; "
        )  # 设置字体，大小，颜色
        self.labelx.setText("翻译平台")

        # 设置“翻译平台”下拉选择框
        self.comboBox_translation_platform = ComboBox()  # 以demo为父类
        self.comboBox_translation_platform.addItems(
            ["Openai官方", "Openai代理", "Google官方", "SakuraLLM"]
        )
        self.comboBox_translation_platform.setCurrentIndex(
            0
        )  # 设置下拉框控件（ComboBox）的当前选中项的索引为0，也就是默认选中第一个选项
        self.comboBox_translation_platform.setFixedSize(150, 35)

        layout_translation_platform.addWidget(self.labelx, 0, 0)
        layout_translation_platform.addWidget(self.comboBox_translation_platform, 0, 1)
        box_translation_platform.setLayout(layout_translation_platform)

        # -----创建第1个组，添加多个组件-----
        box_translation_project = QGroupBox()
        box_translation_project.setStyleSheet(
            """ QGroupBox {border: 1px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout_translation_project = QGridLayout()

        # 设置“翻译项目”标签
        self.labelx = QLabel(flags=Qt.WindowFlags())
        self.labelx.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 17px; "
        )  # 设置字体，大小，颜色
        self.labelx.setText("翻译项目")

        # 设置“翻译项目”下拉选择框
        self.comboBox_translation_project = ComboBox()  # 以demo为父类
        self.comboBox_translation_project.addItems(
            ["Mtool导出文件", "T++导出文件", "Ainiee缓存文件"]
        )
        self.comboBox_translation_project.setCurrentIndex(
            0
        )  # 设置下拉框控件（ComboBox）的当前选中项的索引为0，也就是默认选中第一个选项
        self.comboBox_translation_project.setFixedSize(150, 35)

        layout_translation_project.addWidget(self.labelx, 0, 0)
        layout_translation_project.addWidget(self.comboBox_translation_project, 0, 1)
        box_translation_project.setLayout(layout_translation_project)

        # -----创建第2个组，添加多个组件-----
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
        self.pushButton_input.clicked.connect(
            File_Reader.Select_project_folder
        )  # 按钮绑定槽函数

        layout_input.addWidget(label4)
        layout_input.addWidget(self.label_input_path)
        layout_input.addStretch(1)  # 添加伸缩项
        layout_input.addWidget(self.pushButton_input)
        box_input.setLayout(layout_input)

        # -----创建第3个组，添加多个组件-----
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
        self.pushButton_output.clicked.connect(
            File_Reader.Select_output_folder
        )  # 按钮绑定槽函数

        layout_output.addWidget(label6)
        layout_output.addWidget(self.label_output_path)
        layout_output.addStretch(1)  # 添加伸缩项
        layout_output.addWidget(self.pushButton_output)
        box_output.setLayout(layout_output)

        # -----创建第4个组，添加多个组件-----
        box_source_text = QGroupBox()
        box_source_text.setStyleSheet(
            """ QGroupBox {border: 1px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout_source_text = QHBoxLayout()

        # 设置“文本源语言”标签
        label3 = QLabel(parent=self, flags=Qt.WindowFlags())
        label3.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 17px;  color: black"
        )
        label3.setText("文本源语言")

        # 设置“文本源语言”下拉选择框
        self.comboBox_source_text = ComboBox()  # 以demo为父类
        self.comboBox_source_text.addItems(
            ["日语", "英语", "韩语", "俄语", "简中", "繁中"]
        )
        self.comboBox_source_text.setCurrentIndex(
            0
        )  # 设置下拉框控件（ComboBox）的当前选中项的索引为0，也就是默认选中第一个选项
        self.comboBox_source_text.setFixedSize(127, 30)

        layout_source_text.addWidget(label3)
        layout_source_text.addWidget(self.comboBox_source_text)
        box_source_text.setLayout(layout_source_text)

        # -----创建第5个组(后面添加的)，添加多个组件-----
        box_translated_text = QGroupBox()
        box_translated_text.setStyleSheet(
            """ QGroupBox {border: 1px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout_translated_text = QHBoxLayout()

        # 设置“文本目标语言”标签
        label3_1 = QLabel(parent=self, flags=Qt.WindowFlags())
        label3_1.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 17px;  color: black"
        )
        label3_1.setText("文本目标语言")

        # 设置“文本目标语言”下拉选择框
        self.comboBox_translated_text = ComboBox()  # 以demo为父类
        self.comboBox_translated_text.addItems(["简中", "繁中", "日语", "英语", "韩语"])
        self.comboBox_translated_text.setCurrentIndex(
            0
        )  # 设置下拉框控件（ComboBox）的当前选中项的索引为0，也就是默认选中第一个选项
        self.comboBox_translated_text.setFixedSize(127, 30)

        layout_translated_text.addWidget(label3_1)
        layout_translated_text.addWidget(self.comboBox_translated_text)
        box_translated_text.setLayout(layout_translated_text)

        # -----创建第6个组，添加多个组件-----
        box_save = QGroupBox()
        box_save.setStyleSheet(
            """ QGroupBox {border: 0px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout_save = QHBoxLayout()

        # 设置“保存配置”的按钮
        self.primaryButton_save = PushButton("保存配置", self, FIF.SAVE)
        self.primaryButton_save.clicked.connect(self.saveconfig)  # 按钮绑定槽函数

        layout_save.addStretch(1)  # 添加伸缩项
        layout_save.addWidget(self.primaryButton_save)
        layout_save.addStretch(1)  # 添加伸缩项
        box_save.setLayout(layout_save)

        # 最外层的垂直布局
        container = QVBoxLayout()

        # 把内容添加到容器中
        container.addStretch(1)  # 添加伸缩项
        container.addWidget(box_translation_project)
        container.addWidget(box_translation_platform)
        container.addWidget(box_source_text)
        container.addWidget(box_translated_text)
        container.addWidget(box_input)
        container.addWidget(box_output)
        container.addWidget(box_save)
        container.addStretch(1)  # 添加伸缩项

        # 设置窗口显示的内容是最外层容器
        self.setLayout(container)
        container.setSpacing(28)  # 设置布局内控件的间距为28
        container.setContentsMargins(
            20, 10, 20, 20
        )  # 设置布局的边距, 也就是外边框距离，分别为左、上、右、下

    def saveconfig(self):
        Global.configurator.read_write_config("write")
        Global.user_interface_prompter.createSuccessInfoBar("已成功保存配置")
