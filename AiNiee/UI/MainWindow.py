import os
from PyQt5.QtWidgets import QHBoxLayout, QStackedWidget, QApplication
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices, QIcon
from .CustomTitleBar import CustomTitleBar
from .AvatarWidget import AvatarWidget
from qframelesswindow import FramelessWindow
from qfluentwidgets import (
    setTheme,
    Theme,
    NavigationInterface,
    NavigationItemPosition,
    qrouter,
)
from qfluentwidgets.components import Dialog

from .Widget18 import Widget18
from .Widget21 import Widget21
from .Widget22 import Widget22
from .Widget23 import Widget23
from .Widget_Check import Widget_Check
from .Widget_Google import Widget_Google
from .Widget_Openai import Widget_Openai
from .Widget_Openai_Proxy import Widget_Openai_Proxy
from .Widget_RPG import Widget_RPG
from .Widget_SakuraLLM import Widget_SakuraLLM
from .Widget_Sponsor import Widget_Sponsor
from .Widget_Start_Translation import Widget_Start_Translation
from .Widget_Translation_Settings import Widget_Translation_Settings

from qfluentwidgets import FluentIcon as FIF

from ..Global import Global


class MainWindow(FramelessWindow):  # 主窗口

    def __init__(self):
        super().__init__()

        # 初始化程序图标，resource_dir的Icon.png
        icon = QIcon(os.path.join(Global.resource_dir, "Icon.png"))
        self.setWindowIcon(icon)

        # use dark theme mode
        setTheme(Theme.LIGHT)  # 设置主题

        self.hBoxLayout = QHBoxLayout(self)  # 设置布局为水平布局

        self.setTitleBar(CustomTitleBar(self))  # 设置标题栏，传入参数为自定义的标题栏
        self.stackWidget = QStackedWidget(self)  # 创建堆栈父2窗口
        self.navigationInterface = NavigationInterface(
            self, showMenuButton=True, showReturnButton=True
        )  # 创建父3导航栏

        # 创建子界面控件，传入参数为对象名和parent
        self.Widget_Openai = Widget_Openai("Widget_Openai", self)
        self.Widget_Openai_Proxy = Widget_Openai_Proxy("Widget_Openai_Proxy", self)
        self.Widget_Google = Widget_Google("Widget_Google", self)
        self.Widget_SakuraLLM = Widget_SakuraLLM("Widget_SakuraLLM", self)
        self.Widget_translation_settings = Widget_Translation_Settings(
            "Widget_translation_settings", self
        )
        self.Widget_start_translation = Widget_Start_Translation(
            "Widget_start_translation", self
        )
        self.Widget_RPG = Widget_RPG("Widget_RPG", self)
        self.Interface18 = Widget18("Interface18", self)
        self.Widget_check = Widget_Check("Widget_check", self)
        self.Interface21 = Widget21("Interface21", self)
        self.Interface22 = Widget22("Interface22", self)
        self.Interface23 = Widget23("Interface23", self)
        self.Widget_sponsor = Widget_Sponsor("Widget_sponsor", self)

        self.initLayout()  # 调用初始化布局函数

        self.initNavigation()  # 调用初始化导航栏函数

        self.initWindow()  # 调用初始化窗口函数

    # 初始化布局的函数
    def initLayout(self):
        self.hBoxLayout.setSpacing(0)  # 设置水平布局的间距
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)  # 设置水平布局的边距
        self.hBoxLayout.addWidget(self.navigationInterface)  # 将导航栏添加到布局中
        self.hBoxLayout.addWidget(self.stackWidget)  # 将堆栈窗口添加到布局中
        self.hBoxLayout.setStretchFactor(self.stackWidget, 1)  # 设置堆栈窗口的拉伸因子

        self.titleBar.raise_()  # 将标题栏置于顶层
        self.navigationInterface.displayModeChanged.connect(
            self.titleBar.raise_
        )  # 导航栏的显示模式改变时，将标题栏置于顶层

    # 初始化导航栏的函数
    def initNavigation(
        self,
    ):  # 详细介绍：https://pyqt-fluent-widgets.readthedocs.io/zh_CN/latest/navigation.html

        # 添加closeai官方账号界面
        self.addSubInterface(self.Widget_Openai, FIF.FEEDBACK, "Openai官方")
        # 添加closeai代理账号界面
        self.addSubInterface(self.Widget_Openai_Proxy, FIF.FEEDBACK, "Openai代理")
        # 添加谷歌官方账号界面
        self.addSubInterface(self.Widget_Google, FIF.FEEDBACK, "Google官方")
        # 添加sakura界面
        self.addSubInterface(self.Widget_SakuraLLM, FIF.FEEDBACK, "SakuraLLM")

        self.navigationInterface.addSeparator()  # 添加分隔符

        # 添加翻译设置相关页面
        self.addSubInterface(
            self.Widget_translation_settings, FIF.BOOK_SHELF, "翻译设置"
        )
        self.addSubInterface(self.Widget_start_translation, FIF.PLAY, "开始翻译")

        self.navigationInterface.addSeparator()  # 添加分隔符

        # 添加其他功能页面
        self.addSubInterface(self.Interface23, FIF.CALENDAR, "提示字典")
        self.addSubInterface(self.Interface21, FIF.CALENDAR, "替换字典")
        self.addSubInterface(self.Interface22, FIF.ZOOM, "AI提示词工程")
        self.addSubInterface(self.Interface18, FIF.ALBUM, "AI实时调教")

        self.navigationInterface.addSeparator()  # 添加分隔符,需要删除position=NavigationItemPosition.SCROLL来使分隔符正确显示

        # 添加RPG界面
        self.addSubInterface(self.Widget_RPG, FIF.CALENDAR, "RPG")

        self.navigationInterface.addSeparator()

        # 添加语义检查页面
        self.addSubInterface(self.Widget_check, FIF.HIGHTLIGHT, "错行检查")

        # 添加赞助页面
        self.addSubInterface(
            self.Widget_sponsor, FIF.CAFE, "赞助一下", NavigationItemPosition.BOTTOM
        )

        # 添加头像导航项
        self.navigationInterface.addWidget(
            routeKey="avatar",
            widget=AvatarWidget(),
            onClick=self.showMessageBox,
            position=NavigationItemPosition.BOTTOM,
        )

        # 设置程序默认打开的界面(不起作用)
        qrouter.setDefaultRouteKey(self.stackWidget, self.Widget_Openai.objectName())

        # set the maximum width
        # self.navigationInterface.setExpandWidth(300)

        self.stackWidget.currentChanged.connect(
            self.onCurrentInterfaceChanged
        )  # 堆栈窗口的当前窗口改变时，调用onCurrentInterfaceChanged函数
        self.stackWidget.setCurrentIndex(
            0
        )  # 设置堆栈窗口的当前窗口为0，数字对应的是添加界面时的顺序，也有设置默认打开界面的作用

    # 头像导航项的函数调用的函数
    def showMessageBox(self):
        url = QUrl("https://github.com/NEKOparapa/AiNiee-chatgpt")
        QDesktopServices.openUrl(url)

    # 初始化父窗口的函数
    def initWindow(self):
        self.resize(1200, 700)  # 设置窗口的大小
        # self.setWindowIcon(QIcon('resource/logo.png')) #设置窗口的图标
        self.setWindowTitle(Global.Software_Version)  # 设置窗口的标题
        self.titleBar.setAttribute(Qt.WA_StyledBackground)  # 设置标题栏的属性

        # 移动到屏幕中央
        desktop = QApplication.desktop().availableGeometry()  # 获取桌面的可用几何
        w, h = desktop.width(), desktop.height()  # 获取桌面的宽度和高度
        self.move(
            w // 2 - self.width() // 2, h // 2 - self.height() // 2
        )  # 将窗口移动到桌面的中心

        # 根据主题设置设置样式表的函数
        # color = 'dark' if isDarkTheme() else 'light' #如果是暗色主题，则color为dark，否则为light
        # with open(f'resource/{color}/demo.qss', encoding='utf-8') as f: #打开样式表
        # self.setStyleSheet(f.read()) #设置样式表

        dir1 = os.path.join(Global.resource_dir, "light")
        dir2 = os.path.join(dir1, "demo.qss")
        with open(dir2, encoding="utf-8") as f:  # 打开样式表
            self.setStyleSheet(f.read())  # 设置样式表

    # 切换到某个窗口的函数
    def switchTo(self, widget):
        self.stackWidget.setCurrentWidget(widget)  # 设置堆栈窗口的当前窗口为widget

    # 堆栈窗口的当前窗口改变时，调用的函数
    def onCurrentInterfaceChanged(self, index):
        widget = self.stackWidget.widget(index)  # 获取堆栈窗口的当前窗口
        self.navigationInterface.setCurrentItem(
            widget.objectName()
        )  # 设置导航栏的当前项为widget的对象名
        qrouter.push(
            self.stackWidget, widget.objectName()
        )  # 将堆栈窗口的当前窗口的对象名压入路由器

    # 重写鼠标按下事件
    def resizeEvent(self, e):
        self.titleBar.move(46, 0)  # 将标题栏移动到(46, 0)
        self.titleBar.resize(
            self.width() - 46, self.titleBar.height()
        )  # 设置标题栏的大小

    # 添加界面到导航栏布局函数
    def addSubInterface(
        self, interface, icon, text: str, position=NavigationItemPosition.TOP
    ):
        """add sub interface"""
        self.stackWidget.addWidget(interface)
        self.navigationInterface.addItem(
            routeKey=interface.objectName(),
            icon=icon,
            text=text,
            onClick=lambda: self.switchTo(interface),
            position=position,
            tooltip=text,
        )

    # 窗口关闭函数，放在最后面，解决界面空白与窗口退出后子线程还在运行的问题
    def closeEvent(self, event):
        title = "确定是否退出程序?"
        content = """如果正在进行翻译任务，当前任务会停止。"""
        w = Dialog(title, content, self)

        if w.exec():
            print("[INFO] 主窗口已经退出！")
            Global.Running_status = 10
            event.accept()
        else:
            event.ignore()
