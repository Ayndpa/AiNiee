import threading
from .Request_Tester import Request_Tester
from .Translator import Translator

from ..Global import Global

# 任务分发器(后台运行)
class Background_Executor(threading.Thread):
    def __init__(self, task_id):
        super().__init__()  # 调用父类构造
        self.task_id = task_id

    def run(self):
        # 执行openai官方接口测试
        if self.task_id == "openai官方接口测试":
            Global.Running_status = 1
            Request_Tester.openai_request_test(self)
            Global.Running_status = 0

        # 执行openai代理接口测试
        elif self.task_id == "openai代理接口测试":
            Global.Running_status = 1
            Request_Tester.op_request_test(self)
            Global.Running_status = 0

        # 执行google接口测试
        elif self.task_id == "google官方接口测试":
            Global.Running_status = 1
            Request_Tester.google_request_test(self)
            Global.Running_status = 0

        # 执行google接口测试
        elif self.task_id == "Sakura通讯测试":
            Global.Running_status = 1
            Request_Tester.sakura_request_test(self)
            Global.Running_status = 0

        # 执行翻译
        elif self.task_id == "执行翻译任务":
            Global.Running_status = 6
            Translator.Main(self)
            # 隐藏暂停和取消按钮
            Translator.hide_pause_and_cancel_button()
            Global.Running_status = 0
        # 执行检查任务
        elif self.task_id == "执行检查任务":
            Global.Running_status = 7
            Translator.Check_main(self)
            Global.Running_status = 0
