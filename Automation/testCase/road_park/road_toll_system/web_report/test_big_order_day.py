# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
===================================
@FileName: test_big_order_day.py
@Description: 大额逃费
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
from service.road_park.manage.report_info.recordService import Record


class TestBigOrderDay:

    park_data = filepath.config.get("big_order_day")

    @allure.story("大额逃费")
    @allure.title("校验大额逃费昨日数据是否生成")
    # @pytest.mark.uicase
    @pytest.mark.parametrize('park_code', park_data)
    def test_big_order_day(self, park_code, setupAndTeardown):
        with allure.step(f"得到车场【{park_code}】的大额逃费数据"):
            yesterday_date = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=-1),
                                                        "%Y-%m-%d")
            report_data = Record().get_big_order_day(park_code, yesterday_date, yesterday_date)
            assert report_data != [], f"获取车场【{park_code}】昨日大额逃费数据为空！"
            big_order_info_list = [_ for _ in report_data if _["dateStr"] != "合计"]
            for big_order_info in big_order_info_list:
                assert big_order_info["reportDate"] == yesterday_date, f"获取车场【{park_code}】中的路段" \
                                                                      f"【{big_order_info['roadName']}】" \
                                                                      f"昨日大额逃费统计数据中reportDate字段错误！"


if __name__ == '__main__':
    pytest.main(['-sv', r'test_big_order_day.py'])