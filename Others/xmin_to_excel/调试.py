from xmindparser import xmind_to_dict
import json
import xlwt


xm = xmind_to_dict(r"C:\Users\86364\Desktop\test1.xmind") # 读取xmind数据
print(xm)
# print(json.dumps(xm, indent=2, ensure_ascii=False))  # indent为显示json格式，ensure_ascii未显示为中文，不显示ASCII码
# 读取xmind文件，以json格式展示

