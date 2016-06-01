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


class UserInfo(object):	
# class coder: Collecting user's informations.

	def __init__(self):
		'''
		# Datastructrue of __user_stats:
		#  {'usr_name':{
		#			'addtions':,
		#			'deletions':,
		#			'total':,
		#			'contributes':,
		#			'commit times':,
		#			'email':
		#			}...
		# }
		'''
		self.repo_name = PROJECT_NAME
		self.__user_stats={}		

	def __save_in_mongo(self):
		db = mongodb.Db(PROJECT_NAME)
		db.drop_user()
		for key in self.__user_stats:
			user = {'name':key,
					'email':self.__user_stats[key]['email'],
					'stats':self.__user_stats[key]['stats']}
			db.save_user(user)
			

	def __save_user_data(self, user, email, ins_data, del_data):
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
	

	def init_users(self, commit_dic, *, save_in_mongo=False):
		"""
		# Function collect_stats: 
		# Collecting user's information from the commit_dic.
		# 
		# The information includes:
		# additions,deletions,total codelines,commit times,email.
		# 
		# Params:
		#	commit_dic: Any dict has the same struct of self.__commit_dic

		Normally the function should use like this:
			info = Collector()
			commits = info.get_commits_by_time(st_time,ed_time) 
			data = info.init_users(commits)	
		"""
		print("collecting user's data...")
		p_ins = re.compile("(\d+) insertion")
		p_del = re.compile("(\d+) deletion")
		
		for key in commit_dic:	
			ins_data = 0
			del_data = 0
			sha = commit_dic[key]['sha']
			email = commit_dic[key]['email']
			user = Git.show_format(format_='%an',sha=sha).strip(' \t\n\r')

			if(key == 0):
				data = Git.diff_short(sha1=sha,sha2="")
			else:
				data = Git.diff_short(sha1=sha,sha2=sha+"^")
			
			r_ins = p_ins.search(data)
			r_del = p_del.search(data)
			if(r_ins is not None):
				ins_str = r_ins.group(1)
				ins_data = int(ins_str)
			if(r_del is not None):
				del_str = r_del.group(1)
				del_data = int(del_str)
			self.__save_user_data(user, email, ins_data, del_data)
		
		if save_in_mongo:
			self.__save_in_mongo()
 

	def get_users(self):
		return self.__user_stats

	def show_users(self):
		for i in self.__user_stats:
			print(i,': ',self.__user_stats[i])


	
	
