#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/13 下午22:01
# @Author  : Heshouyi
# @File    : device_manager.py
# @Software: PyCharm
# @description:

from .channel_camera_service import ChannelCameraService
from ..utils.configer import config
from ..utils.logger import logger


class DeviceManager:
    channel_camera_service = None   # 通道相机服务实例
    lora_node_service = None        # Lora节点设备服务实例
    network_led_service = None      # 网络led屏服务实例
    parking_camera_service = None   # 车位相机服务实例

    @classmethod
    def initialize_all_devices(cls):
        """初始化所有设备实例"""

        # 初始化通道相机设备
        try:
            server_ip = config['server']['host']
            server_port = config['server']['port']
            channel_camera_ip = config['devices_addr']['channel_camera_ip']

            # 初始化设备
            cls.channel_camera_service = ChannelCameraService(server_ip, server_port, channel_camera_ip)
            # 连接设备
            cls.channel_camera_service.connect()
            logger.info("通道相机设备初始化成功并已连接")
        except Exception as e:
            logger.error(f"通道相机设备初始化失败: {e}")
            raise e

    @classmethod
    def get_channel_camera_service(cls):
        """获取通道相机服务实例"""
        return cls.channel_camera_service

    @classmethod
    def get_lora_node_service(cls):
        """获取Lora节点设备服务实例"""
        return cls.lora_node_service

    @classmethod
    def get_network_led_service(cls):
        """获取网络led屏服务实例"""
        return cls.network_led_service

    @classmethod
    def get_parking_camera_service(cls):
        """获取车位相机服务实例"""
        return cls.parking_camera_service
