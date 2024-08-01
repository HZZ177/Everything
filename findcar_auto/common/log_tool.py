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


# 定义当前日期
current_date = datetime.now().strftime("%Y-%m-%d")

# 定义并配置自定义 logger
logger.configure(
    handlers=[
        {
            "sink": sys.stdout,  # 日志输出到标准输出
            "format": "<level>{time:YYYY-MM-DD HH:mm:ss.SSSS} | {module} | {level} |</level> {message}",  # 日志格式
            "level": "INFO",  # 日志级别
            "colorize": True  # 启用颜色
        },
        {
            "sink": f"{file_path.pytest_log_path}/{current_date}/pytest.log",  # 日志输出到文件
            "format": "{time:YYYY-MM-DD HH:mm:ss.SSSS} | {module} | {level} | {message}",  # 日志格式
            "level": "INFO",  # 日志级别
            "rotation": "50 MB",  # 文件大小达到 100 MB 时自动分割日志
            "compression": None  # 压缩日志文件
        }
    ]
)

# 供其他模块引用的 logger
logger = logger
