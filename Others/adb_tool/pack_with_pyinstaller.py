#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/4/22 17:49
# @Author  : Heshouyi
# @File    : pack_with_pyinstaller.py
# @Software: PyCharm
# @description:

import subprocess
import shutil
import os


def pack_and_clean_temp(script_name, app_name):
    """
    使用 PyInstaller 打包给定的 Python 脚本，并在打包完成后清理临时文件。

    参数：
        script_name: 要打包的 Python 脚本文件名。
        app_name: 打包后的应用程序名称。
    """
    command = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--add-data', f'{script_name};{app_name}',
        '-n', app_name,
        script_name
    ]
    try:
        print("开始打包...")
        subprocess.run(command, check=True)
        print("打包完成！")
        print("开始清理临时文件...")
        # 清理临时文件
        shutil.rmtree('build')
        os.remove(f'{app_name}.spec')
        print("临时文件清理完成！")
    except subprocess.CalledProcessError:
        print("打包过程中出现错误。")


# 调用函数来执行打包并清理临时文件
pack_and_clean_temp(
    r'C:\Users\86364\PycharmProjects\everything\Others\adb_tool\scrcpy_tool\main.py',
    'adb设备调试工具V1.2.0'
)