#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/4 0:16
# @Author  : Aries
# @File    : mimvp.py
# @Software: PyCharm

import requests
from bs4 import BeautifulSoup
import threading
import Queue


class Get_ips():
    def __init__(self, page):
        self.ips = []
        self.urls = []
        for i in range(page):
            self.urls.append("http://proxy.mimvp.com/free.php?proxy=out_hp&sort=&page=" + str(i))
        self.header = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'}
        self.q = Queue.Queue()
        self.Lock = threading.Lock()
        self.cookies = {"user_trace_token": "20170502200739-07d687303c1e44fa9c7f0259097266d6", }
        self.base_url = "https://www.lagou.com/jobs/positionAjax.json?city=%E5%B9%BF%E5%B7%9E&needAddtionalResult=false&kd=python&pn=1"

    def get_ips(self):
        for url in self.urls:
            res = requests.get(url, headers=self.header)
            soup = BeautifulSoup(res.text, 'lxml')
            ips = soup.find_all('tr')
            for i in range(1, len(ips)):
                ip = ips[i]
                tds = ip.find_all("td")
                ip_temp = "{0}://{1}:{2}".format(tds[5].contents[0], tds[1].contents[0], tds[2].contents[0])
                # print str(ip_temp)
                self.q.put(str(ip_temp))

    def review_ips(self):
        while not self.q.empty():
            ip = self.q.get()
            # print ip,type(ip)
            http_tag = ip.split(":")[0]
            # print http_tag
            try:
                proxy = {http_tag: ip}
                # print proxy
                res = requests.get(self.base_url, proxies=proxy, timeout=1)
                self.Lock.acquire()
                if res.status_code == 200:
                    self.ips.append(ip)
                    # print ip
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
    getips_list = my.main()
    with open("iplist.txt", "w") as f:
        for getip in getips_list:
            f.write(str(getip) + "\n")
            print getip
    f.close()
    return getips_list

if __name__ == "__main__":
    get_ip()