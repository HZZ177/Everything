# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
===================================
@FileName: recordService.py
@Description: 停车记录相关api
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


class Record:
    """
    停车记录相关
    :return:
    """
    def __init__(self, data=None):
        pass

    @util.catch_exception
    @util.retry_fun
    @allure.step("得到大额逃费记录")
    def get_big_order_day(self, park_code, start_date, end_date, **kwargs):
        test_data = {"parkCode": park_code, "startDate": start_date, "endDate": end_date}
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_BIG_ORDER_QUERY_DAY_RECORD, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200:
            logger.info("✔ 获取大额逃费数据成功！")
            return result_dic["data"]
        else:
            raise Exception(f"❌ 获取大额逃费数据失败！错误为【{result_dic}】!")