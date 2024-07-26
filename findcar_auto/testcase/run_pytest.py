#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/27 上午2:00
# @Author  : Heshouyi
# @File    : run_pytest.py
# @Software: PyCharm
# @description:

import subprocess
import os
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger('run_pytest')

# 设置 LANG 环境变量
# os.environ['LANG'] = 'zh_CN'


def main():
    """主函数"""

    steps = [
        "pytest --alluredir report/allure-results --clean-alluredir -p no:warnings",
        "allure generate report/allure-results -c -o report/allure-report",
        # "allure open report/allure-report"
    ]

    for step in steps:
        if "allure open" in step:
            # 使用 Popen 来打开浏览器，不等待它完成
            subprocess.Popen(step, shell=True)
        else:
            result = subprocess.run(step, shell=True)
            if result.returncode != 0:
                logger.warning(f"执行步骤出错: {step}")
                break


if __name__ == "__main__":
    main()
