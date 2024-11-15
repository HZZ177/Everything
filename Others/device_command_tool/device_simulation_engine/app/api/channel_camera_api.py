#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/9 下午7:28
# @Author  : Heshouyi
# @File    : channel_camera_api.py
# @Software: PyCharm
# @description:

import time
import uuid
from flask import Blueprint, request, jsonify
from ..utils.logger import logger
from ..utils.configer import config
from ..services.device_manager import DeviceManager

# 创建蓝图
channel_camera_bp = Blueprint("channel_camera", __name__)
# 从配置文件获取通道相机设备信息
device_id = config["devices_info"]["channel_camera"]["device_id"]
device_version = config["devices_info"]["channel_camera"]["device_version"]


@channel_camera_bp.route('/connect', methods=['GET'])
def connect():
    """尝试连接设备到服务器，连接后发送注册包，开启心跳"""
    channel_camera = DeviceManager.get_channel_camera_service()
    try:
        # 连接服务器
        channel_camera.connect()
        # 连接后发送注册包
        channel_camera.send_register_packet()
        # 注册后开始持续心跳
        channel_camera.start_heartbeat()
        return jsonify({"message": "成功"}), 200
    except Exception as e:
        logger.exception(f"通道相机连接服务器失败: {e}")
        return jsonify({"message": "系统异常"}), 500


@channel_camera_bp.route('/disconnect', methods=['GET'])
def disconnect():
    """断开连接"""
    channel_camera = DeviceManager.get_channel_camera_service()

    try:
        channel_camera.disconnect()
        return jsonify({"message": "成功"}), 200
    except Exception as e:
        logger.exception(f"通道相机断开连接失败: {e}")
        return jsonify({"message": "系统异常"}), 500


@channel_camera_bp.route('/startHeartbeat', methods=['GET'])
def start_heartbeat():
    """开启持续心跳"""
    channel_camera = DeviceManager.get_channel_camera_service()
    try:
        channel_camera.start_heartbeat()
        return jsonify({"message": "成功"}), 200
    except Exception as e:
        logger.exception(f"通道相机开启心跳失败: {e}")
        return jsonify({"message": "系统异常"}), 500


@channel_camera_bp.route('/stopHeartbeat', methods=['GET'])
def stop_heartbeat():
    """停止心跳"""
    channel_camera = DeviceManager.get_channel_camera_service()
    try:
        channel_camera.stop_heartbeat()
        return jsonify({"message": "成功"}), 200
    except Exception as e:
        logger.exception(f"通道相机停止心跳失败: {e}")
        return jsonify({"message": "系统异常"}), 500


@channel_camera_bp.route('/sendCommand', methods=['POST'])
def send_command():
    """
    工具方法，可以自己构造数据体向服务器上报指令

    必填参数:
    - commandData (dict): 指令数据，包含设备上报或控制指令的相关信息

    选填参数:
    - commandCode (str): 命令码，默认为 "T"
    """
    channel_camera = DeviceManager.get_channel_camera_service()

    try:
        # 获取并校验必填参数
        command_data = request.json.get("commandData")
        if not command_data:
            return jsonify({"error": "缺少必填参数: commandData"}), 400

        # 选填参数
        command_code = request.json.get("commandCode", "T")

        # 发送指令
        channel_camera.send_command(command_data, command_code)
        return jsonify({"message": f"成功"}), 200
    except Exception as e:
        logger.exception(f"通道相机发送指令失败: {e}")
        return jsonify({"message": "系统异常"}), 500


@channel_camera_bp.route('/alarmReport', methods=['POST'])
def alarm_report():
    """
    告警上报接口，故障类型包括：
    视频故障/算法未正常运行/图片编码失败/连接图片服务器失败/网络故障

    必填参数：
    message (str): 故障类型，包括：videoFault/algNotWork/jpgEncodeFault/ossNetFault/NetFault

    选填参数：
    moreInfo (str)：更多详细信息
    :return:
    """
    channel_camera = DeviceManager.get_channel_camera_service()

    try:
        # 获取并校验必填参数
        message = request.json.get("message")
        if not message:
            return jsonify({"error": "缺少必填参数: message"}), 400
        if message not in ["videoFault", "algNotWork", "jpgEncodeFault", "ossNetFault", "NetFault"]:
            return jsonify({"error": f"未知的告警类型{message}"}), 400
        # 选填参数
        more_info = request.json.get("moreInfo", "")

        content = {
            "cmd": "faultMessage",
            "cmdTime": str(int(time.time())),
            "deviceType": "5",  # 5为通道监控相机
            "deviceId": device_id,
            "message": message,   # 故障类型
            "moreInfo": more_info   # 可选，补充说明
        }
        channel_camera.send_command(content, "T")
        return jsonify({"message": "成功"}), 200
    except Exception as e:
        logger.exception(f"通道相机告警上报失败: {e}")
        return jsonify({"message": "系统异常"}), 500


@channel_camera_bp.route('/alarmRecoveryReport', methods=['POST'])
def alarm_recovery_report():
    """
    告警恢复上报接口，可恢复故障类型包括：
    视频故障/算法未正常运行/图片编码失败/连接图片服务器失败/网络故障

    必填参数：
    message (str): 要恢复的故障类型，包括：videoFault/algNotWork/jpgEncodeFault/ossNetFault/NetFault

    选填参数：
    moreInfo (str)：更多详细信息
    :return:
    """
    channel_camera = DeviceManager.get_channel_camera_service()
    try:
        # 获取并校验必填参数
        message = request.json.get("message")
        if not message:
            return jsonify({"error": "缺少必填参数: message"}), 400
        if message not in ["videoFault", "algNotWork", "jpgEncodeFault", "ossNetFault", "NetFault"]:
            return jsonify({"error": f"未知的告警类型{message}"}), 400
        # 选填参数
        more_info = request.json.get("moreInfo", "")

        content = {
            "cmd": "faultMessage",
            "cmdTime": str(int(time.time())),
            "deviceType": "5",  # 5为通道监控相机
            "deviceId": device_id,
            "recovery": message,     # 恢复告警类型
            "moreInfo": more_info   # 可选，补充说明
        }
        channel_camera.send_command(content, "T")
        return jsonify({"message": "成功"}), 200
    except Exception as e:
        logger.exception(f"通道相机告警恢复上报失败: {e}")
        return jsonify({"message": "系统异常"}), 500


@channel_camera_bp.route('/carTriggerEvent', methods=['POST'])
def car_trigger_event():
    """
    相机来去车事件上报接口
    触发事件：2：从下到上/去车；3：从上到下/来车

    必填参数：
    triggerFlag (int)：触发事件类型——2：去车；3：来车
    plate (str)：车牌号
    plateReliability (int)：车牌可信度
    carType (str)：车辆类型——小型车/大型车
    carColour (int)：车身颜色——0：无  1："白",  2："黑", 3："蓝", 4："黄", 5："绿"，6："红"

    :return:
    """
    channel_camera = DeviceManager.get_channel_camera_service()
    try:
        # 获取并校验必填参数
        try:
            data = request.get_json()
            trigger_flag = data["triggerFlag"]
            plate = data["plate"]
            plate_reliability = data["plateReliability"]
            car_type = data["carType"]
            car_colour = data["carColour"]
        except KeyError as e:
            return jsonify({"error": f"缺少必填参数: {str(e)}"}), 400
        # 校验事件类型
        if trigger_flag not in [2, 3]:
            return jsonify({"error": f"未知的事件类型{trigger_flag}"}), 400

        content = {
            "cmd": "reportInfo",
            "eventType": "trigerEvent",
            "eventId": uuid.uuid4(),  # 事件ID
            "triggerFlag": trigger_flag,     # 触发事件类型
            "cmdTime": str(int(time.time())),
            "deviceType": "5",  # 5为通道监控相机
            "deviceId": device_id,  # 设备ID
            "imageNum": "1",    # 图片张数，根据协议目前默认一张
            "num": "0",         # 当天事件序号，从0开始，默认序号0
            "plate": plate,     # 车牌号
            "plateReliability": plate_reliability,  # 车牌可信度
            "carType": car_type,        # 车辆类型
            "carColour": car_colour     # 车身颜色
        }
        channel_camera.send_command(content, "T")
        return jsonify({"message": "成功"}), 200
    except Exception as e:
        logger.exception(f"通道相机来去车事件上报失败: {e}")
        return jsonify({"message": "系统异常"}), 500


@channel_camera_bp.route('/carBackEvent', methods=['POST'])
def car_back_event():
    """
    相机后退事件上报接口
    触发类型：9：“/从上到下/来车”后车辆又后退；10: “/从下到上/去车”后车辆又后退

    必填参数：
    triggerFlag (int): 触发类型——9：来车后车辆又后退；10: 去车后车辆又后退
    plate (str)：车牌号
    plateReliability (int)：车牌可信度
    carType (str)：车辆类型；大型车/小型车
    carColour (int)：车身颜色——0：无  1："白",  2："黑", 3："蓝", 4："黄", 5："绿"，6："红"

    :return:
    """
    channel_camera = DeviceManager.get_channel_camera_service()
    try:
        # 获取并校验必填参数
        try:
            data = request.get_json()
            trigger_flag = data["triggerFlag"]
            plate = data["plate"]
            plate_reliability = data["plateReliability"]
            car_type = data["carType"]
            car_colour = data["carColour"]
        except KeyError as e:
            return jsonify({"error": f"缺少必填参数: {str(e)}"}), 400
        # 校验事件类型
        if trigger_flag not in [9, 10]:
            return jsonify({"error": f"未知的事件类型{trigger_flag}"}), 400

        content = {
            "cmd": "reportInfo",
            "eventType": "reverseEvent",
            "eventId": uuid.uuid4(),  # 事件ID
            "triggerFlag": trigger_flag,     # 触发事件类型
            "cmdTime": str(int(time.time())),
            "deviceType": "5",  # 5为通道监控相机
            "deviceId": device_id,  # 设备ID
            "imageNum": "1",    # 图片张数，根据协议目前默认一张
            "num": "0",         # 当天事件序号，从0开始，默认序号0
            "plate": plate,     # 车牌号
            "plateReliability": plate_reliability,  # 车牌可信度
            "carType": car_type,        # 车辆类型
            "carColour": car_colour     # 车身颜色
        }
        channel_camera.send_command(content, "T")
        return jsonify({"message": "成功"}), 200
    except Exception as e:
        logger.exception(f"通道相机后退事件上报失败: {e}")
        return jsonify({"message": "系统异常"}), 500


@channel_camera_bp.route('/carTrafficEvent', methods=['POST'])
def car_traffic_event():
    """
    相机交通流量状态上报接口
    区域状态——0：正常；1：繁忙；2：拥堵

    必填参数：
    areaState (int)： 区域状态， 0：正常；1：繁忙；2：拥堵
    area_state_reliability (int)： 区域状态可信度
    car_num (int)： 车辆数量

    :return:
    """
    channel_camera = DeviceManager.get_channel_camera_service()
    try:
        # 获取并校验必填参数
        try:
            data = request.get_json()
            area_state = data["area_state"]
            area_state_reliability = data["areaStateReliability"]
            car_num = data["carNum"]
        except KeyError as e:
            return jsonify({"error": f"缺少必填参数: {str(e)}"}), 400
        # 校验事件类型
        if area_state not in [0, 1, 2]:
            return jsonify({"error": f"未知的区域状态{area_state}"}), 400

        content = {
            "cmd": "reportInfo",
            "eventType": "trafficEvent",
            "cmdTime": str(int(time.time())),
            "deviceType": "5",      # 5为通道监控相机
            "eventId": uuid.uuid4(),  # 事件ID
            "areaState": area_state,    # 区域状态
            "areaStateReliability": area_state_reliability,     # 区域状态可信度
            "carNum": car_num,  # 车辆数量
            "imageNum": "1",    # 图片张数，根据协议目前默认一张
            "num": "0",     # 当天事件序号，从0开始
        }
        channel_camera.send_command(content, "T")
        return jsonify({"message": "成功"}), 200
    except Exception as e:
        logger.exception(f"通道相机交通流量上报失败: {e}")
        return jsonify({"message": "系统异常"}), 500
