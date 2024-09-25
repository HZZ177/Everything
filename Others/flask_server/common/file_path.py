#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/31 下午7:21
# @Author  : Heshouyi
# @File    : file_path.py
# @Software: PyCharm
# @description: 项目各级目录

import os

'''项目目录'''
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))      # 项目根目录，指向flask_server

'''一级目录'''
common_path = os.path.abspath(os.path.join(project_path, 'common'))
log_path = os.path.abspath(os.path.join(project_path, 'log'))

'''二级目录'''


if __name__ == '__main__':
    # print(project_path)
    pass
