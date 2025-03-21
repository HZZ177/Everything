#!/usr/bin/env python
# -*- coding: utf-8 -*-
# [url=home.php?mod=space&uid=267492]@file[/url]    : main.py
import time
import urllib.parse

import requests
import copy
import os
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

HEADERS = {
    "authority": "www.biqg.cc",
    "accept": "application/json",
    "accept-language": "zh,en;q=0.9,zh-CN;q=0.8",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "x-requested-with": "XMLHttpRequest",
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_PATH = os.path.join(BASE_DIR, "result")


def get_hm_cookie(url):
    session = requests.Session()
    session.get(url=url, headers=HEADERS, timeout=10)
    return session


def search(key_word):
    new_header = copy.deepcopy(HEADERS)
    new_header["referer"] = urllib.parse.quote(
        f"https://www.biqg.cc/s?q={key_word}", safe="/&=:?"
    )

    hm_url = urllib.parse.quote(
        f"https://www.biqg.cc/user/hm.html?q={key_word}", safe="/&=:?"
    )
    session = get_hm_cookie(hm_url)

    params = {
        "q": f"{key_word}",
    }
    try:
        response = session.get(
            "https://www.biqg.cc/user/search.html",
            params=params,
            headers=new_header,
            timeout=10,
        )
    except Exception as e:
        print(f"搜索{key_word}时失败，错误信息:{e}")
        return [], session
    data = response.json()
    return data, session


def download_chapter(args):
    """
    下载单个章节的内容
    返回: (序号, 标题, 内容) 的元组
    """
    tag, href, session, index = args
    title = f"{tag.text}"
    url = f"https://www.biqg.cc{href}"
    print(f"开始下载章节：{title} url: {url}")

    try:
        content_response = session.get(url, headers=HEADERS)
        content_soup = BeautifulSoup(content_response.content, "html.parser")
        text = content_soup.find(id="chaptercontent")

        # 获取章节内容
        content = []
        content.append(f"\n\n{title}\n\n")
        for i in text.get_text().split("　　")[1:-2]:
            content.append(f"{i}\n")

        return (index, title, "".join(content))
    except Exception as e:
        print(f"下载章节 {title} 失败: {e}")
        return (index, title, f"\n\n{title}\n\n下载失败: {str(e)}\n\n")


def download_txt(download_url, path_name, session):
    """
    下载小说
    :param download_url: 下载链接
    :param path_name: 存储文件名
    :return:
    """
    if not os.path.exists(DOWNLOAD_PATH):
        os.makedirs(DOWNLOAD_PATH, exist_ok=True)

    result_file_path = os.path.join(DOWNLOAD_PATH, f"{path_name}.txt")

    try:
        # 获取所有章节链接
        response = session.get(download_url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        down_load_url = soup.select("div[class='listmain'] dl dd a")

        # 准备所有要下载的章节信息
        chapters_to_download = []
        index = 0

        for tag in down_load_url:
            href = tag["href"]
            if href == "javascript:dd_show()":
                hide_dd = soup.select("span[class='dd_hide'] dd a")
                for hide_tag in hide_dd:
                    chapters_to_download.append((hide_tag, hide_tag["href"], session, index))
                    index += 1
            else:
                chapters_to_download.append((tag, href, session, index))
                index += 1

        # 使用线程池并发下载
        chapter_contents = {}
        max_workers = min(20, len(chapters_to_download))  # 最多20个线程
        print(f"开始并发下载，使用{max_workers}个线程...")

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交所有下载任务
            future_to_chapter = {
                executor.submit(download_chapter, args): args
                for args in chapters_to_download
            }

            # 收集下载结果
            for future in as_completed(future_to_chapter):
                index, title, content = future.result()
                chapter_contents[index] = content

        # 按顺序写入文件
        with open(result_file_path, "w", encoding="utf-8") as result_file:
            # 写入书名
            result_file.write(f"《{path_name}》\n\n")

            # 按章节序号顺序写入内容
            for i in range(len(chapter_contents)):
                result_file.write(chapter_contents[i])

        print(f"《{path_name}》下载完成！保存至: {result_file_path}")

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        print(f"下载{download_url}失败，错误信息:{e}")


def run():
    while True:
        keyword = input("请输入搜索的小说名or输入q退出:")
        if keyword.replace(" ", "").lower() == "q":
            break
        if not keyword:
            continue
        data_list, session = search(keyword)
        if not data_list or data_list == 1:
            print("请重试.......")
            continue

        # 显示搜索结果
        print("\n搜索结果:")
        print("-" * 50)
        for i in range(len(data_list)):
            item = data_list[i]
            articlename = item.get("articlename")
            author = item.get("author")
            print(f"编号：{i} 书名：{articlename}----->{author}")
        print("-" * 50)
        print("提示：")
        print("1. 输入单个数字下载单本")
        print("2. 输入多个数字并用逗号分隔下载多本，如：0,1,2")
        print("3. 输入 all 下载全部")

        while True:
            try:
                choice = input("请输入需要下载的编号:").strip().lower()

                # 处理全部下载的情况
                if choice == 'all':
                    selected_indices = list(range(len(data_list)))
                    break

                # 处理单本或多本下载的情况
                selected_indices = []
                for num in choice.split(','):
                    num = int(num.strip())
                    if 0 <= num < len(data_list):
                        selected_indices.append(num)
                    else:
                        raise ValueError(f"编号 {num} 超出范围")

                if not selected_indices:
                    raise ValueError("未选择任何有效编号")
                break

            except ValueError as e:
                print(f"输入错误: {str(e)}")
                continue

        # 下载选中的书籍
        print(f"\n准备下载 {len(selected_indices)} 本书...")
        for num_book in selected_indices:
            try:
                item = data_list[num_book]
                url_list = f"https://www.biqg.cc{item.get('url_list')}"
                articlename = item.get('articlename', '')
                author = item.get('author', '')
                path_name = f"{articlename}___{author}"

                print(f"\n开始下载 《{articlename}》 作者：{author}")
                print(f"下载链接: {url_list}")

                download_txt(url_list, path_name, session)

            except Exception as e:
                print(f"下载编号 {num_book} 的书籍时出错: {str(e)}")
                continue

        print("\n所有选中的书籍下载完成！")


if __name__ == "__main__":
    run()