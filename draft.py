import re

# 正则表达式模式
date_pattern = r"\b\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}\b"

# 测试字符串
test_string = "2024-07-26 16:40:11.573"

# 匹配日期
match = re.search(date_pattern, test_string)

if match:
    print("匹配成功:", match.group())
else:
    print("匹配失败")
