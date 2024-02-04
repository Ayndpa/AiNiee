import json
import re


# 回复解析器
class Response_Parser:
    def __init__(self):
        pass

    # 处理回复，前后加上大括号
    def adjust_string(self, input_str):
        # 检查并添加开头的"{"
        if not input_str.startswith("{"):
            input_str = "{" + input_str

        # 检查并添加结尾的"}"
        if not input_str.endswith("}"):
            input_str = input_str + "}"

        return input_str

    # 将Raw文本恢复根据行数转换成json文本
    def convert_str_to_json_str(self, row_count, input_str):

        # 当发送文本为1行时，就不分割了，以免切错
        if row_count == 1:
            result = {"0": input_str}
            return json.dumps(result, ensure_ascii=False)

        else:
            str_list = input_str.split("\n")
            ret_json = {}
            for idx, text in enumerate(str_list):
                ret_json[f"{idx}"] = f"{text}"
            return json.dumps(ret_json, ensure_ascii=False)

    # 检查回复内容是否存在问题
    def check_response_content(self, response_str, source_text_dict):
        # 存储检查结果
        check_result = False
        # 存储错误内容
        error_content = "0"

        # 检查模型是否退化，出现高频词（只检测中日）
        if Response_Parser.model_degradation_detection(self, response_str):
            pass

        else:
            check_result = False
            # 存储错误内容
            error_content = "AI回复内容出现高频词,并重新翻译"
            return check_result, error_content

        # 检查文本格式
        if Response_Parser.check_response_format(self, response_str):
            # 回复文本转换成字典格式
            response_dict = json.loads(response_str)

        else:
            check_result = False
            # 存储错误内容
            error_content = "AI回复内容不符合要求的格式,将进行重新翻译"
            return check_result, error_content

        # 检查文本行数
        if Response_Parser.check_text_line_count(self, source_text_dict, response_dict):
            pass
        else:
            check_result = False
            # 存储错误内容
            error_content = "AI回复内容文本行数与原来数量不符合,将进行重新翻译"
            return check_result, error_content

        # 检查文本空行
        if Response_Parser.check_empty_response(self, response_dict):
            pass
        else:
            check_result = False
            # 存储错误内容
            error_content = "AI回复内容中有未进行翻译的空行,将进行重新翻译"
            return check_result, error_content

        # 如果检查都没有问题
        check_result = True
        # 存储错误内容
        error_content = "检查无误"
        return check_result, error_content

    # 检查回复内容的json格式
    def check_response_format(self, response_str):
        try:
            response_dict = json.loads(
                response_str
            )  # 注意转化为字典的数字序号key是字符串类型
            return True
        except:
            return False

    # 检查回复内容的文本行数
    def check_text_line_count(self, source_text_dict, response_dict):
        if len(source_text_dict) == len(response_dict):
            return True
        else:
            return False

    # 检查翻译内容是否有空值
    def check_empty_response(self, response_dict):
        for value in response_dict.values():
            # 检查value是不是None，因为AI回回复null，但是json.loads()会把null转化为None
            if value is None:
                return False

            # 检查value是不是空字符串，因为AI回回复空字符串，但是json.loads()会把空字符串转化为""
            if value == "":
                return False

            return True

    # 模型退化检测，高频语气词
    def model_degradation_detection(self, input_string):
        # 使用正则表达式匹配中日语字符
        japanese_chars = re.findall(
            r"[\u3040-\u309F\u30A0-\u30FF\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF]",
            input_string,
        )

        # 统计中日语字符的数量
        char_count = {}
        for char in japanese_chars:
            char_count[char] = char_count.get(char, 0) + 1

        # 输出字符数量
        for char, count in char_count.items():
            if count >= 90:
                return False
                # print(f"中日语字符 '{char}' 出现了 {count} 次一次。")

        return True

    # 计算字符串里面日文与中文，韩文,英文字母（不是单词）的数量
    def count_japanese_chinese_korean(self, text):
        japanese_pattern = re.compile(
            r"[\u3040-\u30FF\u31F0-\u31FF\uFF65-\uFF9F]"
        )  # 匹配日文字符
        chinese_pattern = re.compile(r"[\u4E00-\u9FFF]")  # 匹配中文字符
        korean_pattern = re.compile(
            r"[\uAC00-\uD7AF\u1100-\u11FF\u3130-\u318F\uA960-\uA97F\uD7B0-\uD7FF]"
        )  # 匹配韩文字符
        english_pattern = re.compile(
            r"[A-Za-z\uFF21-\uFF3A\uFF41-\uFF5A]"
        )  # 匹配半角和全角英文字母
        japanese_count = len(japanese_pattern.findall(text))  # 统计日文字符数量
        chinese_count = len(chinese_pattern.findall(text))  # 统计中文字符数量
        korean_count = len(korean_pattern.findall(text))  # 统计韩文字符数量
        english_count = len(english_pattern.findall(text))  # 统计英文字母数量
        return japanese_count, chinese_count, korean_count, english_count
