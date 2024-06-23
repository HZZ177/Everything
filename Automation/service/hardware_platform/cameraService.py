# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
===================================
@FileName: cameraService.py
@Description: 相机相关服务
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
from model.hardware_platform.road_hard_ware_camera_api import send_road_hard_ware_camera_api
from service.road_park.manage.formCenter.carDetailService import CarDetailService


class CameraServer:

    @util.catch_exception
    @util.retry_fun
    @allure.step("移动运营商 - 地磁入车（默认）/出车")
    def in_out_car(self, plate, device_no, reliability=901, eventReliability=901, event_time='', eventId='',
                         eventType='3', **kwargs):
        """
        移动运营商 - 地磁入车（默认）/出车 - /hardware-platform/nbiot/nbiot/oneNetCallBack

        :param device_no: 相机编号
        :param plate: 车牌
        :param event_time: 事件时间
        :param reliability: 车牌可信度
        :param eventReliability: 车位可信度
        :param eventId: 事件Id
        :param eventType: 事件类型  入车：3（默认），出车：2
        """
        cmdTime = generate_data.time_to_unixTime(event_time) if event_time else generate_data.time_to_unixTime()
        if not eventId:
            eventId = generate_data.g_uuid()
        test_data = {
                'cmd': 'eventInfo',
                'cmdTime': cmdTime,
                'deviceId': device_no,
                'areaNum ': '2',
                'parkingNum': '2',
                'eventNum': '1',
                'eventList': [{
                    'eventId': eventId,
                    'eventType': eventType,
                    'areaIndex': '1',
                    'plate': plate,
                    'reliability': reliability,
                    'parkingUse': '2',
                    'parkingVtUse': '2',
                    'eventReliability': eventReliability,
                    'entranceId': '0',
                    'plateType': '2',
                    'carType': '',
                    'imageNum': '2',
                    'carState': '0',
                    'validity': '0'
                }]
            }
        kwargs.update(test_data)
        res = send_road_hard_ware_camera_api(filepath.HARD_WARD_PLATFORM_VIDEO_CMD_TEST, 3, header_data={}, test_data=kwargs)
        if res.status_code == 200:
            logger.info(f"✔ 车辆【{plate}】科拓相机{'入' if eventType == '3' else '出'}场成功！")
        else:
            raise Exception(f"❌ 车辆【{plate}】科拓相机{'入' if eventType == '3' else '出'}场失败！错误为【{res.text}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("相机入车")
    def camera_inCar_success(self, plate, device_no, inTime, parkspaceCode, **kwargs):
        # 入车
        self.in_out_car(plate, device_no, 901, 900, inTime)
        # 查看车位有车
        return CarDetailService().judge_parkspace_haveCar(parkspaceCode, **kwargs)

    @util.catch_exception
    @util.retry_fun
    @allure.step("相机出车")
    def camera_outCar_success(self, plate, device_no, outTime, parkspaceCode, **kwargs):
        # 出车
        self.in_out_car(plate, device_no, 901, 900, outTime, eventType='2')
        # 查看车位无车
        CarDetailService().judge_parkSpace_noCar(parkspaceCode, **kwargs)