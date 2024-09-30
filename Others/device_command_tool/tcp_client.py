#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/30 17:46
# @Author  : Heshouyi
# @File    : tcp_client.py
# @Software: PyCharm
# @description:
import socket
from tkinter import messagebox


class TCPClient:
    def __init__(self, app):
        self.app = app
        self.server_socket = None
        self.server_ip = ""
        self.server_port = 0
        self.detector_id = 1

    def connect_to_server(self, server_ip, server_port, detector_id):
        """尝试连接到服务器"""
        self.server_ip = server_ip
        self.server_port = int(server_port)
        self.detector_id = int(detector_id)

        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.settimeout(5)  # 设置超时为5秒
            self.server_socket.connect((self.server_ip, self.server_port))
            messagebox.showinfo("成功", "成功连接到服务器")
            return True  # 成功连接返回True
        except socket.timeout:
            messagebox.showerror("错误", "连接服务器超时，请检查网络连接或服务器状态")
        except Exception as e:
            messagebox.showerror("错误", f"无法连接到服务器: {e}")

        return False  # 连接失败返回False

    def send_command(self, command):
        """发送生成的指令到服务器"""
        if self.server_socket:
            try:
                self.server_socket.sendall(command.encode())
            except Exception as e:
                messagebox.showerror("错误", f"发送指令时出错: {e}")
        else:
            messagebox.showwarning("警告", "未连接到服务器")

    def disconnect(self):
        """断开连接"""
        if self.server_socket:
            self.server_socket.close()
            self.server_socket = None
            messagebox.showinfo("断开", "已断开与服务器的连接")
