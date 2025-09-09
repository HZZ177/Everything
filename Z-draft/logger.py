import os
import sys
from datetime import datetime
from loguru import logger
from Locust.common import file_path


path = os.path.dirname(os.path.abspath(__file__))

current_date = datetime.now().strftime("%Y-%m-%d")
current_hour = datetime.now().strftime("%H")

# 自定义每个级别日志的信息头颜色
logger.level("DEBUG", color="<blue>")
logger.level("INFO", color="<green>")
logger.level("SUCCESS", color="<bold><green>")
logger.level("WARNING", color="<yellow>")
logger.level("ERROR", color="<red>")
logger.level("CRITICAL", color="<bold><red>")


# 配置自定义 logger handler，输出日志到：1、标准输出 2、日志输出文件 3、Allure报告
logger.configure(
    handlers=[
        {
            "sink": sys.stdout,  # 日志输出到标准输出
            "level": "INFO",  # 日志级别
            "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSSS} | {module}:{line}</green> | <level>{level}</level> | {message}",
            "colorize": True,  # 启用颜色
            "backtrace": False,   # 控制是否追溯详细的回溯信息（即代码调用链和变量状态等详细信息）
            "diagnose": False,    # 控制不会包含详细的诊断信息
            "enqueue": False,  # 关闭多线程安全队列，否则会和locust的协程冲突导致无法启动服务
        },
        # {
        #     "sink": f"{path}/logs/{current_date}/{current_hour}.log",  # 指定日志输出到文件
        #     "level": "INFO",  # 日志级别
        #     "format": "{time:YYYY-MM-DD HH:mm:ss.SSSS} | {module}:{line} | {level} | {message}",  # 日志格式
        #     "rotation": "100 MB",  # 文件大小达到 100 MB 时自动分割日志
        #     "compression": None,  # 压缩日志文件
        #     "backtrace": True,   # 控制是否追溯详细的回溯信息（即代码调用链和变量状态等详细信息）
        #     "diagnose": True,  # 控制是否包含详细的诊断信息
        #     "enqueue": False,  # 关闭多线程安全队列，否则会和locust的协程冲突导致无法启动服务
        # }
    ]
)

# 供其他模块引用的 logger
logger = logger


if __name__ == '__main__':
    print(path)