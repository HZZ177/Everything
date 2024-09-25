#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/25 16:00
# @Author  : Heshouyi
# @File    : insert_case2collection.py
# @Software: PyCharm
# @description:

import uuid

index = 25  # 顺序id
collection_id = 'a923764c-5c3f-43d2-a955-10d38ee9c1f1'  # 集合id
case_id = '8c08b319-8ee2-4518-92da-77a46279568a'        # 用例id

for i in range(18):
    print(f"INSERT INTO `liuma`.`collection_case` (`id`, `index`, `collection_id`, `case_id`) "
          f"VALUES ('{uuid.uuid4()}', {index}, '{collection_id}', '{case_id}');")

    index += 1
