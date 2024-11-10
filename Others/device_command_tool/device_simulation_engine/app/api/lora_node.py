#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/9 下午7:29
# @Author  : Heshouyi
# @File    : lora_node.py
# @Software: PyCharm
# @description:

from flask import Blueprint, request, jsonify
from ..services.lora_node_service import send_lora_node_data

# 创建蓝图对象
lora_node_bp = Blueprint("lora_node", __name__)


@lora_node_bp.route("/send_data", methods=["POST"])
def send_data():
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "无效的JSON"}), 400

    response = send_lora_node_data(data)
    return jsonify(response)
