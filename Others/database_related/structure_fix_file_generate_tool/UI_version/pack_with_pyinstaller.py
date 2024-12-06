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
# script_name = os.path.join(project_path, 'db_struct_fix_tool_by_pyqt5.py')  # pyqt5版本脚本路径(打包出来有点大)
script_name = os.path.join(project_path, 'db_struct_fix_tool_by_tkinter.py')  # tkinter版本主脚本路径
utils_path = os.path.join(project_path, 'utils')     # 数据文件夹路径
app_name = "寻车数据库结构修复工具-V1.0"  # 打包后的应用程序名称


def clean_data_directory(data_path):
    """
    删除目录下所有以 .sql 结尾的文件
    """
    if os.path.exists(data_path):
        for filename in os.listdir(data_path):
            if filename.endswith('.sql'):
                file_path = os.path.join(data_path, filename)
                os.remove(file_path)
                print(f"删除文件: {file_path}")
    else:
        print(f"目录 {data_path} 不存在，跳过清理。")


def pack_and_clean_temp(app_name, script_name):
    """
    使用 PyInstaller 打包给定的 Python 脚本，并在打包完成后清理临时文件。
    app_name: 打包后的应用程序名称
    """
    command = [
        "pyinstaller",
        '--onefile',
        '--windowed',
        '--name', app_name,
        '--add-data', f"{utils_path};utils",
        '--paths', '.',
        script_name
    ]
    try:
        print("开始打包...")
        print("Executing command:", " ".join(command))
        subprocess.run(command, check=True)
        print("打包完成！")
        print("开始清理临时文件...")
        # 清理临时文件
        shutil.rmtree('build')
        spec_file = f"{app_name}.spec"
        if os.path.exists(spec_file):
            os.remove(spec_file)
        print("临时文件清理完成！")
    except subprocess.CalledProcessError:
        print("打包过程中出现错误。")


if __name__ == "__main__":
    # 前置清理步骤
    clean_data_directory(utils_path)
    # 调用函数来执行打包并清理临时文件
    pack_and_clean_temp(app_name, script_name)
