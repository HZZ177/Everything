"""
转换xmind用例为excel方便导入
"""

from xmindparser import xmind_to_dict
import xlwt
import format


xm = xmind_to_dict(r"C:\H\Xmind文件\寻车3.2.3.xmind")[0]['topic']  # 读取xmind数据
# print(json.dumps(xm, indent=2, ensure_ascii=False))  # indent为显示json格式，ensure_ascii未显示为中文，不显示ASCII码
# 读取xmind文件，以json格式展示


workbook = xlwt.Workbook(encoding='utf-8')  # 创建workbook对象
worksheet = workbook.add_sheet(xm["title"], cell_overwrite_ok=True)  # 创建工作表，并设置可以重写单元格内容
row0 = ["用例编号", "分组", '标题', '前置条件', '步骤', '预期结果']  # 写成excel表格用例的要素
sizes = [10, 11, 30, 60, 50, 11, 11, 11]
dicts = {"horz": "CENTER", "vert": "CENTER"}

style2 = format.styles()  # 定义写入标题的style
"""设置单元格的参数"""
style2.alignment = format.alignments(**dicts)
style2.font = format.fonts()
style2.borders = format.borders()
style2.pattern = format.patterns(7)
format.heights(worksheet, 0)

for i in range(len(row0)):
    worksheet.write(0, i, row0[i], style2)  # 按提前设置好的元素和样式写入表格第一行
    format.widths(worksheet, i, size=sizes[i])

style = format.styles()
style.borders = format.borders()

x = 0  # 写入数据的当前行数
z = 0  # 用例的编号
abc = len(xm["topics"])
for i in range(len(xm["topics"])):
    test_module = xm["topics"][i]  # 测试模块
    for j in range(len(test_module["topics"])):
        test_case = test_module["topics"][j]  # 测试用例
        z += 1
        for k in range(len(test_case["topics"])):
            test_describe = test_case["topics"]
            c1 = len(test_describe[0]["topics"])  # 执行步骤数量
            for n in range(len(test_describe[0]["topics"])):  # 循环写入步骤
                test_pre = test_describe[0]["title"]  # 提取前置条件
                x += 1
                test_steps = test_describe[0]["topics"][n]
                test_except = test_steps["topics"][0]
                worksheet.write(x, 5, f"{n + 1}." + test_except["title"], style)  # 写入预期结果
                worksheet.write(x, 4, f"{n + 1}." + test_steps["title"], style)  # 写入步骤
                worksheet.write(x, 3, test_pre, style)  # 前置条件
            worksheet.write_merge(x - c1 + 1, x, 0, 0, z)  # 用例编号
            worksheet.write_merge(x - c1 + 1, x, 1, 1, test_module["title"])  # 分组(模块名称)
            worksheet.write_merge(x - c1 + 1, x, 2, 2, test_case["title"])  # 标题
            worksheet.write_merge(x - c1 + 1, x, 3, 3, test_describe[0]["title"])  # 标题
workbook.save(xm["title"] + ".xls")  # xls名称取xmind主题名称
