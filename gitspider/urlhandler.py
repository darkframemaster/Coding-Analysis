#!/usr/bin/env python3
#-*- coding:utf-8 -*-

__author__='xuehao'

import logging;logging.basicConfig(level=logging.INFO)
import json
import requests
from datetime import datetime

from config import ACCESS_TOKEN,FINGERPRINT,CLIENT_ID,CLIENT_SECRET
from config import TIME_FORMAT



class GitApi():
	def __init__(self):
		self.__base_link = 'https://api.github.com'
		self.__api_links = {}

	def get_links(self):
		return self.__api_links

	def crawl_links(self):
		'''
		'''
		if self.is_ok(self.__base_link):
			head,page_info = self.get_source(self.__base_link)
			
			if self.is_remain(head):
				self.__api_links = page_info
		else:
			logging.warning('Check api url!!!')

		
	def is_ok(self, url):
		'''
		Use this function to confirm the status_code to the url is 200.
		
		Params:
			url: The target webpage
		Return:
			True: status_code == 200
			False: status_code != 200
		'''
		if url == '':
			return False
		status = requests.get(url).status_code
		if status == 200:
			return True
		return False

	def get_source(self, url, params={'access_token':ACCESS_TOKEN}):
		'''
		Use this function to get the information from GitApi.
		
		Params:
			url: The url of the api page.
			params: Other params using in the requests method.
		Return:
			Successd return head,data: 
				head: The head of the HTTP file.
				page_info: The data from the page.  
			else:
				return None		
		'''
		if params != None:
			html=requests.get(url, params=params)
		else:
			html=requests.get(url)
		if html.status_code == 200:	
			head = html.headers
			page_info = json.loads(html.text)
			return head,page_info

	def is_remain(self, head):
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
			logging.warning('Limit arrival! Please try again later!')
			return False
		return True

