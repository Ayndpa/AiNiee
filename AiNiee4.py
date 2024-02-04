# ═══════════════════════════════════════════════════════
# ████ WARNING: Enter at Your Own Risk!               ████
# ████ Congratulations, you have stumbled upon my     ████
# ████ modified AiNiee shit mountain. Despite the     ████
# ████ changes, it remains a shit mountain.           ████
# ████ Proceed with caution, as reading this code     ████
# ████ may result in immediate unhappiness and despair. ████
# ═══════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════
# ████ 警告：擅自进入，后果自负                         ████
# ████ 恭喜你，你已经发现了我改过的AiNiee屎山            ████
# ████ 尽管它终究还是一座屎山                            ████
# ████ 请谨慎前行，阅读这段代码可能会                    ████
# ████ 立刻让你感到不幸和绝望                          ████
# ═══════════════════════════════════════════════════════

# coding:utf-8
import os
import sys
import multiprocessing
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from AiNiee.UI.MainWindow import MainWindow
from AiNiee.Basic_Logic.User_Interface_Prompter import User_Interface_Prompter
from AiNiee.Basic_Logic.Request_Limiter import Request_Limiter
from AiNiee.Basic_Logic.Configurator import Configurator
from AiNiee.Global import Global


# 主函数
def main():
    # 开启子进程支持
    multiprocessing.freeze_support()

    # 启用了高 DPI 缩放
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # 创建全局UI通讯器
    Global.user_interface_prompter = User_Interface_Prompter()
    Global.user_interface_prompter.signal.connect(
        Global.user_interface_prompter.on_update_ui
    )  # 创建信号与槽函数的绑定，使用方法为：Global.user_interface_prompter.signal.emit("str","str"....)

    # 创建全局限制器
    Global.request_limiter = Request_Limiter()

    # 创建全局配置器
    Global.configurator = Configurator()

    # 创建了一个 QApplication 对象
    app = QApplication(sys.argv)
    # 创建全局窗口对象
    Global.window = MainWindow()

    # 窗口对象显示
    Global.window.show()

    # 读取配置文件
    Global.configurator.read_write_config("read")

    # 进入事件循环，等待用户操作
    sys.exit(app.exec_())


# 工作目录改为python源代码所在的目录
Global.script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))  # 获取当前工作目录
print("[INFO] 当前工作目录是:", Global.script_dir, "\n")
# 设置资源文件夹路径
Global.resource_dir = os.path.join(Global.script_dir, "resource")

if __name__ == "__main__":
    main()
