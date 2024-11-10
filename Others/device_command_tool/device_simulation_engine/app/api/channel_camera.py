#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/9 下午7:28
# @Author  : Heshouyi
# @File    : channel_camera.py
# @Software: PyCharm
# @description:

from flask import Blueprint, request, jsonify
from ..services.channel_camera_service import send_channel_camera_data

# 创建蓝图对象
channel_camera_bp = Blueprint("channel_camera", __name__)


@channel_camera_bp.route("/send_data", methods=["POST"])
def send_data():
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "无效的JSON"}), 400

    response = send_channel_camera_data(data)
    return jsonify(response)
