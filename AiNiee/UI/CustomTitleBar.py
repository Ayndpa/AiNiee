from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from qframelesswindow import TitleBar


class CustomTitleBar(TitleBar):  # 标题栏
    """Title bar with icon and title"""

    def __init__(self, parent):
        super().__init__(parent)
        # add window icon
        self.iconLabel = QLabel(self)  # 创建标签
        self.iconLabel.setFixedSize(18, 18)  # 设置标签大小
        self.hBoxLayout.insertSpacing(0, 10)  # 设置布局的间距
        self.hBoxLayout.insertWidget(
            1, self.iconLabel, 0, Qt.AlignLeft | Qt.AlignBottom
        )  # 将标签添加到布局中
        self.window().windowIconChanged.connect(
            self.setIcon
        )  # 窗口图标改变时，调用setIcon函数

        # add title label
        self.titleLabel = QLabel(self)  # 创建标签
        self.hBoxLayout.insertWidget(
            2, self.titleLabel, 0, Qt.AlignLeft | Qt.AlignBottom
        )  # 将标签添加到布局中
        self.titleLabel.setObjectName("titleLabel")  # 设置对象名
        self.window().windowTitleChanged.connect(
            self.setTitle
        )  # 窗口标题改变时，调用setTitle函数

    def setTitle(self, title):  # 设置标题
        self.titleLabel.setText(title)  # 设置标签的文本
        self.titleLabel.adjustSize()  # 调整标签的大小

    def setIcon(self, icon):  # 设置图标
        self.iconLabel.setPixmap(QIcon(icon).pixmap(18, 18))  # 设置图标
