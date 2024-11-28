#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/27 18:06
# @Author  : Heshouyi
# @File    : findcar_report_api.py
# @Software: PyCharm
# @description:

from functools import wraps
from flask import Blueprint, request, jsonify
from ..utils.logger import logger
from ..services.findcar_report_service import FindcarReportService

findcar_report_bp = Blueprint('findcar_report', __name__)


def handle_exceptions(func):
    """通用异常处理装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # 捕获异常时记录请求的所有信息
            logger.error(f"请求 URL: {request.url}")
            logger.error(f"请求方法: {request.method}")
            logger.error(f"请求头: {dict(request.headers)}")
            logger.error(f"请求体: {request.get_data(as_text=True)}")
            logger.exception(f"寻车接收上报信息时系统异常: {e}")
            return error_response()
    return wrapper

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


def success_response(message="成功", data=None):
    """生成成功响应"""
    return jsonify({"message": message, "data": data}), 200


def error_response(message="系统异常", code=500):
    """生成失败响应"""
    return jsonify({"message": message}), code


def get_findcar_report_service():
    """获取通道相机设备实例"""
    service: FindcarReportService = FindcarReportService()
    return service


@findcar_report_bp.route('/upper', methods=['POST'])
@handle_exceptions
def findcar_report():
    """
    接收服务器发来的上报数据，存库后格式化返回
    :return:
    """
    logger.info("寻车接收上报服务upper接口被调用")
    data = request.get_json()
    logger.info(f"接收到寻车上报数据 {data}")
    # 数据入库
    findcar_report_service = get_findcar_report_service()
    findcar_report_service.store_received_message(data)
    return success_response()


@findcar_report_bp.route('/getHistoryReport', methods=['POST'])
@handle_exceptions
def get_history_report():
    """
    查询数据库中记录的寻车上报历史数据
    必填参数：
        pageNo: 页码
        pageSize: 每页数量
    :return:
    """
    logger.info("寻车上报服务getHistoryReport接口被调用")
    # 校验必填参数
    data = request.json
    validation_error = validate_json(['pageNo', 'pageSize'], data)
    if validation_error:
        return validation_error

    page_no = data.get('pageNo', 1)
    page_size = data.get('pageSize', 10)
    # 分页页数和每页数量校验必须为正整数
    if not isinstance(page_no, int) or not isinstance(page_size, int):
        return error_response(message="分页参数必须为正整数")
    if page_no <= 0 or page_size <= 0:
        return error_response(message="分页参数必须为正整数")

    findcar_report_service = get_findcar_report_service()
    result = findcar_report_service.get_db_history_report(page_no, page_size)
    logger.info(f"寻车上报服务查询历史记录成功，返回结果：{result}")
    return success_response(data=result)
