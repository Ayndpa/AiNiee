import re
from ..Global import Global


# 缓存器
class Cache_Manager:
    """
    缓存数据以列表来存储，分文件头和文本单元，文件头数据结构如下:
    1.项目类型： "project_type"

    文本单元的数据结构如下:
    1.翻译状态： "translation_status"   未翻译状态为0，已翻译为1，正在翻译为2，正在嵌入或者嵌入完成为3，不需要翻译为7
    2.文本归类： "text_classification"
    3.文本索引： "text_index"
    4.原文： "source_text"
    5.译文： "translated_text"
    6.语义相似度："semantic_similarity"
    7.存储路径： "storage_path"
    8.存储文件名： "storage_file_name"
    9.行索引： "line_index"
    """

    def __init__(self):
        pass

    # 整数型，浮点型数字变换为字符型数字函数，，且改变翻译状态为7,因为T++读取到整数型数字时，会报错，明明是自己导出来的...
    def convert_source_text_to_str(self, cache_list):
        for entry in cache_list:
            source_text = entry.get("source_text")

            if isinstance(source_text, (int, float)):
                entry["source_text"] = str(source_text)
                entry["translation_status"] = 7

    # 处理缓存数据的非中日韩字符，且改变翻译状态为7
    def process_dictionary_list(self, cache_list):
        pattern = re.compile(
            r"[\u4e00-\u9fff\u3040-\u30ff\u1100-\u11ff\u3130-\u318f\uac00-\ud7af]+"
        )

        def contains_cjk(text):
            return bool(pattern.search(text))

        for entry in cache_list:
            source_text = entry.get("source_text")

            if source_text and not contains_cjk(source_text):
                entry["translation_status"] = 7

    # 获取缓存数据中指定行数的未翻译文本，且改变翻译状态为2
    def process_dictionary_data(self, rows, cache_list):
        """
        列表元素结构如下:
        1.文本索引： "text_index"
        2.原文： "source_text"
        """
        ex_list = [
            {"text_index": 4, "source_text": "しこトラ！"},
            {"text_index": 5, "source_text": "11111"},
            {"text_index": 6, "source_text": "しこトラ！"},
        ]

        new_list = []

        for entry in cache_list:
            translation_status = entry.get("translation_status")

            if translation_status == 0:
                source_text = entry.get("source_text")
                text_index = entry.get("text_index")

                if source_text is not None and text_index is not None:
                    new_list.append(
                        {"text_index": text_index, "source_text": source_text}
                    )

                entry["translation_status"] = 2

                # 如果新列表中的元素个数达到指定行数，则停止遍历
                if len(new_list) == rows:
                    break

        return new_list

    # 将未翻译的文本列表，转换成待发送的原文字典,并计算文本行数，因为最后一些文本可能达到不了每次翻译行数
    def create_dictionary_from_list(self, data_list):
        """
        字典元素结构如下:
        "index":"source_text"
        """
        ex_dict = {
            "0": "测试！",
            "1": "测试1122211",
            "2": "测试xxxx！",
        }

        new_dict = {}

        for index, entry in enumerate(data_list):
            source_text = entry.get("source_text")

            if source_text is not None:
                new_dict[str(index)] = source_text

        return new_dict, len(data_list)

    # 将翻译结果录入缓存函数，且改变翻译状态为1
    def update_cache_data(self, cache_data, source_text_list, response_dict):
        # 输入的数据结构参考
        ex_cache_data = [
            {"project_type": "Mtool"},
            {
                "text_index": 1,
                "text_classification": 0,
                "translation_status": 0,
                "source_text": "しこトラ！",
                "translated_text": "无",
            },
            {
                "text_index": 2,
                "text_classification": 0,
                "translation_status": 1,
                "source_text": "室内カメラ",
                "translated_text": "无",
            },
            {
                "text_index": 3,
                "text_classification": 0,
                "translation_status": 0,
                "source_text": "11111",
                "translated_text": "无",
            },
            {
                "text_index": 4,
                "text_classification": 0,
                "translation_status": 0,
                "source_text": "11111",
                "translated_text": "无",
            },
            {
                "text_index": 5,
                "text_classification": 0,
                "translation_status": 0,
                "source_text": "11111",
                "translated_text": "无",
            },
            {
                "text_index": 6,
                "text_classification": 0,
                "translation_status": 0,
                "source_text": "11111",
                "translated_text": "无",
            },
        ]

        ex_source_text_list = [
            {"text_index": 4, "source_text": "しこトラ！"},
            {"text_index": 5, "source_text": "11111"},
            {"text_index": 6, "source_text": "しこトラ！"},
        ]

        ex_response_dict = {
            "0": "测试！",
            "1": "测试1122211",
            "2": "测试xxxx！",
        }

        # 回复文本的索引
        index = 0

        # 遍历原文本列表
        for source_text_item in source_text_list:
            # 获取缓存文本中索引值
            text_index = source_text_item.get("text_index")
            # 根据回复文本的索引值，在回复内容中获取已翻译的文本
            response_value = response_dict.get(str(index))

            # 缓存文本中索引值，基本上是缓存文件里元素的位置索引值，所以直接获取并修改
            if response_value is not None:
                if (
                    "text_index" in cache_data[text_index]
                    and cache_data[text_index]["text_index"] == text_index
                ):
                    cache_data[text_index]["translation_status"] = 1
                    cache_data[text_index]["translated_text"] = response_value

            # 增加索引值
            index = index + 1

        return cache_data

    # 统计翻译状态等于0的元素个数
    def count_translation_status_0(self, data):
        # 输入的数据结构参考
        ex_cache_data = [
            {"project_type": "Mtool"},
            {
                "text_index": 1,
                "text_classification": 0,
                "translation_status": 0,
                "source_text": "しこトラ！",
                "translated_text": "无",
            },
            {
                "text_index": 2,
                "text_classification": 0,
                "translation_status": 1,
                "source_text": "室内カメラ",
                "translated_text": "无",
            },
            {
                "text_index": 3,
                "text_classification": 0,
                "translation_status": 0,
                "source_text": "11111",
                "translated_text": "无",
            },
            {
                "text_index": 4,
                "text_classification": 0,
                "translation_status": 2,
                "source_text": "11111",
                "translated_text": "无",
            },
            {
                "text_index": 5,
                "text_classification": 0,
                "translation_status": 2,
                "source_text": "11111",
                "translated_text": "无",
            },
            {
                "text_index": 6,
                "text_classification": 0,
                "translation_status": 0,
                "source_text": "11111",
                "translated_text": "无",
            },
        ]

        count_0 = sum(1 for item in data if item.get("translation_status") == 0)

        counts = count_0
        return counts

    # 统计翻译状态等于0或者2的元素个数，且把等于2的翻译状态改为0.并返回元素个数
    def count_and_update_translation_status_0_2(self, data):
        # 输入的数据结构参考
        ex_cache_data = [
            {"project_type": "Mtool"},
            {
                "text_index": 1,
                "text_classification": 0,
                "translation_status": 0,
                "source_text": "しこトラ！",
                "translated_text": "无",
            },
            {
                "text_index": 2,
                "text_classification": 0,
                "translation_status": 1,
                "source_text": "室内カメラ",
                "translated_text": "无",
            },
            {
                "text_index": 3,
                "text_classification": 0,
                "translation_status": 0,
                "source_text": "11111",
                "translated_text": "无",
            },
            {
                "text_index": 4,
                "text_classification": 0,
                "translation_status": 2,
                "source_text": "11111",
                "translated_text": "无",
            },
            {
                "text_index": 5,
                "text_classification": 0,
                "translation_status": 2,
                "source_text": "11111",
                "translated_text": "无",
            },
            {
                "text_index": 6,
                "text_classification": 0,
                "translation_status": 0,
                "source_text": "11111",
                "translated_text": "无",
            },
        ]

        count_0 = sum(1 for item in data if item.get("translation_status") == 0)
        count_2 = sum(1 for item in data if item.get("translation_status") == 2)

        # 将'translation_status'等于2的元素的'translation_status'改为0
        for item in data:
            if item.get("translation_status") == 2:
                item["translation_status"] = 0

        counts = count_0 + count_2
        return counts

    # 统计已翻译文本的tokens总量，并根据不同项目修改翻译状态
    def count_tokens(self, data):
        # 输入的数据结构参考
        ex_cache_data = [
            {"project_type": "Mtool"},
            {
                "text_index": 1,
                "text_classification": 0,
                "translation_status": 0,
                "source_text": "しこトラ！",
                "translated_text": "无",
            },
            {
                "text_index": 2,
                "text_classification": 0,
                "translation_status": 1,
                "source_text": "室内カメラ",
                "translated_text": "无",
            },
            {
                "text_index": 3,
                "text_classification": 0,
                "translation_status": 0,
                "source_text": "11111",
                "translated_text": "无",
            },
            {
                "text_index": 4,
                "text_classification": 0,
                "translation_status": 2,
                "source_text": "11111",
                "translated_text": "无",
            },
            {
                "text_index": 5,
                "text_classification": 0,
                "translation_status": 2,
                "source_text": "11111",
                "translated_text": "无",
            },
            {
                "text_index": 6,
                "text_classification": 0,
                "translation_status": 0,
                "source_text": "11111",
                "translated_text": "无",
            },
        ]

        # 存储tokens总消耗的
        tokens_consume_all = 0

        # 提取项目类型,根据不同项目进行处理
        if data[0]["project_type"] == "Mtool":
            for item in data:
                if item.get("translation_status") == 0:
                    string1 = item["source_text"]
                    tokens_consume_all = (
                        Global.request_limiter.num_tokens_from_string(string1)
                        + tokens_consume_all
                    )
                    string2 = item["translated_text"]
                    tokens_consume_all = (
                        Global.request_limiter.num_tokens_from_string(string2)
                        + tokens_consume_all
                    )
                    pass

        else:
            for item in data:

                # 这个判断要放在前面，比如会和下面的修改冲突
                if item.get("translation_status") == 0:
                    item["translation_status"] = 7

                if item.get("translation_status") == 1:
                    item["translation_status"] = 0
                    string1 = item["source_text"]
                    tokens_consume_all = (
                        Global.request_limiter.num_tokens_from_string(string1)
                        + tokens_consume_all
                    )
                    string2 = item["translated_text"]
                    tokens_consume_all = (
                        Global.request_limiter.num_tokens_from_string(string2)
                        + tokens_consume_all
                    )
                    pass

        return tokens_consume_all

    # 替换或者还原换行符和回车符函数
    def replace_special_characters(self, dict, mode):
        new_dict = {}
        if mode == "替换":
            for key, value in dict.items():
                # 如果value是字符串变量
                if isinstance(value, str):
                    new_value = value.replace("\n", "⚡").replace("\r", "♫")
                    new_dict[key] = new_value
        elif mode == "还原":
            for key, value in dict.items():
                # 如果value是字符串变量
                if isinstance(value, str):
                    new_value = value.replace("⚡", "\n").replace("♫", "\r")
                    new_dict[key] = new_value
        else:
            print("请输入正确的mode参数（替换或还原）")

        return new_dict

    # 根据输入的tokens，从缓存数据中提取对应的翻译对,并改变翻译状态为3，表示正在嵌入中或者嵌入完成
    def process_tokens(cache_data, input_tokens):
        accumulated_tokens = 0
        source_texts = []
        translated_texts = []
        text_index_list = []

        for element in cache_data:
            translation_status = element.get("translation_status")

            if translation_status == 0:
                source_text = element.get("source_text", "")
                translated_text = element.get("translated_text", "")
                text_index = element.get("text_index", "")

                # 计算原文和译文的tokens总和
                total_tokens = Global.request_limiter.num_tokens_from_string(
                    source_text
                ) + Global.request_limiter.num_tokens_from_string(translated_text)

                # 判断累积的tokens是否超过输入的tokens
                if accumulated_tokens + total_tokens <= input_tokens:
                    accumulated_tokens += total_tokens
                    element["translation_status"] = 3
                    source_texts.append(source_text)
                    translated_texts.append(translated_text)
                    text_index_list.append(text_index)

                else:
                    break  # 超过tokens限制，结束遍历

        return accumulated_tokens, source_texts, translated_texts, text_index_list

    # 根据列表修改对应元素的向量距离
    def update_vector_distance(cache_data, text_index_list, vector_distance_list):

        # 输入的数据结构参考
        ex_cache_data = [
            {"project_type": "Mtool"},
            {
                "text_index": 1,
                "text_classification": 0,
                "translation_status": 0,
                "source_text": "しこトラ！",
                "translated_text": "无",
                "semantic_similarity": 0,
            },
            {
                "text_index": 2,
                "text_classification": 0,
                "translation_status": 1,
                "source_text": "室内カメラ",
                "translated_text": "无",
                "semantic_similarity": 0,
            },
            {
                "text_index": 3,
                "text_classification": 0,
                "translation_status": 0,
                "source_text": "11111",
                "translated_text": "无",
                "semantic_similarity": 0,
            },
            {
                "text_index": 4,
                "text_classification": 0,
                "translation_status": 2,
                "source_text": "11111",
                "translated_text": "无",
                "semantic_similarity": 0,
            },
            {
                "text_index": 5,
                "text_classification": 0,
                "translation_status": 2,
                "source_text": "11111",
                "translated_text": "无",
                "semantic_similarity": 0,
            },
            {
                "text_index": 6,
                "text_classification": 0,
                "translation_status": 0,
                "source_text": "11111",
                "translated_text": "无",
                "semantic_similarity": 0,
            },
        ]

        # 输入的索引列表参考
        ex_text_index_list = [2, 3, 4]

        # 输入的向量距离列表参考
        ex_vector_distance_list = [89.911, 51.511, 14.111]

        for i in range(len(text_index_list)):
            index_to_update = text_index_list[i]
            distance_to_update = vector_distance_list[i]

            for data in cache_data:
                if "text_index" in data and data["text_index"] == index_to_update:
                    data["semantic_similarity"] = distance_to_update
                    break
