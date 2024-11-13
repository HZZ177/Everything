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
import time


class ChannelCameraService:
    def __init__(self, server_ip, server_port, device_id, device_version):
        self.device_id = device_id
        self.device_version = device_version
        self.client = TCPClient()
        self.server_ip = server_ip
        self.server_port = server_port
        self.is_reporting = False
        self.heartbeat_interval = 10
        self.timer = None

    def connect(self):
        try:
            self.client.connect(self.server_ip, self.server_port)
            # 设置接收数据的回调函数
            self.client.set_receive_callback(self.handle_received_data)
            self.client.set_disconnect_callback(self.disconnect)
            return True  # 连接成功返回 True
        except Exception as e:
            logger.error(f"连接服务器失败: {e}")
            return False

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
