from scrapy.spiders import Spider
from scrapy import Request
from scrapy import Selector
from MITCrawler.items import Material
import re

ignored_material_types = ['Course Home',
                          'Syllabus',
                          'Download Course Materials',
                          'References',
                          'Calendar',
                          'Lecture Summaries',
                          'This Course at MIT',
                          'Course Publicity',
                          'Tools',
                          'Related Resources',
                          'Image Gallery']

valid_material_regex = r'/(\w*\.\b(pdf|srt)\b)'

parsed_paths = []

courses_list_selector = '//table[@class="courseList"]/tbody/tr/td[2]/a[@rel="coursePreview"]'

material_types_selector = '//div[@id="course_nav"]//ul/li/a[@href!="#"]'

breadcrumb_2_selector = '//div[contains(@id,"breadcrumb")]//a[2]'
breadcrumb_3_selector = '//div[contains(@id,"breadcrumb")]//a[3]'
breadcrumb_4_selector = '//div[contains(@id,"breadcrumb")]//a[4]'
breadcrumb_5_selector = '//div[contains(@id,"breadcrumb")]//a[5]'

title_selector = '//div[@id="section_title"]/h1/span/text()'

inner_links_selector = '//div[@id="course_inner_section"]//a[@href]'

def clean(value):
    '''
    Remove all extra spaces, tabulations, etc. from :value:
    :param value: str
    :return: str
    '''
    return re.sub('\s+', ' ', value).strip()

def extract_selector(response, selector):
    '''
    Returns extracted value from selector, applied for :response:,
    it may be string value or Selector object
    :param response: Selector object of Scrapy Crawler
    :param selector: valid xpath selector
    :return: str | Selector
    '''
    return clean(response.xpath(selector).extract()[0])

def extract_text(selector):
    '''
    Returns extracted text value from selector
    :param selector: valid xpath selector
    :return: str
    '''
    return clean(selector.xpath('text()').extract()[0])

def extract_link(response, selector):
    '''
    Returns full url link form selector, applied for :response:
    :param response: Selector object of Scrapy Crawler
    :param selector: valid xpath selector
    :return:
    '''
    link = clean(selector.xpath('@href').extract()[0])
    return response.urljoin(link)

class ocwMITSpider(Spider):
    name = 'ocwMITSpider'
    allowed_domains = ["ocw.mit.edu"]
    start_urls = ["http://ocw.mit.edu/courses/"]

    def parse(self, response):
        courses_list = response.xpath(courses_list_selector)
        for course_selector in courses_list:
            course_link = extract_link(response, course_selector)
            yield Request(course_link, callback=self.parse_material_types)

    def parse_material_types(self, response):
        material_types_list = response.xpath(material_types_selector)
        for material_type_selector in material_types_list:
            material_type = extract_text(material_type_selector)
            if material_type in ignored_material_types:
                continue
            material_type_link = extract_link(response, material_type_selector)
            yield Request(material_type_link, callback=self.parse_materials)

    def parse_materials(self, response):
        links_list = response.xpath(inner_links_selector)
        for link_selector in links_list:
            material_link = extract_link(response, link_selector)
            if re.search(valid_material_regex, material_link):
                section_selector = response.xpath(breadcrumb_2_selector)
                course_selector = response.xpath(breadcrumb_3_selector)
                breadcrumb_2_text = extract_text(response.xpath(breadcrumb_2_selector))
                if breadcrumb_2_text == 'Courses':
                    section_selector = response.xpath(breadcrumb_3_selector)
                    course_selector =  response.xpath(breadcrumb_4_selector)
                material_section = None
                try:
                    material_section = response.xpath(breadcrumb_5_selector)
                    material_section = extract_text(material_section)
                except IndexError:
                    pass
                finally:
                    pass
                section = extract_text(section_selector)
                course = extract_text(course_selector)
                material_type = extract_selector(response, title_selector)
                material_path = '/'.join([section, course, material_type])
                if material_section != None and len(material_section) > 0:
                    material_path = '/'.join([section,
                                              course,
                                              material_section,
                                              material_type])
                if material_path in parsed_paths:
                    continue
                parsed_paths.append(material_path)
                material = Material()
                material['path'] = material_path
                yield material