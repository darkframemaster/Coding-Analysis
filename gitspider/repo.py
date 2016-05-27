#!/usr/bin/env python3
#-*- coding:utf-8 -*-

__author__='xuehao'

import logging;logging.basicConfig(level=logging.INFO)
from datetime import datetime

from config import ACCESS_TOKEN,TIME_FORMAT
from .urlhandler import GitApi



class RepoApi(GitApi):
		
	def __init__(self,user='',repo=''):
		'''
		__init__ func.
			
		Params:
			user: The user's name of the repo
			repo: The repo_name.

		Values:
			self.name: 
				'GIT: yourgitname/reponame'
			self.__start_url: 
				repo_commits api link.
				https://api.github.com/repos/{name}/{reponame}/commits
			self.__commit_dic: 
				{'sha':{'committer':{'name': ,'email': ,'date': }}}
			self.__user_stats: 
				{'user':{}}
		'''
		self.name = 'GIT:'+user+'/'+repo		
		self.__start_url = 'https://api.github.com/repos/{user}/{repo}/commits'.format(user=user,repo=repo)
		self.__commit_dic = {}
		self.__user_stats = {}
		if not self.is_ok(self.__start_url):
			logging.error('Link error! Check your user and repo!')	
		else:
			logging.info('Initial of %s'%self.name)
			self.__get_base_data()


	def __get_base_data(self):
		# Use this function to collect commit data from gitapi.

		logging.info('Getting basedata from %s'% self.__start_url)
		head,page_info = self.get_source(self.__start_url)
		if self.is_remain(head):
			try:
				for commit in page_info:
					new_data={}
					new_data['committer']=commit['commit']['committer']
					sha=commit['sha']
					self.__commit_dic[sha]=new_data
				return True
			except Exception as error:
				raise error
				logging.warning('MISSING data while getting BaseData.')
				return False	
		else:
			logging.warning('Limit arrival! Please try again later!')
			return False 

	
	def __get_user_stats(self,url=''):
		# This function	for collecting user's stats from url.
		# url should format like this:
		#	https://api.github.com/repo/user/reponame/commits/sha
				
		if url=='':
			return False
		else:
			logging.info('Getting data from %s'% url)
			head,page_info = self.get_source(url) 
			if self.is_remain(head):
				try:
					new_stats={}
					committer=page_info['commit']['committer']['name']
					new_stats['total']=int(page_info['stats']['total'])
					new_stats['additions']=int(page_info['stats']['additions'])
					new_stats['deletions']=int(page_info['stats']['deletions'])
					if committer in self.__user_stats.keys():		
						self.__user_stats[committer]['stats']['total']+=new_data['stats']['total']
						self.__user_stats[committer]['stats']['deletions']+=new_data['stats']['deletions']
						self.__user_stats[committer]['stats']['additions']+=new_data['stats']['additions']	
					else:
						new_user={}
						new_user['committer']=committer
						new_user['email']=page_info['commit']['committer']['email']
						new_user['stats']=new_stats
						self.__user_stats[committer]=new_user
					return True
				except Exception as error:
					logging.warning(error)
					logging.warning('MISSING data while loading user stats. LINK:%s'%url)
					return False
			else:
				logging.Error('Limit arrival! Please try again later')
				return False
				
	def init_user_stats(self):
		self.__user_stats={}
		for sha in self.__commit_dic:
			next_url=self.__start_url+'/'+sha
			if not self.get_user_stats(next_url):
				return False
		
	def init_user_stats_by_time(self, st_time, ed_time):
		self.__user_stats={}
		for sha in self.__commit_dic:
			time=datetime.strptime(self.__commit_dic[sha]['committer']['date'],TIME_FORMAT['GIT_API'])	
			if st_time <= time <= ed_time:
				next_url=self.__start_url+'/'+sha
				if not self.get_user_stats(next_url):
					return False					

	def get_data(self):
		return self.__commit_dic

	def get_data_by_time(self, st_time, ed_time):
		tmp = {}
		for sha in self.__commit_dic:
			time = datetime.strptime(self.__commit_dic[sha]['committer']['date'],TIME_FORMAT['GIT_API'])
			if st_time <= time <= ed_time:
				tmp[sha] = self.__commit_dic[sha]
		return tmp

	def get_user_stats():
		return self.__user_stats

	def show(self):
		print('---------------------data-------------------------')
		for i in self.__commit_dic:
			print(self.__commit_dic[i])
		print('---------------------stats------------------------')
		for i in self.__user_stats:
			print(self.__user_stats[i])	
	
	
	
