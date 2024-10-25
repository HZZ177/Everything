import json
import time
import struct
import queue
import threading
import tkinter as tk
from tkinter import messagebox, ttk
from server_function import ServerFunctions


class TcpLedScreenPage:
    def __init__(self, root, tcp_client, app):
        # UI组件
        self.command_display = None
        self.command_label = None
        self.send_button = None
        self.report_switch = None
        self.root = root
        self.tcp_client = tcp_client
        self.app = app
        self.timer = None
        self.is_reporting = tk.BooleanVar(value=False)
        self.heartbeat_interval = 5  # 心跳间隔5秒

        self.device_type = 0x0C  # DSP类别（网络版LED屏）
        self.device_version = 0x0400  # 设备版本号

        # 实例化服务器功能类
        self.ServerFunctions = ServerFunctions(self.tcp_client.server_ip)

        # 创建队列用于线程通信
        self.result_queue = queue.Queue()
        self.root.after(100, self.process_queue)  # 定时检查队列中的消息

        # 添加用于显示服务器指令的队列
        self.command_queue = queue.Queue()
        self.root.after(100, self.process_command_queue)  # 定时检查服务器指令的队列

    def setup(self):
        """设置页面的UI布局"""
        self.clear_window()
        container = tk.Frame(self.root)
        container.pack(expand=True, fill='both')

        # 显示服务器下发指令的文本框
        # 提示文字
        tk.Label(container, text="接收到的服务器下发的数据：").pack(padx=10, pady=5)
        self.command_display = tk.Text(container, height=10, wrap='word', state='disabled')
        self.command_display.pack(padx=50, pady=10)

        # 创建发送、返回等按钮
        buttons_frame = tk.Frame(container)
        buttons_frame.pack(pady=20)

        # 发送注册包按钮
        self.send_button = tk.Button(buttons_frame, text="发送注册包", command=self.send_register_packet)
        self.send_button.grid(row=0, column=0, padx=10)

        # 返回设备选择界面按钮
        back_button = tk.Button(buttons_frame, text="返回设备选择界面", command=self.back_to_device_selection)
        back_button.grid(row=0, column=1, padx=10)

        # 断开服务器连接按钮
        disconnect_button = tk.Button(buttons_frame, text="断开服务器连接", command=self.disconnect)
        disconnect_button.grid(row=0, column=2, padx=10)

        # 定时心跳开关
        self.report_switch = ttk.Checkbutton(container, text="定时心跳(5s/次)", variable=self.is_reporting,
                                             command=self.heartbeat_by_time)
        self.report_switch.pack(pady=10)

        # 刷新服务器设备状态的便捷按钮框架
        additional_button_frame = tk.Frame(container)
        additional_button_frame.pack(pady=10)

        # 提示文字
        tk.Label(additional_button_frame, text="-------服务器快捷功能|-_-|-------").grid(row=0, column=0, columnspan=2, padx=10, pady=5)

        # 刷新在线设备按钮
        get_online_devices_button = tk.Button(
            additional_button_frame,
            text="findCar刷新在线设备",
            command=self.get_all_online_devices
        )
        get_online_devices_button.grid(row=1, column=0, padx=10, pady=5)

        # 刷新设备状态按钮
        device_status_test_button = tk.Button(
            additional_button_frame,
            text="channel刷新在线设备",
            command=self.device_status_test
        )
        device_status_test_button.grid(row=1, column=1, padx=10, pady=5)

        # 初始化设备注册
        self.send_register_packet()

        # 启用接收服务器指令的回调函数，开始打印服务器下发的信息
        time.sleep(0.1)     # 睡一觉，以免打印返回的注册包信息
        self.tcp_client.set_receive_callback(self.display_server_command)

    def display_server_command(self, command):
        """在文本框中显示服务器下发的指令"""
        self.command_display.config(state='normal')
        print(f"收到{command}")
        # 排除服务器返回的心跳包打印
        if "'data_content': b''," not in str(command):
            self.command_display.insert(tk.END, f"接收到服务器下发数据：{command}\n\n")
        self.command_display.config(state='disabled')
        self.command_display.see(tk.END)  # 滚动到底部

    def process_command_queue(self):
        """处理服务器指令的队列，并在界面上显示"""
        try:
            while True:
                command = self.command_queue.get_nowait()
                self.display_server_command(command)
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.process_command_queue)  # 继续检查队列

    def send_register_packet(self):
        """发送设备注册包，仅包含DSP类别和版本"""
        timestamp = int(time.time())
        register_data = struct.pack(">B H", self.device_type, self.device_version)  # DSP类别和版本
        packet = self.create_packet(register_data, command_code='C')
        self.tcp_client.send_command(packet)
        self.root.after(1000, self.start_heartbeat)  # 延迟1秒后启动心跳包

    def start_heartbeat(self):
        """进入页面时自动开启定时发送心跳包"""
        if not self.is_reporting.get():  # 如果没有手动启动心跳定时器，则启动它
            self.is_reporting.set(True)
            self.heartbeat_by_time()

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
        """定时发送心跳包"""
        if self.is_reporting.get():
            heartbeat_packet = self.create_packet(b"", command_code='F')
            self.tcp_client.send_command(heartbeat_packet)
            self.timer = threading.Timer(self.heartbeat_interval, self.schedule_next_heartbeat)
            self.timer.start()

    def create_packet(self, data_content, command_code):
        """封装指令数据"""
        protocol_head = 0xfb
        protocol_tail = 0xfe
        timestamp = int(time.time())
        command_code_ascii = ord(command_code)
        total_packets = 1
        packet_number = 0
        data_length = len(data_content)

        # 计算校验码
        checksum = self.calculate_checksum(timestamp, command_code_ascii, total_packets, packet_number, data_length, data_content)

        # 封装包
        packet = (
            struct.pack('>B', protocol_head) +
            struct.pack('>I', timestamp) +
            struct.pack('>B', command_code_ascii) +
            struct.pack('>H', total_packets) +
            struct.pack('>H', packet_number) +
            struct.pack('>H', data_length) +
            data_content +
            struct.pack('>H', checksum) +
            struct.pack('>B', protocol_tail)
        )
        return self.escape_packet(packet)

    @staticmethod
    def calculate_checksum(timestamp, command_code_ascii, total_packets, packet_number, data_length, data_content):
        checksum_data = (
            struct.pack('>I', timestamp) +
            struct.pack('>B', command_code_ascii) +
            struct.pack('>H', total_packets) +
            struct.pack('>H', packet_number) +
            struct.pack('>H', data_length) +
            data_content
        )
        return sum(checksum_data) & 0xFFFF

    @staticmethod
    def escape_packet(packet):
        protocol_head = packet[0:1]
        protocol_tail = packet[-1:]
        data_to_escape = packet[1:-1]

        escaped_data = data_to_escape.replace(b'\xfb', b'\xff\xbb') \
            .replace(b'\xfe', b'\xff\xee') \
            .replace(b'\xff', b'\xff\xfc')
        return protocol_head + escaped_data + protocol_tail

    def disconnect(self):
        self.stop_heartbeat()
        self.tcp_client.set_receive_callback(None)  # 断开连接时取消回调，避免一直指向被销毁的输出窗口
        self.tcp_client.disconnect()
        self.app.create_connection_page()

    def back_to_device_selection(self):
        self.stop_heartbeat()
        self.tcp_client.set_receive_callback(None)  # 断开连接时取消回调，避免一直指向被销毁的输出窗口
        self.app.create_device_type_selection_page()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def get_all_online_devices(self):
        """findCarServer获取并刷新所有在线设备信息并显示结果"""
        def task():
            try:
                data = self.ServerFunctions.get_all_online_device_info()
                message = data.get('message')
                formatted_data = json.dumps(data, ensure_ascii=False, indent=4)
                self.result_queue.put(("findCarServer刷新在线设备", f"服务器返回：{message}"))
            except Exception as e:
                self.result_queue.put(("错误", f"findCarServer刷新在线设备信息失败:\n{e}"))

        threading.Thread(target=task, daemon=True).start()

    def device_status_test(self):
        """channel刷新所有设备状态并显示结果"""
        def task():
            try:
                data = self.ServerFunctions.device_status_test()
                message = data.get('message')
                formatted_data = json.dumps(data, ensure_ascii=False, indent=4)
                self.result_queue.put(("channel刷新在线设备", f"服务器返回：{message}"))
            except Exception as e:
                self.result_queue.put(("错误", f"channel刷新设备状态失败:\n{e}"))

        threading.Thread(target=task, daemon=True).start()

    def process_queue(self):
        """处理队列中的消息，并更新GUI"""
        try:
            while True:
                title, message = self.result_queue.get_nowait()
                if title == "错误":
                    messagebox.showerror(title, message)
                else:
                    messagebox.showinfo(title, message)
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.process_queue)  # 继续检查队列
