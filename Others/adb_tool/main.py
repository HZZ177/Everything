#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/4/11 13:55
# @Author  : Heshouyi
# @File    : main.py
# @Software: PyCharm
# @description:
import datetime
import subprocess
import os
import sys
import threading
import ctypes
import winreg
import requests
import platform
import threading
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox, filedialog, ttk


class Application:
    def __init__(self, base_root):
        # 初始化程序基座

        # 获取adb和scrcpy的完整路径

        self.base_path = os.path.abspath(os.path.dirname(__file__))
        self.adb_path = os.path.join(self.base_path, 'scrcpy_tool', 'adb.exe')
        self.scrcpy_path = os.path.join(self.base_path, 'scrcpy_tool', 'scrcpy.exe')

        # 定义不同设备的日志路径
        self.fccc_logfile = "/sdcard/Android/data/com.keytop.fccc/files/log"  # fcc收费一体机
        self.fsfp_logfile = "/sdcard/Android/data/com.keytop.fsfp/files/log"  # fsfp立式人脸找车机
        self.fsfa_logfile = "/sdcard/Android/data/com.keytop.fsfa/files/log"  # fsfa壁挂式人脸找车机
        self.lcdgs_logfile = "/sdcard/Android/data/com.keytop.lcdgs/files/log"  # LCD显示屏

        # 保存日志文件路径
        self.download_log_path = self.base_path

        # 定义一些基本属性
        self.main_frame = None      # 主页基座
        self.function_frame = None  # 功能选择界面基座
        self.top_download_log = None    # 下载日志浮窗基座
        self.basic_frame = None  # 选择连接单个设备/批量设备升级界面基座

        self.progress_window = None     # 多设备升级进度条窗口
        self.progress_frame = None
        self.progress_label = None
        self.progress_bar = None
        self.progress_log_text = None


        self.device_ip = None   # 单设备连接设备ip
        self.device_entries = None   # 输入多设备ip列表
        self.device_number = 0   # 多设备ip在数组中的位置

        # 定义版本号
        self.version = "v1.2.0"

        # 定义初始化窗口的基本信息
        self.root = base_root
        self.root.title(f"ADB-设备调试工具-{self.version}")
        # 初始化窗口居中弹出
        self.center_window(self.root, 3)
        # 当用户尝试关闭窗口时，调用 on_closing 函数
        root.protocol("WM_DELETE_WINDOW", lambda: app.on_closing())

    def choose_devices_mode_page(self, base_root):
        """进入哪种设备连接模式，单设备/多设备升级"""

        # 清除之前的页面内容
        for widget in base_root.winfo_children():
            widget.destroy()

        # 设置按钮加粗字体
        bold_font = tkfont.Font(weight="bold")

        # 单设备连接模式按钮
        single_device_button = tk.Button(base_root, text="连接单个设备",
                                         command=lambda: self.create_ip_input_table(self.root), font=bold_font, width=20, height=2, bd=4)
        single_device_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 多设备批量升级模式按钮
        multiple_devices_button = tk.Button(base_root, text="批量设备一键升级",
                                            command=lambda: self.upgrade_multiple_device(base_root),font=bold_font, width=20, height=2, bd=4)
        multiple_devices_button.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

    def upgrade_multiple_device(self, base_root):
        """批量升级设备页面"""

        # 清除之前的页面内容
        for widget in base_root.winfo_children():
            widget.destroy()

        # self.device_number = 0
        # self.center_window(base_root)

        self.device_entries = []    # 接收批量设备ip的数组
        # 创建页面
        self.basic_frame = tk.Frame(base_root)
        self.basic_frame.pack(pady=20)

        label = tk.Label(self.basic_frame, text="请在下方输入要升级的设备IP:")
        label.pack(pady=(20, 5))

        # 生成添加设备按钮
        add_device_button = tk.Button(self.basic_frame, text="添加设备", command=self.add_device_and_index)
        add_device_button.pack(side="left", pady=10, padx=20)
        # 生成升级按钮
        upgrade_button = tk.Button(self.basic_frame, text="一键升级", command=self.upgrade_all_devices_pre)
        upgrade_button.pack(side="right", pady=10, padx=20)
        # 固定在页面左上角，返回主页面按钮
        back_button = tk.Button(self.root, text="返回主页面", command=lambda: self.choose_devices_mode_page(self.root))
        back_button.place(x=20, y=10)

        # 生成第一个初始输入框
        self.add_device_and_index()

    def back_to_main_page(self, basic_frame):
        # 清除之前的页面内容
        basic_frame.destroy()

        self.choose_devices_mode_page(self.root)
        # # 重新设置窗口大小为初始值
        self.center_window(self.root, relative_size=3)

    def add_device_and_index(self):
        """添加新的设备输入框，并更新索引位置"""
        new_entry_var = tk.StringVar()  # 使用StringVar控件，动态保存输入框的值
        self.device_entries.append(new_entry_var)  # 将每次生成的控件添加到数组中

        # 创建一个框架用于包含输入框和摧毁按钮
        entry_frame = tk.Frame(self.basic_frame)
        entry_frame.pack(pady=2)

        # 在框架中创建输入框
        new_entry = tk.Entry(entry_frame, textvariable=self.device_entries[-1])
        new_entry.pack(side="left")

        # 在框架中创建摧毁按钮
        destroy_button = tk.Button(entry_frame, text="删除", command=lambda: self.remove_entry(new_entry_var, entry_frame))
        destroy_button.pack(side="right", padx=2, pady=0)

        self.device_number += 1
        # self.center_window(self.root, calculate_size=self.device_number)

    def remove_entry(self, entry_var, frame):
        """删除数组中保存的StringVar控件"""
        self.device_entries.remove(entry_var)  # 从数组中移除对应的 StringVar
        frame.destroy()  # 销毁框架

    def upgrade_all_devices_pre(self):
        """一键升级所有设备——前置检查"""

        # 遍历所有输入框的值，并存入数组中
        ip_addresses = []
        for entry in self.device_entries:
            ip_address = entry.get()
            if ip_address not in ip_addresses:
                ip_addresses.append(ip_address)
            else:
                messagebox.showerror("提示", f"存在重复IP{ip_address}")
                return

        # 输入判空
        if len(ip_addresses) == 0:
            messagebox.showerror("提示", "请输入至少一个设备IP！")
            return

        # 如果输入非空，检查所有输入ip合法性并将所有非法地址存入
        error_address = []
        for address in ip_addresses:
            result = self.is_ip_legal(address)
            if result != 0:
                error_address.append(address)

        if len(error_address) != 0:
            messagebox.showerror("提示", f"输入IP地址中存在非法地址！\n包含：{error_address}")
        else:
            self.upgrade_all_devices(ip_addresses)

        # 调试操作
        # print("所有设备的 IP 地址:", ip_addresses)

    def upgrade_all_devices(self, ip_addresses):
        """一次性升级所有列出的设备"""

        # 选择升级包
        apk_path = filedialog.askopenfilename(
            title="选择一个升级包",
            filetypes=(("apk文件", "*.apk"),)
        )

        if not apk_path:
            messagebox.showinfo("提示", "没有选中任何升级包！")
            return

        # 清除之前的进度条框架
        if hasattr(self, 'progress_frame') and self.progress_frame is not None:
            self.progress_frame.destroy()
        # 创建进度条frame
        self.progress_frame = tk.Frame(self.root)
        self.progress_frame.pack()

        # 添加进度条
        self.progress_label = tk.Label(self.progress_frame, text="升级整体进度：")
        self.progress_label.pack()

        self.progress_bar = tk.ttk.Progressbar(self.progress_frame, orient="horizontal", length=200, mode="determinate")
        self.progress_bar.pack()

        # 添加日志输出框
        self.progress_log_text = tk.Text(self.progress_frame, height=10, width=60)
        self.progress_log_text.pack(pady=5)

        self.root.update()
        # 执行升级过程
        upgrade_thread = threading.Thread(target=self.upgrade_devices, args=(apk_path, ip_addresses))
        upgrade_thread.daemon = True  # 将线程设置为守护线程(主线程退出时自动退出)
        upgrade_thread.start()

    def upgrade_devices(self, apk_path, ip_addresses):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        upgrade_fail_devices = []
        for idx, ip in enumerate(ip_addresses):
            # 先断连所有设备
            self.disconnect_all_device()
            # 执行升级包指令
            command_upgrade_by_apk = [self.adb_path, "install", "-r", apk_path]
            try:
                # 尝试连接指定设备。连接失败则跳过
                self.progress_log_text.insert(tk.END, f"{current_time} - 正在连接设备{ip}...\n")
                self.root.update()
                connect_result = self.connect_device(ip)
                if "超时" in connect_result or "失败" in connect_result:
                    self.progress_log_text.insert(tk.END, f"{current_time} - {connect_result}升级跳过该设备!\n")
                    self.root.update()
                    upgrade_fail_devices.append(ip)
                    continue
                # 连接成功则尝试升级
                self.progress_log_text.insert(tk.END, f"{current_time} - 连接成功，正在升级 {ip}...\n")
                self.root.update()
                upload_result = subprocess.run(command_upgrade_by_apk, creationflags=subprocess.CREATE_NO_WINDOW,
                                               encoding='utf-8', capture_output=True, text=True)
                if upload_result.returncode != 0:
                    upgrade_fail_devices.append(ip)
                    self.progress_log_text.insert(tk.END, f"{current_time} - 设备 {ip} 升级失败!\n")
                else:
                    self.progress_log_text.insert(tk.END, f"{current_time} - {ip}升级成功!!!\n")
                    self.root.update()
            except Exception as e:
                pass
            finally:
                # 更新进度条
                progress_value = int((idx + 1) / len(ip_addresses) * 100)
                self.progress_bar["value"] = progress_value
                self.root.update()
        # self.progress_window.destroy()

        if len(upgrade_fail_devices) != 0:
            self.progress_log_text.insert(tk.END, f"\n{current_time} - 所有设备升级已完成，部分设备升级失败！"
                                                  f"请重新尝试升级或手动升级以下设备！\n\n{upgrade_fail_devices}\n")
            self.root.update()
            messagebox.showwarning("提示！", f"所有设备升级已完成，部分设备升级失败!\n请重新尝试升级或手动升级以下设备!(可在日志末尾手动复制出来)\n{upgrade_fail_devices}\n")
        else:
            self.progress_log_text.insert(tk.END, f"\n{current_time} - 所有设备已经成功升级!!!\n")
            self.root.update()
            messagebox.showinfo("提示！", f"所有设备已经成功升级!")

    def create_ip_input_table(self, base_root):
        """设备IP输入界面"""

        # 清除之前的页面内容
        for widget in base_root.winfo_children():
            widget.destroy()

        # 创建主页面
        self.main_frame = tk.Frame(base_root)
        self.main_frame.pack(pady=20)

        # 定义界面提示词
        label_prompt = tk.Label(self.main_frame, text="请输入要连接的设备完整IP地址:")
        label_prompt.pack(pady=(20, 5))
        # 创建IP地址输入框
        entry_ip = tk.Entry(self.main_frame, width=20)
        entry_ip.pack(pady=5)

        # 定义链接设备按钮，触发adb connect
        btn_connect = tk.Button(self.main_frame, text="连接设备",
                                command=lambda: self.entry_select_function_page(entry_ip.get()))
        btn_connect.pack(pady=(5, 20))

        # 固定在页面左上角，返回主页面按钮
        back_button = tk.Button(self.root, text="返回主页面", command=lambda: self.choose_devices_mode_page(base_root))
        back_button.place(x=20, y=10)

        # 聚焦到当前输入框
        entry_ip.focus_set()
        self.root.bind("<Return>", lambda event: self.entry_select_function_page(entry_ip.get()))  # 绑定回车键触发连接按钮

    def entry_select_function_page(self, ip):
        """尝试连接设备并进入控制面板页面"""
        self.device_ip = ip
        result = self.is_ip_legal(ip)
        if not result:
            # 如果ip校验通过，先断连所有adb连接，然后尝试连接ip设备
            self.disconnect_all_device()
            try:
                result = self.connect_device(ip)
                if "成功" in result:
                    self.main_frame.pack_forget()  # 隐藏主连接界面
                    root.title(f"ADB-设备调试工具{self.version}===当前连接设备：{ip}")
                    # 如果成功连接设备，显示后续控制面板界面
                    self.show_control_panel()
                else:
                    messagebox.showerror("连接失败", "连接失败，请检查IP地址并重试。")
            except subprocess.CalledProcessError as e:
                messagebox.showerror("连接错误", "连接错误：命令执行失败，状态码 {}\n错误信息：{}".format(e.returncode, e.stderr))
            except subprocess.TimeoutExpired:
                messagebox.showerror("连接超时", "连接超时，请检查设备是否在线或IP地址是否正确")
        else:
            messagebox.showwarning(title="提示!", message=result)

    def show_control_panel(self):
        """连接设备IP成功后弹出的界面"""

        # 定义选择功能frame界面基座
        self.function_frame = tk.Frame(self.root)
        self.function_frame.pack(pady=20)

        # 定义按钮信息
        buttons_info = {
            "下载设备日志": lambda: self.show_download_panel(),
            "开启设备屏幕镜像": lambda: self.start_screen_mirror(self.device_ip),
            "升级设备程序(仅支持apk)": lambda: self.upgrade_to_device(),
            "发送ADB命令": lambda: self.ask_for_adb_command(root, self.adb_path),  # 发送简单adb指令并执行
            # "断开设备连接": lambda: self.disconnect_device(root, adb_path),  # 暂时屏蔽该功能，感觉用不上
            "连接其他设备": lambda: self.connect_to_other_device(self.function_frame),
            "重启设备": lambda: self.restart_device()
        }

        button_num = 0
        for button_text, command in buttons_info.items():
            button = tk.Button(self.function_frame, text=button_text, command=command, width=25)
            button.pack(pady=10)
            button_num += 1

        self.center_window(self.root, 3, calculate_size=button_num)

    def show_download_panel(self):
        """不同设备下载日志界面"""

        # 创建一个顶层的对话框窗口
        self.top_download_log = tk.Toplevel(self.root)
        self.top_download_log.title("设备日志下载列表")
        self.top_download_log.focus_set()  # 锁定页面聚焦

        # 提示标签
        label = tk.Label(self.top_download_log, text="先选择设备，下一级页面再选择日志文件范围")
        label.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

        # 生成页面按钮
        buttons_info = {
            "fcc收费一体机": lambda: self.download_log_choose_page(self.top_download_log, self.fccc_logfile),
            "fsfp立式人脸找车机": lambda: self.download_log_choose_page(self.top_download_log, self.fsfp_logfile),
            "fsfa壁挂式人脸找车机": lambda: self.download_log_choose_page(self.top_download_log, self.fsfa_logfile),
            "Lcd显示屏": lambda: self.download_log_choose_page(self.top_download_log, self.lcdgs_logfile)
        }

        row_index = 1  # 从第二行开始放置按钮
        for button_text, command in buttons_info.items():
            button = tk.Button(self.top_download_log, text=button_text, command=command, width=20)
            button.grid(row=row_index, column=1, padx=10, pady=10, sticky='ew')
            row_index += 1  # 更新行号，用于下一个按钮

        # 设定列权重
        self.top_download_log.grid_columnconfigure(0, weight=1)
        self.top_download_log.grid_columnconfigure(1, weight=0)
        self.top_download_log.grid_columnconfigure(2, weight=1)
        self.center_window(self.top_download_log, 4, calculate_size=row_index-1)

    def download_log_choose_page(self, previous_top, log_file_path):
        """下载设备日志"""

        today_time = datetime.date.today().strftime("%Y%m%d")
        log_choose_top = previous_top
        # 清除之前的页面元素
        for widget in log_choose_top.winfo_children():
            widget.destroy()
        # 重命名当前界面基座
        log_choose_top.title("日志日期选择列表")

        # 提示文本标签
        label = tk.Label(log_choose_top, text="请选择你需要下载的日志文件日期")
        label.grid(row=0, column=0, columnspan=3, padx=10, pady=(10, 10), sticky='ew')

        # 生成页面按钮
        buttons_info = {
            "该设备全部日志": lambda: self.download_device_logs(log_choose_top, log_file_path),
            "指定日期的日志文件": lambda: self.download_specific_log(log_choose_top, log_file_path),
            "今天的日志": lambda: self.download_device_logs(log_choose_top, log_file_path, filename=today_time+".log")
        }

        row_index = 1  # 从第二行开始放置按钮
        for button_text, command in buttons_info.items():
            button = tk.Button(log_choose_top, text=button_text, command=command, width=20)
            button.grid(row=row_index, column=1, padx=10, pady=10, sticky='ew')
            row_index += 1  # 更新行号，用于下一个按钮

        # 设定列权重
        log_choose_top.grid_columnconfigure(0, weight=1)
        log_choose_top.grid_columnconfigure(1, weight=0)
        log_choose_top.grid_columnconfigure(2, weight=1)

        # 设定窗口大小、位置并锁定聚焦
        self.center_window(log_choose_top, 4, calculate_size=row_index-1)
        log_choose_top.focus_set()  # 锁定页面聚焦

    def download_device_logs(self, log_choose_top, log_file_path, filename=""):
        """下载当前连接设备的日志"""

        # 当前下载时间
        download_time = datetime.date.today().strftime("%Y%m%d")
        # 当前下载文件保存路径，兼容打包为exe后的路径
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))

        # 下载的日志保存路径为当前文件夹下的自定义文件夹
        save_file_name = f"download_log_{download_time}"
        save_path = os.path.join(application_path, f"download_log_{download_time}/")
        # 检查路径是否存在，不存在则创建
        os.makedirs(save_path, exist_ok=True)

        command = [self.adb_path, 'pull', f"{log_file_path}/{filename}", save_path]
        try:
            result = subprocess.run(command, creationflags=subprocess.CREATE_NO_WINDOW, capture_output=True, text=True)
            if result.returncode == 0:
                log_choose_top.destroy()
                messagebox.showinfo("下载完成", f"文件已保存到当前目录的/{save_file_name}路径下")
            elif "does not exist" in result.stdout:
                messagebox.showerror("下载失败", "目标文件不存在，请检查文件日期是否正确！")
            else:
                messagebox.showerror("下载失败", "文件下载失败,请检查设备类型或设备地址！\n" + result.stderr)
        except Exception as e:
            messagebox.showerror("错误", "执行下载时发生错误!\n" + str(e))

    def download_specific_log(self, log_choose_top, log_file_path):
        """下载自定义日期的日志"""

        # 清除页面元素
        for widget in log_choose_top.winfo_children():
            widget.destroy()

        # 生成提示语
        label = tk.Label(log_choose_top, text="请输入需要下载日志的日期（格式：20240808）:")
        label.pack(pady=(5, 10))

        # 生成日期输入框
        entry_date = tk.Entry(log_choose_top, width=20)
        entry_date.pack(pady=20)

        # 生成按钮，触发下载日志
        btn_connect = tk.Button(log_choose_top, text="下载日志", command=lambda: self.download_device_logs(log_choose_top, log_file_path, entry_date.get() + ".zip"))
        btn_connect.pack(pady=(20, 20))

        # 锁定页面聚焦到输入框
        entry_date.focus_set()
        # 绑定下载日志按钮到回车按钮
        log_choose_top.bind("<Return>", lambda event: self.download_device_logs(log_choose_top, log_file_path, entry_date.get() + ".zip"))  # 绑定回车键触发连接按钮

    def start_screen_mirror(self, device_ip):
        """开启设备屏幕镜像"""
        command = [self.scrcpy_path, '-s', device_ip]
        try:
            # 启动scrcpy，尝试连接镜像
            process = subprocess.Popen(command, creationflags=subprocess.CREATE_NO_WINDOW, stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT, text=True, bufsize=1, universal_newlines=True)
            # 在新线程中异步读取输出，判断状态
            thread = threading.Thread(target=self.read_output, args=(process,))
            thread.start()
        except Exception as e:
            messagebox.showerror("错误", f"启动屏幕镜像时发生错误!\n{str(e)}")

    @staticmethod
    def read_output(process):
        """异步读取镜像程序的输出，判断是否出现异常以及是否关闭"""
        try:
            while True:
                line = process.stdout.readline()
                if not line:
                    break
                line = line.strip()
                print(line)  # 实时打印输出到控制台，便于调试
                if "ERROR" in line or "failed" in line:
                    if "adb reverse" in line:
                        pass
                    else:
                        messagebox.showerror("镜像失败", f"启动设备屏幕镜像失败！\n{line}")
                        return
            # 如果正常结束读取循环，假定镜像成功
            # messagebox.showinfo("镜像结束", "设备屏幕镜像已结束！")
        except Exception as e:
            messagebox.showerror("错误", f"读取输出时发生错误！\n{str(e)}")

    def upgrade_to_device(self):
        """从当前电脑选择apk升级包，远程升级目标设备apk"""

        # 让用户从本地选择用于升级的apk安装包
        upgrade_package = filedialog.askopenfilename(
            title="选择一个升级包",  # 对话框的标题
            filetypes=(("apk文件", "*.apk"),)  # 设置可选择的文件类型仅为apk
        )

        # 定义执行升级包指令
        command_upgrade_by_apk = [self.adb_path, "install", "-r", upgrade_package]
        # 用户选择了文件就执行升级
        if upgrade_package:
            upload_result = subprocess.run(command_upgrade_by_apk, creationflags=subprocess.CREATE_NO_WINDOW,
                                           encoding='utf-8', capture_output=True, text=True)
            if upload_result.returncode == 0:
                messagebox.showinfo("成功", "升级成功！")
            else:
                messagebox.showerror("错误", "升级出现异常！请手动升级！")

    def send_simple_adb_command(self, command):
        """发送简单的ADB命令，并处理输出结果显示"""
        result = subprocess.run([self.adb_path] + command.split(), creationflags=subprocess.CREATE_NO_WINDOW,
                                capture_output=True, text=True)
        if result.returncode == 0:
            messagebox.showinfo("执行成功", f"命令执行成功！\n返回结果：{result.stdout}")
        else:
            messagebox.showerror("执行失败", "命令执行失败！\n错误信息：" + result.stderr)

    def ask_for_adb_command(self, root, adb_path):
        """弹出一个输入框让用户输入ADB命令"""
        # 创建一个简单的对话框窗口
        top = tk.Toplevel(root)
        top.title("输入ADB命令")
        self.center_window(top, 4)

        # 提示标签
        label = tk.Label(top, text="前缀不带adb！请直接输入指令部分！\n例如：disconnect/shell input keyevent等")
        label.pack(padx=20, pady=(30, 0))  # 上边距10, 下边距0，增加视觉舒适度

        # 输入命令的文本框
        command_entry = tk.Entry(top, width=40)
        command_entry.pack(padx=20, pady=(30, 0))
        command_entry.focus_set()  # 聚焦到当前输入框

        # <发送指令>按钮绑定指令事件
        def submit(event=None):
            command = str(command_entry.get())
            try:
                self.send_simple_adb_command(command)
            except Exception as e:
                messagebox.showerror("错误", f"发送指令出现异常！\n错误信息：{e}")
            finally:
                top.destroy()

        # 定义确定按钮，点击后执行命令
        submit_button = tk.Button(top, text="发送指令", command=submit)
        submit_button.pack(pady=(20, 20))
        top.bind("<Return>", submit)  # 绑定回车键触发连接按钮

    def restart_device(self):
        """重启设备并检查命令是否成功下发"""
        command = [self.adb_path, '-s', self.device_ip, 'reboot']
        result = subprocess.run(command, creationflags=subprocess.CREATE_NO_WINDOW, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # 检查进程是否成功结束
        if result.returncode == 0:
            messagebox.showinfo("重启设备", "重启指令已经下发！")
        else:
            # 如果命令执行失败，显示错误信息
            error_message = result.stderr.decode()
            messagebox.showerror("错误", f"重启指令下发失败，请检查IP地址是否正确！\n错误信息：{error_message}")

    def disconnect_all_device(self):
        """adb断开所有设备连接函数"""
        command = [self.adb_path, 'disconnect']
        result = subprocess.run(command, creationflags=subprocess.CREATE_NO_WINDOW,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result

    def connect_device(self, ip):
        """adb连接设备函数"""
        command = [self.adb_path, 'connect', ip]
        try:
            subprocess.run(command, creationflags=subprocess.CREATE_NO_WINDOW, check=True,
                                    capture_output=True, text=True, timeout=5)
            return "连接设备成功！"
        except subprocess.CalledProcessError as e:
            return f"连接设备 {ip} 失败！"
        except subprocess.TimeoutExpired as e:
            return f"连接设备 {ip} 超时！"

    def connect_to_other_device(self, now_frame):
        """连接其他设备按钮绑定事件"""
        result = self.disconnect_all_device()
        if result.returncode == 0:
            messagebox.showinfo("断开连接", "当前设备已断开连接！请重新输入ip")
        else:
            messagebox.showerror("错误", f"指令执行出错！\n错误信息：{result.stderr}")
        now_frame.pack_forget()
        self.create_ip_input_table(self.root)

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

    @staticmethod
    def is_ip_legal(ip):
        """工具函数，判断传入ip是否合法"""

        # ip地址元素拆分
        segments = ip.split('.')
        if segments[0] == "":
            return "ip地址不能为空！请重新输入"
        elif len(segments) != 4:
            return "ip地址格式错误！请重新输入！"
        for segment in segments:
            if not segment.isdigit():
                return "ip地址只能输入纯数字！请重新输入！"
            num = int(segment)
            if num < 0 or num > 255:
                return "ip地址中有超出255的值！请重新输入！"
        return 0    # ip地址正确合法

    def on_closing(self):
        """程序退出时自动触发断连函数"""
        self.disconnect_all_device()
        self.root.destroy()  # 关闭窗口


# def get_system_architecture():
#     return platform.machine()
#
#
# def check_dll_exists(dll_name):
#     try:
#         # 尝试加载 DLL
#         ctypes.WinDLL(dll_name)
#         print(f"{dll_name} is present on the system.")
#         return True
#     except OSError as e:
#         print(f"Failed to load {dll_name}: {e}")
#         return False
#
#
# def check_vc_redist_2015_installed():
#     """检查是否安装了任意版本的Visual C++ 2015"""
#
#     # 设置查询注册表的路径
#     path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
#     # 32位和64位键的访问标志
#     arch_keys = [winreg.KEY_WOW64_32KEY, winreg.KEY_WOW64_64KEY]
#
#     for arch in arch_keys:
#         try:
#             # 打开 Uninstall 键，根据架构访问注册表
#             key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_READ | arch)
#             i = 0
#             while True:
#                 try:
#                     # 枚举 Uninstall 键下的子键
#                     subkey_name = winreg.EnumKey(key, i)
#                     subkey = winreg.OpenKey(key, subkey_name)
#                     try:
#                         # 获取 DisplayName 属性
#                         name = winreg.QueryValueEx(subkey, 'DisplayName')[0]
#                         # 检查名称中是否含有 Visual C++ 2015 Redistributable 字样
#                         if 'Visual C++ 2015' in name:
#                             print(f"Found: {name}")
#                             return True
#                     except OSError:
#                         pass
#                     winreg.CloseKey(subkey)
#                 except OSError:
#                     break
#                 i += 1
#             winreg.CloseKey(key)
#         except OSError:
#             pass
#
#     print("Visual C++ 2015 Redistributable is not installed.")
#     return False
#
#
# def download_and_install_vc_redist(architecture):
#     # 根据架构选择正确的下载链接
#     if architecture.endswith('64'):
#         # 64位系统下载链接
#         url = "https://download.visualstudio.microsoft.com/download/pr/11100229/30017d88dbb4c9c2f59083cda4f35f40/vc_redist.x64.exe"
#     else:
#         # 32位系统下载链接
#         url = "https://download.visualstudio.microsoft.com/download/pr/11100229/78c1e864d806e36f6035d80a0e80399e/vc_redist.x86.exe"
#
#     local_filename = url.split('/')[-1]
#     print(f"Downloading {local_filename} for {architecture}...")
#
#     with requests.get(url, stream=True) as r:
#         r.raise_for_status()
#         with open(local_filename, 'wb') as f:
#             for chunk in r.iter_content(chunk_size=8192):
#                 f.write(chunk)
#
#     # 安装下载的文件
#     print(f"Installing {local_filename}...")
#     subprocess.run(local_filename, shell=True)


if __name__ == '__main__':
    # # 前置检查环境依赖！！！！
    # # 检查 DLL 是否存在
    # dll_check_result = check_dll_exists("api-ms-win-crt-stdio-l1-1-0.dll")
    # # 如果不存在目标DLL，检查是否安装Visual C++ 2015
    # if not dll_check_result:
    #     check_vc_result = check_vc_redist_2015_installed()
    #     # 如果没有安装任意版本的Visual C++ 2015，直接拉去官网的Visual C++ 2015下载并安装
    #     if not check_vc_result:
    #         # 检测系统架构
    #         arch = get_system_architecture()
    #         # 根据架构选择正确的下载链接
    #         download_and_install_vc_redist(arch)

    root = tk.Tk()
    app = Application(root)
    app.choose_devices_mode_page(root)

    # 持续事件监控
    root.mainloop()
    # pass1

