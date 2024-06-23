# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
===================================
@FileName: test_park_report_day.py
@Description: 车场每日运营日报
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


class TestParkReportDay:

    park_data = filepath.config.get("park_report_day")

    @allure.story("车场运营日报")
    @allure.title("校验车场运营日报昨日数据是否生成")
    # @pytest.mark.uicase
    @pytest.mark.parametrize('park_code', park_data)
    def test_park_report_day(self, park_code, setupAndTeardown):
        with allure.step(f"得到车场【{park_code}】的运营日报数据"):
            yesterday_date = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=-1),
                                                        "%Y-%m-%d")
            report_data = Report().get_park_report_day(park_code, yesterday_date, yesterday_date)
            assert report_data != [], f"获取车场【{park_code}】昨日运营日报数据为空！"
            assert report_data[0]["reportDate"] == yesterday_date, f"获取车场【{park_code}】昨日运营日报reportDate字段错误！"


if __name__ == '__main__':
    pytest.main(['-sv', r'test_park_report_day.py'])