#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/9 下午7:35
# @Author  : Heshouyi
# @File    : parking_camera_model.py
# @Software: PyCharm
# @description:

import struct
import json
import time


class ParkingCameraModel:
    PROTOCOL_HEAD = 0xfb  # 协议头
    PROTOCOL_TAIL = 0xfe  # 协议尾

    @staticmethod
    def construct_packet(command_data: bytes, command_code: str, total_packets: int = 1, packet_number: int = 0) -> bytes:
        """
        构造事件数据包
        :param command_data: 要发送的数据字节码
        :param command_code: 命令码
        :param packet_number: 包序号，默认为0
        :param total_packets:  总包数，默认为1
        :return:
        """
        data_content = command_data
        timestamp = int(time.time())  # 时间戳
        command_code_ascii = ord(command_code)  # 命令码转换为ASCII码
        data_length = len(data_content)  # 数据长度
        checksum = ParkingCameraModel.calculate_checksum(timestamp, command_code_ascii, total_packets, packet_number,
                                                         data_length, data_content)  # 校验码

        packet = (
                struct.pack('>B', ParkingCameraModel.PROTOCOL_HEAD) +
                struct.pack('>I', timestamp) +
                struct.pack('>B', command_code_ascii) +
                struct.pack('>H', total_packets) +
                struct.pack('>H', packet_number) +
                struct.pack('>H', data_length) +
                data_content +
                struct.pack('>H', checksum) +
                struct.pack('>B', ParkingCameraModel.PROTOCOL_TAIL)
        )
        # 组装数据包，按协议要求处理转义
        processed_packet = ParkingCameraModel.escape_packet(packet)
        return processed_packet

    @staticmethod
    def deconstruct_packet(data):
        """
        根据协议解包服务器下发的数据
        :param data: 返回的原数据字节码
        :return: 根据协议解析后的json
        """
        # 根据协议解析：包含如下字段
        #   协议头 (1字节), 时间戳 (4字节), 命令码 (1字节), 数据长度 (2字节), 数据内容 (N字节), 校验码 (2字节), 协议尾 (1字节)
        protocol_head, timestamp, command_code, total_packets, packet_number, data_length = struct.unpack(
            '>BIBHHH', data[:12])

        # 根据data_length提取数据内容
        data_content = data[12:12 + data_length].decode()
        # 提取校验码和协议尾
        checksum, protocol_tail = struct.unpack('>HB', data[12 + data_length:12 + data_length + 3])

        # 组装解析后数据
        parsed_data = {
            "protocol_head": hex(protocol_head),
            "timestamp": timestamp,
            "command_code": chr(command_code),
            "total_packets": total_packets,
            "packet_number": packet_number,
            "data_length": data_length,
            "data_content": data_content,
            "checksum": checksum,
            "protocol_tail": hex(protocol_tail),
        }

        return parsed_data

    @staticmethod
    def calculate_checksum(timestamp, command_code_ascii, total_packets, packet_number, data_length, data_bytes):
        """按照协议要求，计算校验码"""
        checksum_data = (struct.pack('>I', timestamp) + struct.pack('>B', command_code_ascii) +
                         struct.pack('>H', total_packets) + struct.pack('>H', packet_number) +
                         struct.pack('>H', data_length) + data_bytes)
        checksum = sum(checksum_data) & 0xFFFF
        return checksum

    @staticmethod
    def escape_packet(packet):
        """
        按协议要求，将除了头尾的中间字节进行转义处理
        :param packet: 组装后的未处理字节数据
        :return:
        """
        protocol_head = packet[0:1]
        protocol_tail = packet[-1:]
        data_to_escape = packet[1:-1]
        escaped_data = (data_to_escape.replace(b'\xfb', b'\xff\xbb')
                        .replace(b'\xfe', b'\xff\xee').replace(b'\xff', b'\xff\xfc'))
        full_data = protocol_head + escaped_data + protocol_tail
        return full_data

    @staticmethod
    def create_register_packet(device_type, device_version):
        """根据参数封装注册包字节码"""
        registration_data = struct.pack(">BH", device_type, device_version)    # 协议要求的注册信息
        packet = ParkingCameraModel.construct_packet(registration_data, command_code='C')
        return packet

    @staticmethod
    def create_heartbeat_packet(device_id):
        """按参数封装心跳包"""
        packet = ParkingCameraModel.construct_packet(b"", command_code='F')     # 心跳包没有任何数据内容
        return packet

    @staticmethod
    def create_parking_status_packet(selected_port, status_values):
        """
        按参数封装车位状态包
        :param selected_port: 车位号
        :param status_values: 车位状态
        :return:
        """
        # 初始化要发送的数据体字节码
        parking_status_data = b''
        # 前6个字节用于填充车位状态
        for idx in range(6):
            if idx == selected_port - 1:
                # 传入的车位号，写入对应状态
                status = status_values
            else:
                # 不开启上报的车位状态默认用9填充，会被服务器过滤
                status = 9
            # 每个状态1字节
            parking_status_data += struct.pack(">B", status)
        # 后6个字节为预留位，填充为9
        parking_status_data += struct.pack(">BBBBBB", 9, 9, 9, 9, 9, 9)
        packet = ParkingCameraModel.construct_packet(parking_status_data, command_code='S')
        return packet
