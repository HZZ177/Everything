# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
===================================
@FileName: test_fund_check_day.py
@Description: 资金对账报表
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


class TestFundCheckDay:

    park_data = filepath.config.get("fund_check_day")

    @allure.story("资金对账表")
    @allure.title("校验资金对账表昨日数据是否生成")
    # @pytest.mark.uicase
    @pytest.mark.parametrize('park_code', park_data)
    def test_fund_check_day(self, park_code, setupAndTeardown):
        with allure.step(f"得到车场【{park_code}】的资金对账表数据"):
            yesterday_date = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=-1),
                                                        "%Y-%m-%d")
            report_data = Report().get_fund_check_day(park_code, yesterday_date, yesterday_date)
            assert report_data != [], f"获取车场【{park_code}】昨日资金对账表数据为空！"
            assert report_data[0]["dataTime"] == yesterday_date, f"获取车场【{park_code}】昨日资金对账表reportDate字段错误！"


if __name__ == '__main__':
    pytest.main(['-sv', r'test_fund_check_day.py'])