import logging

# 配置 logging 模块
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


logger = logging.getLogger("draft")
logger.info("123")
