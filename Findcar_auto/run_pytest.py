#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/27 上午2:00
# @Author  : Heshouyi
# @File    : z_run_pytest.py
# @Software: PyCharm
# @description:

import subprocess
import os
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger('z_run_pytest')


def main():

    steps = [
        "pytest --alluredir z_run_pytest/report/allure-results --clean-alluredir",
        "allure generate z_run_pytest/report/allure-results -c -o z_run_pytest/report/allure-report",
        # "allure open report/allure-report"
    ]

    for step in steps:
        if "allure open" in step:
            # 使用 Popen 来打开浏览器，其他方法会导致启动浏览器的服务一直打开，关不掉
            subprocess.Popen(step, shell=True)
        else:
            result = subprocess.run(step, shell=True)
            if result.returncode in [2, 3]:
                logger.warning(f"pytest执行过程中出错,执行返回状态码：{result.returncode}")
                break


if __name__ == "__main__":
    main()
