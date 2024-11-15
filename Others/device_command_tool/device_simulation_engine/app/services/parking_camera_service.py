#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/9 下午7:34
# @Author  : Heshouyi
# @File    : parking_camera_service.py
# @Software: PyCharm
# @description:

import threading
from ..connection.tcp_connection import TCPClient
from ..models.parking_camera_model import ParkingCameraModel
from ..utils.logger import logger
from werkzeug.datastructures import FileStorage


class ParkingCameraService:
    def __init__(self, server_ip, server_port, local_ip, device_type, device_version):
        self.device_type = device_type          # 设备类型，默认为0x00
        self.device_version = device_version    # 设备版本号，默认为0x0400
        self.client = TCPClient()           # TCP客户端连接
        self.server_ip = server_ip          # 服务器IP
        self.server_port = server_port      # 服务器端口
        self.local_ip = local_ip            # 用于连接服务器的设备IP
        self.is_reporting = False           # 是否正在上报数据
        self.heartbeat_interval = 10        # 心跳间隔时间，单位为秒
        self.timer = None                   # 用于定时发送心跳包的定时器
        self.confirmation_event = threading.Event()  # 线程事件对象，用于发送图片时阻塞发送进程，等待服务器返回确认信息
        self.parking_camera_model = ParkingCameraModel()    # 车位相机的数据模型实例

    def connect(self):
        """连接服务器"""
        status = self.client.is_connected()
        try:
            if status:
                logger.warning(f"车位相机尝试连接服务器时，已有连接，断开后重连")
                self.client.disconnect()
            self.client.connect(self.server_ip, self.server_port, self.local_ip)
            # 设置接收数据和断开连接的回调函数
            self.client.set_receive_callback(self.handle_received_data)
            self.client.set_disconnect_callback(self.disconnect)
        except Exception as e:
            raise e

    def send_register_packet(self):
        """发送注册包"""
        try:
            packet = self.parking_camera_model.create_register_packet(self.device_type, self.device_version)
            self.client.send_data(packet)
        except Exception as e:
            raise e

    def start_heartbeat(self):
        """开启持续心跳"""
        try:
            self.is_reporting = True
            self.schedule_next_heartbeat()
            logger.info("车位相机定时心跳开始")
        except Exception as e:
            raise e

    def stop_heartbeat(self):
        """停止心跳"""
        try:
            self.is_reporting = False
            if self.timer:
                self.timer.cancel()
                self.timer = None
                logger.info("车位相机定时心跳停止")
        except Exception as e:
            raise e

    def schedule_next_heartbeat(self):
        if self.is_reporting:
            heartbeat_packet = self.parking_camera_model.create_heartbeat_packet()
            self.client.send_data(heartbeat_packet, need_log=False)
            self.timer = threading.Timer(self.heartbeat_interval, self.schedule_next_heartbeat)
            self.timer.start()

    def send_command(self, command_data: bytes, command_code: str):
        """
        发送指令工具方法，向上供不同指令的发送接口使用
        :param command_data: 需要发送的数据体
        :param command_code: 命令码
        :return:
        """
        try:
            # 根据协议和数据体构造包
            packet = self.parking_camera_model.construct_packet(command_data, command_code)
            self.client.send_data(packet)
        except Exception as e:
            raise e

    def send_parking_status(self, selected_port, status_values):
        """
        上报车位状态(事件)
        :param selected_port: 要上报的车位号
        :param status_values: 车位状态
        :return:
        """
        try:
            packet = self.parking_camera_model.create_parking_status_packet(selected_port, status_values)
            self.client.send_data(packet)
        except Exception as e:
            raise e

    def upload_picture(self, park_num, image: FileStorage):
        """
        给服务器上传图片数据包，包类型为J包
        首先发送一次头包，阻塞进程等待服务器的确认返回，接收到返回后分包发送图片的二进制内容
        :param park_num: 车位号
        :param image: 图片文件对象
        :return:
        """
        try:
            # 读取图片的二进制数据
            image_bytes = image.read()
            # 构造头包后发送
            head_packet = self.parking_camera_model.create_parking_picture_head_packet(park_num, image_bytes)
            self.client.send_data(head_packet)

            # 等待服务器返回确认
            logger.info("图片头包已发送，等待服务器返回确认...")
            self.confirmation_event.clear()  # 设置事件为未触发状态
            if not self.confirmation_event.wait(timeout=5):  # 等待事件被触发，超时时间为5秒
                logger.error("5秒内没有接收到服务器确认信息，停止上传图片")
                raise Exception("5秒内没有接收到服务器确认信息，停止上传图片")
            logger.info("收到服务器的头包确认返回，开始发送图片数据")

            # 计算图片分割总包数
            total_packets = len(image_bytes) // 1024 + (1 if len(image_bytes) % 1024 != 0 else 0)
            # 分包发送图片数据
            for i in range(total_packets):
                chunk = image_bytes[i * 1024:(i + 1) * 1024]    # 每1024字节为一包
                packet = self.parking_camera_model.construct_packet(
                    command_data=chunk,
                    command_code="J",
                    total_packets=total_packets,
                    packet_number=i + 1  # 图片数据包的序号从1开始
                )
                self.client.send_data(packet)
        except Exception as e:
            raise e

    def handle_received_data(self, data):
        """接收到服务器数据时的处理函数"""
        logger.debug(f"车位相机收到来自服务器的数据，开始解包")
        # 根据数据内容进行处理
        try:
            parsed_data = self.parking_camera_model.deconstruct_packet(data)
            if "F" in str(parsed_data):    # 处理车位相机的F心跳包，打成debug
                logger.debug(f"车位相机收到服务器的心跳返回：{parsed_data}")
            elif "J" in str(parsed_data):  # 处理服务器返回的图片头包ACK返回包，返回J包视为确认通过
                logger.info("收到服务器对上传头包的确认信息，解除阻塞状态")
                self.confirmation_event.set()  # 触发事件，解除等待状态
            else:
                logger.info(f"车位相机收到服务器下发数据，解包结果: {parsed_data}")
        except Exception as e:
            logger.error(f"车位相机解析服务器下发数据失败: {e}")

    def disconnect(self):
        try:
            self.stop_heartbeat()
            self.client.disconnect()
        except Exception as e:
            raise e
