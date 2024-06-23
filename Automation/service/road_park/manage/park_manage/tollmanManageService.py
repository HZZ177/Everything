# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
===================================
@FileName: tollmanManageService.py
@Description:
车场管理
    收费员 管理
        收费员管理
        工作站管理
        收费员考勤
        收费员排班
@Author: huangjunhao
@Software: PyCharm
@Version: 1.0
@Update:
@Copyright: 
@time:2023/06/27
===================================
"""
import allure

from common import util, filepath
from common.configLog import logger
from common.filepath import config
from model.road_park.road_toll_system_api import send_road_toll_system_api


class TollManManageService:
    """
    车场管理之收费员管理模块下的api service
    """

    @util.catch_exception
    @util.retry_fun
    @allure.step("添加收费员")
    def add_toll_man(self, toll_man_name, username, park_code="", toll_man_id="", **kwargs):
        """
        :param park_code: 车场编码
        :param toll_man_id: 收费员id(修改时必传)
        :param toll_man_name: 收费员名字
        :param username: 收费员登录账号
        """
        park_code = park_code if park_code else config.get("parkCode")
        test_data = {"tollmanName": toll_man_name,
                     "username": username,
                     "id": toll_man_id,
                     "parkCode": park_code}
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_ADD_PARKING_TOLL_MAN, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 增加车场【{park_code}】收费员【{toll_man_name}】成功！")
            return result_dic
        else:
            raise Exception(f"❌ 增加车场收费员失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("得到收费员列表")
    def get_toll_man_list(self, username='', parkCode="", tollmanName='', status=None, **kwargs):
        """
        :param status: 收费员状态(在线、离线)
        :param tollmanName: 收费员名
        :param username: 收费员登录账号
        :param parkCode: 车场编码
        """
        park_code = parkCode if parkCode else config.get("parkCode")
        test_data = {"username": username,
                     "parkCode": park_code,
                     "tollmanName": tollmanName,
                     "status": status}
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_GET_PARKING_TOLL_MAN_INFO, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 得到车场【{park_code}】收费员列表成功！")
            return result_dic
        else:
            raise Exception(f"❌ 得到车场收费员列表失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("删除收费员")
    def disable_toll_man(self, tollmanId="", **kwargs):
        """
        :param tollmanId: 收费员id(修改时必传)
        """
        tollmanId = tollmanId if tollmanId else self.get_toll_man_list(**kwargs)['data']['records'][0]["id"]
        test_data = {"tollmanId": tollmanId}
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_DISABLE_PARKING_TOLL_MAN, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 删除收费员【{tollmanId}】成功！")
            return result_dic
        else:
            raise Exception(f"❌ 删除收费员失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("添加工作站")
    def add_workstation(self, workstationName, parkCode="", **kwargs):
        """
        :param workstationName: 工作站名称
        :param parkCode: 车场编码
        """
        parkCode = parkCode if parkCode else config.get("parkCode")
        test_data = {
                     "workStationName": workstationName,
                     "parkCode": parkCode}
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_ADD_PARKING_WORKSTATION, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 增加车场【{parkCode}】工作站【{workstationName}】成功！")
            return result_dic
        else:
            raise Exception(f"❌ 增加车场工作站失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("得到工作站列表")
    def get_workstation_list(self, workstationId='', workstationName='', parkCode="", **kwargs):
        """
        :param parkCode: 车场编码
        :param workstationId: 工作站id
        :param workstationName: 工作站名称
        """
        park_code = parkCode if parkCode else config.get("parkCode")
        test_data = {"id": workstationId,
                     "parkCode": park_code,
                     "workStationName": workstationName
                     }
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_GET_PARKING_WORKSTATION_INFO, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 得到车场【{park_code}】工作站列表成功！")
            return result_dic
        else:
            raise Exception(f"❌ 得到车场工作站列表失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("删除工作站")
    def disable_workstation(self, workstationId='', **kwargs):
        """
        :param workstationId: 工作站id
        """
        workstationId = workstationId if workstationId else self.get_workstation_list(**kwargs)['data']['records'][0]["id"]
        test_data = {"workStationId": workstationId}
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_DISABLE_PARKING_WORKSTATION, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 删除工作站【{workstationId}】成功！")
            return result_dic
        else:
            raise Exception(f"❌ 删除工作站失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("获取已绑定的收费员列表")
    def get_bound_tollman_list(self, workstationId, **kwargs):
        """
        :param workstationId: 工作站id
        """
        test_data = {"workstationId": workstationId}
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_GET_PARKING_WORKSTATION_BOUND_TOLL_MANS, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 获取工作站【{workstationId}】已绑定收费员信息成功！")
            return result_dic
        else:
            raise Exception(f"❌ 获取工作站已绑定收费员信息失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("获取已绑定的车位列表")
    def get_bound_parkings_list(self, workstationId, **kwargs):
        """
        :param workstationId: 工作站id
        """
        test_data = {"workstationId": workstationId}
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_GET_PARKING_WORKSTATION_BOUND_PARKING, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 获取工作站【{workstationId}】已绑定车位信息成功！")
            return result_dic
        else:
            raise Exception(f"❌ 获取工作站已绑定车位信息失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("修改工作站")
    def update_workstation(self, workstationId, tollmanIds=None, parkingIds=None, unbind_tollmanIds='', unbind_berthIds='',
                           workstationName='', new_workstationName='', parkCode="", **kwargs):
        """
        :param workstationId: 工作站id
        :param new_workstationName: 新工作站名称
        :param workstationName: 工作站名称
        :param tollmanIds: 新绑定的收费员id
        :param parkingIds: 新绑定的车位id
        :param unbind_tollmanIds: 解绑收费员id
        :param unbind_berthIds: 解绑车位id
        :param parkCode: 车场编码
        """
        park_code = parkCode if parkCode else config.get("parkCode")
        tollmanIds = tollmanIds if tollmanIds else []
        parkingIds = parkingIds if parkingIds else []
        if new_workstationName == '':
            new_workstationName = workstationName
        # 工作站已绑定的收费员
        tollman_data = self.get_bound_tollman_list(workstationId)['data']
        bind_tollmanIds, bind_parkingIds = [], []
        if tollmanIds:  # 如果绑定收费员为list，那么就 extend 进去，如果是str，就 append 进去
            if isinstance(tollmanIds, list):
                bind_tollmanIds.extend(tollmanIds)
            else:
                bind_tollmanIds.append(tollmanIds)
        if tollman_data:
            [bind_tollmanIds.append(tollman['id']) for tollman in tollman_data]
        # 工作站已绑定的车位
        parking_data = self.get_bound_parkings_list(workstationId)['data']
        if parkingIds:  # 如果绑定车位为list，那么就 extend 进去，如果是str，就 append 进去
            if isinstance(parkingIds, list):
                bind_parkingIds.extend(parkingIds)
            else:
                bind_parkingIds.append(parkingIds)
        if parking_data:
            [bind_parkingIds.append(parking['id']) for parking in parking_data]
        if unbind_tollmanIds:
            bind_tollmanIds.remove(unbind_tollmanIds)
        if unbind_berthIds:
            if isinstance(unbind_berthIds, list):
                [bind_parkingIds.remove(parking_id) for parking_id in unbind_berthIds]
            else:
                bind_parkingIds.remove(unbind_berthIds)
        test_data = {"id": workstationId,
                     "workStationName": new_workstationName,
                     "parkCode": park_code,
                     "parkingIds": list(set(bind_parkingIds)),
                     "tollmanIds": bind_tollmanIds
                     }
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_UPDATE_PARKING_WORKSTATION, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 修改工作站【{workstationId}】信息成功！")
            return result_dic
        else:
            raise Exception(f"❌ 修改工作站信息失败！错误为【{result_dic}】!")


if __name__ == '__main__':
    # from service.road_park.manage.roadTollSystemService import RoadTollSystemService
    # RoadTollSystemService().login_manage()
    tollmanName = 'dwb007'
    TollManManageService().add_toll_man(tollmanName, tollmanName)
