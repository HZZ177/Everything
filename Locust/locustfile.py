#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/21 10:47
# @Author  : Heshouyi
# @File    : locustfile.py
# @Software: PyCharm
# @description:

import os
import time

from locust import HttpUser, task, between, events
from locust_tasks import plate_recognition
from Locust.common.config_loader import config
from Locust.common.log_tool import logger


# 全局统计变量
total_successes = 0     # 识别完全正确数量
total_failures = 0      # 识别完全错误数量
chinese_part_fail = 0   # 车牌部分识别正确但汉字错误数量
total_fail_dict = {}    # 识别完全错误字典
chinese_part_fail_dict = {}     # 车牌部分识别正确但汉字错误字典


class MyUser(HttpUser):
    host = config.get('url').get('findcar_url')
    wait_time = between(1, 1)

    @task
    def plate_recognition(self):
        global total_successes, chinese_part_fail, total_failures, total_fail_dict, chinese_part_fail_dict

        before = time.time() * 1000    # 请求开始前时间毫秒数
        flag, recognition_plate, target_plate = plate_recognition.identify_plate_randomly(self.client)
        after = time.time() * 1000
        take_time = round(after - before, 2)

        if flag == 1:
            total_successes += 1
        elif flag == 2:
            chinese_part_fail += 1
            chinese_part_fail_dict[target_plate] = recognition_plate
        else:
            total_failures += 1
            total_fail_dict[target_plate] = recognition_plate

        logger.info(f"当次识别耗时：{take_time}毫秒，识别结果：{recognition_plate}")


def summary(environment, **kwargs):
    # 打印测试总结信息
    logger.info('\n\n==================================测试信息总结==================================')
    logger.info(f"识别完全成功次数：{total_successes}")
    logger.info(f"车牌部分识别成功，但汉字识别失败次数：{chinese_part_fail},识别错误列表(正确车牌:识别结果)：{chinese_part_fail_dict}")
    logger.info(f"识别完全失败次数：{total_failures}，识别错误列表(正确车牌:识别结果)：{total_fail_dict}")


# 绑定统计函数到测试结束事件
events.test_stop.add_listener(summary)


if __name__ == "__main__":
    os.system("locust")
