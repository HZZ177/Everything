# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
===================================
@FileName: carDetailService.py
@Description:
报表中心
    车辆明细
        在场车辆
        进出车明细
        停车计费明细
        巡逻单明细
@Author: huangjunhao
@Software: PyCharm
@Version: 1.0
@Update:
@Copyright: 
@time:2023/06/26
===================================
"""
import time
from time import strftime

import allure

from common import util, filepath
from common.configLog import logger
from common.filepath import config
from model.road_park.road_toll_system_api import send_road_toll_system_api


class CarDetailService:
    """
    报表中心之车辆明细模块下的api service
    """

    @util.catch_exception
    @util.retry_fun
    @allure.step("查询欠费明细列表(分页)")
    def present_car_page(self, workstationIdList=None, tollmanIdList=None, parkCode="", **kwargs):
        """
        分页查询在场车辆信息
    
        :param workstationIdList: 工作站Id
        :param tollmanIdList: 收费员,支持多选
        :param parkCode: 车场编码
        """
        parkCode = parkCode if parkCode else config.get("parkCode")
        workstationIdList = [] if not workstationIdList else workstationIdList
        tollmanIdList = [] if not tollmanIdList else tollmanIdList
        test_data = {"workstationIdList": workstationIdList,
                     "tollmanIdList": tollmanIdList,
                     "parkCode": parkCode}
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_GET_PARKING_PRESENT_CAR_PAGE, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 查询车场【{parkCode}】在场车辆信息成功！")
            return result_dic
        else:
            raise Exception(f"❌ 查询车场【{parkCode}】在场车辆信息失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("分页查询停车计费明细列表")
    def parking_session_page(self, carNo='', outTime=None, inTime=None, roadCode='', parkspaceCode='', status='',
                             workstationIdList=None, outTollmanIdList=None, parkCode="", **kwargs):
        """
        分页查询停车计费明细列表

        :param inTime: 入车时间
        :param outTime: 出车时间
        :param carNo: 车牌
        :param roadCode: 路段
        :param parkspaceCode: 车位
        :param status: 是否缴清
        :param workstationIdList: 工作站
        :param outTollmanIdList: 收费员
        :param parkCode: 车场编码
        """
        parkCode = parkCode if parkCode else config.get("parkCode")
        outTime = (f'{outTime[0]} 00:00:00', f'{outTime[1]} 23:59:59') if outTime else ['', '']
        inTime = (f'{inTime[0]} 00:00:00', f'{inTime[1]} 23:59:59') if inTime else ['', '']
        if workstationIdList is None:
            workstationIdList = []
        if outTollmanIdList is None:
            outTollmanIdList = []
        test_data = {
            'status': status,
            'carNo': carNo,
            'roadCode': roadCode,
            'parkCode': parkCode,
            'workstationIdList': workstationIdList,
            'outTollmanIdList': outTollmanIdList,
            'parkspaceCode': parkspaceCode,
            'inTimeStart': inTime[0],
            'inTimeEnd': inTime[1],
            'outTimeStart': outTime[0],
            'outTimeEnd': outTime[1]
        }
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_LIST_PARKING_SESSION_PAGE, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 查询车场【{parkCode}】停车计费明细列表成功！")
            return result_dic
        else:
            raise Exception(f"❌ 查询车场【{parkCode}】停车计费明细列表失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("清除欠费")
    def out_car(self, carNo='', parkCode="", **kwargs):
        """
        清除欠费

        :param parkCode: 车场编码
        :param cleanMoney: 车场编码
        :param remark: 备注
        :param parkingRecordId: 停车记录id
        :param cleanTime: 清除时间
        :param nickname: 操作员名称
        :param nick_id: 操作员id
        """
        parkCode = parkCode if parkCode else config.get("parkCode")
        car_list = self.present_car_page(carNo=carNo, **kwargs)['data']['records'][0]
        logger.info(f'调试信息-web端出车前查询的在场车信息：{car_list}')
        if not car_list:
            raise Exception('没有此车')
        test_data = car_list
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_OUT_PARKING_PRESENT_CAR, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ web端出车场【{parkCode}】中的在场车【{carNo}】成功！")
            return result_dic
        else:
            raise Exception(f"❌ web端出车场【{parkCode}】中的在场车【{carNo}失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("车辆证据链")
    def evidence(self, parkingRecordId='', **kwargs):
        """
        车辆证据链

        :param parkingRecordId: 停车记录id
        """
        test_data = {
            "parkingRecordId": parkingRecordId
        }
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_GET_PARKING_EVIDENCE, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 查询停车记录【{parkingRecordId}】证据链成功！")
            return result_dic
        else:
            raise Exception(f"❌ 查询停车记录【{parkingRecordId}】证据链失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("判断收费系统后台车位有车")
    def judge_parkspace_haveCar(self, parkspaceCode, parking_info):
        """
        判断收费系统后台车位有车

        :param parkspaceCode: 车位编码
        :param parking_info: 车场信息
        """
        counts = 1
        while counts < 6:
            time.sleep(1.2)
            car_list = self.present_car_page(parkspaceCode=parkspaceCode, **parking_info)['data']['records']
            if car_list:
                return car_list[0]
            else:
                logger.error(f'调试信息-第{counts}次查询，没有查到在场车信息，车位详情：{car_list}')
            counts += 1
            if counts == 6:
                logger.error(f'调试信息-轮询结束，车位无车，车位详情：{car_list}')
                assert False, '收费系统在场车表判断车位有车错误，理论值：有车'

    @util.catch_exception
    @util.retry_fun
    @allure.step("判断收费系统后台车位无车")
    def judge_parkSpace_noCar(self, parkspaceCode, parking_info):
        """
        判断收费系统后台车位无车

        :param parkspaceCode: 车位编码
        :param parking_info: 车场信息
        """
        roadCode = parking_info['roadCode']
        counts = 1
        while counts < 6:
            time.sleep(1.5)
            car_list = self.present_car_page(roadCode=roadCode, parkspaceCode=parkspaceCode)['data'][
                'records']
            if car_list:  # 如果车位有车，输出调试信息，否则退出循环
                logger.error(f'调试信息-第{counts}次查询，有在场车信息，车位详情：{car_list}')
            else:
                return True
            counts += 1
            if counts == 6:
                logger.error(f'调试信息-轮询结束，车位有车，车位详情：{car_list}')
                assert False, '收费系统在场车表判断车位无车错误，理论值：无车'


if __name__ == '__main__':
    # from service.road_park.manage.roadTollSystemService import RoadTollSystemService
    # RoadTollSystemService().login_manage()
    # 添加路段
    roadName = '自动化测试路段'
    # BasicInfoService().road_add(roadName)
    # road_info = BasicInfoService().get_road_info(roadName=roadName)['data']['records'][0]
    # BasicInfoService().park_space_add(road_info['roadCode'], "1")
    # CarDetailService().parking_session_page(roadCode="road002289")
    CarDetailService().parking_session_page(carNo="闽GSD3AG")