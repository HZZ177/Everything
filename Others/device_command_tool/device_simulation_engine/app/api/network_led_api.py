#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/9 下午7:28
# @Author  : Heshouyi
# @File    : network_led_api.py
# @Software: PyCharm
# @description:

from flask import Blueprint, request, jsonify
# from ..services.network_led_service import send_network_led_data

# 创建蓝图对象
network_led_bp = Blueprint("network_led", __name__)


# @network_led_bp.route("/send_data", methods=["POST"])
# def send_data():
#     data = request.json
#     if not data:
#         return jsonify({"status": "error", "message": "无效的JSON"}), 400
#
#     response = send_network_led_data(data)
#     return jsonify(response)
