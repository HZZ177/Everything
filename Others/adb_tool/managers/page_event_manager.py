# -*-coding: Utf-8 -*-
# @File : page_event_manager .py
# author: Heshouyi
# Time：2024/5/14

import tkinter as tk
from Others.adb_tool.ui.main_window import MainWindow


class PageEventManager:
    """页面功能类"""
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

    def tab_change_event(self, root, event):
        """标签页切换事件处理函数"""
        selected_tab = event.widget.index(event.widget.select())
        if selected_tab == 0:  # 单设备连接模式
            root.bind("<Return>", self.handle_enter_key_single_device)
        else:  # 多设备批量升级模式
            root.unbind("<Return>")

    def handle_enter_key_single_device(self, event):
        """处理单设备连接模式下的回车键事件"""
        MainWindow.entry_select_function_page(self.entry_ip.get())
