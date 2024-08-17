#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/17 下午10:30
# @Author  : Heshouyi
# @File    : file_tool.py
# @Software: PyCharm
# @description:

import pandas as pd
from findcar_auto.common.log_tool import logger
from findcar_auto.common.config_loader import configger

config = configger.load_config()


class FileTool:
    def __init__(self, file_path):
        self.file_path = file_path

    def count_rows_excel(self):
        """
        读取Excel文件并返回行数，不计算表头
        :return: Excel文件的行数
        """
        # 读取Excel文件
        read = pd.read_excel(self.file_path)
        # 返回行数，shape属性为DataFrame的维度，其中shape[0]表示行数
        return read.shape[0]


if __name__ == '__main__':
    path = r'C:\Users\86364\PycharmProjects\Everything\findcar_auto\file\device_list_export_20240817.xlsx'
    tool = FileTool(path)
    print(tool.count_rows_excel())
