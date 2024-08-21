#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/21 10:48
# @Author  : Heshouyi
# @File    : plate_recognition.py
# @Software: PyCharm
# @description:

def run(client):
    client.get("/device-access/device/recognitionTest", params={'url': 'plate_lib/鄂W39U02.jpg'})
