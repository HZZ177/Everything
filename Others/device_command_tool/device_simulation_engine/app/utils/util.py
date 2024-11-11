#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/11 17:39
# @Author  : Heshouyi
# @File    : util.py
# @Software: PyCharm
# @description:

import re


def is_valid_ip(ip):
    """验证IPv4地址格式"""
    ip_pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    return bool(ip_pattern.match(ip))