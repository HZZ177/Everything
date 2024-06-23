# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
===================================
@FileName: iotService.py
@Description: 移动运营商 - 地磁相关服务
@Author: huangjunhao
@Software: PyCharm
@Version: 1.0
@Update:
@Copyright: 
@time:2023/07/03
===================================
"""
import time

import allure

from common import util, filepath
from common.configLog import logger
from common.generate_data import generate_data
from model.hardware_platform.road_hard_ware_iot_api import send_road_hard_ware_iot_api
from service.road_park.manage.formCenter.carDetailService import CarDetailService


class IOTService:

    @util.catch_exception
    @util.retry_fun
    @allure.step("移动运营商 - 地磁入车（默认）/出车")
    def inout_car_oneNet(self, event_time, imei, event_type=1, **kwargs):
        """
        移动运营商 - 地磁入车（默认）/出车 - /hardware-platform/nbiot/nbiot/oneNetCallBack

        :param event_type: 事件类型 1：有车0：无车
        :param event_time: 事件时间
        :param imei: 地磁编号
        """
        at = generate_data.time_to_unixTime_ms(event_time)
        test_data = {
            'msg': {
                'at': at,
                'imei': imei,
                'type': 1,
                'ds_id': '3200_0_5750',
                'value': f'(A|{event_type}00R-86V3.3L10S176 EN{event_time} EX{event_time} M441C6849X193Y34596)',
                'dev_id': '1234'
            },
            'msg_signature': 'rSz5DyrvDFt4le4Z3hPLZw==',
            'nonce': '_qKijqYQ'
        }
        kwargs.update(test_data)
        res = send_road_hard_ware_iot_api(filepath.HARD_WARD_PLATFORM_ONE_NET_CALL_BACK, 3, header_data={}, test_data=kwargs)
        time.sleep(1)
        if res.status_code == 200:
            logger.info(f"✔ 地磁入场成功！")
        else:
            raise Exception(f"❌ 地磁入场失败！错误为【{res.text}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("地磁心跳指令")
    def iot_heart(self, at, imei, **kwargs):
        """
        地磁心跳指令

        :param at: 业务时间
        :param imei: 地磁编号
        """
        at = generate_data.time_to_unixTime_ms(at)
        test_data = {
            'msg': {
                'at': at,
                'imei': imei,
                'type': 1,
                'ds_id': '3200_0_5750',
                'value': '(H|M167C21759X202Y3254 P0E20V3.3L11T26 SP:-1015 TOP:-926 TXP:210 CD:69186627 ECL:1 SIR:46 PCI:12 RSRQ:-122)',
                'dev_id': 725759713
            },
            'msg_signature': 'cDbKGKD4AbOFyJmIKblAxA==',
            'nonce': 'b3x!ifgc'
        }
        kwargs.update(test_data)
        res = send_road_hard_ware_iot_api(filepath.HARD_WARD_PLATFORM_ONE_NET_CALL_BACK, 3, header_data={}, test_data=kwargs)
        time.sleep(1)
        if res.status_code == 200:
            logger.info(f"✔ 地磁心跳指令发送成功！")
        else:
            raise Exception(f"❌ 地磁心跳指令发送失败！错误为【{res.text}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("地磁入车")
    def nbiot_inCar_success(self, inTime, imei, parkspaceCode, **kwargs):
        self.inout_car_oneNet(inTime, imei)
        # 查看车位有车
        return CarDetailService().judge_parkspace_haveCar(parkspaceCode, **kwargs)