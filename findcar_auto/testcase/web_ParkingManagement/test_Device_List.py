#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/3 下午9:56
# @Author  : Heshouyi
# @File    : test_Device_List.py
# @Software: PyCharm
# @description: 设备列表页面相关功能自动化
import pytest

from findcar_auto.common.log_tool import logger


class TestDeviceList:

    def test_device_list(self):
        logger.info("test_Device_List")


if __name__ == '__main__':
    pytest.main(['-sv'], ['test_Device_List.py'])
