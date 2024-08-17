#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/3 下午9:56
# @Author  : Heshouyi
# @File    : test_Zone_Management.py
# @Software: PyCharm
# @description:区域管理页面相关功能自动化

import allure
import pytest
from findcar_auto.common.config_loader import configger
from findcar_auto.common.log_tool import logger
from findcar_auto.model.findCarApi import findCar_admin_api

config = configger.load_config()


class TestZoneManagement:

    @allure.story('车场维护-区域管理')
    @allure.title('车场维护-区域管理-查询区域信息')
    def test_query_areainfo(self):
        logger.info("===========================【正在执行用例】===========================")
        with allure.step(f"接口查询车场基础信息"):
            message = findCar_admin_api.query_areainfo(lotid=1, pagenumber=1, pagesize=10, token=config.get('Token'))
        with allure.step(f"判断查询结果"):
            assert message['message'] == '成功', f"查询失败，请检查接口返回信息：{message}"
            logger.info(f"接口查询车场基础信息成功，车场名称：{message}")


if __name__ == '__main__':
    pytest.main(['-sv', 'test_Zone_Management.py'])
