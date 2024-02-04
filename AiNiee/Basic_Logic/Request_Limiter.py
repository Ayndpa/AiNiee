# 请求限制器
import threading
import time

import tiktoken
from ..Global import Global


class Request_Limiter:
    def __init__(self):
        # 示例数据
        self.openai_limit_data = {
            "免费账号": {
                "gpt-3.5-turbo": {"max_tokens": 4000, "TPM": 40000, "RPM": 3},
                "gpt-3.5-turbo-0301": {"max_tokens": 4000, "TPM": 40000, "RPM": 3},
                "gpt-3.5-turbo-0613": {"max_tokens": 4000, "TPM": 40000, "RPM": 3},
                "gpt-3.5-turbo-1106": {"max_tokens": 4000, "TPM": 40000, "RPM": 3},
                "gpt-3.5-turbo-0125": {"max_tokens": 4000, "TPM": 150000, "RPM": 3},
                "gpt-3.5-turbo-16k": {"max_tokens": 16000, "TPM": 40000, "RPM": 3},
                "gpt-3.5-turbo-16k-0613": {"max_tokens": 16000, "TPM": 40000, "RPM": 3},
                "text-embedding-ada-002": {"max_tokens": 8000, "TPM": 150000, "RPM": 3},
                "text-embedding-3-small": {"max_tokens": 8000, "TPM": 150000, "RPM": 3},
                "text-embedding-3-large": {"max_tokens": 8000, "TPM": 150000, "RPM": 3},
            },
            "付费账号(等级1)": {
                "gpt-3.5-turbo": {"max_tokens": 4000, "TPM": 60000, "RPM": 3500},
                "gpt-3.5-turbo-0301": {"max_tokens": 4000, "TPM": 60000, "RPM": 3500},
                "gpt-3.5-turbo-0613": {"max_tokens": 4000, "TPM": 60000, "RPM": 3500},
                "gpt-3.5-turbo-1106": {"max_tokens": 4000, "TPM": 60000, "RPM": 3500},
                "gpt-3.5-turbo-0125": {"max_tokens": 4000, "TPM": 120000, "RPM": 2000},
                "gpt-3.5-turbo-16k": {"max_tokens": 16000, "TPM": 60000, "RPM": 3500},
                "gpt-3.5-turbo-16k-0613": {
                    "max_tokens": 16000,
                    "TPM": 60000,
                    "RPM": 3500,
                },
                "gpt-4": {"max_tokens": 8000, "TPM": 10000, "RPM": 500},
                "gpt-4-0314": {"max_tokens": 8000, "TPM": 10000, "RPM": 500},
                "gpt-4-0613": {"max_tokens": 8000, "TPM": 10000, "RPM": 500},
                "gpt-4-turbo-preview": {"max_tokens": 4000, "TPM": 150000, "RPM": 500},
                "gpt-4-1106-preview": {"max_tokens": 4000, "TPM": 150000, "RPM": 500},
                "gpt-4-0125-preview": {"max_tokens": 4000, "TPM": 150000, "RPM": 500},
                # "gpt-4-32k": {"max_tokens": 32000, "TPM": 200, "RPM": 500},
                # "gpt-4-32k-0314": {"max_tokens": 32000, "TPM": 200, "RPM": 500},
                # "gpt-4-32k-0613": {"max_tokens": 32000, "TPM": 200, "RPM": 500},
                "text-embedding-ada-002": {
                    "max_tokens": 8000,
                    "TPM": 1000000,
                    "RPM": 500,
                },
            },
            "付费账号(等级2)": {
                "gpt-3.5-turbo": {"max_tokens": 4000, "TPM": 80000, "RPM": 3500},
                "gpt-3.5-turbo-0301": {"max_tokens": 4000, "TPM": 80000, "RPM": 3500},
                "gpt-3.5-turbo-0613": {"max_tokens": 4000, "TPM": 80000, "RPM": 3500},
                "gpt-3.5-turbo-1106": {"max_tokens": 4000, "TPM": 80000, "RPM": 3500},
                "gpt-3.5-turbo-0125": {"max_tokens": 4000, "TPM": 160000, "RPM": 2000},
                "gpt-3.5-turbo-16k": {"max_tokens": 16000, "TPM": 80000, "RPM": 3500},
                "gpt-3.5-turbo-16k-0613": {
                    "max_tokens": 16000,
                    "TPM": 80000,
                    "RPM": 3500,
                },
                "gpt-4": {"max_tokens": 8000, "TPM": 40000, "RPM": 5000},
                "gpt-4-0314": {"max_tokens": 8000, "TPM": 40000, "RPM": 5000},
                "gpt-4-0613": {"max_tokens": 8000, "TPM": 40000, "RPM": 5000},
                "gpt-4-turbo-preview": {"max_tokens": 4000, "TPM": 300000, "RPM": 5000},
                "gpt-4-1106-preview": {"max_tokens": 4000, "TPM": 300000, "RPM": 5000},
                "gpt-4-0125-preview": {"max_tokens": 4000, "TPM": 300000, "RPM": 5000},
                # "gpt-4-32k": {"max_tokens": 32000, "TPM": 200, "RPM": 5000},
                # "gpt-4-32k-0314": {"max_tokens": 32000, "TPM": 200, "RPM": 5000},
                # "gpt-4-32k-0613": {"max_tokens": 32000, "TPM": 200, "RPM": 5000},
                "text-embedding-ada-002": {
                    "max_tokens": 8000,
                    "TPM": 1000000,
                    "RPM": 500,
                },
            },
            "付费账号(等级3)": {
                "gpt-3.5-turbo": {"max_tokens": 4000, "TPM": 160000, "RPM": 5000},
                "gpt-3.5-turbo-0301": {"max_tokens": 4000, "TPM": 160000, "RPM": 5000},
                "gpt-3.5-turbo-0613": {"max_tokens": 4000, "TPM": 160000, "RPM": 5000},
                "gpt-3.5-turbo-1106": {"max_tokens": 4000, "TPM": 250000, "RPM": 3000},
                "gpt-3.5-turbo-0125": {"max_tokens": 4000, "TPM": 160000, "RPM": 5000},
                "gpt-3.5-turbo-16k": {"max_tokens": 16000, "TPM": 160000, "RPM": 5000},
                "gpt-3.5-turbo-16k-0613": {
                    "max_tokens": 16000,
                    "TPM": 160000,
                    "RPM": 5000,
                },
                "gpt-4": {"max_tokens": 8000, "TPM": 80000, "RPM": 5000},
                "gpt-4-0314": {"max_tokens": 8000, "TPM": 80000, "RPM": 5000},
                "gpt-4-0613": {"max_tokens": 8000, "TPM": 80000, "RPM": 5000},
                "gpt-4-turbo-preview": {"max_tokens": 4000, "TPM": 300000, "RPM": 5000},
                "gpt-4-1106-preview": {"max_tokens": 4000, "TPM": 300000, "RPM": 5000},
                "gpt-4-0125-preview": {"max_tokens": 4000, "TPM": 300000, "RPM": 5000},
                # "gpt-4-32k": {"max_tokens": 32000, "TPM": 200, "RPM": 5000},
                # "gpt-4-32k-0314": {"max_tokens": 32000, "TPM": 200, "RPM": 5000},
                # "gpt-4-32k-0613": {"max_tokens": 32000, "TPM": 200, "RPM": 5000},
                "text-embedding-ada-002": {
                    "max_tokens": 8000,
                    "TPM": 5000000,
                    "RPM": 5000,
                },
            },
            "付费账号(等级4)": {
                "gpt-3.5-turbo": {"max_tokens": 4000, "TPM": 1000000, "RPM": 10000},
                "gpt-3.5-turbo-0301": {
                    "max_tokens": 4000,
                    "TPM": 1000000,
                    "RPM": 10000,
                },
                "gpt-3.5-turbo-0613": {
                    "max_tokens": 4000,
                    "TPM": 1000000,
                    "RPM": 10000,
                },
                "gpt-3.5-turbo-1106": {
                    "max_tokens": 4000,
                    "TPM": 1000000,
                    "RPM": 10000,
                },
                "gpt-3.5-turbo-0125": {
                    "max_tokens": 4000,
                    "TPM": 2000000,
                    "RPM": 50000,
                },
                "gpt-3.5-turbo-16k": {
                    "max_tokens": 16000,
                    "TPM": 1000000,
                    "RPM": 10000,
                },
                "gpt-3.5-turbo-16k-0613": {
                    "max_tokens": 16000,
                    "TPM": 1000000,
                    "RPM": 10000,
                },
                "gpt-4": {"max_tokens": 8000, "TPM": 300000, "RPM": 10000},
                "gpt-4-0314": {"max_tokens": 8000, "TPM": 300000, "RPM": 10000},
                "gpt-4-0613": {"max_tokens": 8000, "TPM": 300000, "RPM": 10000},
                "gpt-4-turbo-preview": {
                    "max_tokens": 4000,
                    "TPM": 450000,
                    "RPM": 10000,
                },
                "gpt-4-1106-preview": {"max_tokens": 4000, "TPM": 450000, "RPM": 10000},
                "gpt-4-0125-preview": {"max_tokens": 4000, "TPM": 450000, "RPM": 10000},
                # "gpt-4-32k": {"max_tokens": 32000, "TPM": 200, "RPM": 10000},
                # "gpt-4-32k-0314": {"max_tokens": 32000, "TPM": 200, "RPM": 10000},
                # "gpt-4-32k-0613": {"max_tokens": 32000, "TPM": 200, "RPM": 10000},
                "text-embedding-ada-002": {
                    "max_tokens": 8000,
                    "TPM": 5000000,
                    "RPM": 10000,
                },
            },
            "付费账号(等级5)": {
                "gpt-3.5-turbo": {"max_tokens": 4000, "TPM": 2000000, "RPM": 10000},
                "gpt-3.5-turbo-0301": {
                    "max_tokens": 4000,
                    "TPM": 2000000,
                    "RPM": 10000,
                },
                "gpt-3.5-turbo-0613": {
                    "max_tokens": 4000,
                    "TPM": 2000000,
                    "RPM": 10000,
                },
                "gpt-3.5-turbo-1106": {
                    "max_tokens": 4000,
                    "TPM": 2000000,
                    "RPM": 10000,
                },
                "gpt-3.5-turbo-0125": {
                    "max_tokens": 4000,
                    "TPM": 4000000,
                    "RPM": 20000,
                },
                "gpt-3.5-turbo-16k": {
                    "max_tokens": 16000,
                    "TPM": 2000000,
                    "RPM": 10000,
                },
                "gpt-3.5-turbo-16k-0613": {
                    "max_tokens": 16000,
                    "TPM": 2000000,
                    "RPM": 10000,
                },
                "gpt-4": {"max_tokens": 8000, "TPM": 300000, "RPM": 10000},
                "gpt-4-0314": {"max_tokens": 8000, "TPM": 300000, "RPM": 10000},
                "gpt-4-0613": {"max_tokens": 8000, "TPM": 300000, "RPM": 10000},
                "gpt-4-turbo-preview": {
                    "max_tokens": 4000,
                    "TPM": 600000,
                    "RPM": 10000,
                },
                "gpt-4-1106-preview": {"max_tokens": 4000, "TPM": 600000, "RPM": 10000},
                "gpt-4-0125-preview": {"max_tokens": 4000, "TPM": 600000, "RPM": 10000},
                # "gpt-4-32k": {"max_tokens": 32000, "TPM": 200, "RPM": 10000},
                # "gpt-4-32k-0314": {"max_tokens": 32000, "TPM": 200, "RPM": 10000},
                # "gpt-4-32k-0613": {"max_tokens": 32000, "TPM": 200, "RPM": 10000},
                "text-embedding-ada-002": {
                    "max_tokens": 8000,
                    "TPM": 10000000,
                    "RPM": 10000,
                },
            },
        }

        # 示例数据
        self.google_limit_data = {
            "gemini-pro": {
                "inputTokenLimit": 30720,
                "outputTokenLimit": 2048,
                "max_tokens": 2500,
                "TPM": 1000000,
                "RPM": 60,
            },
        }

        # 示例数据
        self.sakura_limit_data = {
            "Sakura-13B-LNovel-v0.8": {
                "inputTokenLimit": 30720,
                "outputTokenLimit": 2400,
                "max_tokens": 2400,
                "TPM": 1000000,
                "RPM": 60,
            },
            "Sakura-13B-LNovel-v0.9": {
                "inputTokenLimit": 30720,
                "outputTokenLimit": 2400,
                "max_tokens": 2400,
                "TPM": 1000000,
                "RPM": 60,
            },
        }

        # TPM相关参数
        self.max_tokens = 0  # 令牌桶最大容量
        self.remaining_tokens = 0  # 令牌桶剩余容量
        self.tokens_rate = 0  # 令牌每秒的恢复速率
        self.last_time = time.time()  # 上次记录时间

        # RPM相关参数
        self.last_request_time = 0  # 上次记录时间
        self.request_interval = 0  # 请求的最小时间间隔（s）
        self.lock = threading.Lock()

    def initialize_limiter(self):
        # 获取翻译平台
        translation_platform = (
            Global.window.Widget_translation_settings.A_settings.comboBox_translation_platform.currentText()
        )

        # 如果进行的是错行检查任务，修改部分设置(补丁)
        if Global.Running_status == 7:
            translation_platform = Global.configurator.translation_platform

        # 根据翻译平台读取配置信息
        if translation_platform == "Openai官方":
            # 获取账号类型
            account_type = (
                Global.window.Widget_Openai.comboBox_account_type.currentText()
            )
            # 获取模型选择
            model = Global.window.Widget_Openai.comboBox_model.currentText()

            # 获取相应的限制
            max_tokens = self.openai_limit_data[account_type][model]["max_tokens"]
            TPM_limit = self.openai_limit_data[account_type][model]["TPM"]
            RPM_limit = self.openai_limit_data[account_type][model]["RPM"]

            # 获取当前key的数量，对限制进行倍数更改
            key_count = len(Global.configurator.apikey_list)
            RPM_limit = RPM_limit * key_count
            TPM_limit = TPM_limit * key_count

            # 设置限制
            self.set_limit(max_tokens, TPM_limit, RPM_limit)

        elif translation_platform == "Openai代理":
            # 获取模型选择
            model = (
                Global.window.Widget_Openai_Proxy.A_settings.comboBox_model.currentText()
            )
            op_rpm_limit = (
                Global.window.Widget_Openai_Proxy.B_settings.spinBox_RPM.value()
            )  # 获取rpm限制值
            op_tpm_limit = (
                Global.window.Widget_Openai_Proxy.B_settings.spinBox_TPM.value()
            )  # 获取tpm限制值

            # 获取相应的限制
            max_tokens = self.openai_limit_data["付费账号(等级1)"][model]["max_tokens"]
            TPM_limit = op_tpm_limit
            RPM_limit = op_rpm_limit

            # 设置限制
            self.set_limit(max_tokens, TPM_limit, RPM_limit)

        elif translation_platform == "Google官方":
            # 获取模型
            model = Global.window.Widget_Google.comboBox_model.currentText()

            # 获取相应的限制
            max_tokens = self.google_limit_data[model]["max_tokens"]
            TPM_limit = self.google_limit_data[model]["TPM"]
            RPM_limit = self.google_limit_data[model]["RPM"]

            # 获取当前key的数量，对限制进行倍数更改
            key_count = len(Global.configurator.apikey_list)
            RPM_limit = RPM_limit * key_count
            TPM_limit = TPM_limit * key_count

            # 设置限制
            self.set_limit(max_tokens, TPM_limit, RPM_limit)

        elif translation_platform == "SakuraLLM":
            # 获取模型
            model = Global.window.Widget_SakuraLLM.comboBox_model.currentText()

            # 获取相应的限制
            max_tokens = self.sakura_limit_data[model]["max_tokens"]
            TPM_limit = self.sakura_limit_data[model]["TPM"]
            RPM_limit = self.sakura_limit_data[model]["RPM"]

            # 设置限制
            self.set_limit(max_tokens, TPM_limit, RPM_limit)

    def initialize_limiter_check(self):
        translation_platform = (
            Global.window.Widget_check.comboBox_translation_platform.currentText()
        )

        # 根据翻译平台读取配置信息
        if translation_platform == "Openai官方":
            # 获取账号类型
            account_type = (
                Global.window.Widget_Openai.comboBox_account_type.currentText()
            )
            # 获取模型选择
            model = "text-embedding-ada-002"

            # 获取相应的限制
            max_tokens = self.openai_limit_data[account_type][model]["max_tokens"]
            TPM_limit = self.openai_limit_data[account_type][model]["TPM"]
            RPM_limit = self.openai_limit_data[account_type][model]["RPM"]

            # 获取当前key的数量，对限制进行倍数更改
            key_count = len(Global.configurator.apikey_list)
            RPM_limit = RPM_limit * key_count
            TPM_limit = TPM_limit * key_count

            # 设置限制
            self.set_limit(max_tokens, TPM_limit, RPM_limit)

        elif translation_platform == "Openai代理":
            # 获取模型选择
            model = "text-embedding-ada-002"
            op_rpm_limit = (
                Global.window.Widget_Openai_Proxy.B_settings.spinBox_RPM.value()
            )  # 获取rpm限制值
            op_tpm_limit = (
                Global.window.Widget_Openai_Proxy.B_settings.spinBox_TPM.value()
            )  # 获取tpm限制值

            # 获取相应的限制
            max_tokens = self.openai_limit_data["付费账号(等级1)"][model]["max_tokens"]
            TPM_limit = op_tpm_limit
            RPM_limit = op_rpm_limit

            # 设置限制
            self.set_limit(max_tokens, TPM_limit, RPM_limit)

    # 设置限制器的参数
    def set_limit(self, max_tokens, TPM, RPM):
        # 将TPM转换成每秒tokens数
        TPs = TPM / 60

        # 将RPM转换成请求的最小时间间隔(S)
        request_interval = 60 / RPM

        # 设置限制器的TPM参数
        self.max_tokens = max_tokens  # 令牌桶最大容量
        self.remaining_tokens = max_tokens  # 令牌桶剩余容量
        self.tokens_rate = TPs  # 令牌每秒的恢复速率

        # 设置限制器的RPM参数
        self.request_interval = request_interval  # 请求的最小时间间隔（s）

    def RPM_limit(self):
        with self.lock:
            current_time = time.time()  # 获取现在的时间
            time_since_last_request = (
                current_time - self.last_request_time
            )  # 计算当前时间与上次记录时间的间隔
            if time_since_last_request < self.request_interval:
                # print("[DEBUG] Request limit exceeded. Please try again later.")
                return False
            else:
                self.last_request_time = current_time
                return True

    def TPM_limit(self, tokens):
        now = time.time()  # 获取现在的时间
        tokens_to_add = (
            now - self.last_time
        ) * self.tokens_rate  # 现在时间减去上一次记录的时间，乘以恢复速率，得出这段时间恢复的tokens数量
        self.remaining_tokens = min(
            self.max_tokens, self.remaining_tokens + tokens_to_add
        )  # 计算新的剩余容量，与最大容量比较，谁小取谁值，避免发送信息超过最大容量
        self.last_time = now  # 改变上次记录时间

        if tokens > self.remaining_tokens:
            # print("[DEBUG] 已超过剩余tokens：", tokens,'\n' )
            return False
        else:
            # print("[DEBUG] 数量足够，剩余tokens：", tokens,'\n' )
            return True

    def RPM_and_TPM_limit(self, tokens):
        if self.RPM_limit() and self.TPM_limit(tokens):
            # 如果能够发送请求，则扣除令牌桶里的令牌数
            self.remaining_tokens = self.remaining_tokens - tokens
            return True
        else:
            return False

    # 计算消息列表内容的tokens的函数
    def num_tokens_from_messages(self, messages):
        """Return the number of tokens used by a list of messages."""
        try:
            encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        except KeyError:
            print("Warning: model not found. Using cl100k_base encoding.")
            encoding = tiktoken.get_encoding("cl100k_base")

        tokens_per_message = 3
        tokens_per_name = 1
        num_tokens = 0
        for message in messages:
            num_tokens += tokens_per_message
            for key, value in message.items():
                # 如果value是字符串类型才计算tokens，否则跳过，因为AI在调用函数时，会在content中回复null，导致报错
                if isinstance(value, str):
                    num_tokens += len(encoding.encode(value))
                if key == "name":
                    num_tokens += tokens_per_name
        num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
        return num_tokens

    # 计算单个字符串tokens数量函数
    def num_tokens_from_string(self, string):
        """Returns the number of tokens in a text string."""
        encoding = tiktoken.get_encoding("cl100k_base")
        num_tokens = len(encoding.encode(string))
        return num_tokens
