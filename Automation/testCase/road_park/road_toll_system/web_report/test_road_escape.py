# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
===================================
@FileName: test_road_escape.py
@Description: 路段逃费明细
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


class TestRoadEscape:

    park_data = filepath.config.get("road_escape")

    @allure.story("路段逃费明细")
    @allure.title("校验路段逃费明细昨日数据是否生成")
    # @pytest.mark.uicase
    @pytest.mark.parametrize('park_code', park_data)
    def test_road_escape(self, park_code, setupAndTeardown):
        with allure.step(f"得到车场【{park_code}】的路段逃费明细数据"):
            yesterday_date = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=-1),
                                                        "%Y-%m-%d")
            report_data = Report().get_road_escape_detail(park_code, yesterday_date, yesterday_date)
            assert report_data["roadEscapeDayList"] is not None, f"获取车场【{park_code}】昨日路段逃费明细的roadEscapeDayList数据为空！"
            assert report_data["roadSumList"] is not None, f"获取车场【{park_code}】昨日路段逃费明细的roadSumList数据为空！"
            assert report_data["totalRoadEscapeDay"] is not None, f"获取车场【{park_code}】昨日路段逃费明细的totalRoadEscapeDay数据为空！"
            for road_info in report_data["roadEscapeDayList"]:
                assert road_info["dateStr"] == yesterday_date, f"获取车场【{park_code}】中的路段" \
                                                                          f"【{road_info['roadName']}】" \
                                                                          f"昨日路段统计数据中dateStr字段错误！"


if __name__ == '__main__':
    pytest.main(['-sv', r'test_road_escape.py'])