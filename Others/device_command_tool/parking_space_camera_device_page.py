import tkinter as tk
from tkinter import ttk
import struct
import time


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

        # 有车无车上报页面状态
        self.parking_statuses_parked = [tk.StringVar(value="0") for _ in range(6)]
        self.parking_selected_parked = [tk.BooleanVar(value=False) for _ in range(6)]  # 控制每个车位是否发送

        # 进车出车上报页面状态
        self.parking_statuses_move = [tk.StringVar(value="2") for _ in range(6)]
        self.parking_selected_move = [tk.BooleanVar(value=False) for _ in range(6)]  # 控制每个车位是否发送

    def setup(self):
        """设置UI界面"""

        # 清空前置页面
        self.clear_window()

        # 创建标签页
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill="both")

        # 创建有车无车上报页面
        parked_page = ttk.Frame(notebook)
        notebook.add(parked_page, text="有车无车上报")

        # 创建进车出车上报页面
        move_page = ttk.Frame(notebook)
        notebook.add(move_page, text="进车出车上报")

        # 创建图片上传页面
        image_page = ttk.Frame(notebook)
        notebook.add(image_page, text="上传图片")

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

        tk.Label(container, text="选择每个车位的状态（有车/无车）：").grid(row=0, column=0, columnspan=8, pady=5)

        # 为每个车位设置复选框和单选框
        self.parking_status_radiobuttons_parked = []
        for idx in range(6):
            check = tk.Checkbutton(container, text=f"车位 {idx + 1}", variable=self.parking_selected_parked[idx],
                                   command=lambda i=idx: self.toggle_parking_status(i, 'parked'))
            check.grid(row=idx + 1, column=0, padx=5, pady=5)

            radio_no_car = tk.Radiobutton(container, text="无车", variable=self.parking_statuses_parked[idx], value="0",
                                          state="disabled")
            radio_no_car.grid(row=idx + 1, column=1, padx=5, sticky="w")

            radio_with_car = tk.Radiobutton(container, text="有车", variable=self.parking_statuses_parked[idx],
                                            value="1", state="disabled")
            radio_with_car.grid(row=idx + 1, column=2, padx=5, sticky="w")

            # 将当前车位的单选按钮添加到列表
            self.parking_status_radiobuttons_parked.append((radio_no_car, radio_with_car))

        # 持续上报和上报一次按钮
        tk.Checkbutton(container, text="持续上报", variable=self.continuous_reporting,
                       command=self.toggle_continuous_reporting).grid(row=8, column=0, padx=5, pady=10)
        tk.Button(container, text="上报一次", command=self.report_parking_status_once).grid(row=8, column=2, padx=5,
                                                                                            pady=10)

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

        tk.Label(container, text="选择每个车位的状态（进车/出车）：").grid(row=0, column=0, columnspan=8, pady=5)

        # 为每个车位设置复选框和单选框
        self.parking_status_radiobuttons_move = []
        for idx in range(6):
            check = tk.Checkbutton(container, text=f"车位 {idx + 1}", variable=self.parking_selected_move[idx],
                                   command=lambda i=idx: self.toggle_parking_status(i, 'move'))
            check.grid(row=idx + 1, column=0, padx=5, pady=5)

            radio_out = tk.Radiobutton(container, text="出车", variable=self.parking_statuses_move[idx], value="2",
                                       state="disabled")
            radio_out.grid(row=idx + 1, column=1, padx=5, sticky="w")

            radio_in = tk.Radiobutton(container, text="进车", variable=self.parking_statuses_move[idx], value="3",
                                      state="disabled")
            radio_in.grid(row=idx + 1, column=2, padx=5, sticky="w")

            # 将当前车位的单选按钮添加到列表
            self.parking_status_radiobuttons_move.append((radio_out, radio_in))

        tk.Button(container, text="上报一次", command=self.report_move_status_once).grid(row=8, column=1, columnspan=4,
                                                                                         pady=10)

    def setup_image_page(self, container):
        """图片上传页面"""

        tk.Label(container, text="图片采集").grid(row=0, column=0, columnspan=6, pady=10)

        # 车牌号：标签和输入框在同一行，居中显示
        tk.Label(container, text="车牌号：").grid(row=1, column=1, sticky="e", padx=5, pady=5)
        self.plate_number = tk.Entry(container)
        self.plate_number.grid(row=1, column=2, columnspan=6, sticky="w", padx=5, pady=5)

        # 车牌颜色：标签和选项在同一行横向排列，选项每行最多三个
        tk.Label(container, text="车牌颜色：").grid(row=2, column=1, sticky="e", padx=5, pady=5)
        self.plate_color = tk.StringVar(value="蓝色")
        color_options = ["蓝色", "绿色", "黄色", "白色", "黑色"]

        # 按每行三个进行分布
        for idx, color in enumerate(color_options):
            row = 2 + idx // 3  # 第2行开始，每三项换一行
            col = idx % 3 + 2  # 从第2列开始分布
            tk.Radiobutton(container, text=color, variable=self.plate_color, value=color).grid(row=row, column=col,
                                                                                               padx=5, pady=5,
                                                                                               sticky="w")

        # 上传图片按钮，居中放置在最后一行
        tk.Button(container, text="上传图片", command=self.upload_image).grid(row=4, column=0, columnspan=6, pady=40)

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
        """发送注册包"""
        timestamp = int(time.time())
        command_code = ord('C')
        data = struct.pack(">B H", self.device_type, self.device_version)

        packet = self.create_packet(data, command_code, timestamp)
        self.tcp_client.send_command(packet)
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
