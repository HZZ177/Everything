#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/30 17:46
# @Author  : Heshouyi
# @File    : main.py
# @Software: PyCharm
# @description:

import tkinter as tk
from tcp_client import TCPClient
from lora_device_page import LoraDevicePage
from other_device_page import OtherDevicePage


class TCPClientApp:
    def __init__(self, root):
        self.root = root
        self.center_window(self.root, relative_size=3, calculate_size=10)
        self.app_name = "TCP设备指令模拟工具"
        self.root.title(self.app_name)
        self.tcp_client = TCPClient(self)  # 创建TCP客户端实例

        # 绑定窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # 初始界面布局
        self.create_connection_page()

    def create_connection_page(self):
        """创建服务器连接界面"""
        self.clear_window()

        container = tk.Frame(self.root)
        container.pack(expand=True)

        tk.Label(container, text="服务器 IP:").pack(pady=10)
        self.server_ip_entry = tk.Entry(container)
        self.server_ip_entry.pack(pady=5)

        tk.Label(container, text="服务器端口:").pack(pady=10)
        self.server_port_entry = tk.Entry(container)
        self.server_port_entry.pack(pady=5)

        self.connect_button = tk.Button(container, text="连接服务器", command=self.connect_to_server)
        self.connect_button.pack(pady=20)

    def connect_to_server(self):
        """尝试连接到服务器"""
        server_ip = self.server_ip_entry.get().strip()
        server_port = self.server_port_entry.get().strip()
        # detector_id = self.detector_id_entry.get().strip()

        # 使用TCP客户端类进行连接
        if self.tcp_client.connect_to_server(server_ip, server_port):
            # 如果成功连接到服务器，更新窗口标题栏以显示当前IP地址
            self.root.title(f"{self.app_name} - 当前连接服务器：{server_ip}")

            # 跳转到设备类型选择页面
            self.create_device_type_selection_page()

    def create_device_type_selection_page(self):
        """创建设备类型选择页面"""
        self.clear_window()

        container = tk.Frame(self.root)
        container.pack(expand=True)

        tk.Label(container, text="请选择设备类型:").pack(pady=10)
        device_types = ["Lora节点", "其他设备类型"]
        self.selected_device_type = tk.StringVar(value="Lora节点")

        device_type_menu = tk.OptionMenu(container, self.selected_device_type, *device_types)
        device_type_menu.pack(pady=10)

        confirm_button = tk.Button(container, text="确认选择", command=self.on_device_type_selected)
        confirm_button.pack(pady=20)

    def on_device_type_selected(self):
        selected_type = self.selected_device_type.get()

        if selected_type == "Lora节点":
            self.load_lora_device_page()
        else:
            self.load_other_device_page()

    def load_lora_device_page(self):
        """加载Lora设备页面"""
        lora_page = LoraDevicePage(self.root, self.tcp_client, self)
        lora_page.setup()

    def load_other_device_page(self):
        """加载其他设备页面"""
        other_page = OtherDevicePage(self.root, self.tcp_client, self)
        other_page.setup()

    def clear_window(self):
        """清除窗口中的所有组件"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def center_window(self, target_window, relative_size=4, calculate_size=0):
        """窗口居中"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        width_min_size = 400
        width = max(screen_width // relative_size, width_min_size)
        height = max(screen_height // relative_size, calculate_size * 50)

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        target_window.geometry('%dx%d+%d+%d' % (width, height, x, y))
        target_window.update()

    def on_closing(self):
        """窗口关闭事件处理"""
        if self.tcp_client.is_connected():
            self.tcp_client.disconnect()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = TCPClientApp(root)
    root.mainloop()
