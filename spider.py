#!/usr/bin/env python3
#-*- coding: utf-8 -*-
"""
本文件主要包括三个函数：
collect_url():
    这个函数主要是用来收集到的热评的URL

parse_review(url):
    抓取对应的热门书评函数

save_file():
    保存抓取到的文件
"""

import requests
import traceback
import json
import re
import queue
import time

from bs4 import BeautifulSoup

from conf import URL, HEADERS, SAVE_PATH, MAX_PAGES

def collect_url(url, max_pages, headers):
    """
    本函数收集热门书评的url，给后面的parse_review函数对应书评的提供url
    """
    url_list = []
    for pages in range(0, max_pages, 20):
        res = requests.get(url, params={"start": pages}, headers=headers)
        soup = BeautifulSoup(res.text, "lxml")
        for ele in soup.find_all("h2"):
            ele = str(ele)
            review_url = re.search(r"\"https:.*/\"", ele).group(0).replace("\"", "")
            url_list.append(review_url)
        time.sleep(5)
    return url_list


def parse_review(url, headers, workqueue):
    """
    爬取对应的热评数据，保存文章标题、文章作者、书籍名称，书籍评分、文章内容、对文章态度
    获取内容对应标签位置：
        文章标题：title
        作者、书籍名称、书籍评分：application/ld+jso
        文章态度：data-ad-ext
        文章内容：link-report
    """
    res = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(res.text, "lxml")
    data_json =json.loads(soup.find("script", type="application/ld+json").text.replace("\n", ""))  # 解析出包含书评的基本信息
    try:
        book = data_json["itemReviewed"]['name']
        title = str(soup.find("title"))
        title = re.sub("<\/?[a-z]+>","", title).replace("\n", "").strip(" ")
        author = data_json["author"]["name"]
        ratingvalue = int(data_json["reviewRating"]['ratingValue'])
        attitude = soup.find("div", class_="main-bd").get("data-ad-ext")
        content = soup.find("div", id="link-report").find_all("p")
        content_str = "".join(list(map(str, content)))
        # 清洗一下content的数据，去掉那些标签
        content_str = re.sub("(?<=\<\w{4}\s).*?(?=\>)", "", content_str)  # 去掉<span>
        content_str = re.sub("<\/?[a-z ]*>", "", content_str)
    except Exception:
        traceback.print_exc()
    data_dict = {}
    data_dict["title"] = title  # 文章题目
    data_dict["bookname"] = book  # 评论书名
    data_dict["author"] = author  # 作者
    data_dict["ratingvalue"] = ratingvalue  # 评星
    data_dict["attitude"] = attitude  # 读者对书评态度
    data_dict["content"] = content_str  # 文章内容
    print(data_dict)
    workqueue.put(json.dumps(data_dict))


def save_file(workqueue, save_path):
    while True:
        item = workqueue.get()
        save_file = open(save_path, "a+")
        save_file.writelines(item + "\n")
        save_file.close()


if __name__ == "__main__":
    url = URL
    headers = HEADERS
    workqueue = queue.Queue(30)
    save_path = SAVE_PATH
    max_pages = MAX_PAGES

    url_list = collect_url(url, max_pages, headers)
    print(url_list)
    data = parse_review(url_list[0], headers, workqueue)
    print(data)
    save_file(workqueue, save_path)
