import re

import openpyxl
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox


def decrease_seat_number(input_string):
    """
    将输入字符串中的座位号（x座）减1。
    如果座位号变为负数，则保持不变并发出警告。

    Args:
        input_string (str): 包含座位信息的字符串，例如 "V2区 12排25座PHAM TRONG THO"。

    Returns:
        str: 更新后的字符串，如果未找到座位号或处理失败则返回原始字符串。
    """
    if not isinstance(input_string, str):
        # 如果不是字符串类型，直接返回原值（例如数字、None等）
        return input_string

    # 正则表达式匹配“数字座”
    match = re.search(r'(\d+)座', input_string)

    if match:
        original_seat_number_str = match.group(1)
        try:
            original_seat_number = int(original_seat_number_str)
            new_seat_number = original_seat_number - 1

            # 检查座位号是否会变为负数
            if new_seat_number < 0:
                # print(f"警告：检测到座位号 '{original_seat_number}' 减1后将变为负数。该单元格保持不变。")
                return input_string  # 保持原值

            # 使用re.sub替换匹配到的部分
            return re.sub(r'(\d+)座', str(new_seat_number) + '座', input_string, count=1)
        except ValueError:
            # print(f"警告：无法将 '{original_seat_number_str}' 转换为数字。该单元格保持不变。")
            return input_string
    else:
        return input_string


def process_excel_seat_numbers(
        filepath: str,
        sheet_name: str,
        start_row: int,
        end_row: int,
        start_col: int,
        end_col: int,
        output_filepath: str = None
):
    """
    处理Excel文件中指定范围的单元格，将座位号减1。

    Args:
        filepath (str): 原始Excel文件的路径。
        sheet_name (str): 要处理的工作表名称。
        start_row (int): 起始行号（从1开始）。
        end_row (int): 终止行号（从1开始）。
        start_col (int): 起始列号（从1开始，可以是数字或列字母，如'A'）。
        end_col (int): 终止列号（从1开始，可以是数字或列字母，如'C'）。
        output_filepath (str, optional): 保存修改后文件的新路径。 如果为None，则在原文件路径前添加"_updated"。
    """
    try:
        wb = load_workbook(filepath)
        sheet = wb[sheet_name]
    except FileNotFoundError:
        messagebox.showerror("错误", f"文件 '{filepath}' 未找到。请检查文件路径是否正确。")
        return False
    except KeyError:
        messagebox.showerror("错误", f"工作表 '{sheet_name}' 未找到。请检查工作表名称是否正确。")
        return False
    except Exception as e:
        messagebox.showerror("错误", f"加载Excel文件时发生错误: {e}")
        return False

    # 将列参数转换为数字索引（如果输入的是字母）
    # openpyxl.utils.column_index_from_string 在 openpyxl.utils 中
    try:
        if isinstance(start_col, str):
            start_col = openpyxl.utils.column_index_from_string(start_col.upper())
        if isinstance(end_col, str):
            end_col = openpyxl.utils.column_index_from_string(end_col.upper())
    except ValueError:
        messagebox.showerror("错误", "列号输入无效，请使用数字（如1）或大写字母（如'A'）。")
        return False

    print(f"\n--- 开始处理 Excel 文件 '{filepath}' 中的 '{sheet_name}' ---")
    print(
        f"处理范围: R{start_row}C{start_col} ({get_column_letter(start_col)}) 到 R{end_row}C{end_col} ({get_column_letter(end_col)})")

    cells_modified_count = 0

    # 遍历指定范围内的所有单元格
    for row_idx in range(start_row, end_row + 1):
        for col_idx in range(start_col, end_col + 1):
            cell = sheet.cell(row=row_idx, column=col_idx)
            original_value = cell.value

            # 只处理非空且为字符串类型的单元格
            if isinstance(original_value, str) and original_value.strip():
                new_value = decrease_seat_number(original_value)
                if new_value != original_value:  # 只有当值实际改变时才更新并计数
                    cell.value = new_value
                    cells_modified_count += 1

    # 确定输出文件路径
    if output_filepath is None:
        if "." in filepath:
            parts = filepath.rsplit('.', 1)
            output_filepath = f"{parts[0]}_updated.{parts[1]}"
        else:
            output_filepath = f"{filepath}_updated.xlsx"  # 默认添加.xlsx后缀

    try:
        wb.save(output_filepath)
        messagebox.showinfo("完成",
                            f"处理完成！\n成功修改 {cells_modified_count} 个单元格的座位号。\n"
                            f"修改后的文件已保存到: '{output_filepath}'")
        print(f"\n--- 处理完成！ ---")
        print(f"成功修改 {cells_modified_count} 个单元格的座位号。")
        print(f"修改后的文件已保存到: '{output_filepath}'")
        return True
    except Exception as e:
        messagebox.showerror("错误", f"保存文件失败。请确保文件未被其他程序占用，并检查路径权限。\n错误信息: {e}")
        print(f"错误：保存文件失败。错误信息: {e}")
        return False


# --- 主程序入口 ---
if __name__ == "__main__":
    # 隐藏Tkinter主窗口（只使用对话框）
    root = tk.Tk()
    root.withdraw()

    # 1. 文件选择器
    excel_file_path = filedialog.askopenfilename(
        title="选择 Excel 文件",
        filetypes=[("Excel files", "*.xlsx *.xls")],
        defaultextension=".xlsx"
    )

    if not excel_file_path:
        messagebox.showwarning("取消", "未选择文件，程序退出。")
        exit()  # 用户取消选择文件，退出程序

    # 2. 获取工作表名称
    sheet_name = simpledialog.askstring("输入", "请输入要处理的工作表名称：", parent=root)
    if not sheet_name:
        messagebox.showwarning("取消", "未输入工作表名称，程序退出。")
        exit()

    # 3. 获取处理范围
    try:
        start_row = simpledialog.askinteger("输入", "请输入起始行号 (例如: 1):", parent=root)
        if start_row is None: raise ValueError("用户取消")
        end_row = simpledialog.askinteger("输入", "请输入终止行号 (例如: 10):", parent=root)
        if end_row is None: raise ValueError("用户取消")
        start_col_str = simpledialog.askstring("输入", "请输入起始列号 (例如: A 或 1):", parent=root)
        if start_col_str is None: raise ValueError("用户取消")
        end_col_str = simpledialog.askstring("输入", "请输入终止列号 (例如: C 或 3):", parent=root)
        if end_col_str is None: raise ValueError("用户取消")

        # 尝试将列号转换为整数，如果不是整数，则保持字符串以便openpyxl处理
        try:
            start_col = int(start_col_str)
        except ValueError:
            start_col = start_col_str.upper()  # 转换为大写字母

        try:
            end_col = int(end_col_str)
        except ValueError:
            end_col = end_col_str.upper()  # 转换为大写字母

    except (ValueError, TypeError):  # 用户点击取消或输入无效
        messagebox.showwarning("取消", "未完整输入处理范围，程序退出。")
        exit()

    # 4. 调用处理函数
    process_excel_seat_numbers(
        filepath=excel_file_path,
        sheet_name=sheet_name,
        start_row=start_row,
        end_row=end_row,
        start_col=start_col,
        end_col=end_col,
        output_filepath=None  # 让程序自动生成 "_updated" 后缀的文件名
    )

    # 保持Tkinter事件循环，直到所有对话框关闭
    # root.mainloop() # 如果只是用withdraw，不需要这个
