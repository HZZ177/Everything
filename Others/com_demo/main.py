import serial.tools.list_ports
import serial

# 列出所有可用的串口
ports = serial.tools.list_ports.comports()
for port in ports:
    print(port.device)


# 打开串口
ser = serial.Serial('COM3', baudrate=9600, timeout=1)

# 检查串口是否打开
if ser.is_open:
    print(f"Serial port {ser.name} is open.")

# 发送消息
message = "Hello from Python!"
ser.write(message.encode('utf-8'))  # 将字符串编码为字节流并发送
print(f"Message sent: {message}")

# 关闭串口
ser.close()