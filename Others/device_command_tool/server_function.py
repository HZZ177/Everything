#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/10/10 10:52
# @Author  : Heshouyi
# @File    : server_function.py
# @Software: PyCharm
# @description: 服务器相关部分功能实现

import requests
from tkinter import messagebox


class ServerFunctions:
    def __init__(self, server_ip):
        self.server_ip = server_ip

    def get_all_online_device_info(self):
        """调用findCarServer获取并更新所有在线设备信息"""
        url = f"http://{self.server_ip}:8080/device-access/device/getAllOnLineDeviceInfo"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise e

    def device_status_test(self):
        """channel刷新所有设备状态"""
        url = f"http://{self.server_ip}:7072/tool/deviceStatusTest"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise e
