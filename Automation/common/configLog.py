# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
===================================
@FileName: configLog.py
@Description: 日志配置类
@Author: wurun
@Software: PyCharm
@Version: 1.0
@Update:
@Copyright:
===================================
"""

import logging
from common import filepath
import os
import warnings
from loguru import logger


class PropagateHandler(logging.Handler):
    def emit(self, record):
        logging.getLogger(record.name).handle(record)


pid = os.getpid()
logger.add(filepath.fetch_path_with_d(filepath.LOG_PATH, f'_{pid}.log'), level="INFO", encoding="utf-8",
           rotation="500 MB",
           format="{time:YYYY-MM-DD HH:mm:ss} | ThreadID: {thread.id} | {level} From 【{file}】 {module}.{function}.{line}: {message}:")
logger.add(PropagateHandler())
logger = logger

if __name__ == "__main__":
    # log = Logger()
    # print(log.get_log())
    pass
