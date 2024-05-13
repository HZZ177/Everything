# -*-coding: Utf-8 -*-
# @File : button_envent .py
# author: Heshouyi
# Time：2024/5/14

from Others.adb_tool.utils.utils import Util
from Others.adb_tool.managers.device_function_manager import DeviceManager
from Others.adb_tool.ui.main_window import MainWindow
from tkinter import messagebox


class ButtonEvent:
    """各类按钮绑定事件类"""

    @staticmethod
    def connect_to_other_device(current_frame, root):
        """连接其他设备按钮绑定事件"""
        result = DeviceManager.disconnect_all_device()
        if result.returncode == 0:
            messagebox.showinfo("断开连接", "当前设备已断开连接！请重新输入ip")
        else:
            messagebox.showerror("错误", f"指令执行出错！\n错误信息：{result.stderr}")
        current_frame.pack_forget()
        MainWindow.create_ip_input_page(root)