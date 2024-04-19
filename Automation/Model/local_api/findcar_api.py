#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/1/29 11:13
# @Author  : Heshouyi
# @File    : findcar_api.py
# @Software: PyCharm
# @description:


import requests
from Automation.Utils.tools import get_uuid

host = "http://192.168.25.250:7072/"
route = {
    "get_all_screen_address": "screen/getAllTcpAddr",
    "car_in": "park/enter",
    "update_plate_no": "park/updatePlateNo",
    "car_leave": "/park/leave",
    "floor_insert": "floorInfo/insert",
    "floor_update": "floorInfo/update",

}


def get_all_tcp_addr():
    """
    获取当前系统所有tcp屏幕地址
    :return:
    """
    url = host+route["get_all_screen_address"]
    reqid = get_uuid()
    body = {
        "reqId": reqid
    }
    response = requests.post(url, json=body)
    if response.status_code == 200:
        data = response.json()
        # print(data)
        print("查询所有屏地址接口返回:", data)
    else:
        print("接口请求失败，接口返回状态:", response.status_code)


def car_in(*args):
    """
    指定车位，进行入车
    :param args:
    :return:
    """
    target_list = []
    for i in args:
        target_list.append(i)
    url = host+route["car_in"]
    reqid = get_uuid()
    body = {
        "list": target_list,
        "reqId": reqid
    }
    response = requests.post(url, json=body)
    data = response.json()
    if response.status_code == 200:
        print("入车接口请求成功，返回信息:", data)
    else:
        print("入车接口请求失败，响应代码:", response.status_code)


def car_leave(*args):
    """
    指定车位，进行出车
    :param args:
    :return:
    """
    target_list = []
    for i in args:
        target_list.append(i)
    url = host+route["car_leave"]
    reqid = get_uuid()
    body = {
        "list": target_list,
        "reqId": reqid
    }
    response = requests.post(url, json=body)
    data = response.json()
    if response.status_code == 200:
        print("出车接口请求成功，返回信息:", data)
    else:
        print("出车接口请求失败，响应代码:", response.status_code)


def update_plate_no(*, carlist, plateno=""):
    """
    指定车位，更新车牌
    :param carlist:
    :param plateno:
    :return:
    """
    url = host+route["update_plate_no"]
    reqid = get_uuid()
    update_list = []
    for i in range(len(carlist)):
        body_list = {
            "addr": carlist[i],
            "carImageUrl": "/home/findcar/FindCarServer/recognition/20231123/2523601/09/2523601_20231123092540.jpg",
            "plateNo": plateno,
            "plateNoReliability": 720
        }
        update_list.append(body_list)
    body = {
        "list": update_list,
        "reqId": reqid
    }
    response = requests.post(url, json=body)
    data = response.json()
    if response.status_code == 200:
        print("车牌更新接口请求成功，返回信息:", data)
    else:
        print("车牌更新接口请求失败，响应代码:", response.status_code)


def login(url, header, params):
    """
    使用selenium打开页面后获取的jsessionid和验证码，调用登录接口，获取时效性token
    :param url: 登录接口地址
    :param header:请求头
    :param params:请求参数
    :return:响应参数的json格式
    """
    result = requests.get(url, headers=header, params=params)
    # print(result)
    message = result.json()
    # print(message)
    return message


if __name__ == "__main__":
    pass
    # url = file_paths.environment229_page
    # username = super_admin["username"]
    # password = super_admin["password"]
    # driver = LogInTool.LogInTool(url, username, password)
    # driver.open_web()
    # JSESSIONID = driver.get_jsessionid()
    # verify_code = driver.get_picture_num_by_baidu_ocr()
    # header = {
    #     "Cookie": f"JSESSIONID={JSESSIONID}"
    # }
    # params = {
    #     "account": f"{'admin@keytop.com'}",
    #     "password": f"{encrypt_password(message='keytop123456')}",
    #     "verifyCode": f"{verify_code}"
    # }
    # login(url, header, params)
