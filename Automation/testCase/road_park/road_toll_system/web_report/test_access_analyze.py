# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
===================================
@FileName: test_access_analyze.py
@Description: 车流分析
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
from service.road_park.manage.report_info.analyzeService import Analyze


class TestAccessAnalyze:

    park_data = filepath.config.get("access_analyze")

    @allure.story("车流分析")
    @allure.title("校验车流分析昨日数据是否生成")
    # @pytest.mark.uicase
    @pytest.mark.parametrize('park_code', park_data)
    def test_access_analyze(self, park_code, setupAndTeardown):
        with allure.step(f"得到车场【{park_code}】的车流分析数据"):
            yesterday_date = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=-1),
                                                        "%Y-%m-%d")
            report_data = Analyze().get_access_analyze(park_code, yesterday_date, yesterday_date)
            assert report_data["inChainRate"] is not None, f"获取车场【{park_code}】昨日入车数据为空！"
            yesterday_info = report_data["accessDatePoints"][-1]
            assert yesterday_info["dateString"] == yesterday_date, f"获取车场【{park_code}】昨日车流分析dateString字段错误！"


if __name__ == '__main__':
    pytest.main(['-sv', r'test_access_analyze.py'])