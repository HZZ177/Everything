# -*-coding: Utf-8 -*-
# @File : button_envent .py
# author: Heshouyi
# Time：2024/5/14

from Others.adb_tool.utils.utils import Util
from Others.adb_tool.managers.device_function_manager import DeviceManager
from Others.adb_tool.ui.main_window import MainWindow
from tkinter import messagebox
import tkinter as tk


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

        MainWindow.create_ip_input_page()

    def connect_device_async(self, ip, ip_record, button, remind_label):
        """异步连接设备"""
        result = DeviceManager.connect_device(ip)
        remind_label.destroy()  # 取消提示标签

        # 在连接结果返回后恢复连接设备按钮为可点击状态
        button.config(state=tk.NORMAL)

        if "connected" in result.stdout:
            if ip not in ip_record:
                ip_record.insert(0, ip)   # 添加校验通过的ip到历史列表
            self.main_frame.pack_forget()  # 隐藏主连接界面
            root.title(f"ADB-设备调试工具{self.version}===当前连接设备：{ip}")
            # 如果成功连接设备，显示后续控制面板界面
            self.show_control_panel()
        elif isinstance(result, subprocess.TimeoutExpired):
            messagebox.showerror("连接超时", "连接超时，请检查设备是否在线或IP地址是否正确")
        elif isinstance(result, subprocess.CalledProcessError):
            messagebox.showerror("连接错误", "连接错误：命令执行失败，状态码 {}\n错误信息：{}".format(result.returncode, result.stderr))
        else:
            messagebox.showerror("连接失败", f"连接失败，请检查IP地址并重试\n报错信息:\n{result.stdout}")