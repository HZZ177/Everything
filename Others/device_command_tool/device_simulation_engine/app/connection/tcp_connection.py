#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/9 下午7:48
# @Author  : Heshouyi
# @File    : tcp_connection.py
# @Software: PyCharm
# @description:

import socket
import threading
from ..utils.logger import logger
from ..utils.util import is_valid_ip


class TCPClient:
    def __init__(self):
        self.local_ip = None    # 用来连接服务器的设备IP
        self.server_socket = None
        self.server_ip = ""
        self.server_port = 0
        self.receive_callback = None    # 处理监控服务器下发数据的回调函数
        self.disconnect_callback = None    # 处理connection层主动断开时后续逻辑的回调函数

    def connect(self, server_ip, server_port, local_ip):
        """连接到服务器"""
        self.local_ip = local_ip
        try:
            # 检查本地IP是否合法
            if not is_valid_ip(local_ip):
                logger.error(f"无效的本地IP地址: {local_ip}")
                return False

            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((local_ip, 0))  # 绑定用于连接的本地IP和端口，端口0表示系统自动分配
            self.server_socket.connect((server_ip, server_port))
            self.server_socket.settimeout(5)    # 设置超时时间为5秒
            logger.info(f"成功使用本地IP：{local_ip}，连接到服务器：{server_ip}:{server_port} ")
            # 连接后启动监听线程，接收服务器返回的数据
            threading.Thread(target=self.receive_data, daemon=True).start()
        except Exception as e:
            logger.error(f"连接失败，错误信息: {e}")
            raise e

    def send_data(self, data, need_log=True):
        """发送数据到服务器"""
        if self.server_socket:
            try:
                # 如果data是字符串，则先encode成bytes，否则直接发送
                if isinstance(data, str):
                    data = data.encode()
                self.server_socket.sendall(data)
                if not need_log:    # 根据参数选择是否打印info日志，否则打debug，主要是为了过滤心跳日志
                    logger.debug(f"发送心跳包：{data}")
                else:
                    logger.info(f"发送数据: {data}")
            except Exception as e:
                logger.error(f"发送数据失败: {e}")
                raise e
        else:
            logger.error("尝试发送数据，但是还未与服务器建立连接")
            raise Exception("尝试发送数据，但是还未与服务器建立连接")

    def receive_data(self):
        """监听来自服务器的数据并调用回调处理"""
        while self.is_connected():
            try:
                # 检查是否已连接，因为是死循环接收，可能断连后无法及时停止
                if not self.server_socket:
                    logger.error("套接字未连接，停止接收数据")
                    break
                data = self.server_socket.recv(2048)    # 一旦缓冲区有数据可读，则接收数据并处理
                if data:
                    logger.debug(f"接收到原始数据: {data}")
                    if self.receive_callback:
                        self.receive_callback(data)     # 调用回调函数，将数据传回业务层处理
            except socket.timeout:
                continue    # 超时大概率是服务器一段时间内没有返回数据，可忽略
            except socket.error:
                continue    # 捕获异常，偶尔会因为连接断连的切换导致短时间内大量的网络错误，这里忽略
            except Exception as e:
                logger.error(f"接收服务器数据时出现未知错误: {e}")
                # self.disconnect()
                # logger.info("连接层主动断开连接，调用回调函数停止其他逻辑")
                # self.disconnect_callback()
                # break

    def disconnect(self):
        """断开连接"""
        if self.server_socket:
            self.server_socket.shutdown(socket.SHUT_RDWR)   # 先shutdown防止服务器端检测异常断开
            self.server_socket.close()
            self.server_socket = None
            self.receive_callback = None    # 断开连接后清空处理数据的回调函数
            logger.info("TCP连接已断开")

    def is_connected(self):
        return self.server_socket is not None

    def set_receive_callback(self, callback):
        """设置接收数据的回调函数"""
        self.receive_callback = callback

    def set_disconnect_callback(self, callback):
        """设置connection层主动断开时的回调函数"""
        self.disconnect_callback = callback
