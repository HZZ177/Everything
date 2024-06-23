# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
===================================
@FileName: hardwardPlatManageService.py
@Description: 硬件云平台之平台管理模块相关serve
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
from model.hardware_platform.road_hard_ware_platform_api import send_road_hard_ware_platform_api


class HardWarePlatformManageService:
    """
    硬件云平台管理端
    """
    def __init__(self, data=None):
        pass

    @util.catch_exception
    @util.retry_fun
    @allure.step("硬件平台车位绑定页列表查询")
    def hd_parkspace_page(self, parkId, roadName, **kwargs):
        """
        硬件平台车位绑定页列表查询 - /hardware-platform/manage/manage/parkspace/page

        :param parkId: 车场id
        :param roadName: 路段名字
        """
        test_data = {
                     'parkId': parkId,
                     'roadName': roadName
                     }
        kwargs.update(test_data)
        res = send_road_hard_ware_platform_api(filepath.HARD_WARD_PLATFORM_PARK_SPACE_PAGE, 3, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 查询车场【{parkId}】硬件平台车位绑定页列表成功！")
            return result_dic
        else:
            raise Exception(f"❌ 查询车场【{parkId}】硬件平台车位绑定页列表失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("车位绑定设备（默认绑定地磁）")
    def bind(self, parkId, roadCode, parkspaceCode, deviceCode, deviceType=0, roadName='', **kwargs):
        """
        车位绑定设备（默认绑定地磁）-/hardware-platform/manage/manage/parkspace/bind

        :param deviceType: 绑定硬件类型，0:地磁（默认）2:相机3:低位视频桩
        :param deviceCode: 设备编号
        :param parkId: 车场ID
        :param parkspaceCode: 车位编码
        :param roadCode: 路段编码
        :param roadName: 路段名字
        """
        # 设备绑定车位之前查询车位是否同步成功
        payload = {
            "roadName": roadName,
            "parkId": parkId
        }
        count = 0
        while count <= 3:  # 如果车位为空，睡眠之后继续请求，请求次数+1，继续轮询
            parkspace = self.hd_parkspace_page(**payload)
            if not parkspace['data']['records']:
                time.sleep(0.7)
                count += 1
                if count == 3:
                    logger.error(f'收费系统同步车位路段信息查询失败！失败信息：{parkspace}')
            else:
                break
        payload = {
            'parkId': parkId,
            'roadName': roadName,
            'roadCode': roadCode,
            'parkspaceCode': parkspaceCode,
            'deviceCode': deviceCode,
            'deviceType': deviceType
        }
        kwargs.update(payload)
        res = send_road_hard_ware_platform_api(filepath.HARD_WARD_PLATFORM_PARK_SPACE_BIND, 3, header_data={},
                                               test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 查询车场【{parkId}】硬件平台车位绑定设备成功！")
            return result_dic
        else:
            raise Exception(f"❌ 查询车场【{parkId}】硬件平台车位绑定设备失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("解绑（批量解绑）")
    def unbind(self, parkId, parkspaceCode, roadCode, **kwargs):
        """
        解绑（批量解绑） - /hardware-platform/manage/manage/parkspace/unbind

        :param parkId: 车场ID
        :param parkspaceCode: 车位编码
        :param roadCode: 路段编码
        """
        payload = [{
            "parkId": parkId,
            "parkspaceNo": parkspaceCode,
            "roadCode": roadCode
        }]
        test_data = {
            "json": payload
        }
        res = send_road_hard_ware_platform_api(filepath.HARD_WARD_PLATFORM_PARK_SPACE_UNBIND, 3, header_data={},
                                               test_data=test_data, custom_param_type=1)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 查询车场【{parkId}】硬件平台车位解绑设备成功！")
            return result_dic
        else:
            raise Exception(f"❌ 查询车场【{parkId}】硬件平台车位解绑设备设备失败！错误为【{result_dic}】!")