#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/3 下午9:56
# @Author  : Heshouyi
# @File    : test_Parking_Management.py
# @Software: PyCharm
# @description:车场信息管理页面相关功能自动化

import allure
import pytest

from findcar_auto.common.config_loader import configger
from findcar_auto.common.log_tool import logger
from findcar_auto.model.findCarApi import findCar_channel_api
from findcar_auto.model.findCarApi import findCar_admin_api

config = configger.load_config()
token = config['Token']


class TestParkingManagement:

    @allure.story("车场信息管理页面")
    @allure.story("车场信息管理页面-查询基础信息")
    def test_check_lotinfo(self):
        logger.info("===========================【正在执行用例】===========================")
        with allure.step(f"接口查询车场基础信息"):
            message = findCar_admin_api.get_lotinfo_byid(id=1, token=token)
        with allure.step(f"判断查询结果"):
            assert message['message'] == '成功', f"查询失败，请检查接口返回信息：{message}"
            logger.info("接口查询车场基础信息成功")
