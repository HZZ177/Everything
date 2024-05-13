import subprocess
from Others.adb_tool.utils.config import Config


class DeviceManager:
    """设备功能类"""

    @staticmethod
    def connect_device(ip):
        """adb连接设备函数"""
        command = [Config.adb_path, 'connect', ip]
        try:
            result = subprocess.run(command, creationflags=subprocess.CREATE_NO_WINDOW, check=True,
                                    capture_output=True, text=True, timeout=5, encoding='utf-8')
            return result   # "连接设备成功！"
        except subprocess.CalledProcessError as e:
            return e    # f"连接设备 {ip} 失败！"
        except subprocess.TimeoutExpired as e:
            return e    # f"连接设备 {ip} 超时！"

    @staticmethod
    def disconnect_all_device():
        """adb断开所有设备连接函数"""
        command = [Config.adb_path, 'disconnect']
        result = subprocess.run(command, creationflags=subprocess.CREATE_NO_WINDOW,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result

