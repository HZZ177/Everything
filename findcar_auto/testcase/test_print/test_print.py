#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/27 上午12:15
# @Author  : Heshouyi
# @File    : test_print.py
# @Software: PyCharm
# @description:

import logging
from time import sleep

import allure
import pytest
import os
from findcar_auto.common.log_tool import logger


class Testprint:
    def test_print(self):
        logger.info("测试用例啦啦啦")
        sleep(0.5)


if __name__ == '__main__':
    pytest.main()
    # os.system('allure generate allure_data -o report --clean')
