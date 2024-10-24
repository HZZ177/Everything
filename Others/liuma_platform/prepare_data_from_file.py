#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/10/24 17:54
# @Author  : Heshouyi
# @File    : prepare_data_from_file.py
# @Software: PyCharm
# @description: 把Excel文件里的用例编号根据模块整理成dict，方便后续脚本更新数据到平台集合中使用

import json
import openpyxl
from tkinter import Tk
from tkinter.filedialog import askopenfilename


def prepare_data_from_file():
    """
    把Excel文件里的用例编号根据模块整理成dict，方便后续脚本更新数据到平台集合中使用
    :return: dict，内部为多个tuple，数据格式：(‘父模块—子模块',[xxx,xxx])
    """
    # 创建一个Tkinter根窗口并隐藏
    Tk().withdraw()

    # 选择用例数据文件
    file_path = askopenfilename(title="请选择用例文件", filetypes=[("Excel files", "*.xlsx *.xls")])

    # 打开Excel文件
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active

    # 初始化变量
    result_dict = {}
    current_parent_module = None
    current_sub_module = None

    # 遍历表格行
    for row in sheet.iter_rows(min_row=2, values_only=True):
        parent_module = row[0]  # 父模块
        sub_module = row[1]     # 子模块
        case_number = row[5]    # 用例编号（平台对应的用例编号）

        # 如果有父模块，就更新当前父模块
        if parent_module:
            current_parent_module = parent_module

        # 如果有子模块，就更新当前子模块
        if sub_module:
            current_sub_module = sub_module

        # 如果有用例编号，处理当前模块的用例编号
        if case_number:
            # 拼接模块名作为集合名称
            key = f"{current_parent_module}—{current_sub_module}"
            if key not in result_dict:
                result_dict[key] = []
            result_dict[key].append(case_number)

    # 使用json.dumps格式化输出，缩进4个空格
    formatted_output = json.dumps(result_dict, indent=4, ensure_ascii=False)

    # for item in result_dict.items():
    #     print(item)

    return result_dict


if __name__ == '__main__':
    prepare_data_from_file()
