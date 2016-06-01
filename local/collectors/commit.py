#!/usr/bin/env python3
#-*- coding:utf-8 -*-

'''this scrpt for collecting the data from local .git directory'''

__author__='xuehao'

import re
import os
import sys
import logging
from datetime import datetime

from config import TIME_FORMAT,PROJECT_NAME
import mongodb
from ..doshell import Git


class CommitInfo(object):
# Class Info:Collecting the informations of the commit in the local repo.

	def __init__(self):
		# Datastructure of commit_dic:
		# {'id_bytime':{'sha': , 'time': ,'email': }}
		#
		# self.commit_times for count of all the commits,except those 			# filter out ones.
		self.repo_name = PROJECT_NAME
		self.__commit_dic = {}
	
	def __is_merge(self, sha):
		# when the sha taged a Merge commit then return True.	
		if sha:
			info = Git.log_one(sha=sha)
			p_merge = re.compile("Merge")
			if(p_merge.search(info) is not None):
				return True
			else:
				return False	
		return False

	def __save_in_mongo(self):
		# save commits info to mongodb database.
		commit_list = [self.__commit_dic[key] for key in self.__commit_dic]
		db = mongodb.Db(PROJECT_NAME)
		db.drop_commit()
		db.save_commits(commit_list)
		
	
	def init_commits(self, *, save_in_mongo=False, merge_filter=False):	
		# Function get_commit_dic: 
		# Collecting all the commit's sha,commit's time,committer's email	
		# 
		# Notice the last commit is the first to deal with

		print('collecting commit data...')
		p_commit = re.compile("commit (\w+)")
		p_date = re.compile("Date:\s+(\S+ \S+ \S+ \S+ \S+)\s+(\S+)")
		p_email = re.compile("<\S+@\S+>")
		sha = ""
		commit_times = 0

		while sha is not None:
			if sha:
				info = Git.log_next(sha=sha)
			else:
				info = Git.log_one(sha=sha)

			try:	
				sha = p_commit.search(info).group(1)
				if merge_filter and self.__is_merge(sha):
					logging.warning('merge %s'%sha)			
					continue
				email = p_email.search(info).group(0)
				time = datetime.strptime(p_date.search(info).group(1),TIME_FORMAT['GIT_LOG'])
				self.__commit_dic[commit_times] = {'sha':sha, 'time':time, 'email':email} 
				commit_times += 1		
			except Exception as error:
				logging.warning('First commit!')
				logging.warning(error)
				break
	
		self.__commit_dic={(commit_times-commit):self.__commit_dic[commit] 
						for commit in self.__commit_dic}

		if save_in_mongo:
			self.__save_in_mongo()
	
	
	def get_time_list(self, st_time, ed_time):
		"""
			Use this function to get a list of the commit_time from
			self.__commit_dic from st_time to ed_time.
			
			Params:
				datetime st_time: Start from st_time. 
				datetime ed_time: End by ed_time.
			Return:
				list time_list: all elements should be datetime instance.
		"""

		if not isinstance(st_time,datetime) or not isinstance(ed_time,datetime):
			raise TypeError("st_time and ed_time require for datetime type.")

		time_list=[]
		for key in self.__commit_dic:
			if(st_time <= self.__commit_dic[key]['time'] <= ed_time):
					time_list.append(self.__commit_dic[key]['time'])	
		return time_list


	def get_commits_by_time(self, st_time, ed_time):
		"""
			Use this function to get a part of the data from 
			self.__commit_dic from st_time to ed_time.
			
			Params:
				datetime st_time: Start from st_time. 
				datetime ed_time: End by ed_time.
			Return:
				dict data: part of the self.__commit_dic.
				Single element structure of data should be: 
				{index:[commit, time, email, diff]} 
		"""

		if not isinstance(st_time,datetime) or not isinstance(ed_time,datetime):
			raise TypeError("st_time and ed_time require for datetime type.")

		tmp={}
		for key in self.__commit_dic:
			if(st_time <= self.__commit_dic[key]['time'] <= ed_time):
					tmp[key] = self.__commit_dic[key]	
		return tmp

	
	def show_commits(self):
		"""
			Use this function to show up all the elements in 
			self.__commit_dic.
			
			Params:
				Not require.
			Return:
				None
		"""

		for i in self.__commit_dic:
			print(str(i)+": %s %s %s"%(self.__commit_dic[i]['sha'],
			self.__commit_dic[i]['time'], self.__commit_dic[i]['email']))
	
	def get_commits(self):
		return self.__commit_dic

