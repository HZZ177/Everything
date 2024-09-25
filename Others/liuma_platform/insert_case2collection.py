#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/25 16:00
# @Author  : Heshouyi
# @File    : insert_case2collection.py
# @Software: PyCharm
# @description:

import uuid

index = 18  # 顺序id
collection_id = '54a2c895-9b0e-4d13-923e-2078147a222c'  # 集合id
case_id = 'a4c75f13-c48e-4547-89f0-228f47733670'        # 用例id

for i in range(10):
    print(f"INSERT INTO `liuma`.`collection_case` (`id`, `index`, `collection_id`, `case_id`) "
          f"VALUES ('{uuid.uuid4()}', {index}, '{collection_id}', '{case_id}');")

    index += 1
