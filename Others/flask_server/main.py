#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/25 10:50
# @Author  : Heshouyi
# @File    : upodate_collections_by_casenum.py
# @Software: PyCharm
# @description:

from flask import Flask, request, jsonify
from common.log_tool import logger
import json

app = Flask(__name__)


@app.route('/findcar-report', methods=['POST'])
def findcar_report():
    if request.is_json:
        # 如果传入的是 JSON 格式
        data = request.json
        logger.info(f'findcar_report 接收到 JSON 数据上报: {json.dumps(data, ensure_ascii=False)}')
    else:
        # 如果不是 JSON，则处理为字节流
        data = request.get_data()  # 获取原始字节数据
        logger.info(f'findcar_report 接收到字节数据上报: {data}')

    # 返回数据，包含原始字符或字节数据
    return jsonify({"received_data": data if request.is_json else list(data)}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1777)
