from websocket import create_connection

ws = create_connection("ws://192.168.21.130:8080/device-access/lcd/192.168.24.117&0")
print("Connected to WebSocket server!")
#
# # 接收响应
# response = ws.recv()
# print("Received response:", response)

# 关闭连接
ws.close()
print("Connection closed.")
