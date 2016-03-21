# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Course(scrapy.Item):
    material_url = scrapy.Field()
    material = scrapy.Field()
    material_section_url = scrapy.Field()
    material_section = scrapy.Field()
    course_url = scrapy.Field()
    course = scrapy.Field()
    section_url = scrapy.Field()
    section = scrapy.Field()

class Material(scrapy.Item):
    path = scrapy.Field()
