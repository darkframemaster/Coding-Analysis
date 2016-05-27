#!/usr/bin/env python3
#-*- coding:utf-8 -*-

__author__='xuehao'

import logging;logging.basicConfig(level=logging.WARNING)
import json
import requests
from datetime import datetime

from code.config import ACCESS_TOKEN,TIME_FORMAT

class GitApi():
	def __init__(self):
		self.__base_link = 'https://api.github.com'
	
	def __get_source(self, url='', params={'access_token':ACCESS_TOKEN}):
		'''
		Use this function to get the information from GitApi.
		
		Params:
			url: The url of the api page.
			params: Other params using in the requests method.
		Return:
			[]: list[0] the head of the HTTP file.
				list[1] the data from the page.  
		'''
		if url == '':
			url=self.__start_url
		if params != None:
			html=requests.get(url,params=params)
		else:
			html=requests.get(url)
		head=html.headers
		return [head,json.loads(html.text)]

	def __isRemain(self, head):
		'''
		Use this function to confirm Remaining>0 so you can get the data.
		
		Params: 
			head: The head of the HTTP file.
		Return:
			True: For X-RateLimit-Remaining > 0
			False: For X-RateLimit-Remaining <= 0
		'''
		print(head['X-RateLimit-Remaining'])
		if head['X-RateLimit-Remaining']=='0':
			logging.warning('Remaining run out!')
			return False
		return True
