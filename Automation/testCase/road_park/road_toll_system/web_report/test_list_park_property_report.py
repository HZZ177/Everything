# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
===================================
@FileName: test_list_park_property_report.py
@Description: 固定资产盘点报表
@Author: huangjunhao
@Software: PyCharm
@Version: 1.0
@Update:
@Copyright: 
@time:2023/06/02
===================================
"""
import datetime

import allure
import pytest

from common import filepath
from service.road_park.manage.report_info.reportService import Report


class TestListParkPropertyReport:

    park_data = filepath.config.get("list_park_property")

    @allure.story("固定资产盘点报表")
    @allure.title("校验基于车场的固定资产报表昨日数据是否生成")
    # @pytest.mark.uicase
    @pytest.mark.parametrize('park_code', park_data)
    def test_list_park_property_report(self, park_code, setupAndTeardown):
        with allure.step(f"得到车场【{park_code}】的基于车场的固定资产报表数据"):
            yesterday_date = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=-1),
                                                        "%Y-%m-%d")
            report_data = Report().get_list_park_property_report(park_code, yesterday_date, yesterday_date)
            assert report_data != [], f"获取车场【{park_code}】基于车场的固定资产报表数据为空！"
            assert report_data[0]["statisticsDate"].split(" ")[0] == yesterday_date, f"获取车场【{park_code}】昨日基于车场的固定资产报表statisticsDate字段错误！"

    @allure.story("固定资产盘点报表")
    @allure.title("校验基于路段的固定资产报表昨日数据是否生成")
    # @pytest.mark.uicase
    @pytest.mark.parametrize('park_code', park_data)
    def test_list_park_property_road_report(self, park_code, setupAndTeardown):
        with allure.step(f"得到车场【{park_code}】的基于路段的固定资产报表数据"):
            yesterday_date = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=-1),
                                                        "%Y-%m-%d")
            report_data = Report().get_list_park_property_report(park_code, yesterday_date, yesterday_date)
            assert report_data != [], f"获取车场【{park_code}】基于路段的固定资产报表数据为空！"
            for road_info in report_data:
                assert road_info["statisticsDate"].split(" ")[0] == yesterday_date, f"获取车场【{park_code}】中的路段" \
                                                                      f"【{road_info['roadName']}】" \
                                                                      f"昨日基于路段的固定资产报表数据中statisticsDate字段错误！"


if __name__ == '__main__':
    pytest.main(['-sv', r'test_list_park_property_report.py'])