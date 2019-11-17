#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import queue
import logging
from concurrent.futures import ThreadPoolExecutor

from conf import URL, MAX_PAGES, SAVE_PATH, HEADERS
from spider import collect_url, parse_review, save_file


if __name__ == "__main__":
    logging.basicConfig(level = logging.DEBUG)
    mylogger = logging.getLogger(__name__)
    workqueue = queue.Queue(600)
    url_list = collect_url(URL, MAX_PAGES, HEADERS)
    mylogger.info("url_list{}".format(url_list))
    mylogger.info("finished collection of url")
    save_thread = threading.Thread(target=save_file, args=[workqueue, SAVE_PATH])
    with ThreadPoolExecutor() as pool:
        for url in url_list:
            print(workqueue)
            pool.submit(parse_review, url, HEADERS, workqueue)
        # pool.submit(save_file, workqueue, SAVE_PATH)
    mylogger.info("lauch threading")
    save_thread.start()
    print(workqueue)
    pool.shutdown(wait=True)
    save_thread.join()
    mylogger.info("finished all")

