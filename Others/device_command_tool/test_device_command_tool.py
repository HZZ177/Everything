import tkinter as tk
import re
from tkinter import messagebox
import socket


class TCPClientApp:
    def __init__(self, root):
        self.root = root
        self.center_window(self.root, relative_size=3, calculate_size=10)
        self.root.title("TCP设备指令模拟工具")
        self.server_socket = None
        self.server_ip = ""
        self.server_port = 0
        self.detector_id = 1  # 默认探测器地址

        # 初始界面布局
        self.create_connection_page()

    def create_connection_page(self):
        """创建服务器连接界面"""
        self.clear_window()

        # 创建一个父容器Frame，用于居中内容
        container = tk.Frame(self.root)
        container.pack(expand=True)  # 使Frame填满整个窗口并居中

        # 创建服务器连接界面控件
        tk.Label(container, text="服务器 IP:").pack(pady=10)
        self.server_ip_entry = tk.Entry(container)
        self.server_ip_entry.pack(pady=5)

        tk.Label(container, text="服务器端口:").pack(pady=10)
        self.server_port_entry = tk.Entry(container)
        self.server_port_entry.pack(pady=5)

        # 添加探测器地址输入框
        tk.Label(container, text="探测器地址:").pack(pady=10)
        self.detector_id_entry = tk.Entry(container)
        self.detector_id_entry.pack(pady=5)

        self.connect_button = tk.Button(container, text="连接服务器", command=self.connect_to_server)
        self.connect_button.pack(pady=20)

    def create_main_page(self):
        """创建主界面，用于生成和发送指令"""
        self.clear_window()

        # 创建一个父容器Frame，用于居中内容
        container = tk.Frame(self.root)
        container.pack(expand=True)  # 使Frame填满整个窗口并居中

        # 创建车位状态选择框架
        tk.Label(container, text="选择车位状态：").pack(pady=10)
        car_status_frame = tk.Frame(container)
        car_status_frame.pack(pady=10)

        # 车位状态选择（两行两列）
        self.car_status = tk.StringVar(value="有车正常")
        car_status_options = [("有车正常", 0, 0), ("有车故障", 0, 1), ("无车正常", 1, 0), ("无车故障", 1, 1)]
        for option, row, col in car_status_options:
            tk.Radiobutton(car_status_frame, text=option, variable=self.car_status, value=option,
                           command=lambda: [self.update_fault_status(), self.generate_command()]).grid(row=row,
                                                                                                       column=col,
                                                                                                       padx=20, pady=5)

        # 创建故障状态选择框架
        tk.Label(container, text="选择故障状态（可多选）：").pack(pady=10)
        self.fault_status_frame = tk.Frame(container)
        self.fault_status_frame.pack(pady=10)

        # 故障状态选择（两行四列）
        self.faults = {}
        self.fault_checkbuttons = {}
        fault_options = [
            ("传感器故障", 0, 0), ("传感器满偏", 0, 1),
            ("雷达故障", 0, 2), ("高低温预警", 0, 3),
            ("RTC故障", 1, 0), ("通讯故障", 1, 1),
            ("电池低压预警", 1, 2)
        ]
        for option, row, col in fault_options:
            var = tk.IntVar()
            self.faults[option] = var
            checkbutton = tk.Checkbutton(self.fault_status_frame, text=option, variable=var,
                                         command=self.generate_command)  # 每次点击复选框生成指令
            checkbutton.grid(row=row, column=col, padx=10, pady=5)
            self.fault_checkbuttons[option] = checkbutton

        # 生成指令和发送按钮
        self.command_label = tk.Label(container, text="生成的指令：")
        self.command_label.pack(pady=10)

        # 底部按钮框架
        button_frame = tk.Frame(container)
        button_frame.pack(pady=10)

        self.send_button = tk.Button(button_frame, text="发送指令", command=self.send_command)
        self.send_button.grid(row=0, column=1, padx=10)

        self.disconnect_button = tk.Button(button_frame, text="断开连接", command=self.disconnect_from_server)
        self.disconnect_button.grid(row=0, column=2, padx=10)

        # 初始化故障状态框为可用，并生成初始指令
        self.update_fault_status()
        self.generate_command()

    def create_device_type_selection_page(self):
        """创建设备类型选择页面"""
        self.clear_window()

        # 创建父容器，用于居中内容
        container = tk.Frame(self.root)
        container.pack(expand=True)

        tk.Label(container, text="请选择设备类型:").pack(pady=10)

        # 设备类型的选择列表
        device_types = ["Lora节点", "其他设备类型"]  # 目前只实现了lora节点，后续可扩展
        self.selected_device_type = tk.StringVar(value="Lora节点")  # 默认选中Lora节点

        # 创建下拉菜单
        device_type_menu = tk.OptionMenu(container, self.selected_device_type, *device_types)
        device_type_menu.pack(pady=10)

        # 确认按钮，选择设备类型后跳转到相应的页面
        confirm_button = tk.Button(container, text="确认选择", command=self.on_device_type_selected)
        confirm_button.pack(pady=20)

    def on_device_type_selected(self):
        """根据设备类型选择跳转到相应的页面"""
        selected_type = self.selected_device_type.get()

        if selected_type == "Lora节点":
            # 跳转到Lora节点页面
            self.create_main_page()  # 这是当前的主页面
        else:
            # 如果是其他设备类型，可以定义一个新的页面
            self.create_other_device_page()

    def create_other_device_page(self):
        """创建其他设备类型的页面"""
        self.clear_window()

        # 创建父容器，用于居中内容
        container = tk.Frame(self.root)
        container.pack(expand=True)

        # 这里可以放置其他设备类型的内容和控件
        tk.Label(container, text="这是其他设备类型的页面").pack(pady=10)
        # 可以继续添加其他控件和功能，根据设备类型的需求

    def clear_window(self):
        """清除窗口中的所有组件"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def center_window(self, target_window, relative_size=4, calculate_size=0):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        width_min_size = 400

        width = max(screen_width // relative_size, width_min_size)
        height = max(screen_height // relative_size, calculate_size * 50)

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        target_window.geometry('%dx%d+%d+%d' % (width, height, x, y))
        target_window.update()

    import re  # 导入正则表达式模块

    def connect_to_server(self):
        """尝试连接到服务器"""
        self.server_ip = self.server_ip_entry.get().strip()
        self.server_port = self.server_port_entry.get().strip()

        # 使用正则表达式校验IP格式
        ip_pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
        if not ip_pattern.match(self.server_ip):
            messagebox.showerror("错误", "请输入有效的IPv4地址")
            return

        # 校验每个部分是否在0到255之间
        octets = self.server_ip.split('.')
        if not all(0 <= int(octet) <= 255 for octet in octets):
            messagebox.showerror("错误", "IP地址的每一部分必须是0到255之间的数字")
            return

        # 校验端口号是否为有效数字
        if not self.server_port.isdigit() or not (0 < int(self.server_port) <= 65535):
            messagebox.showerror("错误", "请输入有效的端口号（1-65535）")
            return

        self.server_port = int(self.server_port)

        # 获取探测器地址
        try:
            self.detector_id = int(self.detector_id_entry.get())
        except ValueError:
            messagebox.showerror("错误", "探测器地址必须为有效的数字")
            return

        try:
            # 设置一个超时时间（例如5秒）
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.settimeout(5)  # 设置超时为5秒
            self.server_socket.connect((self.server_ip, self.server_port))
            messagebox.showinfo("成功", "成功连接到服务器")
            self.create_device_type_selection_page()  # 切换到设备类型选择页面

        except socket.timeout:
            messagebox.showerror("错误", "连接服务器超时，请检查网络连接或服务器状态")
        except Exception as e:
            messagebox.showerror("错误", f"无法连接到服务器: {e}")

    def update_fault_status(self):
        """根据车位状态启用或禁用故障状态，并清除选择"""
        selected_status = self.car_status.get()
        if selected_status in ["有车正常", "无车正常"]:
            # 禁用所有故障状态复选框，并清除选中状态
            for checkbutton in self.fault_checkbuttons.values():
                checkbutton.config(state=tk.DISABLED)
                # 清除选项
                self.faults[checkbutton.cget('text')].set(0)
        else:
            # 启用所有故障状态复选框
            for checkbutton in self.fault_checkbuttons.values():
                checkbutton.config(state=tk.NORMAL)

    def generate_command(self):
        """根据选择生成指令"""
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

        # 使用探测器地址和节点的最后一个字节生成AAAAA部分
        node_last_octet = int(self.server_ip.split(".")[-1])
        aaaaa = f"{(node_last_octet << 8 | self.detector_id):05d}"

        # 拼装命令
        self.command = f"({aaaaa}{car_status_code}{zz_hex})"
        self.command_label.config(text=f"生成的指令：{self.command}")

    def send_command(self):
        """发送生成的指令到服务器"""
        if self.server_socket:
            try:
                self.server_socket.sendall(self.command.encode())
                # response = self.server_socket.recv(1024)
                # messagebox.showinfo("响应", f"收到服务器响应: {response.decode()}")
            except Exception as e:
                messagebox.showerror("错误", f"发送指令时出错: {e}")
        else:
            messagebox.showwarning("警告", "未连接到服务器")

    def disconnect_from_server(self):
        """断开与服务器的连接"""
        if self.server_socket:
            self.server_socket.close()
            self.server_socket = None
            messagebox.showinfo("断开", "已断开与服务器的连接")
        self.create_connection_page()  # 返回初始连接界面


if __name__ == "__main__":
    root = tk.Tk()
    app = TCPClientApp(root)
    root.mainloop()
