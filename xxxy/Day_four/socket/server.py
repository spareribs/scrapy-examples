#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2017/6/30 15:26
# @Author  : Spareribs
# @File    : server.py
"""

import socket

HOST = '127.0.0.1'
PORT = 20000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

print '【info】：Server start at: {0}:{1}'.format(HOST, PORT)
print '【info】：wait for connection...'

while True:
    conn, addr = s.accept()
    print '【info】：Connected by {0}:{1}'.format(addr[0], addr[1])

    while True:
        data = conn.recv(1024)
        print "【info】：{0} --[From client]--".format(data)

        conn.send("【info】：server received you message.")

        # conn.close()
