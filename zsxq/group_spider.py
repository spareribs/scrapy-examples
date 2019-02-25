#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time        : 2019/2/1 00:03
# @Author      : Spareribs
# @File        : group_spider.py
# @Software    : PyCharm
# @Description :
"""
import json
import re
import urllib

import requests

headers = {
    'accept': "application/json, text/plain, */*",
    'origin': "https://wx.zsxq.com",
    'x-version': "1.10.14",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    'x-request-id': "",
    'referer': "https://wx.zsxq.com/dweb/",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7",
    'cookie': "",
}


def get_group_topics(headers, groups_id):
    """
    通过小组获取小组内所有的主题ID
    # TODO 目前只有7个主题，不知道超过count=20会有什么坑
    :param headers: 请求所需要的头部信息
    :param groups_id: 小组ID
    :return: 主题ID列表
    """
    url = "https://api.zsxq.com/v1.10/groups/{0}/topics?count=20".format(groups_id)
    print(url)
    topic_ids = []
    response = requests.request("GET", url, headers=headers)
    # print(response.content)
    res_dict = json.loads(response.text)
    topics = res_dict.get("resp_data").get("topics")
    # print(topics)
    if topics:
        for _topic in topics:
            try:
                topic_id = _topic.get("topic_id")
                _text = _topic.get("talk").get("text")
                topic_ids.append(topic_id)
                # print(topic_id, _text)
            except AttributeError as e:
                print(e)
    return topic_ids


def get_topics_comments(headers, topics_id, begin_time=None):
    """
    通过主题获取小组内所有的评论内容，获得打卡信息和链接
    :param headers: 请求所需要的头部信息
    :param topics_id: 主题ID
    :param begin_time: 偏移量, 这里通过实践来确定起始位置
    :return: 最后一个人的 create_time
    """
    if begin_time:
        url = "https://api.zsxq.com/v1.10/topics/{0}/comments?" \
              "count=30&sort=asc&begin_time={1}".format(topics_id, begin_time)
    else:
        url = "https://api.zsxq.com/v1.10/topics/{0}/comments?count=30&sort=asc".format(topics_id)
    print(url)
    response = requests.request("GET", url, headers=headers)
    # print(response.content)
    res_dict = json.loads(response.text)
    comments = res_dict.get("resp_data").get("comments")
    # print(comments)
    create_time = None
    if comments:
        for _comment in comments:
            try:
                _create_time = _comment.get("create_time")
                create_time = _create_time
                _text = _comment.get("text").encode("utf-8")
                # print(_text.split("<")[0])
                _id = re.findall(r'[1-9]\d*', _text.split("<")[0])[0]
                _url = urllib.unquote(urllib.unquote(re.findall(r'href="(.*?)"', _text.split("<")[1])[0]))
                print("学号: {0} 打卡时间：{1} 链接：{2}".format(_id, _create_time, _url))
            except AttributeError as e:
                print(e)
            except IndexError as e:
                print(e)
    return create_time


def get_comments_count(headers, topics_id):
    """
    用于获取总评论数
    :param headers:
    :param topics_id: 主题ID
    :return: 返回总评论条数
    """
    url = "https://api.zsxq.com/v1.10/topics/{0}".format(topics_id)
    print(url)
    response = requests.request("GET", url, headers=headers)
    # print(response.content)
    res_dict = json.loads(response.text)
    comments_count = res_dict.get("resp_data").get("topic").get("comments_count")
    print("[Info]: topics_id:{0} comments_count:{1}".format(topics_id, comments_count))
    return comments_count


def main():
    """
    知识星球各星球 topic_id
    Datawhale编程: 222248421551
    初级算法编程：822248424542
    高级算法编程：455528252848
    Datawhale统计学：455528252888
    Datawhale数据挖掘：555541454184
    Datawhale爬虫：455528252818
    Datawhale-NLP实战：222248424811
    Datawhale数据分析：144415141422
    Datawhale-MySQL：822245485482
    Datawhale数据竞赛：455528281128
    Leetcode集训打卡：555515244884
    Datawhale知乎小组：458152115158
    Datawhale-Python基础：145841884822
    """
    _topic_id_list = get_group_topics(headers, "555515244884")
    for _topic_id in _topic_id_list:
        # 首次获取 topic_id 的数据
        create_time = get_topics_comments(headers, _topic_id)

        # # 如果评论数超过30 继续获取 topic_id 的数据
        # comments_count = get_comments_count(headers, _topic_id)
        # while comments_count > 30:
        #     create_time = get_topics_comments(headers, _topic_id, create_time)
        #     comments_count -= 30
        #
        #     # TODO 解决create_time编码格式的问题

    # for topics test
    # get_topics_comments(headers, "544455541888154")

    # for comments_count test
    # get_comments_count(headers, "544455541888154")


if __name__ == "__main__":
    main()
