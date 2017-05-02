#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2017/4/27 18:58
# @Author  : Spareribs
# @File    : xicidaili.py
"""

import requests
from bs4 import BeautifulSoup
import threading
import Queue
class Get_ips():
    def __init__(self, page):
        self.ips = []
        self.urls = []
        for i in range(page):
            self.urls.append("http://www.xicidaili.com/nn/" + str(i))
        self.header = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'}
        # self.file=open("ips",'w')
        self.q = Queue.Queue()
        self.Lock = threading.Lock()

    def get_ips(self):
        for url in self.urls:
            res = requests.get(url, headers=self.header)
            soup = BeautifulSoup(res.text, 'lxml')
            ips = soup.find_all('tr')
            for i in range(1, len(ips)):
                ip = ips[i]
                tds = ip.find_all("td")
                ip_temp = "http://" + tds[1].contents[0] + ":" + tds[2].contents[0]
                # print str(ip_temp)
                self.q.put(str(ip_temp))

    def review_ips(self):
        while not self.q.empty():
            ip = self.q.get()
            try:
                proxy = {"http": ip}
                # print proxy
                res = requests.get("http://www.baidu.com", proxies=proxy, timeout=5)
                self.Lock.acquire()
                if res.status_code == 200:
                    self.ips.append(ip)
                    print ip
                    self.Lock.release()
            except Exception:
                pass
                # print 'error'

    def main(self):
        self.get_ips()
        threads = []
        for i in range(40):
            threads.append(threading.Thread(target=self.review_ips, args=[]))
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        return self.ips
def get_ip():
    my = Get_ips(4)
    return my.main()

get_ip()