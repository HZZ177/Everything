# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
===================================
@FileName: reportService.py
@Description: 统计信息相关api
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


class Report:
    """
    统计信息
    """
    def __init__(self, data=None):
        pass

    @util.catch_exception
    @util.retry_fun
    @allure.step("得到车场运营日报")
    def get_park_report_day(self, park_code, start_date, end_date, **kwargs):
        test_data = {"parkCode": park_code, "startDate": start_date, "endDate": end_date}
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_PARK_REPORT_DAY, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200:
            logger.info("✔ 获取车场运营日报数据成功！")
            return result_dic["data"]
        else:
            raise Exception(f"❌ 获取车场运营日报数据失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("得到资金对账报表")
    def get_fund_check_day(self, park_code, start_date, end_date, **kwargs):
        test_data = {"parkCode": park_code, "startDate": start_date, "endDate": end_date}
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_FUND_CHECK_DAY, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200:
            logger.info("✔ 获取资金对账报表数据成功！")
            return result_dic["data"]
        else:
            raise Exception(f"❌ 获取资金对账报表数据失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("得到收费员统计")
    def get_toll_man_profit_day(self, park_code, start_date, end_date, **kwargs):
        test_data = {"parkCode": park_code, "startDate": start_date, "endDate": end_date}
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_TOLL_MAN_PROFIT_DAY, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200:
            logger.info("✔ 获取收费员统计数据成功！")
            return result_dic["data"]
        else:
            raise Exception(f"❌ 获取收费员统计数据失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("得到工作站统计")
    def get_work_station_day_report(self, park_code, start_date, end_date, **kwargs):
        test_data = {"parkCode": park_code, "beginTime": start_date, "endTime": end_date}
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_WORK_STATION_DAY_REPORT, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200:
            logger.info("✔ 获取工作站统计数据成功！")
            return result_dic["data"]
        else:
            raise Exception(f"❌ 获取工作站统计数据失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("得到夜间逃费")
    def get_night_escape_road_day_report(self, park_code, start_date, end_date, **kwargs):
        test_data = {"parkCode": park_code, "beginTime": start_date, "endTime": end_date}
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_NIGHT_ESCAPE_ROAD_DAY_REPORT, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200:
            logger.info("✔ 获取夜间逃费数据成功！")
            return result_dic["data"]
        else:
            raise Exception(f"❌ 获取夜间逃费数据失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("得到固定资产报表查询，基于车场")
    def get_list_park_property_report(self, park_code, start_date, end_date, **kwargs):
        test_data = {"parkCode": park_code, "beginTime": start_date, "endTime": end_date}
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_LIST_PARK_PROPERTY_REPORT, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200:
            logger.info("✔ 获取基于车场的固定资产报表数据成功！")
            return result_dic["data"]
        else:
            raise Exception(f"❌ 获取基于车场的固定资产报表数据失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("得到固定资产报表查询，基于路段")
    def get_list_park_property_road_report(self, park_code, start_date, end_date, **kwargs):
        test_data = {"parkCode": park_code, "beginTime": start_date, "endTime": end_date}
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_LIST_PARK_PROPERTY_ROAD_REPORT, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200:
            logger.info("✔ 获取基于路段的固定资产报表数据成功！")
            return result_dic["data"]
        else:
            raise Exception(f"❌ 获取基于路段的固定资产报表数据失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("得到路段统计信息")
    def get_road_day_and_road_sum(self, park_code, start_date, end_date, **kwargs):
        test_data = {"parkCode": park_code, "startDate": start_date, "endDate": end_date}
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_ROAD_DAY_AND_SUM_REPORT, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200:
            logger.info("✔ 获取路段统计数据成功！")
            return result_dic["data"]
        else:
            raise Exception(f"❌ 获取路段统计数据失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("得到路段逃费明细")
    def get_road_escape_detail(self, park_code, start_date, end_date, **kwargs):
        test_data = {"parkCode": park_code, "startDate": start_date, "endDate": end_date}
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_ROAD_ESCAPE_REPORT, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200:
            logger.info("✔ 获取路段逃费明细数据成功！")
            return result_dic["data"]
        else:
            raise Exception(f"❌ 获取路段逃费明细数据失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("得到收费员效率分析")
    def get_toll_man_efficiency_day(self, park_code, start_date, end_date, **kwargs):
        test_data = {"parkCode": park_code, "startDate": start_date, "endDate": end_date}
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_TOLL_MAN_EFFICIENCY_DAY, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200:
            logger.info("✔ 获取收费员效率分析数据成功！")
            return result_dic["data"]
        else:
            raise Exception(f"❌ 获取收费员效率分析数据失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("得到停车时长统计")
    def get_park_min_detail_day(self, park_code, start_date, end_date, **kwargs):
        test_data = {"parkCode": park_code, "startTime": start_date, "endTime": end_date}
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_PARK_MIN_DETAIL_DAY, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200:
            logger.info("✔ 获取停车时长统计数据成功！")
            return result_dic["data"]
        else:
            raise Exception(f"❌ 获取停车时长统计数据失败！错误为【{result_dic}】!")