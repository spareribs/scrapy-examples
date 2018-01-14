#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/14 18:30
# @Author  : Aries
# @File    : common.py
# @Software: PyCharm

import hashlib


def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


if __name__ == "__main__":
    print get_md5("https://jobbole.com")
