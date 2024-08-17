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

    @allure.story("数据统计-实时车位报表")
    @allure.title("数据统计-实时车位报表-入车后查询对应实时车信息")
    @allure.description('指定车位入车，然后根据车牌号查询实时车信息，根据查询结果判定入车是否成功，最后将测试车牌出车')
    def test_query_realtime_parkinfo_with_specific_car(self):
        parklist = [2523601]
        testdata = {
            'addr': 2523601,
            'plateno': '粤A123456',
            'carimageurl': '12333',
            'platenoreliability': 900
        }
        logger.info("===========================【正在执行用例】===========================")
        with allure.step(f"指定车位入车"):
            carin_message = findCar_channel_api.park_enter(parklist=parklist, token=config.get('Token'))
            assert carin_message['message'] == '成功' or '车位入车-调用频繁', f"入车失败，请检查接口返回信息：{carin_message}"
        with allure.step(f"入车的车位更新车牌信息"):
            update_message = findCar_channel_api.park_updateplateno(**testdata, token=config.get('Token'))
            assert update_message['message'] == '成功', f"更新车牌失败，请检查接口返回信息：{update_message}"
        with allure.step(f"查询指定车牌的实时车位信息并判定结果"):
            query_message = findCar_admin_api.query_realtime_parkinfo(lotid=1, plateno=testdata.get('plateno'), pagenumber=1, pagesize=10, token=config.get('Token'))
            assert query_message['message'] == '成功', f"查询失败，请检查接口返回信息：{query_message}"
            realtime_park_count = len(query_message['data']['records'])
            query_plateno = query_message['data']['records'][0]['plateNo']
            query_parkaddr = int(query_message['data']['records'][0]['parkAddr'])
            logger.info(f"根据车牌查询实时车位表成功！根据车牌查询出的在场车数量：{realtime_park_count},车牌号 {query_plateno} 对应的第一个在场车位号为：{query_parkaddr}")
            assert realtime_park_count != 0, f"车牌号{query_plateno}没有查询到对应在场车，请检查接口返回信息：{query_message}"
            assert query_parkaddr == testdata.get('addr'), f"该次入车车牌对应查询到的车位号与入车位号不一致，请检查接口返回信息：{query_message}"
        with allure.step('指定车位出车'):
            carout_message = findCar_channel_api.park_leave(parklist=parklist, token=config.get('Token'))
            assert carout_message['message'] == '成功', f"出车失败，请检查接口返回信息：{carout_message}"
