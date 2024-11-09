#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/9 下午7:21
# @Author  : Heshouyi
# @File    : file_path.py
# @Software: PyCharm
# @description:

import os

'''项目目录'''
# 项目根目录，指向device_simulation_engine
project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

'''一级目录'''
app_path = os.path.abspath(os.path.join(project_path, 'app'))

'''二级目录'''
api_path = os.path.abspath(os.path.join(app_path, 'api'))
log_path = os.path.abspath(os.path.join(app_path, 'log'))
models_path = os.path.abspath(os.path.join(app_path, 'models'))
utils_path = os.path.abspath(os.path.join(app_path, 'utils'))


if __name__ == '__main__':
    print(project_path)
    # pass
