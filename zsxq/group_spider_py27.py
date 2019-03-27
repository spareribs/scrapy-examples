#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time        : 2019/2/25 13:33
# @Author      : Spareribs
# @File        : group_spider.py
# @Software    : PyCharm
# @Description :
"""
import json
import re
import urllib

import requests
from urllib import quote

headers = {
    'accept': "application/json, text/plain, */*",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7",
    # ********************************
    #   以下内容要根据实际情况修改
    # ********************************
    'user-agent': "****",
    # 将所有cookie的内容写上
    'cookie': "UM_distinctid=****;zsxq_access_token=****;_uab_collina=****;_umdata=****;avatar_url=****;cna=****;isg=****;name=****;upload_channel=****;user_id=****;ws_address=****;"
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
    print(u"[Info]:开始抓取所有主题：\n{0}".format(url))
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
                # print(u"[Info]: {0}".format(_text))
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
                # print(_text)
                # print(_text.split("<")[0])
                _id = re.findall(r'[1-9]\d*', _text.split("<")[0])[0]
                _url = urllib.unquote(urllib.unquote(re.findall(r'href="(.*?)"', _text.split("<")[1])[0]))
                print("学员编号: {0:>3} 打卡时间：{1} 链接：{2}".format(_id, _create_time, _url))
            except AttributeError as e:
                # print(e)
                pass
            except IndexError as e:
                # print(e)
                pass
            except TypeError as e:
                # print(e)
                pass
    return create_time


def get_comments_count(headers, topics_id):
    """
    用于获取总评论数
    :param headers:
    :param topics_id: 主题ID
    :return: 返回总评论条数
    """
    url = "https://api.zsxq.com/v1.10/topics/{0}".format(topics_id)
    print(u"{0}\n[Info]: 开始获取 主题 ** {1} ** 所有评论数 ".format("*" * 40, topics_id))
    response = requests.request("GET", url, headers=headers)
    # print(response.content)
    res_dict = json.loads(response.text)
    comments_count = res_dict.get("resp_data").get("topic").get("comments_count")
    print("[Info]: 获取完毕 主题 ** {0} ** 评论数为:{1}".format(topics_id, comments_count))
    return comments_count


def main():
    """
    知识星球各星球 topic_id
    Datawhale编程: 222248421551
    初级算法梳理：822248424542
    初级算法梳理（二）：222248481411
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
    _topic_id_list = get_group_topics(headers, "144415141422")
    for _topic_id in _topic_id_list:
        # 获取评论数
        comments_count = get_comments_count(headers, _topic_id)
        print(comments_count)
        # 首次获取 topic_id 的数据
        create_time = get_topics_comments(headers, _topic_id)
        # 如果评论数超过30 继续获取 topic_id 的数据
        while comments_count > 30:
            create_time = quote(create_time, 'utf-8')
            create_time = get_topics_comments(headers, _topic_id, create_time)  # 第二次请求都要加create_time
            comments_count -= 30

            # TODO 解决create_time编码格式的问题


if __name__ == "__main__":
    main()
