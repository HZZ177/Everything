import requests

# 定义验证码图片的 URL
url = 'http://192.168.21.249:8083/auth/verifyCode'  # 替换为实际的 URL

# 发送 GET 请求获取图片
response = requests.get(url)

# 检查响应状态码
if response.status_code == 200:
    # 打开本地文件，用于写入二进制数据
    with open('captcha.jpg', 'wb') as file:
        # 将响应的内容写入文件
        file.write(response.content)
    print('Captcha image saved successfully as captcha.jpg.')
else:
    print(f'Failed to retrieve image. Status code: {response.status_code}')
