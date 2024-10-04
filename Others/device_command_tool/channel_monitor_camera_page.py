#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/10/02
# @Author  : Heshouyi
# @File    : channel_monitor_camera_page.py
# @Software: PyCharm
# @description: 通道监控相机页面，支持登录、心跳、告警、事件上报等功能，带封包处理

import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import time
import struct


class ChannelMonitorCameraPage:
    def __init__(self, root, tcp_client, app):
        self.root = root
        self.tcp_client = tcp_client
        self.app = app  # 传入主应用程序引用
        self.command = ""
        self.timer = None  # 用于定时发送心跳包的定时器线程
        self.is_reporting = tk.BooleanVar(value=False)  # 标记是否正在定时上报心跳
        self.heartbeat_interval = 10  # 心跳包间隔时间，单位为秒

        self.device_id = "CA19920123"  # 内置的 deviceID
        self.device_version = "RDD.CSA.S1A.1.0"  # 内置的 deviceVersion

    def setup(self):
        """通道监控相机页面初始化"""
        self.clear_window()
        container = tk.Frame(self.root)
        container.pack(expand=True, fill='both')

        # 创建Notebook，用于多个Tab页面
        notebook = ttk.Notebook(container)
        notebook.pack(expand=True, fill='both')

        # 告警页面
        alarm_page = ttk.Frame(notebook)
        notebook.add(alarm_page, text="相机告警")

        # 事件触发页面
        event_page = ttk.Frame(notebook)
        notebook.add(event_page, text="事件触发")

        # 设置告警类型选项卡中的内容
        self.setup_alarm_page(alarm_page)

        # 设置事件触发选项卡中的内容
        self.setup_event_page(event_page)

        # 显示当前生成的指令
        self.command_label = tk.Label(container, text="生成的指令：")
        self.command_label.pack(pady=10)

        # 底部多个按钮框架
        button_frame = tk.Frame(container)
        button_frame.pack(pady=10)

        # 确保 send_button 被初始化为类属性
        self.send_button = tk.Button(button_frame, text="发送一次当前指令", command=self.send_command,
                                     state=tk.DISABLED)
        self.send_button.grid(row=0, column=1, padx=10)

        disconnect_button = tk.Button(button_frame, text="返回设备选择界面",
                                      command=self.back2device_type_selection_page)
        disconnect_button.grid(row=0, column=2, padx=10)

        disconnect_button = tk.Button(button_frame, text="断开服务器连接", command=self.disconnect)
        disconnect_button.grid(row=0, column=3, padx=10, pady=10)

        self.report_switch = ttk.Checkbutton(button_frame, text="定时上报心跳(10s/次)", variable=self.is_reporting,
                                             command=self.heartbeat_by_time, state=tk.DISABLED)
        self.report_switch.grid(row=1, column=2, padx=10)

        # 设备登录包的初始化发送
        self.send_register_packet()

    def setup_alarm_page(self, alarm_page):
        """在告警页面设置告警选项"""
        tk.Label(alarm_page, text="选择告警类型：").pack(pady=10)
        self.alarm_type = tk.StringVar(value="videoFault")
        alarm_options = [
            ("视频故障", "videoFault"),
            ("算法未正常运行", "algNotWork"),
            ("图片编码失败", "jpgEncodeFault"),
            ("连接图片服务器失败", "ossNetFault")
        ]
        self.create_radiobuttons(alarm_page, alarm_options, self.alarm_type, self.generate_command, max_per_row=5)

    def setup_event_page(self, event_page):
        """在事件触发页面设置事件选项"""
        tk.Label(event_page, text="选择触发事件类型：").pack(pady=10)

        # 创建一个框架来容纳事件类型的 Radiobutton
        event_type_frame = tk.Frame(event_page)
        event_type_frame.pack(pady=5, fill='x')

        self.event_type = tk.StringVar(value="triggerEvent")
        event_options = [
            ("触发事件", "triggerEvent"),
            ("车辆后退事件", "reverseEvent"),
            ("车辆离开事件", "exitEvent"),
            ("交通流量事件", "trafficEvent"),
            ("滞留/违停事件", "illegalParkingEvent")
        ]

        self.create_radiobuttons(event_type_frame, event_options, self.event_type, self.generate_command, max_per_row=5)

        # 设置额外参数（如车牌号、车辆类型等）
        self.setup_event_parameters(event_page)

    def setup_event_parameters(self, event_page):
        """为事件上报设置额外的参数输入框"""

        # 车辆类型选择框
        tk.Label(event_page, text="选择车辆类型：").pack(pady=5)
        vehicle_type_frame = tk.Frame(event_page)
        vehicle_type_frame.pack(pady=5, fill='x')

        self.vehicle_type = tk.StringVar(value="小型车")
        vehicle_options = [
            ("小型车", "小型车"),
            ("大型车", "大型车"),
            ("摩托车", "摩托车"),
            ("其他", "其他")
        ]
        self.create_radiobuttons(vehicle_type_frame, vehicle_options, self.vehicle_type, self.generate_command,
                                 max_per_row=5)

        # 车牌颜色选择框
        tk.Label(event_page, text="车牌颜色：").pack(pady=5)
        plate_color_frame = tk.Frame(event_page)
        plate_color_frame.pack(pady=5, fill='x')

        self.plate_color = tk.StringVar(value="蓝色")
        plate_color_options = [
            ("蓝色", "蓝色"),
            ("黄色", "黄色"),
            ("白色", "白色"),
            ("黑色", "黑色"),
            ("绿色", "绿色")
        ]
        self.create_radiobuttons(plate_color_frame, plate_color_options, self.plate_color, self.generate_command,
                                 max_per_row=5)

        # 创建一个父框架来容纳“车牌号”和“可信度”输入框
        input_frame = tk.Frame(event_page)
        input_frame.pack(pady=5, fill='x')

        # 车牌号输入
        plate_label = tk.Label(input_frame, text="车牌号：")
        plate_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')  # 右对齐
        self.plate_entry = tk.Entry(input_frame)
        self.plate_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')  # 左对齐
        self.plate_entry.bind("<KeyRelease>", self.generate_command)

        # 可信度输入
        confidence_label = tk.Label(input_frame, text="可信度(1-100)：")
        confidence_label.grid(row=0, column=2, padx=5, pady=5, sticky='e')  # 右对齐
        self.confidence_entry = tk.Entry(input_frame)
        self.confidence_entry.grid(row=0, column=3, padx=5, pady=5, sticky='w')  # 左对齐
        self.confidence_entry.bind("<KeyRelease>", self.generate_command)

        # 可选：调整列权重以使输入框扩展
        input_frame.grid_columnconfigure(1, weight=1)
        input_frame.grid_columnconfigure(3, weight=1)

    @staticmethod
    def create_radiobuttons(parent, options, variable, command, max_per_row=3):
        """
        创建横向排列的 Radiobutton，每行最多 max_per_row 个，并居中对齐
        :param parent: 父容器
        :param options: 选项列表，列表中的每个元素是 (显示文本, 值)
        :param variable: 关联的 Tkinter 变量
        :param command: 选中时调用的命令
        :param max_per_row: 每行最大 Radiobutton 数量
        """
        frame = tk.Frame(parent)
        frame.pack(anchor=tk.CENTER)  # 将 Radiobutton 框架居中

        # 创建 Radiobuttons 并排列
        row = 0
        col = 0
        for idx, (text, value) in enumerate(options):
            rb = tk.Radiobutton(frame, text=text, variable=variable, value=value, command=command)
            rb.grid(row=row, column=col, padx=10, pady=5)
            col += 1
            if col >= max_per_row:
                col = 0
                row += 1

        # 让 Radiobutton 框架的列权重相同，以便居中显示
        for c in range(max_per_row):
            frame.grid_columnconfigure(c, weight=1)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def generate_command(self, event=None):
        """根据选项生成告警或事件的指令"""
        try:
            camera_id_num = int(self.device_id)

            # 判断当前选中的标签页
            current_tab = self.get_current_tab()
            if current_tab == "事件触发":
                # 获取事件相关参数
                plate = self.plate_entry.get().strip()
                vehicle_type = self.vehicle_type.get()
                confidence = self.confidence_entry.get().strip()
                plate_color = self.plate_color.get()

                # 构造事件命令
                self.command = f"(ID:{camera_id_num}, EVENT:{self.event_type.get()}, PLATE:{plate}, " \
                               f"TYPE:{vehicle_type}, CONF:{confidence}, COLOR:{plate_color})"
            else:
                # 告警命令
                alarm_msg = self.alarm_type.get()
                self.command = f"(ID:{camera_id_num}, ALARM:{alarm_msg})"

            self.send_button.config(state=tk.NORMAL)
            self.report_switch.config(state=tk.NORMAL)
        except ValueError:
            self.command = "请输入有效的相机ID"
            self.send_button.config(state=tk.DISABLED)
            self.report_switch.config(state=tk.DISABLED)

        self.command_label.config(text=f"生成的指令：{self.command}")

    def get_current_tab(self):
        """获取当前选中的标签页名称"""
        notebook = self.root.nametowidget(self.root.winfo_children()[0].winfo_children()[0])
        selected_tab = notebook.tab(notebook.select(), "text")
        return selected_tab

    def send_register_packet(self):
        """发送设备注册包"""
        camera_id = self.device_id  # 使用内置的 device_id
        device_version = self.device_version  # 使用内置的 device_version
        cmd_time = int(time.time())  # 获取当前时间戳

        if camera_id:
            # 构造符合协议的登录包，保持字段不变
            register_packet = {
                "cmd": "cameraLogin",
                "cmdTime": str(cmd_time),
                "deviceType": "5",
                "deviceId": camera_id,
                "deviceVersion": device_version
            }
            # 将数据封装成二进制包发送
            self.tcp_client.send_command(self.create_packet(register_packet))
            self.root.after(1000, self.start_heartbeat)  # 延迟1秒后启动心跳包
        else:
            self.command_label.config(text="无法获取设备ID，无法发送注册包")

    def start_heartbeat(self):
        """开始定时发送心跳包"""
        if not self.is_reporting.get():  # 如果没有手动启动心跳定时器，则启动它
            self.is_reporting.set(True)
            self.heartbeat_by_time()

    def on_camera_id_entry_change(self, event):
        """当相机ID输入框内容改变时触发的动作"""
        self.generate_command()

    def send_command(self):
        """发送生成的指令到服务器"""
        # 调用封包函数
        packet = self.create_packet(self.command)
        # 通过TCP客户端发送封装后的数据包
        self.tcp_client.send_command(packet)

    def disconnect(self):
        """断开连接并返回初始界面"""
        self.stop_heartbeat()  # 停止心跳包的定时器
        self.tcp_client.disconnect()  # 断开与服务器的连接
        self.app.create_connection_page()  # 返回初始连接界面
        self.app.root.title("TCP设备指令模拟工具")  # 清除标题中的服务器连接信息

    def back2device_type_selection_page(self):
        """返回设备类型选择界面"""
        self.app.create_device_type_selection_page()

    def heartbeat_by_time(self):
        """启动或停止定时上报心跳"""
        if self.is_reporting.get():
            self.schedule_next_heartbeat()
        else:
            self.stop_heartbeat()

    def stop_heartbeat(self):
        """停止心跳包的定时器"""
        if self.timer:
            self.timer.cancel()
            self.timer = None

    def schedule_next_heartbeat(self):
        """定时发送下一次心跳包"""
        if self.is_reporting.get():
            camera_id = self.device_id  # 使用内置的 device_id
            cmd_time = int(time.time())  # 当前时间戳
            area_state = 0  # 默认区域状态为正常

            # 构造符合协议的JSON格式心跳包
            heartbeat_packet = {
                "cmd": "heartbeat",
                "cmdTime": str(cmd_time),
                "deviceId": camera_id,
                "deviceType": "5",
                "areaState": str(area_state)
            }

            # 将字典转换为字符串并封装成二进制包发送
            self.tcp_client.send_command(self.create_packet(heartbeat_packet))

            # 每次间隔10秒发送心跳包
            self.timer = threading.Timer(self.heartbeat_interval, self.schedule_next_heartbeat)
            self.timer.daemon = True
            self.timer.start()

    def create_packet(self, command_data):
        """
        根据协议要求封装指令数据
        :param command_data: 需要封包的命令数据字典
        :return: 封装后的二进制数据
        """
        # 协议头和尾
        protocol_head = 0xfb
        protocol_tail = 0xfe
        timestamp = int(time.time())  # 当前时间戳，4字节
        command_code = 0x01  # 可以根据不同指令自定义
        total_packets = 1
        packet_number = 0

        # 初始化数据部分为空
        data_bytes = b''

        # 动态处理 command_data 中的每个键值对，拼接为二进制数据
        for key, value in command_data.items():
            if isinstance(value, str):
                # 如果是字符串，转为 UTF-8 编码后的字节
                data_bytes += value.encode('utf-8')
            elif isinstance(value, int):
                # 如果是整数，按4字节大端格式存储
                data_bytes += struct.pack('>I', value)
            else:
                # 其他类型暂时作为字符串处理
                data_bytes += str(value).encode('utf-8')

        # 协议部分
        protocol_head = 0xfb  # 协议头
        protocol_tail = 0xfe  # 协议尾
        timestamp = int(time.time())  # 当前时间戳，4字节
        command_code = 0x01  # 具体命令码
        total_packets = 1  # 总包数，假设不分包
        packet_number = 0  # 包序号
        data_length = len(data_bytes)  # 数据长度

        # 计算校验和，累加时间戳、命令码、包序号等内容
        checksum_data = struct.pack('>I', timestamp) + struct.pack('>B', command_code) + \
                        struct.pack('>H', total_packets) + struct.pack('>H', packet_number) + \
                        struct.pack('>H', data_length) + data_bytes
        checksum = sum(checksum_data) & 0xFFFF  # 取16位

        # 组装完整包
        packet = struct.pack('>B', protocol_head) + struct.pack('>I', timestamp) + \
                 struct.pack('>B', command_code) + struct.pack('>H', total_packets) + \
                 struct.pack('>H', packet_number) + struct.pack('>H', data_length) + \
                 data_bytes + struct.pack('>H', checksum) + struct.pack('>B', protocol_tail)

        # 对特殊字符进行转义
        packet = self.escape_packet(packet)

        return packet

    @staticmethod
    def escape_packet(packet):
        """
        根据协议要求对0xFB、0xFE和0xFF进行转义，但不包括协议头和协议尾
        :param packet: 原始封包数据
        :return: 转义后的数据
        """
        # 协议头是第一个字节，协议尾是最后一个字节
        protocol_head = packet[0:1]
        protocol_tail = packet[-1:]
        # 中间部分是需要转义的数据
        data_to_escape = packet[1:-1]

        # 进行转义处理
        escaped_data = data_to_escape.replace(b'\xfb', b'\xff\xbb') \
            .replace(b'\xfe', b'\xff\xee') \
            .replace(b'\xff', b'\xff\xfc')

        # 返回完整的封包，包括未转义的头和尾
        return protocol_head + escaped_data + protocol_tail
