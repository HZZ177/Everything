#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/20 上午12:07
# @Author  : Heshouyi
# @File    : main.py
# @Software: PyCharm
# @description:

import locust


class Test(locust.HttpUser):
    host = "http://192.168.31.177:8083"
    wait_time = locust.between(1, 2)

    @locust.task
    def test_api(self):
        result = self.client.get("/api/v1/test/")
        assert result.status_code == 200
