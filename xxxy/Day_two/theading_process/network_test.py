#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2017/7/4 17:41
# @Author  : Spareribs
# @File    : network_test.py
"""

import requests
import time
from threading import Thread
from multiprocessing import Process

# 定义网络请求函数
_head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'}
url = "http://cuiqingcai.com"


def http_request():
    try:
        webPage = requests.get(url, headers=_head)
        html = webPage.text
        return {"context": html}
    except Exception as e:
        return {"error": e}


def line_httprs():
    """ 测试线性执行网络请求密集型操作所需时间 """
    line_time_before = time.time()
    for x in range(10):
        http_request()
    line_time_now = time.time()
    line_differ_time = line_time_now - line_time_before
    print "Line Http Request: {0}".format(line_differ_time)
    return line_differ_time


def theading_httprs():
    """ 测试多线程并发执行网络密集操作所需时间 """
    theading_httprs = []
    theading_time_before = time.time()
    for theading_item in range(10):
        thread = Thread(target=http_request)
        theading_httprs.append(thread)
        thread.start()

    theading_e = theading_httprs.__len__()
    while True:
        for theading_th in theading_httprs:
            if not theading_th.is_alive():
                theading_e -= 1
        if theading_e <= 0:
            break
    theading_time_now = time.time()
    theading_differ_time = theading_time_now - theading_time_before
    print "Multi - theading Http Request: {0}".format(theading_differ_time)
    return theading_differ_time


def process_httprs():
    """ 测试多进程并发执行Http请求密集型操作 """
    process_httprs = []
    process_time_before = time.time()
    for process_item in range(10):
        process = Process(target=http_request)
        process_httprs.append(process)
        process.start()

    process_e = process_httprs.__len__()
    while True:
        for process_th in process_httprs:
            if not process_th.is_alive():
                process_e -= 1
        if process_e <= 0:
            break
    process_time_now = time.time()
    process_differ_time = process_time_now - process_time_before
    print "Multi - process Http Request: {0}".format(process_differ_time)
    return process_differ_time


if __name__ == '__main__':
    line_time = 0.0
    theading_time = 0.0
    process_time = 0.0
    for item in range(3):
        time.sleep(5)
        line_time += line_httprs()
        time.sleep(5)
        theading_time += theading_httprs()
        time.sleep(5)
        process_time += process_httprs()
    print "执行HTTP请求密集型操作结果如下：\n" \
          "---- Line HTTP: {0:.11f}\n" \
          " Theading HTTP: {1:.11f}\n" \
          "- Process HTTP: {2:.11f}".format(line_time / 3, theading_time / 3, process_time / 3)
