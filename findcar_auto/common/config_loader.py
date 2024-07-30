#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/30 下午11:55
# @Author  : Heshouyi
# @File    : config_loader.py
# @Software: PyCharm
# @description:

import yaml


def load_config(config_file):
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config

