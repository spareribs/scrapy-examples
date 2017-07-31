#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2017/7/4 17:40
# @Author  : Spareribs
# @File    : io_test.py
"""

import os
import time
from threading import Thread
from multiprocessing import Process


# 定义IO密集的文件读写函数
def write(filename):
    with open(filename, "w") as f:
        for write_item in range(5000000):
            f.write("test——write\n")
    f.close()


def read(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    f.close()


def line_io():
    """测试线性执行IO密集操作所需时间"""
    line_time_before = time.time()
    for line_item in range(10):
        write("test_line.txt")
        read("test_line.txt")
    line_time_now = time.time()
    line_differ_time = line_time_now - line_time_before
    print "Line IO: {0}".format(line_differ_time)
    return line_differ_time


def theading_io():
    write("test_theading.txt")
    read("test_theading.txt")


def theading_io_main():
    """测试多线程并发执行IO密集操作所需时间"""
    theading_ios = []
    theading_time_before = time.time()
    for theading_item in range(10):
        thread = Thread(target=theading_io)
        theading_ios.append(thread)
        thread.start()

    theading_e = theading_ios.__len__()
    while True:
        for theading_th in theading_ios:
            if not theading_th.is_alive():
                theading_e -= 1
        if theading_e <= 0:
            break
    theading_time_now = time.time()
    theading_differ_time = theading_time_now - theading_time_before
    print "Multi - theading IO: {0}".format(theading_differ_time)
    return theading_differ_time


def process_io():
    write("test_process.txt")
    read("test_process.txt")


def process_io_main():
    """ 测试多进程并发执行IO密集型操作 """
    process_ios = []
    process_time_before = time.time()
    for process_item in range(10):
        process = Process(target=process_io)
        process_ios.append(process)
        process.start()

    process_e = process_ios.__len__()
    while True:
        for process_th in process_ios:
            if not process_th.is_alive():
                process_e -= 1
        if process_e <= 0:
            break
    process_time_now = time.time()
    process_differ_time = process_time_now - process_time_before
    print "Multi - process IO: {0}".format(process_differ_time)
    return process_differ_time


if __name__ == "__main__":
    line_time = 0.0
    theading_time = 0.0
    process_time = 0.0
    for item in range(3):
        # 自动创建和删除文件
        try:
            time.sleep(5)
            os.remove("test_line.txt")
            os.remove("test_theading.txt")
            os.remove("test_process.txt")
            time.sleep(2)
        except WindowsError as e:
            print e
        line_file = open("test_line.txt", "w")
        line_file.close()
        theading_file = open("test_theading.txt", "w")
        theading_file.close()
        process_file = open("test_process.txt", "w")
        process_file.close()

        time.sleep(5)
        line_time += line_io()
        time.sleep(5)
        theading_time += theading_io_main()
        time.sleep(5)
        process_time += process_io_main()
    print "执行IO请求密集型操作结果如下：\n" \
          "---- Line IO: {0:.11f}\n" \
          " Theading IO: {1:.11f}\n" \
          "- Process IO: {2:.11f}".format(line_time / 3, theading_time / 3, process_time / 3)
