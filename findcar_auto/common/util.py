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
    重试装饰器，需要传参重试次数
    :param retries: 重试次数
    :return:
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            count = 0
            while count < retries:
                try:
                    logger.info(f"函数 <{func.__name__}> 正在进行第{count+1}次重试")
                    return func(*args, **kwargs)
                except Exception:
                    count += 1
                    if count == retries:
                        logger.error(f"函数 <{func.__name__}> 经过{retries}次重试后仍然失败")
                        raise
                    time.sleep(1)  # 简单的等待时间，可以根据需要调整或移除
        return wrapper
    return decorator


@retry(retries=5)
def exception_test():
    raise Exception


if __name__ == '__main__':
    exception_test()
