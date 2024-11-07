#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/6 10:59
# @Author  : Heshouyi
# @File    : test.py
# @Software: PyCharm
# @description:

import requests


def message_test():
    message = {
        "msgtype": "text",
        "text": {
            "content": "以下工单已超1小时未更新，请及时处理（共5单）：工单：20241106X11649；速泊车场：福星惠誉东湖城K2停车场；接收：11-06 17:12；处理人：何守一；已超时：17.8小时；问题优先级：P3工单：20241106S85517；速泊车场：润超停车场；接收：11-07 09:39；处理人：黄倩；已超时：3.4小时；问题优先级：P3@所有人  ",
            # "content": "123",
            "mentioned_list": [],
            "mentioned_mobile_list": []
        }
    }
    response = requests.post('http://127.0.0.1:1778/findcar/receive_message', json=message)
    # response = requests.post('https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=f2cf09ad-c7c6-4544-85a1-dd4737ee0c5a', json=message)

    print(f"接收到返回状态码：{response.status_code}")
    print(f"接收到返回信息：{response.json()}")


if __name__ == '__main__':
    message_test()
