# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
===================================
@FileName: basicInfoService.py
@Description:
车场管理
    基础信息管理
        车场管理
        路段管理
        车位管理
@Author: huangjunhao
@Software: PyCharm
@Version: 1.0
@Update:
@Copyright: 
@time:2023/06/26
===================================
"""
import allure

from common import util, filepath
from common.configLog import logger
from common.filepath import config
from model.road_park.road_toll_system_api import send_road_toll_system_api


class BasicInfoService:
    """
    车场管理--基础信息管理模块
    """

    @util.catch_exception
    @util.retry_fun
    @allure.step("添加路段")
    def road_add(self, roadName, parkCode="", longitude='', latitude='', **kwargs):
        parkCode = parkCode if parkCode else config.get("parkCode")
        test_data = {"parkCode": parkCode,
                     "roadName": roadName,
                     "longitude": longitude,
                     "latitude": latitude}
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_ADD_PARKING_ROAD, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 增加车场【{parkCode}】路段【{roadName}】成功！")
            return result_dic
        else:
            raise Exception(f"❌ 增加车场路段失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("分页查询路段")
    def get_road_info(self, parkCode="", roadCode='', roadName='', **kwargs):
        parkCode = parkCode if parkCode else config.get("parkCode")
        test_data = {"parkCode": parkCode,
                     "roadCode": roadCode,
                     "roadName": roadName}
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_GET_PARKING_ROAD_INFO, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 分页查询车场【{parkCode}】的路段信息成功！")
            return result_dic
        else:
            raise Exception(f"❌ 分页查询车场路段失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("删除路段")
    def road_disable(self, roadName='', road_id='', parkCode="", **kwargs):
        parkCode = parkCode if parkCode else config.get("parkCode")
        if not road_id:
            road_info = self.get_road_info(parkCode, roadName=roadName, **kwargs)['data']['records'][0]
            road_id = road_info.get('id')
        test_data = {"params": {
                        "id": road_id
                        }
                     }
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_DISABLE_PARKING_ROAD, 1, header_data={}, test_data=kwargs,
                                        custom_param_type=1)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            road_tag = roadName if roadName else road_id
            logger.info(f"✔ 删除车场【{parkCode}】路段【{road_tag}】成功！")
            return result_dic
        else:
            raise Exception(f"❌ 删除车场路段失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("新增单车位")
    def park_space_add(self, parkspaceCode, roadCode, parkCode="", longitude='', latitude='', **kwargs):
        """
        :param parkCode: 车场编码
        :param roadCode: 路段编码
        :param parkspaceCode: 车位编码
        :param longitude: 经度
        :param latitude: 纬度
        """
        parkCode = parkCode if parkCode else config.get("parkCode")
        test_data = {"parkCode": parkCode,
                     "parkspaceCode": parkspaceCode,
                     "roadCode": roadCode,
                     "longitude": longitude,
                     "latitude": latitude}
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_ADD_PARKING_PARK_SPACE, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 增加车场【{parkCode}】路段【{roadCode}】车位【{parkspaceCode}】成功！")
            return result_dic
        else:
            raise Exception(f"❌ 增加车场车位失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("批量新增车位")
    def parkspace_batchAdd(self, roadCode, parkspaceStartCode, batchAddNum, parkCode="", **kwargs):
        """
        :param parkCode: 车场编码
        :param roadCode: 路段编码
        :param parkspaceStartCode: 批量新增起始车位编码
        :param batchAddNum: 批量新增车位数量
        """
        parkCode = parkCode if parkCode else config.get("parkCode")
        test_data = {"parkCode": parkCode,
                     "roadCode": roadCode,
                     "parkspaceStartCode": parkspaceStartCode,
                     "batchAddNum": batchAddNum}
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_BATCH_ADD_PARKING_PARK_SPACE, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 批量增加车场【{parkCode}】路段【{roadCode}】车位成功！")
            return result_dic
        else:
            raise Exception(f"❌ 批量增加车场车位失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("分页查询车位")
    def get_park_space_info(self, roadCode, parkCode="", parkspaceCode='', **kwargs):
        """
        :param parkCode: 车场编码
        :param roadCode: 路段编码
        :param parkspaceCode: 车位编码
        """
        parkCode = parkCode if parkCode else config.get("parkCode")
        test_data = {"parkCode": parkCode,
                     "parkspaceCode": parkspaceCode,
                     "roadCode": roadCode}
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_GET_PARKING_PARK_SPACE_INFO, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 获取车场【{parkCode}】路段【{roadCode}】车位信息成功！")
            return result_dic
        else:
            raise Exception(f"❌ 获取车场车位信息失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("查询车场信息")
    def parking_page(self, parkCode="", **kwargs):
        """
        :param parkCode: 车场编码

        """
        parkCode = parkCode if parkCode else config.get("parkCode")
        test_data = {
                    "parkCode": parkCode
                     }
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_GET_PARKING_PARK_INFO, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 获取车场【{parkCode}】信息成功！")
            return result_dic
        else:
            raise Exception(f"❌ 获取车场【{parkCode}】信息失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("为路段新增车位（批量增加）")
    def add_parking_space_for_road(self, roadCode, parkSpaceStartCode, num, parkCode=""):
        """
        为路段新增车位
        @param roadCode: 路段code
        @param parkSpaceStartCode: 车位开始编码
        @param num: 车位数
        @param parkCode: 车场code 默认从配置文件中读取
        @return: 车位信息编码
        """
        parkCode = parkCode if parkCode else config.get("parkCode")
        payload = {
            'parkCode': parkCode,
            'roadCode': roadCode,
            'parkspaceStartCode': parkSpaceStartCode,
            'batchAddNum': num
        }
        with allure.step('批量新增车位'):
            self.parkspace_batchAdd(**payload)
        batch_park_space_info: list = self.get_park_space_info(**payload)['data']['records']
        return batch_park_space_info


if __name__ == '__main__':
    # from service.road_park.manage.roadTollSystemService import RoadTollSystemService
    # RoadTollSystemService().login_manage()
    # 添加路段
    # roadName = '自动化测试路段'
    # BasicInfoService().road_add(roadName)
    # road_info = BasicInfoService().get_road_info(roadName=roadName)['data']['records'][0]
    # BasicInfoService().park_space_add(road_info['roadCode'], "1")
    # BasicInfoService().get_park_space_info(roadCode="road002289")
    BasicInfoService().parking_page()