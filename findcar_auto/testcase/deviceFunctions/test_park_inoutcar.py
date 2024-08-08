#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/2 下午10:56
# @Author  : Heshouyi
# @File    : test_park_inoutcar.py
# @Software: PyCharm
# @description:
import allure
import pytest

from findcar_auto.common.config_loader import configger
from findcar_auto.common.log_tool import logger
from findcar_auto.model.findCarApi import findCar_channel_api

config = configger.load_config()
token = config['Token']


class TestParkInOutCar:

    park_list = [2523601]  # 入车的车位地址列表
    carimageurl = 'http://123'  # 入车图片地址
    plateno = '川ABC123'  # 入车车牌号
    platenoreliability = None  # 入车车牌可信度

    @allure.title(f"车位{park_list}入车")
    def test_park_carin(self):
        """
        对车位列表入车
        :return:
        """
        logger.info("===========================【正在执行用例】===========================")
        with allure.step(f"对车位{self.park_list}入车"):
            message = findCar_channel_api.park_enter(self.park_list, Token=token)
        with allure.step(f"判断入车结果"):
            assert message['message'] == '成功', f"入车失败，请检查入车接口返回信息：{message}"

    @allure.title(f"车位{park_list}更新车牌号")
    def test_update_plate_number(self):
        """
        更新占用车位上的车牌号
        :return:
        """
        logger.info("===========================【正在执行用例】===========================")
        for car_addr in self.park_list:
            with allure.step(f"更新车位{car_addr}车牌号"):
                message = findCar_channel_api.park_updateplateno(addr=car_addr, carimageurl=self.carimageurl, plateno=self.plateno, platenoreliability=self.platenoreliability, Token=token)
            with allure.step("判断更新车牌号结果"):
                assert message['message'] == '成功', f"更新车牌号失败，请检查更新车牌号接口返回信息：{message}"

    @allure.title(f"车位{park_list}出车")
    def test_park_carleave(self):
        """
        对车位列表出车
        :return:
        """
        logger.info("===========================【正在执行用例】===========================")
        with allure.step(f"对车位{self.park_list}出车"):
            message = findCar_channel_api.park_leave(self.park_list, Token=token)
        with allure.step(f"判断出车结果"):
            assert message['message'] == '成功', f"出车失败，请检查出车接口返回信息：{message}"


if __name__ == '__main__':
    pytest.main(['-sv'], ['test_park_inoutcar.py'])
