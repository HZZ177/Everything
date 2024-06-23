# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
===================================
@FileName: test_park_min_detail_day.py
@Description: 停车时长统计
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


class TestParkMinDetailDay:

    park_data = filepath.config.get("park_min_detail")

    @allure.story("停车时长统计")
    @allure.title("校验停车时长统计昨日数据是否生成")
    # @pytest.mark.uicase
    @pytest.mark.parametrize('park_code', park_data)
    def test_park_report_min_detail_day(self, park_code, setupAndTeardown):
        with allure.step(f"得到车场【{park_code}】的停车时长统计数据"):
            yesterday_date = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=-2),
                                                        "%Y-%m-%d")
            report_data = Report().get_park_min_detail_day(park_code, yesterday_date, yesterday_date)
            assert report_data["records"] != [], f"获取车场【{park_code}】昨日停车时长统计数据为空！"


if __name__ == '__main__':
    pytest.main(['-sv', r'test_park_min_detail_day.py'])