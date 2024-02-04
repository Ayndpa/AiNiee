from PyQt5.QtWidgets import QFrame, QGroupBox, QHBoxLayout, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from qfluentwidgets import SpinBox, DoubleSpinBox


class Widget_Openai_Proxy_B(QFrame):  #  代理账号进阶设置子界面
    def __init__(self, text: str, parent=None):  # 解释器会自动调用这个函数
        super().__init__(parent=parent)  # 调用父类的构造函数
        self.setObjectName(
            text.replace(" ", "-")
        )  # 设置对象名，作用是在NavigationInterface中的addItem中的routeKey参数中使用
        # 设置各个控件-----------------------------------------------------------------------------------------

        # -----创建第1个组(后面加的)，添加多个组件-----
        box_RPM = QGroupBox()
        box_RPM.setStyleSheet(
            """ QGroupBox {border: 1px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout_RPM = QHBoxLayout()

        # 设置“RPM”标签
        self.labelY = QLabel(
            flags=Qt.WindowFlags()
        )  # parent参数表示父控件，如果没有父控件，可以将其设置为None；flags参数表示控件的标志，可以不传入
        self.labelY.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 17px;"
        )  # 设置字体，大小，颜色
        self.labelY.setText("每分钟请求数")

        # 设置“说明”显示
        self.labelA = QLabel(parent=self, flags=Qt.WindowFlags())
        self.labelA.setStyleSheet("font-family: 'Microsoft YaHei'; font-size: 11px")
        self.labelA.setText("(RPM)")

        # 数值输入
        self.spinBox_RPM = SpinBox(self)
        self.spinBox_RPM.setRange(0, 2147483647)
        self.spinBox_RPM.setValue(3500)

        layout_RPM.addWidget(self.labelY)
        layout_RPM.addWidget(self.labelA)
        layout_RPM.addStretch(1)  # 添加伸缩项
        layout_RPM.addWidget(self.spinBox_RPM)
        box_RPM.setLayout(layout_RPM)

        # -----创建第2个组（后面加的），添加多个组件-----
        box_TPM = QGroupBox()
        box_TPM.setStyleSheet(
            """ QGroupBox {border: 1px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout_TPM = QHBoxLayout()

        # 设置“TPM”标签
        self.labelB = QLabel(
            flags=Qt.WindowFlags()
        )  # parent参数表示父控件，如果没有父控件，可以将其设置为None；flags参数表示控件的标志，可以不传入
        self.labelB.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 17px;"
        )  # 设置字体，大小，颜色
        self.labelB.setText("每分钟tokens数")

        # 设置“说明”显示
        self.labelC = QLabel(parent=self, flags=Qt.WindowFlags())
        self.labelC.setStyleSheet("font-family: 'Microsoft YaHei'; font-size: 11px")
        self.labelC.setText("(TPM)")

        # 数值输入
        self.spinBox_TPM = SpinBox(self)
        self.spinBox_TPM.setRange(0, 2147483647)
        self.spinBox_TPM.setValue(60000)

        layout_TPM.addWidget(self.labelB)
        layout_TPM.addWidget(self.labelC)
        layout_TPM.addStretch(1)  # 添加伸缩项
        layout_TPM.addWidget(self.spinBox_TPM)
        box_TPM.setLayout(layout_TPM)

        # -----创建第3个组（后面加的），添加多个组件-----
        box_input_pricing = QGroupBox()
        box_input_pricing.setStyleSheet(
            """ QGroupBox {border: 1px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout_input_pricing = QHBoxLayout()

        # 设置“请求输入价格”标签
        self.labelD = QLabel(
            flags=Qt.WindowFlags()
        )  # parent参数表示父控件，如果没有父控件，可以将其设置为None；flags参数表示控件的标志，可以不传入
        self.labelD.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 17px;"
        )  # 设置字体，大小，颜色
        self.labelD.setText("请求输入价格")

        # 设置“说明”显示
        self.labelE = QLabel(parent=self, flags=Qt.WindowFlags())
        self.labelE.setStyleSheet("font-family: 'Microsoft YaHei'; font-size: 11px")
        self.labelE.setText("( /1K tokens)")

        # 数值输入
        self.spinBox_input_pricing = DoubleSpinBox(self)
        self.spinBox_input_pricing.setRange(0.0000, 2147483647)
        self.spinBox_input_pricing.setDecimals(4)  # 设置小数点后的位数
        self.spinBox_input_pricing.setValue(0.0015)

        layout_input_pricing.addWidget(self.labelD)
        layout_input_pricing.addWidget(self.labelE)
        layout_input_pricing.addStretch(1)  # 添加伸缩项
        layout_input_pricing.addWidget(self.spinBox_input_pricing)
        box_input_pricing.setLayout(layout_input_pricing)

        # -----创建第4个组（后面加的），添加多个组件-----
        box_output_pricing = QGroupBox()
        box_output_pricing.setStyleSheet(
            """ QGroupBox {border: 1px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout_output_pricing = QHBoxLayout()

        # 设置“TPM”标签
        self.labelF = QLabel(
            flags=Qt.WindowFlags()
        )  # parent参数表示父控件，如果没有父控件，可以将其设置为None；flags参数表示控件的标志，可以不传入
        self.labelF.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 17px;"
        )  # 设置字体，大小，颜色
        self.labelF.setText("回复输出价格")

        # 设置“说明”显示
        self.labelG = QLabel(parent=self, flags=Qt.WindowFlags())
        self.labelG.setStyleSheet("font-family: 'Microsoft YaHei'; font-size: 11px")
        self.labelG.setText("( /1K tokens)")

        # 数值输入
        self.spinBox_output_pricing = DoubleSpinBox(self)
        self.spinBox_output_pricing.setRange(0.0000, 2147483647)
        self.spinBox_output_pricing.setDecimals(4)  # 设置小数点后的位数
        self.spinBox_output_pricing.setValue(0.002)

        layout_output_pricing.addWidget(self.labelF)
        layout_output_pricing.addWidget(self.labelG)
        layout_output_pricing.addStretch(1)  # 添加伸缩项
        layout_output_pricing.addWidget(self.spinBox_output_pricing)
        box_output_pricing.setLayout(layout_output_pricing)

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
        container.addWidget(box_RPM)
        container.addWidget(box_TPM)
        container.addWidget(box_input_pricing)
        container.addWidget(box_output_pricing)
        container.addStretch(1)  # 添加伸缩项
