#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/21 11:06
# @Author  : Heshouyi
# @File    : file_path.py
# @Software: PyCharm
# @description:

import os


'''项目目录'''
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))      # 项目根目录，指向findcar_auto

'''一级目录'''
config_path = os.path.abspath(os.path.join(project_path, 'config'))
locust_task_path = os.path.abspath(os.path.join(project_path, 'locust_tasks'))
utils_path = os.path.abspath(os.path.join(project_path, 'utils'))


'''二级目录'''
local_config_path = os.path.abspath(os.path.join(config_path, 'local_config.yml'))
