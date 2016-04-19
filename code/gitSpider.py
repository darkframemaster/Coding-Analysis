#!/usr/bin/env python3
#-*- coding:utf-8 -*-

__author__='xuehao'

import logging;logging.basicConfig(level=logging.INFO)
import json
import requests
from config import ACCESS_TOKEN


class GitSpider(object):
	name=''
	start_url=''
	all_commit=0
	data={}
	user_stats={}

	def __init__(self,user='',repo=''):
		self.name='GIT:'+user+'/'+repo		
		self.start_url='https://api.github.com/repos/%s/%s/commits'%(user,repo)
		self.all_commit=0
		self.data={'__name__':repo}
		self.user_stats={'__name__':repo}
		logging.info('INITIAL OF %s'%self.name)
		print('get data from gitapi...')
	
	'''
	返回一个响应头和网页
	[head,html.text]
	'''
	def getSource(self,url='',params={'access_token':ACCESS_TOKEN}):
		if url=='':
			url=self.start_url
		if params!=None:
			html=requests.get(url,params=params)
		else:
			html=requests.get(url)
		head=html.headers
		return [head,json.loads(html.text)]

	'''
	接收一个response头作为参数
	剩余的api访问次数是否为0，返回False可以继续访问api
	'''
	def isRemain(self,head):
		print(head['X-RateLimit-Remaining'])
		if head['X-RateLimit-Remaining']=='0':
			return False
		return True

	
	'''
		getUserData:从给定的api url中获取commit中的stats信息
		input:
			url=''	这里的url为https://api.github.com/repos/name/reponame/commits/sha的形式
		output:
			None
	'''
	def getUserData(self,url=''):
		if url=='':
			return 
		else:
			page_info=self.getSource(url)
			if self.isRemain(page_info[0]):
				page_info=page_info[1]
				try:
					new_data={}
					new_stats={}
					committer=page_info['commit']['committer']['name']
					new_data['committer']=committer
					new_stats['total']=int(page_info['stats']['total'])
					new_stats['additions']=int(page_info['stats']['additions'])
					new_stats['deletions']=int(page_info['stats']['deletions'])
					new_data['stats']=new_stats
					if committer not in self.user_stats.keys():		
						self.user_stats[committer]=new_data
					else:
						self.user_stats[committer]['stats']['total']+=new_data['stats']['total']
						self.user_stats[committer]['stats']['deletions']+=new_data['stats']['deletions']
						self.user_stats[committer]['stats']['additions']+=new_data['stats']['additions']	
						print(self.user_stats[committer])
				except:
					logging.warning('MISSING data while loading user stats.')
			else:
				logging.warning('Limit arrival!') 


	'''
		getBaseData:从给定的api url中获取commit的基本信息
		input:
			url=self.start_url	
		output:
			None			
	'''
	def getBaseData(self,url=start_url):
		page_info=self.getSource(url=url)
		if self.isRemain(page_info[0]):
			page_info=page_info[1]
			'''
			获取 /repos/user/repo/commits 的commit信息
			'''
			try:
				for commit in page_info:
					new_data={}
					sha=commit['sha']
					new_data['sha']=sha
					new_data['committer']=commit['commit']['committer']
					self.data[sha]=new_data
			except:
				logging.warning('MISSING data while getting BaseData.')	
		else:
			logging.warning('Limit arrival!') 
			
		
	def getData(self):
		self.getBaseData()
		#同时获取每个commit的数据
		for sha in self.data:
			self.all_commit=self.all_commit+1
			next_url=self.start_url+'/'+sha
			self.getUserData(next_url)
		return self.all_commit
			

if __name__=='__main__':
	test=GitSpider(user='apple',repo='swift')	
	#print(test.getData())
	test.getBaseData()	
	print('---------------------data-------------------------')
	for i in test.data:
			print(test.data[i])
	print('---------------------stats------------------------')
	for i in test.user_stats:
			print(test.user_stats[i])
	
