#!/usr/bin/env python3
#-*- coding:utf-8 -*-

'''this scrpt for collecting the data from local .git directory'''

__author__='xuehao'

import re
import os
import sys
import logging
from datetime import datetime

from config import TIME_FORMAT
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
		self.__user_stats={}		
	
	def merge_filter(self,sha):
		# Filter merge_filter: Ignore those commits that has 'Merge' mark.
		title = Git.log_one(sha=sha)
		p_merge = re.compile("Merge")
		if(p_merge.search(title) is not None):
			return False
		else:
			return True

	def time_filter(self,diff,limit=3600):
		# Filter time_filter: Ignore those commits that commit in a shot time
		# Param limit is setting for the shot time range.
		print(type(diff))
		if(diff==-1 or diff==-1):
			return False			
		elif(diff<limit):
			return False
		else:
			print('Time')
			return True


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
			stats['additions'] += ins_data
			stats['deletions'] += del_data
			stats['total'] += (ins_data + del_data)
			stats['commit_times'] += 1
			if email not in stats['email']:
				stats['email'].append(email)
			self.__user_stats[user] = stats
		else:
			new_stat = {'additions':ins_data, 
						'deletions':del_data, 
						'total':ins_data+del_data, 
						'contribute':ins_data*0.7+del_data*0.3, 
						'commit_times':1,
						'email':[email]
						}
			self.__user_stats[user] = new_stat
	

	def collect_user_stats(self,commit_dic):
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
			commits = info.get_dic_by_time(st_time,ed_time) 
			data = info.collect_user_stats(commits)	
		"""
		print("collecting user's data...")
		p_ins = re.compile("(\d+) insertion")
		p_del = re.compile("(\d+) deletion")
		
		for key in commit_dic:	
			ins_data = 0
			del_data = 0
			sha = commit_dic[key][0]
			email = commit_dic[key][2]
			user = Git.show_format(format_='%an',sha=sha).strip(' \t\n\r')

			if(key == 1):
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

	def get_user_stats(self):
		return self.__user_stats

	def show_users(self):
		for i in self.__user_stats:
			print(i,': ',self.__user_stats[i])


	
	
