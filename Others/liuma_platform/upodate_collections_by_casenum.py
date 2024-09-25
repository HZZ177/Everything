#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/25 16:36
# @Author  : Heshouyi
# @File    : upodate_collections_by_casenum.py
# @Software: PyCharm
# @description:

import json
import uuid

import pymysql
import requests


class App:

    def __init__(self):

        # 数据库配置
        self.db_config = {
            'host': '101.227.53.213',
            'user': 'root',
            'password': 'K#2dOho@Dgts',
            'port': 3306,
            'database': 'liuma'
        }
        self.conn = self.connect_db()

    def connect_db(self):
        try:
            return pymysql.connect(**self.db_config)
        except Exception as e:
            print(f"连接数据库失败，错误信息: {e}")
            return None

    def select_case_info_by_num(self, case_num_list, case_id_list, case_name_list, module_name_list):
        with self.conn.cursor() as cursor:
            for case_num in case_num_list:
                cursor.execute("SELECT id,name,module_id FROM `case` WHERE num = %s", (case_num,))
                result = cursor.fetchone()
                if result is not None:
                    # 通过module_id查询对应module名称
                    cursor.execute("SELECT name FROM `case_module` WHERE id = %s", (result[2],))
                    module_name = cursor.fetchone()[0]
                    case_id_list.append(result[0])
                    case_name_list.append(result[1])
                    module_name_list.append(module_name)
        print(case_id_list, case_name_list, module_name_list)

    @staticmethod
    def get_collection_detail_byid(token, collection_id):

        url = f'https://cdautotest.keytop.cn/autotest/platform/collection/detail/{collection_id}'
        headers = {'token': token}

        result = requests.get(url=url, headers=headers)
        try:
            json_result = result.json()
            formatted_json = json.dumps(json_result, indent=4, ensure_ascii=False)
            print(formatted_json)
            return json_result
        except ValueError:
            print("响应不是有效的JSON")
            return result

    @staticmethod
    def save_collection_with_new_cases(token, collection_id, collection_case_info, case_id_list, case_name_list, module_name_list):

        url = f'https://cdautotest.keytop.cn/autotest/platform/collection/save'
        headers = {'token': token}

        print(collection_case_info)
        collectionCases = collection_case_info['data']['collectionCases']
        new_start_index = len(collectionCases) + 1

        for i in range(len(case_id_list)):
            # 组装需要新增的单个collectionCase
            new_collectioncase = {
                "id": str(uuid.uuid4()),
                "index": new_start_index,
                "collectionId": collection_id,
                "caseId": case_id_list[i-1],
                "caseName": case_name_list[i-1],
                "caseModule": module_name_list[i-1],
                "caseType": "API",
                "caseSystem": None
            }
            collection_case_info['data']['collectionCases'].append(new_collectioncase)

        print(collection_case_info)

        # result = requests.post(url=url, headers=headers, json=collection_case_info)


if __name__ == '__main__':
    token = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYXNzd29yZCI6Ik1UazVPREV5TURoQWNYZGxjZz09IiwiaWQiOiJiOWNhMGI0NC0zZDg0L"
        "TQwM2MtYTMyMS1hMjVlYzUyYzE0MzMiLCJleHAiOjE3MjcyODI5OTIsImlhdCI6MTcyNzI1NDE5MiwiYWNjb3VudCI6Imhlc2hvdXlpIiwidXN"
        "lcm5hbWUiOiLkvZXlrojkuIAifQ.vmPgVcl8OYgM4n_5prmvcaHfX-XbtaEc7xyNhOq3a9M"
    )

    case_num_list = [10014, 10029, 10038, 10029]  # 用例序号（需要按顺序）
    case_id_list = []       # 查出的用例主键id
    case_name_list = []       # 查出的用例名称
    module_name_list = []     # 对应模块id
    collection_id = '1e5fb29a-d5c7-42ff-9b3f-0db853cd6ee7'  # 要录入的集合id

    app = App()
    # 通过用例序号列表转换需要的信息
    app.select_case_info_by_num(case_num_list, case_id_list, case_name_list, module_name_list)
    # 通过集合查询获取后续保存需要的参数
    collection_case_info = app.get_collection_detail_byid(token, collection_id)
    # 组装新的collectionCase，拼接到上一步查询出的参数中，调接口保存用例到合集
    app.save_collection_with_new_cases(token, collection_id, collection_case_info, case_id_list, case_name_list, module_name_list)
