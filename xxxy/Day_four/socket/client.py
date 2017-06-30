#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2017/6/30 15:27
# @Author  : Spareribs
# @File    : client.py
"""

import socket
HOST = '127.0.0.1'
PORT = 20000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    cmd = raw_input("【info】：Please input msg:")
    s.send(cmd)
    data = s.recv(1024)
    print "【info】：{0} --[From server]--".format(data)