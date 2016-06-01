#!/usr/bin/env python3
#-*- coding:utf-8 -*-

__author__='xuehao'

import logging;logging.basicConfig(level=logging.INFO)
from datetime import datetime

from config import ACCESS_TOKEN,TIME_FORMAT
from .urlhandler import GitApi



class RepoApi(GitApi):
		
	def __init__(self,user,repo):
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


	def __crawl_commits(self, page_info):
		# Use this function to collect commit data from gitapi.
		try:
			for commit in page_info:
				new_data = {}
				new_data['committer'] = commit['commit']['committer']
				sha = commit['sha']
				self.__commit_dic[sha] = new_data
		except Exception as error:
			raise error
			logging.warning('MISSING data while getting BaseData.')	
	
	def __crawl_users(self, page_info):
		# This function	for collecting user's stats from url.
		# url should format like this:
		#	https://api.github.com/repo/user/reponame/commits/sha
					
		try:
			new_stats={}
			committer=page_info['commit']['committer']['name']
			email = page_info['commit']['committer']['email']
			new_stats['total']=int(page_info['stats']['total'])
			new_stats['additions']=int(page_info['stats']['additions'])
			new_stats['deletions']=int(page_info['stats']['deletions'])
			if committer in self.__user_stats.keys():		
				self.__user_stats[committer]['stats']['total']+=new_stats['total']
				self.__user_stats[committer]['stats']['deletions']+=new_stats['deletions']
				self.__user_stats[committer]['stats']['additions']+=new_stats['additions']	
				if email not in self.__user_stats['email']:
					self.__user_stats['email'].append(email)
			else:
				new_user={}
				new_user['committer'] = committer
				new_user['email'] = [email]
				new_user['stats'] = new_stats
				self.__user_stats[committer] = new_user
		except Exception as error:
			raise error
			logging.warning('MISSING data while loading user stats. LINK:%s'%url)

	
	def init_commits(self):
		if not self.is_ok(self.__start_url):
			logging.error('Link error! Check your user and repo!')	
		else:
			logging.info('Initial of %s'%self.name)
			logging.info('Getting commits data from %s'% self.__start_url)

			head,page_info = self.get_source(self.__start_url)
			if self.is_remain(head):
				self.__crawl_commits(page_info)
				return True
			else:
				return False 

	def init_users(self):
		self.__user_stats={}
		for sha in self.__commit_dic:
			next_url=self.__start_url+'/'+sha
			logging.info('Getting user data from %s'% next_url)
			
			head,page_info = self.get_source(next_url) 
			if self.is_remain(head):
				self.__crawl_users(page_info)
			else:
				return False
		return True
		
	def init_users_by_time(self, st_time, ed_time):
		self.__user_stats={}
		for sha in self.__commit_dic:
			time=datetime.strptime(self.__commit_dic[sha]['committer']['date'],TIME_FORMAT['GIT_API'])	
			if st_time <= time <= ed_time:
				next_url=self.__start_url+'/'+sha
				logging.info('Getting user data from %s'% next_url)
			
				head,page_info = self.get_source(next_url) 
				if self.is_remain(head):
					self.__crawl_users(page_info)
				else:
					return False
		return True
								


	def get_commits(self):
		return self.__commit_dic

	def get_commits_by_time(self, st_time, ed_time):
		tmp = {}
		for sha in self.__commit_dic:
			time = datetime.strptime(self.__commit_dic[sha]['committer']['date'],TIME_FORMAT['GIT_API'])
			if st_time <= time <= ed_time:
				tmp[sha] = self.__commit_dic[sha]
		return tmp

	def get_users():
		return self.__user_stats

	def show(self):
		print('---------------------data-------------------------')
		for i in self.__commit_dic:
			print(i,self.__commit_dic[i])
		print('---------------------stats------------------------')
		for i in self.__user_stats:
			print(self.__user_stats[i])	
	
	
	
