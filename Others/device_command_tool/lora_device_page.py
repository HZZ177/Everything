#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/30 17:47
# @Author  : Heshouyi
# @File    : lora_device_page.py.py
# @Software: PyCharm
# @description:
import tkinter as tk
from tkinter import messagebox

class LoraDevicePage:
    def __init__(self, root, tcp_client, app):
        self.root = root
        self.tcp_client = tcp_client
        self.app = app  # 传入主应用程序引用
        self.command = ""
        self.faults = {}

    def setup(self):
        """Lora节点页面的布局"""
        self.clear_window()
        container = tk.Frame(self.root)
        container.pack(expand=True)

        # 创建车位状态选择框架
        tk.Label(container, text="选择车位状态：").pack(pady=10)
        car_status_frame = tk.Frame(container)
        car_status_frame.pack(pady=10)

        self.car_status = tk.StringVar(value="有车正常")
        car_status_options = [("有车正常", 0, 0), ("有车故障", 0, 1), ("无车正常", 1, 0), ("无车故障", 1, 1)]
        for option, row, col in car_status_options:
            tk.Radiobutton(car_status_frame, text=option, variable=self.car_status, value=option,
                           command=lambda: [self.update_fault_status(), self.generate_command()]).grid(row=row, column=col, padx=20, pady=5)

        # 创建故障状态选择框架
        tk.Label(container, text="选择故障状态（可多选）：").pack(pady=10)
        self.fault_status_frame = tk.Frame(container)
        self.fault_status_frame.pack(pady=10)

        fault_options = [
            ("传感器故障", 0, 0), ("传感器满偏", 0, 1),
            ("雷达故障", 0, 2), ("高低温预警", 0, 3),
            ("RTC故障", 1, 0), ("通讯故障", 1, 1),
            ("电池低压预警", 1, 2)
        ]
        self.faults = {}
        self.fault_checkbuttons = {}
        for option, row, col in fault_options:
            var = tk.IntVar()
            self.faults[option] = var
            checkbutton = tk.Checkbutton(self.fault_status_frame, text=option, variable=var, command=self.generate_command)
            checkbutton.grid(row=row, column=col, padx=10, pady=5)
            self.fault_checkbuttons[option] = checkbutton

        # 显示生成的指令
        self.command_label = tk.Label(container, text="生成的指令：")
        self.command_label.pack(pady=10)

        # 底部按钮框架
        button_frame = tk.Frame(container)
        button_frame.pack(pady=10)

        send_button = tk.Button(button_frame, text="发送指令", command=self.send_command)
        send_button.grid(row=0, column=1, padx=10)

        disconnect_button = tk.Button(button_frame, text="断开连接", command=self.disconnect)
        disconnect_button.grid(row=0, column=2, padx=10)

        self.update_fault_status()  # 初始化时更新故障状态框的状态
        self.generate_command()  # 页面加载后生成初始指令

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def update_fault_status(self):
        """根据车位状态启用或禁用故障状态，并清除选择"""
        selected_status = self.car_status.get()

        if selected_status in ["有车正常", "无车正常"]:
            # 禁用所有故障状态复选框，并清除选中状态
            for checkbutton in self.fault_checkbuttons.values():
                checkbutton.config(state=tk.DISABLED)
                self.faults[checkbutton.cget('text')].set(0)  # 清除选中状态
        else:
            # 启用所有故障状态复选框
            for checkbutton in self.fault_checkbuttons.values():
                checkbutton.config(state=tk.NORMAL)

    def generate_command(self):
        """生成Lora节点的指令"""
        # 获取车位状态
        car_status = self.car_status.get()
        car_status_code = {
            "有车正常": "A", "有车故障": "C", "无车正常": "@", "无车故障": "B"
        }[car_status]

        # 获取故障状态
        fault_flags = {
            "传感器故障": 0x80,
            "传感器满偏": 0x40,
            "雷达故障": 0x20,
            "高低温预警": 0x10,
            "RTC故障": 0x08,
            "通讯故障": 0x04,
            "电池低压预警": 0x01
        }
        zz = 0x00
        for fault, var in self.faults.items():
            if var.get():
                zz |= fault_flags[fault]

        # 将ZZ值转换为十六进制
        zz_hex = f"{zz:02X}"

        # 使用服务器IP和探测器ID生成AAAAA部分
        node_last_octet = int(self.tcp_client.server_ip.split(".")[-1])
        aaaaa = f"{(node_last_octet << 8 | self.tcp_client.detector_id):05d}"

        # 拼装命令
        self.command = f"({aaaaa}{car_status_code}{zz_hex})"
        self.command_label.config(text=f"生成的指令：{self.command}")

    def send_command(self):
        """发送生成的指令到服务器，检测是否选择了至少一个故障"""
        car_status = self.car_status.get()

        # 如果是故障状态，检测是否选择了至少一个故障
        if car_status in ["有车故障", "无车故障"]:
            if not any(var.get() for var in self.faults.values()):
                messagebox.showwarning("警告", "请至少选择一个故障详情")
                return  # 阻止发送指令

        # 否则正常发送指令
        self.tcp_client.send_command(self.command)

    def disconnect(self):
        """断开连接并返回初始界面"""
        self.tcp_client.disconnect()  # 断开与服务器的连接
        self.app.create_connection_page()  # 返回初始连接界面
