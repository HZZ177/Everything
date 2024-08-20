import os
import shutil


def remove_duplicates(directory):
    seen_names = set()

    # 遍历文件夹中的所有文件
    for filename in os.listdir(directory):
        if "_" in filename:
            # 提取"_"之前的部分
            base_name = filename.split("_")[0]

            # 如果该名称之前没有出现过，保留文件
            if base_name not in seen_names:
                seen_names.add(base_name)
            else:
                # 删除重复的文件
                file_path = os.path.join(directory, filename)
                os.remove(file_path)
                print(f"Deleted: {filename}")


directory_path = r"C:\XTerminal\下载\20240820"
remove_duplicates(directory_path)
