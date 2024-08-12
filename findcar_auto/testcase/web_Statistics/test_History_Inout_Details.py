#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/12 下午11:35
# @Author  : Heshouyi
# @File    : test_History_Inout_Details.py
# @Software: PyCharm
# @description:历史进出车明细页面相关功能自动化

import allure
import pytest
from findcar_auto.common.config_loader import configger
from findcar_auto.common.log_tool import logger
from findcar_auto.model.findCarApi import findCar_admin_api
from datetime import datetime

config = configger.load_config()


class TestHistoryInoutDetails:

    @allure.story("数据统计-历史进出车明细")
    @allure.title("数据统计-历史进出车明细-默认查询当天前十个记录")
    def test_query_history_car_inout_details(self):
        logger.info("===========================【正在执行用例】===========================")
        with allure.step(f"接口查询历史进出车明细"):
            today_start = datetime.today().strftime('%Y-%m-%d 00:00:00')
            today_end = datetime.today().strftime('%Y-%m-%d 23:59:59')
            message = findCar_admin_api.query_history_car_in_out_record(lotid=1, outstarttime=today_start, outendtime=today_end, pagesize=10, pagenumber=1, token=config['Token'])
        with allure.step(f"判断查询结果"):
            assert message['message'] == '成功', f"查询失败，请检查接口返回信息：{message}"
            logger.info(f"接口查询当天前十个历史进出车明细成功，查出记录数：{message['data']['totalCount']}")
