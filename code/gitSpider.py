#!/usr/bin/env python3
#-*- coding:utf-8 -*-

__author__='xuehao'

import logging;logging.basicConfig(level=logging.WARNING)
import json
import requests
from gitTime import *
from config import ACCESS_TOKEN


class GitApiSpider(object):
	'''	
	name:GIT: yourgitname/reponame
	start_url: commits
	data={'sha': {'committer':{'name':name,'email':email,'date':date}}...}
	user_stats={'user':{}}
	'''		
	name=''
	start_url=''
	data={}
	user_stats={}

	def __init__(self,user='',repo=''):
		self.name='GIT:'+user+'/'+repo		
		self.start_url='https://api.github.com/repos/%s/%s/commits'%(user,repo)
		self.data={'__name__':self.name}
		self.user_stats={'__name__':self.name}
		logging.info('INITIAL OF %s'%self.name)
		self.getBaseData()
	

	'''
		getBaseData:api中获取/repos/user/repo/commits的基本信息
		input:
			url=self.start_url	
		output:
			None			
	'''
	def getBaseData(self):
		logging.info('Getting basedata from %s'% self.start_url)
		page_info=self.getSource(self.start_url)
		if self.isRemain(page_info[0]):
			page_info=page_info[1]
			try:
				for commit in page_info:
					new_data={}
					new_data['committer']=commit['commit']['committer']
					sha=commit['sha']
					self.data[sha]=new_data
			except:
				logging.warning('MISSING data while getting BaseData.')	
		else:
			logging.warning('Limit arrival!') 




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
			logging.info('Getting data from %s'% url)
			page_info=self.getSource(url)
			if self.isRemain(page_info[0]):
				page_info=page_info[1]
				try:
					new_data={}
					new_stats={}
					committer=page_info['commit']['committer']['name']
					new_stats['total']=int(page_info['stats']['total'])
					new_stats['additions']=int(page_info['stats']['additions'])
					new_stats['deletions']=int(page_info['stats']['deletions'])
					new_data['committer']=committer
					new_data['email']=page_info['commit']['committer']['email']
					new_data['stats']=new_stats
					if committer not in self.user_stats.keys():		
						self.user_stats[committer]=new_data
					else:
						self.user_stats[committer]['stats']['total']+=new_data['stats']['total']
						self.user_stats[committer]['stats']['deletions']+=new_data['stats']['deletions']
						self.user_stats[committer]['stats']['additions']+=new_data['stats']['additions']	
						#print(self.user_stats[committer])
				except:
					logging.warning('MISSING data while loading user stats. LINK:%s'%url)
			else:
				logging.warning('Limit arrival!')
				return 

	'''
		获取data中每个commit的数据
	'''
	def getData(self):
		self.user_stats={}
		for sha in self.data:
			if sha!='__name__':
				next_url=self.start_url+'/'+sha
				self.getUserData(next_url)
		
		
	'''
		getDataByTime :可以用该函数仅获得所需时间段内的数据		
	'''
	def getDataByTime(self,st_time,ed_time):
		self.user_stats={}
		time=Time()
		for sha in self.data:
			if sha!='__name__':
				time.set_api(self.data[sha]['committer']['date'])	
				if time.cmp_with(st_time) and time.cmp_with(end_time)!=True:
					next_url=self.start_url+'/'+sha
					self.getUserData(next_url)					
				else:
					continue
			
	
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
			print(head)
			return False
		return True

	def show(self):
		#print('---------------------data-------------------------')
		#for i in self.data:
		#	print(self.data[i])
		print('---------------------stats------------------------')
		for i in self.user_stats:
			print(self.user_stats[i])
	


		
	
			
		

if __name__=='__main__':
	test=GitApiSpider(user='darkframemaster',repo='Coding-Analysis')	
	test.show()
	test.getData()
	test.show()
	st_time=Time(2015,10,1,0,0,0)
	end_time=Time(2016,1,1,0,0,0)
	test.getDataByTime(st_time,end_time)
	test.show()
	
