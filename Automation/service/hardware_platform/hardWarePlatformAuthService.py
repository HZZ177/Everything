# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
===================================
@FileName: authService.py
@Description: 硬件云平台认证相关服务
@Author: huangjunhao
@Software: PyCharm
@Version: 1.0
@Update:
@Copyright: 
@time:2023/07/03
===================================
"""
import allure

from common import util, filepath, baidu_ocr_api
from common.configLog import logger
from model.hardware_platform.road_hard_ware_platform_api import send_road_hard_ware_platform_api


class HardWarePlatformAuthService:
    """
    硬件云平台管理端
    """
    def __init__(self, data=None):
        pass

    @util.catch_exception
    @util.retry_fun
    @allure.step("得到硬件云平台管理端验证码信息")
    def get_verification_code_info(self, **kwargs):
        res = send_road_hard_ware_platform_api(filepath.GET_HARD_WARE_CODE, 3, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200:
            logger.info("✔ 获取硬件云平台管理端验证码信息成功！")
            return result_dic["data"]
        else:
            raise Exception(f"❌ 获取硬件云平台管理端验证码失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("登硬件云平台系统")
    def login_hard_ward_platform(self, **kwargs):
        """

        :param kwargs: 登录所需传入关键字参，目前需要username、password
        :return:
        """

        username = kwargs.get("username") if kwargs.get("username") else \
            filepath.config.get("hardware_platform").get("username")
        password = kwargs.get("password") if kwargs.get("password") else \
            filepath.config.get("hardware_platform").get("password")
        password = util.encrypt_text(password)
        code_info = self.get_verification_code_info()
        uuid, base64_img = code_info['uuid'], code_info['img']
        code = baidu_ocr_api.get_code(base64_img)
        kwargs.update({"code": code, "uuid": uuid, "username": username, "password": password})
        res = send_road_hard_ware_platform_api(filepath.LOGIN_HARD_WARD_PLATFORM, 3, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200:
            logger.info("✔ 硬件云平台管理端登录成功！")
            util.save_response_to_json_file("road_hard_ware_platform_token", result_dic["data"]["token"])
            return result_dic["data"]
        else:
            raise Exception(f"❌ 硬件云平台管理端登录失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("得到硬件云平台管理端token")
    def get_hard_ward_platform_token(self):
        token = util.get_data_from_json_file("road_hard_ware_platform_token")
        if token:
            # token_valid_tag = check_user_token(accessToken)
            # if token_valid_tag:
            return token
        token = self.login_hard_ward_platform()["token"]
        return token


if __name__ == '__main__':
    HardWarePlatformAuthService().login_hard_ward_platform()