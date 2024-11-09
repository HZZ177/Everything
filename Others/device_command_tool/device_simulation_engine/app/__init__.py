#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/9 下午7:10
# @Author  : Heshouyi
# @File    : __init__.py.py
# @Software: PyCharm
# @description:

from flask import Flask
from api.channel_camera import channel_camera_bp
from api.network_led import network_led_bp
from api.parking_camera import parking_camera_bp
from utils.logger import logger


def create_app():
    app = Flask(__name__)

    # 注册蓝图
    app.register_blueprint(channel_camera_bp, url_prefix="/api/channel_camera")
    app.register_blueprint(network_led_bp, url_prefix="/api/network_led")
    app.register_blueprint(parking_camera_bp, url_prefix="/api/parking_camera")

    return app
