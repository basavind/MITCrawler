from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request
from MITCrawler.items import Course
import re

ignored_materials = ['Course Home',
                     'Syllabus',
                     'Download Course Materials',
                     'References',
                     'Readings',
                     'Calendar',
                     'Lecture Summaries',
                     'This Course at MIT',
                     'Course Publicity',
                     'Tools',
                     'Related Resources',
                     'Image Gallery']
ignored_sublinks = 'this-course-at-mit'

valid_material_regex = r'/(\w*\.\b(pdf|srt|rm)\b)'

def clean(value):
    return re.sub('\s+', ' ', value).strip()


class ocwMITSpider(Spider):
    name = 'ocwMITSpider'
    allowed_domains = ["ocw.mit.edu"]
    start_urls = ["http://ocw.mit.edu/courses/"]

    def parse(self, response):
        hxs = Selector(response)
        for tr in hxs.xpath('//table[@class="courseList"]/tbody/tr'):
            href = clean(tr.xpath('td[2]/a[@rel="coursePreview"]/@href').extract()[0].strip())
            url = response.urljoin(href)
            yield Request(url, callback=self.parse_course_page)

    def parse_course_page(self, response):
        for link in response.xpath('//div[@id="course_nav"]//ul/li/a[@href!="#"]'):
            material = clean(link.xpath('text()').extract()[0])
            material_url = clean(link.xpath('@href').extract()[0])
            if material in ignored_materials or ignored_sublinks in response.url:
                continue
            url = response.urljoin(material_url)
            yield Request(url, callback=self.parse_materials)

    def parse_materials(self, response):
        for link in response.xpath('//div[@id="course_inner_section"]//a[@href]'):
            href = clean(link.xpath('@href').extract()[0])
            if re.search(valid_material_regex, href):
                section = clean(response.xpath('//div[contains(@id,"breadcrumb")]//a[3]/text()').extract()[0])
                section_url = response.urljoin(clean(response.xpath('//div[contains(@id,"breadcrumb")]//a[3]/@href').extract()[0]))
                course = clean(response.xpath('//div[contains(@id,"breadcrumb")]//a[4]/text()').extract()[0])
                course_url = response.urljoin(clean(response.xpath('//div[contains(@id,"breadcrumb")]//a[4]/@href').extract()[0]))
                material_section = clean(response.xpath('//div[@id="section_title"]/h1/span/text()').extract()[0])
                material_section_url = response.url
                material = re.search(valid_material_regex, href).group(1)
                material_url = response.urljoin(clean(link.xpath('@href').extract()[0]))
                item = Course()
                item['section'] = section
                item['section_url'] = section_url
                item['course'] = course
                item['course_url'] = course_url
                item['material_section'] = material_section
                item['material_section_url'] = material_section_url
                item['material'] = material
                item['material_url'] = material_url
                yield item