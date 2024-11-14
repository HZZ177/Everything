#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/12 11:25
# @Author  : Heshouyi
# @File    : test.py
# @Software: PyCharm
# @description:

import requests


def channel_camera_connect():
    url = "http://127.0.0.1:1777/api/channel_camera/connect"
    response = requests.get(url)
    print(response.text)


def channel_camera_disconnect():
    url = "http://127.0.0.1:1777/api/channel_camera/disconnect"
    response = requests.get(url)
    print(response.text)


def channel_camera_report_fault():
    url = "http://127.0.0.1:1777/api/channel_camera/alarm_report"
    data = {
        "message": "videoFault",
        "moreInfo": "视频故障测试"
    }
    response = requests.post(url, json=data)
    print(response.text)


def channel_camera_report_fault_recovery():
    url = "http://127.0.0.1:1777/api/channel_camera/alarm_recovery_report"
    data = {
        "message": "videoFault",
        "moreInfo": ""
    }
    response = requests.post(url, json=data)
    print(response.json())


if __name__ == '__main__':
    # channel_camera_connect()
    # channel_camera_disconnect()
    # channel_camera_report_fault()
    channel_camera_report_fault_recovery()

