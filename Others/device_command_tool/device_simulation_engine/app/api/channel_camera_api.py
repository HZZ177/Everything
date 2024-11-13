#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/9 下午7:28
# @Author  : Heshouyi
# @File    : channel_camera_api.py
# @Software: PyCharm
# @description:

from flask import Blueprint, request, jsonify
from ..utils.logger import logger
from ..services.device_manager import DeviceManager

channel_camera_bp = Blueprint("channel_camera", __name__)


# @channel_camera_bp.route('/init', methods=['POST'])
# def init():
#     """
#     初始化设备
#     必填参数:
#     - server_ip (str): 服务器 IP 地址
#     - server_port (int): 服务器端口
#
#     选填参数:
#     - device_id (str): 设备 ID，默认为 "SY17711123"
#     - device_version (str): 设备版本，默认为 "RDD.CSA.S1A.1.0"
#
#     """
#     global channel_camera
#     data = request.json
#
#     # 必填参数校验
#     server_ip = data.get("server_ip")
#     server_port = data.get("server_port")
#     if not server_ip:
#         return jsonify({"error": "缺少必填参数: server_ip"}), 400
#     elif not server_port:
#         return jsonify({"error": "缺少必填参数: server_port"}), 400
#
#     # 选填参数
#     device_id = data.get("device_id", "SY17711123")
#     device_version = data.get("device_version", "RDD.CSA.S1A.1.0")
#
#     # 如果已有初始化的设备存在，先断开连接
#     if channel_camera is not None:
#         channel_camera.disconnect()
#         logger.warning("存在一个设备实例，上一个设备已经被重置")
#
#     # 初始化设备
#     channel_camera = ChannelCameraService(server_ip, server_port, device_id, device_version)
#     logger.info("设备初始化成功")
#     return jsonify({"message": "设备初始化成功"}), 200


@channel_camera_bp.route('/connect', methods=['GET'])
def connect():
    """尝试连接设备到服务器，连接后发送注册包，开启心跳"""
    channel_camera = DeviceManager.get_channel_camera_service()
    if channel_camera:
        success = channel_camera.connect()
        if success:
            # 连接后发送注册包
            channel_camera.send_register_packet()
            # 注册后开始持续心跳
            channel_camera.start_heartbeat()
            return jsonify({"message": "连接成功"}), 200
        else:
            return jsonify({"message": "连接失败"}), 500
    else:
        return jsonify({"message": "设备还未被初始化"}), 500


@channel_camera_bp.route('/start_heartbeat', methods=['GET'])
def start_heartbeat():
    channel_camera = DeviceManager.get_channel_camera_service()
    if channel_camera:
        channel_camera.start_heartbeat()
        return jsonify({"message": "心跳开始"}), 200
    return jsonify({"message": "设备还未被初始化"}), 500


@channel_camera_bp.route('/stop_heartbeat', methods=['GET'])
def stop_heartbeat():
    channel_camera = DeviceManager.get_channel_camera_service()
    if channel_camera:
        channel_camera.stop_heartbeat()
        return jsonify({"message": "心跳停止"}), 200
    return jsonify({"message": "设备还未被初始化"}), 500


@channel_camera_bp.route('/send_command', methods=['POST'])
def send_command():
    """
    向设备发送指令

    必填参数:
    - command_data (dict): 指令数据，包含设备上报或控制指令的相关信息

    选填参数:
    - command_code (str): 命令码，默认为 "T"
    """
    channel_camera = DeviceManager.get_channel_camera_service()
    if channel_camera is None:
        return jsonify({"error": "设备还未被初始化"}), 500

    # 获取并校验必填参数
    command_data = request.json.get("command_data")
    if not command_data:
        return jsonify({"error": "缺少必填参数: command_data"}), 400

    # 选填参数
    command_code = request.json.get("command_code", "T")

    # 发送指令
    channel_camera.send_command(command_data, command_code)
    return jsonify({"message": f"指令发送成功{command_data}"}), 200


@channel_camera_bp.route('/disconnect', methods=['GET'])
def disconnect():
    channel_camera = DeviceManager.get_channel_camera_service()
    if channel_camera:
        channel_camera.disconnect()
        return jsonify({"message": "设备已断开连接"}), 200
    return jsonify({"message": "设备还未被初始化"}), 500
