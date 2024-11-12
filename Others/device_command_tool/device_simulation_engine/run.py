#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/9 下午7:11
# @Author  : Heshouyi
# @File    : run.py.py
# @Software: PyCharm
# @description:
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7777)
