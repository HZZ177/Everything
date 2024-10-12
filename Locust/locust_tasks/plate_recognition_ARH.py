#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/21 10:48
# @Author  : Heshouyi
# @File    : plate_recognition.py
# @Software: PyCharm
# @description: 调用加纳第三方库识别车牌号
import requests

from Locust.common.log_tool import logger
import random
from Locust.files.plate_pic_map import chinese_plate_map


def identify_plate_randomly(client):
    """调用FindCarServer识别库测试接口，图片存放路径为FindCarServer根目录下图片地址"""

    image_path = random.choice(list(chinese_plate_map.keys()))  # 随机选择一张图片
    target_plate = chinese_plate_map[image_path]    # 期望车牌号
    target_plate_pure = chinese_plate_map[image_path][1:]    # 期望车牌号，去除汉字部分
    target_chinese = chinese_plate_map[image_path][0]   # 期望车牌汉字
    result = None
    flag = None
    result = client.get("/device-access/tool/thirdRecognition",
                        params={'imgPath': '/home/findcar/FindCarServer/recognitionTest/pictest/' + image_path})
    # print(f'调试信息：, {result.json()}, {image_path}')
    # 判断是否返回码200
    if result.status_code != 200:
        logger.error(f"调用识别库测试接口失败，接口返回：{result.text}")
        return None, None, None
    elif result.json()['message'] != '成功':
        logger.error(f'调用识别库测试接口报错，详情：{result.json()}')
        return None, None, None
    elif result.json()['data']['plate'] is None:
        logger.warning(f'调用识别库识别结果为空，详情：{result.json()}')
        return None, None, target_plate
    else:
        recognition_plate = result.json()['data']['plate']   # 车牌识别结果
        if recognition_plate != '':
            recognition_plate_pure = result.json()['data']['plate'][1:]   # 识别出的车牌部分，去除汉字和颜色
            recognition_chinese = result.json()['data']['plate'][0]  # 识别出的车牌汉字
            if recognition_plate_pure == target_plate_pure:
                flag = 2    # 2=车牌部分符合但汉字不对
                if recognition_chinese == target_chinese:
                    flag = 1    # 1=车牌部分和汉字都符合
        else:
            flag = 3    # 3=车牌部分不符合
        # print(f'调试：{recognition_plate}, {target_plate}')
        return flag, recognition_plate, target_plate


if __name__ == '__main__':
    host = '192.168.24.199'
    image_path = random.choice(list(chinese_plate_map.keys()))
    result = requests.get(f"http://{host}:8080/device-access/tool/thirdRecognition",
                          params={'imgPath': '/home/findcar/FindCarServer/recognitionTest/pictest/' + image_path})
    print(f'image_path:{image_path}')
    print(result.json())
