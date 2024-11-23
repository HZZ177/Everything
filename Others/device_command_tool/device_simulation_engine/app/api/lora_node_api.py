#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/9 下午7:29
# @Author  : Heshouyi
# @File    : lora_node_api.py
# @Software: PyCharm
# @description:

from flask import Blueprint, request, jsonify
from functools import wraps
from ..utils.logger import logger
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
            logger.exception(f"Lora节点接口调用时系统异常: {e}")
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
        sensorStatus (int): 车位状态
        faultDetails (list[int]): 故障详情列表，每个元素为故障类型枚举值
    车位状态枚举值：
        1: 有车正常 2: 无车正常 3: 有车故障 4: 无车故障
    故障详情枚举值：
        1: 传感器故障 2: 传感器满偏 3: 雷达故障 4: 高低温预警
        5: RTC故障 6: 通讯故障 7: 电池低压
    :return:
    """
    logger.info("Lora节点reportStatus接口被调用")
    try:
        data = request.json
        sensor_addr = data.get("sensorAddr")
        sensor_status = data.get("sensorStatus")
        fault_details = data.get("faultDetails")

        # 参数校验
        if not isinstance(sensor_addr, int) or sensor_addr <= 0:
            return jsonify({"error": f"无效的车位地址{sensor_addr}"}), 400

        if not isinstance(sensor_status, int) or sensor_status not in [1, 2, 3, 4]:
            return jsonify({"error": f"无效的探测器状态: {sensor_status}"}), 400

        if not isinstance(fault_details, list):
            return jsonify({"error": f"故障详情参数类型错误: {sensor_status}"}), 400

        # 故障详情范围1-7
        if any(fault_detail not in [1, 2, 3, 4, 5, 6, 7] for fault_detail in fault_details):
            return jsonify({"error": f"故障详情中包含无效值，有效范围位1-7的整数"}), 400

        # 上报为故障状态时，必须有故障详情
        if sensor_status in [3, 4]:
            if not fault_details:
                return jsonify({"error": "上报车位为故障状态时，必须提供至少一个故障详情"}), 400
        else:   # 如果车位状态为正常，强制将故障详情丢弃
            fault_details = []

        lora_node = get_lora_node()
        lora_node.report_status(sensor_addr, sensor_status, fault_details)
        return success_response(data="上报成功")
    except Exception:
        return error_response()


@lora_node_bp.route('/startReporting', methods=['POST'])
@handle_exceptions
def start_reporting():
    """
    开启持续上报，同时需提供持续上报的状态
    必填参数：
        sensorAddr (int): 探测器地址
        sensorStatus (int): 车位状态
        faultDetails (list[int]): 故障详情列表，每个元素为故障类型枚举值
    选填参数：
        reportInterval (int): 上报时间间隔，不传默认10s/次
    车位状态枚举值：
        1: 有车正常 2: 无车正常 3: 有车故障 4: 无车故障
    故障详情枚举值：
        1: 传感器故障 2: 传感器满偏 3: 雷达故障 4: 高低温预警
        5: RTC故障 6: 通讯故障 7: 电池低压
    :return:
    """
    logger.info("Lora节点startReporting接口被调用")
    try:
        data = request.json
        sensor_addr = data.get("sensorAddr")
        sensor_status = data.get("sensorStatus")
        fault_details = data.get("faultDetails")
        report_interval = data.get("reportInterval", 10)    # 上报的间隔时间，不传的话默认时间10s/次

        # 参数校验
        if not isinstance(sensor_addr, int) or sensor_addr <= 0:
            return jsonify({"error": f"无效的车位地址{sensor_addr}"}), 400

        if not isinstance(sensor_status, int) or sensor_status not in [0, 1, 2, 3]:
            return jsonify({"error": f"无效的探测器状态: {sensor_status}"}), 400

        if not isinstance(fault_details, list):
            return jsonify({"error": f"故障详情参数类型错误: {sensor_status}"}), 400

        if report_interval is not None and not isinstance(report_interval, int):
            return jsonify({"error": f"无效的上报时间间隔: {sensor_status}"}), 400

        # 故障详情范围1-7
        if any(fault_detail not in [1, 2, 3, 4, 5, 6, 7] for fault_detail in fault_details):
            return jsonify({"error": f"故障详情中包含无效值，有效范围位1-7的整数"}), 400

        # 有故障状态时，必须有故障详情
        if sensor_status in [3, 4]:
            if not fault_details:
                return jsonify({"error": "上报车位为故障状态时，必须提供至少一个故障详情"}), 400
        else:   # 如果车位状态为正常，强制将故障详情丢弃
            fault_details = []

        lora_node = get_lora_node()
        lora_node.start_reporting(sensor_addr, sensor_status, fault_details, report_interval)
        logger.info("Lora节点成功开启持续上报")
        return success_response(data="开启持续上报成功")
    except Exception:
        return error_response()


@lora_node_bp.route('/stopReporting', methods=['GET'])
@handle_exceptions
def stop_reporting():
    """
    停止持续上报
    :return:
    """
    logger.info("Lora节点stopReporting接口被调用")
    try:
        lora_node = get_lora_node()
        lora_node.stop_reporting()
        logger.info("Lora节点成功停止持续上报")
        return success_response(data="停止持续上报成功")
    except Exception:
        return error_response()
