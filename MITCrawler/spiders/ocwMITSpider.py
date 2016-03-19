from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request
from MITCrawler.items import Course
import re


def clean(value):
    return re.sub('\s+', ' ', value).strip()


class ocwMITSpider(Spider):
    name = 'ocwMITSpider'
    allowed_domains = ["http://ocw.mit.edu/courses/"]
    start_urls = ["http://ocw.mit.edu/courses/"]

    def parse(self, response):
        hxs = Selector(response)
        for tr in hxs.xpath('//table[@class="courseList"]/tbody/tr'):
            item = Course()
            number = clean(tr.xpath('td[1]/a[@rel="coursePreview"]/text()').extract()[0]).strip()
            item['title'] = number + ' ' + clean(tr.xpath('td[2]/a[@rel="coursePreview"]/text()').extract()[0].strip())
            item['url'] = 'http://ocw.mit.edu' + clean(tr.xpath('td[2]/a[@rel="coursePreview"]/@href').extract()[0].strip())
            yield (item)
