try:
    data = {
        "port1": 1,
    }
    park_num = data['port']
except KeyError as e:
    print(f'缺少必填参数: {str(e)}')
