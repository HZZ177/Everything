import pulsar

# Pulsar 地址
service_url = 'pulsar://61.171.113.40:16650'
topic_name = 'yongce-pro/busness-center/temp-pay-callback'
try:
    client = pulsar.Client(service_url)
    producer = client.create_producer(topic_name)

    message = {
        "test": 123
    }
    producer.send(str(message).encode('utf-8'))

    print(f"已发送消息: {message} 到主题: {topic_name}")

    producer.close()
    client.close()

except pulsar.PulsarException as e:
    print(f"连接或发送消息时发生错误: {e}")