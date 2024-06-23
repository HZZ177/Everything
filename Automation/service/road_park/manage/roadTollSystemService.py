# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
===================================
@FileName: roadTollSystemService.py
@Description: 路侧收费系统服务api
@Author: huangjunhao
@Software: PyCharm
@Version: 1.0
@Update:
@Copyright: 
@time:2023/05/31
===================================
"""
import datetime

import allure

from common import util, filepath, baidu_ocr_api
from common.configLog import logger
from model.road_park.road_toll_system_api import send_road_toll_system_api


class RoadTollSystemService:
    """
    路侧收费系统
    """
    def __init__(self, data=None):
        pass

    @util.catch_exception
    @util.retry_fun
    @allure.step("得到验证码信息")
    def get_verification_code_info(self, **kwargs):
        res = send_road_toll_system_api(filepath.MANAGE_GET_VERIFICATION_CODE, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200:
            logger.info("✔ 获取路侧收费系统验证码信息成功！")
            return result_dic["data"]
        else:
            raise Exception(f"❌ 获取路侧收费系统验证码失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("登录路侧收费系统")
    def login_manage(self, **kwargs):
        """

        :param kwargs: 登录所需传入关键字参，目前需要username、password
        :return:
        """

        username = kwargs.get("username") if kwargs.get("username") else \
            filepath.config.get("roadTollSystem").get("username")
        password = kwargs.get("password") if kwargs.get("password") else \
            filepath.config.get("roadTollSystem").get("password")
        password = util.encrypt_text(password)
        code_info = self.get_verification_code_info()
        uuid, base64_img = code_info['uuid'], code_info['img']
        code = baidu_ocr_api.get_code(base64_img)
        kwargs.update({"code": code, "uuid": uuid, "username": username, "password": password})
        res = send_road_toll_system_api(filepath.MANAGE_AUTH_LOGIN, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200:
            logger.info("✔ 路侧收费系统验登录成功！")
            util.save_response_to_json_file("road_toll_system_token", result_dic["data"]["token"])
            util.save_response_to_json_file("Code", result_dic["data"]["code"])
            return result_dic["data"]
        else:
            raise Exception(f"❌ 路侧收费系统登录失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("得到路侧收费系统管理端token")
    def get_manage_token(self):
        token = util.get_data_from_json_file("road_toll_system_token")
        if token:
            # token_valid_tag = check_user_token(accessToken)
            # if token_valid_tag:
            return token
        token = self.login_manage()["token"]
        return token


if __name__ == '__main__':
    park_code = "LC5001000005"
    # park_code = filepath.config.get("parkCode")
    yesterday_date = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=1), "%Y-%m-%d")
    # now = datetime.datetime.now()
    # today_start = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(days=-1)
    # today_end = today_start + datetime.timedelta(days=1) - datetime.timedelta(seconds=1)
    # yesterday_start = datetime.datetime.strftime(today_start, "%Y-%m-%d %H:%M:%S")
    # yesterday_end = datetime.datetime.strftime(today_end, "%Y-%m-%d %H:%M:%S")
    # print(Analyze().get_income_analyze(park_code, yesterday_start, yesterday_end))
    # print(Report().get_park_min_detail_day(park_code, yesterday_date, yesterday_date))