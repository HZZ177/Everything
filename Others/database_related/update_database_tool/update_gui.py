#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/14 下午12:51
# @Author  : Heshouyi
# @File    : update_gui.py
# @Software: PyCharm
# @description:
import datetime
import os
import sys
import threading
import tkinter as tk
import parking_guidance_update_tool


class Application:
    def __init__(self, base_root):

        # 初始化窗口
        self.root = base_root
        self.root.title("2.0版本3D寻车服务器升级工具")

        # 升级工具对象实例化
        self.update_tool = None     # 负责实现升级的逻辑功能

        # 页面初始化
        self.basic_frame = None     # 基础页面，输入数据库信息
        self.processing_frame = None    # 升级过程页面，显示升级过程

        # 页面组件初始化
        self.old_host_entry = None
        self.old_name_entry = None
        self.old_user_entry = None
        self.old_password_entry = None
        self.new_host_entry = None
        self.new_name_entry = None
        self.new_user_entry = None
        self.new_password_entry = None

        self.log_text = None        # 日志文本框

        # 参数初始化
        self.old_db_host = None
        self.old_db_name = None
        self.old_db_user = None
        self.old_db_password = None
        self.new_db_host = None
        self.new_db_name = None
        self.new_db_user = None
        self.new_db_password = None

        # 路径参数定义
        # 获取项目路径，兼容打包后的临时路径
        if getattr(sys, 'frozen', False):
            # 如果应用程序是被打包成可执行文件
            self.project_path = sys._MEIPASS  # 解压后的临时路径
            self.exe_path = os.path.dirname(sys.executable)  # exe本体所在路径
        else:
            # 如果应用程序直接运行
            self.project_path = os.path.dirname(os.path.abspath(__file__))  # 解压后的临时路径
            self.exe_path = os.path.dirname(os.path.abspath(__file__))

        # 日志存放路径
        self.log_file_path = os.path.join(self.exe_path, 'Update_logs')     # 保存日志路径

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

    def create_main_frame(self):
        # 清除跟页面所有组件
        for widget in self.root.winfo_children():
            widget.destroy()

        # 设置列和行的权重，以便内容居中
        for i in range(3):
            self.root.grid_columnconfigure(i, weight=1)
        for i in range(4):
            self.root.grid_rowconfigure(i, weight=1)

        # 新建一个页面用于放置输入框和信息
        self.basic_frame = tk.Frame(self.root)
        self.basic_frame.pack()

        # 旧服务器提示文字标签
        tk.Label(self.basic_frame, text="旧数据库配置:").grid(row=1, column=0, padx=20, pady=10, sticky='w')
        tk.Label(self.basic_frame, text="        数据库IP:").grid(row=2, column=0, padx=20, pady=10, sticky='w')
        tk.Label(self.basic_frame, text="        数据库名:").grid(row=3, column=0, padx=20, pady=10, sticky='w')
        tk.Label(self.basic_frame, text="        数据库账号:").grid(row=4, column=0, padx=20, pady=10, sticky='w')
        tk.Label(self.basic_frame, text="        数据库密码:").grid(row=5, column=0, padx=20, pady=10, sticky='w')
        # 旧服务器输入框以及默认值定义
        self.old_host_entry = tk.Entry(self.basic_frame)
        self.old_host_entry.insert(0, "")
        self.old_name_entry = tk.Entry(self.basic_frame)
        self.old_name_entry.insert(0, "parking_guidance")
        self.old_user_entry = tk.Entry(self.basic_frame)
        self.old_user_entry.insert(0, "root")
        self.old_password_entry = tk.Entry(self.basic_frame, show='*')
        self.old_password_entry.insert(0, "Keytop:wabjtam!")
        # 旧服务器输入框布局定义
        self.old_host_entry.grid(row=2, column=1, padx=20, pady=10)
        self.old_name_entry.grid(row=3, column=1, padx=20, pady=10)
        self.old_user_entry.grid(row=4, column=1, padx=20, pady=10)
        self.old_password_entry.grid(row=5, column=1, padx=20, pady=10)

        # 新服务器提示文字标签
        tk.Label(self.basic_frame, text="新数据库配置:").grid(row=6, column=0, padx=20, pady=10, sticky='w')
        tk.Label(self.basic_frame, text="        数据库IP:").grid(row=7, column=0, padx=20, pady=10, sticky='w')
        tk.Label(self.basic_frame, text="        数据库名:").grid(row=8, column=0, padx=20, pady=10, sticky='w')
        tk.Label(self.basic_frame, text="        数据库账号:").grid(row=9, column=0, padx=20, pady=10, sticky='w')
        tk.Label(self.basic_frame, text="        数据库密码:").grid(row=10, column=0, padx=20, pady=10, sticky='w')
        # 新服务器输入框以及默认值定义
        self.new_host_entry = tk.Entry(self.basic_frame)
        self.new_host_entry.insert(0, "172.20.10.254")
        self.new_name_entry = tk.Entry(self.basic_frame)
        self.new_name_entry.insert(0, "parking_guidance")
        self.new_user_entry = tk.Entry(self.basic_frame)
        self.new_user_entry.insert(0, "root")
        self.new_password_entry = tk.Entry(self.basic_frame, show="*")
        self.new_password_entry.insert(0, "Keytop:wabjtam!")
        # 新服务器输入框布局定义
        self.new_host_entry.grid(row=7, column=1, padx=20, pady=10)
        self.new_name_entry.grid(row=8, column=1, padx=20, pady=10)
        self.new_user_entry.grid(row=9, column=1, padx=20, pady=10)
        self.new_password_entry.grid(row=10, column=1, padx=20, pady=10)

        start_bt = tk.Button(self.basic_frame, text='数据库一键升级', command=lambda: self.transport_frame(self.root))
        start_bt.grid(row=12, column=0, columnspan=3, pady=20)

        self.center_window(self.root, 2, 12)

    def start_transfer(self, log_callback):
        """
        调用update_database方法进行升级
        :param log_callback:
        :return:
        """
        self.update_tool = parking_guidance_update_tool.UpdateDatabase(
                                          old_db_host=self.old_db_host, new_db_host=self.new_db_host,
                                          old_db_name=self.old_db_name, new_db_name=self.new_db_name,
                                          old_db_user=self.old_db_user, new_db_user=self.new_db_user,
                                          old_db_password=self.old_db_password, new_db_password=self.new_db_password)
        self.update_tool.update_database(log_callback)
        # 升级完成后把当前文本框内的所有内容写入到日志文件中
        os.makedirs(self.log_file_path, exist_ok=True)
        current_log_day = datetime.datetime.now().strftime("%Y-%m-%d")
        with open(f"{self.log_file_path}\\{current_log_day}.txt", "a", encoding="utf-8") as log_file:
            log_file.write(self.log_text.get("1.0", tk.END))

    def transport_frame(self, previous_root):
        # 获取主页输入的各种数据库参数，下一步销毁之后就拿不到了
        self.old_db_host = self.old_host_entry.get()
        self.old_db_name = self.old_name_entry.get()
        self.old_db_user = self.old_user_entry.get()
        self.old_db_password = self.old_password_entry.get()
        self.new_db_host = self.new_host_entry.get()
        self.new_db_user = self.new_user_entry.get()
        self.new_db_name = self.new_name_entry.get()
        self.new_db_password = self.new_password_entry.get()

        # 清除主页面所有组件并重新居中
        for widget in previous_root.winfo_children():
            widget.destroy()

        # 创建一个新的页面用于显示传输过程
        self.processing_frame = tk.Frame(self.root)
        self.processing_frame.pack(padx=20, pady=20)

        processing_label = tk.Label(self.processing_frame, text="数据库传输中，请耐心等待...")
        processing_label.pack(side=tk.TOP, pady=20)

        # 创建一个带滚动条的文本框用来展示执行升级过程中的日志信息
        scrollbar = tk.Scrollbar(self.processing_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text = tk.Text(self.processing_frame, yscrollcommand=scrollbar.set)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.log_text.yview)

        # 创建一个按钮用于返回主页面
        back_bt = tk.Button(self.root, text='返回主页面', command=lambda: self.create_main_frame())
        back_bt.pack(side=tk.BOTTOM, padx=20, pady=20)

        # 定义一个日志回调函数，将日志信息写入log_text
        def log_callback(message):
            self.log_text.insert(tk.END, message + '\n')
            self.log_text.see(tk.END)

        # 新开一个现场开始执行升级，并设置为守护线程，防止UI无响应
        update_thread = threading.Thread(target=self.start_transfer, args=(log_callback,))
        update_thread.daemon = True
        update_thread.start()


if __name__ == '__main__':

    # 创建GUI界面
    root = tk.Tk()
    app = Application(root)
    app.center_window(root, 2)
    app.create_main_frame()

    root.mainloop()
