#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/9 下午7:28
# @Author  : Heshouyi
# @File    : parking_camera_api.py
# @Software: PyCharm
# @description:

from flask import Blueprint, request, jsonify
from functools import wraps
from enum import Enum
from ..services.device_manager import DeviceManager
from ..utils.logger import logger
from ..utils.util import get_inner_picture
from ..services.parking_camera_service import ParkingCameraService


# 创建蓝图对象
parking_camera_bp = Blueprint("parking_camera", __name__)


# 枚举类，维护各种数据类型对应值
class ParkingEvent(Enum):
    """
    车位状态枚举值
    0：无车；1：有车；2：出车；3：进车；4：设备故障；5：压线告警：6：压线取消
    """
    NO_CAR = 0
    HAS_CAR = 1
    CAR_OUT = 2
    CAR_IN = 3
    FAULT = 4
    PRESSURE = 5
    PRESSURE_CANCEL = 6


# 公共工具函数和装饰器
def handle_exceptions(func):
    """通用异常处理装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception(f"调用车位相机接口时系统异常: {e}")
            return jsonify({"message": "系统异常"}), 500
    return wrapper


def success_response(message="成功", data=None):
    """生成成功响应"""
    return jsonify({"message": message, "data": data}), 200


def error_response(message="系统异常", code=500):
    """生成失败响应"""
    return jsonify({"message": message}), code


def validate_json(required_fields, request_data):
    """
    校验接口JSON必填参数
    :param required_fields: 必填参数列表
    :param request_data: 接口请求传入的数据
    :return:
    """
    missing_fields = [field for field in required_fields if field not in request_data]
    if missing_fields:
        return jsonify({"error": f"缺少必填参数: {', '.join(missing_fields)}"}), 400
    return None


def validate_form_field(field_name, data, valid_values=None):
    """
    检查表单字段中的整数必填参数，可选校验范围，没有范围不校验
    :param field_name: 要校验的表单字段名称（字符串类型）
    :param data: 表单数据，一般通过request.form获取，类型为dict
    :param valid_values: 可选的字段取值范围（列表或其他可迭代对象）如果不为None，字段值必须在这个范围内
    :return:
    """
    try:
        value = int(data.get(field_name))
    except (TypeError, ValueError):
        return jsonify({"error": f"缺少必填参数: {field_name}或参数不是有效的整数"}), 400
    if valid_values and value not in valid_values:
        return jsonify({"error": f"错误的参数值: {field_name}={value}，有效范围: {valid_values}"}), 400
    return value


def get_parking_camera():
    """获取车位相机设备实例"""
    service: ParkingCameraService = DeviceManager.get_parking_camera_service()
    return service


# 核心 API 路由
@parking_camera_bp.route('/connect', methods=['GET'])
@handle_exceptions
def connect():
    """
    尝试连接设备到服务器
    连接后发送注册包并开启心跳
    :return:
    """
    logger.info("车位相机connect接口被调用")
    parking_camera = get_parking_camera()
    parking_camera.connect()
    logger.info("车位相机成功连接服务器")
    return success_response()


@parking_camera_bp.route('/disconnect', methods=['GET'])
@handle_exceptions
def disconnect():
    """
    断开服务器连接并停止心跳
    :return:
    """
    logger.info("车位相机disconnect接口被调用")
    parking_camera = get_parking_camera()
    parking_camera.disconnect()
    logger.info("车位相机成功断开连接")
    return success_response()


@parking_camera_bp.route('/startHeartbeat', methods=['GET'])
@handle_exceptions
def start_heartbeat():
    """
    开启持续心跳
    :return:
    """
    logger.info("车位相机startHeartbeat接口被调用")
    parking_camera = get_parking_camera()
    parking_camera.start_heartbeat()
    logger.info("车位相机成功开启心跳")
    return success_response()


@parking_camera_bp.route('/stopHeartbeat', methods=['GET'])
@handle_exceptions
def stop_heartbeat():
    """
    停止心跳
    :return:
    """
    logger.info("车位相机stopHeartbeat接口被调用")
    parking_camera = get_parking_camera()
    parking_camera.stop_heartbeat()
    logger.info("车位相机成功停止心跳")
    return success_response()


@parking_camera_bp.route('/parkingStatusReport', methods=['POST'])
@handle_exceptions
def parking_status_report():
    """
    上报单个车位状态（事件）
    必填参数：
    port (int): 车位号——范围1-6
    parkEvent (int): 车位状态——0：无车；1：有车；2：出车；3：进车；4：设备故障；5：压线告警：6：压线取消
    """
    logger.info("车位相机parkingStatusReport接口被调用")
    # 校验必填参数
    data = request.get_json()
    validation_error = validate_json(["port", "parkEvent"], data)
    if validation_error:
        return validation_error

    # 校验参数合法性
    park_num = data["port"]
    park_event = data["parkEvent"]

    if park_num not in range(1, 7):     # 车位号范围1-6
        return error_response(f"错误的车位号: {park_num}，范围应为1-6", 400)
    if park_event not in (item.value for item in ParkingEvent):
        return error_response(f"错误的事件类型: {park_event}，范围应为0-6", 400)

    parking_camera = get_parking_camera()   # 获取设备实例
    parking_camera.send_parking_status(park_num, park_event)    # 上报车位状态
    logger.info(f"车位相机上报车位状态成功，车位号: {park_num}, 车位状态: {park_event}")
    return success_response()


@parking_camera_bp.route('/uploadParkingPicture', methods=['POST'])
@handle_exceptions
def upload_parking_picture():
    """
    上报车位图片，目前只支持软识别模式
    必填参数：
        parkNum (int): 车位号
    以下两个必填其一：
        image (file): 车牌图片，base64编码
        innerPic (str): 内置图片名称
    """
    logger.info("车位相机uploadParkingPicture接口被调用")
    # 校验必填参数；因为涉及文件上传，需要使用表单类型提交，所以用form获取，另起一个检验方法
    park_num = validate_form_field("parkNum", request.form, valid_values=range(1, 7))
    if isinstance(park_num, tuple):  # 校验不通过会返回flask的错误对象，直接返回错误信息
        return park_num

    # 校验image和innerPic至少存在一个
    image = request.files.get('image')  # 上传的图片文件
    inner_pic = request.form.get('innerPic')  # 内置图片名称
    if not image and not inner_pic:
        return error_response("image或innerPic至少需要填一个", 400)

    # 获取图片数据
    if inner_pic:   # 如果有内置图片，尝试获取，忽略自定义上传图片参数
        image_bytes = get_inner_picture(inner_pic)
        if image_bytes is None:
            return error_response(f"无法找到内置图片: {inner_pic}", 400)
    else:
        image_bytes = image.read()  # 如果没有指定内置图片，将上传的文件转换为二进制数据

    parking_camera = get_parking_camera()   # 获取设备实例
    parking_camera.upload_picture(park_num, image_bytes)    # 上传图片
    logger.info(f"车位相机{park_num}号车位成功上报车位图片")
    return success_response()
