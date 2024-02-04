from PyQt5.QtWidgets import QFrame, QGroupBox, QHBoxLayout, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from qfluentwidgets import ProgressRing, PrimaryPushButton, FluentIcon as FIF

from ..Global import Global


class Widget_Start_Translation_A(QFrame):  #  开始翻译子界面
    def __init__(self, text: str, parent=None):  # 解释器会自动调用这个函数
        super().__init__(parent=parent)  # 调用父类的构造函数
        self.setObjectName(
            text.replace(" ", "-")
        )  # 设置对象名，作用是在NavigationInterface中的addItem中的routeKey参数中使用
        # 设置各个控件-----------------------------------------------------------------------------------------

        # -----创建第1个组，添加多个组件-----
        box_project = QGroupBox()
        box_project.setStyleSheet(
            """ QGroupBox {border: 1px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout_project = QHBoxLayout()

        # 第一组水平布局
        layout_horizontal_1 = QHBoxLayout()

        self.label111 = QLabel(flags=Qt.WindowFlags())
        self.label111.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 17px; "
        )  # 设置字体，大小，颜色
        self.label111.setText("项目类型 :")

        self.translation_project = QLabel(flags=Qt.WindowFlags())
        self.translation_project.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 17px; "
        )  # 设置字体，大小，颜色
        self.translation_project.setText("无")

        layout_horizontal_1.addWidget(self.label111)
        layout_horizontal_1.addStretch(1)  # 添加伸缩项
        layout_horizontal_1.addWidget(self.translation_project)
        layout_horizontal_1.addStretch(1)  # 添加伸缩项

        # 第二组水平布局
        layout_horizontal_2 = QHBoxLayout()

        self.label222 = QLabel(flags=Qt.WindowFlags())
        self.label222.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 17px; "
        )  # 设置字体，大小，颜色
        self.label222.setText("项目ID :")

        self.project_id = QLabel(flags=Qt.WindowFlags())
        self.project_id.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 17px; "
        )  # 设置字体，大小，颜色
        self.project_id.setText("无")

        layout_horizontal_2.addWidget(self.label222)
        layout_horizontal_2.addStretch(1)  # 添加伸缩项
        layout_horizontal_2.addWidget(self.project_id)
        layout_horizontal_2.addStretch(1)  # 添加伸缩项

        # 将两个水平布局放入最外层水平布局
        layout_project.addLayout(layout_horizontal_1)
        layout_project.addLayout(layout_horizontal_2)

        box_project.setLayout(layout_project)

        # -----创建第2个组，添加多个组件-----
        box_text_line_count = QGroupBox()
        box_text_line_count.setStyleSheet(
            """ QGroupBox {border: 1px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout_text_line_count = QHBoxLayout()

        # 第三组水平布局
        layout_horizontal_3 = QHBoxLayout()

        self.label333 = QLabel(flags=Qt.WindowFlags())
        self.label333.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 17px; "
        )  # 设置字体，大小，颜色
        self.label333.setText("总文本行数 :")

        self.total_text_line_count = QLabel(flags=Qt.WindowFlags())
        self.total_text_line_count.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 17px; "
        )  # 设置字体，大小，颜色
        self.total_text_line_count.setText("无")

        layout_horizontal_3.addWidget(self.label333)
        layout_horizontal_3.addStretch(1)  # 添加伸缩项
        layout_horizontal_3.addWidget(self.total_text_line_count)
        layout_horizontal_3.addStretch(1)  # 添加伸缩项

        # 第四组水平布局
        layout_horizontal_4 = QHBoxLayout()

        self.label444 = QLabel(flags=Qt.WindowFlags())
        self.label444.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 17px; "
        )  # 设置字体，大小，颜色
        self.label444.setText("已翻译行数 :")

        self.translated_line_count = QLabel(flags=Qt.WindowFlags())
        self.translated_line_count.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 17px; "
        )  # 设置字体，大小，颜色
        self.translated_line_count.setText("无")

        layout_horizontal_4.addWidget(self.label444)
        layout_horizontal_4.addStretch(1)  # 添加伸缩项
        layout_horizontal_4.addWidget(self.translated_line_count)
        layout_horizontal_4.addStretch(1)  # 添加伸缩项

        # 将第三组和第四组水平布局放入最外层水平布局
        layout_text_line_count.addLayout(layout_horizontal_3)
        layout_text_line_count.addLayout(layout_horizontal_4)

        box_text_line_count.setLayout(layout_text_line_count)

        # -----创建第3个组，添加多个组件-----
        box_spent = QGroupBox()
        box_spent.setStyleSheet(
            """ QGroupBox {border: 1px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout_spent = QHBoxLayout()

        # 第五组水平布局
        layout_horizontal_5 = QHBoxLayout()

        self.labelx1 = QLabel(flags=Qt.WindowFlags())
        self.labelx1.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 17px; "
        )  # 设置字体，大小，颜色
        self.labelx1.setText("已花费tokens :")

        self.tokens_spent = QLabel(flags=Qt.WindowFlags())
        self.tokens_spent.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 17px; "
        )  # 设置字体，大小，颜色
        self.tokens_spent.setText("无")

        layout_horizontal_5.addWidget(self.labelx1)
        layout_horizontal_5.addStretch(1)  # 添加伸缩项
        layout_horizontal_5.addWidget(self.tokens_spent)
        layout_horizontal_5.addStretch(1)  # 添加伸缩项

        # 第六组水平布局
        layout_horizontal_6 = QHBoxLayout()

        self.labelx2 = QLabel(flags=Qt.WindowFlags())
        self.labelx2.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 17px; "
        )  # 设置字体，大小，颜色
        self.labelx2.setText("已花费金额(＄) :")

        self.amount_spent = QLabel(flags=Qt.WindowFlags())
        self.amount_spent.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 17px; "
        )  # 设置字体，大小，颜色
        self.amount_spent.setText("无")

        layout_horizontal_6.addWidget(self.labelx2)
        layout_horizontal_6.addStretch(1)  # 添加伸缩项
        layout_horizontal_6.addWidget(self.amount_spent)
        layout_horizontal_6.addStretch(1)  # 添加伸缩项

        # 将第五组和第六组水平布局放入最外层水平布局
        layout_spent.addLayout(layout_horizontal_5)
        layout_spent.addLayout(layout_horizontal_6)

        box_spent.setLayout(layout_spent)

        # -----创建第4个组，添加多个组件-----
        box_progressRing = QGroupBox()
        box_progressRing.setStyleSheet(
            """ QGroupBox {border: 1px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout_progressRing = QHBoxLayout()

        # 设置“翻译进度”标签
        self.label_progressRing = QLabel(flags=Qt.WindowFlags())
        self.label_progressRing.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 17px; "
        )  # 设置字体，大小，颜色
        self.label_progressRing.setText("翻译进度")

        # 设置翻译进度条
        self.progressRing = ProgressRing(self)
        self.progressRing.setValue(0)
        self.progressRing.setTextVisible(True)
        self.progressRing.setFixedSize(80, 80)

        layout_progressRing.addWidget(self.label_progressRing)
        layout_progressRing.addStretch(1)  # 添加伸缩项
        layout_progressRing.addWidget(self.progressRing)
        box_progressRing.setLayout(layout_progressRing)

        # -----创建第5个组，添加多个组件-----
        box_start_translation = QGroupBox()
        box_start_translation.setStyleSheet(
            """ QGroupBox {border: 0px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout_start_translation = QHBoxLayout()

        # 设置“开始翻译”的按钮
        self.primaryButton_start_translation = PrimaryPushButton(
            "开始翻译", self, FIF.UPDATE
        )
        self.primaryButton_start_translation.clicked.connect(
            self.Start_translation_mtool
        )  # 按钮绑定槽函数

        layout_start_translation.addStretch(1)  # 添加伸缩项
        layout_start_translation.addWidget(self.primaryButton_start_translation)
        layout_start_translation.addStretch(1)  # 添加伸缩项
        box_start_translation.setLayout(layout_start_translation)

        # 最外层的垂直布局
        container = QVBoxLayout()

        # 把内容添加到容器中
        container.addStretch(1)  # 添加伸缩项
        container.addWidget(box_project)
        container.addWidget(box_text_line_count)
        container.addWidget(box_spent)
        container.addWidget(box_progressRing)
        container.addWidget(box_start_translation)
        container.addStretch(1)  # 添加伸缩项

        # 设置窗口显示的内容是最外层容器
        self.setLayout(container)
        container.setSpacing(28)  # 设置布局内控件的间距为28
        container.setContentsMargins(
            20, 10, 20, 20
        )  # 设置布局的边距, 也就是外边框距离，分别为左、上、右、下

    # 开始翻译按钮绑定函数
    def Start_translation_mtool(self):
        if Global.Running_status == 0:
            # 创建子线程
            thread = Global.background_executor("执行翻译任务")
            thread.start()

        elif Global.Running_status != 0:
            Global.user_interface_prompter.createWarningInfoBar(
                "正在进行任务中，请等待任务结束后再操作~"
            )
