#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/30 下午10:56
# @Author  : Heshouyi
# @File    : conftest.py
# @Software: PyCharm
# @description:
import pytest
from loguru import logger


@pytest.fixture(scope='session', autouse=True)
def global_session_setup():
    logger.info("=================================【【正在执行global级前置处理】】=================================")
    # 实现登录，获取token

@pytest.fixture(scope='session', autouse=True)
def global_session_teardown():
    logger.info("=================================【【正在执行global级后置处理】】=================================")
