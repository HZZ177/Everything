#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/12 下午11:36
# @Author  : Heshouyi
# @File    : test_Realtime_Parking_Space_Report.py
# @Software: PyCharm
# @description: 实时车位报表页面相关功能自动化

import allure
import pytest
from findcar_auto.common.config_loader import configger
from findcar_auto.common.log_tool import logger
from findcar_auto.model.findCarApi import findCar_admin_api, findCar_channel_api, findCar_findcar_api

config = configger.load_config()


class TestRealTimeParkingSpaceReport:
    @allure.story("数据统计-实时车位报表")
    @allure.title("数据统计-实时车位报表-默认查询1页前10条实时车位信息")
    def test_query_realtime_parkinfo(self):
        logger.info("===========================【正在执行用例】===========================")
        with allure.step(f"默认查询1页10个实时车位列表"):
            message = findCar_admin_api.query_realtime_parkinfo(lotid=1, pagenumber=1, pagesize=10, token=config.get('Token'))
        with allure.step(f"判断查询结果"):
            realtime_park_count = len(message['data']['records'])
            assert message['message'] == '成功', f"查询失败，请检查接口返回信息：{message}"
            logger.info(f"接口带参查询实时车位表成功，当前查询到的实时在场车数量：{realtime_park_count}")

    # 定义一个测试用例，先用特定车牌入车到特定车位，然后查询该车位的实时车位信息，判断该车位的实时车位数据的车位和车牌是否符合
    @allure.story("数据统计-实时车位报表")
    @allure.title("数据统计-实时车位报表-查询特定车位的实时车位信息")
    def test_query_realtime_parkinfo_with_specific_car(self):
        parklist = [2523601]
        logger.info("===========================【正在执行用例】===========================")
        with allure.step(f"指定车位入车"):
            message = findCar_channel_api.park_enter(parklist=parklist, token=config.get('Token'))
        with allure.step(f"入车的车位更新车牌信息"):
            message = findCar_channel_api.park_enter(parklist=parklist, token=config.get('Token'))
        with allure.step(f"判断查询结果"):
            realtime_park_count = len(message['data']['records'])
            assert message['message'] == '成功',f"查询失败，请检查接口返回信息：{message}"
            logger.info(f"接口带参查询实时车位表成功，当前查询到的实时在场车数量：{realtime_park_count}")

