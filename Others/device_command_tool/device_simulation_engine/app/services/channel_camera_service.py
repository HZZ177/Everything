#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/9 下午7:34
# @Author  : Heshouyi
# @File    : channel_camera_service.py
# @Software: PyCharm
# @description:

import threading
from ..connection.tcp_connection import TCPClient
from ..models.channel_camera_model import ChannelCameraModel
from ..utils.logger import logger


class ChannelCameraService:
    def __init__(self, server_ip, server_port, local_ip, device_id, device_version):
        self.device_id = device_id              # 设备ID，默认为SY17711123
        self.device_version = device_version    # 设备版本号，默认为RDD.CSA.S1A.1.0
        self.client = TCPClient()       # TCP客户端连接
        self.server_ip = server_ip      # 服务器IP
        self.server_port = server_port  # 服务器端口
        self.local_ip = local_ip        # 用于连接服务器的设备IP
        self.is_reporting = False       # 是否正在上报数据
        self.heartbeat_interval = 10    # 心跳间隔时间，单位为秒
        self.timer = None               # 用于定时发送心跳包的定时器
        self.channel_camera_model = ChannelCameraModel()    # 通道相机数据模型实例

    def connect(self):
        status = self.client.is_connected()
        try:
            if status:
                logger.debug(f"通道相机尝试连接服务器时，已有连接，断开后重连")
                self.client.disconnect()
            self.client.connect(self.server_ip, self.server_port, self.local_ip)
            # 设置接收数据和断开连接的回调函数
            self.client.set_receive_callback(self.handle_received_data)
            self.client.set_disconnect_callback(self.disconnect)
        except Exception as e:
            raise e

    def send_register_packet(self):
        """
        发送注册包
        :return:
        """
        # 构造注册包
        try:
            packet = self.channel_camera_model.create_register_packet(self.device_id, self.device_version)
            self.client.send_data(packet)
        except Exception as e:
            raise e

    def start_heartbeat(self):
        try:
            self.is_reporting = True
            self.schedule_next_heartbeat()
            logger.debug("通道相机定时心跳开始")
        except Exception as e:
            raise e

    def stop_heartbeat(self):
        try:
            self.is_reporting = False
            if self.timer:
                self.timer.cancel()
                self.timer = None
                logger.debug("通道相机定时心跳停止")
        except Exception as e:
            raise e

    def schedule_next_heartbeat(self):
        if self.is_reporting:
            heartbeat_packet = self.channel_camera_model.create_heartbeat_packet(self.device_id)
            self.client.send_data(heartbeat_packet, need_log=False)
            self.timer = threading.Timer(self.heartbeat_interval, self.schedule_next_heartbeat)
            self.timer.start()

    def send_command(self, command_data, command_code='T'):
        """
        发送指令工具方法，向上供不同指令的发送接口使用，默认T包
        :param command_data: 需要发送的数据体
        :param command_code: 命令码，默认T包
        :return:
        """
        try:
            # 根据协议和数据体构造包
            packet = self.channel_camera_model.construct_packet(command_data, command_code)
            self.client.send_data(packet)
        except Exception as e:
            raise e

    def handle_received_data(self, data):
        """接收到服务器数据时的处理函数"""
        logger.debug(f"通道相机收到来自服务器的数据，开始解包")
        # 根据数据内容进行处理
        try:
            parsed_data = self.channel_camera_model.deconstruct_packet(data)
            if "heartbeatResult" in str(parsed_data):
                logger.debug(f"通道相机收到服务器的心跳返回：{parsed_data}")
            else:
                logger.info(f"通道相机收到服务器下发数据，解包结果: {parsed_data}")
        except Exception as e:
            logger.exception(f"通道相机解析服务器下发数据失败: {e}")

    def disconnect(self):
        try:
            self.stop_heartbeat()
            self.client.disconnect()
        except Exception as e:
            raise e
