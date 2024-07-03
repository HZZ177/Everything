#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/3 17:33
# @Author  : Heshouyi
# @File    : channel_swagger.py
# @Software: PyCharm
# @description:

import requests
import json

# 替换为你的Swagger文档URL
swagger_url = 'http://192.168.21.249:7072/v2/api-docs?group=front-api'

# 发送HTTP请求获取Swagger文档
response = requests.get(swagger_url)
swagger_data = response.json()
print(swagger_data)


# 保存json到文件，ensure_ascii=False表示不自动转ASCII码
with open('channel_swagger_data.json', 'w', encoding='utf-8') as f:
    json.dump(swagger_data, f, ensure_ascii=False, indent=2)
