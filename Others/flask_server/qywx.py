#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/6 10:48
# @Author  : Heshouyi
# @File    : qywx.py
# @Software: PyCharm
# @description:

import requests
from flask import Flask, request, jsonify
from common.log_tool import logger
import pymysql

app = Flask(__name__)

# 群消息机器人的webhook
target_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=f2cf09ad-c7c6-4544-85a1-dd4737ee0c5a'
# 默认消息处理人（找不到需要@的人的电话/转单对象是软件中心等情况）
default_transfer_people = "何守一"


@app.route('/cd-autotest/order-message', methods=['POST'])
def transfer_findcar_order_message():
    data = request.get_json()   # 尝试获取有效的json数据
    if not data:
        logger.error('无效的JSON数据')
        return jsonify({"error": "无效的JSON数据"}), 400

    logger.info(f'收到数据：{data}')
    # 使用.get()方法来避免没有数据时的KeyError异常
    text = data.get("text", {}).get("content", "")

    with pymysql.connect(
        host='127.0.0.1',
        port=5831,
        user='root',
        password='Keytop:wabjtam!',
        database='work_order',
        cursorclass=pymysql.cursors.DictCursor,     # 使用字典类型游标
        autocommit=True     # 自动提交事务
    ) as db_connection:

        if text.startswith("以下工单已超1小时未更新"):
            # 处理超时工单提醒
            process_timeout_orders(text, db_connection)
        elif "指派了工单给" in text:
            # 处理指派工单提醒
            process_assigned_orders(text, db_connection)

    return jsonify({"message": "已接收到数据", "data": data}), 200


def process_timeout_orders(text, db_connection):
    """处理超时工单提醒"""
    orders = text.split("工单：")[1:]
    for order in orders:
        if "处理人" in order:
            # 获取处理人
            process_people = order.split("处理人：")[1].split("；")[0]
            message = "工单：" + order
            phonenum = get_phone_number(process_people, db_connection)
            # 如果未找到处理人，则转为@默认处理人
            if not phonenum:
                logger.warning(f"未找到处理人 {process_people}，转为@默认处理人：{default_transfer_people}")
                phonenum = get_phone_number(default_transfer_people, db_connection)
                if not phonenum:
                    logger.error(f"未找到默认处理人 {default_transfer_people} 的电话号码")
                    return
            send_message(message, [phonenum])


def process_assigned_orders(text, db_connection):
    """处理指派工单提醒"""
    logger.info(f"收到指派工单给软件中心，@默认处理人：{default_transfer_people}")
    phonenum = get_phone_number(default_transfer_people, db_connection)
    if not phonenum:
        logger.error(f"未找到默认处理人 {default_transfer_people} 的电话号码")
        return
    send_message(text, [phonenum])


def get_phone_number(name, db_connection):
    """获取处理人对应电话号码"""
    try:
        with db_connection.cursor() as cursor:
            cursor.execute("SELECT phone FROM members WHERE name = %s", (name,))
            result = cursor.fetchone()
            return result['phone'] if result else None
    except pymysql.MySQLError as e:
        logger.error(f"数据库查询失败: {e}")
        return None


def send_message(content, mentioned_mobile_list):
    """转发到企业微信群机器人"""
    payload = {
        "msgtype": "text",
        "text": {
            "content": content,
            "mentioned_list": [],
            "mentioned_mobile_list": mentioned_mobile_list
        }
    }
    try:
        response = requests.post(target_url, json=payload)
        if response.status_code == 200:
            logger.info(f"消息发送成功: {payload}")
        else:
            logger.error(f"消息发送失败: {response.json()}")
    except requests.RequestException as e:
        logger.error(f"请求异常: {e}")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
