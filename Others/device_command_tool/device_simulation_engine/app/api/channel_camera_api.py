#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/9 下午7:28
# @Author  : Heshouyi
# @File    : channel_camera_api.py
# @Software: PyCharm
# @description:

from typing import Optional
from flask import Blueprint, request, jsonify
from ..services.channel_camera_service import ChannelCameraService
from ..utils.logger import logger

channel_camera_bp = Blueprint("channel_camera", __name__)
camera_service: Optional[ChannelCameraService] = None


@channel_camera_bp.route('/connect', methods=['POST'])
def connect():
    """
    连接设备到服务器

    必填参数:
    - server_ip (str): 服务器 IP 地址
    - server_port (int): 服务器端口

    选填参数:
    - device_id (str): 设备 ID，默认为 "SY17711123"
    - device_version (str): 设备版本，默认为 "RDD.CSA.S1A.1.0"
    """
    global camera_service
    data = request.json

    # 参数校验
    server_ip = data.get("server_ip")
    server_port = data.get("server_port")
    if not server_ip or not server_port:
        return jsonify({"error": "缺少必填参数: server_ip, server_port"}), 400

    # 选填参数
    device_id = data.get("device_id", "SY17711123")
    device_version = data.get("device_version", "RDD.CSA.S1A.1.0")

    # 如果已有实例存在，先断开连接
    if camera_service is not None:
        camera_service.disconnect()
        logger.info("上一个连接已经被重置")

    # 实例化服务并连接
    camera_service = ChannelCameraService(server_ip, server_port, device_id, device_version)
    if camera_service.connect():
        camera_service.send_register_packet()
        return jsonify({"status": "连接成功"}), 200
    return jsonify({"status": "连接失败"}), 500


@channel_camera_bp.route('/start_heartbeat', methods=['GET'])
def start_heartbeat():
    if camera_service:
        camera_service.start_heartbeat()
        return jsonify({"status": "心跳开始"}), 200
    return jsonify({"status": "设备还未被初始化"}), 500


@channel_camera_bp.route('/stop_heartbeat', methods=['GET'])
def stop_heartbeat():
    if camera_service:
        camera_service.stop_heartbeat()
        return jsonify({"status": "心跳停止"}), 200
    return jsonify({"status": "设备还未被初始化"}), 500


@channel_camera_bp.route('/send_command', methods=['POST'])
def send_command():
    """
    向设备发送指令

    必填参数:
    - command_data (dict): 指令数据，包含设备上报或控制指令的相关信息

    选填参数:
    - command_code (str): 命令码，默认为 "T"
    """
    if camera_service is None:
        return jsonify({"error": "设备还未被初始化"}), 500

    # 获取并校验必填参数
    command_data = request.json.get("command_data")
    if not command_data:
        return jsonify({"error": "缺少必填参数: command_data"}), 400

    # 选填参数
    command_code = request.json.get("command_code", "T")

    # 发送指令
    camera_service.send_command(command_data, command_code)
    return jsonify({"status": f"指令发送成功{command_data}"}), 200


@channel_camera_bp.route('/disconnect', methods=['GET'])
def disconnect():
    if camera_service:
        camera_service.disconnect()
        return jsonify({"status": "设备已断开连接"}), 200
    return jsonify({"status": "设备还未被初始化"}), 500
