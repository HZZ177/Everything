# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
===================================
@FileName: conftest.py
@Description: session级别的前/后置
@Author: huangjunhao
@Software: PyCharm
@Version: 1.0
@Update:
@Copyright: 
@time:2023/05/31
===================================
"""
import datetime
import os
import sys

import pytest
from filelock import FileLock
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from common import util, filepath
from common.configLog import logger
from common.file_tool import filetool


@pytest.fixture(scope="session", autouse=True)
def globalSessionSetupAndTeardown():
    logger.info("=================================【【正在进行session级前置处理】】=================================")
    global_session_dic = globalSessionSetup()
    yield global_session_dic
    logger.info("=================================【【正在进行session级后置处理】】=================================")
    globalSessionTeardown()


def globalSessionSetup():
    with FileLock("session.lock"):
        with open(filepath.TOKEN_FILE) as f:
            content = f.read()
        if eval(content).get("session_up_tag"):
            logger.info("已执行一次session前置")
        else:
            util.save_response_to_json_file("session_up_tag", 1)
    return {}


def globalSessionTeardown():
    if util.get_data_from_json_file("session_up_tag"):
        # 更改session
        util.save_response_to_json_file("session_up_tag", 0)
        # 删除7天前的log
        filetool.del_folder(diff_day=7)
        # filetool.del_folder(file_path=filepath.NORMAL_PICTURE, diff_day=1)
        # filetool.del_folder(file_path=filepath.ERROR_PICTURE, diff_day=7)


# 以下判断是否需要发送消息
def pytest_addoption(parser):
    parser.addoption(
        "--send_message",
        action="store",
        default="0",
        help="0：不发送消息, \
              1：普通用例类消息, \
              2：报表用例类消息, \
              默认 0不发送"
    )

    parser.addoption(
        "--test_module",
        action="store",
        default="",
        help="当前运行模块名"
    )


# 得到失败用例、成功、失败用例数
failed_cases = []
passed_tests = 0
failed_tests = 0
total_tests = 0
success_rate = 0


# 捕获错误用例
def pytest_exception_interact(node, call, report):
    global failed_cases
    if report.failed:
        failed_cases.append(report)


# 得到成功、失败用例数
def pytest_sessionfinish(session, exitstatus):
    global total_tests, passed_tests, failed_tests, success_rate
    total_tests = len(session.items)
    passed_tests = session.testscollected - session.testsfailed
    failed_tests = session.testsfailed
    success_rate = passed_tests / total_tests * 100


def pytest_unconfigure(config):
    # 执行全部测试用例后的操作
    if config.getoption('--send_message') == "1":
        from common.wechat_robot import robot
        date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
        if failed_tests > 0:
            message = f"**模块 <font color=\"comment\">{config.getoption('--test_module')}</font>\n" \
                      f"<font color=\"info\">{date}</font>日常巡检用例数为【{total_tests}】，成功率为【{success_rate:.2f}%】，失败用例为：**\n"
            for report in failed_cases:
                if report.outcome != "passed":
                    message = message + f">【{report.nodeid}】\n"

        else:
            message = f"**模块 <font color=\"comment\">{config.getoption('--test_module')}</font>\n" \
                      f"<font color=\"info\">{date}</font>日常巡检用例无异常**"
        robot.send_message(message, "markdown")
    # print("##########   All tests have finished running!")
