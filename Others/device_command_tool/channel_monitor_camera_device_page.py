import time
import json
import queue
import struct
import threading
import tkinter as tk
import uuid
from tkinter import ttk, messagebox
from server_function import ServerFunctions


class ChannelMonitorCameraPage:
    def __init__(self, root: tk.Tk, tcp_client, app):
        # UI组件
        self.command_label: tk.Label = None
        self.send_button: tk.Button = None
        self.report_switch: ttk.Checkbutton = None
        self.alarm_type: tk.StringVar = None
        self.event_type: tk.StringVar = None
        self.vehicle_type: tk.StringVar = None
        self.plate_color: tk.StringVar = None
        self.plate_entry: tk.Entry = None
        self.confidence_entry: tk.Entry = None

        # 新增的复选框变量
        self.recovery_var = tk.BooleanVar(value=False)

        # 额外的上报事件信息控件
        self.event_specific_frame: tk.Frame = None  # 用于动态显示特定事件的输入控件

        self.root = root
        self.tcp_client = tcp_client
        self.app = app  # 传入主应用程序引用
        self.command = {}  # 改为字典类型
        self.timer = None  # 用于定时发送心跳包的定时器线程
        self.is_reporting = tk.BooleanVar(value=False)  # 标记是否正在定时上报心跳
        self.heartbeat_interval = 10  # 心跳包间隔时间，单位为秒

        self.device_id = "SY17711123"  # 内置的 deviceID
        self.device_version = "RDD.CSA.S1A.1.0"  # 内置的 deviceVersion

        # 绑定窗口大小调整的事件
        self.root.bind("<Configure>", self.on_window_resize)

        # 实例化服务器工具类
        self.ServerFunctions = ServerFunctions(self.tcp_client.server_ip)

        # 创建队列用于线程通信
        self.result_queue = queue.Queue()
        self.root.after(100, self.process_queue)  # 定时检查队列中的消息

    def setup(self):
        """通道监控相机页面初始化"""
        self.clear_window()
        container = tk.Frame(self.root)
        container.pack(expand=True, fill='both')

        # 创建Notebook，用于多个Tab页面
        notebook = ttk.Notebook(container)
        notebook.pack(expand=True, fill='both')

        # 绑定标签页切换事件，触发生成指令
        notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

        # 告警页面
        alarm_page = ttk.Frame(notebook)
        notebook.add(alarm_page, text="相机告警")

        # 事件触发页面
        event_page = ttk.Frame(notebook)
        notebook.add(event_page, text="事件上报")

        # 设置告警类型选项卡中的内容
        self.setup_alarm_page(alarm_page)

        # 设置事件上报选项卡中的内容
        self.setup_event_page(event_page)

        # 显示当前生成的指令，文本居中
        self.command_label = tk.Label(container, text="生成的指令：", anchor='center', justify='center')
        self.command_label.pack(pady=10, fill='x')

        # 底部多个按钮框架
        buttons_frame = tk.Frame(container)
        buttons_frame.pack(pady=20)

        # 发送指令按钮
        self.send_button = tk.Button(buttons_frame, text="发送一次当前指令", command=self.send_command)
        self.send_button.grid(row=0, column=0, padx=10)

        # 返回设备选择界面按钮
        back_button = tk.Button(buttons_frame, text="返回设备选择界面",
                                command=self.back2device_type_selection_page)
        back_button.grid(row=0, column=1, padx=10)

        # 断开服务器连接按钮
        disconnect_button = tk.Button(buttons_frame, text="断开服务器连接", command=self.disconnect)
        disconnect_button.grid(row=0, column=2, padx=10, pady=10)

        # 定时心跳开关
        self.report_switch = ttk.Checkbutton(container, text="定时心跳(10s/次)", variable=self.is_reporting,
                                             command=self.heartbeat_by_time)
        self.report_switch.pack(pady=10)

        # 刷新服务器设备状态的便捷按钮框架
        additional_button_frame = tk.Frame(container)
        additional_button_frame.pack(pady=10)

        # 提示文字
        tk.Label(additional_button_frame, text="-------服务器快捷功能|-_-|-------").grid(row=0, column=0, columnspan=2, padx=10,
                                                                           pady=5)

        get_online_devices_button = tk.Button(
            additional_button_frame,
            text="findCar刷新在线设备",
            command=self.get_all_online_devices
        )
        get_online_devices_button.grid(row=1, column=0, padx=10, pady=5)

        device_status_test_button = tk.Button(
            additional_button_frame,
            text="channel刷新在线设备",
            command=self.device_status_test
        )
        device_status_test_button.grid(row=1, column=1, padx=10, pady=5)

        # 初始化指令生成
        self.generate_command()
        # 设备登录包的初始化发送
        self.send_register_packet()

    def adjust_window_size(self):
        """根据当前组件的需求调整窗口大小"""
        self.root.update_idletasks()  # 确保所有布局都已更新

        # 获取所需的宽度和高度
        required_width = self.root.winfo_reqwidth()
        required_height = self.root.winfo_reqheight()

        # 设置窗口大小
        self.root.geometry(f'{required_width}x{required_height}')

    def on_window_resize(self, event):
        """防止窗口大小调整事件触发无限循环"""
        pass  # 可以根据需要实现额外的逻辑

    def update_wraplength(self, event):
        """根据窗口宽度动态更新command_label的wraplength"""
        # 设置wraplength为容器宽度的90%
        new_wraplength = event.width * 0.9
        self.command_label.config(wraplength=new_wraplength)

    def on_tab_change(self, event):
        """处理标签页切换事件"""
        self.generate_command()

    def setup_alarm_page(self, alarm_page):
        """在告警页面设置告警选项"""
        tk.Label(alarm_page, text="选择告警类型：").pack(pady=10)
        self.alarm_type = tk.StringVar(value="videoFault")
        alarm_options = [
            ("视频故障", "videoFault"),
            ("算法未正常运行", "algNotWork"),
            ("图片编码失败", "jpgEncodeFault"),
            ("连接图片服务器失败", "ossNetFault"),
            ("网络故障", "NetFault")
        ]
        self.create_radiobuttons(alarm_page, alarm_options, self.alarm_type, self.generate_command, max_per_row=3)

        # 可选的moreInfo输入
        tk.Label(alarm_page, text="故障详细信息：").pack(pady=5)
        self.more_info_entry = tk.Entry(alarm_page, width=50)
        self.more_info_entry.pack(pady=5)
        self.more_info_entry.bind("<KeyRelease>", self.generate_command)

        # 添加 recovery 复选框
        self.recovery_checkbox = ttk.Checkbutton(
            alarm_page,
            text="告警恢复",
            variable=self.recovery_var,
            command=self.generate_command  # 复选框状态变化时重新生成命令
        )
        self.recovery_checkbox.pack(pady=10)

    def setup_event_page(self, event_page):
        """在事件触发页面设置事件选项"""
        tk.Label(event_page, text="选择上报事件类型：").pack(pady=10)

        # 创建一个框架来容纳事件类型的 Radiobutton
        event_type_frame = tk.Frame(event_page)
        event_type_frame.pack(pady=5, fill='x')

        self.event_type = tk.StringVar(value="trigerEvent")
        event_options = [
            ("触发事件", "trigerEvent"),
            ("车辆后退事件", "reverseEvent"),
            ("车辆离开事件", "exitEvent"),
            ("交通流量事件", "trafficEvent"),
            # ("滞留/违停事件", "illegalParkingEvent")
        ]

        self.create_radiobuttons(event_type_frame, event_options, self.event_type, self.on_event_type_change,
                                 max_per_row=4)

        # 设置额外参数的框架
        self.event_specific_frame = tk.Frame(event_page)
        self.event_specific_frame.pack(pady=10, fill='both', expand=True)

        # 初始化特定事件的输入控件
        self.setup_event_specific_fields()

    def setup_event_specific_fields(self):
        """根据选择的事件类型，动态设置输入字段"""
        # 首先清空当前的控件
        for widget in self.event_specific_frame.winfo_children():
            widget.destroy()

        event = self.event_type.get()

        # 基础输入字段
        input_frame = tk.Frame(self.event_specific_frame)
        input_frame.pack(pady=5, fill='x')

        # 设置列权重，使控件居中
        for i in range(4):
            input_frame.grid_columnconfigure(i, weight=1)

        # 车辆类型选择框
        tk.Label(input_frame, text="选择车辆类型：").grid(row=0, column=0, columnspan=6, padx=5, pady=5)
        self.vehicle_type = tk.StringVar(value="小型车")
        vehicle_options = [
            ("小型车", "小型车"),
            ("大型车", "大型车"),
            ("摩托车", "摩托车"),
            # ("其他", "其他")  # 没有这个类型
        ]

        # 创建车辆类型的Radiobuttons，文字和选项分两行
        vehicle_rb_frame = tk.Frame(input_frame)
        vehicle_rb_frame.grid(row=1, column=0, columnspan=4, padx=5, pady=5)
        self.create_radiobuttons(vehicle_rb_frame, vehicle_options, self.vehicle_type, self.generate_command, max_per_row=4)

        # 车牌颜色选择框
        tk.Label(input_frame, text="车牌颜色：").grid(row=2, column=0, columnspan=6, padx=5, pady=5)
        self.plate_color = tk.StringVar(value="蓝色")
        plate_color_options = [
            ("蓝色", "蓝色"),
            ("绿色", "绿色"),
            ("黄色", "黄色"),
            ("白色", "白色"),
            ("黑色", "黑色")
        ]

        # 创建车牌颜色的Radiobuttons，文字和选项分两行
        plate_color_rb_frame = tk.Frame(input_frame)
        plate_color_rb_frame.grid(row=3, column=0, columnspan=4, padx=5, pady=5)
        self.create_radiobuttons(plate_color_rb_frame, plate_color_options, self.plate_color, self.generate_command, max_per_row=5)

        # 车牌号输入
        plate_label = tk.Label(input_frame, text="车牌号：")
        plate_label.grid(row=4, column=0, padx=5, pady=5, sticky='e')
        self.plate_entry = tk.Entry(input_frame)
        self.plate_entry.grid(row=4, column=1, padx=5, pady=5, sticky='w')
        self.plate_entry.bind("<KeyRelease>", self.generate_command)

        # 可信度输入
        confidence_label = tk.Label(input_frame, text="可信度(1-1000)：")
        confidence_label.grid(row=4, column=2, padx=5, pady=5, sticky='e')
        self.confidence_entry = tk.Entry(input_frame)
        self.confidence_entry.grid(row=4, column=3, padx=5, pady=5, sticky='w')
        self.confidence_entry.bind("<KeyRelease>", self.generate_command)

        # 根据事件类型添加额外字段
        if event in ["trigerEvent", "reverseEvent", "exitEvent"]:
            # 事件ID输入
            event_id_label = tk.Label(input_frame, text="事件ID：")
            event_id_label.grid(row=5, column=0, padx=5, pady=5, sticky='e')
            self.event_id_entry = tk.Entry(input_frame)
            self.event_id_entry.grid(row=5, column=1, padx=5, pady=5, sticky='w')
            self.event_id_entry.insert(0, str(uuid.uuid4()))
            self.event_id_entry.bind("<KeyRelease>", self.generate_command)

            # 触发标志输入
            trigger_flag_label = tk.Label(input_frame, text="触发标志：")
            trigger_flag_label.grid(row=5, column=2, padx=5, pady=5, sticky='e')
            self.trigger_flag_entry = tk.Entry(input_frame)
            self.trigger_flag_entry.grid(row=5, column=3, padx=5, pady=5, sticky='w')
            self.trigger_flag_entry.bind("<KeyRelease>", self.generate_command)

        elif event == "trafficEvent":
            # 区域状态
            tk.Label(input_frame, text="区域状态：").grid(row=5, column=0, columnspan=6, padx=5, pady=5)
            self.area_state = tk.StringVar(value="0")
            area_state_options = [
                ("正常", "0"),
                ("繁忙", "1"),
                ("拥堵", "2")
            ]
            area_state_rb_frame = tk.Frame(input_frame)
            area_state_rb_frame.grid(row=6, column=0, columnspan=4, padx=5, pady=5)
            self.create_radiobuttons(area_state_rb_frame, area_state_options, self.area_state, self.generate_command, max_per_row=3)

            # 区域状态可信度
            area_state_reliability_label = tk.Label(input_frame, text="区域状态可信度：")
            area_state_reliability_label.grid(row=7, column=0, padx=5, pady=5, sticky='e')
            self.area_state_reliability_entry = tk.Entry(input_frame)
            self.area_state_reliability_entry.grid(row=7, column=1, padx=5, pady=5, sticky='w')
            self.area_state_reliability_entry.bind("<KeyRelease>", self.generate_command)

            # 车辆数量
            car_num_label = tk.Label(input_frame, text="车辆数量：")
            car_num_label.grid(row=7, column=2, padx=5, pady=5, sticky='e')
            self.car_num_entry = tk.Entry(input_frame)
            self.car_num_entry.grid(row=7, column=3, padx=5, pady=5, sticky='w')
            self.car_num_entry.bind("<KeyRelease>", self.generate_command)

        elif event == "illegalParkingEvent":
            # 事件ID输入
            event_id_label = tk.Label(input_frame, text="事件ID：")
            event_id_label.grid(row=5, column=0, padx=5, pady=5, sticky='e')
            self.event_id_entry = tk.Entry(input_frame)
            self.event_id_entry.grid(row=5, column=1, padx=5, pady=5, sticky='w')
            self.event_id_entry.bind("<KeyRelease>", self.generate_command)

            # 违法类型
            tk.Label(input_frame, text="违法类型：").grid(row=6, column=0, padx=5, pady=5, sticky='e')
            self.illegal_type = tk.StringVar(value="0")
            illegal_type_options = [
                ("车辆滞留", "0"),
                ("车辆违停", "1"),
                ("人员滞留", "2"),
                ("非机动车滞留", "3")
            ]
            illegal_type_rb_frame = tk.Frame(input_frame)
            illegal_type_rb_frame.grid(row=7, column=0, columnspan=4, padx=5, pady=5)
            self.create_radiobuttons(illegal_type_rb_frame, illegal_type_options, self.illegal_type, self.generate_command, max_per_row=4)

            # 违法车辆数量
            illegal_car_num_label = tk.Label(input_frame, text="违法车辆数量：")
            illegal_car_num_label.grid(row=8, column=0, padx=5, pady=5, sticky='e')
            self.illegal_car_num_entry = tk.Entry(input_frame)
            self.illegal_car_num_entry.grid(row=8, column=1, padx=5, pady=5, sticky='w')
            self.illegal_car_num_entry.bind("<KeyRelease>", self.generate_command)

            # 违法车辆信息列表
            self.illegal_car_info_frame = tk.Frame(self.event_specific_frame)
            self.illegal_car_info_frame.pack(pady=5, fill='both', expand=True)

            self.illegal_car_info_list = []
            self.add_illegal_car_info()

        # 添加图片数量输入
        image_num_label = tk.Label(input_frame, text="图片数量：")
        image_num_label.grid(row=9, column=0, padx=5, pady=5, sticky='e')
        self.image_num_entry = tk.Entry(input_frame)
        self.image_num_entry.grid(row=9, column=1, padx=5, pady=5, sticky='w')
        self.image_num_entry.insert(0, "1")
        self.image_num_entry.bind("<KeyRelease>", self.generate_command)

        # 当天事件序号
        num_label = tk.Label(input_frame, text="当天事件序号：")
        num_label.grid(row=9, column=2, padx=5, pady=5, sticky='e')
        self.num_entry = tk.Entry(input_frame)
        self.num_entry.grid(row=9, column=3, padx=5, pady=5, sticky='w')
        self.num_entry.insert(0, f"0")
        self.num_entry.bind("<KeyRelease>", self.generate_command)

    def add_illegal_car_info(self):
        """添加一个违法车辆信息输入行"""
        frame = tk.Frame(self.illegal_car_info_frame)
        frame.pack(pady=2, fill='x')

        # 车牌号
        plate_label = tk.Label(frame, text="车牌号：")
        plate_label.grid(row=0, column=0, padx=5, pady=2, sticky='e')
        plate_entry = tk.Entry(frame)
        plate_entry.grid(row=0, column=1, padx=5, pady=2, sticky='w')
        plate_entry.bind("<KeyRelease>", self.generate_command)

        # 车牌可信度
        plate_reliability_label = tk.Label(frame, text="车牌可信度：")
        plate_reliability_label.grid(row=0, column=2, padx=5, pady=2, sticky='e')
        plate_reliability_entry = tk.Entry(frame)
        plate_reliability_entry.grid(row=0, column=3, padx=5, pady=2, sticky='w')
        plate_reliability_entry.bind("<KeyRelease>", self.generate_command)

        # 车牌类型
        plate_type_label = tk.Label(frame, text="车牌类型：")
        plate_type_label.grid(row=0, column=4, padx=5, pady=2, sticky='e')
        plate_type_entry = tk.Entry(frame)
        plate_type_entry.grid(row=0, column=5, padx=5, pady=2, sticky='w')
        plate_type_entry.bind("<KeyRelease>", self.generate_command)

        # 添加到列表
        self.illegal_car_info_list.append({
            "frame": frame,
            "plate_entry": plate_entry,
            "plate_reliability_entry": plate_reliability_entry,
            "plate_type_entry": plate_type_entry
        })

    def create_radiobuttons(self, parent, options, variable, command, max_per_row=3):
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

        # 创建Radiobuttons并排列
        row = 0
        col = 0
        for idx, (text, value) in enumerate(options):
            rb = tk.Radiobutton(frame, text=text, variable=variable, value=value, command=command)
            rb.grid(row=row, column=col, padx=10, pady=5)
            col += 1
            if col >= max_per_row:
                col = 0
                row += 1

        # 让Radiobutton框架的列权重相同，以便居中显示
        for c in range(max_per_row):
            frame.grid_columnconfigure(c, weight=1)

    def create_radiobuttons_inline(self, parent, options, variable, command, row=0, column=0, max_per_row=3):
        """
        创建横向排列的 Radiobutton，每行最多 max_per_row 个，并在指定位置排列
        :param parent: 父容器
        :param options: 选项列表，列表中的每个元素是 (显示文本, 值)
        :param variable: 关联的 Tkinter 变量
        :param command: 选中时调用的命令
        :param row: 起始行
        :param column: 起始列
        :param max_per_row: 每行最大 Radiobutton 数量
        """
        for idx, (text, value) in enumerate(options):
            rb = tk.Radiobutton(parent, text=text, variable=variable, value=value, command=command)
            current_row = row + idx // max_per_row
            current_col = column + idx % max_per_row
            rb.grid(row=current_row, column=current_col, padx=2, pady=2, sticky='nwse')

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def generate_command(self, event=None):
        """根据选项生成告警或事件的指令"""
        # 直接使用内置的device_id
        camera_id = self.device_id

        # 判断当前选中的标签页
        current_tab = self.get_current_tab()
        if current_tab == "相机告警":
            # 获取告警相关参数
            message = self.alarm_type.get()
            more_info = self.more_info_entry.get().strip()
            is_recovery = self.recovery_var.get()

            # 构造告警命令
            command_data = {
                "cmd": "faultMessage",
                "cmdTime": str(int(time.time())),
                "deviceType": "5",
                "deviceId": camera_id
            }

            if is_recovery:
                command_data["recovery"] = message
            else:
                command_data["message"] = message

            if more_info:
                command_data["moreInfo"] = more_info

            self.command = command_data

        elif current_tab == "事件上报":
            # 获取事件相关参数
            event_type = self.event_type.get()
            plate = self.plate_entry.get().strip()
            confidence = self.confidence_entry.get().strip()
            vehicle_type = self.vehicle_type.get()
            plate_color = self.plate_color.get()
            image_num = self.image_num_entry.get().strip()
            num = self.num_entry.get().strip()

            # 基础事件数据
            command_data = {
                "cmd": "reportInfo",
                "cmdTime": str(int(time.time())),
                "deviceType": "5",
                "deviceId": camera_id,
                "eventType": event_type,
                "imageNum": image_num,
                "num": num
            }

            # 公共字段
            if plate:
                command_data["plate"] = plate
            if confidence:
                command_data["plateReliability"] = confidence
            if hasattr(self, 'plate_type_entry') and self.plate_type_entry.get():
                command_data["plateType"] = self.plate_type_entry.get()
            if vehicle_type:
                command_data["carType"] = vehicle_type
            if plate_color:
                command_data["carColour"] = plate_color

            # 根据事件类型添加特定字段
            if event_type in ["trigerEvent", "reverseEvent", "exitEvent"]:
                event_id = getattr(self, 'event_id_entry', None)
                trigger_flag = getattr(self, 'trigger_flag_entry', None)
                if event_id and event_id.get():
                    command_data["eventId"] = event_id.get()
                if trigger_flag and trigger_flag.get():
                    command_data["triggerFlag"] = trigger_flag.get()

            elif event_type == "trafficEvent":
                area_state = self.area_state.get()
                area_state_reliability = getattr(self, 'area_state_reliability_entry', None)
                car_num = getattr(self, 'car_num_entry', None)
                if area_state:
                    command_data["areaState"] = area_state
                if area_state_reliability and area_state_reliability.get():
                    command_data["areaStateReliability"] = area_state_reliability.get()
                if car_num and car_num.get():
                    command_data["carNum"] = car_num.get()

            elif event_type == "illegalParkingEvent":
                event_id = getattr(self, 'event_id_entry', None)
                illegal_type = self.illegal_type.get()
                illegal_car_num = getattr(self, 'illegal_car_num_entry', None)
                if event_id and event_id.get():
                    command_data["eventId"] = event_id.get()
                if illegal_type:
                    command_data["eventTypeVal"] = illegal_type
                if illegal_car_num and illegal_car_num.get():
                    command_data["illegalCarNum"] = illegal_car_num.get()

                # 违法车辆信息列表
                illegal_car_info_list = []
                for car_info in self.illegal_car_info_list:
                    plate = car_info["plate_entry"].get().strip()
                    reliability = car_info["plate_reliability_entry"].get().strip()
                    plate_type = car_info["plate_type_entry"].get().strip()
                    if plate and reliability and plate_type:
                        illegal_car_info = {
                            "plate": plate,
                            "plateReliability": reliability,
                            "plateType": plate_type
                        }
                        illegal_car_info_list.append(illegal_car_info)
                if illegal_car_info_list:
                    command_data["illegalCarInfoList"] = illegal_car_info_list

            self.command = command_data

        else:
            self.command = {}

        # 更新指令显示为单行字符串，并允许自动换行，文本居中
        command_str = f"生成的指令：{json.dumps(self.command, ensure_ascii=False)}"
        current_width = self.root.winfo_width()  # 获取当前窗口宽度
        self.command_label.config(text=command_str, wraplength=current_width * 0.9)

        # 调整窗口大小
        self.adjust_window_size()

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
            packet = self.create_packet(register_packet, command_code='T')
            self.tcp_client.send_command(packet)
            self.root.after(1000, self.start_heartbeat)  # 延迟1秒后启动心跳包
        else:
            self.command_label.config(text="无法获取设备ID，无法发送注册包")

    def start_heartbeat(self):
        """开始定时发送心跳包"""
        if not self.is_reporting.get():  # 如果没有手动启动心跳定时器，则启动它
            self.is_reporting.set(True)
            self.heartbeat_by_time()

    def send_command(self):
        """发送生成的指令到服务器"""
        if not self.command:
            messagebox.showwarning("警告", "没有生成的指令可发送！")
            return
        # 调用封包函数
        packet = self.create_packet(self.command, command_code='T')
        if packet:
            # 通过TCP客户端发送封装后的数据包
            self.tcp_client.send_command(packet)
            # messagebox.showinfo("成功", "指令已发送！")

    def disconnect(self):
        """断开连接并返回初始界面"""
        self.stop_heartbeat()  # 停止心跳包的定时器
        self.tcp_client.disconnect()  # 断开与服务器的连接
        self.app.create_connection_page()  # 返回初始连接界面
        self.app.root.title("TCP设备指令模拟工具")  # 清除标题中的服务器连接信息

    def back2device_type_selection_page(self):
        """返回设备类型选择界面"""
        self.stop_heartbeat()  # 停止心跳包的定时器
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
            heartbeat_packet = self.construct_heartbeat_packet()
            self.tcp_client.send_command(heartbeat_packet)

            # 每次间隔10秒发送心跳包
            self.timer = threading.Timer(self.heartbeat_interval, self.schedule_next_heartbeat)
            self.timer.daemon = True
            self.timer.start()

    def construct_heartbeat_packet(self):
        """构造心跳包"""
        camera_id = self.device_id
        cmd_time = int(time.time())
        area_state = 0  # 默认区域状态为正常

        heartbeat_packet = {
            "cmd": "heartbeat",
            "cmdTime": str(cmd_time),
            "deviceId": camera_id,
            "deviceType": "5",
            "areaState": str(area_state)
        }

        return self.create_packet(heartbeat_packet, command_code='T')

    def create_packet(self, command_data: dict, command_code: str) -> bytes:
        """
        根据协议要求封装指令数据
        :param command_data: 需要封包的命令数据字典
        :param command_code: 命令码，作为字符传入，将转换为ASCII并使用16进制表示
        :return: 封装后的二进制数据
        """
        try:
            # 将 command_data 字典转换为 JSON 字符串，并编码为 gbk 字节
            data_bytes = json.dumps(command_data, ensure_ascii=False).encode('gbk')
        except (TypeError, ValueError) as e:
            self.command_label.config(text=f"JSON编码错误: {e}")
            return b''

        protocol_head = 0xfb  # 协议头
        protocol_tail = 0xfe  # 协议尾
        timestamp = int(time.time())

        if len(command_code) != 1:
            raise ValueError("command_code必须是单个字符")
        command_code_ascii = ord(command_code)

        total_packets = 1  # 总包数
        packet_number = 0  # 包序号
        data_length = len(data_bytes)  # 数据长度

        checksum = self.calculate_checksum(timestamp, command_code_ascii, total_packets, packet_number, data_length,
                                           data_bytes)

        try:
            packet = (struct.pack('>B', protocol_head) +
                      struct.pack('>I', timestamp) +
                      struct.pack('>B', command_code_ascii) +
                      struct.pack('>H', total_packets) +
                      struct.pack('>H', packet_number) +
                      struct.pack('>H', data_length) +
                      data_bytes +
                      struct.pack('>H', checksum) +
                      struct.pack('>B', protocol_tail))
        except struct.error as e:
            self.command_label.config(text=f"封包结构错误: {e}")
            return b''

        # 对特殊字符进行转义
        escaped_packet = self.escape_packet(packet)

        return escaped_packet

    @staticmethod
    def calculate_checksum(timestamp, command_code_ascii, total_packets, packet_number, data_length, data_bytes):
        """
        计算校验和
        """
        checksum_data = (struct.pack('>I', timestamp) + struct.pack('>B', command_code_ascii) +
                         struct.pack('>H', total_packets) + struct.pack('>H', packet_number) +
                         struct.pack('>H', data_length) + data_bytes)
        checksum = sum(checksum_data) & 0xFFFF  # 取16位
        return checksum

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

    def on_event_type_change(self):
        """事件类型改变时，更新特定字段的显示"""
        self.setup_event_specific_fields()
        self.generate_command()

    def on_device_type_selected(self):
        """确认选择设备类型后的处理逻辑"""
        # 这里你需要实现确认选择后的具体逻辑
        # 例如，获取选择的设备类型并进行相应的处理
        messagebox.showinfo("确认选择", "设备类型已确认选择！")
        # 你可以根据实际需求进行更多处理
        pass

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
    # 测试运行该模块时直接生成界面
    root = tk.Tk()  # 创建根窗口
    root.title("通道监控相机页面 - 调试模式")

    # 模拟一个TCP客户端（需要根据你的实际实现进行修改）
    class MockTCPClient:
        def __init__(self):
            pass

        def send_command(self, packet):
            print(f"发送数据包: {packet}")

        def disconnect(self):
            print("断开连接")


    # 模拟主程序对象（如果有特定功能需要主程序支持可以在这里模拟）
    class MockApp:
        def create_device_type_selection_page(self):
            print("返回设备选择界面")

        def create_connection_page(self):
            print("返回连接界面")


    # 创建一个模拟的TCP客户端和应用程序实例
    tcp_client = MockTCPClient()
    app = MockApp()

    # 实例化通道监控相机页面
    page = ChannelMonitorCameraPage(root, tcp_client, app)
    page.setup()  # 初始化界面

    root.mainloop()  # 启动Tkinter事件循环
