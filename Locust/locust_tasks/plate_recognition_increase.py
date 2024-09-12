#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/3 16:45
# @Author  : Heshouyi
# @File    : plate_recognition_increase.py
# @Software: PyCharm
# @description:

import os
import paramiko
from Locust.common.log_tool import logger
import random
import logging
from Locust.common.config_loader import config
from Locust.files.plate_pic_map import plate_map, plate_map_one

# 将paramiko的日志级别设置为WARNING，屏蔽INFO级别的信息
logging.getLogger("paramiko").setLevel(logging.WARNING)


class SSHManager:
    def __init__(self):
        self.hostname = config.get('server').get('ip')
        self.username = config.get('server').get('user')
        self.password = config.get('server').get('password')
        self.ssh = None

    def connect(self):
        """连接到Linux服务器"""
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(self.hostname, username=self.username, password=self.password, timeout=10)
            logger.debug("SSH连接成功")
        except Exception as e:
            logger.error(f"SSH连接失败: {e}")

    def disconnect(self):
        """关闭SSH连接"""
        if self.ssh:
            self.ssh.close()
            logger.debug("SSH连接已关闭")

    def rename_and_copy_file(self, image_path, filename):
        """生成随机名称重命名并复制文件"""
        try:
            random_name = "img_" + str(random.randint(10000, 99999)) + ".jpg"
            image_path_full = fr"{image_path}{filename}"
            new_image_path = fr"{image_path}{random_name}"

            cp_command = f'cp {image_path_full} {new_image_path}'
            stdin, stdout, stderr = self.ssh.exec_command(cp_command)
            error_output = stderr.read().decode('utf-8').strip()
            if error_output:
                logger.error(f"文件复制失败: {error_output}")
            else:
                logger.info(f"文件复制为: {new_image_path}")

            return random_name

        except Exception as e:
            logger.error(f"复制文件失败: {e}")
            return None

    def check_file_exists(self, randomname, target_file_path):
        """检查文件是否存在"""
        try:
            stdin, stdout, stderr = self.ssh.exec_command(f'ls {target_file_path}')
            result = stdout.read().decode('utf-8')
            # logger.info('目标目录文件内容：' + result)
            # 分离文件名和扩展名
            name_part, extension = randomname.rsplit('.', 1)
            target_name = f"{name_part}_0.{extension}"

            flag = target_name in result
            if flag:
                logger.info(f"切割后生成文件【{target_name}】存在，名称正确")
                return 1
            else:
                logger.error(f"切割后生成文件【{target_name}】不存在或名称不正确")
                return 2
        except Exception as e:
            logger.error(f"检查文件是否存在失败: {e}")
            return False


def identify_plate_randomly(client):
    """调用FindCarServer识别库测试接口，图片存放路径为FindCarServer根目录下图片地址"""

    # 使用ssh_manager重命名图片
    ssh_manager = SSHManager()
    ssh_manager.connect()
    image_path = fr'/home/findcar/FindCarServer/recognitionTest/pictest/'
    filename = random.choice(list(plate_map_one.keys()))
    randomname = ssh_manager.rename_and_copy_file(image_path, filename)

    if not randomname:
        logger.error("图片重命名失败，终止识别操作")
        return None, None, None

    image_path = random.choice(list(plate_map_one.keys()))
    target_plate = plate_map_one[image_path]    # 期望车牌号
    target_plate_pure = plate_map_one[image_path][1:]    # 期望车牌号，去除汉字部分
    target_chinese = plate_map_one[image_path][0]   # 期望车牌汉字
    result = None
    flag = None
    result = client.get("/device-access/device/recognitionTest", params={'url': 'pictest/' + randomname})
    # 判断是否返回码200
    if result.status_code != 200:
        logger.error("调用识别库测试接口失败，返回码：" + str(result.status_code))
        ssh_manager.disconnect()
        return None, None, None
    else:
        recognition_plate = result.json()['data']['carPlate']   # 完整识别结果
        if recognition_plate != '':
            recognition_plate_pure = result.json()['data']['carPlate'][2:]   # 识别出的车牌部分，去除汉字和颜色
            recognition_chinese = result.json()['data']['carPlate'][1]  # 识别出的车牌汉字
            if recognition_plate_pure == target_plate_pure:
                flag = 2    # 2=车牌部分符合但汉字不对
                if recognition_chinese == target_chinese:
                    flag = 1    # 1=车牌部分和汉字都符合
        else:
            flag = 3    # 3=车牌部分不符合

        # 检查生成文件是否存在
        target_file_path = rf'/home/findcar/FindCarServer/recognitionTest'
        check_result = ssh_manager.check_file_exists(randomname, target_file_path)
        ssh_manager.disconnect()
        return flag, recognition_plate, target_plate, check_result


if __name__ == '__main__':
    # ssh_manager = SSHManager()
    # ssh_manager.connect()
    # # 随机重命名并粘贴图片
    # image_path = rf'/home/findcar/FindCarServer/recognitionTest/pictest/'
    # filename = random.choice(list(plate_map_one.keys()))
    # randomname = ssh_manager.rename_and_copy_file(image_path, filename)
    #
    # # 检查是否存在切割后文件
    # target_file_path = rf'/home/findcar/FindCarServer/recognitionTest'
    # exist = ssh_manager.check_file_exists(randomname, target_file_path)
    pass
