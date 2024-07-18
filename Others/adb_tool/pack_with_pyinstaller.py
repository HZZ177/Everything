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

project_path = os.getcwd()  # 项目基础路径
extra_tool_path = os.path.join(project_path, 'scrcpy_tool')     # 打包的额外资源文件
main_script_path = os.path.join(project_path, 'main_origin.py')    # 主题代码文件路径
version = "v1.2.3"  # 打包程序名称中的版本号

script_name = main_script_path
app_name = f"ADB-设备调试工具-{version}"


def pack_and_clean_temp(extra_tool_path, app_name):
    """
    使用 PyInstaller 打包给定的 Python 脚本，并在打包完成后清理临时文件。
    app_name: 打包后的应用程序名称
    """
    command = [
        "pyinstaller",
        '--onefile',
        '--windowed',
        '--add-data', f"{extra_tool_path};scrcpy_tool",
        '-n', f"{app_name}",
        "main_origin.py"
    ]
    try:
        print("开始打包...")
        print("Executing command:", " ".join(command))
        subprocess.run(command, check=True)
        print("打包完成！")
        print("开始清理临时文件...")
        # 清理临时文件
        shutil.rmtree('build')
        os.remove(f'{app_name}.spec')
        print("临时文件清理完成！")
    except subprocess.CalledProcessError:
        print("打包过程中出现错误。")


if __name__ == "__main__":
    # 调用函数来执行打包并清理临时文件
    pack_and_clean_temp(extra_tool_path, app_name)
