import os
import sys


class Config:
    ADB_PATH = '/path/to/adb'
    SCRCPY_PATH = '/path/to/scrcpy'
    # 更多配置

    # 当前文件所处路径，兼容打包为exe后的路径
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))

    # 临时目录
    if getattr(sys, 'frozen', False):
        # 如果应用程序是被打包成可执行文件
        temp_dir = sys._MEIPASS
    else:
        # 如果应用程序直接运行
        temp_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 获取adb和scrcpy的完整路径
    log_file_path = os.path.join(application_path, 'logs')
    base_path = os.path.abspath(os.path.dirname(__file__))
    adb_path = os.path.join(base_path, 'scrcpy_tool', 'adb.exe')
    adb_window_path = os.path.join(temp_dir, 'scrcpy_tool', 'adb.exe')
    scrcpy_path = os.path.join(base_path, 'scrcpy_tool', 'scrcpy.exe')

    # 定义不同设备的日志路径
    fccc_logfile = "/sdcard/Android/data/com.keytop.fccc/files/log"  # fcc收费一体机
    fsfp_logfile = "/sdcard/Android/data/com.keytop.fsfp/files/log"  # fsfp立式人脸找车机
    frsa_logfile = "/sdcard/Android/data/com.keytop.frsa/files/log"  # frsa壁挂式人脸找车机
    lcdgs_logfile = "/sdcard/Android/data/com.keytop.lcdgs/files/log"  # LCD显示屏

    # 保存设备日志文件路径
    download_log_path = base_path

    version = "v1.3.0"