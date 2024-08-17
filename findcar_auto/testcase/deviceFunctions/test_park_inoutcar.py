#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/2 下午10:56
# @Author  : Heshouyi
# @File    : test_park_inoutcar.py
# @Software: PyCharm
# @description:
import threading
from time import sleep

import allure
import pytest
from findcar_auto.common import util
from findcar_auto.common.config_loader import configger
from findcar_auto.common.log_tool import logger
from findcar_auto.model.findCarApi import findCar_channel_api
from findcar_auto.common.linux_server_tool import LinuxServerTool

config = configger.load_config()


class TestParkInOutCar:

    park_list = [2523602]  # 入车的车位地址列表
    carimageurl = 'http://123'  # 入车图片地址
    plateno = '川ABC123'  # 入车车牌号
    platenoreliability = None  # 入车车牌可信度

    @allure.title(f"车位{park_list}入车")
    @util.retry
    def test_park_carin(self):
        """
        对车位列表入车
        :return:
        """
        logger.info("===========================【正在执行用例】===========================")
        with allure.step(f"对车位{self.park_list}入车"):
            message = findCar_channel_api.park_enter(self.park_list, token=config.get('Token'))
        with allure.step(f"判断入车结果"):
            assert message['message'] == '成功', f"入车失败，请检查入车接口返回信息：{message}"
            logger.info(f"车位{self.park_list}入车成功")

    @allure.title(f"车位{park_list}更新车牌号")
    def test_park_updateplateno(self):
        """
        更新占用车位上的车牌号，由于接口问题无法通过接口返回assert，异步调用日志监控方法来assert
        :return:
        """
        logger.info("===========================【正在执行用例】===========================")
        for car_addr in self.park_list:
            with allure.step(f"异步线程捕获channel日志并更新车位{car_addr}车牌号"):
                with LinuxServerTool() as tool:
                    wanted_log = f"更新车牌-更新"
                    # 异步模式启动日志监控线程
                    future = tool.tail_log_file(channelservice=True, async_mode=True)
                    # 等待一秒后启动请求更新车牌接口
                    sleep(1)
                    message = findCar_channel_api.park_updateplateno(addr=car_addr, carimageurl=self.carimageurl,
                                                                     plateno=self.plateno,
                                                                     platenoreliability=self.platenoreliability,
                                                                     token=config.get('Token'))
                    # 接口请求发送之后，等待日志监控线程完成
                    logs = future.result()

            with allure.step("通过监控日志内容判断更新车牌号结果"):
                assert any(wanted_log in log for log in logs), f"更新车牌号失败，捕获到的channel日志输出：{logs}"
                logger.info(f"车位{self.park_list}更新车牌成功")

    @allure.title(f"车位{park_list}出车")
    def test_park_carleave(self):
        """
        对车位列表出车
        :return:
        """
        logger.info("===========================【正在执行用例】===========================")
        with allure.step(f"对车位{self.park_list}出车"):
            message = findCar_channel_api.park_leave(self.park_list, token=config.get('Token'))
        with allure.step(f"判断出车结果"):
            assert message['message'] == '成功', f"出车失败，请检查出车接口返回信息：{message}"
            logger.info(f"车位{self.park_list}出车成功")


if __name__ == '__main__':
    pytest.main(['-sv', 'test_park_inoutcar.py'])
