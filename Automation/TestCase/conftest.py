#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/2/8 15:36
# @Author  : Heshouyi
# @File    : conftest.py
# @Software: PyCharm
# @description:

from Automation.Model.local_api import findcar_api
from Automation.Files import file_paths
from findcar_auto.common import login_tool
from Automation.Utils.accounts import super_admin
from findcar_auto.common.encrypt import encrypt_password
import pytest


@pytest.fixture(scope="session")
def login_info():
    """
    定义超级管理员权限的账号和登录地址，传参给setup调用
    :return:
    """
    get_param_page = file_paths.environment229_page  # 定义获取参数路径（网页）
    login_target = file_paths.environment229_login  # 定义登录路径（接口）
    account = super_admin
    return get_param_page, login_target, account


@pytest.fixture(scope="session")
def setup(login_info):
    """
    前置处理，通过selenium打开登录界面拿到关联的参数，之后通过接口登录获取返回的时效性token
    :param login_info:
    :return:
    """
    print("================================正在进行前置处理，获取token===========================")
    get_param_page, login_target, account = login_info
    # 解析传入的用户名密码
    username = account['username']
    password = account['password']
    count = 0
    while count <= 3:  # 一直重试直到使用验证码登录成功，重试次数上限为三次
        # 获取jsessionid和验证码，添加到header和请求参数中
        log_info = login_tool.get_login_info(get_param_page, username, password)
        jsessionid = log_info["jsessionid"]
        verify_code = log_info["verify_code"]
        # 定义请求头
        header = {
            "Cookie": f"JSESSIONID={jsessionid}"
        }
        # 定义请求参数
        params = {
            "account": f"{username}",
            "password": f"{encrypt_password(message=password)}",
            "verifyCode": f"{verify_code}"
        }
        # 返回消息为登录后拿到的响应
        print("正在使用识别出的验证码登陆中......")
        response = findcar_api.login(url=login_target, header=header, params=params)
        message = response['message']
        if message == "成功":
            print("登录成功！正在获取token......")
            token = response['data']['token']
            print("Token获取成功！")
            print("==========================前置处理完成，成功获取token=======================")
            return token
        elif message == "验证码错误":
            count += 1
            print(f"验证码输入错误，正在进行第{count}次重试，获取登录参数")
        else:
            count += 1
            print(f"发生未知错误，正在进行第{count}次重试，获取登录参数")
        if count == 4:
            raise Exception("使用获取参数调用登录接口重试3次后依然失败，请检查！！！")
