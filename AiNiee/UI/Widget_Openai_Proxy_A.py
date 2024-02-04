from PyQt5.QtWidgets import (
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QGridLayout,
    QVBoxLayout,
    QWidget,
    QInputDialog,
)
from PyQt5.QtCore import Qt
from qfluentwidgets import (
    ComboBox,
    TextEdit,
    LineEdit,
    PushButton,
    PrimaryPushButton,
    FluentIcon as FIF,
)

from ..Basic_Logic.Background_Executor import Background_Executor

from ..Global import Global


class Widget_Openai_Proxy_A(QFrame):  #  代理账号基础设置子界面
    # 保存默认下拉框选项数量的变量，应与下拉框选项数量一致
    default_model_count = None

    # 下拉框选择事件
    def model_select(self):
        if self.comboBox_model.currentText() == "自定义":
            # 弹出一个新的qfluentwidgets输入框，输入自定义模型名称
            widget = QWidget()
            # 创建一个 QInputDialog 对话框
            dialog = QInputDialog(widget)
            # 设置对话框的标题和标签
            dialog.setWindowTitle('输入模型名称')
            dialog.setLabelText('请输入模型名称:')
            # 设置对话框的输入模式
            dialog.setInputMode(QInputDialog.TextInput)
            dialog.setTextValue('')
            # 获取当前的窗口标志
            flags = dialog.windowFlags()
            # 去除 "?" 按钮
            dialog.setWindowFlags(flags & ~Qt.WindowContextHelpButtonHint)

            ok = dialog.exec_()
            text = dialog.textValue() if ok else None

            # 如果点击了确定按钮，则设置下拉框文本为输入的文本
            if ok:
                # 如果下拉框数量大于默认数量，则覆盖最后一个选项，否则添加新选项
                if self.comboBox_model.count() > self.default_model_count:
                    self.comboBox_model.setItemText(self.comboBox_model.count() - 1, text)
                else:
                    self.comboBox_model.addItem(text)
                # 设置选择序列为最后一个
                self.comboBox_model.setCurrentIndex(self.comboBox_model.count() - 1)
            # 否则设置选择序列为0
            else:
                self.comboBox_model.setCurrentIndex(0)

    def __init__(self, text: str, parent=None):  # 解释器会自动调用这个函数
        super().__init__(parent=parent)  # 调用父类的构造函数
        self.setObjectName(
            text.replace(" ", "-")
        )  # 设置对象名，作用是在NavigationInterface中的addItem中的routeKey参数中使用
        # 设置各个控件-----------------------------------------------------------------------------------------

        # -----创建第1个组，添加多个组件-----
        box_relay_address = QGroupBox()
        box_relay_address.setStyleSheet(
            """ QGroupBox {border: 1px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout_relay_address = QHBoxLayout()

        # 设置“中转地址”标签
        self.labelA = QLabel(
            flags=Qt.WindowFlags()
        )  # parent参数表示父控件，如果没有父控件，可以将其设置为None；flags参数表示控件的标志，可以不传入
        self.labelA.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 17px;"
        )  # 设置字体，大小，颜色
        self.labelA.setText("中转请求地址")

        # 设置微调距离用的空白标签
        self.labelB = QLabel()
        self.labelB.setText("                ")

        # 设置“中转地址”的输入框
        self.LineEdit_relay_address = LineEdit()
        # LineEdit1.setFixedSize(300, 30)

        layout_relay_address.addWidget(self.labelA)
        layout_relay_address.addWidget(self.labelB)
        layout_relay_address.addWidget(self.LineEdit_relay_address)
        box_relay_address.setLayout(layout_relay_address)

        # -----创建第2个组，添加多个组件-----
        box_model = QGroupBox()
        box_model.setStyleSheet(
            """ QGroupBox {border: 1px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout_model = QGridLayout()

        # 设置“模型选择”标签
        self.labelx = QLabel(
            flags=Qt.WindowFlags()
        )  # parent参数表示父控件，如果没有父控件，可以将其设置为None；flags参数表示控件的标志，可以不传入
        self.labelx.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 17px;"
        )  # 设置字体，大小，颜色
        self.labelx.setText("模型选择")

        # 设置“模型类型”下拉选择框
        self.comboBox_model = ComboBox()  # 以demo为父类
        self.comboBox_model.addItems(
            [
                "gpt-3.5-turbo",
                "gpt-3.5-turbo-0301",
                "gpt-3.5-turbo-0613",
                "gpt-3.5-turbo-1106",
                "gpt-3.5-turbo-0125",
                "gpt-3.5-turbo-16k",
                "gpt-3.5-turbo-16k-0613",
                "gpt-4",
                "gpt-4-0314",
                "gpt-4-0613",
                "gpt-4-turbo-preview",
                "gpt-4-1106-preview",
                "gpt-4-0125-preview",
                "自定义"
            ]
        )
        # 保存下拉框数量
        self.default_model_count = self.comboBox_model.count()
        # 下拉框选择事件，绑定到新函数
        self.comboBox_model.currentIndexChanged.connect(self.model_select)
        self.comboBox_model.setCurrentIndex(
            0
        )  # 设置下拉框控件（ComboBox）的当前选中项的索引为0，也就是默认选中第一个选项
        self.comboBox_model.setFixedSize(200, 35)
        # 设置下拉选择框默认选择
        self.comboBox_model.setCurrentText("gpt-3.5-turbo-0613")

        layout_model.addWidget(self.labelx, 0, 0)
        layout_model.addWidget(self.comboBox_model, 0, 1)
        box_model.setLayout(layout_model)

        # -----创建第3个组，添加多个组件-----
        box_apikey = QGroupBox()
        box_apikey.setStyleSheet(
            """ QGroupBox {border: 1px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout_apikey = QHBoxLayout()

        # 设置“API KEY”标签
        self.labelx = QLabel(flags=Qt.WindowFlags())
        self.labelx.setStyleSheet("font-family: 'Microsoft YaHei'; font-size: 17px;")
        self.labelx.setText("API KEY")

        # 设置微调距离用的空白标签
        self.labely = QLabel()
        self.labely.setText("                       ")

        # 设置“API KEY”的输入框
        self.TextEdit_apikey = TextEdit()

        # 追加到容器中
        layout_apikey.addWidget(self.labelx)
        layout_apikey.addWidget(self.labely)
        layout_apikey.addWidget(self.TextEdit_apikey)
        # 添加到 box中
        box_apikey.setLayout(layout_apikey)

        # -----创建第4个组，添加多个组件-----
        box_proxy_port = QGroupBox()
        box_proxy_port.setStyleSheet(
            """ QGroupBox {border: 1px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout_proxy_port = QHBoxLayout()

        # 设置“系统代理端口”标签
        self.label_proxy_port = QLabel(
            flags=Qt.WindowFlags()
        )  # parent参数表示父控件，如果没有父控件，可以将其设置为None；flags参数表示控件的标志，可以不传入
        self.label_proxy_port.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 17px;"
        )  # 设置字体，大小，颜色
        self.label_proxy_port.setText("系统代理")

        # 设置微调距离用的空白标签
        self.labelx = QLabel()
        self.labelx.setText("                      ")

        # 设置“系统代理端口”的输入框
        self.LineEdit_proxy_port = LineEdit()
        # LineEdit1.setFixedSize(300, 30)

        layout_proxy_port.addWidget(self.label_proxy_port)
        layout_proxy_port.addWidget(self.labelx)
        layout_proxy_port.addWidget(self.LineEdit_proxy_port)
        box_proxy_port.setLayout(layout_proxy_port)

        # -----创建第5个组，添加多个组件-----
        box_test = QGroupBox()
        box_test.setStyleSheet(
            """ QGroupBox {border: 0px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout_test = QHBoxLayout()

        # 设置“测试请求”的按钮
        primaryButton_test = PrimaryPushButton("测试请求", self, FIF.SEND)
        primaryButton_test.clicked.connect(self.test_request)  # 按钮绑定槽函数

        # 设置“保存配置”的按钮
        primaryButton_save = PushButton("保存配置", self, FIF.SAVE)
        primaryButton_save.clicked.connect(self.saveconfig)  # 按钮绑定槽函数

        layout_test.addStretch(1)  # 添加伸缩项
        layout_test.addWidget(primaryButton_save)
        layout_test.addStretch(1)  # 添加伸缩项
        layout_test.addWidget(primaryButton_test)
        layout_test.addStretch(1)  # 添加伸缩项
        box_test.setLayout(layout_test)

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
        container.addWidget(box_relay_address)
        container.addWidget(box_model)
        container.addWidget(box_apikey)
        container.addWidget(box_proxy_port)
        container.addWidget(box_test)
        container.addStretch(1)  # 添加伸缩项

    def saveconfig(self):
        Global.configurator.read_write_config("write")
        Global.user_interface_prompter.createSuccessInfoBar("已成功保存配置")

    def test_request(self):
        if Global.Running_status == 0:
            # 创建子线程
            thread = Background_Executor("openai代理接口测试")
            thread.start()

        elif Global.Running_status != 0:
            Global.user_interface_prompter.createWarningInfoBar(
                "正在进行任务中，请等待任务结束后再操作~"
            )
