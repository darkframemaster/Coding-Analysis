# -*- coding: utf-8 -*-

# Scrapy settings for gitScrapy project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'gitScrapy'

SPIDER_MODULES = ['gitScrapy.spiders']
NEWSPIDER_MODULE = 'gitScrapy.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'gitScrapy (+http://www.yourdomain.com)'
USER_AGENT='User-Agent:Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'

DEFAULT_REQUEST_HEADERS={
	'Referer':'http://www.weibo.com'
}

ITEM_PIPELINES={
	'gitScrapy.pipelines.testPipeline':1
}

DOWNLOAD_DELAY=0.5	#设置下载间隔
