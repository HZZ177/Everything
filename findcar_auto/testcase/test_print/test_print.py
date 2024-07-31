#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/27 上午12:15
# @Author  : Heshouyi
# @File    : test_print.py
# @Software: PyCharm
# @description:

import logging
import allure
import pytest
import os

# 配置 logger 模块
logger = logging.getLogger('test_print_module')


class Testprint:
    def test_print(self):
        logger.info("666")


if __name__ == '__main__':
    pytest.main()
    # os.system('allure generate allure_data -o report --clean')
