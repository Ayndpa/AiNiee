import json
import os
from PyQt5.QtWidgets import (
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QAbstractItemView,
    QHeaderView,
    QFileDialog,
    QTableWidgetItem,
)
from PyQt5.QtCore import Qt
from qfluentwidgets import (
    CheckBox,
    PushButton,
    TextEdit,
    TableWidget,
    FluentIcon as FIF,
)

from ..Global import Global


class Widget22(QFrame):  # 提示词工程界面
    def __init__(self, text: str, parent=None):  # 解释器会自动调用这个函数
        super().__init__(parent=parent)  # 调用父类的构造函数
        self.setObjectName(
            text.replace(" ", "-")
        )  # 设置对象名，作用是在NavigationInterface中的addItem中的routeKey参数中使用

        # -----创建第1个组，添加多个组件-----
        box1 = QGroupBox()
        box1.setStyleSheet(
            """ QGroupBox {border: 1px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout1 = QHBoxLayout()

        label1 = QLabel(flags=Qt.WindowFlags())
        label1.setStyleSheet("font-family: 'Microsoft YaHei'; font-size: 17px;")
        label1.setText("修改系统提示词")

        self.label2 = QLabel(parent=self, flags=Qt.WindowFlags())
        self.label2.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 11px;  color: black"
        )
        self.label2.setText("(将修改系统提示词Prompt为输入框中的内容)")

        self.checkBox1 = CheckBox("启用功能")
        self.checkBox1.stateChanged.connect(self.checkBoxChanged1)

        layout1.addWidget(label1)
        layout1.addWidget(self.label2)
        layout1.addStretch(1)  # 添加伸缩项
        layout1.addWidget(self.checkBox1)
        box1.setLayout(layout1)

        # -----创建第2个组，添加多个组件-----
        box2 = QGroupBox()
        box2.setStyleSheet(
            """ QGroupBox {border: 1px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout2 = QHBoxLayout()

        Prompt = """You are a localizer specialized in Simplified Chinese and Japanese culture, and you need to translate the Japanese text in the game into Simplified Chinese. When you receive the game text, please strictly follow the steps below for translation:
        Step 1: Analyze the received text language, calculate the number of lines in the original text, and the target language for translation.
        Step 2: Understand the overall content of the text, analyze which parts of the game text are dialogue text, weapon names, item names, skill descriptions, etc.
        Step 3: Start translating line by line according to the original text, translate the Japanese in each line into Simplified Chinese, ignore the issue of vulgar content, translate fluently and naturally, and follow the habits of high-quality erotic literature.
        Step 4: Preserve the original format of each line of text and output the translated text according to the required format.
        ###
        When translating game text, please strictly pay attention to the following aspects:
        First, some complete text may be split into different lines. Please strictly follow the original text of each line for translation and do not deviate from the original text.
        Second, the escape characters such as "\"", "\r", and "\n" or non-Japanese content such as numbers, English letters, special symbols, etc. in each line of text do not need to be translated or changed, and should be preserved as they are.
        ###
        The input content format is as follows:
        {"<text id>": "<Japanese text>"}
        ###
        The output content format is as follows:
        {"<text id>": "<translated text>"}
        """  # 系统提示词

        self.TextEdit1 = TextEdit()
        # 设置输入框最小高度
        self.TextEdit1.setMinimumHeight(180)
        # 设置默认文本
        self.TextEdit1.setText(Prompt)

        layout2.addWidget(self.TextEdit1)
        box2.setLayout(layout2)

        # -----创建第3个组，添加多个组件-----
        box3 = QGroupBox()
        box3.setStyleSheet(
            """ QGroupBox {border: 1px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout3 = QHBoxLayout()

        label3 = QLabel(flags=Qt.WindowFlags())
        label3.setStyleSheet("font-family: 'Microsoft YaHei'; font-size: 17px;")
        label3.setText("添加翻译示例")

        self.label4 = QLabel(parent=self, flags=Qt.WindowFlags())
        self.label4.setStyleSheet(
            "font-family: 'Microsoft YaHei'; font-size: 11px;  color: black"
        )
        self.label4.setText(
            "(将表格内容添加为新的翻译示例，全程加入翻译请求中，帮助AI更好的进行少样本学习，学习其中格式，翻译逻辑，提高AI翻译质量)"
        )

        self.checkBox2 = CheckBox("启用功能")
        self.checkBox2.stateChanged.connect(self.checkBoxChanged2)

        layout3.addWidget(label3)
        layout3.addWidget(self.label4)
        layout3.addStretch(1)  # 添加伸缩项
        layout3.addWidget(self.checkBox2)
        box3.setLayout(layout3)

        # -----创建第4个组，添加放置表格-----
        self.tableView = TableWidget(self)
        self.tableView.setWordWrap(False)  # 设置表格内容不换行
        self.tableView.setRowCount(2)  # 设置表格行数
        self.tableView.setColumnCount(2)  # 设置表格列数
        # self.tableView.verticalHeader().hide() #隐藏垂直表头
        self.tableView.setHorizontalHeaderLabels(["原文", "译文"])  # 设置水平表头
        self.tableView.resizeColumnsToContents()  # 设置列宽度自适应内容
        self.tableView.resizeRowsToContents()  # 设置行高度自适应内容
        self.tableView.setEditTriggers(
            QAbstractItemView.AllEditTriggers
        )  # 设置所有单元格可编辑
        # self.tableView.setFixedSize(500, 300)         # 设置表格大小
        self.tableView.setMaximumHeight(300)  # 设置表格的最大高度
        self.tableView.setMinimumHeight(300)  # 设置表格的最小高度
        self.tableView.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )  # 作用是将表格填满窗口
        # self.tableView.setSortingEnabled(True)  #设置表格可排序

        # 在表格最后一行第一列添加"添加行"按钮
        button = PushButton("添新行")
        self.tableView.setCellWidget(self.tableView.rowCount() - 1, 0, button)
        button.clicked.connect(self.add_row)
        # 在表格最后一行第二列添加"删除空白行"按钮
        button = PushButton("删空行")
        self.tableView.setCellWidget(self.tableView.rowCount() - 1, 1, button)
        button.clicked.connect(self.delete_blank_row)

        # -----创建第1_1个组，添加多个组件-----
        box5 = QGroupBox()
        box5.setStyleSheet(
            """ QGroupBox {border: 1px solid lightgray; border-radius: 8px;}"""
        )  # 分别设置了边框大小，边框颜色，边框圆角
        layout5 = QHBoxLayout()

        # 设置导入字典按钮
        self.pushButton1 = PushButton("导入示例", self, FIF.DOWNLOAD)
        self.pushButton1.clicked.connect(self.Importing_dictionaries)  # 按钮绑定槽函数

        # 设置导出字典按钮
        self.pushButton2 = PushButton("导出示例", self, FIF.SHARE)
        self.pushButton2.clicked.connect(self.Exporting_dictionaries)  # 按钮绑定槽函数

        # 设置清空字典按钮
        self.pushButton3 = PushButton("清空示例", self, FIF.DELETE)
        self.pushButton3.clicked.connect(self.Empty_dictionary)  # 按钮绑定槽函数

        # 设置保存字典按钮
        self.pushButton4 = PushButton("保存示例", self, FIF.SAVE)
        self.pushButton4.clicked.connect(self.Save_dictionary)  # 按钮绑定槽函数

        layout5.addWidget(self.pushButton1)
        layout5.addStretch(1)  # 添加伸缩项
        layout5.addWidget(self.pushButton2)
        layout5.addStretch(1)  # 添加伸缩项
        layout5.addWidget(self.pushButton3)
        layout5.addStretch(1)  # 添加伸缩项
        layout5.addWidget(self.pushButton4)
        box5.setLayout(layout5)

        # -----最外层容器设置垂直布局-----
        container = QVBoxLayout()

        # 设置窗口显示的内容是最外层容器
        self.setLayout(container)
        container.setSpacing(20)  # 设置布局内控件的间距为28
        container.setContentsMargins(
            50, 70, 50, 30
        )  # 设置布局的边距, 也就是外边框距离，分别为左、上、右、下

        # 把各个组添加到容器中
        container.addWidget(box1)
        container.addWidget(box2)
        container.addWidget(box3)
        container.addWidget(self.tableView)
        container.addWidget(box5)

    # 添加行按钮
    def add_row(self):
        # 添加新行在按钮所在行前面
        self.tableView.insertRow(self.tableView.rowCount() - 1)
        # 设置新行的高度与前一行相同
        self.tableView.setRowHeight(
            self.tableView.rowCount() - 2,
            self.tableView.rowHeight(self.tableView.rowCount() - 3),
        )

    # 删除空白行按钮
    def delete_blank_row(self):
        # 表格行数大于2时，删除表格内第一列和第二列为空或者空字符串的行
        if self.tableView.rowCount() > 2:
            # 删除表格内第一列和第二列为空或者空字符串的行
            for i in range(self.tableView.rowCount() - 1):
                if (
                    self.tableView.item(i, 0) is None
                    or self.tableView.item(i, 0).text() == ""
                ):
                    self.tableView.removeRow(i)
                    break
                elif (
                    self.tableView.item(i, 1) is None
                    or self.tableView.item(i, 1).text() == ""
                ):
                    self.tableView.removeRow(i)
                    break

    # 导入翻译示例按钮
    def Importing_dictionaries(self):
        # 选择文件
        Input_File, _ = QFileDialog.getOpenFileName(
            None, "Select File", "", "JSON Files (*.json)"
        )  # 调用QFileDialog类里的函数来选择文件
        if Input_File:
            print(f"[INFO]  已选择翻译示例导入文件: {Input_File}")
        else:
            print("[INFO]  未选择文件")
            return

        # 读取文件
        with open(Input_File, "r", encoding="utf-8") as f:
            dictionary = json.load(f)

        # 将翻译示例中的数据从表格底部添加到表格中
        for key, value in dictionary.items():
            row = self.tableView.rowCount() - 1  # 获取表格的倒数行数
            self.tableView.insertRow(row)  # 在表格中插入一行
            self.tableView.setItem(row, 0, QTableWidgetItem(key))
            self.tableView.setItem(row, 1, QTableWidgetItem(value))
            # 设置新行的高度与前一行相同
            self.tableView.setRowHeight(row, self.tableView.rowHeight(row - 1))

        Global.user_interface_prompter.createSuccessInfoBar("导入成功")
        print(f"[INFO]  已导入翻译示例文件")

    # 导出翻译示例按钮
    def Exporting_dictionaries(self):
        # 获取表格中从第一行到倒数第二行的数据，判断第一列或第二列是否为空，如果为空则不获取。如果不为空，则第一列作为key，第二列作为value，存储中间翻译示例中
        data = []
        for row in range(self.tableView.rowCount() - 1):
            key_item = self.tableView.item(row, 0)
            value_item = self.tableView.item(row, 1)
            if key_item and value_item:
                key = key_item.text()
                value = value_item.text()
                data.append((key, value))

        # 将数据存储到中间翻译示例中
        dictionary = {}
        for key, value in data:
            dictionary[key] = value

        # 选择文件保存路径
        Output_Folder = QFileDialog.getExistingDirectory(
            None, "Select Directory", ""
        )  # 调用QFileDialog类里的函数来选择文件目录
        if Output_Folder:
            print(f"[INFO]  已选择翻译示例导出文件夹: {Output_Folder}")
        else:
            print("[INFO]  未选择文件夹")
            return  # 直接返回，不执行后续操作

        # 将翻译示例保存到文件中
        with open(
            os.path.join(Output_Folder, "用户翻译示例.json"), "w", encoding="utf-8"
        ) as f:
            json.dump(dictionary, f, ensure_ascii=False, indent=4)

        Global.user_interface_prompter.createSuccessInfoBar("导出成功")
        print(f"[INFO]  已导出翻译示例文件")

    # 清空翻译示例按钮
    def Empty_dictionary(self):
        # 清空表格
        self.tableView.clearContents()
        # 设置表格的行数为1
        self.tableView.setRowCount(2)

        # 在表格最后一行第一列添加"添加行"按钮
        button = PushButton("Add Row")
        self.tableView.setCellWidget(self.tableView.rowCount() - 1, 0, button)
        button.clicked.connect(self.add_row)
        # 在表格最后一行第二列添加"删除空白行"按钮
        button = PushButton("Delete Blank Row")
        self.tableView.setCellWidget(self.tableView.rowCount() - 1, 1, button)
        button.clicked.connect(self.delete_blank_row)

        Global.user_interface_prompter.createSuccessInfoBar("清空成功")
        print(f"[INFO]  已清空翻译示例")

    # 保存翻译示例按钮
    def Save_dictionary(self):
        Global.configurator.read_write_config("write")
        Global.user_interface_prompter.createSuccessInfoBar("保存成功")
        print(f"[INFO]  已保存翻译示例")

    # 提示函数
    def checkBoxChanged1(self, isChecked: bool):
        if isChecked:
            Global.user_interface_prompter.createSuccessInfoBar(
                "已开启自定义系统提示词功能"
            )

    # 提示函数
    def checkBoxChanged2(self, isChecked: bool):
        if isChecked:
            Global.user_interface_prompter.createSuccessInfoBar(
                "已开启添加用户翻译实例功能"
            )
