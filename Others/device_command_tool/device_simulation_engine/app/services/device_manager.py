#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/13 下午22:01
# @Author  : Heshouyi
# @File    : device_manager.py
# @Software: PyCharm
# @description:

from .channel_camera_service import ChannelCameraService
from .parking_camera_service import ParkingCameraService
from .lora_node_service import LoraNodeService
from .four_bytes_node_service import FourBytesNodeService
from ..utils.configer import config
from ..utils.logger import logger


class DeviceManager:
    channel_camera_service = None   # 通道相机服务实例
    lora_node_service = None        # Lora节点设备服务实例
    four_bytes_node_service = None   # 四字节网络节点服务实例
    network_led_service = None      # 网络led屏服务实例
    parking_camera_service = None   # 车位相机服务实例

    @classmethod
    def initialize_all_devices(cls):
        """初始化所有设备实例"""

        # 读取配置文件
        try:
            # 服务器配置参数
            server_ip = config['server']['host']
            server_port_7799 = config['server']['port_7799']
            server_port_7777 = config['server']['port_7777']
            # 通道相机配置参数
            channel_camera_ip = config['devices_addr']['channel_camera_ip']
            channel_camera_device_id = config["devices_info"]["channel_camera"]["device_id"]
            channel_camera_device_version = config["devices_info"]["channel_camera"]["device_version"]
            # 车位相机配置参数
            parking_camera_ip = config['devices_addr']['parking_camera_ip']
            parking_camera_device_type = config["devices_info"]["parking_camera"]["device_type"]
            parking_camera_device_version = config["devices_info"]["parking_camera"]["device_version"]
            # lora节点配置参数
            lora_node_ip = config['devices_addr']['lora_node_ip']
            # 四字节网络节点配置参数
            four_bytes_node_ip = config['devices_addr']['four_bytes_node_ip']
        except Exception as e:
            raise Exception(f"初始化时配置读取失败：{e}")

        # 初始化通道相机设备
        try:
            # 初始化设备实例
            cls.channel_camera_service = ChannelCameraService(server_ip, server_port_7799, channel_camera_ip,
                                                              channel_camera_device_id, channel_camera_device_version)
            # 连接服务器
            cls.channel_camera_service.connect()
            # 连接后发送注册包
            cls.channel_camera_service.send_register_packet()
            # 注册后开始持续心跳
            cls.channel_camera_service.start_heartbeat()
            logger.info("通道相机设备初始化成功")
        except Exception as e:
            raise Exception(f"通道相机设备初始化失败: {e}")

        # 初始化车位相机设备
        try:
            # 初始化设备实例
            cls.parking_camera_service = ParkingCameraService(server_ip, server_port_7799, parking_camera_ip,
                                                              parking_camera_device_type, parking_camera_device_version)
            # 连接服务器
            cls.parking_camera_service.connect()
            # 连接后发送注册包
            cls.parking_camera_service.send_register_packet()
            # 特殊步骤，注册后立即发一个无实际业务数据的车位状态上报，全部用9占位，用于服务器识别设备类型
            cls.parking_camera_service.send_all9_packet_for_recognition()
            # 注册后开始持续心跳
            cls.parking_camera_service.start_heartbeat()
            logger.info("车位相机设备初始化成功")
        except Exception as e:
            raise Exception(f"车位相机设备初始化失败: {e}")

        # 初始化lora节点设备
        try:
            # 初始化设备实例
            cls.lora_node_service = LoraNodeService(server_ip, server_port_7777, lora_node_ip)
            # 连接服务器
            cls.lora_node_service.connect()
            logger.info("Lora节点初始化成功")
        except Exception as e:
            raise Exception(f"Lora节点初始化失败: {e}")

        # 初始化四字节节点设备
        try:
            # 初始化设备实例
            cls.four_bytes_node_service = FourBytesNodeService(server_ip, server_port_7777, four_bytes_node_ip)
            # 连接服务器
            cls.four_bytes_node_service.connect()
            logger.info("四字节网络节点初始化成功")
        except Exception as e:
            raise Exception(f"四字节网络节点初始化失败: {e}")

    @classmethod
    def get_channel_camera_service(cls):
        """获取通道相机服务实例"""
        return cls.channel_camera_service

    @classmethod
    def get_lora_node_service(cls):
        """获取Lora节点设备服务实例"""
        return cls.lora_node_service

    @classmethod
    def get_four_bytes_node_service(cls):
        """获取Lora节点设备服务实例"""
        return cls.four_bytes_node_service

    @classmethod
    def get_network_led_service(cls):
        """获取网络led屏服务实例"""
        return cls.network_led_service

    @classmethod
    def get_parking_camera_service(cls):
        """获取车位相机服务实例"""
        return cls.parking_camera_service
