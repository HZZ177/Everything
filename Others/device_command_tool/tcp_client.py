#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/30 17:46
# @Author  : Heshouyi
# @File    : tcp_client.py
# @Software: PyCharm
# @description:
import socket
import struct
import threading
from tkinter import messagebox
from utils import is_valid_ip


class TCPClient:
    def __init__(self, app):
        self.app = app
        self.server_socket = None
        self.server_ip = ""
        self.server_port = 0
        self.receive_callback = None  # 用于处理接收数据的回调函数

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
            if server_ip == "127.0.0.1":
                local_ip = "127.0.0.1"

            self.server_socket.bind((local_ip, 0))  # 端口号0表示由系统自动分配
            self.server_socket.connect((self.server_ip, self.server_port))
            # messagebox.showinfo("成功", "成功连接到服务器")

            # 启动一个线程用于接收led网络屏的服务器下发数据
            threading.Thread(target=self.receive_tcp_command, daemon=True).start()
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
                print(f"tcp_client：已发送指令: {command}")
            except Exception as e:
                messagebox.showerror("错误", f"发送指令时出错: {e}")
        else:
            messagebox.showwarning("警告", "未连接到服务器")

    def receive_tcp_command(self):
        """接收来自服务器的指令并按协议解析"""
        while self.is_connected():
            try:
                data = self.server_socket.recv(2048)  # 接收字节流，设置接收缓冲区的大小2048字节
                if data:
                    print(f"tcp_client：接收到字节流数据: {data}")

                    # 根据协议解析数据，例如假设协议包含如下字段：
                    # 协议头 (1字节), 时间戳 (4字节), 命令码 (1字节), 数据长度 (2字节), 数据内容 (N字节), 校验码 (2字节), 协议尾 (1字节)
                    protocol_head, timestamp, command_code, total_packets, packet_number, data_length = struct.unpack(
                        '>BIBHHH', data[:12])  # 假设前12字节包含头部字段

                    # 提取数据内容（根据data_length确定长度）
                    data_content = data[12:12 + data_length]
                    checksum, protocol_tail = struct.unpack('>HB', data[12 + data_length:12 + data_length + 3])

                    # 将解析结果输出到回调
                    parsed_data = {
                        "protocol_head": protocol_head,
                        "timestamp": timestamp,
                        "command_code": chr(command_code),
                        "total_packets": total_packets,
                        "packet_number": packet_number,
                        "data_length": data_length,
                        "data_content": data_content,
                        "checksum": checksum,
                        "protocol_tail": protocol_tail,
                    }

                    # 调用回调函数处理解析的数据
                    if self.receive_callback:
                        print("tcp_client：解析后的数据:", parsed_data)
                        self.app.root.after(0, self.receive_callback, parsed_data)
                else:
                    print("tcp_client：服务器主动断开连接")
                    messagebox.showerror("错误", "服务器主动断开连接！")
                    self.disconnect()
                    break
            except socket.timeout:
                continue  # 超时不一定是错误，可忽略并继续
            except socket.error as e:
                print(f"tcp_client：接收数据时网络错误: {e}")
                self.disconnect()
                # messagebox.showerror("错误", f"接收数据时出错: {e}")
                break
            except Exception as e:
                print(f"tcp_client：接收数据时出现未知错误: {e}")
                # messagebox.showerror("错误", f"接收数据时出现未知错误: {e}")
                break

    def disconnect(self):
        """断开连接"""
        if self.server_socket:
            self.server_socket.close()
            self.server_socket = None

    def is_connected(self):
        return self.server_socket is not None

    def set_receive_callback(self, callback):
        """设置接收数据时的回调函数"""
        self.receive_callback = callback
