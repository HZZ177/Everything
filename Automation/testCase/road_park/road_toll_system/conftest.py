# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
===================================
@FileName: conftest.py
@Description: 用例前置/后置
@Author: huangjunhao
@Software: PyCharm
@Version: 1.0
@Update:
@Copyright: 
@time:2023/06/02
===================================
"""
import importlib
import traceback

import pytest

from common.configLog import logger
from service.road_park.manage import roadTollSystemService

manage_token = ""
metaclass = None


@pytest.fixture()
def setupAndTeardown(request, globalSessionSetupAndTeardown, getPath):
    """
    前后置操作
    :param 前后自带参数
    :param globalSessionSetupAndTeardown: 全局session fixture
    :param getPath 用例自带前后置
    :return:
    """
    logger.info("=================================【【正在进行前置处理】】=================================")
    try:
        # 全局session级别前置数据
        global_session_dic = globalSessionSetupAndTeardown
        # 获得用例级别conftest文件模块
        global metaclass
        import_name = getPath
        metaclass = importlib.import_module(import_name)
        # 方法前置级别的数据
        set_up_dic = setup()
        logger.info(f"当前管理平台token【{manage_token}】")
        yield {}
    except Exception as msg:
        raise Exception(logger.error(traceback.format_exc(), f"错误信息为：{msg}"))
    finally:
        pass
    logger.info("=================================【【正在进行后置处理】】=================================")
    teardown()


def setup():
    """
    前置处理函数
    :return:
    """
    try:
        start_dict = metaclass.start_operation()
        return {}
    except Exception as msg:
        raise Exception(logger.error(traceback.format_exc()))


def teardown():
    """
    后置处理函数
    :return:
    """
    try:
        end_dict = metaclass.end_operation()
    except Exception as msg:
        raise Exception(logger.error(traceback.format_exc()))


@pytest.fixture(scope="session", autouse=True)
def road_session_setup():
    # 储存收费系统管理端token
    road_toll_system_token = roadTollSystemService.RoadTollSystemService().login_manage()
    global manage_token
    manage_token = road_toll_system_token["token"]
    return {"road_toll_system_token": road_toll_system_token["token"]}