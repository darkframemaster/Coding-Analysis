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

	def __init__(self):
		"""
		# Datastructure of commit_dic:
		# {'id_bytime':[commit,time,email,diff]}
		#
		# Datastructrue of __user_stats:
		# {'usr_name':{
		#			'addtions':,
		#			'deletions':,
		#			'total':,
		#			'contributes':,
		#			'commit times':,
		#			'email':
		#			}...
		# }
		#
		#	
		# self.__commit_dic and self.user_stats save all the information
		# of the repo.
		#
		# self.__user_stats_tmp should has the same structure as 
		# self.__user_stats and normally it is a part of it.
		"""
		self.__user_stats_tmp = {}

		self.__commit_dic = {}
		self.__user_stats = {}
		
		self.__init_commit_dic()	
		self.__user_stats = self.collect_user_stats(self.__commit_dic)

	def __init_commit_dic(self):	
		# Function get_commit_dic: 
		# Collecting all the commit's sha,commit's time,committer's email	
		# 
		# Notice the last commit is the first to deal with

		print('collecting commit data...')
		p_commit = re.compile("commit (\w+)")
		p_date = re.compile("Date:\s+(\S+ \S+ \S+ \S+ \S+)\s+(\S+)")
		p_email = re.compile("<\S+@\S+>")
		sha = ""
		commit_list = []
		time_list = []
		email_list = []

		while(sha != None):
			if sha:
				info = Git.log_next(sha=sha)
			else:
				info = Git.log_one(sha=sha)		
			try:	
				sha = p_commit.search(info).group(1)
				email = p_email.search(info).group(0)
				time = datetime.strptime(p_date.search(info).group(1),TIME_FORMAT['GIT_LOG'])
				commit_list.append(sha)
				time_list.append(time)
				email_list.append(email)			
			except Exception as error:
				logging.warning("First commit!")
				logging.warning(error)
				break

		lenth=len(commit_list)
		for i in range(0,lenth):
			if i<lenth-1:
				self.__commit_dic[lenth-i] = [commit_list[i], 
									time_list[i],
									email_list[i],
									(time_list[i]-time_list[i+1]).total_seconds()]
			else:
				self.__commit_dic[lenth-i] = [commit_list[i], time_list[i], email_list[i],-1]

	def __save_user_data(self, user, email, ins_data, del_data):
		# Save the data of the users
		# 
		# Params:
		#	user: The committer's name
		#	email: The committer's email
		# 	ins_data: The addition of the code in this commit
		# 	del_data: The deletion of the code in this commit

		if user in self.__user_stats_tmp:
			stats = self.__user_stats_tmp[user]
			stats['additions'] += ins_data
			stats['deletions'] += del_data
			stats['total'] += (ins_data + del_data)
			stats['commit_times'] += 1
			if email not in stats['email']:
				stats['email'].append(email)
			self.__user_stats_tmp[user] = stats
		else:
			new_stat = {'additions':ins_data, 
						'deletions':del_data, 
						'total':ins_data+del_data, 
						'contribute':ins_data*0.7+del_data*0.3, 
						'commit_times':1,
						'email':[email]
						}
			self.__user_stats_tmp[user] = new_stat
	

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
		return self.__user_stats_tmp
			
	def get_dic_by_time(self, st_time, ed_time):
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
			Example:
				time1 = datetime(2000,1,1)
				time2 = datetime.now()
				commits = get_dic_by_time(time1, time2)
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
			Example:
				time1 = datetime(2000,1,1)
				time2 = datetime.now()
				commits = get_time_list(time1, time2)
		"""
		if not isinstance(st_time,datetime) or not isinstance(ed_time,datetime):
			raise TypeError("st_time and ed_time require for datetime type.")
		
		time_list=[]
		for key in self.__commit_dic:
			if(st_time <= self.__commit_dic[key][1] <= ed_time):
					time_list.append(self.__commit_dic[key][1])	
		return time_list

	def show_commits(self):
		for i in self.__commit_dic:
			print(str(i)+": %s %s %s"%(self.__commit_dic[i][0], \
				self.__commit_dic[i][1].__reStr__(),self.__commit_dic[i][2]))

	def show_users(self):
		for i in self.__user_stats:
			print(i,': ',self.__user_stats[i])

	def get_commit_dic(self):
		return self.__commit_dic

	def get_user_stats(self):
		return self.__user_stats





