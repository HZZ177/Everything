#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/25 16:36
# @Author  : Heshouyi
# @File    : update_collections_by_casenum.py
# @Software: PyCharm
# @description:

import json
import uuid
import base64
import pymysql
import requests
from log_module import logger


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
            return pymysql.connect(**self.db_config, charset='utf8mb4')
        except Exception as e:
            logger.error(f"连接数据库失败，错误信息: {e}")
            return None

    @staticmethod
    def platform_login(account, password):
        url = 'https://cdautotest.keytop.cn/autotest/platform/login'

        # 密码进行base64转换
        encoded_bytes = base64.b64encode(password.encode('utf-8'))  # 字符串转换为utf-8字节串后进行base64编码
        encoded_password = encoded_bytes.decode('utf-8')    # 将base64编码的字节串转换回字符串

        data = {
            "account": account,
            "password": encoded_password
        }

        try:
            result = requests.post(url=url, json=data)
            result.raise_for_status()  # 如果响应状态码不是200，将引发HTTPError
            token = result.headers.get('token')
            if not token:
                logger.info("登录成功但未获取到token")
            return token
        except requests.exceptions.RequestException as e:
            logger.error(f"请求失败，错误信息：{e}")
            return None

    def select_case_info_by_num(self, case_num_list):
        """
        根据用例编号列表，查询对应的用例ID、名称和模块名称
        :param case_num_list: 用例编号列表
        :return: dict, key为num, value为字典包含id, name, module_name
        """
        case_info = {}
        if not self.conn:
            logger.error("数据库连接未建立")
            return case_info

        if not case_num_list:
            return case_info

        # 根据用例case_list查询用例信息并组装
        format_strings = ','.join(['%s'] * len(case_num_list))
        query = f"SELECT c.num, c.id, c.name, cm.name FROM `case` c LEFT JOIN `case_module` cm ON c.module_id = cm.id WHERE c.num IN ({format_strings}) ORDER BY FIELD(c.num, {','.join(['%s'] * len(case_num_list))})"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, tuple(case_num_list + case_num_list))
                results = cursor.fetchall()
                for row in results:
                    num, case_id, name, module_name = row
                    case_info[num] = {
                        'id': case_id,
                        'name': name,
                        'module_name': module_name if module_name else "未知模块"
                    }
        except Exception as e:
            logger.error(f"查询用例信息失败，错误信息: {e}")
        return case_info

    def get_related_case_nums(self, case_num):
        """
        获取给定用例编号的直接前置和后置用例编号
        :param case_num: 当前用例编号
        :return: list 包含所有相关的用例编号，按照依赖顺序排列
        """
        related_nums = []

        with self.conn.cursor() as cursor:
            cursor.execute("SELECT common_param FROM `case` WHERE num = %s", (case_num,))
            result = cursor.fetchone()
            if not result:
                logger.info(f"用例编号 {case_num} 未找到对应的用例")
                return [case_num]  # 仅返回当前用例

            common_param = result[0]

            # 解析common_param中的startCase和endCase
            try:
                params = json.loads(common_param)
                start_cases = params.get('startCase', [])
                end_cases = params.get('endCase', [])
            except json.JSONDecodeError as e:
                logger.error(f"解析common_param失败，错误信息: {e}")
                start_cases = []
                end_cases = []

            # 前置用例之前增加分隔用例
            related_nums.append(10076)

            # 添加前置用例
            related_nums.extend(start_cases)

            # 添加当前用例
            related_nums.append(case_num)

            # 添加后置用例
            related_nums.extend(end_cases)

        return related_nums

    def get_all_related_case_nums(self, main_case_num_list):
        """
        获取所有主用例及其直接相关的前置和后置用例编号
        :param main_case_num_list: 主用例编号列表
        :return: list 包含所有相关的用例编号，按照依赖顺序排列
        """
        all_related_nums = []
        for num in main_case_num_list:
            related = self.get_related_case_nums(num)
            all_related_nums.extend(related)
        return all_related_nums

    @staticmethod
    def get_collection_detail_byid(token, collection_id):
        url = f'https://cdautotest.keytop.cn/autotest/platform/collection/detail/{collection_id}'
        headers = {'token': token}

        try:
            result = requests.get(url=url, headers=headers)
            result.raise_for_status()
            json_result = result.json()
            return json_result.get('data')
        except requests.exceptions.RequestException as e:
            logger.error(f"获取集合详情失败，错误信息：{e}")
            return None
        except ValueError:
            logger.error("获取集合信息的响应不是有效的JSON")
            return None

    def assemble_case_info(self, main_case_num_list):
        """
        根据主用例编号列表，获取所有相关用例的信息，并按顺序排序
        :param main_case_num_list: 主用例编号列表
        :return: list，按顺序排列的用例信息字典
        """
        # 获取所有相关的用例编号
        all_related_nums = self.get_all_related_case_nums(main_case_num_list)
        logger.info(f"根据主用例列表组合的所有用例编号：{all_related_nums}")

        # 获取所有相关用例的信息
        case_info_dict = self.select_case_info_by_num(all_related_nums)

        # 构建按顺序排列的用例信息列表
        ordered_case_info_list = []
        for num in all_related_nums:
            case_info = case_info_dict.get(num)
            if case_info:
                # 添加num到case_info中，方便后续处理
                case_info_with_num = case_info.copy()
                case_info_with_num['num'] = num
                ordered_case_info_list.append(case_info_with_num)
            else:
                logger.info(f"用例编号 {num} 的信息未找到，跳过")
        logger.debug(f"排序后的用例信息列表：{ordered_case_info_list}")
        return ordered_case_info_list



    @staticmethod
    def save_collection_with_new_cases(token, collection_id, collection_case_info, case_info_list):
        """
        保存新的collectionCases到集合中
        :param token: 平台token
        :param collection_id: 集合ID
        :param collection_case_info: 当前集合的详细信息
        :param case_info_list: 按顺序排列的用例信息列表
        """
        url = f'https://cdautotest.keytop.cn/autotest/platform/collection/save'
        headers = {'token': token}

        collection_cases = collection_case_info.get('collectionCases', [])
        new_start_index = len(collection_cases) + 1

        for case_info in case_info_list:
            new_collectioncase = {
                "id": str(uuid.uuid4()),
                "index": new_start_index,
                "collectionId": collection_id,
                "caseId": case_info['id'],
                "caseName": case_info['name'],
                "caseModule": case_info['module_name'],
                "caseType": "API",
                "caseSystem": None
            }
            collection_cases.append(new_collectioncase)
            new_start_index += 1

        logger.info(f'组装后集合内用例数据：{json.dumps(collection_case_info, indent=4, ensure_ascii=False)}')

        try:
            response = requests.post(url=url, headers=headers, json=collection_case_info)
            response.raise_for_status()
            logger.info(f"集合新增用例接口返回信息：{response.json()}")
        except requests.exceptions.RequestException as e:
            logger.error(f"保存集合失败，错误信息：{e}")

    def get_collection_id_by_name(self, collection_name):
        get_collection_id = f"SELECT id FROM `collection` where name = %s and `status` = 1"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(get_collection_id, collection_name)
                results = cursor.fetchall()
                if results:
                    if len(results) == 1:
                        return results[0][0]
                    else:
                        logger.error(f"集合【{collection_name}】对应的未删除id数量大于1，请检查")
                        return None
                else:
                    return None
        except Exception as e:
            logger.error(f"查询集合ID失败，错误信息：{e}")
            return None

    def execute(self, account, password, main_case_num_list, collection_name):
        # 登录获取token
        token = self.platform_login(account, password)
        if not token:
            logger.error("无法获取token，已终止")
            return

        # 获取集合id
        collection_id = self.get_collection_id_by_name(collection_name)
        if not collection_id:
            logger.error(f"集合【{collection_name}】没有获取到对应的有效集合id，已终止")
            return

        # 获取并组装所有相关用例的信息
        ordered_case_info_list = self.assemble_case_info(main_case_num_list)
        if not ordered_case_info_list:
            logger.error(f"用例id集合{main_case_num_list}没有获取到任何用例信息，已终止")
            return

        # 获取集合的当前信息
        collection_case_info = self.get_collection_detail_byid(token, collection_id)
        if not collection_case_info:
            logger.error(f"无法获取集合{collection_id}的详情，已终止")
            return

        # 组装新的collectionCase，拼接到上一步查询出的参数中，调接口保存用例到合集
        self.save_collection_with_new_cases(token, collection_id, collection_case_info, ordered_case_info_list)


if __name__ == '__main__':
    app = App()

    # 登录的账号信息
    account = "heshouyi"
    password = "19981208@qwer"

    # 需要添加到集合中的主用例编号列表，按顺序填写，别填前后置id
    main_case_num_list = [
        10384
    ]

    # 要录入的集合名称
    collection_name = 'test'  # 替换为实际的集合名称

    # 执行流程
    app.execute(account, password, main_case_num_list, collection_name)
