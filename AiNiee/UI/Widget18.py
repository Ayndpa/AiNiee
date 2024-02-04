from PyQt5.QtWidgets import QFrame, QVBoxLayout, QGroupBox, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices
from qfluentwidgets import CheckBox, HyperlinkButton, Slider, PushButton

from ..Global import Global


class Widget18(QFrame):  # AI实时调教界面
    def __init__(self, text: str, parent=None):  # 解释器会自动调用这个函数
        super().__init__(parent=parent)  # 调用父类的构造函数
        self.setObjectName(
            text.replace(" ", "-")
        )  # 设置对象名，作用是在NavigationInterface中的addItem中的routeKey参数中使用

        # 最外层的垂直布局
        container = QVBoxLayout()

        # -----创建第1个组，添加多个组件-----
        box1 = QGroupBox()
        box1.setStyleSheet(
            """ QGroupBox {border: 1px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout1 = QHBoxLayout()

        # 设置“启用实时参数”标签
        label0 = QLabel(flags=Qt.WindowFlags())
        label0.setStyleSheet("font-family: 'Microsoft YaHei'; font-size: 17px")
        label0.setText("启用调教功能（OpenAI）")

        # 设置官方文档说明链接按钮
        hyperlinkButton = HyperlinkButton(
            url="https://platform.openai.com/docs/api-reference/chat/create",
            text="(官方文档)",
        )

        # 设置“启用实时参数”开关
        self.checkBox = CheckBox("实时设置AI参数", self)
        self.checkBox.stateChanged.connect(self.checkBoxChanged)

        layout1.addWidget(label0)
        layout1.addWidget(hyperlinkButton)
        layout1.addStretch(1)  # 添加伸缩项
        layout1.addWidget(self.checkBox)
        box1.setLayout(layout1)

        # -----创建第2个组，添加多个组件-----
        box2 = QGroupBox()
        box2.setStyleSheet(
            """ QGroupBox {border: 1px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout2 = QHBoxLayout()

        # 设置“官方文档”标签
        label01 = QLabel(parent=self, flags=Qt.WindowFlags())
        label01.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 17px;  color: black"
        )
        label01.setText("官方文档说明")

        # 设置官方文档说明链接按钮
        pushButton1 = PushButton("文档链接", self)
        pushButton1.clicked.connect(
            lambda: QDesktopServices.openUrl(
                QUrl("https://platform.openai.com/docs/api-reference/chat/create")
            )
        )

        layout2.addWidget(label01)
        layout2.addStretch(1)  # 添加伸缩项
        layout2.addWidget(pushButton1)
        box2.setLayout(layout2)

        # -----创建第3个组，添加多个组件-----
        box3 = QGroupBox()
        box3.setStyleSheet(
            """ QGroupBox {border: 1px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout3 = QHBoxLayout()

        # 设置“温度”标签
        label1 = QLabel(parent=self, flags=Qt.WindowFlags())
        label1.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 17px;  color: black"
        )
        label1.setText("温度")

        # 设置“温度”副标签
        label11 = QLabel(parent=self, flags=Qt.WindowFlags())
        label11.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 10px;  color: black"
        )
        label11.setText("(官方默认值为1)")

        # 设置“温度”滑动条
        self.slider1 = Slider(Qt.Horizontal, self)
        self.slider1.setFixedWidth(200)

        # 创建一个QLabel控件，并设置初始文本为滑动条的初始值,并实时更新
        self.label2 = QLabel(str(self.slider1.value()), self)
        self.label2.setFixedSize(100, 15)  # 设置标签框的大小，不然会显示不全
        self.label2.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 12px;  color: black"
        )
        self.slider1.valueChanged.connect(
            lambda value: self.label2.setText(str("{:.1f}".format(value * 0.1)))
        )

        # 设置滑动条的最小值、最大值、当前值，放到后面是为了让上面的label2显示正确的值
        self.slider1.setMinimum(0)
        self.slider1.setMaximum(20)
        self.slider1.setValue(0)

        layout3.addWidget(label1)
        layout3.addWidget(label11)
        layout3.addStretch(1)  # 添加伸缩项
        layout3.addWidget(self.slider1)
        layout3.addWidget(self.label2)
        box3.setLayout(layout3)

        # -----创建第4个组，添加多个组件-----
        box4 = QGroupBox()
        box4.setStyleSheet(
            """ QGroupBox {border: 0px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout4 = QHBoxLayout()

        # 设置“温度”说明文档
        label3 = QLabel(parent=self, flags=Qt.WindowFlags())
        label3.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 14px;  color: black"
        )
        label3.setText(
            "Temperature：控制结果的随机性。如果希望结果更有创意可以尝试 0.9，或者希望有固定结果可以尝试0.0\n官方建议不要与Top_p一同改变 "
        )

        layout4.addWidget(label3)
        box4.setLayout(layout4)

        # -----创建第5个组，添加多个组件-----
        box5 = QGroupBox()
        box5.setStyleSheet(
            """ QGroupBox {border: 1px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout5 = QHBoxLayout()

        # 设置“top_p”标签
        label4 = QLabel(parent=self, flags=Qt.WindowFlags())
        label4.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 17px;  color: black"
        )
        label4.setText("概率阈值")

        # 设置“top_p”副标签
        label41 = QLabel(parent=self, flags=Qt.WindowFlags())
        label41.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 10px;  color: black"
        )
        label41.setText("(官方默认值为1)")

        # 设置“top_p”滑动条
        self.slider2 = Slider(Qt.Horizontal, self)
        self.slider2.setFixedWidth(200)

        # 创建一个QLabel控件，并设置初始文本为滑动条的初始值,并实时更新
        self.label5 = QLabel(str(self.slider2.value()), self)
        self.label5.setFixedSize(100, 15)  # 设置标签框的大小，不然会显示不全
        self.label5.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 12px;  color: black"
        )
        self.slider2.valueChanged.connect(
            lambda value: self.label5.setText(str("{:.1f}".format(value * 0.1)))
        )

        # 设置滑动条的最小值、最大值、当前值，放在后面是为了让上面的label5显示正确的值和格式
        self.slider2.setMinimum(0)
        self.slider2.setMaximum(10)
        self.slider2.setValue(10)

        layout5.addWidget(label4)
        layout5.addWidget(label41)
        layout5.addStretch(1)  # 添加伸缩项
        layout5.addWidget(self.slider2)
        layout5.addWidget(self.label5)
        box5.setLayout(layout5)

        # -----创建第6个组，添加多个组件-----
        box6 = QGroupBox()
        box6.setStyleSheet(
            """ QGroupBox {border: 0px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout6 = QHBoxLayout()

        # 设置“top_p”说明文档
        label6 = QLabel(parent=self, flags=Qt.WindowFlags())
        label6.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 14px;  color: black"
        )
        label6.setText(
            "Top_p：用于控制生成文本的多样性，与Temperature的作用相同。如果希望结果更加多样可以尝试 0.9\n或者希望有固定结果可以尝试 0.0。官方建议不要与Temperature一同改变 "
        )

        layout6.addWidget(label6)
        box6.setLayout(layout6)

        # -----创建第7个组，添加多个组件-----
        box7 = QGroupBox()
        box7.setStyleSheet(
            """ QGroupBox {border: 1px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout7 = QHBoxLayout()

        # 设置“presence_penalty”标签
        label7 = QLabel(parent=self, flags=Qt.WindowFlags())
        label7.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 17px;  color: black"
        )
        label7.setText("主题惩罚")

        # 设置“presence_penalty”副标签
        label71 = QLabel(parent=self, flags=Qt.WindowFlags())
        label71.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 10px;  color: black"
        )
        label71.setText("(官方默认值为0)")

        # 设置“presence_penalty”滑动条
        self.slider3 = Slider(Qt.Horizontal, self)
        self.slider3.setFixedWidth(200)

        # 创建一个QLabel控件，并设置初始文本为滑动条的初始值,并实时更新
        self.label8 = QLabel(str(self.slider3.value()), self)
        self.label8.setFixedSize(100, 15)  # 设置标签框的大小，不然会显示不全
        self.label8.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 12px;  color: black"
        )
        self.slider3.valueChanged.connect(
            lambda value: self.label8.setText(str("{:.1f}".format(value * 0.1)))
        )

        # 设置滑动条的最小值、最大值、当前值，放到后面是为了让上面的label8显示正确的值和格式
        self.slider3.setMinimum(-20)
        self.slider3.setMaximum(20)
        self.slider3.setValue(5)

        layout7.addWidget(label7)
        layout7.addWidget(label71)
        layout7.addStretch(1)  # 添加伸缩项
        layout7.addWidget(self.slider3)
        layout7.addWidget(self.label8)
        box7.setLayout(layout7)

        # -----创建第8个组，添加多个组件-----
        box8 = QGroupBox()
        box8.setStyleSheet(
            """ QGroupBox {border: 0px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout8 = QHBoxLayout()

        # 设置“presence_penalty”说明文档
        label82 = QLabel(parent=self, flags=Qt.WindowFlags())
        label82.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 14px;  color: black"
        )
        label82.setText(
            "Presence_penalty：用于控制主题的重复度。AI生成新内容时，会根据到目前为止已经出现在文本中的语句  \n负值是增加生成的新内容，正值是减少生成的新内容，从而改变AI模型谈论新主题内容的可能性"
        )

        layout8.addWidget(label82)
        box8.setLayout(layout8)

        # -----创建第9个组，添加多个组件-----
        box9 = QGroupBox()
        box9.setStyleSheet(
            """ QGroupBox {border: 1px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout9 = QHBoxLayout()

        # 设置“frequency_penalty”标签
        label9 = QLabel(parent=self, flags=Qt.WindowFlags())
        label9.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 17px;  color: black"
        )
        label9.setText("频率惩罚")

        # 设置“presence_penalty”副标签
        label91 = QLabel(parent=self, flags=Qt.WindowFlags())
        label91.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 10px;  color: black"
        )
        label91.setText("(官方默认值为0)")

        # 设置“frequency_penalty”滑动条
        self.slider4 = Slider(Qt.Horizontal, self)
        self.slider4.setFixedWidth(200)

        # 创建一个QLabel控件，并设置初始文本为滑动条的初始值,并实时更新
        self.label10 = QLabel(str(self.slider4.value()), self)
        self.label10.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 12px;  color: black"
        )
        self.label10.setFixedSize(100, 15)  # 设置标签框的大小，不然会显示不全
        self.slider4.valueChanged.connect(
            lambda value: self.label10.setText(str("{:.1f}".format(value * 0.1)))
        )

        # 设置滑动条的最小值、最大值、当前值，放到后面是为了让上面的label10显示正确的值和格式
        self.slider4.setMinimum(-20)
        self.slider4.setMaximum(20)
        self.slider4.setValue(0)

        layout9.addWidget(label9)
        layout9.addWidget(label91)
        layout9.addStretch(1)  # 添加伸缩项
        layout9.addWidget(self.slider4)
        layout9.addWidget(self.label10)
        box9.setLayout(layout9)

        # -----创建第10个组，添加多个组件-----
        box10 = QGroupBox()
        box10.setStyleSheet(
            """ QGroupBox {border: 0px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout10 = QHBoxLayout()

        # 设置“frequency_penalty”说明文档
        label11 = QLabel(parent=self, flags=Qt.WindowFlags())
        label11.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 14px;  color: black"
        )
        label11.setText(
            "Frequency_penalty：用于控制词语的频率。AI在生成新词时，会根据该词在文本中的现有频率 \n负值进行奖励，增加出现频率；正值进行惩罚，降低出现频率；以便增加或降低逐字重复同一行的可能性"
        )

        layout10.addWidget(label11)
        box10.setLayout(layout10)

        # 把内容添加到容器中
        container.addStretch(1)  # 添加伸缩项
        container.addWidget(box1)
        # container.addWidget(box2)
        container.addWidget(box3)
        container.addWidget(box4)
        container.addWidget(box5)
        container.addWidget(box6)
        container.addWidget(box7)
        container.addWidget(box8)
        container.addWidget(box9)
        container.addWidget(box10)
        container.addStretch(1)  # 添加伸缩项

        # 设置窗口显示的内容是最外层容器
        self.setLayout(container)
        container.setSpacing(20)  # 设置布局内控件的间距为28
        container.setContentsMargins(
            50, 70, 50, 30
        )  # 设置布局的边距, 也就是外边框距离，分别为左、上、右、下

    # 勾选事件
    def checkBoxChanged(self, isChecked: bool):
        if isChecked:
            Global.user_interface_prompter.createSuccessInfoBar("已启用实时调教功能")
