from scrapy.spiders import Spider
from scrapy.selector import Selector
from MITCrawler.items import CourseItem
from scrapy.loader import ItemLoader
from scrapy.http import Request
import re

class ocwMITSpider(Spider):
    name = 'ocwMITSpider'
    allowed_domains = ["http://ocw.mit.edu/courses/audio-video-courses/"]
    start_urls = ["http://ocw.mit.edu/courses/audio-video-courses/"]

    def parse(self, response):
        hxs = Selector(response)
        # links = hxs.xpath('//a/@href').extract()

        # crawled_links = []

        # link_pattern = re.compile("^(?:ftp|http|https):\/\/(?:[\w\.\-\+]+:{0,1}[\w\.\-\+]*@)?(?:[a-z0-9\-\.]+)(?::[0-9]+)?(?:\/|\/(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+)|\?(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+))?$")

        # for link in links:
        #     if link_pattern.match(link) and not link in crawled_links:
        #         crawled_links.append(link)
        #         yield Request(link, self.parse)

        l = ItemLoader(item=CourseItem(), response=response)
        l.add_xpath('number', '//table[@class="courseList"]/tbody/tr/td[0]/a[@rel="coursePreview"]/text()')
        l.add_xpath('title', '//table[@class="courseList"]/tbody/tr/td[1]/a[@rel="coursePreview"]/text()')
        l.add_xpath('level', '//table[@class="courseList"]/tbody/tr/td[2]/a[@rel="coursePreview"]/text()')
        return l.load_item()
        # titles = hxs.xpath('//a[@rel="coursePreview"]/text()').extract()
        # for title in titles:
        #     item = MITCrawlerItem()
        #     item['course'] = title.strip()
        #     yield item