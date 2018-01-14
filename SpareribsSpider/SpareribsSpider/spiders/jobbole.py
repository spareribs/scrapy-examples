# -*- coding: utf-8 -*-
import re
import scrapy


class JobboleSpider(scrapy.Spider):
    name = "jobbole"
    allowed_domains = ["blog.jobbole.com"]
    start_urls = ['http://blog.jobbole.com/113367/']

    def parse(self, response):
        # ********************
        # use xpath selector *
        # ********************
        title = response.xpath("//div[@class='entry-header']/h1/text()").extract()
        create_date = response.xpath("//p[@class='entry-meta-hide-on-mobile']//text()").extract()[0].split()[0]
        prasise_nums = response.xpath("//span[contains(@class,'vote-post-up')]//text()").extract()[1]
        fav_nums = response.xpath("//span[contains(@class,'bookmark-btn')]//text()").extract()[0]
        match_re = re.match(".*?(\d+).*", fav_nums)
        if match_re:
            fav_nums = match_re.group(1)

        commonts_nums = response.xpath("//a[@href='#article-comment']/span//text()").extract()[0]
        match_re = re.match(".*?(\d+).*", commonts_nums)
        if match_re:
            commonts_nums = match_re.group(1)

        content = response.xpath("//div[@class='entry']").extract()[0]

        tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a//text()").extract()

        # # Python2 error
        # tag_list = [element for element in tag_list if not element.encode("utf-8").strip().endswitch("评论".decode("utf-8"))]
        # tags = ",".join(tag_list)

        suffix = "评论"
        tags = []
        for tag in tag_list:
            if tag.encode("utf-8").strip().endswith(suffix):
                break
            else:
                tags.append(tag)

        # ******************
        # use css selector *
        # ******************
        title = response.css(".entry-header h1::text").extract_first()
        create_date = response.css("p.entry-meta-hide-on-mobile::text").extract_first().split()[0]
        prasise_nums = response.css("span.vote-post-up h10::text").extract_first()
        fav_nums = response.css("span.bookmark-btn::text").extract_first()
        match_re = re.match(".*?(\d+).*", fav_nums)
        if match_re:
            fav_nums = match_re.group(1)

        commonts_nums = response.css("a[href*='#article-comment'] span::text").extract_first()
        match_re = re.match(".*?(\d+).*", commonts_nums)
        if match_re:
            commonts_nums = match_re.group(1)

        content = response.css("div.entry").extract_first()

        tag_list = response.css("p.entry-meta-hide-on-mobile a::text").extract_first()

        # # Python2 error
        # tag_list = [element for element in tag_list if not element.encode("utf-8").strip().endswitch("评论".decode("utf-8"))]
        # tags = ",".join(tag_list)

        suffix = "评论"
        tags = []
        for tag in tag_list:
            if tag.encode("utf-8").strip().endswith(suffix):
                break
            else:
                tags.append(tag)

        pass
