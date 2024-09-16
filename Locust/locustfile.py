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
from locust_tasks import plate_recognition, plate_recognition_increase
from Locust.common.config_loader import config
from Locust.common.log_tool import logger

# 全局统计变量
total_count = 0  # 识别总次数
total_successes = 0  # 识别完全正确数量
total_failures = 0  # 识别完全错误数量
chinese_part_fail = 0  # 车牌部分识别正确但汉字错误数量
total_fail_dict = {}  # 识别完全错误字典
chinese_part_fail_dict = {}  # 车牌部分识别正确但汉字错误字典
recognition_times = 0  # 识别次数统计
file_check_fail = 0  # 检查识别切割后文件失败次数

# 任务是否执行标识
plate_recognition_task = 1  # 随机识别任务
plate_recognition_and_check_file = 0    # 验证识别后车位切割图任务


class RecognitionUser(HttpUser):
    # 基础参数
    host = config.get('url').get('findcar_url')
    # wait_time = between(0.1, 0.5)

    @task
    def plate_recognition(self):
        """
        调用识别接口，随机请求图片池中的车位图，并统计识别信息
        :return:
        """
        if plate_recognition_task:
            global total_successes, chinese_part_fail, total_failures, total_fail_dict, chinese_part_fail_dict, total_count, recognition_times

            before = time.time() * 1000  # 请求开始前时间毫秒数
            flag, recognition_plate, target_plate = plate_recognition.identify_plate_randomly(self.client)
            after = time.time() * 1000
            total_count += 1
            take_time = round(after - before, 2)
            recognition_times += 1

            if flag == 1:
                total_successes += 1
            elif flag == 2:
                chinese_part_fail += 1
                chinese_part_fail_dict[target_plate] = recognition_plate
            else:
                total_failures += 1
                total_fail_dict[target_plate] = recognition_plate

            logger.info(f"当前次数{recognition_times}，当次识别耗时：{take_time} 毫秒，识别结果：{recognition_plate}")

    @task
    def plate_recognition_and_check_file(self):
        """
        调用识别接口，请求固定图片，统计识别信息，并检查每次识别后是否在对应路径下生成了切割后的车位图
        :return:
        """
        if plate_recognition_and_check_file:
            global total_successes, chinese_part_fail, total_failures, total_fail_dict, chinese_part_fail_dict, total_count, recognition_times, file_check_fail

            before = time.time() * 1000  # 请求开始前时间毫秒数
            flag, recognition_plate, target_plate, check_result = plate_recognition_increase.identify_plate_randomly(self.client)
            after = time.time() * 1000
            total_count += 1
            take_time = round(after - before, 2)
            recognition_times += 1

            # 验证切割后文件是否存在，不存在则计数
            if check_result == 2:
                file_check_fail += 1

            if flag == 1:  # 1为识别完全成功次数
                total_successes += 1
            elif flag == 2:  # 2为中文错误但车牌正确
                chinese_part_fail += 1
                chinese_part_fail_dict[target_plate] = recognition_plate
            else:  # 其余是车牌部分都识别错误
                total_failures += 1
                total_fail_dict[target_plate] = recognition_plate

            logger.info(f"当前次数{recognition_times}，当次识别耗时：{take_time} 毫秒，识别结果：{recognition_plate}")


def summary(environment, **kwargs):
    # 打印测试总结信息
    logger.info(
        '\n\n============================================测试信息汇总============================================')
    logger.info(f"识别总次数：{total_count}")
    logger.info(f"识别完全成功次数：{total_successes}，识别成功率：【{round((total_successes / total_count) * 100, 2)}%】")
    logger.info(
        f"车牌部分识别成功，但汉字识别失败次数：{chinese_part_fail},识别错误列表(正确车牌:识别结果)：{chinese_part_fail_dict}")
    logger.info(f"识别完全失败次数：{total_failures}，识别错误列表(正确车牌:识别结果)：{total_fail_dict}")

    # 获取请求统计信息
    request_stats = environment.stats.total
    total_request_count = request_stats.num_requests
    total_response_time = request_stats.total_response_time

    # 计算平均响应时间
    if total_request_count > 0:
        avg_response_time = total_response_time / total_request_count
        logger.info(f"所有请求平均响应时间：{round(avg_response_time, 2)} 毫秒")

        # 获取 50%、95%、99% 百分位数响应时间
        percentile_50 = request_stats.get_response_time_percentile(0.5)
        percentile_95 = request_stats.get_response_time_percentile(0.95)
        percentile_99 = request_stats.get_response_time_percentile(0.99)

        # 打印百分位数信息
        logger.info(f"50% 响应时间：{percentile_50} 毫秒")
        logger.info(f"95% 响应时间：{percentile_95} 毫秒")
        logger.info(f"99% 响应时间：{percentile_99} 毫秒")
    else:
        logger.info("没有完成任何请求，无法计算响应时间百分位数")

    # 统计验证切割文件失败次数
    if plate_recognition_and_check_file:
        logger.info("\n")
        logger.info(f"检测切割后文件生成失败次数：{file_check_fail}")


# 绑定统计函数到测试结束事件
events.test_stop.add_listener(summary)


if __name__ == "__main__":
    os.system("locust")
