#!/usr/bin/env python2
import scrapy
from gitScrapy.items import testItem

class testSpider(scrapy.Spider):
	name="test"
	allowed_domains=["sina.com.cn"]
	start_urls=['http://weather.sina.com.cn']
	
	def parse(self,response):
		item=testItem()
		item['city']=response.xpath('//*[@id="slider_ct_name"]/text()').extract()
		tenDay=response.xpath('//*[@id="blk_fc_c0_scroll"]');
		item['date']=tenDay.css('p.wt_fc_c0_i_date::text').extract()
		item['dayDesc']=tenDay.css('img.icons0_wt::attr(title)').extract()
		item['dayTemp']=tenDay.css('p.wt_fc_c0_i_temp::text').extract()
		return item
