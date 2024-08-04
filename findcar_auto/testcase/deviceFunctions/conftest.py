#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/3 下午10:21
# @Author  : Heshouyi
# @File    : conftest.py
# @Software: PyCharm
# @description:
import pytest

from findcar_auto.common.log_tool import logger


@pytest.fixture(scope="module", autouse=True)
def module_setupandteardown(request):
    request.addfinalizer(teardown_module)
    setup_module()


def setup_module():
    logger.info("===============================正在执行module级前置处理===============================")


def teardown_module():
    logger.info("===============================正在执行module级后置处理===============================")
