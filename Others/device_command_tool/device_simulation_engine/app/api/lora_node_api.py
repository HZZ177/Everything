#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/9 下午7:29
# @Author  : Heshouyi
# @File    : lora_node_api.py
# @Software: PyCharm
# @description:

from flask import Blueprint, request, jsonify
from functools import wraps
from enum import Enum
from ..utils.logger import logger
from ..utils.configer import config
from enum import Enum
from ..services.device_manager import DeviceManager

# 创建蓝图
lora_node_bp = Blueprint("lora_node", __name__)


# 工具函数和装饰器
def handle_exceptions(func):
    """通用异常处理装饰器"""
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
    校验接口JSON传参的必填参数
    校验通过返回None
    校验失败返回错误信息，包含缺少的具体参数信息
    """
    missing_fields = [field for field in required_fields if field not in request_data]
    if missing_fields:
        return jsonify({"error": f"缺少必填参数: {','.join(missing_fields)}"}), 400
    return None


def get_lora_node():
    """获取通道相机设备实例"""
    return DeviceManager.get_lora_node_service()


# API 路由
@lora_node_bp.route('/connect', methods=['GET'])
@handle_exceptions
def connect():
    """
    尝试连接设备到服务器
    :return:
    """
    logger.info("Lora节点connect接口被调用")
    lora_node = get_lora_node()
    lora_node.connect()
    logger.info("Lora节点成功连接服务器")
    return success_response()


@lora_node_bp.route('/disconnect', methods=['GET'])
@handle_exceptions
def disconnect():
    """
    断开服务器连接
    :return:
    """
    logger.info("Lora节点disconnect接口被调用")
    lora_node = get_lora_node()
    lora_node.disconnect()
    logger.info("Lora节点成功断开连接")
    return success_response()


@lora_node_bp.route('/reportStatus', methods=['POST'])
@handle_exceptions
def report_status():
    """
    上报节点下探测器状态，车位为故障时必须上报故障详情
    必填参数：
        sensorAddr (int): 探测器地址
        carStatus (int): 车位状态
        faultDetails (list[int]): 故障详情列表，每个元素为故障类型枚举值
    车位状态枚举值：
        0: 有车正常
        1: 有车故障
        2: 无车正常
        3: 无车故障
    故障详情枚举值：
        1: 传感器故障
        2: 传感器满偏
        3: 雷达故障
        4: 高低温预警
        5: RTC故障
        6: 通讯故障
        7: 电池低压

    :return:
    """
    try:
        data = request.json
        sensor_addr = data.get("sensor_addr")
        car_status = data.get("car_status")
        fault_details = data.get("fault_details", [])

        # 参数校验
        if not isinstance(sensor_addr, int) or sensor_addr <= 0:
            return jsonify({"error": "无效的车位地址"}), 400

        if not isinstance(car_status, int) or car_status not in [0, 1, 2, 3]:
            return jsonify({"error": f"无效的车位状态值: {car_status}"}), 400

        # 有故障状态时，必须有故障详情
        if car_status in [1, 3] and not fault_details:
            return jsonify({"error": "故障状态必须提供至少一个故障详情"}), 400

        # 调用 Service 层
        lora_node = get_lora_node()
        lora_node.report_status(sensor_addr, car_status, fault_details)

        return jsonify({"message": "状态上报成功"}), 200
    except Exception as e:
        return jsonify({"error": f"状态上报失败: {e}"}), 500
