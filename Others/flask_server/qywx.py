#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/6 10:48
# @Author  : Heshouyi
# @File    : qywx.py
# @Software: PyCharm
# @description:
import re
import requests
from flask import Flask, request, jsonify
from common.log_tool import logger
import pymysql

app = Flask(__name__)
# 群消息机器人的webhook
target_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=f2cf09ad-c7c6-4544-85a1-dd4737ee0c5a'


@app.route('/findcar/receive_message', methods=['POST'])
def findcar_get_message():
    # 获取数据解析为JSON
    data = request.get_json()
    if data is None:  # 如果没有JSON数据
        logger.error('接收到的请求数据不是有效的JSON')
        return jsonify({"error": "无效的JSON数据"}), 400

    logger.info(f'收到数据：{data}')

    # 创建数据库连接
    db_connection = pymysql.connect(
        host='127.0.0.1',
        port=5831,
        user='root',
        password='Keytop:wabjtam!',
        database='work_order',
        cursorclass=pymysql.cursors.DictCursor,     # 以字典形式返回
        autocommit=True  # 自动提交事务
    )

    try:
        # 分离出原信息的"@所有人"
        text = data["text"]["content"].split("@")[0]
        # 分离每条工单提醒
        orders = text.split("工单：")
        for order in orders:
            if "处理人" in order:
                # 组合完整信息和提取处理人
                process_people = order.split("处理人：")[1].split("；")[0]
                # 把之前分离的"工单："拼回去
                message = "工单：" + order

                # 获取处理人的电话号码
                phonenum = get_phone_number(process_people, db_connection)
                if phonenum is None:
                    logger.warning(f"未找到处理人 {process_people} 的电话号码")
                    mentioned_mobile_list = []
                else:
                    mentioned_mobile_list = [phonenum]

                payload = {
                    "msgtype": "text",
                    "text": {
                        "content": message,
                        "mentioned_list": [],
                        "mentioned_mobile_list": mentioned_mobile_list
                    }
                }

                try:
                    response = requests.post(
                        'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=f2cf09ad-c7c6-4544-85a1-dd4737ee0c5a',
                        json=payload
                    )

                    if response.status_code == 200:
                        logger.info(f"成功转发消息: {payload}")
                    else:
                        logger.error(f"转发失败: {response.json()}")
                except requests.RequestException as e:
                    logger.error(f"请求异常: {e}")
    finally:
        # 关闭数据库连接
        db_connection.close()

    return jsonify({"message": "已接收到数据", "data": data}), 200


# 根据处理人查询电话号码
def get_phone_number(process_people, db_connection):
    try:
        with db_connection.cursor() as cursor:
            sql = "SELECT phone FROM members WHERE name = %s"
            cursor.execute(sql, (process_people,))
            result = cursor.fetchone()
            return result['phone'] if result else None
    except pymysql.MySQLError as e:
        logger.error(f"数据库查询失败: {e}")
        return None


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1778)
