#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/2 上午5:13
# @Author  : Heshouyi
# @File    : login_tool.py
# @Software: PyCharm
# @description: 登录工具

import os
import json
import base64
import requests
from findcar_auto.common.log_tool import logger
from findcar_auto.common import file_path
from findcar_auto.common import baidu_ocr_api
from findcar_auto.common.config_loader import configger
from findcar_auto.model.findCarApi import findCar_admin_api

config = configger.load_config()


class LogInToolTest:
    def __init__(self):
        # 设定保存验证码图片目录
        self.save_path = rf'{file_path.verify_picture_path}\verify_code.png'
        # 验证码图片的response对象
        self.verify_response = None

    def get_picture_num_by_baidu_ocr(self):
        """
        调用百度ocr接口，识别图片中的内容
        :return: 识别结果
        """
        # 获取百度OCR的access token
        token = baidu_ocr_api.fetch_token()
        # 拼接通用文字识别高精度url
        image_url = baidu_ocr_api.OCR_URL + "?access_token=" + token
        text = ""
        # 读取验证码图片
        file_content = baidu_ocr_api.read_file(self.save_path)
        # 调用文字识别服务
        result = baidu_ocr_api.request(image_url, baidu_ocr_api.urlencode({'image': base64.b64encode(file_content)}))
        # 解析返回结果
        result_json = json.loads(result)
        # 取出返回体中的识别结果value
        for words_result in result_json["words_result"]:
            text = text + words_result["words"]
        logger.info(f"百度ocr识别结果：{text}")
        return text

    def get_verify_pic(self):
        """
        通过接口获取验证码图片的二进制文件，写入为png图片
        :return:
        """
        # 发送 GET 请求获取图片二进制码
        logger.info("正在获取验证码图片")
        self.verify_response = findCar_admin_api.get_verifycode()

        # 获取验证码图片二进制，写入文件
        if self.verify_response.status_code == 200:
            # 打开本地文件，用于写入二进制数据
            with open(f'{self.save_path}', 'wb') as file:
                file.write(self.verify_response.content)
            logger.info(f"成功获取验证码图片，保存在{self.save_path}")

    def get_jsessionid(self):
        """
        获取接口响应头中，set-cookie的jsessionid
        :return:
        """
        cookies = self.verify_response.headers.get('Set-Cookie')
        if cookies:
            for cookie in cookies.split(';'):
                if 'JSESSIONID' in cookie:
                    jsessionid = cookie.split('=')[1]
                    logger.info(f"成功获取JSESSIONID: {jsessionid}")
                    return jsessionid
                else:
                    logger.info("header中没有JSESSIONID信息，请检查")
        else:
            logger.info(f'接口返回中没有cookie，请检查')

    def get_verify_code(self):
        """
        尝试通过百度ocr识别验证码，每个验证码的返回结果格式容错三次
        :return:
        """
        count = 0  # 重试次数
        while True:
            self.get_verify_pic()    # 获取验证码图片
            logger.info("正在调用百度ocr识别验证码")
            verify_code = self.get_picture_num_by_baidu_ocr()    # 获取ocr识别结果
            if len(verify_code) == 4:
                is_digit = 1    # 标识ocr识别验证码中是否全部为正整数
                for i in verify_code:
                    if not i.isdigit():
                        is_digit = 0
                if is_digit == 0:
                    count += 1
                    logger.info(f"验证码中存在非正整数，即将进行第{count}次重新识别")
                else:
                    return verify_code
            elif count == 3:  # 识别重试三次之后仍然获取不到格式正确的识别结果，返回失败
                logger.error("==============百度ocr识别已失败三次，请检查==============")
                raise Exception
            else:  # 如果在重试次数消耗完之前，返回识别结果不是4位数，重新打开页面，获取图片并识别
                count += 1
                logger.info(f"验证码'{verify_code}'识别结果不是四位数，即将进行第{count}次重新识别")

    def get_verifycode_and_jsessionid(self):
        """
        获取验证码和与其绑定的jsessionid，用于登录获取token
        :return: verify_code, jsessionid
        """
        verify_code = self.get_verify_code()
        jsessionid = self.get_jsessionid()
        return verify_code, jsessionid


if __name__ == "__main__":
    # app = LogInToolTest()
    # app.get_verifycode_and_jsessionid()
    pass
