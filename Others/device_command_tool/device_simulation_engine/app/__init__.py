#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/9 下午7:10
# @Author  : Heshouyi
# @File    : __init__.py.py
# @Software: PyCharm
# @description:

import socket
import psutil
from flask import Flask
from .api.channel_camera_api import channel_camera_bp
from .api.network_led_api import network_led_bp
from .api.parking_camera_api import parking_camera_bp
from .api.lora_node_api import lora_node_bp
from .api.four_bytes_node_api import four_bytes_node_bp
from .utils.logger import logger
from .utils.configer import config
from .services.channel_camera_service import ChannelCameraService
from .services.network_led_service import NetworkLedService
from .services.parking_camera_service import ParkingCameraService
from .services.lora_node_service import LoraNodeService
from .services.device_manager import DeviceManager


def get_all_local_ips():
    """获取本机所有网卡的IP地址"""
    ips = []
    try:
        # 获取所有网络接口
        for iface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                # 过滤出IPv4地址，用socket.AF_INET来过滤是因为psutil没有提供AF_INET常量
                if addr.family == socket.AF_INET:
                    ips.append(addr.address)
    except Exception as e:
        logger.error(f"获取本机所有IP地址失败: {e}")
    return ips


def create_app():
    app = Flask(__name__)

    # 注册Flask蓝图
    app.register_blueprint(channel_camera_bp, url_prefix="/api/channel_camera")
    app.register_blueprint(network_led_bp, url_prefix="/api/network_led")
    app.register_blueprint(parking_camera_bp, url_prefix="/api/parking_camera")
    app.register_blueprint(lora_node_bp, url_prefix="/api/lora_node")
    app.register_blueprint(four_bytes_node_bp, url_prefix="/api/four_bytes_node")

    logger.info("开始检查当前环境是否满足配置文件中设备所需全部IP")
    # 获取当前环境中的所有IP地址
    local_ips = get_all_local_ips()
    logger.debug(f"当前环境的所有IP地址: {local_ips}")

    # 加载配置中的设备IP
    try:
        required_ips = [addr for device, addr in config['devices_addr'].items()]
        logger.debug(f"配置文件中所需的所有设备IP地址: {required_ips}")
    except Exception as e:
        raise Exception(f"获取配置文件所需的IP失败: {e}")

    # 检查配置的IP是否存在当前环境中
    missing_ips = [ip for ip in required_ips if ip not in local_ips]
    if missing_ips:
        logger.error(f"环境缺少设备所需IP地址: {missing_ips}")
        raise Exception(f"环境缺少设备所需IP地址：{missing_ips}")

    # 如果检测通过，初始化所有设备
    logger.info("环境满足，开始初始化设备")
    try:
        DeviceManager.initialize_all_devices()
        logger.info("所有设备初始化成功")
    except Exception as e:
        raise Exception(f"设备初始化失败: {e}")

    return app
