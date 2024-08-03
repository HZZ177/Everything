#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/2 上午5:13
# @Author  : Heshouyi
# @File    : log_tool.py
# @Software: PyCharm
# @description:

import sys
import os
from datetime import datetime

from loguru import logger
from findcar_auto.common import file_path


current_date = datetime.now().strftime("%Y-%m-%d")
current_hour = datetime.now().strftime("%H")

# 自定义每个级别的颜色
logger.level("DEBUG", color="<blue>")
logger.level("INFO", color="<green>")
logger.level("SUCCESS", color="<bold><green>")
logger.level("WARNING", color="<yellow>")
logger.level("ERROR", color="<red>")
logger.level("CRITICAL", color="<bold><red>")


# 定义并配置自定义 logger
logger.configure(
    handlers=[
        {
            "sink": sys.stdout,  # 日志输出到标准输出
            "level": "INFO",  # 日志级别
            "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSSS} | {module}</green> | <level>{level}</level> | {message}",
            "colorize": True,  # 启用颜色
            "backtrace": False,   # 控制是否追溯详细的回溯信息（即代码调用链和变量状态等详细信息）
            "diagnose": False,    # 控制不会包含详细的诊断信息
            "enqueue": True,  # 启用多线程安全队列
        },
        {
            "sink": f"{file_path.pytest_log_path}/{current_date}/pytest_{current_hour}.log",  # 指定日志输出到文件
            "level": "INFO",  # 日志级别
            "format": "{time:YYYY-MM-DD HH:mm:ss.SSSS} | {module} | {level} | {message}",  # 日志格式
            "rotation": "100 MB",  # 文件大小达到 100 MB 时自动分割日志
            "compression": None,  # 压缩日志文件
            "backtrace": True,   # 控制是否追溯详细的回溯信息（即代码调用链和变量状态等详细信息）
            "diagnose": True,  # 控制是否包含详细的诊断信息
            "enqueue": True,  # 启用多线程安全队列
        }
    ]
)

# 供其他模块引用的 logger
logger = logger
