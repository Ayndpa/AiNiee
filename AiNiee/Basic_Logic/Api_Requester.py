import json
import os
import threading
import numpy as np
from .Cache_Manager import Cache_Manager
from .File_Outputter import File_Outputter
from ..Global import Global
from .Request_Limiter import Request_Limiter
import time
from openai import OpenAI
import google.generativeai as genai
from .Response_Parser import Response_Parser


# 接口请求器
class Api_Requester:
    def __init__(self):
        pass

    # 整理发送内容（Openai）
    def organize_send_content_openai(self, source_text_dict):
        # 创建message列表，用于发送
        messages = []

        # 构建系统提示词
        prompt = Global.configurator.get_system_prompt()
        system_prompt = {"role": "system", "content": prompt}
        # print("[INFO] 当前系统提示词为", prompt,'\n')
        messages.append(system_prompt)

        # 构建原文与译文示例
        original_exmaple, translation_example = (
            Global.configurator.get_default_translation_example()
        )
        the_original_exmaple = {"role": "user", "content": original_exmaple}
        the_translation_example = {"role": "assistant", "content": translation_example}
        # print("[INFO]  已添加默认原文示例",original_exmaple)
        # print("[INFO]  已添加默认译文示例",translation_example)

        messages.append(the_original_exmaple)
        messages.append(the_translation_example)

        # 如果开启了译时提示字典功能，则添加新的原文与译文示例
        if Global.window.Interface23.checkBox2.isChecked():
            original_exmaple_2, translation_example_2 = (
                Global.configurator.build_prompt_dictionary(source_text_dict)
            )
            if original_exmaple_2 and translation_example_2:
                the_original_exmaple = {"role": "user", "content": original_exmaple_2}
                the_translation_example = {
                    "role": "assistant",
                    "content": translation_example_2,
                }
                messages.append(the_original_exmaple)
                messages.append(the_translation_example)
                print(
                    "[INFO]  检查到请求的原文中含有用户字典内容，已添加新的原文与译文示例"
                )
                print("[INFO]  已添加提示字典原文示例", original_exmaple_2)
                print("[INFO]  已添加提示字典译文示例", translation_example_2)

        # 如果提示词工程界面的用户翻译示例开关打开，则添加新的原文与译文示例
        if Global.window.Interface22.checkBox2.isChecked():
            original_exmaple_3, translation_example_3 = (
                Global.configurator.build_user_translation_example()
            )
            if original_exmaple_3 and translation_example_3:
                the_original_exmaple = {"role": "user", "content": original_exmaple_3}
                the_translation_example = {
                    "role": "assistant",
                    "content": translation_example_3,
                }
                messages.append(the_original_exmaple)
                messages.append(the_translation_example)
                print("[INFO]  检查到用户翻译示例开关打开，已添加新的原文与译文示例")
                print("[INFO]  已添加用户原文示例", original_exmaple_3)
                print("[INFO]  已添加用户译文示例", translation_example_3)

        # 如果开启了保留换行符功能
        if Global.configurator.preserve_line_breaks_toggle and Global.Running_status == 6:
            print("[INFO] 你开启了保留换行符功能，正在进行替换", "\n")
            source_text_dict = Cache_Manager.replace_special_characters(
                self, source_text_dict, "替换"
            )

        # 如果开启译前替换字典功能，则根据用户字典进行替换
        if Global.window.Interface21.checkBox1.isChecked():
            print("[INFO] 你开启了译前替换字典功能，正在进行替换", "\n")
            source_text_dict = Global.configurator.replace_strings_dictionary(
                source_text_dict
            )

        # 将原文本字典转换成JSON格式的字符串，方便发送
        source_text_str = json.dumps(source_text_dict, ensure_ascii=False)

        # 构建需要翻译的文本
        Original_text = {"role": "user", "content": source_text_str}
        messages.append(Original_text)

        return messages, source_text_str

    # 并发接口请求（Openai）
    def Concurrent_Request_Openai(self):
        try:  # 方便排查子线程bug

            # ——————————————————————————————————————————截取需要翻译的原文本——————————————————————————————————————————
            Global.lock1.acquire()  # 获取锁
            # 获取设定行数的文本，并修改缓存文件里的翻译状态为2，表示正在翻译中
            rows = Global.configurator.text_line_counts
            source_text_list = Cache_Manager.process_dictionary_data(
                self, rows, Global.cache_list
            )
            Global.lock1.release()  # 释放锁

            # ——————————————————————————————————————————转换原文本的格式——————————————————————————————————————————
            # 将原文本列表改变为请求格式
            source_text_dict, row_count = Cache_Manager.create_dictionary_from_list(
                self, source_text_list
            )

            # ——————————————————————————————————————————整合发送内容——————————————————————————————————————————
            messages, source_text_str = Api_Requester.organize_send_content_openai(
                self, source_text_dict
            )

            # ——————————————————————————————————————————检查tokens发送限制——————————————————————————————————————————
            # 计算请求的tokens预计花费
            request_tokens_consume = Request_Limiter.num_tokens_from_messages(
                self, messages
            )
            # 计算回复的tokens预计花费，只计算发送的文本，不计算提示词与示例，可以大致得出
            Original_text = [
                {"role": "user", "content": source_text_str}
            ]  # 需要拿列表来包一层，不然计算时会出错
            completion_tokens_consume = Request_Limiter.num_tokens_from_messages(
                self, Original_text
            )

            # 如果没有取消
            if (
                request_tokens_consume >= Global.request_limiter.max_tokens
                and Global.Running_status == 6
            ):
                print("\033[1;31mError:\033[0m 该条消息总tokens数大于单条消息最大数量")
                print("\033[1;31mError:\033[0m 该条消息取消任务，进行拆分翻译")
                return

            # ——————————————————————————————————————————开始循环请求，直至成功或失败——————————————————————————————————————————
            start_time = time.time()
            timeout = 850  # 设置超时时间为x秒
            request_errors_count = 0  # 设置请求错误次数限制
            Wrong_answer_count = 0  # 设置错误回复次数限制
            model_degradation = False  # 模型退化检测

            while 1:
                # 检查是否取消
                if Global.Running_status == 10:
                    return
                # 检查是否暂停
                if Global.Running_status == 1011:
                    time.sleep(1)
                    continue

                # 检查子线程运行是否超时---------------------------------
                if time.time() - start_time > timeout:
                    print(
                        "\033[1;31mError:\033[0m 子线程执行任务已经超时，将暂时取消本次任务"
                    )
                    break

                # 检查是否符合速率限制---------------------------------
                if Global.request_limiter.RPM_and_TPM_limit(request_tokens_consume):

                    print("[INFO] 已发送请求,正在等待AI回复中-----------------------")
                    print(
                        "[INFO] 请求与回复的tokens数预计值是：",
                        request_tokens_consume + completion_tokens_consume,
                    )
                    print("[INFO] 当前发送的原文文本：\n", source_text_str)

                    # ——————————————————————————————————————————发送会话请求——————————————————————————————————————————
                    # 记录开始请求时间
                    Start_request_time = time.time()

                    # 获取AI的参数设置
                    temperature, top_p, presence_penalty, frequency_penalty = (
                        Global.configurator.get_model_parameters()
                    )
                    # 如果上一次请求出现模型退化，更改参数
                    if model_degradation:
                        frequency_penalty = 0.2

                    # 获取apikey
                    openai_apikey = Global.configurator.get_apikey()
                    # 获取请求地址
                    openai_base_url = Global.configurator.openai_base_url
                    # 创建openai客户端
                    openaiclient = OpenAI(
                        api_key=openai_apikey, base_url=openai_base_url
                    )
                    # 发送对话请求
                    try:
                        # 如果开启了回复josn格式的功能和可以开启该功能的模型
                        if (Global.configurator.response_json_format_toggle) and (
                            Global.configurator.model_type == "gpt-3.5-turbo-0125"
                            or Global.configurator.model_type == "gpt-4-turbo-preview"
                        ):
                            print("[INFO] 已开启强制回复josn格式功能")
                            response = openaiclient.chat.completions.create(
                                model=Global.configurator.model_type,
                                messages=messages,
                                temperature=temperature,
                                top_p=top_p,
                                presence_penalty=presence_penalty,
                                frequency_penalty=frequency_penalty,
                                response_format={"type": "json_object"},
                            )
                        else:
                            response = openaiclient.chat.completions.create(
                                model=Global.configurator.model_type,
                                messages=messages,
                                temperature=temperature,
                                top_p=top_p,
                                presence_penalty=presence_penalty,
                                frequency_penalty=frequency_penalty,
                            )

                    # 抛出错误信息
                    except Exception as e:
                        print(
                            "\033[1;31mError:\033[0m 进行请求时出现问题！！！错误信息如下"
                        )
                        print(f"Error: {e}\n")

                        # 请求错误计次
                        request_errors_count = request_errors_count + 1
                        # 如果错误次数过多，就取消任务
                        if request_errors_count >= 6:
                            print(
                                "\033[1;31m[ERROR]\033[0m 请求发生错误次数过多，该线程取消任务！"
                            )
                            break

                        # 处理完毕，再次进行请求
                        continue

                    # ——————————————————————————————————————————收到回复，并截取回复内容中的文本内容 ————————————————————————————————————————
                    # 计算AI回复花费的时间
                    response_time = time.time()
                    Request_consumption_time = round(
                        response_time - Start_request_time, 2
                    )

                    # 计算本次请求的花费的tokens
                    try:  # 因为有些中转网站不返回tokens消耗
                        prompt_tokens_used = int(
                            response.usage.prompt_tokens
                        )  # 本次请求花费的tokens
                    except Exception as e:
                        prompt_tokens_used = 0
                    try:
                        completion_tokens_used = int(
                            response.usage.completion_tokens
                        )  # 本次回复花费的tokens
                    except Exception as e:
                        completion_tokens_used = 0

                    # 提取回复的文本内容
                    response_content = response.choices[0].message.content

                    print("\n")
                    print("[INFO] 已成功接受到AI的回复-----------------------")
                    print(
                        "[INFO] 该次请求已消耗等待时间：",
                        Request_consumption_time,
                        "秒",
                    )
                    print(
                        "[INFO] 本次请求与回复花费的总tokens是：",
                        prompt_tokens_used + completion_tokens_used,
                    )
                    print("[INFO] AI回复的文本内容：\n", response_content, "\n", "\n")

                    # ——————————————————————————————————————————对AI回复内容进行各种处理和检查——————————————————————————————————————————
                    # 处理回复内容
                    response_content = Response_Parser.adjust_string(
                        self, response_content
                    )

                    # 检查回复内容
                    check_result, error_content = (
                        Response_Parser.check_response_content(
                            self, response_content, source_text_dict
                        )
                    )

                    # 如果没有出现错误
                    if check_result:
                        # 转化为字典格式
                        response_dict = json.loads(
                            response_content
                        )  # 注意转化为字典的数字序号key是字符串类型

                        # 如果开启了保留换行符功能
                        if Global.configurator.preserve_line_breaks_toggle and Global.Running_status == 6:
                            response_dict = Cache_Manager.replace_special_characters(
                                self, response_dict, "还原"
                            )

                        # 录入缓存文件
                        Global.lock1.acquire()  # 获取锁
                        Cache_Manager.update_cache_data(
                            self, Global.cache_list, source_text_list, response_dict
                        )
                        Global.lock1.release()  # 释放锁

                        # 如果开启自动备份,则自动备份缓存文件
                        if (
                            Global.window.Widget_start_translation.B_settings.checkBox_switch.isChecked()
                        ):
                            Global.lock3.acquire()  # 获取锁

                            # 创建存储缓存文件的文件夹，如果路径不存在，创建文件夹
                            output_path = os.path.join(
                                Global.configurator.Output_Folder, "cache"
                            )
                            os.makedirs(output_path, exist_ok=True)
                            # 输出备份
                            File_Outputter.output_cache_file(
                                self, Global.cache_list, output_path
                            )
                            Global.lock3.release()  # 释放锁

                        Global.lock2.acquire()  # 获取锁

                        # 如果是进行平时的翻译任务
                        if Global.Running_status == 6:
                            # 计算进度信息
                            progress = (
                                (
                                    Global.user_interface_prompter.translated_line_count
                                    + row_count
                                )
                                / Global.user_interface_prompter.total_text_line_count
                                * 100
                            )
                            progress = round(progress, 1)

                            # 更改UI界面信息,注意，传入的数值类型分布是字符型与整数型，小心浮点型混入
                            Global.user_interface_prompter.signal.emit(
                                "更新翻译界面数据",
                                "翻译成功",
                                row_count,
                                prompt_tokens_used,
                                completion_tokens_used,
                            )

                        # 如果进行的是错行检查任务，使用不同的计算方法
                        elif Global.Running_status == 7:
                            Global.user_interface_prompter.translated_line_count = (
                                Global.user_interface_prompter.translated_line_count
                                + row_count
                            )
                            progress = (
                                Global.user_interface_prompter.translated_line_count
                                / Global.user_interface_prompter.total_text_line_count
                                * 100
                            )
                            progress = round(progress, 1)

                        print(
                            f"\n--------------------------------------------------------------------------------------"
                        )
                        print(
                            f"\n\033[1;32mSuccess:\033[0m AI回复内容检查通过！！！已翻译完成{progress}%"
                        )
                        print(
                            f"\n--------------------------------------------------------------------------------------\n"
                        )
                        Global.lock2.release()  # 释放锁

                        break

                    # 如果出现回复错误
                    else:

                        # 更改UI界面信息
                        Global.lock2.acquire()  # 获取锁
                        # 如果是进行平时的翻译任务
                        if Global.Running_status == 6:
                            Global.user_interface_prompter.signal.emit(
                                "更新翻译界面数据",
                                "翻译失败",
                                row_count,
                                prompt_tokens_used,
                                completion_tokens_used,
                            )
                        Global.lock2.release()  # 释放锁
                        print(
                            "\033[1;33mWarning:\033[0m AI回复内容存在问题:",
                            error_content,
                            "\n",
                        )
                        # 检查一下是不是模型退化
                        if error_content == "AI回复内容出现高频词,并重新翻译":
                            print(
                                "\033[1;33mWarning:\033[0m 下次请求将修改参数，回避高频词输出",
                                "\n",
                            )
                            model_degradation = True

                        # 错误回复计次
                        Wrong_answer_count = Wrong_answer_count + 1
                        print(
                            "\033[1;33mWarning:\033[0m AI回复内容格式错误次数:",
                            Wrong_answer_count,
                            "到达2次后将该段文本进行拆分翻译\n",
                        )
                        # 检查回答错误次数，如果达到限制，则跳过该句翻译。
                        if Wrong_answer_count >= 2:
                            print(
                                "\033[1;33mWarning:\033[0m 错误次数已经达限制,将该段文本进行拆分翻译！\n"
                            )
                            break

                        # 进行下一次循环
                        time.sleep(3)
                        continue

        # 子线程抛出错误信息
        except Exception as e:
            print("\033[1;31mError:\033[0m 子线程运行出现问题！错误信息如下")
            print(f"Error: {e}\n")
            return

    # 整理发送内容（Google）
    def organize_send_content_google(self, source_text_dict):
        # 创建message列表，用于发送
        messages = []

        # 获取系统提示词
        prompt = Global.configurator.get_system_prompt()

        # 获取原文与译文示例
        original_exmaple, translation_example = (
            Global.configurator.get_default_translation_example()
        )

        # 构建系统提示词与默认示例
        messages.append(
            {"role": "user", "parts": prompt + "\n###\n" + original_exmaple}
        )
        messages.append({"role": "model", "parts": translation_example})

        # 如果开启了译时提示字典功能，则添加新的原文与译文示例
        if Global.window.Interface23.checkBox2.isChecked():
            original_exmaple_2, translation_example_2 = (
                Global.configurator.build_prompt_dictionary(source_text_dict)
            )
            if original_exmaple_2 and translation_example_2:
                the_original_exmaple = {"role": "user", "parts": original_exmaple_2}
                the_translation_example = {
                    "role": "model",
                    "parts": translation_example_2,
                }
                messages.append(the_original_exmaple)
                messages.append(the_translation_example)
                print(
                    "[INFO]  检查到请求的原文中含有用户字典内容，已添加新的原文与译文示例"
                )
                print("[INFO]  已添加提示字典原文示例", original_exmaple_2)
                print("[INFO]  已添加提示字典译文示例", translation_example_2)

        # 如果提示词工程界面的用户翻译示例开关打开，则添加新的原文与译文示例
        if Global.window.Interface22.checkBox2.isChecked():
            original_exmaple_3, translation_example_3 = (
                Global.configurator.build_user_translation_example()
            )
            if original_exmaple_3 and translation_example_3:
                the_original_exmaple = {"role": "user", "parts": original_exmaple_3}
                the_translation_example = {
                    "role": "model",
                    "parts": translation_example_3,
                }
                messages.append(the_original_exmaple)
                messages.append(the_translation_example)
                print("[INFO]  检查到用户翻译示例开关打开，已添加新的原文与译文示例")
                print("[INFO]  已添加用户原文示例", original_exmaple_3)
                print("[INFO]  已添加用户译文示例", translation_example_3)

        # 如果开启了保留换行符功能
        if Global.configurator.preserve_line_breaks_toggle and Global.Running_status == 6:
            print("[INFO] 你开启了保留换行符功能，正在进行替换", "\n")
            source_text_dict = Cache_Manager.replace_special_characters(
                self, source_text_dict, "替换"
            )

        # 如果开启译前替换字典功能，则根据用户字典进行替换
        if Global.window.Interface21.checkBox1.isChecked():
            print("[INFO] 你开启了译前替换字典功能，正在进行替换", "\n")
            source_text_dict = Global.configurator.replace_strings_dictionary(
                source_text_dict
            )

        # 将原文本字典转换成JSON格式的字符串，方便发送
        source_text_str = json.dumps(source_text_dict, ensure_ascii=False)

        # 构建需要翻译的文本
        Original_text = {"role": "user", "parts": source_text_str}
        messages.append(Original_text)

        return messages, source_text_str

    # 并发接口请求（Google）
    def Concurrent_Request_Google(self):
        try:  # 方便排查子线程bug

            # ——————————————————————————————————————————截取需要翻译的原文本——————————————————————————————————————————
            Global.lock1.acquire()  # 获取锁
            # 获取设定行数的文本，并修改缓存文件里的翻译状态为2，表示正在翻译中
            rows = Global.configurator.text_line_counts
            source_text_list = Cache_Manager.process_dictionary_data(
                self, rows, Global.cache_list
            )
            Global.lock1.release()  # 释放锁

            # ——————————————————————————————————————————转换原文本的格式——————————————————————————————————————————
            # 将原文本列表改变为请求格式
            source_text_dict, row_count = Cache_Manager.create_dictionary_from_list(
                self, source_text_list
            )

            # ——————————————————————————————————————————整合发送内容——————————————————————————————————————————
            messages, source_text_str = Api_Requester.organize_send_content_google(
                self, source_text_dict
            )

            # ——————————————————————————————————————————检查tokens发送限制——————————————————————————————————————————
            # 计算请求的tokens预计花费
            request_tokens_consume = Request_Limiter.num_tokens_from_messages(
                self, messages
            )
            # 计算回复的tokens预计花费，只计算发送的文本，不计算提示词与示例，可以大致得出
            Original_text = [
                {"role": "user", "content": source_text_str}
            ]  # 需要拿列表来包一层，不然计算时会出错
            completion_tokens_consume = Request_Limiter.num_tokens_from_messages(
                self, Original_text
            )

            if (
                request_tokens_consume >= Global.request_limiter.max_tokens
                and Global.Running_status == 6
            ):
                print(
                    "\033[1;33mWarning:\033[0m 该条消息总tokens数大于单条消息最大数量"
                )
                print("\033[1;33mWarning:\033[0m 该条消息取消任务，进行拆分翻译")
                return

            # ——————————————————————————————————————————开始循环请求，直至成功或失败——————————————————————————————————————————
            start_time = time.time()
            timeout = 850  # 设置超时时间为x秒
            request_errors_count = 0  # 设置请求错误次数限制
            Wrong_answer_count = 0  # 设置错误回复次数限制

            while 1:
                # 检查是否取消
                if Global.Running_status == 10:
                    return
                # 检查是否暂停
                if Global.Running_status == 1011:
                    time.sleep(1)
                    continue

                # 检查子线程运行是否超时---------------------------------
                if time.time() - start_time > timeout:
                    print(
                        "\033[1;31mError:\033[0m 子线程执行任务已经超时，将暂时取消本次任务"
                    )
                    break

                # 检查是否符合速率限制---------------------------------
                if Global.request_limiter.RPM_and_TPM_limit(request_tokens_consume):

                    print("[INFO] 已发送请求,正在等待AI回复中-----------------------")
                    print(
                        "[INFO] 请求与回复的tokens数预计值是：",
                        request_tokens_consume + completion_tokens_consume,
                    )
                    print("[INFO] 当前发送的原文文本：\n", source_text_str)

                    # ——————————————————————————————————————————发送会话请求——————————————————————————————————————————
                    # 记录开始请求时间
                    Start_request_time = time.time()

                    # 设置AI的参数
                    generation_config = {
                        "temperature": 0,
                        "top_p": 1,
                        "top_k": 1,
                        "max_output_tokens": 2048,  # 最大输出，pro最大输出是2048
                    }

                    # 调整安全限制
                    safety_settings = [
                        {
                            "category": "HARM_CATEGORY_HARASSMENT",
                            "threshold": "BLOCK_NONE",
                        },
                        {
                            "category": "HARM_CATEGORY_HATE_SPEECH",
                            "threshold": "BLOCK_NONE",
                        },
                        {
                            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                            "threshold": "BLOCK_NONE",
                        },
                        {
                            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                            "threshold": "BLOCK_NONE",
                        },
                    ]

                    # 获取apikey
                    apikey = Global.configurator.get_apikey()
                    genai.configure(api_key=apikey)

                    # 设置对话模型及参数
                    model = genai.GenerativeModel(
                        model_name=Global.configurator.model_type,
                        generation_config=generation_config,
                        safety_settings=safety_settings,
                    )

                    # 发送对话请求
                    try:
                        response = model.generate_content(messages)

                    # 抛出错误信息
                    except Exception as e:
                        print(
                            "\033[1;31mError:\033[0m 进行请求时出现问题！！！错误信息如下"
                        )
                        print(f"Error: {e}\n")

                        # 请求错误计次
                        request_errors_count = request_errors_count + 1
                        # 如果错误次数过多，就取消任务
                        if request_errors_count >= 6:
                            print(
                                "\033[1;31m[ERROR]\033[0m 请求发生错误次数过多，该线程取消任务！"
                            )
                            break

                        # 处理完毕，再次进行请求
                        continue

                    # ——————————————————————————————————————————收到回复，并截取回复内容中的文本内容 ————————————————————————————————————————
                    # 计算AI回复花费的时间
                    response_time = time.time()
                    Request_consumption_time = round(
                        response_time - Start_request_time, 2
                    )

                    # 计算本次请求的花费的tokens
                    prompt_tokens_used = int(request_tokens_consume)
                    completion_tokens_used = int(completion_tokens_consume)

                    # 提取回复的文本内容
                    try:
                        response_content = response.text
                    # 抛出错误信息
                    except Exception as e:
                        print(
                            "\033[1;31mError:\033[0m 提取文本时出现错误！！！运行的错误信息如下"
                        )
                        print(f"Error: {e}\n")
                        print("接口返回的错误信息如下")
                        print(response.prompt_feedback)
                        # 处理完毕，再次进行请求
                        continue

                    print("\n")
                    print("[INFO] 已成功接受到AI的回复-----------------------")
                    print(
                        "[INFO] 该次请求已消耗等待时间：",
                        Request_consumption_time,
                        "秒",
                    )
                    print(
                        "[INFO] 本次请求与回复花费的总tokens是：",
                        prompt_tokens_used + completion_tokens_used,
                    )
                    print("[INFO] AI回复的文本内容：\n", response_content, "\n", "\n")

                    # ——————————————————————————————————————————对AI回复内容进行各种处理和检查——————————————————————————————————————————
                    # 处理回复内容
                    response_content = Response_Parser.adjust_string(
                        self, response_content
                    )

                    # 检查回复内容
                    check_result, error_content = (
                        Response_Parser.check_response_content(
                            self, response_content, source_text_dict
                        )
                    )

                    # 如果没有出现错误
                    if check_result:
                        # 转化为字典格式
                        response_dict = json.loads(
                            response_content
                        )  # 注意转化为字典的数字序号key是字符串类型

                        # 如果开启了保留换行符功能
                        if Global.configurator.preserve_line_breaks_toggle and Global.Running_status == 6:
                            response_dict = Cache_Manager.replace_special_characters(
                                self, response_dict, "还原"
                            )

                        # 录入缓存文件
                        Global.lock1.acquire()  # 获取锁
                        Cache_Manager.update_cache_data(
                            self, Global.cache_list, source_text_list, response_dict
                        )
                        Global.lock1.release()  # 释放锁

                        # 如果开启自动备份,则自动备份缓存文件
                        if (
                            Global.window.Widget_start_translation.B_settings.checkBox_switch.isChecked()
                        ):
                            Global.lock3.acquire()  # 获取锁

                            # 创建存储缓存文件的文件夹，如果路径不存在，创建文件夹
                            output_path = os.path.join(
                                Global.configurator.Output_Folder, "cache"
                            )
                            os.makedirs(output_path, exist_ok=True)
                            # 输出备份
                            File_Outputter.output_cache_file(
                                self, Global.cache_list, output_path
                            )
                            Global.lock3.release()  # 释放锁

                        Global.lock2.acquire()  # 获取锁
                        # 计算进度信息
                        progress = (
                            (
                                Global.user_interface_prompter.translated_line_count
                                + row_count
                            )
                            / Global.user_interface_prompter.total_text_line_count
                            * 100
                        )
                        progress = round(progress, 1)

                        # 更改UI界面信息,注意，传入的数值类型分布是字符型与整数型，小心浮点型混入
                        Global.user_interface_prompter.signal.emit(
                            "更新翻译界面数据",
                            "翻译成功",
                            row_count,
                            prompt_tokens_used,
                            completion_tokens_used,
                        )
                        print(
                            f"\n--------------------------------------------------------------------------------------"
                        )
                        print(
                            f"\n\033[1;32mSuccess:\033[0m AI回复内容检查通过！！！已翻译完成{progress}%"
                        )
                        print(
                            f"\n--------------------------------------------------------------------------------------\n"
                        )

                        Global.lock2.release()  # 释放锁

                        break

                    # 如果出现回复错误
                    else:
                        # 更改UI界面信息
                        Global.lock2.acquire()  # 获取锁
                        # 更改UI界面信息,注意，传入的数值类型分布是字符型与整数型，小心浮点型混入
                        Global.user_interface_prompter.signal.emit(
                            "更新翻译界面数据",
                            "翻译失败",
                            row_count,
                            prompt_tokens_used,
                            completion_tokens_used,
                        )
                        Global.lock2.release()  # 释放锁
                        print(
                            "\033[1;33mWarning:\033[0m AI回复内容存在问题:",
                            error_content,
                            "\n",
                        )

                        # 错误回复计次
                        Wrong_answer_count = Wrong_answer_count + 1
                        print(
                            "\033[1;33mWarning:\033[0m AI回复内容格式错误次数:",
                            Wrong_answer_count,
                            "到达2次后将该段文本进行拆分翻译\n",
                        )
                        # 检查回答错误次数，如果达到限制，则跳过该句翻译。
                        if Wrong_answer_count >= 2:
                            print(
                                "\033[1;33mWarning:\033[0m 错误次数已经达限制,将该段文本进行拆分翻译！\n"
                            )
                            break

                        # 进行下一次循环
                        time.sleep(1)
                        continue

        # 子线程抛出错误信息
        except Exception as e:
            print("\033[1;31mError:\033[0m 子线程运行出现问题！错误信息如下")
            print(f"Error: {e}\n")
            return

    # 并发嵌入请求
    def Concurrent_request_Embeddings(self):
        try:  # 方便排查子线程bug
            # ——————————————————————————————————————————提取需要嵌入的翻译对——————————————————————————————————————————
            Global.lock1.acquire()  # 获取锁
            accumulated_tokens, source_texts, translated_texts, text_index_list = (
                Cache_Manager.process_tokens(Global.cache_list, 7500)
            )
            Global.lock1.release()  # 释放锁

            # 计算一下文本长度
            text_len = len(source_texts)

            # 检查一下返回值是否为空，如果为空则表示已经嵌入完了
            if accumulated_tokens == 0 or text_len == 0:
                return

            # ——————————————————————————————————————————整合发送内容——————————————————————————————————————————
            # 构建发送文本列表，长度为end - start的两倍，前半部分为原文，后半部分为译文
            input_txt = []
            for i in range(text_len):
                input_txt.append(source_texts[i])
            for i in range(text_len):
                input_txt.append(translated_texts[i])

            # ——————————————————————————————————————————开始循环请求，直至成功或失败——————————————————————————————————————————
            while 1:
                # 检查是否取消
                if Global.Running_status == 10:
                    return
                # 检查是否暂停
                if Global.Running_status == 1011:
                    time.sleep(1)
                    continue

                # 检查是否符合速率限制---------------------------------
                if Global.request_limiter.RPM_and_TPM_limit(accumulated_tokens):

                    # ————————————————————————————————————————发送请求————————————————————————————————————————
                    # 获取apikey
                    openai_apikey = Global.configurator.get_apikey()
                    # 获取请求地址
                    openai_base_url = Global.configurator.openai_base_url
                    # 创建openai客户端
                    openaiclient = OpenAI(
                        api_key=openai_apikey, base_url=openai_base_url
                    )
                    try:
                        print(
                            "[INFO] 已发送文本嵌入请求-------------------------------------"
                        )
                        print("[INFO] 请求内容长度是：", len(input_txt))
                        print("[INFO] 已发送请求，请求内容是：", input_txt, "\n", "\n")
                        response = openaiclient.embeddings.create(
                            input=input_txt, model="text-embedding-ada-002"
                        )

                    except Exception as e:
                        print("\033[1;33m线程ID:\033[0m ", threading.get_ident())
                        print("\033[1;31mError:\033[0m api请求出现问题！错误信息如下")
                        print(f"Error: {e}\n")

                        # 等待五秒再次请求
                        print("\033[1;33m线程ID:\033[0m 该任务五秒后再次请求")
                        time.sleep(5)

                        continue  # 处理完毕，再次进行请求

                    # ————————————————————————————————————————处理回复————————————————————————————————————————

                    print("[INFO] 已收到回复--------------------------------------")
                    print("[INFO] 正在计算语义相似度并录入缓存中")

                    # 计算相似度
                    Semantic_similarity_list = []
                    for i in range(text_len):
                        # 计算获取原文编码的索引位置，并获取
                        Original_Index = i
                        # openai返回的嵌入值是存储在data列表的字典元素里，在字典元素里以embedding为关键字，所以才要改变data的索引值
                        Original_Embeddings = response.data[Original_Index].embedding

                        # 计算获取译文编码的索引位置，并获取
                        Translation_Index = i + text_len
                        # openai返回的嵌入值是存储在data列表的字典元素里，在字典元素里以embedding为关键字，所以才要改变data的索引值
                        Translation_Embeddings = response.data[
                            Translation_Index
                        ].embedding

                        # 计算每对翻译语义相似度
                        similarity_score = np.dot(
                            Original_Embeddings, Translation_Embeddings
                        )
                        Semantic_similarity_list.append(
                            (similarity_score - 0.75) / (1 - 0.75) * 150
                        )

                    Global.lock1.acquire()  # 获取锁
                    Global.user_interface_prompter.translated_line_count = (
                        Global.user_interface_prompter.translated_line_count + text_len
                    )
                    progress = (
                        Global.user_interface_prompter.translated_line_count
                        / Global.user_interface_prompter.total_text_line_count
                        * 100
                    )
                    progress = round(progress, 1)
                    Cache_Manager.update_vector_distance(
                        Global.cache_list, text_index_list, Semantic_similarity_list
                    )
                    print("[INFO] 已计算语义相似度并存储", "\n", "\n")
                    Global.lock1.release()  # 释放锁

                    # ————————————————————————————————————————结束循环，并结束子线程————————————————————————————————————————
                    print(
                        f"\n--------------------------------------------------------------------------------------"
                    )
                    print(
                        f"\n\033[1;32mSuccess:\033[0m 嵌入编码已完成：{progress}%             "
                    )
                    print(
                        f"\n--------------------------------------------------------------------------------------\n"
                    )
                    break

        # 子线程抛出错误信息
        except Exception as e:
            print("\033[1;33m线程ID:\033[0m ", threading.get_ident())
            print("\033[1;31mError:\033[0m 线程出现问题！错误信息如下")
            print(f"Error: {e}\n")
            return

    # 整理发送内容（sakura）
    def organize_send_content_Sakura(self, source_text_dict):
        # 创建message列表，用于发送
        messages = []

        # 构建系统提示词
        system_prompt = {
            "role": "system",
            "content": "你是一个轻小说翻译模型，可以流畅通顺地以日本轻小说的风格将日文翻译成简体中文，并联系上下文正确使用人称代词，不擅自添加原文中没有的代词。",
        }
        # print("[INFO] 当前系统提示词为", prompt,'\n')
        messages.append(system_prompt)

        # 0.8模型不支持下面功能
        if Global.configurator.model_type != "Sakura-13B-LNovel-v0.8":

            prompt = "将下面的日文文本翻译成中文："

            # 构建原文与译文示例
            original_exmaple, translation_example = (
                Global.configurator.get_default_translation_example()
            )
            the_original_exmaple = {
                "role": "user",
                "content": prompt + original_exmaple,
            }
            the_translation_example = {
                "role": "assistant",
                "content": translation_example,
            }
            # print("[INFO]  已添加默认原文示例",original_exmaple)
            # print("[INFO]  已添加默认译文示例",translation_example)

            # messages.append(the_original_exmaple)
            # messages.append(the_translation_example)

            # 如果开启了译时提示字典功能，则添加新的原文与译文示例
            if Global.window.Interface23.checkBox2.isChecked():
                original_exmaple_2, translation_example_2 = (
                    Global.configurator.build_prompt_dictionary(source_text_dict)
                )
                if original_exmaple_2 and translation_example_2:
                    the_original_exmaple = {
                        "role": "user",
                        "content": prompt + original_exmaple_2,
                    }
                    the_translation_example = {
                        "role": "assistant",
                        "content": translation_example_2,
                    }
                    messages.append(the_original_exmaple)
                    messages.append(the_translation_example)
                    print(
                        "[INFO]  检查到请求的原文中含有用户字典内容，已添加新的原文与译文示例"
                    )
                    print("[INFO]  已添加提示字典原文示例", original_exmaple_2)
                    print("[INFO]  已添加提示字典译文示例", translation_example_2)

            # 如果提示词工程界面的用户翻译示例开关打开，则添加新的原文与译文示例
            if Global.window.Interface22.checkBox2.isChecked():
                original_exmaple_3, translation_example_3 = (
                    Global.configurator.build_user_translation_example()
                )
                if original_exmaple_3 and translation_example_3:
                    the_original_exmaple = {
                        "role": "user",
                        "content": prompt + original_exmaple_3,
                    }
                    the_translation_example = {
                        "role": "assistant",
                        "content": translation_example_3,
                    }
                    messages.append(the_original_exmaple)
                    messages.append(the_translation_example)
                    print(
                        "[INFO]  检查到用户翻译示例开关打开，已添加新的原文与译文示例"
                    )
                    print("[INFO]  已添加用户原文示例", original_exmaple_3)
                    print("[INFO]  已添加用户译文示例", translation_example_3)

        # 如果开启了保留换行符功能
        if Global.configurator.preserve_line_breaks_toggle and Global.Running_status == 6:
            print("[INFO] 你开启了保留换行符功能，正在进行替换", "\n")
            source_text_dict = Cache_Manager.replace_special_characters(
                self, source_text_dict, "替换"
            )

        # 如果开启译前替换字典功能，则根据用户字典进行替换
        if Global.window.Interface21.checkBox1.isChecked():
            print("[INFO] 你开启了译前替换字典功能，正在进行替换", "\n")
            source_text_dict = Global.configurator.replace_strings_dictionary(
                source_text_dict
            )

        # 将原文本字典转换成raw格式的字符串，方便发送
        source_text_str_raw = self.convert_dict_to_raw_str(source_text_dict)

        # 处理全角数字
        source_text_str_raw = self.convert_fullwidth_to_halfwidth(source_text_str_raw)

        # 构建需要翻译的文本
        prompt = "将下面的日文文本翻译成中文："
        Original_text = {"role": "user", "content": prompt + source_text_str_raw}
        messages.append(Original_text)

        return messages, source_text_str_raw

    # 并发接口请求（sakura）
    def Concurrent_Request_Sakura(self):
        try:  # 方便排查子线程bug

            # ——————————————————————————————————————————截取需要翻译的原文本——————————————————————————————————————————
            Global.lock1.acquire()  # 获取锁
            # 获取设定行数的文本，并修改缓存文件里的翻译状态为2，表示正在翻译中
            rows = Global.configurator.text_line_counts
            source_text_list = Cache_Manager.process_dictionary_data(
                self, rows, Global.cache_list
            )
            Global.lock1.release()  # 释放锁

            # ——————————————————————————————————————————转换原文本的格式——————————————————————————————————————————
            # 将原文本列表改变为请求格式
            source_text_dict, row_count = Cache_Manager.create_dictionary_from_list(
                self, source_text_list
            )

            # ——————————————————————————————————————————整合发送内容——————————————————————————————————————————
            messages, source_text_str = Api_Requester.organize_send_content_Sakura(
                self, source_text_dict
            )

            # ——————————————————————————————————————————检查tokens发送限制——————————————————————————————————————————
            # 计算请求的tokens预计花费
            request_tokens_consume = Request_Limiter.num_tokens_from_messages(
                self, messages
            )  # 加上2%的修正系数
            # 计算回复的tokens预计花费，只计算发送的文本，不计算提示词与示例，可以大致得出
            Original_text = [
                {"role": "user", "content": source_text_str}
            ]  # 需要拿列表来包一层，不然计算时会出错
            completion_tokens_consume = Request_Limiter.num_tokens_from_messages(
                self, Original_text
            )  # 加上2%的修正系数

            if (
                request_tokens_consume >= Global.request_limiter.max_tokens
                and Global.Running_status == 6
            ):
                print("\033[1;31mError:\033[0m 该条消息总tokens数大于单条消息最大数量")
                print("\033[1;31mError:\033[0m 该条消息取消任务，进行拆分翻译")
                return

            # ——————————————————————————————————————————开始循环请求，直至成功或失败——————————————————————————————————————————
            start_time = time.time()
            timeout = 850  # 设置超时时间为x秒
            request_errors_count = 0  # 设置请求错误次数限制
            Wrong_answer_count = 0  # 设置错误回复次数限制
            model_degradation = False  # 模型退化检测

            while 1:
                # 检查是否取消
                if Global.Running_status == 10:
                    return
                # 检查是否暂停
                if Global.Running_status == 1011:
                    time.sleep(1)
                    continue

                # 检查子线程运行是否超时---------------------------------
                if time.time() - start_time > timeout:
                    print(
                        "\033[1;31mError:\033[0m 子线程执行任务已经超时，将暂时取消本次任务"
                    )
                    break

                # 检查是否符合速率限制---------------------------------
                if Global.request_limiter.RPM_and_TPM_limit(request_tokens_consume):

                    print("[INFO] 已发送请求,正在等待AI回复中-----------------------")
                    print(
                        "[INFO] 请求与回复的tokens数预计值是：",
                        request_tokens_consume + completion_tokens_consume,
                    )
                    print("[INFO] 当前发送的原文文本：\n", source_text_str)

                    # ——————————————————————————————————————————发送会话请求——————————————————————————————————————————
                    # 记录开始请求时间
                    Start_request_time = time.time()

                    # 获取AI的参数设置
                    temperature, top_p, presence_penalty, frequency_penalty = (
                        Global.configurator.get_model_parameters()
                    )
                    # 如果上一次请求出现模型退化，更改参数
                    if model_degradation:
                        frequency_penalty = 0.2

                    # 获取apikey
                    openai_apikey = Global.configurator.get_apikey()
                    # 获取请求地址
                    openai_base_url = Global.configurator.openai_base_url
                    # 创建openai客户端
                    openaiclient = OpenAI(
                        api_key=openai_apikey, base_url=openai_base_url
                    )
                    # 发送对话请求
                    try:
                        response = openaiclient.chat.completions.create(
                            model=Global.configurator.model_type,
                            messages=messages,
                            temperature=temperature,
                            top_p=top_p,
                            presence_penalty=presence_penalty,
                            frequency_penalty=frequency_penalty,
                        )

                    # 抛出错误信息
                    except Exception as e:
                        print(
                            "\033[1;31mError:\033[0m 进行请求时出现问题！！！错误信息如下"
                        )
                        print(f"Error: {e}\n")

                        # 请求错误计次
                        request_errors_count = request_errors_count + 1
                        # 如果错误次数过多，就取消任务
                        if request_errors_count >= 6:
                            print(
                                "\033[1;31m[ERROR]\033[0m 请求发生错误次数过多，该线程取消任务！"
                            )
                            break

                        # 处理完毕，再次进行请求
                        continue

                    # ——————————————————————————————————————————收到回复，并截取回复内容中的文本内容 ————————————————————————————————————————
                    # 计算AI回复花费的时间
                    response_time = time.time()
                    Request_consumption_time = round(
                        response_time - Start_request_time, 2
                    )

                    # 计算本次请求的花费的tokens
                    try:  # 因为有些中转网站不返回tokens消耗
                        prompt_tokens_used = int(
                            response.usage.prompt_tokens
                        )  # 本次请求花费的tokens
                    except Exception as e:
                        prompt_tokens_used = 0
                    try:
                        completion_tokens_used = int(
                            response.usage.completion_tokens
                        )  # 本次回复花费的tokens
                    except Exception as e:
                        completion_tokens_used = 0

                    # 提取回复的文本内容
                    response_content = response.choices[0].message.content

                    print("\n")
                    print("[INFO] 已成功接受到AI的回复-----------------------")
                    print(
                        "[INFO] 该次请求已消耗等待时间：",
                        Request_consumption_time,
                        "秒",
                    )
                    print(
                        "[INFO] 本次请求与回复花费的总tokens是：",
                        prompt_tokens_used + completion_tokens_used,
                    )
                    print("[INFO] AI回复的文本内容：\n", response_content, "\n", "\n")

                    # ——————————————————————————————————————————对AI回复内容进行各种处理和检查——————————————————————————————————————————
                    # 处理回复内容
                    response_content = Response_Parser.convert_str_to_json_str(
                        self, row_count, response_content
                    )

                    # 检查回复内容
                    check_result, error_content = (
                        Response_Parser.check_response_content(
                            self, response_content, source_text_dict
                        )
                    )

                    # 如果没有出现错误
                    if check_result:
                        # 转化为字典格式
                        response_dict = json.loads(
                            response_content
                        )  # 注意转化为字典的数字序号key是字符串类型

                        # 如果开启了保留换行符功能
                        if Global.configurator.preserve_line_breaks_toggle and Global.Running_status == 6:
                            response_dict = Cache_Manager.replace_special_characters(
                                self, response_dict, "还原"
                            )

                        # 录入缓存文件
                        Global.lock1.acquire()  # 获取锁
                        Cache_Manager.update_cache_data(
                            self, Global.cache_list, source_text_list, response_dict
                        )
                        Global.lock1.release()  # 释放锁

                        # 如果开启自动备份,则自动备份缓存文件
                        if (
                            Global.window.Widget_start_translation.B_settings.checkBox_switch.isChecked()
                        ):
                            Global.lock3.acquire()  # 获取锁

                            # 创建存储缓存文件的文件夹，如果路径不存在，创建文件夹
                            output_path = os.path.join(
                                Global.configurator.Output_Folder, "cache"
                            )
                            os.makedirs(output_path, exist_ok=True)
                            # 输出备份
                            File_Outputter.output_cache_file(
                                self, Global.cache_list, output_path
                            )
                            Global.lock3.release()  # 释放锁

                        Global.lock2.acquire()  # 获取锁

                        # 如果是进行平时的翻译任务
                        if Global.Running_status == 6:
                            # 计算进度信息
                            progress = (
                                (
                                    Global.user_interface_prompter.translated_line_count
                                    + row_count
                                )
                                / Global.user_interface_prompter.total_text_line_count
                                * 100
                            )
                            progress = round(progress, 1)

                            # 更改UI界面信息,注意，传入的数值类型分布是字符型与整数型，小心浮点型混入
                            Global.user_interface_prompter.signal.emit(
                                "更新翻译界面数据",
                                "翻译成功",
                                row_count,
                                prompt_tokens_used,
                                completion_tokens_used,
                            )

                        # 如果进行的是错行检查任务，使用不同的计算方法
                        elif Global.Running_status == 7:
                            Global.user_interface_prompter.translated_line_count = (
                                Global.user_interface_prompter.translated_line_count
                                + row_count
                            )
                            progress = (
                                Global.user_interface_prompter.translated_line_count
                                / Global.user_interface_prompter.total_text_line_count
                                * 100
                            )
                            progress = round(progress, 1)

                        print(
                            f"\n--------------------------------------------------------------------------------------"
                        )
                        print(
                            f"\n\033[1;32mSuccess:\033[0m AI回复内容检查通过！！！已翻译完成{progress}%"
                        )
                        print(
                            f"\n--------------------------------------------------------------------------------------\n"
                        )
                        Global.lock2.release()  # 释放锁

                        break

                    # 如果出现回复错误
                    else:

                        # 更改UI界面信息
                        Global.lock2.acquire()  # 获取锁
                        # 如果是进行平时的翻译任务
                        if Global.Running_status == 6:
                            Global.user_interface_prompter.signal.emit(
                                "更新翻译界面数据",
                                "翻译失败",
                                row_count,
                                prompt_tokens_used,
                                completion_tokens_used,
                            )
                        Global.lock2.release()  # 释放锁
                        print(
                            "\033[1;33mWarning:\033[0m AI回复内容存在问题:",
                            error_content,
                            "\n",
                        )
                        # 检查一下是不是模型退化
                        if error_content == "AI回复内容出现高频词,并重新翻译":
                            print(
                                "\033[1;33mWarning:\033[0m 下次请求将修改参数，回避高频词输出",
                                "\n",
                            )
                            model_degradation = True

                        # 错误回复计次
                        Wrong_answer_count = Wrong_answer_count + 1
                        print(
                            "\033[1;33mWarning:\033[0m AI回复内容格式错误次数:",
                            Wrong_answer_count,
                            "到达2次后将该段文本进行拆分翻译\n",
                        )
                        # 检查回答错误次数，如果达到限制，则跳过该句翻译。
                        if Wrong_answer_count >= 2:
                            print(
                                "\033[1;33mWarning:\033[0m 错误次数已经达限制,将该段文本进行拆分翻译！\n"
                            )
                            break

                        # 进行下一次循环
                        time.sleep(3)
                        continue

        # 子线程抛出错误信息
        except Exception as e:
            print("\033[1;31mError:\033[0m 子线程运行出现问题！错误信息如下")
            print(f"Error: {e}\n")
            return

    # 将json文本改为纯文本
    def convert_dict_to_raw_str(self, source_text_dict):
        str_list = []
        for idx in range(len(source_text_dict.keys())):
            # str_list.append(s['source_text'])
            str_list.append(source_text_dict[f"{idx}"])
        raw_str = "\n".join(str_list)
        return raw_str

    # 将列表中的字符串中的全角数字转换为半角数字
    def convert_fullwidth_to_halfwidth(self, input_string):
        modified_string = ""
        for char in input_string:
            if "０" <= char <= "９":  # 判断是否为全角数字
                modified_string += chr(
                    ord(char) - ord("０") + ord("0")
                )  # 转换为半角数字
            else:
                modified_string += char

        return modified_string
