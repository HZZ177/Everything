import socket
import time

# 服务器的IP地址和端口
server_ip = '192.168.21.249'
server_port = 8083

# 创建一个列表来保存所有的socket对象
sockets = []

for i in range(1000):
    try:
        # 创建socket对象
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 连接到服务器
        s.connect((server_ip, server_port))

        # 将socket对象保存到列表中，防止垃圾回收导致连接关闭
        sockets.append(s)

        print(f"连接 {i + 1} 成功")

        # 适当的延迟，防止过快创建连接导致系统过载
        time.sleep(0.01)

    except Exception as e:
        print(f"连接 {i + 1} 失败: {e}")

# 保持连接
try:
    while True:
        # 保持主程序运行，所有连接保持打开状态
        time.sleep(10)

except KeyboardInterrupt:
    # 当按下Ctrl+C时，关闭所有的socket连接
    for s in sockets:
        s.close()
    print("所有连接已关闭")
