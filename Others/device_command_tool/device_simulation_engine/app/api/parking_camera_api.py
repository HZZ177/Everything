#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/9 下午7:28
# @Author  : Heshouyi
# @File    : parking_camera_api.py
# @Software: PyCharm
# @description:

from flask import Blueprint, request, jsonify
from ..services.device_manager import DeviceManager
from ..utils.logger import logger
from ..utils.util import get_inner_picture

# 创建蓝图对象
parking_camera_bp = Blueprint("parking_camera", __name__)


@parking_camera_bp.route('/connect', methods=['GET'])
def connect():
    """尝试连接设备到服务器，连接后发送注册包，开启心跳"""
    logger.info("车位相机connect接口被调用")
    parking_camera = DeviceManager.get_parking_camera_service()
    try:
        # 连接服务器
        parking_camera.connect()
        # 连接后发送注册包
        parking_camera.send_register_packet()
        # 注册后开始持续心跳
        parking_camera.start_heartbeat()
        logger.info("车位相机成功连接服务器")
        return jsonify({"message": "成功"}), 200
    except Exception as e:
        logger.exception(f"车位相机连接服务器失败: {e}")
        return jsonify({"message": "系统异常"}), 500


@parking_camera_bp.route('/disconnect', methods=['GET'])
def disconnect():
    """断开连接"""
    logger.info("车位相机disconnect接口被调用")
    parking_camera = DeviceManager.get_parking_camera_service()
    try:
        parking_camera.disconnect()
        logger.info("车位相机成功断开连接")
        return jsonify({"message": "成功"}), 200
    except Exception as e:
        logger.exception(f"车位相机断开连接失败: {e}")
        return jsonify({"message": "系统异常"}), 500


@parking_camera_bp.route('/startHeartbeat', methods=['GET'])
def start_heartbeat():
    """开启持续心跳"""
    logger.info("车位相机startHeartbeat接口被调用")
    parking_camera = DeviceManager.get_parking_camera_service()
    try:
        parking_camera.start_heartbeat()
        logger.info("车位相机成功开启心跳")
        return jsonify({"message": "成功"}), 200
    except Exception as e:
        logger.exception(f"车位相机开启心跳失败: {e}")
        return jsonify({"message": "系统异常"}), 500


@parking_camera_bp.route('/stopHeartbeat', methods=['GET'])
def stop_heartbeat():
    """停止心跳"""
    logger.info("车位相机stopHeartbeat接口被调用")
    parking_camera = DeviceManager.get_parking_camera_service()
    try:
        parking_camera.stop_heartbeat()
        logger.info("车位相机成功停止心跳")
        return jsonify({"message": "成功"}), 200
    except Exception as e:
        logger.exception(f"车位相机停止心跳失败: {e}")
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
    logger.info("车位相机parkingStatusReport接口被调用")
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
        logger.info(f"车位相机上报车位状态成功，车位号: {park_num}, 车位状态: {park_event}")
        return jsonify({"message": "成功"}), 200
    except Exception as e:
        logger.exception(f"车位相机上报车位状态失败: {e}")
        return jsonify({"message": "系统异常"}), 500


@parking_camera_bp.route('/uploadParkingPicture', methods=['POST'])
def upload_parking_picture():
    """
    上报车位图片，目前只支持软识别模式

    必填参数：
        parkNum (int): 车位号
    以下两个必填其一：
        image (file): 车牌图片，base64编码
        innerPic (str): 内置图片名称

    :return:
    """
    logger.info("车位相机uploadParkingPicture接口被调用")
    parking_camera = DeviceManager.get_parking_camera_service()

    # 获取参数
    park_num = request.form.get('parkNum')
    image = request.files.get('image')  # 获取上传的图片文件（FileStorage对象）
    inner_pic = request.form.get('innerPic')    # 内置图片

    # 校验parkNum
    try:
        park_num = int(park_num)    # flask中从表获取的参数都是字符串，需要手动转换为整数
    except (TypeError, ValueError):
        return jsonify({"error": "缺少必填参数parkNum或parkNum不是有效的整数"}), 400
    # 校验车位号是否合法
    if park_num not in [1, 2, 3, 4, 5, 6]:
        return jsonify({"error": f"错误的车位号{park_num}"}), 400

    # 校验图片参数：image和innerPic必填其一
    if not inner_pic and not image:
        return jsonify({"error": "image或innerPic至少需要有其中一个"}), 400

    # 判断图片来源并获取二进制数据
    if inner_pic:
        image_bytes = get_inner_picture(inner_pic)
        if image_bytes is None:
            return jsonify({"error": f"无法找到内置图片: {inner_pic}"}), 400
    else:
        # 将上传的图片文件转换为二进制数据
        image_bytes = image.read()

    # 校验通过，组装数据，图片上报
    try:
        parking_camera.upload_picture(park_num, image_bytes)
        logger.info(f"车位相机 {park_num} 号车位成功上报车位图片")
        return jsonify({"message": "成功"}), 200
    except Exception as e:
        logger.exception(f"车位相机上传图片失败: {e}")
        return jsonify({"message": "系统异常"}), 500
