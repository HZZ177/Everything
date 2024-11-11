#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/9 下午7:34
# @Author  : Heshouyi
# @File    : channel_camera_model.py
# @Software: PyCharm
# @description:

import struct
import json
import time


class ChannelCameraModel:
    PROTOCOL_HEAD = 0xfb    # 协议头
    PROTOCOL_TAIL = 0xfe    # 协议尾

    @staticmethod
    def construct_packet(command_data: dict, command_code: str) -> bytes:
        data_bytes = json.dumps(command_data, ensure_ascii=False).encode('gbk')
        timestamp = int(time.time())
        command_code_ascii = ord(command_code)
        total_packets = 1
        packet_number = 0
        data_length = len(data_bytes)
        checksum = ChannelCameraModel.calculate_checksum(timestamp, command_code_ascii, total_packets, packet_number, data_length, data_bytes)

        packet = (struct.pack('>B', ChannelCameraModel.PROTOCOL_HEAD) +
                  struct.pack('>I', timestamp) +
                  struct.pack('>B', command_code_ascii) +
                  struct.pack('>H', total_packets) +
                  struct.pack('>H', packet_number) +
                  struct.pack('>H', data_length) +
                  data_bytes +
                  struct.pack('>H', checksum) +
                  struct.pack('>B', ChannelCameraModel.PROTOCOL_TAIL))
        processed_packet = ChannelCameraModel.escape_packet(packet)
        return processed_packet

    @staticmethod
    def calculate_checksum(timestamp, command_code_ascii, total_packets, packet_number, data_length, data_bytes):
        checksum_data = (struct.pack('>I', timestamp) + struct.pack('>B', command_code_ascii) +
                         struct.pack('>H', total_packets) + struct.pack('>H', packet_number) +
                         struct.pack('>H', data_length) + data_bytes)
        checksum = sum(checksum_data) & 0xFFFF
        return checksum

    @staticmethod
    def escape_packet(packet):
        protocol_head = packet[0:1]
        protocol_tail = packet[-1:]
        data_to_escape = packet[1:-1]
        escaped_data = data_to_escape.replace(b'\xfb', b'\xff\xbb').replace(b'\xfe', b'\xff\xee').replace(b'\xff', b'\xff\xfc')
        full_data = protocol_head + escaped_data + protocol_tail
        return full_data

    @staticmethod
    def create_register_packet(device_id, device_version):
        packet = ChannelCameraModel.construct_packet({
            "cmd": "cameraLogin",
            "cmdTime": str(int(time.time())),
            "deviceType": "5",
            "deviceId": device_id,
            "deviceVersion": device_version
        }, command_code='T')
        return packet

    @staticmethod
    def create_heartbeat_packet(device_id):
        packet = ChannelCameraModel.construct_packet({
            "cmd": "heartbeat",
            "cmdTime": str(int(time.time())),
            "deviceType": "5",
            "deviceId": device_id,
            "areaState": "0"
        }, command_code='H')
        return packet
