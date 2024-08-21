#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/21 10:47
# @Author  : Heshouyi
# @File    : locustfile.py
# @Software: PyCharm
# @description:

import os
from locust import HttpUser, task, between
from locust_tasks import plate_recognition, task_group2
from Locust.utils.config_loader import config


class MyUser(HttpUser):
    host = config.get('host')
    wait_time = between(1, 5)

    @task
    def plate_recognition(self):
        plate_recognition.run(self.client)


if __name__ == "__main__":
    os.system("locust")
