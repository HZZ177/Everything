import json
import queue
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import struct
import time
from server_function import ServerFunctions


class ParkingCameraPage:
    def __init__(self, root, tcp_client, app):
        # 初始化变量
        self.root = root
        self.tcp_client = tcp_client
        self.app = app
        self.heartbeat_interval = 10
        self.device_type = 0x0A  # 根据协议的设备类型
        self.device_version = 0x0400  # 版本信息

        self.is_reporting = tk.BooleanVar(value=False)
        self.continuous_reporting = tk.BooleanVar(value=False)  # 持续上报开关变量
        self.report_job = None  # 用于跟踪持续上报的任务

        # 实例化服务器工具类
        self.ServerFunctions = ServerFunctions(self.tcp_client.server_ip)

        # 有车无车上报页面状态
        self.parking_statuses_parked = [tk.StringVar(value="0") for _ in range(6)]
        self.parking_selected_parked = [tk.BooleanVar(value=False) for _ in range(6)]  # 控制每个车位是否发送

        # 进车出车上报页面状态
        self.parking_statuses_move = [tk.StringVar(value="2") for _ in range(6)]
        self.parking_selected_move = [tk.BooleanVar(value=False) for _ in range(6)]  # 控制每个车位是否发送

        # 创建队列用于线程通信
        self.result_queue = queue.Queue()
        self.root.after(100, self.process_queue)  # 定时检查队列中的消息


    def setup(self):
        """设置UI界面"""

        # 清空前置页面
        self.clear_window()

        container = tk.Frame(self.root)
        container.pack(expand=True, fill='both')

        # 创建标签页
        notebook = ttk.Notebook(container)
        notebook.pack(expand=True, fill="both")

        # 创建有车无车上报页面
        parked_page = ttk.Frame(notebook)
        # 配置每列的权重，使其随窗口大小自适应分布
        for i in range(3):  # 3列布局
            parked_page.grid_columnconfigure(i, weight=1)
        notebook.add(parked_page, text="有车无车上报")

        # 创建进车出车上报页面
        move_page = ttk.Frame(notebook)
        # 配置每列的权重，使其随窗口大小自适应分布
        for i in range(3):  # 3列布局
            move_page.grid_columnconfigure(i, weight=1)
        notebook.add(move_page, text="进车出车上报")

        # 创建图片上传页面
        image_page = ttk.Frame(notebook)
        # 配置每列的权重，使其随窗口大小自适应分布
        for i in range(3):  # 3列布局
            image_page.grid_columnconfigure(i, weight=1)
        notebook.add(image_page, text="车牌更新上报")

        # 设置有车无车上报页面的内容
        self.setup_parked_page(parked_page)

        # 设置进车出车上报页面的内容
        self.setup_move_page(move_page)

        # 设置图片上传页面的内容
        self.setup_image_page(image_page)

        # 自动注册并启动心跳
        self.register_device()
        self.start_heartbeat()

    def setup_parked_page(self, container):
        """有车无车上报页面"""

        # 放置选择按钮
        selection_frame = tk.Frame(container)
        selection_frame.grid(row=0, column=1, pady=15, sticky="nsew")

        # 配置每列的权重，使其随窗口大小自适应分布
        for i in range(5):  # 5列布局
            selection_frame.grid_columnconfigure(i, weight=1)

        # 设置标题
        tk.Label(selection_frame, text="选择每个车位的状态（有车/无车）：").grid(row=0, column=0, columnspan=5, pady=15, sticky="nsew")

        # 为每个车位设置复选框和单选框
        self.parking_status_radiobuttons_parked = []
        for idx in range(6):
            # 每行创建一个车位的复选框
            check = tk.Checkbutton(selection_frame, text=f"车位 {idx + 1}", variable=self.parking_selected_parked[idx],
                                   command=lambda i=idx: self.toggle_parking_status(i, 'parked'))
            check.grid(row=idx + 1, column=0, padx=40, pady=5, sticky="nsew")  # 放在第1列

            # "无车"选项
            radio_no_car = tk.Radiobutton(selection_frame, text="无车", variable=self.parking_statuses_parked[idx], value="0",
                                          state="disabled")
            radio_no_car.grid(row=idx + 1, column=2, padx=5, sticky="nsew")  # 放在第3列

            # "有车"选项
            radio_with_car = tk.Radiobutton(selection_frame, text="有车", variable=self.parking_statuses_parked[idx],
                                            value="1", state="disabled")
            radio_with_car.grid(row=idx + 1, column=4, padx=40, sticky="nsew")  # 放在第5列

            # 将单选按钮添加到列表中
            self.parking_status_radiobuttons_parked.append((radio_no_car, radio_with_car))

        # 底部frame框架放置上报操作按钮
        operation_frame = tk.Frame(container)
        operation_frame.grid(row=1, column=1, pady=15, sticky="nsew")

        # 配置每列的权重，使其随窗口大小自适应分布
        for i in range(3):  # 3列布局
            operation_frame.grid_columnconfigure(i, weight=1)

        # 在下段frame设置“持续上报”复选框和“上报一次”按钮
        tk.Checkbutton(operation_frame, text="车位状态持续上报开关", variable=self.continuous_reporting,
                       command=self.toggle_continuous_reporting).grid(row=0, column=1, padx=5, pady=10, sticky="nsew")
        tk.Button(operation_frame, text="上报一次当前车位状态", command=self.report_parking_status_once).grid(row=1, column=1, padx=5, pady=10, sticky="nsew")

        # 刷新服务器设备状态的便捷按钮框架
        additional_button_frame = tk.Frame(container)
        additional_button_frame.grid(row=2, column=1, pady=15, sticky="nsew")

        # 配置每列的权重，使其随窗口大小自适应分布
        for i in range(3):  # 3列布局
            additional_button_frame.grid_columnconfigure(i, weight=1)

        # 提示文字
        tk.Label(additional_button_frame, text="-------服务器快捷功能|-_-|-------").grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

        get_online_devices_button = tk.Button(
            additional_button_frame,
            text="findCar刷新在线设备",
            command=self.get_all_online_devices
        )
        get_online_devices_button.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        device_status_test_button = tk.Button(
            additional_button_frame,
            text="channel刷新在线设备",
            command=self.device_status_test
        )
        device_status_test_button.grid(row=1, column=2, padx=10, pady=5, sticky="nsew")

    def toggle_continuous_reporting(self):
        """切换持续上报状态"""
        if self.continuous_reporting.get():
            self.report_parking_status_once()  # 立即开始上报
        else:
            if self.report_job:
                self.root.after_cancel(self.report_job)
                self.report_job = None

    def setup_move_page(self, container):
        """进车出车上报页面"""

        # 放置选择按钮
        selection_frame = tk.Frame(container)
        selection_frame.grid(row=0, column=1, pady=15, sticky="nsew")

        # 配置每列的权重，使其随窗口大小自适应分布
        for i in range(5):  # 5列布局
            selection_frame.grid_columnconfigure(i, weight=1)

        # 设置标题
        tk.Label(selection_frame, text="选择每个车位要上报的事件（进车/出车）：").grid(row=0, column=0, columnspan=5, pady=15, sticky="nsew")

        # 为每个车位设置复选框和单选框
        self.parking_status_radiobuttons_move = []
        for idx in range(6):
            # 车位选择框放在第1列
            check = tk.Checkbutton(selection_frame, text=f"车位 {idx + 1}", variable=self.parking_selected_move[idx],
                                   command=lambda i=idx: self.toggle_parking_status(i, 'move'))
            check.grid(row=idx + 1, column=0, padx=40, pady=5, sticky="nsew")

            # "出车"单选框放在第3列
            radio_out = tk.Radiobutton(selection_frame, text="出车", variable=self.parking_statuses_move[idx], value="2",
                                       state="disabled")
            radio_out.grid(row=idx + 1, column=2, padx=5, sticky="nsew")

            # "进车"单选框放在第5列
            radio_in = tk.Radiobutton(selection_frame, text="进车", variable=self.parking_statuses_move[idx], value="3",
                                      state="disabled")
            radio_in.grid(row=idx + 1, column=4, padx=40, sticky="nsew")

            # 将当前车位的单选按钮添加到列表
            self.parking_status_radiobuttons_move.append((radio_out, radio_in))

        # 底部frame框架放置上报操作按钮
        operation_frame = tk.Frame(container)
        operation_frame.grid(row=1, column=1, pady=15, sticky="nsew")

        # 配置三列布局，使得中间列居中显示控件
        for i in range(3):  # 3列布局
            operation_frame.grid_columnconfigure(i, weight=1)

        # 上报一次按钮放在第底部框架中间
        tk.Button(operation_frame, text="上报进出车事件", command=self.report_move_status_once).grid(row=0, column=1, pady=10, sticky="nsew")

        # 刷新服务器设备状态的便捷按钮框架
        additional_button_frame = tk.Frame(container)
        additional_button_frame.grid(row=2, column=1, pady=15, sticky="nsew")

        # 配置三列布局，使得中间列居中显示控件
        for i in range(3):  # 3列布局
            additional_button_frame.grid_columnconfigure(i, weight=1)

        # 提示文字
        tk.Label(additional_button_frame, text="-------服务器快捷功能|-_-|-------").grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

        get_online_devices_button = tk.Button(
            additional_button_frame,
            text="findCar刷新在线设备",
            command=self.get_all_online_devices
        )
        get_online_devices_button.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        device_status_test_button = tk.Button(
            additional_button_frame,
            text="channel刷新在线设备",
            command=self.device_status_test
        )
        device_status_test_button.grid(row=1, column=2, padx=10, pady=5, sticky="nsew")

    def setup_image_page(self, container):
        """图片上传页面"""

        # 车牌号输入框架
        plate_frame = tk.Frame(container)
        plate_frame.grid(row=0, column=1, pady=15, sticky="nsew")

        # 配置每列的权重，使其随窗口大小自适应分布
        for i in range(3):  # 3列布局
            plate_frame.grid_columnconfigure(i, weight=1)

        # 车牌号标签放在第1列，输入框放在第2列
        tk.Label(plate_frame, text="车牌号：").grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.plate_number = tk.Entry(plate_frame)
        self.plate_number.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        # 车牌颜色选择框架
        plate_color_frame = tk.Frame(container)
        plate_color_frame.grid(row=1, column=1, pady=15, sticky="nsew")

        # 配置每列的权重，使其随窗口大小自适应分布
        for i in range(5):  # 5列布局
            plate_color_frame.grid_columnconfigure(i, weight=1)

            # 车牌颜色标签放在第1列，颜色选项按每行三个分布在第2至第4列
            tk.Label(plate_color_frame, text="车牌颜色：").grid(row=2, column=2, sticky="nsew", padx=5, pady=5)
            self.plate_color = tk.StringVar(value="蓝色")
            color_options = ["蓝色", "绿色", "黄色", "白色", "黑色"]

            # 将颜色选项按每行三个进行分布
            for idx, color in enumerate(color_options):
                row = 3 + idx // 3  # 从第3行开始，每三项换一行
                col = (idx % 3) + 1  # 每项在第2，3，4列分布
                tk.Radiobutton(plate_color_frame, text=color, variable=self.plate_color, value=color).grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

        # 底部frame框架放置上报操作按钮
        operation_frame = tk.Frame(container)
        operation_frame.grid(row=2, column=1, pady=15, sticky="nsew")

        # 上传图片按钮放在最后一行并居中
        tk.Button(operation_frame, text="上报车牌更新", command=self.upload_image).grid(row=1, column=1, pady=40, sticky="nsew")

        # 刷新服务器设备状态的便捷按钮框架
        additional_button_frame = tk.Frame(container)
        additional_button_frame.grid(row=2, column=1, pady=15, sticky="nsew")

        # 配置三列布局，使得中间列居中显示控件
        for i in range(3):  # 3列布局
            additional_button_frame.grid_columnconfigure(i, weight=1)

        # 提示文字
        tk.Label(additional_button_frame, text="-------服务器快捷功能|-_-|-------").grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

        get_online_devices_button = tk.Button(
            additional_button_frame,
            text="findCar刷新在线设备",
            command=self.get_all_online_devices
        )
        get_online_devices_button.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        device_status_test_button = tk.Button(
            additional_button_frame,
            text="channel刷新在线设备",
            command=self.device_status_test
        )
        device_status_test_button.grid(row=1, column=2, padx=10, pady=5, sticky="nsew")

    def report_parking_status_once(self):
        """上报一次有车无车状态"""
        self.send_parking_status(self.parking_selected_parked, self.parking_statuses_parked)
        if self.continuous_reporting.get():
            self.report_job = self.root.after(10000, self.report_parking_status_once)  # 每10秒上报一次

    def report_move_status_once(self):
        """上报一次进车出车状态"""
        self.send_parking_status(self.parking_selected_move, self.parking_statuses_move)

    def toggle_parking_status(self, index, page_type):
        """启用或禁用特定车位的状态选择框"""
        if page_type == 'parked':
            radios = self.parking_status_radiobuttons_parked[index]
            state = "normal" if self.parking_selected_parked[index].get() else "disabled"
        elif page_type == 'move':
            radios = self.parking_status_radiobuttons_move[index]
            state = "normal" if self.parking_selected_move[index].get() else "disabled"

        for radio in radios:
            radio.config(state=state)

    def send_parking_status(self, selected_status, status_values):
        """根据勾选情况发送车位状态"""
        timestamp = int(time.time())
        command_code = ord('S')

        parking_status_data = b''
        for idx, selected in enumerate(selected_status):
            if selected.get():
                status = int(status_values[idx].get())
                parking_status_data += struct.pack(">H", status)
            else:
                parking_status_data += struct.pack(">H", 4)

        packet = self.create_packet(parking_status_data, command_code, timestamp)
        self.tcp_client.send_command(packet)
        print("车位状态包已发送: [状态]",
              [status.get() for idx, status in enumerate(status_values) if selected_status[idx].get()])

    def upload_image(self):
        """上传图片采集信息"""
        timestamp = int(time.time())
        command_code = ord('J')

        # 假设 plate_color 和 plate_number 为协议要求的格式
        plate_color = {"蓝色": 0, "绿色": 1, "黄色": 2, "白色": 3, "黑色": 4}[self.plate_color.get()]
        plate_number = self.plate_number.get().encode('gbk')
        confidence = 1000
        has_car = 1  # 假设有车

        data = struct.pack(">B 6s H", has_car, plate_color.to_bytes(1, 'big') + plate_number, confidence)
        packet = self.create_packet(data, command_code, timestamp)
        self.tcp_client.send_command(packet)
        print("图片采集包已发送")

    def create_packet(self, data_content, command_code, timestamp):
        """创建数据包"""
        protocol_head = 0xfb
        protocol_tail = 0xfe
        total_packets = 1
        packet_number = 0
        data_length = len(data_content)

        checksum = self.calculate_checksum(timestamp, command_code, total_packets, packet_number, data_length,
                                           data_content)

        packet = (
                struct.pack('>B', protocol_head) +
                struct.pack('>I', timestamp) +
                struct.pack('>B', command_code) +
                struct.pack('>H', total_packets) +
                struct.pack('>H', packet_number) +
                struct.pack('>H', data_length) +
                data_content +
                struct.pack('>H', checksum) +
                struct.pack('>B', protocol_tail)
        )
        return packet

    @staticmethod
    def calculate_checksum(timestamp, command_code, total_packets, packet_number, data_length, data_content):
        checksum_data = (
                struct.pack('>I', timestamp) +
                struct.pack('>B', command_code) +
                struct.pack('>H', total_packets) +
                struct.pack('>H', packet_number) +
                struct.pack('>H', data_length) +
                data_content
        )
        return sum(checksum_data) & 0xFFFF

    def register_device(self):
        """完整的注册流程（等待0.5秒后直接发送注册包内容）"""

        # 步骤一：发送初始请求 <001001>，用于注册启动
        timestamp = int(time.time())
        command_code = ord('C')
        initial_data = b"<001001>"
        initial_packet = self.create_packet(initial_data, command_code, timestamp)
        self.tcp_client.send_command(initial_packet)
        print("初始请求包已发送：<001001>")

        # 等待 0.5 秒，不接收服务器确认，直接进入下一步
        time.sleep(0.5)

        # 步骤二：发送注册包内容，包括 DSP 类型和版本号
        registration_data = struct.pack(">B H", self.device_type, self.device_version)
        registration_packet = self.create_packet(registration_data, command_code, timestamp)
        self.tcp_client.send_command(registration_packet)
        print("注册包已发送")

    def start_heartbeat(self):
        """开始心跳包的定时发送"""
        if not self.is_reporting.get():
            self.is_reporting.set(True)
            self.schedule_next_heartbeat()

    def schedule_next_heartbeat(self):
        """定时发送心跳包"""
        if self.is_reporting.get():
            self.send_heartbeat()
            self.root.after(self.heartbeat_interval * 1000, self.schedule_next_heartbeat)

    def send_heartbeat(self):
        """发送心跳包（空包）"""
        timestamp = int(time.time())
        command_code = ord('F')
        data = b''  # 心跳包没有数据内容
        packet = self.create_packet(data, command_code, timestamp)
        self.tcp_client.send_command(packet)
        print("心跳包已发送")

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


if __name__ == "__main__":
    root = tk.Tk()
    root.title("车位相机页面 - 调试模式")


    class MockTCPClient:
        def __init__(self):
            self.server_ip = "127.0.0.1"

        def send_command(self, packet):
            print("发送数据包:", packet)


    class MockApp:
        def create_device_type_selection_page(self):
            print("返回设备选择界面")

        def create_connection_page(self):
            print("返回连接界面")


    tcp_client = MockTCPClient()
    app = MockApp()
    page = ParkingCameraPage(root, tcp_client, app)
    page.setup()

    root.mainloop()
