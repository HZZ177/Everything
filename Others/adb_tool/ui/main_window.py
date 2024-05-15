import threading
import tkinter as tk
import os
import sys
from tkinter import ttk, messagebox
from tkinter import font as tkfont
from Others.adb_tool.managers.device_function_manager import DeviceManager
from Others.adb_tool.managers.log_manager import LogManager
from Others.adb_tool.utils.utils import Util
from Others.adb_tool.utils.config import Config


class MainWindow:
    def __init__(self, root):

        self.root = root

        # 当前执行程序所处路径，兼容打包为exe后的路径
        if getattr(sys, 'frozen', False):
            self.application_path = os.path.dirname(sys.executable)
        else:
            self.application_path = os.path.dirname(os.path.abspath(__file__))

        # 运行时所处的临时目录位置
        if getattr(sys, 'frozen', False):
            # 如果应用程序是被打包成可执行文件
            self.temp_dir = sys._MEIPASS
        else:
            # 如果应用程序直接运行
            self.temp_dir = os.path.dirname(os.path.abspath(__file__))

        # 定义一些基本变量
        self.btn_connect = None  # 链接设备按钮
        self.device_ip = None  # 单设备连接设备ip
        self.ip_record = []  # 连接设备历史
        self.device_entries = None  # 输入多设备ip列表
        self.device_number = 0  # 多设备ip在数组中的位置

        # 定义一些基本页面属性
        self.main_frame = None  # 主页基座
        self.function_frame = None  # 功能选择界面基座
        self.top_download_log = None  # 下载日志浮窗基座
        self.basic_frame = None  # 选择连接单个设备/批量设备升级界面基座

        self.progress_window = None  # 多设备升级进度窗口
        self.progress_frame = None  # 批量设备升级界面
        self.progress_label = None  # 批量设备升级提示标签
        self.progress_bar = None  # 批量设备升级进度条
        self.text_frame = None  # 多设备升级日志输出frame页
        self.progress_log_text = None  # 日志输出文本框
        self.scrollbar = None  # 多设备升级滚动条

        # 当用户尝试关闭窗口时，调用 on_closing 函数
        root.protocol("WM_DELETE_WINDOW", lambda: Util.on_closing(self.root))

    def initialize_ui(self):
        """初始化程序基座UI"""

        # 设置程序抬头名称
        self.root.title(f"ADB-设备调试工具-{Config.version}")
        # 居中弹出基座
        Util.center_window(self.root, self.root)
        self.create_function_notebook()

    def create_function_notebook(self):
        """顶部标签页：单设备连接/多设备升级"""

        # 清除之前的页面内容
        for widget in self.root.winfo_children():
            widget.destroy()

        # 设置按钮加粗字体
        bold_font = tkfont.Font(weight="bold")

        # 创建 Notebook 组件
        notebook = ttk.Notebook(self.root)

        # 添加第一个标签页 - 单设备连接模式
        single_device_frame = ttk.Frame(notebook)
        notebook.add(single_device_frame, text='连接单个设备')
        self.create_ip_input_page(single_device_frame)  # 直接显示设备IP输入界面

        # 添加第二个标签页 - 多设备批量升级模式
        multiple_devices_frame = ttk.Frame(notebook)
        notebook.add(multiple_devices_frame, text='批量设备一键升级')
        self.upgrade_multiple_device_page(multiple_devices_frame)  # 直接显示批量升级设备页面

        # 绑定标签页切换事件
        notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

        # 将 Notebook 组件放置到窗口中
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    def create_ip_input_page(self, father_frame):
        """连接设备IP输入界面"""

        # 清除之前的页面内容
        for widget in father_frame.winfo_children():
            widget.destroy()

        # 创建主页面
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=20)

        # 定义界面提示词
        label_prompt = tk.Label(self.main_frame, text="请输入要连接的设备完整IP地址:")
        label_prompt.pack(pady=(20, 5))
        # 创建IP地址输入框
        entry_ip = ttk.Combobox(self.main_frame, width=20)
        entry_ip.pack(pady=5)

        # 添加历史记录到下拉列表
        # self.record_previous_devices()
        previous_devices = self.ip_record  # 获取历史记录
        entry_ip['values'] = previous_devices  # 将历史记录填充到下拉列表中

        # 定义链接设备按钮，触发adb connect
        self.btn_connect = tk.Button(self.main_frame, text="连接设备",
                                command=lambda: self.entry_select_function_page(entry_ip.get()))
        self.btn_connect.pack(pady=(5, 20))

        # 固定在页面左上角，返回主页面按钮
        # back_button = tk.Button(self.root, text="返回主页面", command=lambda: self.choose_devices_mode_page(base_root))
        # back_button.place(x=20, y=50)

        # 聚焦到当前输入框
        entry_ip.focus_set()
        self.root.bind("<Return>", lambda event: self.entry_select_function_page(entry_ip.get()))  # 绑定回车键触发连接按钮

        def entry_select_function_page():
            pass

    def entry_select_function_page(self, ip):
        """控制面板页面"""
        self.device_ip = ip
        result = Util.is_ip_legal(ip)
        if not result:
            # 禁用连接设备按钮
            self.btn_connect.config(state=tk.DISABLED)

            remind_label = tk.Label(self.main_frame, text="正在连接设备...")
            remind_label.pack(pady=2)  # 创建并显示提醒标签
            self.main_frame.update_idletasks()  # 强制更新界面

            # 创建并启动连接设备的守护线程
            connect_thread = threading.Thread(target=self.connect_device_async, args=(ip, remind_label))
            connect_thread.daemon = True
            connect_thread.start()
        else:
            messagebox.showwarning(title="提示!", message=result)

    def upgrade_multiple_device_page(self, multiple_devices_frame):
        """批量升级设备页面"""

        # 清除之前的页面内容
        for widget in multiple_devices_frame.winfo_children():
            widget.destroy()

        # self.device_number = 0
        # self.center_window(base_root)

        self.device_entries = []  # 接收批量设备ip的数组
        # # 创建页面
        # self.basic_frame = tk.Frame(multiple_devices_frame)
        # self.basic_frame.pack(pady=20)

        label = tk.Label(multiple_devices_frame, text="请在下方输入要升级的设备IP:")
        label.pack(pady=(20, 5))

        # 生成添加设备按钮
        add_device_button = tk.Button(multiple_devices_frame, text="添加设备", command=self.add_device_and_index)
        add_device_button.pack(side="left", pady=10, padx=20)
        # 生成升级按钮
        upgrade_button = tk.Button(multiple_devices_frame, text="一键升级", command=self.upgrade_all_devices_pre)
        upgrade_button.pack(side="right", pady=10, padx=20)
        # 固定在页面左上角，返回主页面按钮
        # back_button = tk.Button(self.root, text="返回主页面", command=lambda: self.choose_devices_mode_page(self.root))
        # back_button.place(x=20, y=50)

        # 生成第一个初始输入框
        self.add_device_and_index()
