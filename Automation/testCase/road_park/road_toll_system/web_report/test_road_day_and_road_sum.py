# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
===================================
@FileName: test_road_day_and_road_sum.py
@Description: 路段统计
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


class TestRoadDayAndRoadSum:

    park_data = filepath.config.get("road_info")

    @allure.story("路段统计")
    @allure.title("校验路段统计昨日数据是否生成")
    # @pytest.mark.uicase
    @pytest.mark.parametrize('park_code', park_data)
    def test_road_day_and_road_sum(self, park_code, setupAndTeardown):
        with allure.step(f"得到车场【{park_code}】的路段统计数据"):
            yesterday_date = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=-1),
                                                        "%Y-%m-%d")
            report_data = Report().get_road_day_and_road_sum(park_code, yesterday_date, yesterday_date)
            assert report_data["roadDayList"] is not None, f"获取车场【{park_code}】昨日路段统计的roadDayList数据为空！"
            assert report_data["roadSumList"] is not None, f"获取车场【{park_code}】昨日路段统计的roadSumList数据为空！"
            assert report_data["totalRoadDay"] is not None, f"获取车场【{park_code}】昨日路段统计的totalRoadDay数据为空！"
            for road_info in report_data["roadDayList"]:
                assert road_info["reportDate"] == yesterday_date, f"获取车场【{park_code}】中的路段" \
                                                                          f"【{road_info['roadName']}】" \
                                                                          f"昨日路段统计数据中reportDate字段错误！"


if __name__ == '__main__':
    pytest.main(['-sv', r'test_road_day_and_road_sum.py'])