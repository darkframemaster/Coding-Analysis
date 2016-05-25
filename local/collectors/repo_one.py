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


class Collector(object):
# Class Info:Collecting the informations of the commit in the local repo.

	def __init__(self, ignore_commit=False, ignore_user=False, ignore_merge=False):
		# Datastructure of commit_dic:
		# {'id_bytime':[commit,time,email,diff]}
		#
		# Datastructrue of __user_stats:
		#  {'usr_name':{
		#			'addtions':,
		#			'deletions':,
		#			'total':,
		#			'commit times':,
		#			'email':
		#			}...
		# }
		self.__commit_dic = {}
		self.__user_stats = {}
				
		self.__init_data(ignore_commit, ignore_user, ignore_merge)

	''' Filters: Setting filters to ignore commits 
	All filters should return False for ignoring the commit.	
	'''
	def __merge_filter(self,sha):
		# Filter merge_filter: Ignore those commits that has 'Merge' mark.
		# return True when ignore.

		title = Git.log_one(sha=sha)
		p_merge = re.compile("Merge")
		if(p_merge.search(title) is not None):
			return True
		else:
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
			sha = info[7:47]
			stats = Git.diff_short(sha1 = sha, sha2 = "")
		return user,info[:200],stats

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

	def __save_commit_data(self, id_num, sha, time):
		# Save the data of the commit
		#
		# Params:
		#	id_num: The commit id from 1 to commit_times.
		#			(The last commit should be 1)
		#	sha: The hash code of the commit
		#	time: The time of the commit

		self.__commit_dic[id_num] = [sha, time]
	
	def __init_data(self, ignore_commit, ignore_user, ignore_merge):	
		# Function get_commit_dic: 
		# Init all the datas.

		print('collecting commit datas...')
		p_commit = re.compile("commit (\w+)")
		p_date = re.compile("Date:\s+(\S+ \S+ \S+ \S+ \S+)\s+(\S+)")
		p_email = re.compile("<\S+@\S+>")
		p_ins = re.compile("(\d+) insertion")
		p_del = re.compile("(\d+) deletion")

		sha = ""
		id_num = 0
		
		while(sha is not None):
			print(id_num, sha)
			ins_data = 0
			del_data = 0
			
			if ignore_merge and merge_filter(sha):
				continue
			else:
				user,info,stats = self.__get_info(sha)
			try:	
				sha = p_commit.search(info).group(1)
				email = p_email.search(info).group(0)
				time = datetime.strptime(p_date.search(info).group(1),TIME_FORMAT['GIT_LOG'])
				r_ins = p_ins.search(stats)
				r_del = p_del.search(stats)
				if r_ins is not None:
					ins_data = int(r_ins.group(1))
				if r_del is not None:
					del_data = int(r_del.group(1))
				if not ignore_commit:
					id_num += 1
					self.__save_commit_data(id_num, sha, time)	
				if not ignore_user:
					self.__save_user_data(user, email, ins_data, del_data)
			except Exception as error:
				logging.warning(error)
				print("First commit")	
				break

	
	def get_data_by_time(self, st_time, ed_time):
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
 
		data={}
		for key in self.__commit_dic:
			if(st_time <= self.__commit_dic[key][1] <= ed_time):
					data[key] = self.__commit_dic[key]	
		return data
		

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
			if(st_time <= self.__commit_dic[key][1] <= ed_time):
					time_list.append(self.__commit_dic[key][1])	
		return time_list
		

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
			print(str(i)+": %s %s %s"%(self.__commit_dic[i][0], \
				self.__commit_dic[i][1].__reStr__(),self.__commit_dic[i][2]))

	def show_users(self):
		"""
			Use this function to show up all the elements in 
			self.__user_stats.
			
			Params:
				Not require.
			Return:
				None
		"""
		for user in self.__user_stats:
			print(i,': ',self.__user_stats[user])

	
	def get_commit_dic(self):
		return self.__commit_dic
	
	def get_user_stats(self):
		return self.__user_stats



if __name__=='__main__':
	#init time
	st_time = datetime(2010,12,1,0,0,0)
	ed_time = datetime(2016,7,1,0,0,0)
	 
	#init commit 
	commit = Info()
	temp = commit.get_data_by_time(st_time,ed_time)
	
	#show up
	print(temp.get_commit_dic())

