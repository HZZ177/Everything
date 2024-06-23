# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
===================================
@FileName: wechat_robot.py
@Description: 企业微信机器人
@Author: wangmengzhou
@Software: PyCharm
@Version: 1.0
@Update:
@Copyright:
@time:2022/11/15 11:46
===================================
"""
import datetime

import requests
from common import filepath
from common.configLog import logger

robot_key = filepath.config.get("auto_city_wx").get("robot_key")


class WeChatRobot:
    def __init__(self, robot_key):
        robot_curl = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={robot_key}"
        update_url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={robot_key}&type=file"
        self.robot_curl = robot_curl
        self.upload_url = update_url

    def upload_file(self, file_path: str) -> str:
        """
        企业微信机器人上传文件，发送文件前需要现上传
        :param file_path: 文件路径
        :return:
        """
        try:
            data = {'file': open(file_path, 'rb')}
            resp = requests.post(self.upload_url, files=data)
            json_res = resp.json()
            if json_res.get('media_id'):
                logger.info(f"企业微信机器人上传文件成功，file:{file_path}")
                return json_res.get('media_id')
        except Exception:
            logger.exception(f"企业微信机器人上传文件失败，file: {file_path}")
            return ""

    def send_file(self, file_path: str):
        """
        企业微信机器人发送文件，例如：report.html
        :param file_path: 文件路径
        :return:
        """
        try:
            headers = {
                "Content-Type": "application/json"
            }

            data = {
                "msgtype": "file",
                "file": {
                    "media_id": self.upload_file(file_path)
                }
            }
            resp = requests.post(url=self.robot_curl, headers=headers, json=data)
            logger.info(f"企业微信机器人发送文件：req_json: {data}\n"
                        f"response: {resp.text}")
        except Exception:
            logger.exception(f"企业微信机器人发送文件失败，req_json: {data}")

    def send_message(self, content, message_type="text"):
        """
        企业微信机器人发送消息
        :return:
        """
        try:
            headers = {
                "Content-Type": "application/json"
            }

            data = {
                "msgtype": message_type,
                message_type: {
                    "content": content
                }
            }
            resp = requests.post(url=self.robot_curl, headers=headers, json=data)
            logger.info(f"企业微信机器人发送消息，req_json: {data}\n"
                        f"response: {resp.text}")
        except Exception:
            logger.exception(f"企业微信机器人发送消息失败，req_json: {data}")


robot = WeChatRobot(robot_key)

if __name__ == '__main__':
    # file_suffix = "lot_label_result.csv"
    # file_path = filepath.fetch_path_by_now_day(REPORT_PATH, file_suffix)
    # robot.send_file(file_path)
    year = datetime.datetime.now().strftime("%Y")
    month = datetime.datetime.now().strftime("%m")
    day = datetime.datetime.now().strftime("%d")
    column_name_list = ["省份ID", "城市ID"]
    # 每日定时任务有异常
    # content = f"{year}年{month}月{day}日 车场标签自动化测试结果："
    # 每日定时任务无异常
    content = f"{year}年{month}月{day}日 车场标签自动化测试无异常"
    # 平台任务有异常
    # content = f"{year}年{month}月{day}日 "
    # for column_name in column_name_list:
    #     content = content + f"【{column_name}】"
    # content = content + "自动化测试结果:"
    # 平台任务无异常
    # content = f"{year}年{month}月{day}日 "
    # for column_name in column_name_list:
    #     content = content + f"【{column_name}】"
    # content = content + "自动化测试无异常"
    # print(content)
    robot.send_message(content)
