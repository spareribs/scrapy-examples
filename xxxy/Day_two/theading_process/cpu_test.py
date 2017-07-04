#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2017/7/4 17:38
# @Author  : Spareribs
# @File    : cpu_test.py
"""

import time
from threading import Thread
from multiprocessing import Process


# 定义CPU密集的计算函数
def count(x, y):
    """ 定义CPU密集的计算函数 """
    # 使程序完成150万计算
    c = 0
    while c < 500000:
        c += 1
        x += x
        y += y


def line_count():
    """ 测试线性执行CPU密集操作所需时间 """
    line_time_before = time.time()
    for x in range(10):
        count(1, 1)
    line_time_now = time.time()
    line_differ_time = line_time_now - line_time_before
    # print "Line CPU: {0}".format(line_differ_time)
    return line_differ_time


def theading_count():
    """ 测试多线程并发执行CPU密集操作所需时间 """
    theading_counts = []
    theading_time_before = time.time()
    for theading_item in range(10):
        thread = Thread(target=count, args=(1, 1))
        theading_counts.append(thread)
        thread.start()

    theading_e = theading_counts.__len__()
    while True:
        for theading_th in theading_counts:
            if not theading_th.is_alive():
                theading_e -= 1
        if theading_e <= 0:
            break
    theading_time_now = time.time()
    theading_differ_time = theading_time_now - theading_time_before
    # print "Multi - theading CPU: {0}".format(theading_differ_time)
    return theading_differ_time


def process_count():
    """ 测试多进程并发执行CPU密集操作所需时间 """
    process_counts = []
    process_time_before = time.time()
    for process_item in range(10):
        process = Process(target=count, args=(1, 1))
        process_counts.append(process)
        process.start()
    process_e = process_counts.__len__()
    while True:
        for process_th in process_counts:
            if not process_th.is_alive():
                process_e -= 1
        if process_e <= 0:
            break
    process_time_now = time.time()
    process_differ_time = process_time_now - process_time_before
    # print "Multi - process CPU: {0}".format(process_differ_time)
    return process_differ_time


if __name__ == "__main__":
    line_time = 0.0
    theading_time = 0.0
    process_time = 0.0
    for item in range(3):
        time.sleep(5)
        line_time += line_count()
        time.sleep(5)
        theading_time += theading_count()
        time.sleep(5)
        process_time += process_count()
    print "执行CPU请求密集型操作结果如下：\n" \
          "---- Line CPU: {0:.11f}\n" \
          " Theading CPU: {1:.11f}\n" \
          "- Process CPU: {2:.11f}".format(line_time / 3, theading_time / 3, process_time / 3)
