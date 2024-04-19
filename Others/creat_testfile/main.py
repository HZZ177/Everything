"""
生成指定大小和内容的txt文件
"""

import threading
import os
import time


class CreatTestFile:

    park_hascar = ("INFO  http-nio-7072-exec-2 c.k.stc.cs.controller.ParkController.occupyForFindCar:104 - "
                   "[车位状态更新接口][找车系统][有车] body={'list':[2523601],'reqId':'4f357bcf77bd1bffb13f52d3d09b6486'}\n")
    park_nocar = ("INFO  http-nio-7072-exec-6 c.k.stc.cs.controller.ParkController.freeForFindCar:111 - "
                  "[车位状态更新接口][找车系统][无车] body={'list':[2523601],'reqId':'96210e60bf434a6f91a26a2747f5d0f0'}\n")
    park_incar = ("INFO  http-nio-7072-exec-2 c.k.stc.cs.controller.ParkController.enter:38 - "
                  "[车位状态更新接口][找车系统][入车] body={'list':[2523601],'reqId':'bbaa19eba3f74d5f8e6acfe5536814db'}\n")
    park_outcar = ("INFO  http-nio-7072-exec-7 c.k.stc.cs.controller.ParkController.leave:45 - "
                   "[车位状态更新接口][找车系统][出车] body={'list':[2523601],'reqId':'25bb21acee4849898074569eb973f7b9'}\n")
    plate_change = ("INFO  http-nio-7072-exec-3 c.k.stc.cs.controller.ParkController.updatePlateNo:52 - "
                    "[更新车牌接口][有效数据] body={'list':[{'addr':2523601,'carImageUrl':'/home/findcar/FindCarServer/"
                    "recognition/20231123/2523601/09/2523601_20231123092540.jpg','plateNo':'蓝渝G83666',"
                    "'plateNoReliability':820}],"
                    "'reqId':'bf2cabdf4f8b419288bca9281b41c79a'}\n")
    park_grpc = ("INFO  http-nio-7072-exec-7 c.k.stc.cs.controller.ParkController.leave:45 - "
                 "[gRPC异常] body={'list':[2523601],'reqId':'25bb21acee4849898074569eb973f7b9'}\n")
    park_oss = ("INFO  http-nio-7072-exec-7 c.k.stc.cs.controller.ParkController.leave:45 - "
                "[oss异常] body={'list':[2523601],'reqId':'25bb21acee4849898074569eb973f7b9'}\n")
    park_ERROR = (" ERROR  http-nio-7072-exec-7 c.k.stc.cs.controller.ParkController.leave:45 - "
                  "body={'list':[2523601],'reqId':'25bb21acee4849898074569eb973f7b9'}\n")
    park_ping = (" INFO  http-nio-7072-exec-7 c.k.stc.cs.controller.ParkController.leave:45 - "
                 "[屏指令发送成功] body={'list':[2523601],'reqId':'25bb21acee4849898074569eb973f7b9'}\n")

    def __init__(self, path, size_limit):
        self.path = path
        self.size_limit = size_limit

    # 写入文件
    def write_file(self):
        with open(self.path, "w", encoding="utf-8") as f:
            count = 1
            # while f.tell() < self.size_limit:
            while count <= 500000:
                f.write(CreatTestFile.park_hascar)
                f.write(CreatTestFile.park_nocar)
                f.write(CreatTestFile.park_incar)
                f.write(CreatTestFile.park_outcar)
                f.write(CreatTestFile.plate_change)
                f.write(CreatTestFile.park_grpc)
                f.write(CreatTestFile.park_ERROR)
                f.write(CreatTestFile.park_ping)
                count += 1

    # 监控进度
    # def monitor_progress(self):
    #     while not os.path.exists(self.path):  # 等待文件被创建
    #         time.sleep(0.1)  # 简短暂停以减少活跃等待
    #     while True:
    #         if os.path.exists(self.path):
    #             current_size = os.stat(self.path).st_size
    #             percent_complete = (current_size / self.size_limit) * 100
    #             print(f"Current progress: {percent_complete: .2f}%")
    #             if current_size >= self.size_limit:  # 如果达到或超过了目标文件大小
    #                 break
    #         time.sleep(0.5)  # 每隔0.5秒检查一次

    def start_writing(self):
        writer_thread = threading.Thread(target=self.write_file)
        # progress_thread = threading.Thread(target=self.monitor_progress)

        writer_thread.start()
        # progress_thread.start()

        writer_thread.join()
        # progress_thread.join()  # 等待进度监控结束


# 设置大小和文件信息
file_creator1 = CreatTestFile("channelService.2023-11-29_17.log", 300 * 1024 * 1024)
file_creator2 = CreatTestFile("parkingGuidance.2023-11-29_17.log", 300 * 1024 * 1024)
file_creator3 = CreatTestFile("findCarServer.2023-11-29_17.log", 300 * 1024 * 1024)
file_creator1.start_writing()
file_creator2.start_writing()
file_creator3.start_writing()

