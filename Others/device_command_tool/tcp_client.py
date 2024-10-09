#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/30 17:46
# @Author  : Heshouyi
# @File    : tcp_client.py
# @Software: PyCharm
# @description:
import socket
from tkinter import messagebox
from utils import is_valid_ip


class TCPClient:
    def __init__(self, app):
        self.app = app
        self.server_socket = None
        self.server_ip = ""
        self.server_port = 0

    def connect_to_server(self, server_ip, server_port, local_ip, event=None) -> bool:
        """尝试连接到服务器"""
        # 验证IP地址格式
        if not is_valid_ip(server_ip):
            messagebox.showerror("输入错误", "请输入有效的服务器IP地址。")
            return False

        # 验证本地IP地址格式
        if not is_valid_ip(local_ip):
            messagebox.showerror("输入错误", "请选择有效的本地IP地址。")
            return False

        # 验证端口号是否为有效的整数且在1-65535之间
        try:
            port_num = int(server_port)
            if not (1 <= port_num <= 65535):
                messagebox.showerror("输入错误", "请输入有效的端口号（1-65535）")
                return False
        except ValueError:
            messagebox.showerror("输入错误", "端口号必须是整数")
            return False

        self.server_ip = server_ip
        self.server_port = port_num

        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.settimeout(5)  # 设置超时为5秒

            # 绑定到指定的本地IP地址
            # 如果服务器IP是回环地址，绑定本地地址到本地回环地址，否则局域网地址连接回环地址会报错
            if server_ip == "127.0.0.1":
                local_ip = "127.0.0.1"

            self.server_socket.bind((local_ip, 0))  # 端口号0表示由系统自动分配

            self.server_socket.connect((self.server_ip, self.server_port))
            # messagebox.showinfo("成功", "成功连接到服务器")
            return True
        except socket.timeout:
            messagebox.showerror("错误", "连接服务器超时，请检查网络连接或服务器状态")
        except Exception as e:
            messagebox.showerror("错误", f"无法连接到服务器: {e}")

        return False

    def send_command(self, command):
        """发送生成的指令到服务器"""
        if self.server_socket:
            try:
                # 如果command是字符串，则先encode成bytes，否则直接发送
                if isinstance(command, str):
                    command = command.encode()

                # 发送指令到服务器
                self.server_socket.sendall(command)
                print(f"已发送指令: {command}")
            except Exception as e:
                messagebox.showerror("错误", f"发送指令时出错: {e}")
        else:
            messagebox.showwarning("警告", "未连接到服务器")

    def disconnect(self):
        """断开连接"""
        if self.server_socket:
            self.server_socket.close()
            self.server_socket = None

    def is_connected(self):
        if self.server_socket is None:
            return False
        else:
            return True
