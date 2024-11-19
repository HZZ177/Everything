#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/9 下午7:28
# @Author  : Heshouyi
# @File    : channel_camera_api.py
# @Software: PyCharm
# @description:

import time
from ..utils.util import generate_uuid
from flask import Blueprint, request, jsonify
from functools import wraps
from enum import Enum
from ..utils.logger import logger
from ..utils.configer import config
from ..services.device_manager import DeviceManager

# 创建蓝图
channel_camera_bp = Blueprint("channel_camera", __name__)
# 从配置文件获取通道相机设备信息
device_id = config["devices_info"]["channel_camera"]["device_id"]
device_version = config["devices_info"]["channel_camera"]["device_version"]


# 枚举类：用于定义事件类型和颜色类型
class CarTriggerFlag(Enum):
    """
    相机触发事件枚举值
    2-去车
    3-来车
    """
    TO_CAR = 2
    FROM_CAR = 3


class CarBackFlag(Enum):
    """
    相机后退事件枚举值
    9-来车后车辆又后退
    9-去车后车辆又后退
    """
    BACK_FROM_CAR = 9
    BACK_TO_CAR = 10


class CarColour(Enum):
    """
    车牌颜色枚举值
    0：无  1："白",  2："黑", 3："蓝", 4："黄", 5："绿"，6："红"
    """
    NONE = 0
    WHITE = 1
    BLACK = 2
    BLUE = 3
    YELLOW = 4
    GREEN = 5
    RED = 6


class AreaState(Enum):
    """
    区域交通流量状态
    0：正常；1：繁忙；2：拥堵
    """
    NORMAL = 0
    BUSY = 1
    JAM = 2


# 工具函数和装饰器
def handle_exceptions(func):
    """处理通用异常装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception(f"通道相机接口调用时系统异常: {e}")
            return error_response()
    return wrapper


def success_response(message="成功", data=None):
    """生成成功响应"""
    return jsonify({"message": message, "data": data}), 200


def error_response(message="系统异常", code=500):
    """生成失败响应"""
    return jsonify({"message": message}), code


def validate_json(required_fields, request_data):
    """
    校验接口JSON传参必填参数
    校验通过返回None，校验失败返回错误信息
    """
    missing_fields = [field for field in required_fields if field not in request_data]
    if missing_fields:
        return jsonify({"error": f"缺少必填参数: {', '.join(missing_fields)}"}), 400
    return None


def get_channel_camera():
    """获取通道相机实例"""
    return DeviceManager.get_channel_camera_service()


# API 路由
@channel_camera_bp.route('/connect', methods=['GET'])
@handle_exceptions
def connect():
    """尝试连接设备到服务器，连接后发送注册包，开启心跳"""
    logger.info("通道相机connect接口被调用")
    camera = get_channel_camera()
    camera.connect()
    camera.send_register_packet()
    camera.start_heartbeat()
    logger.info("通道相机成功连接服务器")
    return success_response()


@channel_camera_bp.route('/disconnect', methods=['GET'])
@handle_exceptions
def disconnect():
    """断开连接"""
    logger.info("通道相机disconnect接口被调用")
    camera = get_channel_camera()
    camera.disconnect()
    logger.info("通道相机成功断开连接")
    return success_response()


@channel_camera_bp.route('/startHeartbeat', methods=['GET'])
@handle_exceptions
def start_heartbeat():
    """开启持续心跳"""
    logger.info("通道相机startHeartbeat接口被调用")
    camera = get_channel_camera()
    camera.start_heartbeat()
    logger.info("通道相机成功开启心跳")
    return success_response()


@channel_camera_bp.route('/stopHeartbeat', methods=['GET'])
@handle_exceptions
def stop_heartbeat():
    """停止心跳"""
    logger.info("通道相机stopHeartbeat接口被调用")
    camera = get_channel_camera()
    camera.stop_heartbeat()
    logger.info("通道相机成功停止心跳")
    return success_response()


@channel_camera_bp.route('/sendCommand', methods=['POST'])
@handle_exceptions
def send_command():
    """
    工具方法，构造数据体向服务器上报指令，默认T包
    需要自己提供发送的所有消息体部分
    :return:
    """
    logger.info("通道相机sendCommand接口被调用")
    # 检验必填参数
    data = request.get_json()
    validation_error = validate_json(["commandData"], data)
    if validation_error:
        return validation_error

    # 校验参数合法性
    command_data = data["commandData"]

    camera = get_channel_camera()
    camera.send_command(command_data, command_code="T")
    logger.info(f"通道相机成功发送指令: {command_data}")
    return success_response()


@channel_camera_bp.route('/alarmReport', methods=['POST'])
@handle_exceptions
def alarm_report():
    """
    告警上报接口，故障类型包括：
    视频故障/算法未正常运行/图片编码失败/连接图片服务器失败/网络故障

    必填参数：
    message (str): 故障类型：videoFault/algNotWork/jpgEncodeFault/ossNetFault/NetFault

    选填参数：
    moreInfo (str)：更多详细信息
    :return:
    """
    logger.info("通道相机alarmReport接口被调用")
    # 检验必填参数
    data = request.get_json()
    validation_error = validate_json(["message"], data)
    if validation_error:
        return validation_error

    # 校验参数合法性
    message = data["message"]
    more_info = data.get("moreInfo", "")

    if message not in ["videoFault", "algNotWork", "jpgEncodeFault", "ossNetFault", "NetFault"]:
        return error_response(f"未知的告警类型: {message}", 400)

    # 组装上报数据
    content = {
        "cmd": "faultMessage",
        "cmdTime": str(int(time.time())),
        "deviceType": "5",
        "deviceId": device_id,
        "message": message,
        "moreInfo": more_info
    }

    camera = get_channel_camera()
    camera.send_command(content, "T")
    logger.info(f"通道相机成功上报告警: {message}")
    return success_response()


@channel_camera_bp.route('/alarmRecoveryReport', methods=['POST'])
@handle_exceptions
def alarm_recovery_report():
    """
    告警恢复上报接口，可恢复故障类型包括：
    视频故障/算法未正常运行/图片编码失败/连接图片服务器失败/网络故障

    必填参数：
    message (str): 要恢复的故障类型：videoFault/algNotWork/jpgEncodeFault/ossNetFault/NetFault

    选填参数：
    moreInfo (str)：更多详细信息
    :return:
    """
    logger.info("通道相机alarmRecoveryReport接口被调用")
    # 检验必填参数
    data = request.get_json()
    validation_error = validate_json(["message"], data)
    if validation_error:
        return validation_error

    # 校验参数合法性
    message = data["message"]
    more_info = data.get("moreInfo", "")

    if message not in ["videoFault", "algNotWork", "jpgEncodeFault", "ossNetFault", "NetFault"]:
        return error_response(f"未知的告警类型: {message}", 400)

    # 组装上报数据
    content = {
        "cmd": "faultMessage",
        "cmdTime": str(int(time.time())),
        "deviceType": "5",
        "deviceId": device_id,
        "recovery": message,
        "moreInfo": more_info
    }

    camera = get_channel_camera()
    camera.send_command(content, "T")
    logger.info(f"通道相机成功上报告警恢复: {message}")
    return success_response()


@channel_camera_bp.route('/carTriggerEvent', methods=['POST'])
@handle_exceptions
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
    logger.info("通道相机carTriggerEvent接口被调用")
    # 检验必填参数
    required_fields = ["triggerFlag", "plate", "plateReliability", "carType", "carColour"]
    data = request.get_json()
    validation_error = validate_json(required_fields, data)
    if validation_error:
        return validation_error

    # 校验参数合法性
    trigger_flag = data["triggerFlag"]
    plate = data["plate"]
    plate_reliability = data["plateReliability"]
    car_type = data["carType"]
    car_colour = data["carColour"]

    if trigger_flag not in (item.value for item in CarTriggerFlag):
        return error_response(f"未知的车位事件类型: {trigger_flag}", 400)
    if plate_reliability not in range(0, 1001):
        return error_response(f"无效的可信度 {plate_reliability}，取值范围0-1000: ", 400)
    if car_type not in ["小型车", "大型车"]:
        return error_response(f"无效的车辆类型: {car_type}", 400)
    if car_colour not in (item.value for item in CarColour):
        return error_response(f"无效的车辆颜色: {car_colour}", 400)

    # 组装上报数据
    content = {
        "cmd": "reportInfo",
        "eventType": "trigerEvent",     # trigerEvent没写错，协议就是这个单词
        "eventId": generate_uuid(),
        "triggerFlag": trigger_flag,
        "cmdTime": str(int(time.time())),
        "deviceType": "5",
        "deviceId": device_id,
        "plate": plate,
        "plateReliability": plate_reliability,
        "carType": car_type,
        "carColour": car_colour
    }

    camera = get_channel_camera()
    camera.send_command(content, "T")
    logger.info(f"通道相机成功上报事件类型: {trigger_flag}")
    return success_response()


@channel_camera_bp.route('/carBackEvent', methods=['POST'])
@handle_exceptions
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
    logger.info("通道相机carBackEvent接口被调用")
    # 检验必填参数
    required_fields = ["triggerFlag", "plate", "plateReliability", "carType", "carColour"]
    data = request.get_json()
    validation_error = validate_json(required_fields, data)
    if validation_error:
        return validation_error

    # 校验参数合法性
    trigger_flag = data["triggerFlag"]
    plate = data["plate"]
    plate_reliability = data["plateReliability"]
    car_type = data["carType"]
    car_colour = data["carColour"]

    if trigger_flag not in (item.value for item in CarBackFlag):
        return error_response(f"未知的后退事件类型: {trigger_flag}", 400)
    if plate_reliability not in range(0, 1001):
        return error_response(f"无效的可信度 {plate_reliability}，取值范围0-1000: ", 400)
    if car_type not in ["小型车", "大型车"]:
        return error_response(f"无效的车辆类型: {car_type}", 400)
    if car_colour not in (item.value for item in CarColour):
        return error_response(f"无效的车辆颜色: {car_colour}", 400)

    # 组装上报数据
    content = {
        "cmd": "reportInfo",
        "eventType": "trigerEvent",     # trigerEvent没写错，协议就是这个单词
        "eventId": generate_uuid(),
        "triggerFlag": trigger_flag,
        "cmdTime": str(int(time.time())),
        "deviceType": "5",
        "deviceId": device_id,
        "plate": plate,
        "plateReliability": plate_reliability,
        "carType": car_type,
        "carColour": car_colour
    }

    camera = get_channel_camera()
    camera.send_command(content, "T")
    logger.info(f"通道相机成功上报后退事件: {trigger_flag}")
    return success_response()


@channel_camera_bp.route('/carTrafficEvent', methods=['POST'])
@handle_exceptions
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
    logger.info("通道相机carTrafficEvent接口被调用")
    # 检验必填参数
    required_fields = ["areaState", "areaStateReliability", "carNum"]
    data = request.get_json()
    validation_error = validate_json(required_fields, data)
    if validation_error:
        return validation_error

    # 校验参数合法性
    area_state = data["areaState"]
    area_state_reliability = data["areaStateReliability"]
    car_num = data["carNum"]

    if area_state not in (item.value for item in AreaState):
        return error_response(f"未知的区域状态: {data['areaState']}", 400)
    if area_state_reliability not in range(0, 1001):
        return error_response(f"无效的区域状态可信度 {area_state_reliability}，取值范围0-1000: ", 400)

    # 组装上报数据
    content = {
        "cmd": "reportInfo",
        "eventType": "trafficEvent",
        "cmdTime": str(int(time.time())),
        "deviceType": "5",
        "deviceId": device_id,
        "areaState": area_state,
        "areaStateReliability": area_state_reliability,
        "carNum": car_num
    }

    camera = get_channel_camera()
    camera.send_command(content, "T")
    logger.info(f"通道相机成功上报交通流量状态: {data['areaState']}")
    return success_response()
