#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/21 10:48
# @Author  : Heshouyi
# @File    : plate_recognition.py
# @Software: PyCharm
# @description: 调用FindCarServer识别库测试接口

from Locust.common.log_tool import logger
import random
from Locust.files.plate_pic_map import plate_map


def identify_plate_randomly(client):
    """调用FindCarServer识别库测试接口，图片存放路径为FindCarServer根目录下图片地址"""

    image_path = random.choice(list(plate_map.keys()))  # 随机选择一张图片
    target_plate = plate_map[image_path]    # 期望车牌号
    target_plate_pure = plate_map[image_path][1:]    # 期望车牌号，去除汉字部分
    target_chinese = plate_map[image_path][0]   # 期望车牌汉字
    result = None
    flag = None
    try:
        result = client.get("/device-access/device/recognitionTest", params={'url': 'pictest/' + image_path})
    except Exception as e:
        logger.error(f"请求失败，报错信息：{e}")
        return

    recognition_plate = result.json()['data']['carPlate']   # 完整识别结果
    if recognition_plate != '':
        recognition_plate_pure = result.json()['data']['carPlate'][2:]   # 识别出的车牌部分，去除汉字和颜色
        recognition_chinese = result.json()['data']['carPlate'][1]  # 识别出的车牌汉字
        if recognition_plate_pure == target_plate_pure:
            flag = 2    # 2=车牌部分符合但汉字不对
            if recognition_chinese == target_chinese:
                flag = 1    # 1=车牌部分和汉字都符合
    else:
        flag = 3    # 3=车牌部分不符合

    return flag, recognition_plate, target_plate
