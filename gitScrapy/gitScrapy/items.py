# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class testItem(scrapy.Item):
    	# define the fields for your item here like:
    	# name = scrapy.Field()
	city=scrapy.Field()
    	date=scrapy.Field()
	dayDesc=scrapy.Field()
	dayTemp=scrapy.Field()
	pass

class GitItem(scrapy.Item):
	commit=scrapy.Field()
	author=scrapy.Field()
	commiter=scrapy.Field()
	stats=scrapy.Field()

