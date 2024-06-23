# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
===================================
@FileName: tollManService.py
@Description: 
@Author: huangjunhao
@Software: PyCharm
@Version: 1.0
@Update:
@Copyright: 
@time:2023/06/29
===================================
"""
import allure

from common import util, filepath
from common.configLog import logger
from common.filepath import config
from model.road_park.road_app_api import send_road_app_api


class TollManService:
    """
    路内停车助手App收费员相关的 api service
    """

    @util.catch_exception
    @util.retry_fun
    @allure.step("收费员登录")
    def login(self, parkCode="", **kwargs):
        """收费员登录接口

        :param parkCode: 车场编码
        """
        parkCode = parkCode if parkCode else config.get("parkCode")
        username = kwargs.get("username")
        password = kwargs.get("password")
        test_data = {"parkCode": parkCode,
                     "username": username,
                     "password": password}
        kwargs.update(test_data)
        res = send_road_app_api(filepath.TOLLMAN_LOGIN, 2, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200:
            logger.info("✔ 路内停车助手App登录成功！")
            util.save_response_to_json_file("road_app_api_token", result_dic["data"]["token"])
            return result_dic["data"]
        else:
            raise Exception(f"❌ 路内停车助手App登录失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("得到路内停车助手App token")
    def get_road_app_token(self):
        token = util.get_data_from_json_file("road_app_api_token")
        if token:
            # token_valid_tag = check_user_token(accessToken)
            # if token_valid_tag:
            return token
        token = self.login()["token"]
        return token

    @util.catch_exception
    @util.retry_fun
    @allure.step("选择工作站")
    def select_workstation(self, tollmanId, workstationId, parkCode="", **kwargs):
        """选择工作站

        :param parkCode: 车场编码
        :param tollmanId: 收费员ID
        :param workstationId: 工作站ID
        """
        parkCode = parkCode if parkCode else config.get("parkCode")
        test_data = {"parkCode": parkCode,
                     "tollmanId": tollmanId,
                     "workstationId": workstationId}
        kwargs.update(test_data)
        res = send_road_app_api(filepath.TOLLMAN_SELECT_WORKSTATION, 2, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 收费员【{tollmanId}】选择工作站【{workstationId}】成功！")
            return result_dic["data"]
        else:
            raise Exception(f"❌  收费员【{tollmanId}】选择工作站【{workstationId}】失败！错误为【{result_dic}】!")


if __name__ == '__main__':
    # TollManService().login(username="dwb007", password="dwb007")
    TollManService().select_workstation("1674336312138788865", "1462622751352295426")