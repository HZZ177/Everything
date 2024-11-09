#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/9 下午7:34
# @Author  : Heshouyi
# @File    : channel_camera_model.py
# @Software: PyCharm
# @description:

import struct


def pack_channel_camera_data(payload: bytes) -> bytes:
    header = 0xfb
    footer = 0xfe
    length = len(payload)
    packet = struct.pack(f"!B I {length}s B", header, length, payload, footer)
    return packet
