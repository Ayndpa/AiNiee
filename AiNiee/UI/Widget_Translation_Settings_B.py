from PyQt5.QtWidgets import QFrame, QGroupBox, QHBoxLayout, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from qfluentwidgets import SpinBox, SwitchButton

from ..Global import Global


class Widget_Translation_Settings_B(QFrame):  #  进阶设置子界面
    def __init__(self, text: str, parent=None):  # 解释器会自动调用这个函数
        super().__init__(parent=parent)  # 调用父类的构造函数
        self.setObjectName(
            text.replace(" ", "-")
        )  # 设置对象名，作用是在NavigationInterface中的addItem中的routeKey参数中使用
        # 设置各个控件-----------------------------------------------------------------------------------------

        # -----创建第1个组，添加多个组件-----
        box_Lines = QGroupBox()
        box_Lines.setStyleSheet(
            """ QGroupBox {border: 1px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout_Lines = QHBoxLayout()

        # 设置“翻译行数”标签
        label1 = QLabel(parent=self, flags=Qt.WindowFlags())
        label1.setStyleSheet("font-family: 'Microsoft YaHei'; font-size: 17px")
        label1.setText("每次翻译行数")

        # 设置“翻译行数”数值输入框
        self.spinBox_Lines = SpinBox(self)
        self.spinBox_Lines.setRange(1, 1000)
        self.spinBox_Lines.setValue(30)

        layout_Lines.addWidget(label1)
        layout_Lines.addStretch(1)  # 添加伸缩项
        layout_Lines.addWidget(self.spinBox_Lines)
        box_Lines.setLayout(layout_Lines)

        # -----创建第1.4个组(后来补的)，添加多个组件-----
        box1_jsonmode = QGroupBox()
        box1_jsonmode.setStyleSheet(
            """ QGroupBox {border: 1px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout1_jsonmode = QHBoxLayout()

        # 设置“回复json格式”标签
        labe1_4 = QLabel(flags=Qt.WindowFlags())
        labe1_4.setStyleSheet("font-family: 'Microsoft YaHei'; font-size: 17px")
        labe1_4.setText("回复json格式")

        # 设置“回复json格式”选择开关
        self.SwitchButton_jsonmode = SwitchButton(parent=self)
        self.SwitchButton_jsonmode.checkedChanged.connect(self.onjsonmode)

        layout1_jsonmode.addWidget(labe1_4)
        layout1_jsonmode.addStretch(1)  # 添加伸缩项
        layout1_jsonmode.addWidget(self.SwitchButton_jsonmode)
        box1_jsonmode.setLayout(layout1_jsonmode)

        # -----创建第1.6个组(后来补的)，添加多个组件-----
        box1_conversion_toggle = QGroupBox()
        box1_conversion_toggle.setStyleSheet(
            """ QGroupBox {border: 1px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout1_conversion_toggle = QHBoxLayout()

        # 设置“简繁转换开关”标签
        labe1_6 = QLabel(flags=Qt.WindowFlags())
        labe1_6.setStyleSheet("font-family: 'Microsoft YaHei'; font-size: 17px")
        labe1_6.setText("简繁体自动转换")

        # 设置“简繁体自动转换”选择开关
        self.SwitchButton_conversion_toggle = SwitchButton(parent=self)

        layout1_conversion_toggle.addWidget(labe1_6)
        layout1_conversion_toggle.addStretch(1)  # 添加伸缩项
        layout1_conversion_toggle.addWidget(self.SwitchButton_conversion_toggle)
        box1_conversion_toggle.setLayout(layout1_conversion_toggle)

        # -----创建第1.6个组(后来补的)，添加多个组件-----
        box1_line_breaks = QGroupBox()
        box1_line_breaks.setStyleSheet(
            """ QGroupBox {border: 1px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout1_line_breaks = QHBoxLayout()

        # 设置“换行符保留”标签
        labe1_6 = QLabel(flags=Qt.WindowFlags())
        labe1_6.setStyleSheet("font-family: 'Microsoft YaHei'; font-size: 17px")
        labe1_6.setText("保留换行符")

        # 设置“换行符保留”选择开关
        self.SwitchButton_line_breaks = SwitchButton(parent=self)

        layout1_line_breaks.addWidget(labe1_6)
        layout1_line_breaks.addStretch(1)  # 添加伸缩项
        layout1_line_breaks.addWidget(self.SwitchButton_line_breaks)
        box1_line_breaks.setLayout(layout1_line_breaks)

        # -----创建第1.7个组(后来补的)，添加多个组件-----
        box1_thread_count = QGroupBox()
        box1_thread_count.setStyleSheet(
            """ QGroupBox {border: 1px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout1_thread_count = QHBoxLayout()

        # 设置“最大线程数”标签
        label1_7 = QLabel(parent=self, flags=Qt.WindowFlags())
        label1_7.setStyleSheet("font-family: 'Microsoft YaHei'; font-size: 17px")
        label1_7.setText("最大线程数")

        # 设置“说明”显示
        label2_7 = QLabel(parent=self, flags=Qt.WindowFlags())
        label2_7.setStyleSheet("font-family: 'Microsoft YaHei'; font-size: 11px")
        label2_7.setText("(0是自动根据电脑设置线程数)")

        # 设置“最大线程数”数值输入框
        self.spinBox_thread_count = SpinBox(self)
        # 设置最大最小值
        self.spinBox_thread_count.setRange(0, 1000)
        self.spinBox_thread_count.setValue(0)

        layout1_thread_count.addWidget(label1_7)
        layout1_thread_count.addWidget(label2_7)
        layout1_thread_count.addStretch(1)  # 添加伸缩项
        layout1_thread_count.addWidget(self.spinBox_thread_count)
        box1_thread_count.setLayout(layout1_thread_count)

        # 最外层的垂直布局
        container = QVBoxLayout()

        # 把内容添加到容器中
        container.addStretch(1)  # 添加伸缩项
        container.addWidget(box_Lines)
        container.addWidget(box1_line_breaks)
        container.addWidget(box1_jsonmode)
        container.addWidget(box1_conversion_toggle)
        container.addWidget(box1_thread_count)
        container.addStretch(1)  # 添加伸缩项

        # 设置窗口显示的内容是最外层容器
        self.setLayout(container)
        container.setSpacing(28)  # 设置布局内控件的间距为28
        container.setContentsMargins(
            20, 10, 20, 20
        )  # 设置布局的边距, 也就是外边框距离，分别为左、上、右、下

    # 设置“回复json格式”选择开关绑定函数
    def onjsonmode(self, isChecked: bool):
        if isChecked:
            Global.user_interface_prompter.createWarningInfoBar(
                "该设置现在仅支持openai接口的gpt-3.5-turbo-0125与gpt-4-turbo-preview模型开启"
            )
