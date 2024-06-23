# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
===================================
@FileName: LowVideoService.py
@Description: 低位视频桩相关业务逻辑
@Author: huangjunhao
@Software: PyCharm
@Version: 1.0
@Update:
@Copyright: 
@time:2023/07/04
===================================
"""
import allure

from common import filepath, util
from common.configLog import logger
from common.generate_data import generate_data
from model.hardware_platform.road_hard_ware_low_video_api import send_road_hard_ware_low_video_api
from service.road_park.manage.formCenter.carDetailService import CarDetailService


class LowVideoService:

    @util.catch_exception
    @util.retry_fun
    @allure.step("低位视频桩--入车命令")
    def in_car(self, eventId, plateReliability, plate, deviceId, inTime, carStateReliability, **kwargs):
        """
        低位视频桩--入车命令

        :param plate: 车牌
        :param eventId: 事件Id
        """
        cmdTime = generate_data.time_to_unixTime(inTime)
        test_data = {
            "deviceType": "1",
            "eventId": eventId,
            "cache": 0,
            "plateReliability": str(plateReliability),
            "plateType": "0",
            "triggerFlag": "2",
            "triggerDistance": "0",
            "imageNum": "1",
            "eleValue": "60",
            "plate": plate,
            "deviceId": deviceId,
            "triggerFlagCur": "0",
            "triggerDistanceCur": "22",
            "carType": "0",
            "at": "+CSQ: 25,99",
            "cmdTime": cmdTime,
            "carStateReliability": str(carStateReliability),
            "cmd": "ReportInfo",
            "carState": "1"
        }
        kwargs.update(test_data)
        res = send_road_hard_ware_low_video_api(filepath.HARD_WARD_PLATFORM_LOW_VIDEO_CMD_TEST, 3, header_data={}, test_data=kwargs)
        if res.status_code == 200:
            logger.info(f"✔ 车辆【{plate}】低位视频桩入场成功！")
        else:
            raise Exception(f"❌ 车辆【{plate}】低位视频桩出场失败！错误为【{res.text}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("低位视频桩--出车命令")
    def out_car(self, eventId, plateReliability, plate, deviceId, outTime, carStateReliability, **kwargs):
        """
        低位视频桩--出车命令

        :param plate: 车牌
        :param eventId: 事件Id
        """
        cmdTime = generate_data.time_to_unixTime(outTime)
        test_data = {
            "deviceType": "1",
            "eventId": eventId,
            "cache": 0,
            "plateReliability": plateReliability,
            "plateType": "0",
            "triggerFlag": "2",
            "triggerDistance": "0",
            "imageNum": "1",
            "eleValue": "50",
            "plate": plate,
            "deviceId": deviceId,
            "triggerFlagCur": "0",
            "triggerDistanceCur": "0",
            "carType": "0",
            "at": "+CSQ: 31,99",
            "cmdTime": cmdTime,
            "carStateReliability": carStateReliability,
            "cmd": "ReportInfo",
            "carState": "0"
        }
        kwargs.update(test_data)
        res = send_road_hard_ware_low_video_api(filepath.HARD_WARD_PLATFORM_LOW_VIDEO_CMD_TEST, 3, header_data={}, test_data=kwargs)
        if res.status_code == 200:
            logger.info(f"✔ 车辆【{plate}】低位视频桩出场成功！")
        else:
            raise Exception(f"❌ 车辆【{plate}】低位视频桩出场失败！错误为【{res.text}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("低位视频桩入车成功")
    def low_video_inCar_success(self, plate, device_no, inTime, parkspaceCode, **kwargs):
        # 入车
        eventId = generate_data.g_uuid()
        self.in_car(eventId, 901, plate, device_no, inTime, 900)
        # 查看车位有车
        return CarDetailService().judge_parkspace_haveCar(parkspaceCode, **kwargs)

    @util.catch_exception
    @util.retry_fun
    @allure.step("低位视频桩出车成功")
    def low_video_outCar_success(self, plate, device_no, outTime, parkspaceCode, **kwargs):
        # 出车
        eventId = generate_data.g_uuid()
        self.out_car(eventId, 901, plate, device_no, outTime, 900)
        # 查看车位无车
        CarDetailService().judge_parkSpace_noCar(parkspaceCode, **kwargs)