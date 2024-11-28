#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/9 下午7:11
# @Author  : Heshouyi
# @File    : run.py.py
# @Software: PyCharm
# @description:

from app import init_app
from app.services.device_manager import DeviceManager
from app.utils.logger import logger
import sys


def main():
    # 初始化引擎
    try:
        logger.info("初始化引擎ing")
        app = init_app()
        # flask的快捷返回响应方法jsonify底层调用json.dumps，会自动排序，这里禁用掉sort_keys，否则会导致返回字典的字段顺序变化
        app.json.sort_keys = False
    except Exception as e:
        logger.exception(f"自动化引擎启动失败: {e}")
        # 注销所有设备后退出，避免设备的监听子线程阻塞主进程
        DeviceManager.shutdown_all_devices()
        sys.exit(1)

    # 初始化成功，启动flask服务
    try:
        logger.info("自动化引擎启动成功，启动flask服务")
        app.run(host="0.0.0.0", port=1777)
    except Exception as e:
        logger.exception(f"自动化引擎启动失败: {e}")
        # 注销所有设备后退出，避免设备的监听子线程阻塞主进程
        DeviceManager.shutdown_all_devices()
        sys.exit(1)


if __name__ == "__main__":
    main()
