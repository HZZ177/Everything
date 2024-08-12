#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/30 下午10:56
# @Author  : Heshouyi
# @File    : conftest.py
# @Software: PyCharm
# @description:
from time import sleep

import allure
import pytest
from findcar_auto.common.log_tool import logger
from findcar_auto.common import login_tool
from findcar_auto.common.config_loader import configger
from findcar_auto.model.findCarApi import findCar_admin_api

config = configger.load_config()


@pytest.fixture(scope="session", autouse=True)
def global_setup_and_teardown(request):
    """
    全局前置和后置处理
    :param request:
    :return:
    """
    request.addfinalizer(global_session_teardown)
    global_session_setup()


@allure.step("global前置，获取超管token")
def global_session_setup():
    """
    全局前置处理，通过selenium打开登录界面拿到关联的参数，之后通过接口登录获取返回的时效性token
    :return:超管Token
    """
    logger.info("\n\n")
    logger.info("===============================【正在执行global级前置处理 获取超管Token】===============================")
    login_page_url = config['url']['admin_url']+config['url']['login_page_route']   # 定义获取参数路径（网页）

    # 清空yml中的历史Token
    configger.update_config("Token", "")
    logger.info("已清空历史Token")

    # 尝试用默认验证码登录，不行就走ocr
    verify_code = "9999"
    logger.info("正在尝试使用默认验证码登录")
    try:
        res = findCar_admin_api.login(verify_code)
        if res['message'] == "成功":
            token = res['data']['token']
            logger.info(f"默认验证码登录成功！获取Token：{token}")
            configger.update_config("Token", token)
            logger.info("Token已更新到yml")
            return token
        else:
            logger.info("使用默认验证码登录失败，尝试ocr识别登录")
            count = 0
            while count <= 5:  # 一直重试直到使用验证码登录成功，重试次数上限为五次
                # 获取验证码和绑定的jsessionid
                logtool = login_tool.LogInToolTest()
                verify_code, jsessionid = logtool.get_verifycode_and_jsessionid()

                # 通过ocr结果登录
                logger.info("正在使用识别出的验证码登陆中...")
                res = findCar_admin_api.login(verify_code, jsessionid)
                message = res['message']
                if message == "成功":
                    token = res['data']['token']
                    logger.info(f"登录成功！获取Token：{token}")
                    # 更新Token到配置文件
                    configger.update_config("Token", token)
                    logger.info("Token已更新到yml")
                    break
                elif message == "验证码错误":
                    count += 1
                    logger.info(f"验证码输入错误，正在进行第{count}次重试，获取登录参数")
                else:
                    count += 1
                    logger.info(f"发生未知错误，正在进行第{count}次重试，获取登录参数")
                if count == 6:
                    logger.exception("使用ocr识别结果调用登录接口重试5次后依然失败，请检查")
                    raise Exception
    except Exception:
        logger.exception("登录失败，请检查！报错信息：")
        pytest.fail()


@allure.step("global后置")
def global_session_teardown():
    """
    全局后置处理
    :return:
    """
    logger.info("=================================【正在执行global级后置处理】=================================")


if __name__ == '__main__':
    global_session_setup()
