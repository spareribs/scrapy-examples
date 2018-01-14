# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.http import Request

try:
    import urlparse
except:
    from urllib import prase as urlparse


class JobboleSpider(scrapy.Spider):
    name = "jobbole"
    allowed_domains = ["blog.jobbole.com"]
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        1. 获取文章列表中的URL交给Scrapy下载后并进行具体字段解析
        2. 获取下一页URL并交给Scrapy进行下载，下载完成后交给parse
        """
        # 解析列表页面所有文章URL并交给Scrapy下载后进行解析
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            yield Request(
                url=urlparse.urljoin(response.url, post_url),
                meta={"front_images_url": urlparse.urljoin(response.url, image_url)},
                callback=self.parse_detail
            )

        # 提取下一页并交给Scrapy进行下载
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            yield Request(
                url=urlparse.urljoin(response.url, next_url),
                callback=self.parse
            )

    def parse_detail(self, response):
        """
        提取文章具体字段
        """
        # # ********************
        # # use xpath selector *
        # # ********************
        # title = response.xpath("//div[@class='entry-header']/h1/text()").extract()
        # create_date = response.xpath("//p[@class='entry-meta-hide-on-mobile']//text()").extract()[0].split()[0]
        # prasise_nums = response.xpath("//span[contains(@class,'vote-post-up')]//text()").extract()[1]
        # fav_nums = response.xpath("//span[contains(@class,'bookmark-btn')]//text()").extract()[0]
        # match_re = re.match(".*?(\d+).*", fav_nums)
        # if match_re:
        #     fav_nums = match_re.group(1)
        #
        # commonts_nums = response.xpath("//a[@href='#article-comment']/span//text()").extract()[0]
        # match_re = re.match(".*?(\d+).*", commonts_nums)
        # if match_re:
        #     commonts_nums = match_re.group(1)
        #
        # content = response.xpath("//div[@class='entry']").extract()[0]
        #
        # tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a//text()").extract()
        #
        # # # Python2 error
        # # tag_list = [element for element in tag_list if not element.encode("utf-8").strip().endswitch("评论".decode("utf-8"))]
        # # tags = ",".join(tag_list)
        #
        # suffix = "评论"
        # tags = []
        # for tag in tag_list:
        #     if tag.encode("utf-8").strip().endswith(suffix):
        #         break
        #     else:
        #         tags.append(tag)

        # ******************
        # use css selector *
        # ******************
        front_images_url = response.meta.get("front_images_url", "")
        title = response.css(".entry-header h1::text").extract_first("")
        create_date = response.css("p.entry-meta-hide-on-mobile::text").extract_first("").split()[0]
        prasise_nums = response.css("span.vote-post-up h10::text").extract_first("")
        fav_nums = response.css("span.bookmark-btn::text").extract_first("")
        match_re = re.match(".*?(\d+).*", fav_nums)
        if match_re:
            fav_nums = int(match_re.group(1))
        else:
            fav_nums = 0

        commonts_nums = response.css("a[href*='#article-comment'] span::text").extract_first("")
        match_re = re.match(".*?(\d+).*", commonts_nums)
        if match_re:
            commonts_nums = int(match_re.group(1))
        else:
            fav_nums = 0

        content = response.css("div.entry").extract_first("")

        tag_list = response.css("p.entry-meta-hide-on-mobile a::text").extract_first("")

        suffix = "评论"
        tags = []
        for tag in tag_list:
            if tag.encode("utf-8").strip().endswith(suffix):
                break
            else:
                tags.append(tag)

        pass
