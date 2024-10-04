#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/30 18:26
# @Author  : Heshouyi
# @File    : pack_with_pyinstaller.py
# @Software: PyCharm
# @description:
import subprocess
import shutil
import os

version = "v1.0"  # 版本号

# 项目基础路径
project_path = os.getcwd()
# 主程序文件路径
main_script_path = os.path.join(project_path, 'main.py')
# 打包后的应用程序名称
app_name = f"TCP设备指令模拟工具-{version}"


def pack_and_clean_temp(app_name):
    """
    使用 PyInstaller 打包 TCPClientApp 项目，并在打包完成后清理临时文件。
    app_name: 打包后的应用程序名称
    """
    # PyInstaller 命令
    command = [
        "pyinstaller",
        '--onefile',  # 打包成一个独立的可执行文件
        '--windowed',  # 不显示控制台窗口（适用于 GUI 应用程序）
        '-n', f"{app_name}",  # 指定生成的应用程序名称
        '--add-data', '"lora_node_device_page.py;." '
        '--add-data', '"other_device_page.py;." '
        '--add-data', '"tcp_client.py;." '
        '--add-data', '"utils.py;." '
        '--hidden-import=tkinter',
        '--hidden-import=tkinter.messagebox',
        '--hidden-import=tkinter.ttk',
        'main.py'  # 主程序入口文件
    ]

    try:
        print("开始打包...")
        print("执行打包命令:", " ".join(command))
        # 执行打包命令
        subprocess.run(" ".join(command), check=True)
        print("打包完成！")
    except subprocess.CalledProcessError:
        print("打包过程中出现错误")
    finally:
        print("开始清理临时文件...")
        # 清理临时文件
        if os.path.exists('build'):
            shutil.rmtree('build')
        spec_file = f'{app_name}.spec'
        if os.path.exists(spec_file):
            os.remove(spec_file)
        print("临时文件清理完成！")


if __name__ == "__main__":
    # 执行打包和清理过程
    pack_and_clean_temp(app_name)
