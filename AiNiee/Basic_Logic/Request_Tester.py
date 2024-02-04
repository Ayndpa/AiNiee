import os
from openai import OpenAI
from ..Global import Global
import google.generativeai as genai

# 接口测试器
class Request_Tester:
    def __init__(self):
        pass

    # openai官方接口测试
    def openai_request_test(self):
        Account_Type = (
            Global.window.Widget_Openai.comboBox_account_type.currentText()
        )  # 获取账号类型下拉框当前选中选项的值
        Model_Type = (
            Global.window.Widget_Openai.comboBox_model.currentText()
        )  # 获取模型类型下拉框当前选中选项的值
        API_key_str = (
            Global.window.Widget_Openai.TextEdit_apikey.toPlainText()
        )  # 获取apikey输入值
        Proxy_port = (
            Global.window.Widget_Openai.LineEdit_proxy_port.text()
        )  # 获取代理端口

        # 如果填入地址，则设置系统代理
        if Proxy_port:
            print("[INFO] 系统代理端口是:", Proxy_port, "\n")
            os.environ["http_proxy"] = Proxy_port
            os.environ["https_proxy"] = Proxy_port

        # 分割KEY字符串并存储进列表里,如果API_key_str中没有逗号，split(",")方法仍然返回一个只包含一个元素的列表
        API_key_list = API_key_str.replace("\n", "").replace(" ", "").split(",")

        # 创建openai客户端
        openaiclient = OpenAI(
            api_key=API_key_list[0], base_url="https://api.openai.com/v1"
        )

        print("[INFO] 账号类型是:", Account_Type, "\n")
        print("[INFO] 模型选择是:", Model_Type, "\n")

        # 创建存储每个key测试结果的列表
        test_results = [None] * len(API_key_list)

        # 循环测试每一个apikey情况
        for i, key in enumerate(API_key_list):
            print(f"[INFO] 正在测试第{i+1}个API KEY：{key}", "\n")

            # 更换key
            openaiclient.api_key = API_key_list[i]

            # 构建发送内容
            messages_test = [
                {
                    "role": "system",
                    "content": "你是我的女朋友欣雨。接下来你必须以女朋友的方式回复我",
                },
                {"role": "user", "content": "小可爱，你在干嘛"},
            ]
            print("[INFO] 当前发送内容：\n", messages_test, "\n")

            # 尝试请求，并设置各种参数
            try:
                response_test = openaiclient.chat.completions.create(
                    model=Model_Type,
                    messages=messages_test,
                )

                # 如果回复成功，显示成功信息
                response_test = response_test.choices[0].message.content
                print("[INFO] 已成功接受到AI的回复")
                print("[INFO] AI回复的文本内容：\n", response_test, "\n", "\n")

                test_results[i] = 1  # 记录成功结果

            # 如果回复失败，抛出错误信息，并测试下一个key
            except Exception as e:
                print(
                    "\033[1;31mError:\033[0m key：",
                    API_key_list[i],
                    "请求出现问题！错误信息如下",
                )
                print(f"Error: {e}\n\n")
                test_results[i] = 0  # 记录错误结果
                continue

        # 输出每个API密钥测试的结果
        print("[INFO] 全部API KEY测试结果--------------")
        for i, key in enumerate(API_key_list):
            result = "成功" if test_results[i] == 1 else "失败"
            print(f"第{i+1}个 API KEY：{key} 测试结果：{result}")

        # 检查测试结果是否全部成功
        all_successful = all(result == 1 for result in test_results)
        # 输出总结信息
        if all_successful:
            print("[INFO] 所有API KEY测试成功！！！！")
            Global.user_interface_prompter.signal.emit(
                "接口测试结果", "测试成功", 0, 0, 0
            )
        else:
            print("[INFO] 存在API KEY测试失败！！！！")
            Global.user_interface_prompter.signal.emit(
                "接口测试结果", "测试失败", 0, 0, 0
            )

    # openai代理接口测试
    def op_request_test(self):

        Base_url = (
            Global.window.Widget_Openai_Proxy.A_settings.LineEdit_relay_address.text()
        )  # 获取请求地址
        Model_Type = (
            Global.window.Widget_Openai_Proxy.A_settings.comboBox_model.currentText()
        )  # 获取模型类型下拉框当前选中选项的值
        API_key_str = (
            Global.window.Widget_Openai_Proxy.A_settings.TextEdit_apikey.toPlainText()
        )  # 获取apikey输入值
        Proxy_port = (
            Global.window.Widget_Openai_Proxy.A_settings.LineEdit_proxy_port.text()
        )  # 获取代理端口

        # 如果填入地址，则设置系统代理
        if Proxy_port:
            print("[INFO] 系统代理端口是:", Proxy_port, "\n")
            os.environ["http_proxy"] = Proxy_port
            os.environ["https_proxy"] = Proxy_port

        # 分割KEY字符串并存储进列表里,如果API_key_str中没有逗号，split(",")方法仍然返回一个只包含一个元素的列表
        API_key_list = API_key_str.replace("\n", "").replace(" ", "").split(",")

        # 检查一下请求地址尾部是否为/v1，自动补全
        if Base_url[-3:] != "/v1":
            Base_url = Base_url + "/v1"

        # 创建openai客户端
        openaiclient = OpenAI(api_key=API_key_list[0], base_url=Base_url)

        print("[INFO] 中转请求地址是:", Base_url, "\n")
        print("[INFO] 模型选择是:", Model_Type, "\n")

        # 创建存储每个key测试结果的列表
        test_results = [None] * len(API_key_list)

        # 循环测试每一个apikey情况
        for i, key in enumerate(API_key_list):
            print(f"[INFO] 正在测试第{i+1}个API KEY：{key}", "\n")

            # 更换key
            openaiclient.api_key = API_key_list[i]

            # 构建发送内容
            messages_test = [
                {
                    "role": "system",
                    "content": "你是我的女朋友欣雨。接下来你必须以女朋友的方式回复我",
                },
                {"role": "user", "content": "小可爱，你在干嘛"},
            ]
            print("[INFO] 当前发送内容：\n", messages_test, "\n")

            # 尝试请求，并设置各种参数
            try:
                response_test = openaiclient.chat.completions.create(
                    model=Model_Type,
                    messages=messages_test,
                )

                # 如果回复成功，显示成功信息
                print("[INFO] 接口回复的文本内容：\n", response_test, "\n", "\n")
                response_test = response_test.choices[0].message.content
                print("[INFO] 已成功接受到AI的回复")

                test_results[i] = 1  # 记录成功结果

            # 如果回复失败，抛出错误信息，并测试下一个key
            except Exception as e:
                print(
                    "\033[1;31mError:\033[0m key：",
                    API_key_list[i],
                    "请求出现问题！错误信息如下",
                )
                print(f"Error: {e}\n\n")
                test_results[i] = 0  # 记录错误结果
                continue

        # 输出每个API密钥测试的结果
        print("[INFO] 全部API KEY测试结果--------------")
        for i, key in enumerate(API_key_list):
            result = "成功" if test_results[i] == 1 else "失败"
            print(f"第{i+1}个 API KEY：{key} 测试结果：{result}")

        # 检查测试结果是否全部成功
        all_successful = all(result == 1 for result in test_results)
        # 输出总结信息
        if all_successful:
            print("[INFO] 所有API KEY测试成功！！！！")
            Global.user_interface_prompter.signal.emit(
                "接口测试结果", "测试成功", 0, 0, 0
            )
        else:
            print("[INFO] 存在API KEY测试失败！！！！")
            Global.user_interface_prompter.signal.emit(
                "接口测试结果", "测试失败", 0, 0, 0
            )

    # google官方接口测试
    def google_request_test(self):

        Model_Type = (
            Global.window.Widget_Google.comboBox_model.currentText()
        )  # 获取模型类型下拉框当前选中选项的值
        API_key_str = (
            Global.window.Widget_Google.TextEdit_apikey.toPlainText()
        )  # 获取apikey输入值
        Proxy_port = (
            Global.window.Widget_Google.LineEdit_proxy_port.text()
        )  # 获取代理端口

        # 如果填入地址，则设置系统代理
        if Proxy_port:
            print("[INFO] 系统代理端口是:", Proxy_port, "\n")
            os.environ["http_proxy"] = Proxy_port
            os.environ["https_proxy"] = Proxy_port

        # 分割KEY字符串并存储进列表里,如果API_key_str中没有逗号，split(",")方法仍然返回一个只包含一个元素的列表
        API_key_list = API_key_str.replace("\n", "").replace(" ", "").split(",")

        print("[INFO] 模型选择是:", Model_Type, "\n")

        # 设置ai参数
        generation_config = {
            "temperature": 0,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,  # 最大输出，pro最大输出是2048
        }

        # 调整安全限制
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]

        # 创建存储每个key测试结果的列表
        test_results = [None] * len(API_key_list)

        # 循环测试每一个apikey情况
        for i, key in enumerate(API_key_list):
            print(f"[INFO] 正在测试第{i+1}个API KEY：{key}", "\n")

            # 更换key
            genai.configure(api_key=API_key_list[i])

            # 构建发送内容
            messages_test = [
                "你是我的女朋友欣雨。接下来你必须以女朋友的方式向我问好",
            ]
            print("[INFO] 当前发送内容：\n", messages_test, "\n")

            # 设置对话模型
            model = genai.GenerativeModel(
                model_name=Model_Type,
                generation_config=generation_config,
                safety_settings=safety_settings,
            )

            # 尝试请求，并设置各种参数
            try:
                response_test = model.generate_content(messages_test)

                # 如果回复成功，显示成功信息
                response_test = response_test.text
                print("[INFO] 已成功接受到AI的回复")
                print("[INFO] AI回复的文本内容：\n", response_test, "\n", "\n")

                test_results[i] = 1  # 记录成功结果

            # 如果回复失败，抛出错误信息，并测试下一个key
            except Exception as e:
                print(
                    "\033[1;31mError:\033[0m key：",
                    API_key_list[i],
                    "请求出现问题！错误信息如下",
                )
                print(f"Error: {e}\n\n")
                test_results[i] = 0  # 记录错误结果
                continue

        # 输出每个API密钥测试的结果
        print("[INFO] 全部API KEY测试结果--------------")
        for i, key in enumerate(API_key_list):
            result = "成功" if test_results[i] == 1 else "失败"
            print(f"第{i+1}个 API KEY：{key} 测试结果：{result}")

        # 检查测试结果是否全部成功
        all_successful = all(result == 1 for result in test_results)
        # 输出总结信息
        if all_successful:
            print("[INFO] 所有API KEY测试成功！！！！")
            Global.user_interface_prompter.signal.emit(
                "接口测试结果", "测试成功", 0, 0, 0
            )
        else:
            print("[INFO] 存在API KEY测试失败！！！！")
            Global.user_interface_prompter.signal.emit(
                "接口测试结果", "测试失败", 0, 0, 0
            )

    # sakura接口测试
    def sakura_request_test(self):

        Base_url = (
            Global.window.Widget_SakuraLLM.LineEdit_address.text()
        )  # 获取请求地址
        Model_Type = (
            Global.window.Widget_SakuraLLM.comboBox_model.currentText()
        )  # 获取模型类型下拉框当前选中选项的值
        Proxy_port = (
            Global.window.Widget_SakuraLLM.LineEdit_proxy_port.text()
        )  # 获取代理端口

        # 如果填入地址，则设置系统代理
        if Proxy_port:
            print("[INFO] 系统代理端口是:", Proxy_port, "\n")
            os.environ["http_proxy"] = Proxy_port
            os.environ["https_proxy"] = Proxy_port

        # 检查一下请求地址尾部是否为/v1，自动补全
        if Base_url[-3:] != "/v1":
            Base_url = Base_url + "/v1"

        # 创建openai客户端
        openaiclient = OpenAI(api_key="sakura", base_url=Base_url)

        print("[INFO] 模型地址是:", Base_url, "\n")
        print("[INFO] 模型选择是:", Model_Type, "\n")

        # 构建发送内容
        messages_test = [
            {
                "role": "system",
                "content": "你是一个轻小说翻译模型，可以流畅通顺地以日本轻小说的风格将日文翻译成简体中文，并联系上下文正确使用人称代词，不擅自添加原文中没有的代词。",
            },
            {"role": "user", "content": "将下面的日文文本翻译成中文：サポートキャスト"},
        ]
        print("[INFO] 当前发送内容：\n", messages_test, "\n")

        # 尝试请求，并设置各种参数
        try:
            response_test = openaiclient.chat.completions.create(
                model=Model_Type,
                messages=messages_test,
            )

            # 如果回复成功，显示成功信息
            response_test = response_test.choices[0].message.content
            print("[INFO] 已成功接受到AI的回复")
            print("[INFO] AI回复的文本内容：\n", response_test, "\n", "\n")

            print("[INFO] 模型通讯测试成功！！！！")
            Global.user_interface_prompter.signal.emit(
                "接口测试结果", "测试成功", 0, 0, 0
            )

        # 如果回复失败，抛出错误信息，并测试下一个key
        except Exception as e:
            print("\033[1;31mError:\033[0m 请求出现问题！错误信息如下")
            print(f"Error: {e}\n\n")
            print("[INFO] 模型通讯测试失败！！！！")
            Global.user_interface_prompter.signal.emit(
                "接口测试结果", "测试失败", 0, 0, 0
            )
