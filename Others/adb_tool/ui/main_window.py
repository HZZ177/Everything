import tkinter as tk
import os
import sys
from tkinter import ttk
from tkinter import font as tkfont
from Others.adb_tool.managers.device_manager import DeviceManager
from Others.adb_tool.managers.upgrade_manager import UpgradeManager
from Others.adb_tool.managers.log_manager import LogManager
from Others.adb_tool.utils.utils import Util
from Others.adb_tool.utils.config import Config


class MainWindow:
    def __init__(self, root):

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

        self.root = root
        self.device_manager = DeviceManager()
        self.upgrade_manager = UpgradeManager()
        self.log_manager = LogManager()

    def initialize_ui(self):
        """初始化程序基座UI"""

        # 设置程序抬头名称
        self.root.title(f"ADB-设备调试工具-{Config.version}")
        # 居中弹出基座
        Util.center_window(self.root, self.root)

    def create_function_notebook(self, root):
        """顶部标签页：单设备连接/多设备升级"""

        # 清除之前的页面内容
        for widget in root.winfo_children():
            widget.destroy()

        # 设置按钮加粗字体
        bold_font = tkfont.Font(weight="bold")

        # 创建 Notebook 组件
        notebook = ttk.Notebook(root)

        # 添加第一个标签页 - 单设备连接模式
        single_device_frame = ttk.Frame(notebook)
        notebook.add(single_device_frame, text='连接单个设备')
        self.create_ip_input_page(single_device_frame)  # 直接显示设备IP输入界面

        # # 在第一个标签页中添加按钮
        # single_device_button = tk.Button(single_device_frame, text="连接单个设备",
        #                                  command=lambda: self.create_ip_input_table(base_root), font=bold_font,
        #                                  width=20, height=2, bd=4)
        # single_device_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 添加第二个标签页 - 多设备批量升级模式
        multiple_devices_frame = ttk.Frame(notebook)
        notebook.add(multiple_devices_frame, text='批量设备一键升级')
        #self.upgrade_multiple_device(multiple_devices_frame)  # 直接显示批量升级设备页面

        # # 在第二个标签页中添加按钮
        # multiple_devices_button = tk.Button(multiple_devices_frame, text="批量设备一键升级",
        #                                     command=lambda: self.upgrade_multiple_device(base_root), font=bold_font,
        #                                     width=20, height=2, bd=4)
        # multiple_devices_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

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
