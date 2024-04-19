"""
固定写入excel的格式
"""
import xlwt  # 导入模块
from xmindparser import xmind_to_dict


def styles():
    """设置单元格的样式的基础方法"""
    style = xlwt.XFStyle()
    return style


def borders(status=1):
    """设置单元格的边框
    细实线:1，小粗实线:2，细虚线:3，中细虚线:4，大粗实线:5，双线:6，细点虚线:7大粗虚线:8，细点划线:9，粗点划线:10，细双点划线:11，粗双点划线:12，斜点划线:13"""
    border = xlwt.Borders()
    border.left = status
    border.right = status
    border.top = status
    border.bottom = status
    return border


def heights(worksheet, line, size=4):
    """设置单元格的高度"""
    worksheet.row(line).height_mismatch = True
    worksheet.row(line).height = size * 256


def widths(worksheet, line, size=11):
    """设置单元格的宽度"""
    worksheet.col(line).width = size * 256


def alignments(**kwargs):
    """设置单元格的对齐方式
    status有两种：horz（水平），vert（垂直）
    horz中的direction常用的有：CENTER（居中）,DISTRIBUTED（两端）,GENERAL,CENTER_ACROSS_SEL（分散）,RIGHT（右边）,LEFT（左边）
    vert中的direction常用的有：CENTER（居中）,DISTRIBUTED（两端）,BOTTOM(下方),TOP（上方）"""
    alignment = xlwt.Alignment()

    if "horz" in kwargs.keys():
        alignment.horz = eval(f"xlwt.Alignment.HORZ_{kwargs['horz'].upper()}")
    if "vert" in kwargs.keys():
        alignment.vert = eval(f"xlwt.Alignment.VERT_{kwargs['vert'].upper()}")
    alignment.wrap = 1  # 设置自动换行
    return alignment


def fonts(name='宋体', bold=False, underline=False, italic=False, colour='black', height=11):
    """设置单元格中字体的样式
    默认字体为宋体，不加粗，没有下划线，不是斜体，黑色字体"""
    font = xlwt.Font()
    # 字体
    font.name = name
    # 加粗
    font.bold = bold
    # 下划线
    font.underline = underline
    # 斜体
    font.italic = italic
    # 颜色
    font.colour_index = xlwt.Style.colour_map[colour]
    # 大小
    font.height = 20 * height
    return font


def patterns(colors=1):
    """设置单元格的背景颜色，该数字表示的颜色在xlwt库的其他方法中也适用，默认颜色为白色
    0 = Black, 1 = White,2 = Red, 3 = Green, 4 = Blue,5 = Yellow, 6 = Magenta, 7 = Cyan,
    16 = Maroon, 17 = Dark Green,18 = Dark Blue, 19 = Dark Yellow ,almost brown), 20 = Dark Magenta,
    21 = Teal, 22 = Light Gray,23 = Dark Gray, the list goes on..."""
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = colors
    return pattern
