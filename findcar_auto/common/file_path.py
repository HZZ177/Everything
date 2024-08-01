#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/30 下午11:22
# @Author  : Heshouyi
# @File    : file_path.py
# @Software: PyCharm
# @description:

import os

'''项目目录'''
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))      # 项目根目录，指向findcar_auto

'''一级目录'''
common_path = os.path.abspath(os.path.join(project_path, 'common'))
test_case_path = os.path.abspath(os.path.join(project_path, 'testcase'))
test_data_path = os.path.abspath(os.path.join(project_path, 'testdata'))
test_file_path = os.path.abspath(os.path.join(project_path, 'file'))
pictures_path = os.path.abspath(os.path.join(project_path, 'pictures'))

'''二级目录'''
config_path = os.path.abspath(os.path.join(test_data_path, 'config'))
verify_picture_path = os.path.abspath(os.path.join(pictures_path, 'verified_picture'))
pytest_log_path = os.path.abspath(os.path.join(test_case_path, 'pytest_log'))

'''三级目录'''
test_config_path = os.path.abspath(os.path.join(config_path, 'test_config.yml'))



















