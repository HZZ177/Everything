#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/30 17:47
# @Author  : Heshouyi
# @File    : utils.py.py
# @Software: PyCharm
# @description:
import re


def is_valid_ip(ip):
    """验证IPv4地址格式"""
    ip_pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    return bool(ip_pattern.match(ip))
