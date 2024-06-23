# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
===================================
@FileName: analyzeService.py
@Description: 分析相关api
@Author: huangjunhao
@Software: PyCharm
@Version: 1.0
@Update:
@Copyright: 
@time:2023/06/26
===================================
"""
import allure

from common import util, filepath
from common.configLog import logger
from model.road_park.road_toll_system_api import send_road_toll_system_api


class Analyze:
    """
    分析相关
    """
    def __init__(self, data=None):
        pass

    @util.catch_exception
    @util.retry_fun
    @allure.step("得到车流分析记录")
    def get_access_analyze(self, park_code, start_date, end_date, **kwargs):
        test_data = {"parkCode": park_code, "startDate": start_date, "endDate": end_date}
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_ACCESS_ANALYZE, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200:
            logger.info("✔ 获取车流分析数据成功！")
            return result_dic["data"]
        else:
            raise Exception(f"❌ 获取车流分析数据失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("得到收入分析记录")
    def get_income_analyze(self, park_code, start_date, end_date, **kwargs):
        test_data = {"parkCode": park_code, "startDate": start_date, "endDate": end_date}
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_INCOME_ANALYZE, 1, header_data={}, test_data=kwargs, timeout=20)
        result_dic = res.json()
        if result_dic["code"] == 200:
            logger.info("✔ 获取收入分析数据成功！")
            return result_dic["data"]
        else:
            raise Exception(f"❌ 获取收入分析数据失败！错误为【{result_dic}】!")