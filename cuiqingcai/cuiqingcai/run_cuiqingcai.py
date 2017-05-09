#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2017/5/9 18:42
# @Author  : Spareribs
# @File    : run_cuiqingcai.py
"""
from scrapy import cmdline

cmd = 'scrapy crawl cqc'
cmdline.execute(cmd.split(' '))