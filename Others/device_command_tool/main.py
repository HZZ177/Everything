# main.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/30 17:46
# @Author  : Heshouyi
# @File    : main.py
# @Software: PyCharm
# @description:

import tkinter as tk
from tkinter import messagebox
from tcp_client import TCPClient
from lora_node_device_page import LoraDevicePage
from other_device_page import OtherDevicePage
from channel_monitor_camera_page import ChannelMonitorCameraPage


class TCPClientApp:
    def __init__(self, root: tk.Tk):
        self.server_ip_entry = None  # 服务器IP地址输入框
        self.server_port_entry = None  # 服务器端口输入框
        self.connect_button = None  # 连接服务器按钮
        self.selected_device_type = None    # 选择的设备类型

        self.root = root
        self.center_window(self.root, relative_size=3, calculate_size=10)
        self.app_name = "TCP设备指令模拟工具"
        self.root.title(self.app_name)
        self.tcp_client = TCPClient(self)  # 创建TCP客户端实例

        # 绑定窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # 初始化起始界面布局
        self.create_connection_page()

        # 定义设备类型到处理函数的映射
        self.device_type_handlers = {
            "Lora节点": self.load_lora_device_page,
            "通道监控相机": self.load_channel_monitor_camera_page,
            "其他设备类型": self.load_other_device_page
        }

    def create_connection_page(self):
        """创建服务器连接界面"""
        self.clear_window()

        container = tk.Frame(self.root)
        container.pack(expand=True)

        tk.Label(container, text="服务器IP:").pack(pady=10)
        self.server_ip_entry = tk.Entry(container)
        self.server_ip_entry.pack(pady=5)

        tk.Label(container, text="服务器端口:").pack(pady=10)
        self.server_port_entry = tk.Entry(container)
        self.server_port_entry.pack(pady=5)

        self.connect_button = tk.Button(container, text="连接服务器", command=self.connect_to_server)
        self.connect_button.pack(pady=20)

        # 绑定回车按键到输入框(只能绑定到有焦点的部件上才能监控按键事件)，触发连接功能
        self.server_ip_entry.bind('<Return>', self.connect_to_server)
        self.server_port_entry.bind('<Return>', self.connect_to_server)

        self.server_ip_entry.focus()

    def connect_to_server(self, event=None):
        """尝试连接到服务器"""
        server_ip = self.server_ip_entry.get().strip()
        server_port = self.server_port_entry.get().strip()

        # 调用 TCPClient 的 connect_to_server 方法
        success = self.tcp_client.connect_to_server(server_ip, server_port, event)

        if success:
            # 如果成功连接到服务器，更新窗口标题栏以显示当前IP地址
            self.root.title(f"{self.app_name} - 当前连接服务器：{server_ip}")

            # 跳转到设备类型选择页面
            self.create_device_type_selection_page()
        else:
            # 连接失败后，重新启用按钮并恢复按钮文本
            self.connect_button.config(state=tk.NORMAL)
            self.connect_button.config(text="连接服务器")

    def create_device_type_selection_page(self):
        """创建设备类型选择页面"""
        self.clear_window()

        container = tk.Frame(self.root)
        container.pack(expand=True)

        tk.Label(container, text="请选择设备类型:").pack(pady=10)

        # 从字典的键生成设备类型列表
        device_types = list(self.device_type_handlers.keys())
        self.selected_device_type = tk.StringVar(value=device_types[0])    # 默认初始选择为第一个设备类型

        # 使用 OptionMenu 创建下拉菜单
        device_type_menu = tk.OptionMenu(container, self.selected_device_type, *device_types)
        device_type_menu.pack(pady=10)

        confirm_button = tk.Button(container, text="确认选择", command=self.on_device_type_selected)
        confirm_button.pack(pady=20)

    def on_device_type_selected(self):
        """根据选择的设备类型加载对应的设备页面"""
        selected_type = self.selected_device_type.get()
        handler = self.device_type_handlers.get(selected_type)

        if handler:
            handler()
        else:
            messagebox.showerror("错误", f"未知的设备类型: {selected_type}")

    def load_lora_device_page(self):
        """加载Lora设备页面"""
        lora_page = LoraDevicePage(self.root, self.tcp_client, self)
        lora_page.setup()

    def load_channel_monitor_camera_page(self):
        """加载通道监控相机设备页面"""
        channel_camera_page = ChannelMonitorCameraPage(self.root, self.tcp_client, self)
        channel_camera_page.setup()

    def load_other_device_page(self):
        """加载其他设备页面"""
        other_page = OtherDevicePage(self.root, self.tcp_client, self)
        other_page.setup()

    def clear_window(self):
        """清除窗口中的所有组件"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def center_window(self, target_window: tk.Tk, relative_size=4, calculate_size=0):
        """窗口居中"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        width_min_size = 400
        width = max(screen_width // relative_size, width_min_size)
        height = max(screen_height // relative_size, calculate_size * 50)

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        target_window.geometry(f'{width}x{height}+{x}+{y}')
        target_window.update()

    def on_closing(self):
        """程序窗口关闭事件处理"""
        if self.tcp_client.is_connected():
            self.tcp_client.disconnect()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = TCPClientApp(root)
    root.mainloop()
