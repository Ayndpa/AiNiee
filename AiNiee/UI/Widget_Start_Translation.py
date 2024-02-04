from PyQt5.QtWidgets import QFrame, QLabel, QStackedWidget, QVBoxLayout
from qfluentwidgets import SegmentedWidget

from .Widget_Start_Translation_A import Widget_Start_Translation_A
from .Widget_Start_Translation_B import Widget_Start_Translation_B


class Widget_Start_Translation(QFrame):  # 开始翻译主界面
    def __init__(self, text: str, parent=None):  # 构造函数，初始化实例时会自动调用
        super().__init__(parent=parent)  # 调用父类 QWidget 的构造函数
        self.setObjectName(
            text.replace(" ", "-")
        )  # 设置对象名，用于在 NavigationInterface 中的 addItem 方法中的 routeKey 参数中使用

        self.pivot = SegmentedWidget(
            self
        )  # 创建一个 SegmentedWidget 实例，分段式导航栏
        self.stackedWidget = QStackedWidget(
            self
        )  # 创建一个 QStackedWidget 实例，堆叠式窗口
        self.vBoxLayout = QVBoxLayout(self)  # 创建一个垂直布局管理器

        self.A_settings = Widget_Start_Translation_A(
            "A_settings", self
        )  # 创建实例，指向界面
        self.B_settings = Widget_Start_Translation_B(
            "B_settings", self
        )  # 创建实例，指向界面

        # 添加子界面到分段式导航栏
        self.addSubInterface(self.A_settings, "A_settings", "开始翻译")
        self.addSubInterface(self.B_settings, "B_settings", "备份功能")

        # 将分段式导航栏和堆叠式窗口添加到垂直布局中
        self.vBoxLayout.addWidget(self.pivot)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setContentsMargins(30, 50, 30, 30)  # 设置布局的外边距

        # 连接堆叠式窗口的 currentChanged 信号到槽函数 onCurrentIndexChanged
        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(
            self.A_settings
        )  # 设置默认显示的子界面为xxx界面
        self.pivot.setCurrentItem(
            self.A_settings.objectName()
        )  # 设置分段式导航栏的当前项为xxx界面

    def addSubInterface(self, widget: QLabel, objectName, text):
        """
        添加子界面到堆叠式窗口和分段式导航栏
        """
        widget.setObjectName(objectName)
        # widget.setAlignment(Qt.AlignCenter) # 设置 widget 对象的文本（如果是文本控件）在控件中的水平对齐方式
        self.stackedWidget.addWidget(widget)
        self.pivot.addItem(
            routeKey=objectName,
            text=text,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget),
        )

    def onCurrentIndexChanged(self, index):
        """
        槽函数：堆叠式窗口的 currentChanged 信号的槽函数
        """
        widget = self.stackedWidget.widget(index)
        self.pivot.setCurrentItem(widget.objectName())
