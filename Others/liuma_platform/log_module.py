#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/2 上午5:13
# @Author  : Heshouyi
# @File    : log_module.py
# @Software: PyCharm
# @description: 自定义日志工具封装

import sys
from datetime import datetime
from loguru import logger

current_date = datetime.now().strftime("%Y-%m-%d")
current_hour = datetime.now().strftime("%H")

# 自定义每个级别日志的信息头颜色
logger.level("DEBUG", color="<blue>")
logger.level("INFO", color="<green>")
logger.level("SUCCESS", color="<bold><green>")
logger.level("WARNING", color="<yellow>")
logger.level("ERROR", color="<red>")
logger.level("CRITICAL", color="<bold><red>")


# 配置自定义 logger handler，输出日志到标准输出
logger.configure(
    handlers=[
        {
            "sink": sys.stdout,  # 日志输出到标准输出
            "level": "INFO",  # 日志级别
            "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSSS} | {module}:{line}</green> | <level>{level}</level> | {message}",
            "colorize": True,  # 启用颜色
            "backtrace": False,   # 控制是否追溯详细的回溯信息（即代码调用链和变量状态等详细信息）
            "diagnose": False,    # 控制不会包含详细的诊断信息
            "enqueue": True,  # 启用多线程安全队列
        }
    ]
)

# 供其他模块引用的 logger
logger = logger
