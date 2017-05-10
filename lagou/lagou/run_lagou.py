#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2017/5/10 19:31
# @Author  : Spareribs
# @File    : run_lagou.py
"""

from scrapy import cmdline

cmd = 'scrapy crawl job -o items.json'
cmdline.execute(cmd.split(' '))