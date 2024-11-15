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

    def connect(self):
        status = self.client.is_connected()
        try:
            if status:
                logger.warning(f"通道相机尝试连接服务器时，已有连接，断开后重连")
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
            packet = ChannelCameraModel.create_register_packet(self.device_id, self.device_version)
            self.client.send_data(packet)
        except Exception as e:
            raise e

    def start_heartbeat(self):
        try:
            self.is_reporting = True
            self.schedule_next_heartbeat()
            logger.info("通道相机定时心跳开始")
        except Exception as e:
            raise e

    def stop_heartbeat(self):
        try:
            self.is_reporting = False
            if self.timer:
                self.timer.cancel()
                self.timer = None
                logger.info("通道相机定时心跳停止")
        except Exception as e:
            raise e

    def schedule_next_heartbeat(self):
        if self.is_reporting:
            heartbeat_packet = ChannelCameraModel.create_heartbeat_packet(self.device_id)
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
            packet = ChannelCameraModel.construct_packet(command_data, command_code)
            self.client.send_data(packet)
        except Exception as e:
            raise e

    def upload_picture(self, park_num, image):
        """
        给服务器上传图片数据包

        :return:
        """
        # TODO

        command_code = ord('J')

        # 默认所有不用的字符9占位，并设置每个车位的状态和端口号
        data_content = b''
        selected_slot = park_num    # 选中的车位编号

        for slot_number in range(4):
            # 此部分不按照协议封装，服务器端根据实际收到3的数据长度取不同标志位的数据作为通道口数据
            # 65为长度数据时，取第16byte数据作为通道口
            # 因此直接把所有车位数据都设置为选中车位的车位端口号
            status_and_port = selected_slot

            # 默认车牌颜色、车牌号码和可信度
            plate_color = plate_color  # 3表示蓝色
            plate_number = plate_number.encode('gbk')
            confidence = confidence

            # 按协议格式打包每个车位信息
            data_content += struct.pack(">B B 11s H", status_and_port, plate_color, plate_number, confidence)
        logger.info(f"车位相机上传图片头包content部分：{data_content}")

        # 有卡/无卡标志位
        #   低4位为6：找车系统主动上传
        #   高4位为0：旧模式(单车牌+车型信息等)
        has_card_flag = struct.pack(">B", 0x06)  # 高4位为0，低4位为6

        # 获取当前路径
        current_path = os.path.dirname(os.path.abspath(__file__))

        if mode == 1:
            # 读取自选图片文件数据
            with open(self.file_path.get(), "rb") as img_file:
                image_data = img_file.read()
        elif mode == 2:
            # 读取内置整图数据
            with open(f'{current_path}/resource/full_photo.jpg', "rb") as img_file:
                image_data = img_file.read()
        elif mode == 3:
            # 读取内置车位图数据
            with open(f'{current_path}/resource/single_park_photo.jpg', "rb") as img_file:
                image_data = img_file.read()
            # return
        # 计算总包数
        total_packets = len(image_data) // 1024 + (1 if len(image_data) % 1024 != 0 else 0)

        # 总图像数据长度
        total_image_length = struct.pack(">I", len(image_data))
        print(f"头包—总图像数据长度_bytes：{total_image_length}")
        print(f"头包—总图像数据长度_size：{len(image_data)}")

        # 组装包头包（包含有卡/无卡标志位、车位信息和图像数据总长度）
        packet_header = self.create_packet(
            data_content=has_card_flag + data_content + total_image_length,
            command_code=command_code,
            timestamp=timestamp,
            total_packets=total_packets + 1,
            packet_number=0
        )
        self.tcp_client.send_command(packet_header)
        print(f"头包full_content_hex：{(has_card_flag + data_content + total_image_length).hex()}")
        print(f"头包封装数据：{packet_header}")

        # # 等待服务器返回确认
        # with self.upload_condition:
        #     self.upload_condition.wait_for(lambda: self.upload_response_received)
        #     self.upload_response_received = False  # 重置状态

        # 分批次发送图片数据，仅包含图片数据
        for i in range(total_packets):
            chunk = image_data[i * 1024:(i + 1) * 1024]
            packet = self.create_packet(
                data_content=chunk,
                command_code=command_code,
                timestamp=timestamp,
                total_packets=total_packets,
                packet_number=i + 1  # 图片数据包的序号从1开始
            )
            print(f"发送图片数据包，第{i + 1}包")
            self.tcp_client.send_command(packet)

    @staticmethod
    def handle_received_data(data):
        """接收到服务器数据时的处理函数"""
        logger.debug(f"通道相机收到来自服务器的数据，开始解包")
        # 根据数据内容进行处理
        try:
            parsed_data = ChannelCameraModel.deconstruct_packet(data)
            if "heartbeatResult" in str(parsed_data):    # 心跳包的日志打成debug，太多了
                logger.debug(f"通道相机收到服务器的心跳返回：{parsed_data}")
            else:
                logger.info(f"通道相机收到服务器下发数据，解包结果: {parsed_data}")
        except Exception as e:
            logger.error(f"通道相机解析服务器下发数据失败: {e}")

    def disconnect(self):
        try:
            self.stop_heartbeat()
            self.client.disconnect()
        except Exception as e:
            raise e
