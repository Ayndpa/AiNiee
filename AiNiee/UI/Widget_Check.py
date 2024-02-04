from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QLabel, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout
from qfluentwidgets import (
    PushButton,
    PrimaryPushButton,
    ComboBox,
    SpinBox,
    DoubleSpinBox,
)
from qfluentwidgets import FluentIcon as FIF
from ..Basic_Logic.File_Reader import File_Reader

from ..Global import Global


class Widget_Check(QFrame):  # 错行检查界面
    def __init__(self, text: str, parent=None):  # 解释器会自动调用这个函数
        super().__init__(parent=parent)  # 调用父类的构造函数
        self.setObjectName(
            text.replace(" ", "-")
        )  # 设置对象名，作用是在NavigationInterface中的addItem中的routeKey参数中使用
        # 设置各个控件-----------------------------------------------------------------------------------------

        # -----创建第0-1个组，添加多个组件-----
        box_weight = QGroupBox()
        box_weight.setStyleSheet(
            """ QGroupBox {border: 1px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout_weight = QHBoxLayout()

        # 设置“语义权重”标签
        label0_1 = QLabel(flags=Qt.WindowFlags())
        label0_1.setStyleSheet("font-family: 'Microsoft YaHei'; font-size: 17px;")
        label0_1.setText("语义权重")

        # 设置“语义权重”输入
        self.doubleSpinBox_semantic_weight = DoubleSpinBox(self)
        self.doubleSpinBox_semantic_weight.setMaximum(1.0)
        self.doubleSpinBox_semantic_weight.setMinimum(0.0)
        self.doubleSpinBox_semantic_weight.setValue(0.6)

        # 设置“符号权重”标签
        label0_2 = QLabel(flags=Qt.WindowFlags())
        label0_2.setStyleSheet("font-family: 'Microsoft YaHei'; font-size: 17px;")
        label0_2.setText("符号权重")

        # 设置“符号权重”输入
        self.doubleSpinBox_symbol_weight = DoubleSpinBox(self)
        self.doubleSpinBox_symbol_weight.setMaximum(1.0)
        self.doubleSpinBox_symbol_weight.setMinimum(0.0)
        self.doubleSpinBox_symbol_weight.setValue(0.2)

        # 设置“字数权重”标签
        label0_3 = QLabel(flags=Qt.WindowFlags())
        label0_3.setStyleSheet("font-family: 'Microsoft YaHei'; font-size: 17px;")
        label0_3.setText("字数权重")

        # 设置“字数权重”输入
        self.doubleSpinBox_word_count_weight = DoubleSpinBox(self)
        self.doubleSpinBox_word_count_weight.setMaximum(1.0)
        self.doubleSpinBox_word_count_weight.setMinimum(0.0)
        self.doubleSpinBox_word_count_weight.setValue(0.2)

        layout_weight.addWidget(label0_1)
        layout_weight.addWidget(self.doubleSpinBox_semantic_weight)
        layout_weight.addStretch(1)  # 添加伸缩项
        layout_weight.addWidget(label0_2)
        layout_weight.addWidget(self.doubleSpinBox_symbol_weight)
        layout_weight.addStretch(1)  # 添加伸缩项
        layout_weight.addWidget(label0_3)
        layout_weight.addWidget(self.doubleSpinBox_word_count_weight)

        box_weight.setLayout(layout_weight)

        # -----创建第0-2个组，添加多个组件-----
        box_similarity_threshold = QGroupBox()
        box_similarity_threshold.setStyleSheet(
            """ QGroupBox {border: 1px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout_similarity_threshold = QHBoxLayout()

        # 设置“相似度阈值”标签
        label0_4 = QLabel(flags=Qt.WindowFlags())
        label0_4.setStyleSheet("font-family: 'Microsoft YaHei'; font-size: 17px;")
        label0_4.setText("相似度阈值")

        # 设置“相似度阈值”输入
        self.spinBox_similarity_threshold = SpinBox(self)
        self.spinBox_similarity_threshold.setMaximum(100)
        self.spinBox_similarity_threshold.setMinimum(0)
        self.spinBox_similarity_threshold.setValue(50)

        layout_similarity_threshold.addWidget(label0_4)
        layout_similarity_threshold.addStretch(1)  # 添加伸缩项
        layout_similarity_threshold.addWidget(self.spinBox_similarity_threshold)
        box_similarity_threshold.setLayout(layout_similarity_threshold)

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
        self.labelx.setText("重翻平台")

        # 设置“翻译平台”下拉选择框
        self.comboBox_translation_platform = ComboBox()  # 以demo为父类
        self.comboBox_translation_platform.addItems(["Openai官方", "Openai代理"])
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
        self.labelx.setText("检查项目")

        # 设置“翻译项目”下拉选择框
        self.comboBox_translation_project = ComboBox()  # 以demo为父类
        self.comboBox_translation_project.addItems(["Mtool导出文件", "T++导出文件"])
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
        self.label_input_path.setText("(请选择已翻译文件所在的文件夹)")

        # 设置打开文件按钮
        self.pushButton_input = PushButton("选择文件夹", self, FIF.FOLDER)
        self.pushButton_input.clicked.connect(
            File_Reader.Select_project_folder_check
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
        self.label_output_path.setText("(请选择检查重翻后文件存放的文件夹)")

        # 设置输出文件夹按钮
        self.pushButton_output = PushButton("选择文件夹", self, FIF.FOLDER)
        self.pushButton_output.clicked.connect(
            File_Reader.Select_output_folder_check
        )  # 按钮绑定槽函数

        layout_output.addWidget(label6)
        layout_output.addWidget(self.label_output_path)
        layout_output.addStretch(1)  # 添加伸缩项
        layout_output.addWidget(self.pushButton_output)
        box_output.setLayout(layout_output)

        # -----创建第3个组，添加多个组件-----
        box_check = QGroupBox()
        box_check.setStyleSheet(
            """ QGroupBox {border: 0px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout_check = QHBoxLayout()

        # 设置“保存配置”的按钮
        self.primaryButton_save = PushButton("保存配置", self, FIF.SAVE)
        self.primaryButton_save.clicked.connect(self.saveconfig)  # 按钮绑定槽函数

        # 设置“开始检查”的按钮
        self.primaryButton1 = PrimaryPushButton("开始检查错行", self, FIF.UPDATE)
        self.primaryButton1.clicked.connect(self.Start_check)  # 按钮绑定槽函数

        layout_check.addStretch(1)  # 添加伸缩项
        layout_check.addWidget(self.primaryButton_save)
        layout_check.addStretch(1)  # 添加伸缩项
        layout_check.addWidget(self.primaryButton1)
        layout_check.addStretch(1)  # 添加伸缩项
        box_check.setLayout(layout_check)

        # 最外层的垂直布局
        container = QVBoxLayout()

        # 把内容添加到容器中
        container.addStretch(1)  # 添加伸缩项
        container.addWidget(box_weight)
        container.addWidget(box_similarity_threshold)
        container.addWidget(box_translation_platform)
        container.addWidget(box_translation_project)
        container.addWidget(box_input)
        container.addWidget(box_output)
        container.addWidget(box_check)
        container.addStretch(1)  # 添加伸缩项

        # 设置窗口显示的内容是最外层容器
        self.setLayout(container)
        container.setSpacing(28)  # 设置布局内控件的间距为28
        container.setContentsMargins(
            50, 70, 50, 30
        )  # 设置布局的边距, 也就是外边框距离，分别为左、上、右、下

    def saveconfig(self):
        Global.configurator.read_write_config("write")
        Global.user_interface_prompter.createSuccessInfoBar("已成功保存配置")

    # 开始翻译按钮绑定函数
    def Start_check(self):
        if Global.Running_status == 0:
            # 创建子线程
            thread = Global.background_executor("执行检查任务")
            thread.start()

        elif Global.Running_status != 0:
            Global.user_interface_prompter.createWarningInfoBar(
                "正在进行任务中，请等待任务结束后再操作~"
            )
