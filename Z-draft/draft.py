import requests
import time
import datetime
import json
from logger import logger

# --- 配置区 ---
# 目标接口URL
TARGET_URL = "https://yongce-pro-test.keytop.cn/vehicle-pay-center/common/config/getCurrentZone"

# 请求超时时间（秒）
REQUEST_TIMEOUT = 5

# 每次请求之间的间隔时间（秒）
SLEEP_INTERVAL = 0.1


# --- 脚本主逻辑 ---
def run_test_loop():
    """
    主测试循环函数
    """
    logger.info("--- API稳定性测试已启动 ---")
    logger.info(f"测试目标: GET {TARGET_URL}")
    logger.info(f"请求间隔: {SLEEP_INTERVAL} 秒")
    logger.info("按 Ctrl+C 停止测试.")
    logger.info("-" * 30)

    request_count = 0

    while True:
        request_count += 1
        # 获取当前时间作为请求时间戳
        request_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

        try:
            # 记录请求开始的时间点
            start_time = time.time()

            # 发起GET请求，并设置超时
            response = requests.get(TARGET_URL, timeout=REQUEST_TIMEOUT)

            # 记录请求结束的时间点
            end_time = time.time()

            # 计算请求耗时（毫秒）
            duration_ms = (end_time - start_time) * 1000

            # 1. 检查HTTP状态码是否为 200 (OK)
            if response.status_code == 200:
                try:
                    # 尝试解析返回的JSON数据
                    json_data = response.json()

                    # 2. 提取业务码和消息 (使用.get()方法防止KeyError)
                    result_code = json_data.get("resultCode")
                    result_msg = json_data.get("resultMsg")

                    # 3. 判断业务是否成功
                    if result_code == 200 and result_msg is not None:
                        log_message = (
                            f"[{request_timestamp}] SUCCESS | "
                            f"耗时: {duration_ms:.2f} ms | "
                            f"HTTP Status: {response.status_code} | "
                            f"分区: '{result_msg}'"
                        )
                    else:
                        # 业务逻辑失败，例如resultCode不是200
                        log_message = (
                            f"[{request_timestamp}] LOGIC_FAIL | "
                            f"耗时: {duration_ms:.2f} ms | "
                            f"HTTP Status: {response.status_code} | "
                            f"Response Body: {response.text}"
                        )
                except json.JSONDecodeError:
                    # 返回的不是有效的JSON格式
                    log_message = (
                        f"[{request_timestamp}] JSON_ERROR | "
                        f"耗时: {duration_ms:.2f} ms | "
                        f"HTTP Status: {response.status_code} | "
                        f"Invalid JSON Body: {response.text}"
                    )
            else:
                # HTTP状态码不是200，例如 404, 500, 502 等
                log_message = (
                    f"[{request_timestamp}] HTTP_ERROR | "
                    f"耗时: {duration_ms:.2f} ms | "
                    f"HTTP Status: {response.status_code} | "
                    f"Response Body: {response.text}"
                )

        except requests.exceptions.Timeout:
            # 请求超时
            log_message = f"[{request_timestamp}] REQUEST_FAIL | 错误: 请求超时 (超过 {REQUEST_TIMEOUT} 秒)"
        except requests.exceptions.RequestException as e:
            # 其他网络层面的错误，如DNS解析失败、连接被拒绝等
            log_message = f"[{request_timestamp}] REQUEST_FAIL | 错误: {e}"

        logger.info(log_message)

        # 等待指定间隔时间后进行下一次请求
        time.sleep(SLEEP_INTERVAL)


if __name__ == "__main__":
    try:
        run_test_loop()
    except KeyboardInterrupt:
        logger.info("\n--- 测试被手动停止 ---")

