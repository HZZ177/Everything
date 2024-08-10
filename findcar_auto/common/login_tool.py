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
from loguru import logger
from bs4 import BeautifulSoup
from findcar_auto.common import file_path
from findcar_auto.common import baidu_ocr_api
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.edge.options import Options


class VerificationCodeError(Exception):
    """验证码类型异常"""
    pass


class LogInTool:
    def __init__(self, url, username, password):
        self.edge_option = Options()
        self.edge_option.add_argument("--headless")  # 无头模式
        self.driver = webdriver.Edge(options=self.edge_option)
        self.driver.implicitly_wait(10)
        self.url = url
        self.username = username
        self.password = password
        # 设定保存验证码图片目录
        self.save_path = rf'{file_path.verify_picture_path}\verify_code.png'

    def open_web(self):
        # 打开网页
        self.driver.get(self.url)

    def get_jsessionid(self):
        """
        进入登录页面后，页面上获取后端框架提供的jsessionid，用来和验证码做绑定
        :return:jsessionid
        """
        # 以验证码图片加载成功为标志，继续进行后面的操作
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "h-full")))
        if element:
            cookies = self.driver.get_cookies()
            jsessionid = [cookie["value"] for cookie in cookies if cookie["name"] == "JSESSIONID"][0]
            return jsessionid
        else:
            logger.error("获取jsessionid时，页面加载出现未知异常，10秒内捕获验证码图片失败，请检查！")
            return

    def get_picture_src(self):
        """
        获取图片源链接（图片标签中的src地址）
        :return: src
        """
        # 通过驱动打开网页获取源码，解析方式为html.parser
        html = BeautifulSoup(self.driver.page_source, "html.parser")
        # 定位class为h-full的标签，即为验证码图片
        tag = html.find(class_="h-full")
        # 通过标签定位src链接
        src = tag["src"]
        return src

    def get_picture(self):
        """
        获取验证码图片，方便调用百度OCR识别
        :return:
        """
        # 定位验证码图片
        wait = WebDriverWait(self.driver, 5)
        try:
            picture_element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "h-full")))
            # logger.info(f"保存路径: {self.save_path}")

            # 检查路径是否存在，不存在则创建
            save_dir = os.path.dirname(self.save_path)
            if not os.path.exists(save_dir):
                logger.info(f"路径不存在，创建路径: {save_dir}")
                os.makedirs(save_dir)

            result = picture_element.screenshot(self.save_path)
            if result:
                logger.info(f"成功获取验证码图片，保存在{self.save_path}")
            else:
                logger.info("验证码图片保存失败，请检查路径和写权限")
                raise VerificationCodeError("验证码图片保存失败")
        except Exception as e:
            logger.error("获取验证码图片过程中发生错误", exc_info=True)
            raise VerificationCodeError from e

    def get_picture_num_by_baidu_ocr(self):
        # 定位并截图保存验证码图片
        self.get_picture()
        # 获取百度OCR的access token
        token = baidu_ocr_api.fetch_token()
        # 拼接通用文字识别高精度url
        image_url = baidu_ocr_api.OCR_URL + "?access_token=" + token
        text = ""
        # print(self.save_path)
        # 读取测试图片
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

    def login(self):
        """
        直接通过页面模拟点击输入，登录管理后台页面（此方法拿不到token）
        :return:
        """
        self.open_web()
        # 调用百度ocr识别验证码图片
        verify_code = self.get_picture_num_by_baidu_ocr()
        # 输入登录参数，点击登录
        self.driver.find_element(By.XPATH, "//input[@placeholder = '请输入用户名']").send_keys(self.username)
        self.driver.find_element(By.XPATH, "//input[@placeholder = '请输入密码']").send_keys(self.password)
        self.driver.find_element(By.XPATH, "//input[@placeholder = '请输入验证码']").send_keys(verify_code)
        self.driver.find_element(By.XPATH, "//span[text() = '登 录']").click()


def get_login_info(url, username, password):
    """
    通过selenium打开登录界面，获取调用登录接口所需的所有参数
    :param url: 指定打开登录网页地址
    :param username: 要使用的用户名
    :param password: 要使用的密码
    :return: 带有jsessionid和verify_code的一个字典
    """
    driver = LogInTool(url, username, password)
    count = 0   # 定义最大重试次数
    while True:
        driver.open_web()
        logger.info("成功打开登录页面，开始获取验证码图片")
        jsessionid = driver.get_jsessionid()
        verify_code = driver.get_picture_num_by_baidu_ocr()
        if len(verify_code) == 4:   # 如果验证码识别位数为4，则判断是否含有非正整数
            # 标识是否ocr识别验证码中全部为正整数
            is_digit = 1
            for i in verify_code:
                if not i.isdigit():
                    is_digit = 0
            if is_digit == 0:
                count += 1
                logger.info(f"验证码中存在非正整数，即将进行第{count}次重试")
            else:
                result = {
                    "jsessionid": jsessionid,
                    "verify_code": verify_code
                }
                return result
        elif count == 3:    # 识别重试三次之后仍然获取不到四位数的识别结果，返回失败信息，手动检查
            driver.driver.close()   # 关闭浏览器
            logger.error("==============百度ocr识别已失败三次，请检查==============")
            raise Exception
        else:  # 如果在重试次数消耗完之前，返回识别结果不是4位数，重新打开页面，获取图片并识别
            count += 1
            logger.info(f"验证码'{verify_code}'识别结果不是四位数，即将进行第{count}次重试")


if __name__ == "__main__":
    pass

    # username = super_admin['username']
    # password = super_admin['password']
    # tool = LogInTool(file_paths.environment229_page, username, password)
    # tool.open_web()

    # get_login_info(file_paths.environment229_page, username, password)
