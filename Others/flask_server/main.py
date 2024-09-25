#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/25 10:50
# @Author  : Heshouyi
# @File    : main.py
# @Software: PyCharm
# @description:

from flask import Flask, request, jsonify
from common.log_tool import logger

app = Flask(__name__)


@app.route('/findcar-report', methods=['POST'])
def findcar_report():
    data = request.json
    logger.info(f'findcar_report 接收到数据上报: {data}')  # 格式化输出接收日志
    return jsonify(data), 200   # 对发送端返回格式化数据


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
