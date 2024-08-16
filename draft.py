import serial


def monitor_com_port(port, baudrate):
    try:
        # 打开指定的COM端口
        ser = serial.Serial(port, baudrate, timeout=1)
        print(f"Listening on {port} at {baudrate} baud rate...")

        while True:
            # 读取数据
            data = ser.readline(ser.in_waiting or 1)
            if data:
                # 将数据转换为16进制字符串并打印
                hex_data = data.hex().upper()
                print(f"Received: {hex_data}")

    except serial.SerialException as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("Monitoring stopped by user.")
    finally:
        if ser.is_open:
            ser.close()


if __name__ == "__main__":
    # 指定端口号和波特率
    port = "COM3"  # COM端口
    baudrate = 9600  # 波特率

    monitor_com_port(port, baudrate)
