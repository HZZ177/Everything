import struct
import json

def unescape_data(data):
    """还原转义的数据"""
    result = bytearray()
    i = 0
    while i < len(data):
        if data[i] == 0xff:
            if i + 1 < len(data):
                if data[i + 1] == 0xbb:
                    result.append(0xfb)
                elif data[i + 1] == 0xfc:
                    result.append(0xff)
                elif data[i + 1] == 0xee:
                    result.append(0xfe)
                i += 2
            else:
                raise ValueError("转义格式错误")
        else:
            result.append(data[i])
            i += 1
    return bytes(result)

def parse_packet(packet):
    """解包协议封包数据"""
    # 先去掉头尾并还原转义内容
    if packet[0] != 0xfb or packet[-1] != 0xfe:
        raise ValueError("协议头或协议尾不正确")
    data = unescape_data(packet[1:-1])

    # 解析各字段
    timestamp, command_code, total_packets, packet_seq, data_length = struct.unpack_from('>IBHHH', data[:11])
    data_content = data[11:11 + data_length]
    checksum, = struct.unpack_from('>H', data[11 + data_length:13 + data_length])

    # 校验和验证
    calculated_checksum = sum(data[:11 + data_length]) & 0xFFFF
    if calculated_checksum != checksum:
        raise ValueError("校验码不正确")

    return {
        "timestamp": timestamp,
        "command_code": chr(command_code),
        "total_packets": total_packets,
        "packet_seq": packet_seq,
        "data_length": data_length,
        # "data_content": data_content.decode(errors='ignore') if data_content.isascii() else data_content.hex(),
        "data_content": str(data_content),
        "checksum": checksum
    }

# 示例使用
packet = b'\xfbg#W?J\x00g\x00\x00\x00A\x06\x01\x03\xe5\xb7\x9dABC123\x00\x00\x03\x84\x01\x03\xe5\xb7\x9dABC123\x00\x00\x03\x84\x01\x03\xe5\xb7\x9dABC123\x00\x00\x03\x84\x01\x03\xe5\xb7\x9dABC123\x00\x00\x03\x84\x00\x01\x98\xa4\x13\xd5\xfe'

parsed_data = parse_packet(packet)
json_data = json.dumps(parsed_data, indent=4, ensure_ascii=False)

# 带格式输出
print("解析结果:")
print(json_data)
