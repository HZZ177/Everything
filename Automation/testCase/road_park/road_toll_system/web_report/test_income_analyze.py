# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
===================================
@FileName: test_income_analyze.py
@Description: 收入分析
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


class TestIncomeAnalyze:

    park_data = filepath.config.get("income_analyze")

    @allure.story("收入分析")
    @allure.title("校验收入分析昨日数据是否生成")
    # @pytest.mark.uicase
    @pytest.mark.parametrize('park_code', park_data)
    def test_income_analyze(self, park_code, setupAndTeardown):
        with allure.step(f"得到车场【{park_code}】的收入分析数据"):
            now = datetime.datetime.now()
            yesterday_date = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(days=-1)
            yesterday_end = yesterday_date + datetime.timedelta(days=1) - datetime.timedelta(seconds=1)
            yesterday_date_str = datetime.datetime.strftime(yesterday_date, "%Y-%m-%d")
            yesterday_start_time = datetime.datetime.strftime(yesterday_date, "%Y-%m-%d %H:%M:%S")
            yesterday_end_time = datetime.datetime.strftime(yesterday_end, "%Y-%m-%d %H:%M:%S")
            report_data = Analyze().get_income_analyze(park_code, yesterday_start_time, yesterday_end_time)
            assert report_data["incomeChainRate"] is not None, f"获取车场【{park_code}】昨日收入分析数据为空！"
            yesterday_info = report_data["incomeDatePoints"][-1]
            assert yesterday_info["dateString"] == yesterday_date_str, f"获取车场【{park_code}】昨日收入分析dateString字段错误！"


if __name__ == '__main__':
    pytest.main(['-sv', r'test_income_analyze.py'])