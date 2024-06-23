"""
@File    : conftest.py
@Time    : 2023/3/17/10:36
@Author  : chenyong
@Software: PyCharm
备注：
"""
import datetime

import pytest
from common import filepath
from common.configLog import logger
from common.processYaml import Yaml
import platform


@pytest.fixture()
def getPath():
    """获取此文件路径"""
    try:
        if 'Windows' == platform.system():
            filenames = __file__.split("\\")
        elif 'Linux' == platform.system():
            filenames = __file__.split("/")
        else:
            raise Exception(f"脚本暂不支持在平台【{platform.system()}】上运行")
        import_name = ".".join(filenames[filenames.index('testCase'):-1] + [filenames[-1][:-3]])
        return import_name
    except Exception as msg:
        raise Exception(logger.error(msg))


def start_operation():
    """
    自定义前置要配置的操作,一定要有此函数，内容根据用例需求配置
    """
    logger.info("=================================【【正在进行用例级别前置处理】】=================================")


def end_operation():
    """
    自定义后置要配置的操作,一定要有此函数，内容根据用例需求配置
    parameter:
    """
    logger.info("=================================【【正在进行用例级别后置处理】】=================================")


case_map = {
    "test_work_station_day_report": "工作站统计",
    "test_tollman_profit_day.py": "收费员统计",
    "test_big_order_day.py": "大额逃费",
    "test_night_escape_road_day_report.py": "夜间逃费",
    "test_access_analyze.py": "车流分析",
    "test_income_analyze.py": "收入分析",
    "test_list_park_property_report.py::TestListParkPropertyReport::test_list_park_property_report": "固定资产盘点报表-基于车场",
    "test_list_park_property_report.py::TestListParkPropertyReport::test_list_park_property_road_report": "固定资产盘点报表-基于路段",
    "test_road_day_and_road_sum.py": "路段统计",
    "test_road_escape.py": "路段逃费明细",
    "test_tollman_efficiency_day.py": "收费员效率分析",
    "test_park_min_detail_day.py": "停车时长统计",
    "test_fund_check_day.py": "资金对账表",
    "test_park_report_day.py": "运营日报"
    }

# 以下钩子函数用于判断用例是否每日报表类型，失败时触发发送机器人警告
date = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=-1), '%Y-%m-%d')
# message = f"【{date}】报表数据无异常"
message = f""
case_list = []

# def pytest_addoption(parser):
#     # 注册参数
#     parser.addoption(
#         "--platform",
#         action="store",
#         default="false",
#         choices=["false", "true"],
#         help="false：平台下发, \
#              true：定时任务, \
#              默认 false 平台下发"
#     )


def pytest_runtest_logreport(report):
    global case_list
    if report.when == 'call':
        case_list.append(report.nodeid)
    logger.info(f"########### 用例【{report.nodeid}】的执行结果为【{report.outcome}】")
    # # 用例执行中的操作
    # if report.when == 'call' and report.failed:
    #     logger.info(f"用例【{report.nodeid}】的执行结果为【{report.outcome}】")


def pytest_exception_interact(node, call, report):
    # 用例失败后的操作
    if call.excinfo is not None:
        # logger.error(f"###############【{node.nodeid}】")
        error_info = [[case_map.get(case_title), call.excinfo.value] for case_title in case_map.keys() if case_title in str(node.nodeid)]
        logger.error(error_info)
        if error_info:
            global message
            if not message:
                message = f"**<font color=\"info\">{date}</font> 报表数据存在异常:**\n"
            message += f">**<font color=\"comment\"> {error_info[0][0]}</font> : <font color=\"warning\"> {error_info[0][1]} </font>**\n"

        # logger.error(f"用例【{node.nodeid}】发生错误: 【{call.excinfo.typename}】: 【{call.excinfo.value}】")


def pytest_unconfigure(config):
    from common.wechat_robot import robot
    global message
    if config.getoption('--send_message') == "2":
        if not message:
            case_title_list = []
            for case_node in case_list:
                case_title_list += [case_map.get(case_title) for case_title in case_map.keys() if case_title in case_node]
            case_title_list = list(set(case_title_list))
            message = f"**<font color=\"info\">{date}</font> 报表数据无异常**\n"
            for case_title in case_title_list:
                message += f">**【{case_title}】**\n"
        robot.send_message(message, "markdown")
    print(message)
    # 执行全部测试用例后的操作
    print("All tests have finished running!")


if __name__ == '__main__':
    # pass
    getPath()