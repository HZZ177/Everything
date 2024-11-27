#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/25 13:51
# @Author  : Heshouyi
# @File    : websocket_connection.py
# @Software: PyCharm
# @description:

import websocket
import threading
from ..utils.logger import logger


class WebSocketClient:
    def __init__(self):
        self.ws = None
        self.server_url = ""    # 服务器地址，需要以ws://或wss://开头
        self.receive_callback = None  # 处理服务器下发数据的回调函数
        self.disconnect_callback = None  # 处理主动断开连接时的回调函数
        self.connected = False

    def connect(self, server_url):
        """连接到服务器"""
        self.server_url = server_url
        try:
            self.ws = websocket.WebSocket()
            self.ws.connect(server_url, timeout=5)  # 设置连接超时时间为5秒
            self.connected = True
            logger.debug(f"成功连接到WebSocket服务器：{server_url}")
            # 启动线程接收数据
            threading.Thread(target=self.receive_data, daemon=True).start()
        except Exception as e:
            logger.error(f"WebSocket连接失败，错误信息: {e}")
            self.connected = False
            raise e

    def send_data(self, data, need_log=True):
        """发送数据到服务器"""
        if self.ws and self.connected:
            try:
                if isinstance(data, str):
                    self.ws.send(data)
                else:
                    raise ValueError("WebSocket数据必须是字符串类型")

                if not need_log:
                    logger.debug(f"发送数据：{data}")
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
        while self.connected:
            try:
                if not self.ws:
                    logger.error("WebSocket未连接，停止接收数据")
                    break

                data = self.ws.recv()  # 阻塞等待接收数据
                if data:
                    logger.debug(f"接收到原始数据: {data}")
                    if self.receive_callback:
                        self.receive_callback(data)  # 调用回调函数处理数据
            except websocket.WebSocketTimeoutException:
                continue  # 超时大概率是服务器一段时间内没有返回数据，可忽略
            except websocket.WebSocketConnectionClosedException:
                logger.warning("WebSocket连接已关闭")
                self.disconnect()
                break
            except Exception as e:
                logger.error(f"接收服务器数据时出现未知错误: {e}")

    def disconnect(self):
        """断开连接"""
        if self.ws:
            try:
                self.ws.close()
                self.ws = None
                self.connected = False
                logger.info("WebSocket连接已断开")
            except Exception as e:
                logger.error(f"断开WebSocket连接失败: {e}")

    def is_connected(self):
        return self.connected

    def set_receive_callback(self, callback):
        """设置接收数据的回调函数"""
        self.receive_callback = callback

    def set_disconnect_callback(self, callback):
        """设置主动断开连接时的回调函数"""
        self.disconnect_callback = callback
