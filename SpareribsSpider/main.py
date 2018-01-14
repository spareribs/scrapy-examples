#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/14 11:01
# @Author  : Spareribs
# @File    : main.py
# @Software: PyCharm


from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "jobbole"])
