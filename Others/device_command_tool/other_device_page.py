#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/30 17:47
# @Author  : Heshouyi
# @File    : other_device_page.py
# @Software: PyCharm
# @description:
import tkinter as tk


class OtherDevicePage:
    def __init__(self, root, tcp_client, app):
        self.root = root
        self.tcp_client = tcp_client
        self.app = app

    def setup(self):
        self.clear_window()
        container = tk.Frame(self.root)
        container.pack(expand=True)

        tk.Label(container, text="其他设备类型页面(暂未实现)").pack(pady=10)

        self.command_label = tk.Label(container, text="生成的指令：")
        self.command_label.pack(pady=10)

        button_frame = tk.Frame(container)
        button_frame.pack(pady=10)

        send_button = tk.Button(button_frame, text="发送指令", command=self.send_command)
        send_button.config(state=tk.DISABLED)
        send_button.grid(row=0, column=1, padx=10)

        disconnect_button = tk.Button(button_frame, text="返回设备选择界面", command=self.back2device_type_selection_page)
        disconnect_button.grid(row=0, column=2, padx=10)

        disconnect_button = tk.Button(button_frame, text="断开连接", command=self.disconnect)
        disconnect_button.grid(row=0, column=3, padx=10)

        self.generate_command()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def generate_command(self):
        """生成其他设备特定指令"""
        self.command = "(滴滴滴滴滴滴)"
        self.command_label.config(text=f"生成的指令：{self.command}")

    def send_command(self):
        self.tcp_client.send_command(self.command)

    def disconnect(self):
        """断开连接并返回初始界面"""
        self.tcp_client.disconnect()  # 断开与服务器的连接
        self.app.create_connection_page()  # 返回初始连接界面
        self.app.root.title("TCP设备指令模拟工具")

    def back2device_type_selection_page(self):
        """返回设备类型选择界面"""
        self.app.create_device_type_selection_page()
