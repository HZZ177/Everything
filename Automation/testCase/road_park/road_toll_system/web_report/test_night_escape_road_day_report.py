# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
===================================
@FileName: test_night_escape_road_day_report.py
@Description: 夜间逃费
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


class TestNightEscapeRoadDayReport:

    park_data = filepath.config.get("night_escape")

    @allure.story("夜间逃费")
    @allure.title("校验夜间逃费昨日数据是否生成")
    # @pytest.mark.uicase
    @pytest.mark.parametrize('park_code', park_data)
    def test_night_escape_road_day_report(self, park_code, setupAndTeardown):
        with allure.step(f"得到车场【{park_code}】的夜间逃费数据"):
            yesterday_date = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=-1),
                                                        "%Y-%m-%d")
            report_data = Report().get_night_escape_road_day_report(park_code, yesterday_date, yesterday_date)
            assert report_data["nightEscapeRoadDayList"] is not None, f"获取车场【{park_code}】昨日夜间逃费的nightEscapeRoadDayList数据为空！"
            assert report_data["nightEscapeRoadDaySumList"] is not None, f"获取车场【{park_code}】昨日夜间逃费的nightEscapeRoadDaySumList数据为空！"
            assert report_data["nightEscapeRoadDayTotal"] is not None, f"获取车场【{park_code}】昨日夜间逃费的nightEscapeRoadDayTotal数据为空！"
            for night_escape_info in report_data["nightEscapeRoadDayList"]:
                assert night_escape_info["reportDate"] == yesterday_date, f"获取车场【{park_code}】中的路段" \
                                                                      f"【{night_escape_info['roadName']}】" \
                                                                      f"昨日夜间逃费数据中reportDate字段错误！"


if __name__ == '__main__':
    pytest.main(['-sv', r'test_night_escape_road_day_report.py'])