#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/30 下午10:56
# @Author  : Heshouyi
# @File    : conftest.py
# @Software: PyCharm
# @description:
from time import sleep
import pytest
from findcar_auto.common.log_tool import logger
from findcar_auto.common import login_tool
from findcar_auto.common.encrypt import encrypt_password
from findcar_auto.common.config_loader import load_config
from findcar_auto.common.file_path import test_config_path
from findcar_auto.model.findCarApi import findCar_admin_api


@pytest.fixture(scope="session", autouse=True)
def global_setup_and_teardown():
    token = global_session_setup()
    yield token
    global_session_teardown()


def login_param():
    """
    获取登录前置所需参数，传参给setup调用
    :return:
    """
    config = load_config(test_config_path)
    login_page_url = config['url']['login_url']   # 定义获取参数路径（网页）
    # todo 维护接口地址（考虑单独开文档？还是在config里维护baseurl然后在接口封装中拼接路由？）
    login_api = config['url']['login_api']  # 定义登录路径（接口）
    account = config['account']
    return login_page_url, login_api, account


def global_session_setup():
    """
    前置处理，通过selenium打开登录界面拿到关联的参数，之后通过接口登录获取返回的时效性token
    :return:超管Token
    """
    logger.info('')
    logger.info("===============================【【正在执行global级前置处理 获取超管Token】】===============================")
    login_page_url, login_api, account = login_param()
    # 解析传入的用户名密码
    username = account['username']
    password = account['password']

    # 先尝试用9999验证码登录
    params_9999 = {
        "account": f"{username}",
        "password": f"{encrypt_password(message=password)}",
        "verifyCode": "9999"
    }

    logger.info("正在尝试使用默认验证码登录")
    try:
        res = findCar_admin_api.login(url=login_api, header='', params=params_9999)
        if res['message'] == "成功":
            token = res['data']['token']
            logger.info(f"默认验证码登录成功！获取Token：{token}")
            logger.info("===============================【【前置处理完成，成功获取token】】===============================")
            return token
        else:
            logger.info("使用默认验证码登录失败，尝试ocr识别登录")
            count = 0
            while count <= 5:  # 一直重试直到使用验证码登录成功，重试次数上限为五次
                # 获取jsessionid和验证码，添加到header和请求参数中
                log_info = login_tool.get_login_info(login_page_url, username, password)
                jsessionid = log_info["jsessionid"]
                verify_code = log_info["verify_code"]
                # 定义请求头
                header = {
                    "Cookie": f"JSESSIONID={jsessionid}"
                }
                # 定义请求参数
                params = {
                    "account": f"{username}",
                    "password": f"{encrypt_password(message=password)}",
                    "verifyCode": f"{verify_code}"
                }
                # 返回消息为登录后拿到的响应
                logger.info("正在使用识别出的验证码登陆中......")
                response = findCar_admin_api.login(url=login_api, header=header, params=params)
                message = response['message']
                if message == "成功":
                    token = response['data']['token']
                    logger.info(f"登录成功！获取Token：{token}")
                    logger.info("===============================【【前置处理完成，成功获取token】】===============================")
                    return token
                elif message == "验证码错误":
                    count += 1
                    logger.info(f"验证码输入错误，正在进行第{count}次重试，获取登录参数")
                else:
                    count += 1
                    logger.info(f"发生未知错误，正在进行第{count}次重试，获取登录参数")
                if count == 6:
                    logger.exception("使用ocr识别结果调用登录接口重试5次后依然失败，请检查！！！")
    except Exception:
        logger.exception("登录失败，请检查！报错信息：")


def global_session_teardown():
    logger.info("=================================【【正在执行global级后置处理】】=================================")


if __name__ == '__main__':
    pass
