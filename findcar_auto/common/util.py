#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/30 下午11:30
# @Author  : Heshouyi
# @File    : util.py
# @Software: PyCharm
# @description:
import uuid


def get_uuid():
    """
    创建一个32位(不带-的格式)的uuid，作为reqId
    :return:
    """
    return str(uuid.uuid4()).replace("-", "")
