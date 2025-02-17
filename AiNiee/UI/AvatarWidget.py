import os
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QImage, QPainter, QColor, QBrush, QFont
from qfluentwidgets import NavigationWidget, isDarkTheme
from ..Global import Global


class AvatarWidget(NavigationWidget):  # 头像导航项
    """Avatar widget"""

    def __init__(self, parent=None):
        super().__init__(isSelectable=False, parent=parent)
        self.avatar = QImage(os.path.join(Global.resource_dir, "Avatar.png")).scaled(
            24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.SmoothPixmapTransform | QPainter.Antialiasing)

        painter.setPen(Qt.NoPen)

        if self.isPressed:
            painter.setOpacity(0.7)

        # draw background
        if self.isEnter:
            c = 255 if isDarkTheme() else 0
            painter.setBrush(QColor(c, c, c, 10))
            painter.drawRoundedRect(self.rect(), 5, 5)

        # draw avatar
        painter.setBrush(QBrush(self.avatar))
        painter.translate(8, 6)
        painter.drawEllipse(0, 0, 24, 24)
        painter.translate(-8, -6)

        if not self.isCompacted:
            painter.setPen(Qt.white if isDarkTheme() else Qt.black)
            font = QFont("Segoe UI")
            font.setPixelSize(14)
            painter.setFont(font)
            painter.drawText(QRect(44, 0, 255, 36), Qt.AlignVCenter, "NEKOparapa")
