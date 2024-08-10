#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/30 下午11:30
# @Author  : Heshouyi
# @File    : util.py
# @Software: PyCharm
# @description: 通用类工具

import uuid
import functools
import time
from findcar_auto.common.log_tool import logger


def get_uuid():
    """
    创建一个32位(不带-的格式)的uuid
    :return:
    """
    return str(uuid.uuid4()).replace("-", "")


def retry(retries=3):
    """
    重试装饰器，默认重试3次
    :param retries: 重试次数，默认3次
    :return:
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            count = 0
            while count < retries:
                try:
                    logger.info(f"重试第{count}次，重试函数：{func.__name__}")
                    return func(*args, **kwargs)
                except Exception:
                    count += 1
                    if count == retries:
                        raise
                    time.sleep(1)  # 简单的等待时间，可以根据需要调整或移除
        return wrapper
    return decorator

