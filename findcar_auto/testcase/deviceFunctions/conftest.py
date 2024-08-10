#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/3 下午10:21
# @Author  : Heshouyi
# @File    : conftest.py
# @Software: PyCharm
# @description:
import pytest
import allure
from findcar_auto.common.log_tool import logger


@pytest.fixture(scope="module", autouse=True)
def module_setupandteardown(request):
    request.addfinalizer(module_teardown_module)
    module_setup_module()


def module_setup_module():
    logger.info("===============================正在执行module级前置处理===============================")


def module_teardown_module():
    logger.info("===============================正在执行module级后置处理===============================")


@pytest.fixture(scope='function', autouse=True)
def set_parent_suite_name():
    """
    设置所有用例的父套件名称，方便allure报告查看，建议每个模块级的conftest都要有
    :return:
    """
    allure.dynamic.parent_suite("【设备相关】交互功能测试套")
