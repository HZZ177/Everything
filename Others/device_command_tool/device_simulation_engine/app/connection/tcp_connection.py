#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/9 下午7:48
# @Author  : Heshouyi
# @File    : tcp_connection.py
# @Software: PyCharm
# @description:

import socket
import struct
from ..utils.logger import logger
from ..utils.util import is_valid_ip


class TCPClient:
    def __init__(self):
        self.server_socket = None
        self.server_ip = ""
        self.server_port = 0
        self.receive_callback = None

    def connect(self, server_ip, server_port, local_ip="0.0.0.0"):
        """连接到服务器"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((local_ip, 0))
            self.server_socket.connect((server_ip, server_port))
            self.server_socket.settimeout(5)
            logger.info(f"连接到服务器 {server_ip}: {server_port} ")
            return True
        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            self.disconnect()
            return False

    def send_data(self, data):
        """发送数据到服务器"""
        if self.server_socket:
            try:
                if isinstance(data, str):
                    data = data.encode()
                self.server_socket.sendall(data)
                logger.info(f"Sent data: {data}")
            except Exception as e:
                logger.error(f"Error sending data: {e}")
                self.disconnect()
        else:
            logger.error("No active connection")

    def receive_data(self):
        """接收来自服务器的数据并调用回调处理"""
        try:
            while self.is_connected():
                data = self.server_socket.recv(2048)
                if data:
                    logger.info(f"Received raw data: {data}")
                    if self.receive_callback:
                        self.receive_callback(data)
                else:
                    logger.warning("Connection closed by server")
                    self.disconnect()
                    break
        except Exception as e:
            logger.error(f"Error receiving data: {e}")
            self.disconnect()

    def disconnect(self):
        """断开连接"""
        if self.server_socket:
            self.server_socket.close()
            self.server_socket = None
            logger.info("Disconnected from server")

    def is_connected(self):
        return self.server_socket is not None

    def set_receive_callback(self, callback):
        """设置接收数据的回调函数"""
        self.receive_callback = callback
