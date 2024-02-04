import json
import math
import multiprocessing
import os
import re
import time
import concurrent.futures
from .Api_Requester import Api_Requester
from .Cache_Manager import Cache_Manager
from .File_Outputter import File_Outputter
from .File_Reader import File_Reader
from ..Global import Global
from .Response_Parser import Response_Parser


# 翻译器
class Translator:
    def __init__(self):
        pass

    # 隐藏暂停按钮和取消按钮
    def hide_pause_and_cancel_button():
        Global.window.Widget_start_translation.A_settings.primaryButton_pause_translation.hide()
        Global.window.Widget_start_translation.A_settings.primaryButton_cancel_translation.hide()

    def Main(self):
        # ——————————————————————————————————————————配置信息初始化—————————————————————————————————————————
        Global.configurator.initialize_configuration()
        Global.request_limiter.initialize_limiter()

        # ——————————————————————————————————————————读取原文到缓存—————————————————————————————————————————
        # 读取文件
        Input_Folder = Global.configurator.Input_Folder
        if Global.configurator.translation_project == "Mtool导出文件":
            Global.cache_list = File_Reader.read_mtool_files(self, folder_path=Input_Folder)
        elif Global.configurator.translation_project == "T++导出文件":
            Global.cache_list = File_Reader.read_xlsx_files(self, folder_path=Input_Folder)
        elif Global.configurator.translation_project == "Ainiee缓存文件":
            Global.cache_list = File_Reader.read_cache_files(self, folder_path=Input_Folder)

        # 将浮点型，整数型文本内容变成字符型文本内容
        Cache_Manager.convert_source_text_to_str(self, Global.cache_list)

        # 如果翻译日语或者韩语文本时，则去除非中日韩文本
        Text_Source_Language = (
            Global.window.Widget_translation_settings.A_settings.comboBox_source_text.currentText()
        )
        if Text_Source_Language == "日语" or Text_Source_Language == "韩语":
            Cache_Manager.process_dictionary_list(self, Global.cache_list)

        # ——————————————————————————————————————————构建并发任务池子—————————————————————————————————————————

        # 计算并发任务数
        line_count_configuration = (
            Global.configurator.text_line_counts
        )  # 获取每次翻译行数配置
        total_text_line_count = Cache_Manager.count_translation_status_0(
            self, Global.cache_list
        )

        if total_text_line_count % line_count_configuration == 0:
            tasks_Num = total_text_line_count // line_count_configuration
        else:
            tasks_Num = total_text_line_count // line_count_configuration + 1

        # 更新界面UI信息，并输出各种配置信息
        project_id = Global.cache_list[0]["project_id"]
        Global.user_interface_prompter.signal.emit(
            "初始化翻译界面数据", project_id, total_text_line_count, 0, 0
        )  # 需要输入够当初设定的参数个数
        Global.user_interface_prompter.signal.emit("翻译状态提示", "开始翻译", 0, 0, 0)
        print("[INFO]  翻译项目为", Global.configurator.translation_project, "\n")
        print("[INFO]  翻译平台为", Global.configurator.translation_platform, "\n")
        print("[INFO]  AI模型为", Global.configurator.model_type, "\n")
        if (
            Global.configurator.translation_platform == "Openai代理"
            or Global.configurator.translation_platform == "SakuraLLM"
        ):
            print("[INFO]  请求地址为", Global.configurator.openai_base_url, "\n")
        elif Global.configurator.translation_platform == "Openai官方":
            print(
                "[INFO]  账号类型为",
                Global.window.Widget_Openai.comboBox_account_type.currentText(),
                "\n",
            )
        print(
            "[INFO]  游戏文本从",
            Global.configurator.source_language,
            "翻译到",
            Global.configurator.target_language,
            "\n",
        )
        if Global.configurator.translation_platform != "SakuraLLM":
            print(
                "[INFO]  当前设定的系统提示词为：",
                Global.configurator.get_system_prompt(),
                "\n",
            )
            original_exmaple, translation_example = (
                Global.configurator.get_default_translation_example()
            )
            print("[INFO]  已添加默认原文示例", original_exmaple, "\n")
            print("[INFO]  已添加默认译文示例", translation_example, "\n")
        print(
            "[INFO]  文本总行数为：",
            total_text_line_count,
            "  每次发送行数为：",
            line_count_configuration,
            "  计划的翻译任务总数是：",
            tasks_Num,
        )
        print(
            "\033[1;32m[INFO] \033[0m 五秒后开始进行翻译，请注意保持网络通畅，余额充足。",
            "\n",
        )
        time.sleep(5)

        # 测试用，会导致任务多一个，注意下
        # api_requester_instance = Api_Requester()
        # api_requester_instance.Concurrent_Request_Openai()

        # 创建实例
        api_requester_instance = Api_Requester()
        if Global.configurator.translation_platform in ["Openai官方", "Openai代理"]:
            task_func = api_requester_instance.Concurrent_Request_Openai
        elif Global.configurator.translation_platform == "Google官方":
            task_func = api_requester_instance.Concurrent_Request_Google
        elif Global.configurator.translation_platform == "SakuraLLM":
            task_func = api_requester_instance.Concurrent_Request_Sakura

        # 创建线程池
        The_Max_workers = Global.configurator.thread_counts  # 获取线程数配置
        with concurrent.futures.ThreadPoolExecutor(The_Max_workers) as executor:
            # 向线程池提交任务
            for i in range(tasks_Num):
                # 判断是否暂停，如果暂停则等待
                while Global.Running_status == 1011:
                    time.sleep(1)
                # 判断是否取消，如果取消则退出
                if Global.Running_status == 10:
                    Translator.hide_pause_and_cancel_button()
                    Global.user_interface_prompter.signal.emit("翻译状态提示","取消翻译",0,0,0)
                    return

                executor.submit(task_func)

            # 等待线程池任务完成
            executor.shutdown(wait=True)

        # 检查是否已经取消
        if Global.Running_status == 10:
            Translator.hide_pause_and_cancel_button()
            Global.user_interface_prompter.signal.emit("翻译状态提示","取消翻译",0,0,0)
            return

        # 检查是否暂停，暂停则等待
        while Global.Running_status == 1011:
            time.sleep(1)

        # ——————————————————————————————————————————检查没能成功翻译的文本，拆分翻译————————————————————————————————————————

        # 计算未翻译文本的数量
        untranslated_text_line_count = (
            Cache_Manager.count_and_update_translation_status_0_2(self, Global.cache_list)
        )

        # 重新翻译次数限制
        retry_translation_count = 1

        while untranslated_text_line_count != 0:
            print(
                "\033[1;33mWarning:\033[0m 仍然有部分未翻译，将进行拆分后重新翻译，-----------------------------------"
            )
            print(
                "[INFO] 当前重新翻译次数：",
                retry_translation_count,
                " 到达最大次数：10 时，将停止翻译",
            )

            # 根据算法计算拆分的文本行数
            line_count_configuration = Global.configurator.update_text_line_count(
                line_count_configuration
            )
            print(
                "[INFO] 未翻译文本总行数为：",
                untranslated_text_line_count,
                "  每次发送行数修改为：",
                line_count_configuration,
                "\n",
            )

            # 如果实时调教功能没有开的话，则每次重新翻译，增加OpenAI的随机性
            if (
                Global.configurator.translation_platform == "Openai官方"
                or Global.configurator.translation_platform == "Openai代理"
            ):
                if (Global.window.Interface18.checkBox.isChecked() == False) and (
                    retry_translation_count != 1
                ):
                    if Global.configurator.openai_temperature + 0.1 <= 1.0:
                        Global.configurator.openai_temperature = (
                            Global.configurator.openai_temperature + 0.1
                        )
                    else:
                        Global.configurator.openai_temperature = 1.0
                    print(
                        "\033[1;33mWarning:\033[0m 当前AI模型的随机度设置为：",
                        Global.configurator.openai_temperature,
                    )

            # 计算可并发任务总数
            if untranslated_text_line_count % line_count_configuration == 0:
                tasks_Num = untranslated_text_line_count // line_count_configuration
            else:
                tasks_Num = untranslated_text_line_count // line_count_configuration + 1

            # 创建线程池
            The_Max_workers = Global.configurator.thread_counts  # 获取线程数配置
            with concurrent.futures.ThreadPoolExecutor(The_Max_workers) as executor:
                # 向线程池提交任务
                for i in range(tasks_Num):
                    # 如果暂停则等待
                    while Global.Running_status == 1011:
                        time.sleep(1)
                    # 如果取消则退出
                    if Global.Running_status == 10:
                        Translator.hide_pause_and_cancel_button()
                        Global.user_interface_prompter.signal.emit("翻译状态提示","取消翻译",0,0,0)
                        return
                    
                    executor.submit(task_func)

                # 等待线程池任务完成
                executor.shutdown(wait=True)

            # 检查是否已经取消
            if Global.Running_status == 10:
                Translator.hide_pause_and_cancel_button()
                Global.user_interface_prompter.signal.emit("翻译状态提示","取消翻译",0,0,0)
                return
            
            # 检查是否暂停，暂停则等待
            while Global.Running_status == 1011:
                time.sleep(1)

            # 检查是否已经达到重翻次数限制
            retry_translation_count = retry_translation_count + 1
            if retry_translation_count >= 10:
                print(
                    "\033[1;33mWarning:\033[0m 已经达到重新翻译次数限制，但仍然有部分文本未翻译，不影响使用，可手动翻译",
                    "\n",
                )
                break

            # 重新计算未翻译文本的数量
            untranslated_text_line_count = (
                Cache_Manager.count_and_update_translation_status_0_2(self, Global.cache_list)
            )

        # ——————————————————————————————————————————将数据处理并保存为文件—————————————————————————————————————————
        print(
            "\033[1;32mSuccess:\033[0m  翻译阶段已完成，正在处理数据-----------------------------------",
            "\n",
        )

        # 如果开启了转换简繁开关功能，则进行文本转换
        if Global.configurator.conversion_toggle:
            if (
                Global.configurator.target_language == "简中"
                or Global.configurator.target_language == "繁中"
            ):
                try:
                    Global.cache_list = File_Outputter.simplified_and_traditional_conversion(
                        self, Global.cache_list, Global.configurator.target_language
                    )
                    print(
                        f"\033[1;32mSuccess:\033[0m  文本转化{Global.configurator.target_language}完成-----------------------------------",
                        "\n",
                    )

                except Exception as e:
                    print(
                        "\033[1;33mWarning:\033[0m 文本转换出现问题！！将跳过该步，错误信息如下"
                    )
                    print(f"Error: {e}\n")

        # 将翻译结果写为文件
        output_path = Global.configurator.Output_Folder

        if Global.configurator.translation_project == "Mtool导出文件":
            File_Outputter.output_json_file(self, Global.cache_list, output_path)

        elif Global.configurator.translation_project == "T++导出文件":
            File_Outputter.output_excel_file(self, Global.cache_list, output_path)

        elif Global.configurator.translation_project == "Ainiee缓存文件":
            if Global.cache_list[0]["project_type"] == "Mtool":
                File_Outputter.output_json_file(self, Global.cache_list, output_path)
            else:
                File_Outputter.output_excel_file(self, Global.cache_list, output_path)

        print(
            "\033[1;32mSuccess:\033[0m  译文文件写入完成-----------------------------------",
            "\n",
        )

        # —————————————————————————————————————#全部翻译完成——————————————————————————————————————————
        Global.user_interface_prompter.signal.emit("翻译状态提示", "翻译完成", 0, 0, 0)
        print(
            "\n--------------------------------------------------------------------------------------"
        )
        print("\n\033[1;32mSuccess:\033[0m 已完成全部翻译任务，程序已经停止")
        print(
            "\n\033[1;32mSuccess:\033[0m 请检查译文文件，格式是否错误，存在错行，或者有空行等问题"
        )
        print(
            "\n-------------------------------------------------------------------------------------\n"
        )

    def Check_main(self):
        # ——————————————————————————————————————————配置信息初始化—————————————————————————————————————————
        Global.configurator.initialize_configuration_check()

        Global.request_limiter.initialize_limiter_check()

        # ——————————————————————————————————————————读取原文到缓存—————————————————————————————————————————
        # 读取文件
        Input_Folder = Global.configurator.Input_Folder
        if Global.configurator.translation_project == "Mtool导出文件":
            Global.cache_list = File_Reader.read_mtool_files(self, folder_path=Input_Folder)
        elif Global.configurator.translation_project == "T++导出文件":
            Global.cache_list = File_Reader.read_xlsx_files(self, folder_path=Input_Folder)

        # —————————————————————————————————————处理读取的文件——————————————————————————————————————————

        # 将浮点型，整数型文本内容变成字符型文本内容
        Cache_Manager.convert_source_text_to_str(self, Global.cache_list)

        # 统计已翻译文本的tokens总量，并根据不同项目修改翻译状态
        tokens_consume_all = Cache_Manager.count_tokens(self, Global.cache_list)

        # —————————————————————————————————————创建并发嵌入任务——————————————————————————————————————————

        # 根据tokens_all_consume与除以6090计算出需要请求的次数,并向上取整（除以6090是为了富余任务数）
        tasks_Num = int(math.ceil(tokens_consume_all / 7000))

        print("[DEBUG] 全部文本需要嵌入请求的次数是", tasks_Num)

        # 初始化一下界面提示器里面存储的相关变量
        Global.user_interface_prompter.translated_line_count = 0
        Global.user_interface_prompter.total_text_line_count = (
            Cache_Manager.count_translation_status_0(self, Global.cache_list)
        )

        # 测试用
        # api_requester_instance = Api_Requester()
        # api_requester_instance.Concurrent_request_Embeddings()

        # 创建线程池
        The_Max_workers = multiprocessing.cpu_count() * 4 + 1
        with concurrent.futures.ThreadPoolExecutor(The_Max_workers) as executor:
            # 创建实例
            api_requester_instance = Api_Requester()
            # 向线程池提交任务
            for i in range(tasks_Num):
                # 根据不同平台调用不同接口
                executor.submit(api_requester_instance.Concurrent_request_Embeddings)

            # 等待线程池任务完成
            executor.shutdown(wait=True)

        # 检查主窗口是否已经退出
        if Global.Running_status == 10:
            # 隐藏暂停按钮和取消按钮
            Global.window.Widget_Start_Translation_A.primaryButton_pause_translation.hide()
            Global.window.Widget_Start_Translation_A.primaryButton_cancel_translation.hide()
            return

        print(
            "\033[1;32mSuccess:\033[0m  全部文本检查编码完成-------------------------------------"
        )
        # —————————————————————————————————————开始检查，并整理需要重新翻译的文本——————————————————————————————————————————

        # 创建存储原文与译文的列表，方便复制粘贴，这里是两个空字符串，后面会被替换
        sentences = ["", ""]

        misaligned_text = {}  # 存储错行文本的字典

        # 创建存储每对翻译相似度计算过程日志的字符串
        similarity_log = ""
        log_count = 0
        count_error = 0  # 错误文本计数变量

        # 把等于3的翻译状态改为0
        for item in Global.cache_list:
            if item.get("translation_status") == 3:
                item["translation_status"] = 0

        # 统计翻译状态为0的文本数
        List_len = Cache_Manager.count_translation_status_0(self, Global.cache_list)

        for entry in Global.cache_list:
            translation_status = entry.get("translation_status")

            if translation_status == 0:

                # 将sentence[0]与sentence[1]转换成字符串数据，确保能够被语义相似度检查模型识别，防止数字型数据导致报错
                sentences[0] = str(entry["source_text"])
                sentences[1] = str(entry["translated_text"])

                # 输出sentence里的两个文本 和 语义相似度检查结果
                print("[INFO] 原文是：", sentences[0])
                print("[INFO] 译文是：", sentences[1])

                # 计算语义相似度----------------------------------------
                Semantic_similarity = entry["semantic_similarity"]
                print("[INFO] 语义相似度：", Semantic_similarity, "%")

                # 计算符号相似度----------------------------------------
                # 用正则表达式匹配原文与译文中的标点符号
                k_syms = re.findall(r"[。！？…♡♥=★♪]", sentences[0])
                v_syms = re.findall(r"[。！？…♡♥=★♪]", sentences[1])

                # 假如v_syms与k_syms都不为空
                if len(v_syms) != 0 and len(k_syms) != 0:
                    # 计算v_syms中的符号在k_syms中存在相同符号数量，再除以v_syms的符号总数，得到相似度
                    Symbolic_similarity = (
                        len([sym for sym in v_syms if sym in k_syms])
                        / len(v_syms)
                        * 100
                    )
                # 假如v_syms与k_syms都为空，即原文和译文都没有标点符号
                elif len(v_syms) == 0 and len(k_syms) == 0:
                    Symbolic_similarity = 1 * 100
                else:
                    Symbolic_similarity = 0

                print("[INFO] 符号相似度：", Symbolic_similarity, "%")

                # 计算字数相似度----------------------------------------
                # 计算k中的日文、中文,韩文，英文字母的个数
                Q, W, E, R = Response_Parser.count_japanese_chinese_korean(
                    self, sentences[0]
                )
                # 计算v中的日文、中文,韩文，英文字母的个数
                A, S, D, F = Response_Parser.count_japanese_chinese_korean(
                    self, sentences[1]
                )

                # 计算每个总字数
                len1 = Q + W + E + R
                len2 = A + S + D + F

                # 设定基准字数差距，暂时靠经验设定
                if len1 <= 25:
                    Base_word_count = 15
                else:
                    Base_word_count = 25

                # 计算字数差值
                Word_count_difference = abs((len1 - len2))
                if Word_count_difference > Base_word_count:
                    Word_count_difference = Base_word_count

                # 计算字数相差程度
                Word_count_similarity = (
                    1 - Word_count_difference / Base_word_count
                ) * 100
                print("[INFO] 字数相似度：", Word_count_similarity, "%")

                # 获取设定的权重
                Semantic_weight = (
                    Global.window.Widget_check.doubleSpinBox_semantic_weight.value()
                )
                Symbolic_weight = (
                    Global.window.Widget_check.doubleSpinBox_symbol_weight.value()
                )
                Word_count_weight = (
                    Global.window.Widget_check.doubleSpinBox_word_count_weight.value()
                )
                similarity_threshold = (
                    Global.window.Widget_check.spinBox_similarity_threshold.value()
                )

                # 计算总相似度
                similarity = (
                    Semantic_similarity * Semantic_weight
                    + Symbolic_similarity * Symbolic_weight
                    + Word_count_similarity * Word_count_weight
                )
                # 输出各权重值
                print(
                    "[INFO] 语义权重：",
                    Semantic_weight,
                    "符号权重：",
                    Symbolic_weight,
                    "字数权重：",
                    Word_count_weight,
                )

                # 如果语义相似度小于于等于阈值，需要重翻译
                if similarity <= similarity_threshold:
                    count_error = count_error + 1
                    print(
                        "[INFO] 总相似度结果：",
                        similarity,
                        "%，小于相似度阈值",
                        similarity_threshold,
                        "%，需要重翻译",
                    )
                    # 错误文本计数提醒
                    print("\033[1;33mWarning:\033[0m 当前错误文本数量：", count_error)
                    # 将错误文本存储到字典里
                    misaligned_text[sentences[0]] = sentences[1]

                # 检查通过,改变翻译状态为不需要翻译
                else:
                    entry["translation_status"] = 1
                    print("[INFO] 总相似度结果：", similarity, "%", "，不需要重翻译")

                # 创建格式化字符串，用于存储每对翻译相似度计算过程日志
                if log_count <= 10000:  # 如果log_count小于等于10000,避免太大
                    similarity_log = (
                        similarity_log
                        + "\n"
                        + "原文是："
                        + sentences[0]
                        + "\n"
                        + "译文是："
                        + sentences[1]
                        + "\n"
                        + "语义相似度："
                        + str(Semantic_similarity)
                        + "%"
                        + "\n"
                        + "符号相似度："
                        + str(Symbolic_similarity)
                        + "%"
                        + "\n"
                        + "字数相似度："
                        + str(Word_count_similarity)
                        + "%"
                        + "\n"
                        + "总相似度结果："
                        + str(similarity)
                        + "%"
                        + "\n"
                        + "语义权重："
                        + str(Semantic_weight)
                        + "，符号权重："
                        + str(Symbolic_weight)
                        + "，字数权重："
                        + str(Word_count_weight)
                        + "\n"
                        + "当前检查进度："
                        + str(round((log_count + 1) / List_len * 100, 2))
                        + "%"
                        + "\n"
                    )
                    log_count = log_count + 1

                # 输出遍历进度，转换成百分百进度
                print(
                    "[INFO] 当前检查进度：",
                    round((log_count) / List_len * 100, 2),
                    "% \n",
                )

        # 构建输出检查结果路径
        output_path = Global.configurator.Output_Folder
        folder_path = os.path.join(output_path, "misalignment_check_result")
        os.makedirs(folder_path, exist_ok=True)

        # 检查完毕，将错误文本字典写入json文件
        with open(
            os.path.join(folder_path, "misaligned_text.json"), "w", encoding="utf-8"
        ) as f:
            json.dump(misaligned_text, f, ensure_ascii=False, indent=4)

        # 将每对翻译相似度计算过程日志写入txt文件
        with open(os.path.join(folder_path, "log.txt"), "w", encoding="utf-8") as f:
            f.write(similarity_log)

        # ——————————————————————————————————————————配置信息初始化—————————————————————————————————————————
        Global.configurator.initialize_configuration()
        Global.request_limiter.initialize_limiter()

        # 初始化一下界面提示器里面存储的相关变量
        Global.user_interface_prompter.translated_line_count = 0
        Global.user_interface_prompter.total_text_line_count = (
            Cache_Manager.count_translation_status_0(self, Global.cache_list)
        )

        # —————————————————————————————————————开始重新翻译——————————————————————————————————————————

        # 记录循环翻译次数
        Number_of_iterations = 0

        # 计算需要翻译文本的数量
        count_not_Translate = Cache_Manager.count_translation_status_0(self, Global.cache_list)

        while count_not_Translate != 0:

            # 计算可并发任务总数
            if count_not_Translate % 1 == 0:
                tasks_Num = count_not_Translate // 1
            else:
                tasks_Num = count_not_Translate // 1 + 1

            # 创建线程池
            The_Max_workers = Global.configurator.thread_counts  # 获取线程数配置
            with concurrent.futures.ThreadPoolExecutor(The_Max_workers) as executor:
                # 创建实例
                api_requester_instance = Api_Requester()
                # 向线程池提交任务
                for i in range(tasks_Num):
                    # 根据不同平台调用不同接口
                    executor.submit(api_requester_instance.Concurrent_Request_Openai)

                # 等待线程池任务完成
                executor.shutdown(wait=True)

            # 检查主窗口是否已经退出
            if Global.Running_status == 10:
                return

            # 重新计算未翻译文本的数量
            count_not_Translate = Cache_Manager.count_and_update_translation_status_0_2(
                self, Global.cache_list
            )

            # 记录循环次数
            Number_of_iterations = Number_of_iterations + 1
            print(
                "\033[1;33mWarning:\033[0m 当前循环翻译次数：",
                Number_of_iterations,
                "次，到达最大循环次数5次后将退出翻译任务",
            )
            # 检查是否已经陷入死循环
            if Number_of_iterations == 5:
                print(
                    "\033[1;33mWarning:\033[0m 已达到最大循环次数，退出重翻任务，不影响后续使用-----------------------------------"
                )
                break

        print(
            "\n\033[1;32mSuccess:\033[0m  已重新翻译完成-----------------------------------"
        )

        # —————————————————————————————————————写入文件——————————————————————————————————————————
        # 将翻译结果写为文件
        output_path = Global.configurator.Output_Folder

        File_Outputter.output_translated_content(self, Global.cache_list, output_path)

        # —————————————————————————————————————全部翻译完成——————————————————————————————————————————
        print(
            "\n--------------------------------------------------------------------------------------"
        )
        print("\n\033[1;32mSuccess:\033[0m 已完成全部翻译任务，程序已经停止")
        print(
            "\n\033[1;32mSuccess:\033[0m 请检查译文文件，格式是否错误，存在错行，或者有空行等问题"
        )
        print(
            "\n-------------------------------------------------------------------------------------\n"
        )