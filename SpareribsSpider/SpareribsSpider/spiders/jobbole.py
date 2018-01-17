# -*- coding: utf-8 -*-
import re
import scrapy
import datetime
from scrapy.http import Request
from scrapy.loader import ItemLoader
from SpareribsSpider.items import JobBoleAticleItem
from SpareribsSpider.utils.common import get_md5

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
                meta={"front_image_url": urlparse.urljoin(response.url, image_url)},
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
        # praise_nums = response.xpath("//span[contains(@class,'vote-post-up')]//text()").extract()[1]
        # fav_nums = response.xpath("//span[contains(@class,'bookmark-btn')]//text()").extract()[0]
        # match_re = re.match(".*?(\d+).*", fav_nums)
        # if match_re:
        #     fav_nums = match_re.group(1)
        #
        # comment_nums = response.xpath("//a[@href='#article-comment']/span//text()").extract()[0]
        # match_re = re.match(".*?(\d+).*", comment_nums)
        # if match_re:
        #     comment_nums = match_re.group(1)
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

        # # ******************
        # # use css selector *
        # # ******************
        #
        # article_item = JobBoleAticleItem()
        # front_image_url = response.meta.get("front_image_url", "")
        # title = response.css(".entry-header h1::text").extract_first("")
        # create_date = response.css("p.entry-meta-hide-on-mobile::text").extract_first("").split()[0]
        # try:
        #     create_date = datetime.datetime.strptime(create_date, "%Y/%m/%d").date()
        # except Exception as e:
        #     create_date = datetime.datetime.now().date()
        # praise_nums = response.css("span.vote-post-up h10::text").extract_first("")
        # fav_nums = response.css("span.bookmark-btn::text").extract_first("")
        # match_re = re.match(".*?(\d+).*", fav_nums)
        # if match_re:
        #     fav_nums = int(match_re.group(1))
        # else:
        #     fav_nums = 0
        #
        # comment_nums = response.css("a[href*='#article-comment'] span::text").extract_first("")
        # match_re = re.match(".*?(\d+).*", comment_nums)
        # if match_re:
        #     comment_nums = int(match_re.group(1))
        # else:
        #     comment_nums = 0
        #
        # content = response.css("div.entry").extract_first("")
        #
        # tag_list = response.css("p.entry-meta-hide-on-mobile a::text").extract_first("")
        #
        # suffix = "评论"
        # tags = []
        # for tag in tag_list:
        #     if tag.encode("utf-8").strip().endswith(suffix):
        #         break
        #     else:
        #         tags.append(tag)
        #
        # article_item["title"] = title
        # article_item["url"] = response.url
        # article_item["url_object_id"] = get_md5(response.url)
        # article_item["tags"] = tags
        # article_item["front_image_url"] = [front_image_url]
        # # article_item["front_image_path"] = # get this varialbe in pipline
        # article_item["create_date"] = create_date
        # article_item["content"] = content
        # article_item["praise_nums"] = praise_nums
        # article_item["fav_nums"] = fav_nums
        # article_item["comment_nums"] = comment_nums

        # ************************
        # 通过item loader加载item *
        # ************************
        """
        1. item_loader常用的函数
        item_loader.add_css()
        item_loader.add_xpath()
        item_loader.add_value()
        2. 默认取值都是List对象
        """
        front_image_url = response.meta.get("front_image_url", "")  # 文章封面图
        item_loader = ItemLoader(item=JobBoleAticleItem(), response=response)
        item_loader.add_css("title", ".entry-header h1::text")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_css("create_date", "p.entry-meta-hide-on-mobile::text")
        item_loader.add_value("front_image_url", [front_image_url])
        item_loader.add_css("praise_nums", ".vote-post-up h10::text")
        item_loader.add_css("comment_nums", "a[href='#article-comment'] span::text")
        item_loader.add_css("fav_nums", ".bookmark-btn::text")
        item_loader.add_css("tags", "p.entry-meta-hide-on-mobile a::text")
        item_loader.add_css("content", "div.entry")

        article_item = item_loader.load_item()
        yield article_item
