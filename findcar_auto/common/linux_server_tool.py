#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/13 下午11:29
# @Author  : Heshouyi
# @File    : linux_server_tool.py
# @Software: PyCharm
# @description: 封装关于服务器功能相关的工具

import paramiko
import time
from findcar_auto.common.log_tool import logger
from findcar_auto.common.config_loader import configger
from concurrent.futures import ThreadPoolExecutor

config = configger.load_config()


class LinuxServerTool:
    def __init__(self):
        # 服务器基础信息
        self.Linux_server_ip = config['server']['ip']
        self.Linux_server_user = config['server']['user']
        self.Linux_server_password = config['server']['password']
        # 服务日志路径
        self.ChannelService_log_path = config['server']['ChannelService_log_path']
        self.ParkingGuidance_log_path = config['server']['ParkingGuidance_log_path']
        self.FindCarServer_log_path = config['server']['FindCarServer_log_path']
        # 服务器连接信息
        self.ssh_client = None
        self.tcp_socket = None
        self.executor = ThreadPoolExecutor(max_workers=3)   # 创建一个线程池，默认线程池的最大线程数为3

    def connect_ssh(self):
        """
        ssh连接服务器
        :return:
        """
        self.ssh_client = paramiko.SSHClient()
        # 设置SSH客户端的主机密钥策略，自动将未知主机的密钥添加到本地HostKeys对象中，不会提示用户确认
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            # 尝试连接到远程服务器
            self.ssh_client.connect(
                self.Linux_server_ip,
                username=self.Linux_server_user,
                password=self.Linux_server_password,
                timeout=10  # 连接超时设置10秒，防止连接尝试无限期挂起
            )
            logger.info(f"成功连接到服务器: {self.Linux_server_ip}")
        except paramiko.AuthenticationException:
            logger.info("认证失败，请检查用户名或密码")
        except paramiko.SSHException as sshException:
            logger.info(f"无法建立SSH连接: {sshException}")
        except Exception as e:
            logger.info(f"连接时发生错误: {e}")

    def close_ssh(self):
        """
        关闭ssh连接
        :return:
        """
        if self.ssh_client:
            self.ssh_client.close()
            logger.info(f'已断开服务器SSH连接: {self.Linux_server_ip}')

    def tail_log_file(self, channelservice: bool = False, parkingguidance: bool = False, findcarserver: bool = False,
                      timeout=10, target_str=None, async_mode=False):
        """
        调用内置_tail_log_file方法，通过已有的SSH连接，实时监控指定服务的日志文件，监控到目标string后会提前return
        该函数有异步和同步两种模式：
            同步模式：直接监控指定日志，返回list对象
            异步模式：会开启一个默认最大三线程的线程池，异步监控，适用于启动监控之后异步调用接口，从而实现监控调用后实时
                    生成的日志，线程池在退出工具类后通过__exit__()自动销毁，返回future对象，可以通过future.result()获取返回值

        :param target_str: 希望监控到的目标内容
        :param channelservice: ChannelService服务
        :param parkingguidance: ParkingGuidance服务
        :param findcarserver: FindCarServer服务
        :param timeout: 要实时监控的时长，默认10秒
        :param async_mode: 是否以异步方式执行，默认False
        :return: 返回监控到的所有日志内容，如果同步执行，返回一个list；如果异步执行，返回Future对象
        """
        if async_mode:
            return self.executor.submit(self._tail_log_file, channelservice, parkingguidance, findcarserver, timeout,
                                        target_str)
        else:
            return self._tail_log_file(channelservice, parkingguidance, findcarserver, timeout, target_str)

    def _tail_log_file(self, channelservice: bool = False, parkingguidance: bool = False, findcarserver: bool = False, timeout=10, target_str=None):
        """
        通过已有的SSH连接，实时监控指定服务的日志文件，监控到目标string后会提前return
        :param target_str: 希望监控到的目标内容
        :param channelservice: ChannelService服务
        :param parkingguidance: ParkingGuidance服务
        :param findcarserver: FindCarServer服务
        :param timeout: 要实时监控的时长，默认10秒
        :return: 返回监控到的所有日志内容，类型为list
        """
        if not self.ssh_client:
            raise Exception("暂无SSH连接，请检查")
        # 根据布尔参数选择日志文件路径
        if channelservice:
            log_file_path = self.ChannelService_log_path
            service_name = "ChannelService"
        elif parkingguidance:
            log_file_path = self.ParkingGuidance_log_path
            service_name = "ParkingGuidance"
        elif findcarserver:
            log_file_path = self.FindCarServer_log_path
            service_name = "FindCarServer"
        else:
            raise ValueError("必须指定一个日志文件进行监控")

        stdin, stdout, stderr = self.ssh_client.exec_command(f'tail -f {log_file_path}')
        end_time = time.time() + timeout
        log_lines = []

        while time.time() < end_time:
            if stdout.channel.recv_ready():
                line = stdout.readline().strip()
                if line:
                    log_lines.append(line)
                    logger.info(f"监控到{service_name}日志: {line}")
                    if target_str and target_str in line:
                        break
            time.sleep(0.1)     # 每隔0.1秒检查并添加一次日志监控结果，防止占用资源过高

        stdout.channel.close()
        return log_lines

    # 通过 __enter__ 和 __exit__ 方法实现上下文管理器，通过 with LinuxServerTool() as tool:可以实现用完自动关闭连接
    def __enter__(self):
        self.connect_ssh()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close_ssh()
        self.executor.shutdown()


if __name__ == "__main__":
    with LinuxServerTool() as tool:
        logs = tool.tail_log_file(channelservice=True)
        # logger.info(logs)
