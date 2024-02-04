from PyQt5.QtCore import QObject, pyqtSignal, Qt
from qfluentwidgets import StateToolTip, InfoBar, InfoBarPosition
from ..Global import Global


# 界面提示器
class User_Interface_Prompter(QObject):
    signal = pyqtSignal(str, str, int, int, int)  # 创建信号,并确定发送参数类型

    def __init__(self):
        super().__init__()  # 调用父类的构造函数
        self.stateTooltip = None  # 存储翻译状态控件
        self.total_text_line_count = 0  # 存储总文本行数
        self.translated_line_count = 0  # 存储已经翻译文本行数
        self.tokens_spent = 0  # 存储已经花费的tokens
        self.amount_spent = 0  # 存储已经花费的金钱

        self.openai_price_data = {
            "gpt-3.5-turbo": {
                "input_price": 0.0015,
                "output_price": 0.002,
            },  # 存储的价格是 /k tokens
            "gpt-3.5-turbo-0301": {"input_price": 0.0015, "output_price": 0.002},
            "gpt-3.5-turbo-0613": {"input_price": 0.0015, "output_price": 0.002},
            "gpt-3.5-turbo-1106": {"input_price": 0.001, "output_price": 0.002},
            "gpt-3.5-turbo-0125": {"input_price": 0.0005, "output_price": 0.0015},
            "gpt-3.5-turbo-16k": {"input_price": 0.001, "output_price": 0.002},
            "gpt-3.5-turbo-16k-0613": {"input_price": 0.001, "output_price": 0.002},
            "gpt-4": {"input_price": 0.03, "output_price": 0.06},
            "gpt-4-0314": {"input_price": 0.03, "output_price": 0.06},
            "gpt-4-0613": {"input_price": 0.03, "output_price": 0.06},
            "gpt-4-turbo-preview": {"input_price": 0.01, "output_price": 0.03},
            "gpt-4-1106-preview": {"input_price": 0.01, "output_price": 0.03},
            "gpt-4-0125-preview": {"input_price": 0.01, "output_price": 0.03},
            "gpt-4-32k": {"input_price": 0.06, "output_price": 0.12},
            "gpt-4-32k-0314": {"input_price": 0.06, "output_price": 0.12},
            "gpt-4-32k-0613": {"input_price": 0.06, "output_price": 0.12},
            "text-embedding-ada-002": {"input_price": 0.0001, "output_price": 0},
            "text-embedding-3-small": {"input_price": 0.00002, "output_price": 0},
            "text-embedding-3-large": {"input_price": 0.00013, "output_price": 0},
        }

        self.google_price_data = {
            "gemini-pro": {
                "input_price": 0.00001,
                "output_price": 0.00001,
            },  # 存储的价格是 /k tokens
        }

        self.sakura_price_data = {
            "Sakura-13B-LNovel-v0.8": {
                "input_price": 0.00001,
                "output_price": 0.00001,
            },  # 存储的价格是 /k tokens
            "Sakura-13B-LNovel-v0.9": {
                "input_price": 0.00001,
                "output_price": 0.00001,
            },  # 存储的价格是 /k tokens
        }

    # 槽函数，用于接收子线程发出的信号，更新界面UI的状态，因为子线程不能更改父线程的QT的UI控件的值
    def on_update_ui(self, input_str1, input_str2, iunput_int1, input_int2, input_int3):

        if input_str1 == "翻译状态提示":
            if input_str2 == "开始翻译":
                self.stateTooltip = StateToolTip(
                    "正在进行翻译中", "客官请耐心等待哦~~", Global.window
                )
                self.stateTooltip.move(
                    510, 30
                )  # 设定控件的出现位置，该位置是传入的Global.window窗口的位置
                self.stateTooltip.show()
            elif input_str2 == "翻译完成":
                self.stateTooltip.setContent("已经翻译完成啦 😆")
                self.stateTooltip.setState(True)
                self.stateTooltip = None

        elif input_str1 == "初始化翻译界面数据":
            # 更新翻译项目信息
            translation_project = Global.configurator.translation_project
            Global.window.Widget_start_translation.A_settings.translation_project.setText(
                translation_project
            )

            # 更新项目ID信息
            Global.window.Widget_start_translation.A_settings.project_id.setText(
                input_str2
            )

            # 更新需要翻译的文本行数信息
            self.total_text_line_count = iunput_int1  # 存储总文本行数
            Global.window.Widget_start_translation.A_settings.total_text_line_count.setText(
                str(self.total_text_line_count)
            )

            # 其他信息设置为0
            Global.window.Widget_start_translation.A_settings.translated_line_count.setText(
                "0"
            )
            Global.window.Widget_start_translation.A_settings.tokens_spent.setText("0")
            Global.window.Widget_start_translation.A_settings.amount_spent.setText("0")
            Global.window.Widget_start_translation.A_settings.progressRing.setValue(0)

            # 初始化存储的数值
            self.translated_line_count = 0  # 存储已经翻译文本行数
            self.tokens_spent = 0  # 存储已经花费的tokens
            self.amount_spent = 0  # 存储已经花费的金钱

        elif input_str1 == "更新翻译界面数据":
            if input_str2 == "翻译成功":
                # 更新已经翻译的文本数
                self.translated_line_count = self.translated_line_count + iunput_int1
                Global.window.Widget_start_translation.A_settings.translated_line_count.setText(
                    str(self.translated_line_count)
                )

            # 更新已经花费的tokens
            self.tokens_spent = self.tokens_spent + input_int2 + input_int3
            Global.window.Widget_start_translation.A_settings.tokens_spent.setText(
                str(self.tokens_spent)
            )

            # 更新已经花费的金额
            if Global.configurator.translation_platform == "Openai官方":
                # 获取使用的模型输入价格与输出价格
                input_price = self.openai_price_data[Global.configurator.model_type][
                    "input_price"
                ]
                output_price = self.openai_price_data[Global.configurator.model_type][
                    "output_price"
                ]

            elif Global.configurator.translation_platform == "Openai代理":
                # 获取使用的模型输入价格与输出价格
                input_price = (
                    Global.window.Widget_Openai_Proxy.B_settings.spinBox_input_pricing.value()
                )  # 获取输入价格
                output_price = (
                    Global.window.Widget_Openai_Proxy.B_settings.spinBox_output_pricing.value()
                )  # 获取输出价格

            elif Global.configurator.translation_platform == "Google官方":
                # 获取使用的模型输入价格与输出价格
                input_price = self.google_price_data[Global.configurator.model_type][
                    "input_price"
                ]
                output_price = self.google_price_data[Global.configurator.model_type][
                    "output_price"
                ]

            elif Global.configurator.translation_platform == "SakuraLLM":
                # 获取使用的模型输入价格与输出价格
                input_price = self.sakura_price_data[Global.configurator.model_type][
                    "input_price"
                ]
                output_price = self.sakura_price_data[Global.configurator.model_type][
                    "output_price"
                ]

            self.amount_spent = (
                self.amount_spent
                + (input_price / 1000 * input_int2)
                + (output_price / 1000 * input_int3)
            )
            self.amount_spent = round(self.amount_spent, 4)
            Global.window.Widget_start_translation.A_settings.amount_spent.setText(
                str(self.amount_spent)
            )

            # 更新进度条
            result = self.translated_line_count / self.total_text_line_count * 100
            result = round(result, 0)
            result = int(result)
            Global.window.Widget_start_translation.A_settings.progressRing.setValue(
                result
            )

        elif input_str1 == "接口测试结果":
            if input_str2 == "测试成功":
                self.createSuccessInfoBar("全部Apikey请求测试成功")
            else:
                self.createErrorInfoBar("存在Apikey请求测试失败")

    # 成功信息居中弹出框函数
    def createSuccessInfoBar(self, str):
        InfoBar.success(
            title="[Success]",
            content=str,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=Global.window,
        )

    # 错误信息右下方弹出框函数
    def createErrorInfoBar(self, str):
        InfoBar.error(
            title="[Error]",
            content=str,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=-1,  # won't disappear automatically
            parent=Global.window,
        )

    # 提醒信息左上角弹出框函数
    def createWarningInfoBar(self, str):
        InfoBar.warning(
            title="[Warning]",
            content=str,
            orient=Qt.Horizontal,
            isClosable=False,  # disable close button
            position=InfoBarPosition.TOP_LEFT,
            duration=2000,
            parent=Global.window,
        )
