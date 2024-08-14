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


# 统计成功、失败用例数和失败用例名称
total_tests = 0
passed_tests = 0
failed_tests = 0
failed_cases = []
success_rate = 0


def pytest_exception_interact(node, call, report):
    """
    用例执行失败时，将失败用例名称添加到failed_cases列表中
    :param node: 当前测试节点
    :param call: 测试调用信息
    :param report: 测试报告
    :return:
    """
    global failed_cases
    if report.failed:
        # 获取测试名称
        test_name = node.name
        # 获取异常信息
        exception_info = call.excinfo
        failed_cases.append(test_name)


def pytest_sessionfinish(session, exitstatus):
    """
    所有用例执行完成之后，统计执行过程中的用例执行数据
    :param session: 当前的测试会话对象，包含了有关测试会话的信息
    :param exitstatus: 测试会话的退出状态码，0表示所有测试通过，其他值表示有失败或错误
    :return:
    """
    global total_tests, passed_tests, failed_tests, success_rate
    total_tests = len(session.items)
    passed_tests = session.testscollected - session.testsfailed
    failed_tests = session.testsfailed
    success_rate = passed_tests / total_tests * 100
    # 输出执行情况
    print('\n\n###############统计自动化用例执行情况###############')
    print(f'执行测试用例总数：{total_tests}')
    print(f'通过用例数：{passed_tests}')
    print(f'失败用例数：{failed_tests}，失败用例集：{failed_cases}')
    print(f'统计执行用例成功率：{success_rate:.2f}%')


if __name__ == '__main__':
    global_session_setup()
