#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/3 下午9:56
# @Author  : Heshouyi
# @File    : test_Distribution_record_of_parking_lamp_scheme.py
# @Software: PyCharm
# @description: 车位灯方案下发记录页面相关功能自动化

import allure
import pytest
from findcar_auto.common.config_loader import configger
from findcar_auto.common.log_tool import logger
from findcar_auto.model.findCarApi import findCar_admin_api

config = configger.load_config()


if __name__ == '__main__':
    pytest.main(['-sv'], ['test_Distribution_record_of_parking_lamp_scheme.py'])
