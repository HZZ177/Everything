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


if __name__ == '__main__':
    # pass
    getPath()

