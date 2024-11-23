#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/9 下午7:11
# @Author  : Heshouyi
# @File    : run.py.py
# @Software: PyCharm
# @description:

from app import create_app
from app.utils.logger import logger
import sys

app = None
try:
    app = create_app()
except Exception as e:
    logger.exception(f"自动化引擎启动失败: {e}")
    sys.exit(1)

if __name__ == "__main__":
    if app:
        logger.info("自动化引擎启动成功")
        app.run(host="0.0.0.0", port=1777)
    else:
        logger.exception("应用尚未初始化，自动化引擎启动失败")
        sys.exit(1)
