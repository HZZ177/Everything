#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/30 17:47
# @Author  : Heshouyi
# @File    : lora_node_device_page.py
# @Software: PyCharm
# @description: lora无线节点页面

import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class LoraDevicePage:
    def __init__(self, root, tcp_client, app):

        self.address_entry = None  # 地址输入框
        self.car_status = None  # 车位状态选择框
        self.fault_status_frame = None  # 故障状态frame
        self.fault_checkbuttons = None  # 故障状态选择框
        self.command_label = None  # 显示生成的指令
        self.send_button = None  # 发送一次指令按钮
        self.report_switch = None  # 定时上报开关

        self.root = root
        self.tcp_client = tcp_client
        self.app = app  # 传入主应用程序引用
        self.command = ""
        self.faults = {}
        self.timer = None  # 用于定时发送指令的定时器线程
        self.is_reporting = tk.BooleanVar(value=False)  # 标记是否正在定时上报

    def setup(self):
        """Lora节点页面初始化"""
        self.clear_window()
        container = tk.Frame(self.root)
        container.pack(expand=True)

        # 添加地址输入框
        address_frame = tk.Frame(container)
        address_frame.pack(pady=10)
        tk.Label(address_frame, text="请输入探测器地址：").pack(side=tk.LEFT)
        self.address_entry = tk.Entry(address_frame)
        self.address_entry.pack(side=tk.LEFT)
        # 绑定输入框的键盘释放事件，按任意键时监控输入长度以及生成对应指令
        self.address_entry.bind("<KeyRelease>", self.on_address_entry_change)

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
        self.fault_checkbuttons = {}    # 故障选项复选框
        for option, row, col in fault_options:
            var = tk.IntVar()
            self.faults[option] = var
            # 创建一个复选框，设置显示的文本、关联的变量以及触发的命令
            checkbutton = tk.Checkbutton(self.fault_status_frame, text=option, variable=var, command=self.generate_command)
            checkbutton.grid(row=row, column=col, padx=10, pady=5)
            # 将复选框存储在字典中，以便后续可以通过选项名称直接访问
            self.fault_checkbuttons[option] = checkbutton

        # 显示当前生成的指令
        self.command_label = tk.Label(container, text="生成的指令：")
        self.command_label.pack(pady=10)

        # 底部多个按钮框架
        button_frame = tk.Frame(container)
        button_frame.pack(pady=10)

        self.send_button = tk.Button(button_frame, text="发送一次当前指令", command=self.send_command, state=tk.DISABLED)
        self.send_button.grid(row=0, column=1, padx=10)

        disconnect_button = tk.Button(button_frame, text="返回设备选择界面", command=self.back2device_type_selection_page)
        disconnect_button.grid(row=0, column=2, padx=10)

        disconnect_button = tk.Button(button_frame, text="断开服务器连接", command=self.disconnect)
        disconnect_button.grid(row=0, column=3, padx=10, pady=10)

        self.report_switch = ttk.Checkbutton(button_frame, text="定时上报开关(10s/次)", variable=self.is_reporting,
                                             command=self.report_by_time, state=tk.DISABLED)
        self.report_switch.grid(row=1, column=2, padx=10)

        self.update_fault_status()  # 初始化时更新故障状态框的状态
        self.generate_command()  # 页面加载后生成初始指令

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def update_fault_status(self):
        """根据车位状态启用或禁用故障状态，并清除选择"""
        selected_status = self.car_status.get()

        if selected_status in ["有车正常", "无车正常"]:
            # 如果选择的是正常的两个状态，禁用所有故障状态复选框，并清除选中状态
            for checkbutton in self.fault_checkbuttons.values():
                checkbutton.config(state=tk.DISABLED)
                self.faults[checkbutton.cget('text')].set(0)  # 清除选中状态
        else:
            # 反之启用所有故障状态复选框
            for checkbutton in self.fault_checkbuttons.values():
                checkbutton.config(state=tk.NORMAL)

    def generate_command(self):
        """
        根据页面选择组合，生成Lora节点上报的指令
        1、获取车位状态并映射为单个字符代码
        2、获取多种故障状态标志，根据当前故障情况组合成一个字节值，并转换为十六进制形式
            a.根据协议定义字典fault_flags，标记每个故障类型对应的一个二进制标志位
            b.组合标志位：遍历faults字典，如果某项为真(即被选中)，则取对应故障的标志位和zz进行按位或运算 (|)，最终得到新的故障状态字节值zz
            c.转换为十六进制：将最终转换出的ZZ值转换为两个字符长度的十六进制字符串zz_hex
        3、获取探测器地址，若为空或无效，则禁用发送按钮和报告开关，并提示输入有效地址；否则，根据地址和获取的状态信息构造命令字符串
        4、最终将构造好的命令存储并显示在界面上
        :return:
        """
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
        # 遍历faults字典，如果某项为真(即被选中)，则取对应故障的标志位和zz进行按位或运算 (|)，最终得到新的故障状态字节值zz
        for fault, var in self.faults.items():
            if var.get():
                zz |= fault_flags[fault]

        # 将最终转换出的ZZ值转换为十六进制
        zz_hex = f"{zz:02X}"

        # 获取探测器地址
        address = self.address_entry.get().strip()
        if not address:
            self.command = "请输入探测器地址"
            self.send_button.config(state=tk.DISABLED)
            self.report_switch.config(state=tk.DISABLED)
        else:
            try:
                detector_id = int(address)
                node_last_octet = int(self.tcp_client.server_ip.split(".")[-1])
                aaaaa = f"{(node_last_octet << 8 | detector_id):05d}"
                # 拼装命令
                self.command = f"({aaaaa}{car_status_code}{zz_hex})"
                self.send_button.config(state=tk.NORMAL)
                self.report_switch.config(state=tk.NORMAL)
            except ValueError:
                self.command = "请输入有效的探测器地址"
                self.send_button.config(state=tk.DISABLED)
                self.report_switch.config(state=tk.DISABLED)

        self.command_label.config(text=f"生成的指令：{self.command}")

    def on_address_entry_change(self, event):
        """当地址输入框内容改变时触发的动作"""
        # 获取当前输入框内容
        current_text = self.address_entry.get()

        # 检查内容是否为数字且长度不超过3
        if not current_text.isdigit() or len(current_text) > 3:
            # 如果内容不符合条件，则移除最后一个字符
            self.address_entry.delete(len(current_text) - 1, tk.END)

        self.generate_command()

    def send_command(self):
        """检测是否选择了至少一个故障，如果满足，发送生成的指令到服务器"""
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
        self.app.root.title("TCP设备指令模拟工具")  # 清除标题中的服务器连接信息

    def back2device_type_selection_page(self):
        """返回设备类型选择界面"""
        self.app.create_device_type_selection_page()

    def report_by_time(self):
        """启动或停止定时上报"""
        if self.is_reporting.get():
            self.start_reporting()
        else:
            self.stop_reporting()

    def start_reporting(self):
        """开始定时上报"""
        self.schedule_next_report()

    def stop_reporting(self):
        """停止定时上报"""
        if self.timer:
            self.timer.cancel()
            self.timer = None

    def schedule_next_report(self):
        """计时上报下一次指令"""
        if self.is_reporting.get():
            self.generate_command()
            self.send_command()
            # 通过基于线程的定时器实现，每隔10s发送一次指令
            self.timer = threading.Timer(10, self.schedule_next_report)
            self.timer.daemon = True  # 将计时器线程设置为守护线程
            self.timer.start()
