# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
===================================
@FileName: test_work_station_day_report.py
@Description: 工作站统计
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


class TestWorkStationDayReport:

    park_data = filepath.config.get("test_work_station_day_report")

    @allure.story("工作站统计")
    @allure.title("校验工作站统计昨日数据是否生成")
    # @pytest.mark.uicase
    @pytest.mark.parametrize('park_code', park_data)
    def test_work_station_day_report(self, park_code, setupAndTeardown):
        with allure.step(f"得到车场【{park_code}】的工作站统计数据"):
            yesterday_date = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=-1),
                                                        "%Y-%m-%d")
            report_data = Report().get_work_station_day_report(park_code, yesterday_date, yesterday_date)
            assert report_data["workStationDayList"] is not None, f"获取车场【{park_code}】昨日工作站统计的workStationDayList数据为空！"
            assert report_data["workStationSumList"] is not None, f"获取车场【{park_code}】昨日工作站统计的workStationSumList数据为空！"
            assert report_data["totalWorkStationDay"] is not None, f"获取车场【{park_code}】昨日工作站统计的totalWorkStationDay数据为空！"
            for work_station_info in report_data["workStationDayList"]:
                assert work_station_info["reportDateStr"] == yesterday_date, f"获取车场【{park_code}】中的工作站" \
                                                                      f"【{work_station_info['workStationName']}】" \
                                                                      f"昨日统计数据中reportDateStr字段错误！"


if __name__ == '__main__':
    pytest.main(['-sv', r'test_work_station_day_report.py'])