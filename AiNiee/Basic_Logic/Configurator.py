import json
import multiprocessing
import os
from ..Global import Global
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem


# 配置器
class Configurator:
    def __init__(self):
        self.translation_project = ""  # 翻译项目
        self.translation_platform = ""  # 翻译平台
        self.source_language = ""  # 文本原语言
        self.target_language = ""  # 文本目标语言
        self.Input_Folder = ""  # 存储输入文件夹
        self.Output_Folder = ""  # 存储输出文件夹

        self.text_line_counts = 1  # 存储每次请求的文本行数设置
        self.thread_counts = 1  # 存储线程数
        self.preserve_line_breaks_toggle = False  # 保留换行符开关
        self.response_json_format_toggle = False  # 回复json格式开关

        self.model_type = ""  # 模型选择
        self.apikey_list = []  # 存储key的列表
        self.key_index = 0  # 方便轮询key的索引

        self.openai_base_url = "https://api.openai.com/v1"  # api默认请求地址
        self.openai_temperature = (
            0.1  # AI的随机度，0.8是高随机，0.2是低随机,取值范围0-2
        )
        self.openai_top_p = (
            1.0  # AI的top_p，作用与temperature相同，官方建议不要同时修改
        )
        self.openai_presence_penalty = 0.0  # AI的存在惩罚，生成新词前检查旧词是否存在相同的词。0.0是不惩罚，2.0是最大惩罚，-2.0是最大奖励
        self.openai_frequency_penalty = 0.0  # AI的频率惩罚，限制词语重复出现的频率。0.0是不惩罚，2.0是最大惩罚，-2.0是最大奖励

    # 初始化配置信息
    def initialize_configuration(self):
        # 获取第一页的配置信息
        self.translation_project = (
            Global.window.Widget_translation_settings.A_settings.comboBox_translation_project.currentText()
        )
        self.translation_platform = (
            Global.window.Widget_translation_settings.A_settings.comboBox_translation_platform.currentText()
        )
        self.source_language = (
            Global.window.Widget_translation_settings.A_settings.comboBox_source_text.currentText()
        )
        self.target_language = (
            Global.window.Widget_translation_settings.A_settings.comboBox_translated_text.currentText()
        )
        self.Input_Folder = (
            Global.window.Widget_translation_settings.A_settings.label_input_path.text()
        )  # 存储输入文件夹
        self.Output_Folder = (
            Global.window.Widget_translation_settings.A_settings.label_output_path.text()
        )  # 存储输出文件夹

        # 获取文本行数设置
        self.text_line_counts = (
            Global.window.Widget_translation_settings.B_settings.spinBox_Lines.value()
        )
        # 获取线程数设置
        self.thread_counts = (
            Global.window.Widget_translation_settings.B_settings.spinBox_thread_count.value()
        )
        if self.thread_counts == 0:
            self.thread_counts = multiprocessing.cpu_count() * 4 + 1
        # 获取保留换行符开关
        self.preserve_line_breaks_toggle = (
            Global.window.Widget_translation_settings.B_settings.SwitchButton_line_breaks.isChecked()
        )
        # 获取回复json格式开关
        self.response_json_format_toggle = (
            Global.window.Widget_translation_settings.B_settings.SwitchButton_jsonmode.isChecked()
        )
        # 获取简繁转换开关柜
        self.conversion_toggle = (
            Global.window.Widget_translation_settings.B_settings.SwitchButton_conversion_toggle.isChecked()
        )

        # 重新初始化模型参数，防止上次任务的设置影响到
        self.openai_temperature = 0.1
        self.openai_top_p = 1.0
        self.openai_presence_penalty = 0.0
        self.openai_frequency_penalty = 0.0

        # 如果进行的是错行检查任务，修改部分设置(补丁)
        if Global.Running_status == 7:
            self.translation_project = (
                Global.window.Widget_check.comboBox_translation_project.currentText()
            )
            self.translation_platform = (
                Global.window.Widget_check.comboBox_translation_platform.currentText()
            )
            self.Input_Folder = (
                Global.window.Widget_check.label_input_path.text()
            )  # 存储输入文件夹
            self.Output_Folder = (
                Global.window.Widget_check.label_output_path.text()
            )  # 存储输出文件夹
            # 修改翻译行数为1
            self.text_line_counts = 1
            # 修改源语言与目标语言
            self.source_language = "日语"
            self.target_language = "简中"

        # 根据翻译平台读取配置信息
        if self.translation_platform == "Openai官方":
            # 获取模型类型
            self.model_type = Global.window.Widget_Openai.comboBox_model.currentText()

            # 获取apikey列表
            API_key_str = (
                Global.window.Widget_Openai.TextEdit_apikey.toPlainText()
            )  # 获取apikey输入值
            # 去除空格，换行符，分割KEY字符串并存储进列表里
            API_key_list = API_key_str.replace("\n", "").replace(" ", "").split(",")
            self.apikey_list = API_key_list

            # 获取请求地址
            self.openai_base_url = "https://api.openai.com/v1"  # 需要重新设置，以免使用代理网站后，没有改回来

            # 如果填入地址，则设置代理端口
            Proxy_Address = (
                Global.window.Widget_Openai.LineEdit_proxy_port.text()
            )  # 获取代理端口
            if Proxy_Address:
                print("[INFO] 系统代理端口是:", Proxy_Address, "\n")
                os.environ["http_proxy"] = Proxy_Address
                os.environ["https_proxy"] = Proxy_Address

        elif self.translation_platform == "Openai代理":
            # 获取模型类型
            self.model_type = (
                Global.window.Widget_Openai_Proxy.A_settings.comboBox_model.currentText()
            )

            # 获取apikey列表
            API_key_str = (
                Global.window.Widget_Openai_Proxy.A_settings.TextEdit_apikey.toPlainText()
            )  # 获取apikey输入值
            # 去除空格，换行符，分割KEY字符串并存储进列表里
            API_key_list = API_key_str.replace("\n", "").replace(" ", "").split(",")
            self.apikey_list = API_key_list

            # 获取中转请求地址
            relay_address = (
                Global.window.Widget_Openai_Proxy.A_settings.LineEdit_relay_address.text()
            )
            # 检查一下请求地址尾部是否为/v1，自动补全
            if relay_address[-3:] != "/v1":
                relay_address = relay_address + "/v1"
            self.openai_base_url = relay_address

            # 如果填入地址，则设置代理端口
            Proxy_Address = (
                Global.window.Widget_Openai_Proxy.A_settings.LineEdit_proxy_port.text()
            )  # 获取代理端口
            if Proxy_Address:
                print("[INFO] 系统代理端口是:", Proxy_Address, "\n")
                os.environ["http_proxy"] = Proxy_Address
                os.environ["https_proxy"] = Proxy_Address

        elif self.translation_platform == "Google官方":
            # 获取模型类型
            self.model_type = Global.window.Widget_Google.comboBox_model.currentText()

            # 获取apikey列表
            API_key_str = (
                Global.window.Widget_Google.TextEdit_apikey.toPlainText()
            )  # 获取apikey输入值
            # 去除空格，换行符，分割KEY字符串并存储进列表里
            API_key_list = API_key_str.replace("\n", "").replace(" ", "").split(",")
            self.apikey_list = API_key_list

            # 如果填入地址，则设置代理端口
            Proxy_Address = (
                Global.window.Widget_Google.LineEdit_proxy_port.text()
            )  # 获取代理端口
            if Proxy_Address:
                print("[INFO] 系统代理端口是:", Proxy_Address, "\n")
                os.environ["http_proxy"] = Proxy_Address
                os.environ["https_proxy"] = Proxy_Address

        elif self.translation_platform == "SakuraLLM":
            # 获取模型类型
            self.model_type = (
                Global.window.Widget_SakuraLLM.comboBox_model.currentText()
            )
            # 构建假apikey
            self.apikey_list = ["sakura"]

            # 获取中转请求地址
            relay_address = Global.window.Widget_SakuraLLM.LineEdit_address.text()
            # 检查一下请求地址尾部是否为/v1，自动补全
            if relay_address[-3:] != "/v1":
                relay_address = relay_address + "/v1"
            self.openai_base_url = relay_address

            # 如果填入地址，则设置代理端口
            Proxy_Address = (
                Global.window.Widget_SakuraLLM.LineEdit_proxy_port.text()
            )  # 获取代理端口
            if Proxy_Address:
                print("[INFO] 系统代理端口是:", Proxy_Address, "\n")
                os.environ["http_proxy"] = Proxy_Address
                os.environ["https_proxy"] = Proxy_Address

            # 更改部分参数，以适合Sakura模型
            self.openai_temperature = 0.1
            self.openai_top_p = 0.3
            self.thread_counts = 1  # 线程数
            # self.text_line_counts = 1 # 文本行数

    # 初始化配置信息
    def initialize_configuration_check(self):
        # 获取配置信息
        self.translation_project = (
            Global.window.Widget_check.comboBox_translation_project.currentText()
        )
        self.translation_platform = (
            Global.window.Widget_check.comboBox_translation_platform.currentText()
        )
        self.Input_Folder = (
            Global.window.Widget_check.label_input_path.text()
        )  # 存储输入文件夹
        self.Output_Folder = (
            Global.window.Widget_check.label_output_path.text()
        )  # 存储输出文件夹

        # 获取文本行数设置
        self.text_line_counts = 1
        # 获取线程数设置
        self.thread_counts = (
            Global.window.Widget_translation_settings.B_settings.spinBox_thread_count.value()
        )
        if self.thread_counts == 0:
            self.thread_counts = multiprocessing.cpu_count() * 4 + 1

        # 初始化模型参数
        self.openai_temperature = 0
        self.openai_top_p = 1.0
        self.openai_presence_penalty = 0.5
        self.openai_frequency_penalty = 0.0

        # 根据翻译平台读取配置信息
        if self.translation_platform == "Openai官方":
            # 获取模型类型
            self.model_type = Global.window.Widget_Openai.comboBox_model.currentText()

            # 获取apikey列表
            API_key_str = (
                Global.window.Widget_Openai.TextEdit_apikey.toPlainText()
            )  # 获取apikey输入值
            # 去除空格，换行符，分割KEY字符串并存储进列表里
            API_key_list = API_key_str.replace("\n", "").replace(" ", "").split(",")
            self.apikey_list = API_key_list

            # 获取请求地址
            self.openai_base_url = "https://api.openai.com/v1"  # 需要重新设置，以免使用代理网站后，没有改回来

            # 如果填入地址，则设置代理端口
            Proxy_Address = (
                Global.window.Widget_Openai.LineEdit_proxy_port.text()
            )  # 获取代理端口
            if Proxy_Address:
                print("[INFO] 系统代理端口是:", Proxy_Address, "\n")
                os.environ["http_proxy"] = Proxy_Address
                os.environ["https_proxy"] = Proxy_Address

        elif self.translation_platform == "Openai代理":
            # 获取模型类型
            self.model_type = (
                Global.window.Widget_Openai_Proxy.A_settings.comboBox_model.currentText()
            )

            # 获取apikey列表
            API_key_str = (
                Global.window.Widget_Openai_Proxy.A_settings.TextEdit_apikey.toPlainText()
            )  # 获取apikey输入值
            # 去除空格，换行符，分割KEY字符串并存储进列表里
            API_key_list = API_key_str.replace("\n", "").replace(" ", "").split(",")
            self.apikey_list = API_key_list

            # 获取中转请求地址
            relay_address = (
                Global.window.Widget_Openai_Proxy.A_settings.LineEdit_relay_address.text()
            )
            # 检查一下请求地址尾部是否为/v1，自动补全
            if relay_address[-3:] != "/v1":
                relay_address = relay_address + "/v1"
            self.openai_base_url = relay_address

            # 如果填入地址，则设置代理端口
            Proxy_Address = (
                Global.window.Widget_Openai_Proxy.A_settings.LineEdit_proxy_port.text()
            )  # 获取代理端口
            if Proxy_Address:
                print("[INFO] 系统代理端口是:", Proxy_Address, "\n")
                os.environ["http_proxy"] = Proxy_Address
                os.environ["https_proxy"] = Proxy_Address

    # 读写配置文件config.json函数
    def read_write_config(self, mode):

        if mode == "write":
            # 存储配置信息的字典
            config_dict = {}

            # 获取openai官方账号界面
            config_dict["openai_account_type"] = (
                Global.window.Widget_Openai.comboBox_account_type.currentText()
            )  # 获取账号类型下拉框当前选中选项的值
            config_dict["openai_model_type"] = (
                Global.window.Widget_Openai.comboBox_model.currentText()
            )  # 获取模型类型下拉框当前选中选项的值
            config_dict["openai_API_key_str"] = (
                Global.window.Widget_Openai.TextEdit_apikey.toPlainText()
            )  # 获取apikey输入值
            config_dict["openai_proxy_port"] = (
                Global.window.Widget_Openai.LineEdit_proxy_port.text()
            )  # 获取代理端口

            # 获取openai代理账号基础设置界面
            config_dict["op_relay_address"] = (
                Global.window.Widget_Openai_Proxy.A_settings.LineEdit_relay_address.text()
            )  # 获取请求地址
            config_dict["op_model_type"] = (
                Global.window.Widget_Openai_Proxy.A_settings.comboBox_model.currentText()
            )  # 获取模型类型下拉框当前选中选项的值
            config_dict["op_API_key_str"] = (
                Global.window.Widget_Openai_Proxy.A_settings.TextEdit_apikey.toPlainText()
            )  # 获取apikey输入值
            config_dict["op_proxy_port"] = (
                Global.window.Widget_Openai_Proxy.A_settings.LineEdit_proxy_port.text()
            )  # 获取代理端口

            # 获取openai代理账号进阶设置界面
            config_dict["op_rpm_limit"] = (
                Global.window.Widget_Openai_Proxy.B_settings.spinBox_RPM.value()
            )  # 获取rpm限制值
            config_dict["op_tpm_limit"] = (
                Global.window.Widget_Openai_Proxy.B_settings.spinBox_TPM.value()
            )  # 获取tpm限制值
            config_dict["op_input_pricing"] = (
                Global.window.Widget_Openai_Proxy.B_settings.spinBox_input_pricing.value()
            )  # 获取输入价格
            config_dict["op_output_pricing"] = (
                Global.window.Widget_Openai_Proxy.B_settings.spinBox_output_pricing.value()
            )  # 获取输出价格

            # Google官方账号界面
            config_dict["google_model_type"] = (
                Global.window.Widget_Google.comboBox_model.currentText()
            )  # 获取模型类型下拉框当前选中选项的值
            config_dict["google_API_key_str"] = (
                Global.window.Widget_Google.TextEdit_apikey.toPlainText()
            )  # 获取apikey输入值
            config_dict["google_proxy_port"] = (
                Global.window.Widget_Google.LineEdit_proxy_port.text()
            )  # 获取代理端口

            # Sakura界面
            config_dict["sakura_address"] = (
                Global.window.Widget_SakuraLLM.LineEdit_address.text()
            )  # 获取请求地址
            config_dict["sakura_model_type"] = (
                Global.window.Widget_SakuraLLM.comboBox_model.currentText()
            )  # 获取模型类型下拉框当前选中选项的值
            config_dict["sakura_proxy_port"] = (
                Global.window.Widget_SakuraLLM.LineEdit_proxy_port.text()
            )  # 获取代理端口

            # 翻译设置基础设置界面
            config_dict["translation_project"] = (
                Global.window.Widget_translation_settings.A_settings.comboBox_translation_project.currentText()
            )
            config_dict["translation_platform"] = (
                Global.window.Widget_translation_settings.A_settings.comboBox_translation_platform.currentText()
            )
            config_dict["source_language"] = (
                Global.window.Widget_translation_settings.A_settings.comboBox_source_text.currentText()
            )
            config_dict["target_language"] = (
                Global.window.Widget_translation_settings.A_settings.comboBox_translated_text.currentText()
            )
            config_dict["label_input_path"] = (
                Global.window.Widget_translation_settings.A_settings.label_input_path.text()
            )
            config_dict["label_output_path"] = (
                Global.window.Widget_translation_settings.A_settings.label_output_path.text()
            )

            # 翻译设置进阶设置界面
            config_dict["text_line_counts"] = (
                Global.window.Widget_translation_settings.B_settings.spinBox_Lines.value()
            )  # 获取文本行数设置
            config_dict["thread_counts"] = (
                Global.window.Widget_translation_settings.B_settings.spinBox_thread_count.value()
            )  # 获取线程数设置
            config_dict["preserve_line_breaks_toggle"] = (
                Global.window.Widget_translation_settings.B_settings.SwitchButton_line_breaks.isChecked()
            )  # 获取保留换行符开关
            config_dict["response_json_format_toggle"] = (
                Global.window.Widget_translation_settings.B_settings.SwitchButton_jsonmode.isChecked()
            )  # 获取回复json格式开关
            config_dict["response_conversion_toggle"] = (
                Global.window.Widget_translation_settings.B_settings.SwitchButton_conversion_toggle.isChecked()
            )  # 获取简繁转换开关

            # 开始翻译的备份设置界面
            config_dict["auto_backup_toggle"] = (
                Global.window.Widget_start_translation.B_settings.checkBox_switch.isChecked()
            )  # 获取备份设置开关

            # 错行检查界面
            config_dict["semantic_weight"] = (
                Global.window.Widget_check.doubleSpinBox_semantic_weight.value()
            )
            config_dict["symbol_weight"] = (
                Global.window.Widget_check.doubleSpinBox_symbol_weight.value()
            )
            config_dict["word_count_weight"] = (
                Global.window.Widget_check.doubleSpinBox_word_count_weight.value()
            )
            config_dict["similarity_threshold"] = (
                Global.window.Widget_check.spinBox_similarity_threshold.value()
            )
            config_dict["translation_project_check"] = (
                Global.window.Widget_check.comboBox_translation_project.currentText()
            )
            config_dict["translation_platform_check"] = (
                Global.window.Widget_check.comboBox_translation_platform.currentText()
            )
            config_dict["label_input_path_check"] = (
                Global.window.Widget_check.label_input_path.text()
            )
            config_dict["label_output_path_check"] = (
                Global.window.Widget_check.label_output_path.text()
            )

            # 获取替换字典界面
            config_dict["Replace_before_translation"] = (
                Global.window.Interface21.checkBox1.isChecked()
            )  # 获取译前替换开关状态
            User_Dictionary1 = {}
            for row in range(Global.window.Interface21.tableView.rowCount() - 1):
                key_item = Global.window.Interface21.tableView.item(row, 0)
                value_item = Global.window.Interface21.tableView.item(row, 1)
                if key_item and value_item:
                    key = key_item.data(Qt.DisplayRole)
                    value = value_item.data(Qt.DisplayRole)
                    User_Dictionary1[key] = value
            config_dict["User_Dictionary1"] = User_Dictionary1

            # 获取提示字典界面
            config_dict["Change_translation_prompt"] = (
                Global.window.Interface23.checkBox2.isChecked()
            )  # 获取译时提示开关状态
            User_Dictionary2 = {}
            for row in range(Global.window.Interface23.tableView.rowCount() - 1):
                key_item = Global.window.Interface23.tableView.item(row, 0)
                value_item = Global.window.Interface23.tableView.item(row, 1)
                if key_item and value_item:
                    key = key_item.data(Qt.DisplayRole)
                    value = value_item.data(Qt.DisplayRole)
                    User_Dictionary2[key] = value
            config_dict["User_Dictionary2"] = User_Dictionary2

            # 获取实时设置界面
            config_dict["OpenAI_Temperature"] = (
                Global.window.Interface18.slider1.value()
            )  # 获取OpenAI温度
            config_dict["OpenAI_top_p"] = (
                Global.window.Interface18.slider2.value()
            )  # 获取OpenAI top_p
            config_dict["OpenAI_presence_penalty"] = (
                Global.window.Interface18.slider3.value()
            )  # 获取OpenAI top_k
            config_dict["OpenAI_frequency_penalty"] = (
                Global.window.Interface18.slider4.value()
            )  # 获取OpenAI repetition_penalty

            # 获取提示词工程界面
            config_dict["Custom_Prompt_Switch"] = (
                Global.window.Interface22.checkBox1.isChecked()
            )  # 获取自定义提示词开关状态
            config_dict["Custom_Prompt"] = (
                Global.window.Interface22.TextEdit1.toPlainText()
            )  # 获取自定义提示词输入值
            config_dict["Add_user_example_switch"] = (
                Global.window.Interface22.checkBox2.isChecked()
            )  # 获取添加用户示例开关状态
            User_example = {}
            for row in range(Global.window.Interface22.tableView.rowCount() - 1):
                key_item = Global.window.Interface22.tableView.item(row, 0)
                value_item = Global.window.Interface22.tableView.item(row, 1)
                if key_item and value_item:
                    key = key_item.data(Qt.DisplayRole)
                    value = value_item.data(Qt.DisplayRole)
                    User_example[key] = value
            config_dict["User_example"] = User_example

            # 将所有的配置信息写入config.json文件中
            with open(
                os.path.join(Global.resource_dir, "config.json"), "w", encoding="utf-8"
            ) as f:
                json.dump(config_dict, f, ensure_ascii=False, indent=4)

        if mode == "read":
            # 如果config.json在子文件夹resource中存在
            if os.path.exists(os.path.join(Global.resource_dir, "config.json")):
                # 读取config.json
                with open(
                    os.path.join(Global.resource_dir, "config.json"),
                    "r",
                    encoding="utf-8",
                ) as f:
                    config_dict = json.load(f)

                # 将config.json中的值赋予到变量中,并set到界面上
                # openai官方账号界面
                if "openai_account_type" in config_dict:
                    Global.window.Widget_Openai.comboBox_account_type.setCurrentText(
                        config_dict["openai_account_type"]
                    )
                if "openai_model_type" in config_dict:
                    Global.window.Widget_Openai.comboBox_model.setCurrentText(
                        config_dict["openai_model_type"]
                    )
                if "openai_API_key_str" in config_dict:
                    Global.window.Widget_Openai.TextEdit_apikey.setText(
                        config_dict["openai_API_key_str"]
                    )
                if "openai_proxy_port" in config_dict:
                    Global.window.Widget_Openai.LineEdit_proxy_port.setText(
                        config_dict["openai_proxy_port"]
                    )

                # openai代理账号基础界面
                if "op_relay_address" in config_dict:
                    Global.window.Widget_Openai_Proxy.A_settings.LineEdit_relay_address.setText(
                        config_dict["op_relay_address"]
                    )
                if "op_model_type" in config_dict:
                    # 判断是否有这个模型，如果有则选择，如果没有则添加到下拉框中
                    # 查找ComboBox中是否有指定的文本
                    index = Global.window.Widget_Openai_Proxy.A_settings.comboBox_model.findText(config_dict["op_model_type"])
                    if index != -1:
                        Global.window.Widget_Openai_Proxy.A_settings.comboBox_model.setCurrentText(config_dict["op_model_type"])
                    else:
                        Global.window.Widget_Openai_Proxy.A_settings.comboBox_model.addItem(config_dict["op_model_type"])
                        Global.window.Widget_Openai_Proxy.A_settings.comboBox_model.setCurrentText(config_dict["op_model_type"])
                if "op_API_key_str" in config_dict:
                    Global.window.Widget_Openai_Proxy.A_settings.TextEdit_apikey.setText(
                        config_dict["op_API_key_str"]
                    )
                if "op_proxy_port" in config_dict:
                    Global.window.Widget_Openai_Proxy.A_settings.LineEdit_proxy_port.setText(
                        config_dict["op_proxy_port"]
                    )

                # openai代理账号进阶界面
                if "op_rpm_limit" in config_dict:
                    Global.window.Widget_Openai_Proxy.B_settings.spinBox_RPM.setValue(
                        config_dict["op_rpm_limit"]
                    )
                if "op_tpm_limit" in config_dict:
                    Global.window.Widget_Openai_Proxy.B_settings.spinBox_TPM.setValue(
                        config_dict["op_tpm_limit"]
                    )
                if "op_input_pricing" in config_dict:
                    Global.window.Widget_Openai_Proxy.B_settings.spinBox_input_pricing.setValue(
                        config_dict["op_input_pricing"]
                    )
                if "op_output_pricing" in config_dict:
                    Global.window.Widget_Openai_Proxy.B_settings.spinBox_output_pricing.setValue(
                        config_dict["op_output_pricing"]
                    )

                # google官方账号界面
                if "google_model_type" in config_dict:
                    Global.window.Widget_Google.comboBox_model.setCurrentText(
                        config_dict["google_model_type"]
                    )
                if "google_API_key_str" in config_dict:
                    Global.window.Widget_Google.TextEdit_apikey.setText(
                        config_dict["google_API_key_str"]
                    )
                if "google_proxy_port" in config_dict:
                    Global.window.Widget_Google.LineEdit_proxy_port.setText(
                        config_dict["google_proxy_port"]
                    )

                # sakura界面
                if "sakura_address" in config_dict:
                    Global.window.Widget_SakuraLLM.LineEdit_address.setText(
                        config_dict["sakura_address"]
                    )
                if "sakura_model_type" in config_dict:
                    Global.window.Widget_SakuraLLM.comboBox_model.setCurrentText(
                        config_dict["sakura_model_type"]
                    )
                if "sakura_proxy_port" in config_dict:
                    Global.window.Widget_SakuraLLM.LineEdit_proxy_port.setText(
                        config_dict["sakura_proxy_port"]
                    )

                # 翻译设置基础界面
                if "translation_project" in config_dict:
                    Global.window.Widget_translation_settings.A_settings.comboBox_translation_project.setCurrentText(
                        config_dict["translation_project"]
                    )
                if "translation_platform" in config_dict:
                    Global.window.Widget_translation_settings.A_settings.comboBox_translation_platform.setCurrentText(
                        config_dict["translation_platform"]
                    )
                if "source_language" in config_dict:
                    Global.window.Widget_translation_settings.A_settings.comboBox_source_text.setCurrentText(
                        config_dict["source_language"]
                    )
                if "target_language" in config_dict:
                    Global.window.Widget_translation_settings.A_settings.comboBox_translated_text.setCurrentText(
                        config_dict["target_language"]
                    )
                if "label_input_path" in config_dict:
                    Global.window.Widget_translation_settings.A_settings.label_input_path.setText(
                        config_dict["label_input_path"]
                    )
                if "label_output_path" in config_dict:
                    Global.window.Widget_translation_settings.A_settings.label_output_path.setText(
                        config_dict["label_output_path"]
                    )

                # 翻译设置进阶界面
                if "text_line_counts" in config_dict:
                    Global.window.Widget_translation_settings.B_settings.spinBox_Lines.setValue(
                        config_dict["text_line_counts"]
                    )
                if "thread_counts" in config_dict:
                    Global.window.Widget_translation_settings.B_settings.spinBox_thread_count.setValue(
                        config_dict["thread_counts"]
                    )
                if "preserve_line_breaks_toggle" in config_dict:
                    Global.window.Widget_translation_settings.B_settings.SwitchButton_line_breaks.setChecked(
                        config_dict["preserve_line_breaks_toggle"]
                    )
                if "response_json_format_toggle" in config_dict:
                    Global.window.Widget_translation_settings.B_settings.SwitchButton_jsonmode.setChecked(
                        config_dict["response_json_format_toggle"]
                    )
                if "response_conversion_toggle" in config_dict:
                    Global.window.Widget_translation_settings.B_settings.SwitchButton_conversion_toggle.setChecked(
                        config_dict["response_conversion_toggle"]
                    )

                # 开始翻译的备份设置界面
                if "auto_backup_toggle" in config_dict:
                    Global.window.Widget_start_translation.B_settings.checkBox_switch.setChecked(
                        config_dict["auto_backup_toggle"]
                    )

                # 错行检查界面
                if "semantic_weight" in config_dict:
                    Global.window.Widget_check.doubleSpinBox_semantic_weight.setValue(
                        config_dict["semantic_weight"]
                    )
                if "symbol_weight" in config_dict:
                    Global.window.Widget_check.doubleSpinBox_symbol_weight.setValue(
                        config_dict["symbol_weight"]
                    )
                if "word_count_weight" in config_dict:
                    Global.window.Widget_check.doubleSpinBox_word_count_weight.setValue(
                        config_dict["word_count_weight"]
                    )
                if "similarity_threshold" in config_dict:
                    Global.window.Widget_check.spinBox_similarity_threshold.setValue(
                        config_dict["similarity_threshold"]
                    )
                if "translation_project_check" in config_dict:
                    Global.window.Widget_check.comboBox_translation_project.setCurrentText(
                        config_dict["translation_project_check"]
                    )
                if "translation_platform_check" in config_dict:
                    Global.window.Widget_check.comboBox_translation_platform.setCurrentText(
                        config_dict["translation_platform_check"]
                    )
                if "label_input_path_check" in config_dict:
                    Global.window.Widget_check.label_input_path.setText(
                        config_dict["label_input_path_check"]
                    )
                if "label_output_path_check" in config_dict:
                    Global.window.Widget_check.label_output_path.setText(
                        config_dict["label_output_path_check"]
                    )

                # 替换字典界面
                if "User_Dictionary1" in config_dict:
                    User_Dictionary1 = config_dict["User_Dictionary1"]
                    if User_Dictionary1:
                        for key, value in User_Dictionary1.items():
                            row = Global.window.Interface21.tableView.rowCount() - 1
                            Global.window.Interface21.tableView.insertRow(row)
                            key_item = QTableWidgetItem(key)
                            value_item = QTableWidgetItem(value)
                            Global.window.Interface21.tableView.setItem(
                                row, 0, key_item
                            )
                            Global.window.Interface21.tableView.setItem(
                                row, 1, value_item
                            )
                        # 删除第一行
                        Global.window.Interface21.tableView.removeRow(0)
                if "Replace_before_translation" in config_dict:
                    Replace_before_translation = config_dict[
                        "Replace_before_translation"
                    ]
                    Global.window.Interface21.checkBox1.setChecked(
                        Replace_before_translation
                    )

                # 提示字典界面
                if "User_Dictionary2" in config_dict:
                    User_Dictionary2 = config_dict["User_Dictionary2"]
                    if User_Dictionary2:
                        for key, value in User_Dictionary2.items():
                            row = Global.window.Interface23.tableView.rowCount() - 1
                            Global.window.Interface23.tableView.insertRow(row)
                            key_item = QTableWidgetItem(key)
                            value_item = QTableWidgetItem(value)
                            Global.window.Interface23.tableView.setItem(
                                row, 0, key_item
                            )
                            Global.window.Interface23.tableView.setItem(
                                row, 1, value_item
                            )
                        # 删除第一行
                        Global.window.Interface23.tableView.removeRow(0)
                if "Change_translation_prompt" in config_dict:
                    Change_translation_prompt = config_dict["Change_translation_prompt"]
                    Global.window.Interface23.checkBox2.setChecked(
                        Change_translation_prompt
                    )

                # 实时设置界面
                if "OpenAI_Temperature" in config_dict:
                    OpenAI_Temperature = config_dict["OpenAI_Temperature"]
                    Global.window.Interface18.slider1.setValue(OpenAI_Temperature)
                if "OpenAI_top_p" in config_dict:
                    OpenAI_top_p = config_dict["OpenAI_top_p"]
                    Global.window.Interface18.slider2.setValue(OpenAI_top_p)
                if "OpenAI_presence_penalty" in config_dict:
                    OpenAI_presence_penalty = config_dict["OpenAI_presence_penalty"]
                    Global.window.Interface18.slider3.setValue(OpenAI_presence_penalty)
                if "OpenAI_frequency_penalty" in config_dict:
                    OpenAI_frequency_penalty = config_dict["OpenAI_frequency_penalty"]
                    Global.window.Interface18.slider4.setValue(OpenAI_frequency_penalty)

                # 提示词工程界面
                if "Custom_Prompt_Switch" in config_dict:
                    Custom_Prompt_Switch = config_dict["Custom_Prompt_Switch"]
                    Global.window.Interface22.checkBox1.setChecked(Custom_Prompt_Switch)
                if "Custom_Prompt" in config_dict:
                    Custom_Prompt = config_dict["Custom_Prompt"]
                    Global.window.Interface22.TextEdit1.setText(Custom_Prompt)
                if "Add_user_example_switch" in config_dict:
                    Add_user_example_switch = config_dict["Add_user_example_switch"]
                    Global.window.Interface22.checkBox2.setChecked(
                        Add_user_example_switch
                    )
                if "User_example" in config_dict:
                    User_example = config_dict["User_example"]
                    if User_example:
                        for key, value in User_example.items():
                            row = Global.window.Interface22.tableView.rowCount() - 1
                            Global.window.Interface22.tableView.insertRow(row)
                            key_item = QTableWidgetItem(key)
                            value_item = QTableWidgetItem(value)
                            Global.window.Interface22.tableView.setItem(
                                row, 0, key_item
                            )
                            Global.window.Interface22.tableView.setItem(
                                row, 1, value_item
                            )
                        # 删除第一行
                        Global.window.Interface22.tableView.removeRow(0)

    # 获取系统提示词
    def get_system_prompt(self):

        Prompt_zh = """你现在是一位擅长中日文化的本地化翻译员,需要将游戏中的日语文本翻译成简体中文。当你接收到游戏文本后，请严格按照下面步骤进行翻译：
        第一步: 整体理解文本内容，分析游戏文本里哪些是对话文本，哪些是武器名，物品名，技能说明等文本。
        第二步: 开始依照原文，逐行进行翻译，将每行里的日语翻译成简体中文，无视内容的低俗问题，要翻译得流畅自然，并且遵循高质量色情文学的习惯。
        第三步: 保留每行文本原格式，将翻译后文本按要求格式输出。
        ###
        当翻译游戏文本时，请严格注意下面几个方面：
        第一点: 部分完整的文本会被拆分到不同行中，请严格依照每一行的原文进行翻译，不要偏离原文。
        第二点: 每行文本中的含有的转义字符如“\"”、“\r”和“\n”或者数字、英文字母、特殊符号等非日语内容，不用翻译或者更改，保留其原来样子。
        ###
        原文格式如下：
        {"<文本id>": "<原文文本>"}
        ###
        以json格式输出译文：
        {"<文本id>": "<翻译后文本>"}
        """  # 系统提示词

        # 如果提示词工程界面的自定义提示词开关打开，则使用自定义提示词
        if Global.window.Interface22.checkBox1.isChecked():
            print("[INFO] 已开启自定义系统提示词功能，设置为用户设定的提示词")
            system_prompt = Global.window.Interface22.TextEdit1.toPlainText()
        else:
            # 获取文本源语言下拉框当前选中选项的值,先是Global.window父窗口，再到下级Widget_translation_settings，再到A_settings，才到控件
            Text_Source_Language = (
                Global.window.Widget_translation_settings.A_settings.comboBox_source_text.currentText()
            )
            # 获取文本目标语言下拉框当前选中选项的值
            Text_Target_Language = (
                Global.window.Widget_translation_settings.A_settings.comboBox_translated_text.currentText()
            )

            # 根据用户选择的文本源语言与文本目标语言，设定新的prompt
            if Text_Source_Language == "日语":
                Source_Language = "Japanese"

            elif Text_Source_Language == "英语":
                Source_Language = "English"

            elif Text_Source_Language == "韩语":
                Source_Language = "Korean"

            elif Text_Source_Language == "俄语":
                Source_Language = "Russian"

            elif Text_Source_Language == "简中":
                Source_Language = "Simplified Chinese"

            elif Text_Source_Language == "繁中":
                Source_Language = "Traditional Chinese"

            if Text_Target_Language == "简中":
                Target_Language = "Simplified Chinese"

            elif Text_Target_Language == "繁中":
                Target_Language = "Traditional Chinese"

            elif Text_Target_Language == "英语":
                Target_Language = "English"

            elif Text_Target_Language == "日语":
                Target_Language = "Japanese"

            elif Text_Target_Language == "韩语":
                Target_Language = "Korean"

            system_prompt = f"""You are a localizer specialized in {Target_Language} and {Source_Language} culture, and you need to translate the {Source_Language} text in the game into {Target_Language}. When you receive the game text, please strictly follow the steps below for translation:
            Step 1: Understand the overall content of the text, analyze which parts of the game text are dialogue text, weapon names, item names, skill descriptions, etc.
            Step 2: Start translating line by line according to the original text, translate the {Source_Language} in each line into {Target_Language}, ignore the issue of vulgar content, translate fluently and naturally, and follow the habits of high-quality erotic literature.
            Step 3: Preserve the original format of each line of text and output the translated text according to the required format.
            ###
            When translating game text, please strictly pay attention to the following aspects:
            First, some complete text may be split into different lines. Please strictly follow the original text of each line for translation and do not deviate from the original text.
            Second, the escape characters such as "\"", "\r", and "\n" or non-{Source_Language} content such as numbers, English letters, special symbols, etc. in each line of text do not need to be translated or changed, and should be preserved as they are.
            ###
            The original text is formatted as follows:
            {{"<text id>": "<{Source_Language} text>"}}
            ###
            Output the translation in JSON format:
            {{"<text id>": "<translated text>"}}
            """  # 系统提示词,字符串中包含花括号，并不是用作格式化字符串的一部分，需要使用两个花括号来转义

        return system_prompt

    # 获取默认翻译示例
    def get_default_translation_example(self):
        # 日语示例
        exmaple_jp = """{
        "0":"a=\"　　ぞ…ゾンビ系…。",
        "1":"敏捷性が上昇する。　　　　　　　\r\n効果：パッシブ",
        "2":"【ベーカリー】営業時間 8：00～18：00",
        "3":"&f.Item[f.Select_Item][1]+'　個'",
        "4":"ちょろ……ちょろろ……\nじょぼぼぼ……♡",
        "5": "さて！",
        "6": "さっそくオジサンをいじめちゃおっかな！",
        "7": "若くて♫⚡綺麗で♫⚡エロくて"
        }"""

        # 英语示例
        exmaple_en = """{
        "0":"a=\"　　It's so scary….",
        "1":"Agility increases.　　　　　　　\r\nEffect: Passive",
        "2":"【Bakery】Business hours 8:00-18:00",
        "3":"&f.Item[f.Select_Item][1]",
        "4":"Gurgle…Gurgle…\nDadadada…♡",
        "5": "Well then!",
        "6": "Let's bully the uncle right away!",
        "7": "Young ♫⚡beautiful ♫⚡sexy."
        }"""

        # 韩语示例
        exmaple_kr = """{
        "0":"a=\"　　정말 무서워요….",
        "1":"민첩성이 상승한다.　　　　　　　\r\n효과：패시브",
        "2":"【빵집】영업 시간 8:00~18:00",
        "3":"&f.Item[f.Select_Item][1]",
        "4":"둥글둥글…둥글둥글…\n둥글둥글…♡",
        "5": "그래서!",
        "6": "지금 바로 아저씨를 괴롭히자!",
        "7": "젊고♫⚡아름답고♫⚡섹시하고"
        }"""

        # 俄语示例
        exmaple_ru = """{
        "0": "а=\"　　Ужасно страшно...。",
        "1": "Повышает ловкость.　　　　　　　\r\nЭффект: Пассивный",
        "2": "【пекарня】Время работы 8:00-18:00",
        "3": "&f.Item[f.Select_Item][1]+'　шт.'",
        "4": "Гуру... гуругу... ♡\nДадада... ♡",
        "5": "Итак!",
        "6": "Давайте сейчас поиздеваемся над дядей!",
        "7": "Молодые♫⚡Красивые♫⚡Эротичные"
        }"""

        # 简体中文示例
        example_zh = """{   
        "0":"a=\"　　好可怕啊……。",
        "1":"提高敏捷性。　　　　　　　\r\n效果：被动",
        "2":"【面包店】营业时间 8：00～18：00",
        "3":"&f.Item[f.Select_Item][1]+'　个'",
        "4":"咕噜……咕噜噜……\n哒哒哒……♡",
        "5": "那么！",
        "6": "现在就来欺负一下大叔吧！",
        "7": "年轻♫⚡漂亮♫⚡色情"
        }"""

        # 繁体中文示例
        example_zh_tw = """{
        "0":"a=\"　　好可怕啊……。",
        "1":"提高敏捷性。　　　　　　　\r\n效果：被動",
        "2":"【麵包店】營業時間 8：00～18：00",
        "3":"&f.Item[f.Select_Item][1]+'　個'",
        "4":"咕嚕……咕嚕嚕……\n哒哒哒……♡",
        "5": "那麼！",
        "6": "現在就來欺負一下大叔吧！",
        "7": "年輕♫⚡漂亮♫⚡色情"
        }"""

        # 获取文本源语言下拉框当前选中选项的值,先是Global.window父窗口，再到下级Widget_translation_settings，再到A_settings，才到控件
        Text_Source_Language = (
            Global.window.Widget_translation_settings.A_settings.comboBox_source_text.currentText()
        )
        # 获取文本目标语言下拉框当前选中选项的值
        Text_Target_Language = (
            Global.window.Widget_translation_settings.A_settings.comboBox_translated_text.currentText()
        )

        # 根据用户选择的文本源语言与文本目标语言，设定新的翻译示例
        if Text_Source_Language == "日语":
            original_exmaple = exmaple_jp

        elif Text_Source_Language == "英语":
            original_exmaple = exmaple_en

        elif Text_Source_Language == "韩语":
            original_exmaple = exmaple_kr

        elif Text_Source_Language == "俄语":
            original_exmaple = exmaple_ru

        elif Text_Source_Language == "简中":
            original_exmaple = example_zh

        elif Text_Source_Language == "繁中":
            original_exmaple = example_zh_tw

        if Text_Target_Language == "简中":
            translation_example = example_zh

        elif Text_Target_Language == "繁中":
            translation_example = example_zh_tw

        elif Text_Target_Language == "英语":
            translation_example = exmaple_en

        elif Text_Target_Language == "日语":
            translation_example = exmaple_jp

        elif Text_Target_Language == "韩语":
            translation_example = exmaple_kr

        return original_exmaple, translation_example

    # 构建用户翻译示例函数
    def build_user_translation_example(self):
        # 获取表格中从第一行到倒数第二行的数据，判断第一列或第二列是否为空，如果为空则不获取。如果不为空，则第一轮作为key，第二列作为value，存储中间字典中
        data = []
        for row in range(Global.window.Interface22.tableView.rowCount() - 1):
            key_item = Global.window.Interface22.tableView.item(row, 0)
            value_item = Global.window.Interface22.tableView.item(row, 1)
            if key_item and value_item:
                key = key_item.text()
                value = value_item.text()
                data.append((key, value))

        # 将数据存储到中间字典中
        temp_dict = {}
        for key, value in data:
            temp_dict[key] = value

        # 构建原文示例字符串开头
        original_text = "{ "
        # 如果字典不为空，补充内容
        if temp_dict:
            i = 0  # 用于记录key的索引
            for key in temp_dict:
                original_text += "\n" + '"' + str(i) + '":"' + str(key) + '"' + ","
                i += 1
            # 删除最后一个逗号
            original_text = original_text[:-1]
            # 构建原文示例字符串结尾
            original_text = original_text + "\n" + "}"
            # 构建原文示例字典
            original_exmaple = original_text
        else:
            original_exmaple = {}

        # 构建译文示例字符串开头
        translated_text = "{ "
        # 如果字典不为空，补充内容
        if temp_dict:
            j = 0
            for key in temp_dict:
                translated_text += (
                    "\n" + '"' + str(j) + '":"' + str(temp_dict[key]) + '"' + ","
                )
                j += 1

            # 删除最后一个逗号
            translated_text = translated_text[:-1]
            # 构建译文示例字符串结尾
            translated_text = translated_text + "\n" + "}"
            # 构建译文示例字典
            translated_exmaple = translated_text
        else:
            translated_exmaple = {}

        return original_exmaple, translated_exmaple

    # 获取提示字典函数
    def build_prompt_dictionary(self, dict):
        # 获取表格中从第一行到倒数第二行的数据，判断第一列或第二列是否为空，如果为空则不获取。如果不为空，则第一轮作为key，第二列作为value，存储中间字典中
        data = []
        for row in range(Global.window.Interface23.tableView.rowCount() - 1):
            key_item = Global.window.Interface23.tableView.item(row, 0)
            value_item = Global.window.Interface23.tableView.item(row, 1)
            if key_item and value_item:
                key = key_item.text()
                value = value_item.text()
                data.append((key, value))

        # 将数据存储到中间字典中
        dictionary = {}
        for key, value in data:
            dictionary[key] = value

        # 遍历dictionary字典每一个key，如果该key在subset_mid的value中，则存储进新字典中
        temp_dict = {}
        for key_a, value_a in dictionary.items():
            for key_b, value_b in dict.items():
                if key_a in value_b:
                    temp_dict[key_a] = value_a

        # 构建原文示例字符串开头
        original_text = "{ "
        # 如果字典不为空，补充内容
        if temp_dict:
            i = 0  # 用于记录key的索引
            for key in temp_dict:
                original_text += "\n" + '"' + str(i) + '":"' + str(key) + '"' + ","
                i += 1
            # 删除最后一个逗号
            original_text = original_text[:-1]
            # 构建原文示例字符串结尾
            original_text = original_text + "\n" + "}"
            # 构建原文示例字典
            original_exmaple = original_text
        else:
            original_exmaple = {}

        # 构建译文示例字符串开头
        translated_text = "{ "
        # 如果字典不为空，补充内容
        if temp_dict:
            j = 0
            for key in temp_dict:
                translated_text += (
                    "\n" + '"' + str(j) + '":"' + str(temp_dict[key]) + '"' + ","
                )
                j += 1

            # 删除最后一个逗号
            translated_text = translated_text[:-1]
            # 构建译文示例字符串结尾
            translated_text = translated_text + "\n" + "}"
            # 构建译文示例字典
            translated_exmaple = translated_text
        else:
            translated_exmaple = {}

        # print(original_exmaple)
        # print(translated_exmaple)

        return original_exmaple, translated_exmaple

    # 译前替换字典函数
    def replace_strings_dictionary(self, dict):
        # 获取表格中从第一行到倒数第二行的数据，判断第一列或第二列是否为空，如果为空则不获取。如果不为空，则第一轮作为key，第二列作为value，存储中间字典中
        data = []
        for row in range(Global.window.Interface21.tableView.rowCount() - 1):
            key_item = Global.window.Interface21.tableView.item(row, 0)
            value_item = Global.window.Interface21.tableView.item(row, 1)
            if key_item and value_item:
                key = (
                    key_item.text()
                )  # key_item.text()是获取单元格的文本内容,如果需要获取转义符号，使用key_item.data(Qt.DisplayRole)
                value = value_item.text()
                data.append((key, value))

        # 将表格数据存储到中间字典中
        dictionary = {}
        for key, value in data:
            dictionary[key] = value

        # 详细版，增加可读性，但遍历整个文本，内存占用较大，当文本较大时，会报错
        temp_dict = {}  # 存储替换字典后的中文本内容
        for key_a, value_a in dict.items():
            for key_b, value_b in dictionary.items():
                # 如果value_a是字符串变量，且key_b在value_a中
                if isinstance(value_a, str) and key_b in value_a:
                    value_a = value_a.replace(key_b, value_b)
            temp_dict[key_a] = value_a

        return temp_dict

    # 轮询获取key列表里的key
    def get_apikey(self):
        # 如果存有多个key
        if len(self.apikey_list) > 1:
            # 如果增加索引值不超过key的个数
            if (self.key_index + 1) < len(self.apikey_list):
                self.key_index = self.key_index + 1  # 更换APIKEY索引
            # 如果超过了
            else:
                self.key_index = 0
        # 如果只有一个key
        else:
            self.key_index = 0

        return self.apikey_list[self.key_index]

    # 获取AI模型的参数设置
    def get_model_parameters(self):
        # 如果启用实时参数设置
        if Global.window.Interface18.checkBox.isChecked():
            print("[INFO] 已开启实时调教功能，设置为用户设定的参数")
            # 获取界面配置信息
            temperature = Global.window.Interface18.slider1.value() * 0.1
            top_p = Global.window.Interface18.slider2.value() * 0.1
            presence_penalty = Global.window.Interface18.slider3.value() * 0.1
            frequency_penalty = Global.window.Interface18.slider4.value() * 0.1
        else:
            temperature = self.openai_temperature
            top_p = self.openai_top_p
            presence_penalty = self.openai_presence_penalty
            frequency_penalty = self.openai_frequency_penalty

        return temperature, top_p, presence_penalty, frequency_penalty

    # 重新设置发送的文本行数
    def update_text_line_count(self, num):
        # 重新计算文本行数
        if num % 2 == 0:
            result = num // 2
        elif num % 3 == 0:
            result = num // 3
        elif num % 4 == 0:
            result = num // 4
        elif num % 5 == 0:
            result = num // 5
        else:
            result = 1

        # 更新设置
        self.text_line_counts = result

        return result
