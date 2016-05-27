#!/usr/bin/env python3
#-*- coding:utf-8 -*-

__author__='xuehao'

import logging;logging.basicConfig(level=logging.info)
import json
import requests
from datetime import datetime

from config import ACCESS_TOKEN,TIME_FORMAT


class RepoApi(GitApi):
	'''	
	name:GIT: yourgitname/reponame
	start_url: commits
	data={'sha': {'committer':{'name':name,'email':email,'date':date}}...}
	user_stats={'user':{}}
	'''		
	def __init__(self,user='',repo=''):
		self.__name='GIT:'+user+'/'+repo		
		self.__start_url='https://api.github.com/repos/%s/%s/commits'%(user,repo)
		self.__data={'__name__':self.__name}
		self.__user_stats={'__name__':self.__name}
		logging.warning('INITIAL OF %s'%self.__name)
		self.__getBaseData()


	'''
		getBaseData:api中获取/repos/user/repo/commits的基本信息
		input:
			url=self.__start_url	
		output:
			False(only failed)			
	'''
	def __getBaseData(self):
		logging.info('Getting basedata from %s'% self.__start_url)
		page_info=self.__getSource(self.__start_url)
		if self.__isRemain(page_info[0]):
			page_info=page_info[1]
			try:
				for commit in page_info:
					new_data={}
					new_data['committer']=commit['commit']['committer']
					sha=commit['sha']
					self.__data[sha]=new_data
			except:
				logging.warning('MISSING data while getting BaseData.')	
		else:
			logging.Error('Limit arrival!') 
			return False

	'''
		getUserData:从给定的api url中获取commit中的stats信息
		input:
			url=''	这里的url为https://api.github.com/repos/name/reponame/commits/sha的形式
		output:
			False(only failed).
	'''
	def __getUserStats(self,url=''):
		if url=='':
			return False
		else:
			logging.info('Getting data from %s'% url)
			page_info=self.__getSource(url)
			if self.__isRemain(page_info[0]):
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
					if committer not in self.__user_stats.keys():		
						self.__user_stats[committer]=new_data
					else:
						self.__user_stats[committer]['stats']['total']+=new_data['stats']['total']
						self.__user_stats[committer]['stats']['deletions']+=new_data['stats']['deletions']
						self.__user_stats[committer]['stats']['additions']+=new_data['stats']['additions']	
						#print(self.__user_stats[committer])
				except:
					logging.warning('MISSING data while loading user stats. LINK:%s'%url)
			else:
				logging.Error('Limit arrival!')
				return False

	#Public functions
	'''
		获取data中每个commit的数据
	'''
	def initUserStats(self):
		self.__user_stats={}
		for sha in self.__data:
			if sha!='__name__':
				next_url=self.__start_url+'/'+sha
				self.__getUserStats(next_url)
		
		
	'''
		getDataByTime :可以用该函数仅获得所需时间段内的数据		
	'''
	def initUserStatsByTime(self,st_time,ed_time):
		self.__user_stats={}
		for sha in self.__data:
			if sha!='__name__':
				time=datetime.strptime(self.__data[sha]['committer']['date'],TIME_FORMAT['GIT_API'])	
				if not (st_time <= time <= ed_time):
					next_url=self.__start_url+'/'+sha
					self.__getUserStats(next_url)					
				else:
					continue
			
	


	def show(self):
		print('---------------------data-------------------------')
		for i in self.__data:
			print(self.__data[i])
		print('---------------------stats------------------------')
		for i in self.__user_stats:
			print(self.__user_stats[i])	
	
	def getData(self):
		return self.__data

	def getName(self):
		return self.__name
	
	def getStartUrl(self):
		return self.__start_url
			
		

if __name__=='__main__':
	test=GitApiSpider(user='darkframemaster',repo='Coding-Analysis')	
	test.show()
	test.initUserStats()
	test.show()
	st_time=datetime(2015,10,1,0,0,0)
	end_time=datetime(2016,1,1,0,0,0)
	test.initUserStatsByTime(st_time,end_time)
	test.show()
	
