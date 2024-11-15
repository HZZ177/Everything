#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/9 下午7:28
# @Author  : Heshouyi
# @File    : parking_camera_api.py
# @Software: PyCharm
# @description:

import time
import uuid
from flask import Blueprint, request, jsonify
from ..services.device_manager import DeviceManager
from ..utils.logger import logger
from ..utils.configer import config


# 创建蓝图对象
parking_camera_bp = Blueprint("parking_camera", __name__)


@parking_camera_bp.route('/connect', methods=['GET'])
def connect():
    """尝试连接设备到服务器，连接后发送注册包，开启心跳"""
    parking_camera = DeviceManager.get_parking_camera_service()
    try:
        # 连接服务器
        parking_camera.connect()
        # 连接后发送注册包
        parking_camera.send_register_packet()
        # 注册后开始持续心跳
        parking_camera.start_heartbeat()
        return jsonify({"message": "成功"}), 200
    except Exception as e:
        logger.error(f"车位相机连接服务器失败: {e}")
        return jsonify({"message": "系统异常"}), 500


@parking_camera_bp.route('/disconnect', methods=['GET'])
def disconnect():
    """断开连接"""
    parking_camera = DeviceManager.get_parking_camera_service()
    try:
        parking_camera.disconnect()
        return jsonify({"message": "成功"}), 200
    except Exception as e:
        logger.error(f"车位相机断开连接失败: {e}")
        return jsonify({"message": "系统异常"}), 500


@parking_camera_bp.route('/startHeartbeat', methods=['GET'])
def start_heartbeat():
    """开启持续心跳"""
    parking_camera = DeviceManager.get_parking_camera_service()
    try:
        parking_camera.start_heartbeat()
        return jsonify({"message": "成功"}), 200
    except Exception as e:
        logger.error(f"车位相机开启心跳失败: {e}")
        return jsonify({"message": "系统异常"}), 500


@parking_camera_bp.route('/stopHeartbeat', methods=['GET'])
def stop_heartbeat():
    """停止心跳"""
    parking_camera = DeviceManager.get_parking_camera_service()
    try:
        parking_camera.stop_heartbeat()
        return jsonify({"message": "成功"}), 200
    except Exception as e:
        logger.error(f"车位相机停止心跳失败: {e}")
        return jsonify({"message": "系统异常"}), 500


@parking_camera_bp.route('/parkingStatusReport', methods=['POST'])
def parking_status_report():
    """
    上报单个车位状态（事件）

    必填参数：
    port (int): 车位号——范围1-6
    parkEvent (int): 车位状态——0：无车；1：有车；2：出车；3：进车；4：设备故障

    :return:
    """
    parking_camera = DeviceManager.get_parking_camera_service()
    # 获取必填参数并校验
    try:
        data = request.get_json()
        park_num = data['port']
        park_event = data['parkEvent']
    except KeyError as e:
        return jsonify({"error": f"缺少必填参数: {str(e)}"}), 400
    if park_num not in [1, 2, 3, 4, 5, 6]:
        return jsonify({"error": f"错误的通道号{park_num}"}), 400
    if park_event not in [0, 1, 2, 3, 4]:
        return jsonify({"error": f"错误的事件类型{park_event}"}), 400

    # 校验通过，组装数据，状态上报
    try:
        parking_camera.send_parking_status(park_num, park_event)
        return jsonify({"message": "成功"}), 200
    except Exception as e:
        logger.error(f"车位相机上报车位状态失败: {e}")
        return jsonify({"message": "系统异常"}), 500


@parking_camera_bp.route('/reportParkingPicture', methods=['POST'])
def report_parking_picture():
    """
    上报车位图片，目前只支持软识别模式
    :return:
    """
    parking_camera = DeviceManager.get_parking_camera_service()
    try:
        data = request.get_json()
        park_num = data['parkNum']
        mode = data['mode']
        image = data['image']

    except KeyError as e:
        return jsonify({"error": f"缺少必填参数: {str(e)}"}), 400
    try:
        parking_camera.upload_picture(park_num, mode, image)
        return jsonify({"message": "成功"}), 200
    except Exception as e:
        logger.error(f"车位相机上传图片失败: {e}")
        return jsonify({"message": "系统异常"}), 500
