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


class Collector(object):
# Class Info:Collecting the informations of the commit in the local repo.

	def __init__(self):
		"""
		# Datastructure of commit_dic:
		# {...,sha:{'commit':{'name': ,'email': ,'time': },...}
		#
		# Datastructrue of __user_stats:
		# {...
		# 'usr_name':{
		#		'stats':{'addtions':,'deletions':,'total':,'commit times':},
		#		'email': 
		#		},
		# ...}
		"""
		self.name = PROJECT_NAME
		self.__commit_dic = {}
		self.__user_stats = {}
				

	def __merge_filter(self,info):
		# Filter merge_filter: Ignore those commits that has 'Merge' mark.
		# return True when ignore.
		if sha:
			p_merge = re.compile("Merge")
			if(p_merge.search(info) is not None):
				logging.warning('Merge commit!')
				return True
			else:
				return False	
		return False

	def __get_info(self, sha):
		# Get the information of a commit. 
		#
		# Params: 
		#	sha: Hash code of commit.
		#	igonre_merge: If you want to ignore those merged commit
		#			set this to True
		# Return:
		#	user,info: user for the committer of this commit
		#			info for the information will be used to collect datas.
			
		user = Git.show_format(format_='%an',sha=sha).strip(' \t\n\r')
		if sha != "": 
			info = Git.log_next(sha = sha)				
			stats = Git.diff_short(sha1 = sha, sha2 = sha+"^")
		else:
			info = Git.log_one(sha = sha)
			stats = Git.diff_short(sha1 = sha, sha2 = "")
		return user,info[:200],stats

	def __save_user(self, user, email, ins_data, del_data):
		# Save the data of the users
		# 
		# Params:
		#	user: The committer's name
		#	email: The committer's email
		# 	ins_data: The addition of the code in this commit
		# 	del_data: The deletion of the code in this commit

		if user in self.__user_stats:
			stats = self.__user_stats[user]
			stats['stats']['additions'] += ins_data
			stats['stats']['deletions'] += del_data
			stats['stats']['total'] += (ins_data + del_data)
			stats['stats']['commit_times'] += 1
			if email not in stats['email']:
				stats['email'].append(email)
			self.__user_stats[user] = stats
		else:
			new_stat = {'stats':{'additions':ins_data, 
								'deletions':del_data, 
								'total':ins_data+del_data, 
								'commit_times':1},
						'email':[email]
						}
			self.__user_stats[user] = new_stat

	def __save_commit(self, sha, user, time, email):
		# Save the data of the commit
		#
		# Params:
		#	sha: The hash code of the commit
		#	user: The user who make the commit
		#	time: The time of the commit
		#	email: The email of the user
		new_commit = {}
		new_commit['committer'] = {'name':user,'email':email,'time':time}  
		self.__commit_dic[sha] = new_commit
	
	def __save_in_mongo(self):
		# Save the data in mongodb after init
		# 
		# Database is named by PROJECT_NAME
		# Collections for commits and users are named as 'commit' and 'user'
		 
		db = mongodb.Db(PROJECT_NAME)
		db.drop_commit()
		db.drop_user()
		for key in  self.__commit_dic:
			commit = {'sha':key,
					'committer':self.__commit_dic[key]['committer']}
			db.save_commit(commit)
		for key in self.__user_stats:
			user = {'name':key,
					'email':self.__user_stats[key]['email'],
					'stats':self.__user_stats[key]['stats']}
			db.save_user(user)
				
	
	def init_data(self, *, ignore_merge=False,  save_in_mongo=False):	
		"""
		Init all the datas of commits and users
			
		Params:
		key params:
			ignore_merge (False): Set this to True to ignore those merge commits.
			save_in_mongo (False): Set this to True to save the datas to mongodb. 
		
		Return:
			None
		"""

		print('collecting commit datas...')
		p_commit = re.compile("commit (\w+)")
		p_date = re.compile("Date:\s+(\S+ \S+ \S+ \S+ \S+)\s+(\S+)")
		p_email = re.compile("<\S+@\S+>")
		p_ins = re.compile("(\d+) insertion")
		p_del = re.compile("(\d+) deletion")

		sha = ""
		id_num = 0
		
		while(sha is not None):
			# print(sha)
			ins_data = 0
			del_data = 0
			
			user,info,stats = self.__get_info(sha)
			try:	
				sha = p_commit.search(info).group(1)
				if ignore_merge and __is_merge(info):
					continue
				email = p_email.search(info).group(0)
				time = datetime.strptime(p_date.search(info).group(1),TIME_FORMAT['GIT_LOG'])
				r_ins = p_ins.search(stats)
				r_del = p_del.search(stats)
				if r_ins is not None:
					ins_data = int(r_ins.group(1))
				if r_del is not None:
					del_data = int(r_del.group(1))
				self.__save_user(user, email, ins_data, del_data)
				self.__save_commit(sha, user, time, email)
			except Exception as error:
				logging.warning(error)
				print("First commit")	
				break
		if save_in_mongo:
			self.__save_in_mongo()

	
	def get_commits_by_time(self, st_time, ed_time):
		"""
			Use this function to get a part of the data from 
			self.__commit_dic from st_time to ed_time.
			
			Params:
				datetime st_time: Start from st_time. 
				datetime ed_time: End by ed_time.
			Return:
				tmp: part of the self.__commit_dic.
		"""
			
		if not isinstance(st_time,datetime) or not isinstance(ed_time,datetime):
			raise TypeError("st_time and ed_time require for datetime type.")
 
		tmp={}
		for key in self.__commit_dic:
			cur_time = self.__commit_dic[key]['committer']['time']
			if(st_time <= cur_time <= ed_time):
					tmp[key] = self.__commit_dic[key]	
		return tmp

	def get_commit_by_user(self, username):
		"""
			Get the commit made by user named 'username'
			
			Params:
				username: The name of the user.
			Return:
				tmp: A part of the self.__commit_dic.
		"""
		if username:
			tmp = {}
			for key in self.__commit_dic:
				if self.__commit_dic['committer']['name'] == username:
					tmp[key] = self.__commit_dic[key]
			return tmp	
		else:
			return {}

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
			cur_time = self.__commit_dic[key]['committer']['time']
			if(st_time <= cur_time <= ed_time):
					time_list.append(cur_time)	
		return time_list


	def get_commits(self):
		return self.__commit_dic
	
	def get_users(self):
		return self.__user_stats



