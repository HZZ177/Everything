#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/3 下午9:56
# @Author  : Heshouyi
# @File    : test_Device_List.py
# @Software: PyCharm
# @description: 设备列表页面相关功能自动化

import allure
import pytest
from findcar_auto.common.config_loader import configger
from findcar_auto.common.log_tool import logger
from findcar_auto.model.findCarApi import findCar_admin_api

config = configger.load_config()


class TestDeviceList:

    @allure.story("车场维护-设备列表")
    @allure.title("车场维护-设备列表-进入默认查询1页10个设备信息")
    def test_query_floor_info(self):
        logger.info("===========================【正在执行用例】===========================")
        with allure.step(f"默认查询1页10个设备列表"):
            message = findCar_admin_api.query_deviceinfo(pagenumber=1, pagesize=10, token=config['Token'])
        with allure.step(f"判断查询结果"):
            devices_count = len(message['data']['records'])
            assert message['message'] == '成功', f"查询失败，请检查接口返回信息：{message}"
            logger.info(f"接口带参查询楼层信息成功，当前查询到的设备个数：{devices_count}")

    @allure.story("车场维护-设备列表")
    @allure.title("车场维护-设备列表-设备列表校准")
    def test_align_devices(self):
        logger.info("===========================【正在执行用例】===========================")
        with allure.step(f"接口触发设备列表校准"):
            message = findCar_admin_api.align_devices(token=config['Token'])
        with allure.step(f"判断查询结果"):
            assert message['message'] == '成功', f"查询失败，请检查接口返回信息：{message}"
            logger.info(f"校准设备列表成功，接口返回：{message}")

    @allure.story("车场维护-设备列表")
    @allure.title("车场维护-设备列表-导出设备列表")
    # todo：导出接口怎么调用？没有设置导出路径，调用直接报错
    def test_export_devicelist(self):
        logger.info("===========================【正在执行用例】===========================")
        with allure.step(f"接口触发设备列表导出"):
            message = findCar_admin_api.export_deviceList(id=1, token=config['Token'])
        with allure.step(f"判断导出结果"):
            assert message['message'] == '成功', f"查询失败，请检查接口返回信息：{message}"
            logger.info(f"导出设备列表成功，接口返回：{message}")


if __name__ == '__main__':
    pytest.main(['-sv'], ['test_Device_List.py'])
