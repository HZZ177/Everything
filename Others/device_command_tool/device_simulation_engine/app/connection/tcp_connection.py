#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/9 下午7:48
# @Author  : Heshouyi
# @File    : tcp_connection.py
# @Software: PyCharm
# @description:

import socket
import struct
import threading
from ..utils.logger import logger
from ..utils.util import is_valid_ip


class TCPClient:
    def __init__(self):
        self.server_socket = None
        self.server_ip = ""
        self.server_port = 0
        self.receive_callback = None    # 回调函数

    def connect(self, server_ip, server_port, local_ip="0.0.0.0"):
        """连接到服务器"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((local_ip, 0))  # 绑定用于连接的本地IP和端口，端口0表示系统自动分配
            self.server_socket.connect((server_ip, server_port))
            self.server_socket.settimeout(5)
            logger.info(f"连接到服务器 {server_ip}: {server_port} ")
            # 连接后启动监听线程，接收服务器返回的数据
            threading.Thread(target=self.receive_data, daemon=True).start()
            return True
        except Exception as e:
            logger.error(f"连接失败，错误信息: {e}")
            self.disconnect()
            return False

    def send_data(self, data):
        """发送数据到服务器"""
        if self.server_socket:
            try:
                if isinstance(data, str):
                    data = data.encode()
                self.server_socket.sendall(data)
                logger.info(f"发送数据成功: {data}")
            except Exception as e:
                logger.error(f"发送数据失败: {e}")
                self.disconnect()
        else:
            logger.error("没有建立连接")

    def receive_data(self):
        """监听来自服务器的数据并调用回调处理"""
        try:
            while self.is_connected():
                data = self.server_socket.recv(2048)
                if data:
                    logger.info(f"接收到原始数据: {data}")
                    if self.receive_callback:
                        self.receive_callback(data)
                else:
                    logger.error("数据为空，断开连接")
                    self.disconnect()
        except socket.timeout:
            pass  # 超时不一定是错误，可忽略并继续
        except socket.error as e:
            logger.error(f"接收数据时网络错误: {e}")
            self.disconnect()
        except Exception as e:
            logger.error(f"接收数据时出现未知错误: {e}")

    def disconnect(self):
        """断开连接"""
        if self.server_socket:
            self.server_socket.close()
            self.server_socket = None
            self.receive_callback = None
            logger.info("断开连接")

    def is_connected(self):
        return self.server_socket is not None

    def set_receive_callback(self, callback):
        """设置接收数据的回调函数"""
        self.receive_callback = callback
