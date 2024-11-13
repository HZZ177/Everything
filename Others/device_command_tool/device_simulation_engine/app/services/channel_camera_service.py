#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/9 下午7:34
# @Author  : Heshouyi
# @File    : channel_camera_service.py
# @Software: PyCharm
# @description:

from ..connection.tcp_connection import TCPClient
from ..models.channel_camera_model import ChannelCameraModel
from ..utils.logger import logger
import threading


class ChannelCameraService:
    def __init__(self, server_ip, server_port, local_ip, device_id="SY17711123", device_version="RDD.CSA.S1A.1.0"):
        self.device_id = device_id              # 设备ID，默认为SY17711123
        self.device_version = device_version    # 设备版本号，默认为RDD.CSA.S1A.1.0
        self.client = TCPClient()       # TCP客户端连接
        self.server_ip = server_ip      # 服务器IP
        self.server_port = server_port  # 服务器端口
        self.local_ip = local_ip        # 用语连接服务器的设备IP
        self.is_reporting = False       # 是否正在上报数据
        self.heartbeat_interval = 10    # 心跳间隔时间，单位为秒
        self.timer = None               # 用于定时发送心跳包的定时器

    def connect(self):
        try:
            self.client.connect(self.server_ip, self.server_port, self.local_ip)
            # 设置接收数据和断开连接的回调函数
            self.client.set_receive_callback(self.handle_received_data)
            self.client.set_disconnect_callback(self.disconnect)
            return True  # 连接成功返回 True
        except Exception as e:
            logger.error(f"连接服务器失败: {e}")
            raise e

    def send_register_packet(self):
        packet = ChannelCameraModel.create_register_packet(self.device_id, self.device_version)
        self.client.send_data(packet)

    def start_heartbeat(self):
        self.is_reporting = True
        self.schedule_next_heartbeat()

    def stop_heartbeat(self):
        self.is_reporting = False
        if self.timer:
            self.timer.cancel()
            self.timer = None

    def schedule_next_heartbeat(self):
        if self.is_reporting:
            heartbeat_packet = ChannelCameraModel.create_heartbeat_packet(self.device_id)
            self.client.send_data(heartbeat_packet)
            self.timer = threading.Timer(self.heartbeat_interval, self.schedule_next_heartbeat)
            self.timer.start()

    def send_command(self, command_data, command_code='T'):
        packet = ChannelCameraModel.construct_packet(command_data, command_code)
        self.client.send_data(packet)

    @staticmethod
    def handle_received_data(data):
        """接收到服务器数据时的处理函数"""
        logger.info(f"收到来自服务器的数据，开始解包")
        # 根据数据内容进行处理
        parsed_data = ChannelCameraModel.deconstruct_packet(data)
        logger.info(f"收到服务器下发数据: {parsed_data}")

    def disconnect(self):
        self.stop_heartbeat()
        self.client.disconnect()
