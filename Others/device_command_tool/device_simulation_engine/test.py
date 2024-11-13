#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/12 11:25
# @Author  : Heshouyi
# @File    : test.py
# @Software: PyCharm
# @description:

import requests


def channel_camera_init():
    url = "http://127.0.0.1:7777/api/channel_camera/init"
    data = {
        "server_ip": "192.168.21.130",
        "server_port": 7799
    }
    response = requests.post(url, json=data)
    print(response.json())


def channel_camera_connect():
    url = "http://127.0.0.1:7777/api/channel_camera/connect"
    response = requests.post(url)
    print(response.json())


def channel_camera_disconnect():
    url = "http://127.0.0.1:7777/api/channel_camera/disconnect"
    response = requests.get(url)
    print(response.json())


if __name__ == '__main__':
    channel_camera_init()
    # channel_camera_connect()
    # channel_camera_disconnect()

