# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
===================================
@FileName: test_tollman_profit_day.py
@Description: 收费员统计
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


class TestTollManProfitDay:

    park_data = filepath.config.get("toll_man_profit_day")

    @allure.story("收费员统计")
    @allure.title("校验收费员统计昨日数据是否生成")
    # @pytest.mark.uicase
    @pytest.mark.parametrize('park_code', park_data)
    def test_toll_man_profit_day(self, park_code, setupAndTeardown):
        with allure.step(f"得到车场【{park_code}】的收费员统计数据"):
            yesterday_date = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=-1),
                                                        "%Y-%m-%d")
            report_data = Report().get_toll_man_profit_day(park_code, yesterday_date, yesterday_date)
            assert report_data["tollmanDayList"] != [], f"获取车场【{park_code}】昨日收费员统计数据为空！"
            for toll_man_info in report_data["tollmanDayList"]:
                assert toll_man_info["dateString"] == yesterday_date, f"获取车场【{park_code}】中的收费员" \
                                                                      f"【{toll_man_info['tollmanName']}】" \
                                                                      f"昨日统计数据中dateString字段错误！"


if __name__ == '__main__':
    pytest.main(['-sv', r'test_toll_man_profit_day.py'])