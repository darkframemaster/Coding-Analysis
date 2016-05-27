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

	def __init__(self, save_inmongo=False):
		# Datastructure of commit_dic:
		# {'id_bytime':[commit,time,email,diff]}
		self.name = PROJECT_NAME
		self.__commit_dic={}
				
		self.__init_commit_dic(save_inmongo)	#init operations	

	
	def __init_commit_dic(self, save_inmongo):	
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

		while(sha!=None):
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
				logging.warning('First commit!')
				logging.warning(error)
				break

		lenth=len(commit_list)
		for i in range(0,lenth):
			if i<lenth-1:
				self.__commit_dic[lenth-i] = [commit_list[i], time_list[i], email_list[i], (time_list[i]-time_list[i+1]).total_seconds()]
			else:
				self.__commit_dic[lenth-i] = [commit_list[i], time_list[i], email_list[i],-1]

		if save_inmongo:
			commit_list = [{'sha':self.__commit_dic[key][0],
						'time':self.__commit_dic[key][1],
						'email':self.__commit_dic[key][2]} 
						for key in self.__commit_dic]
			db = mongodb.Db(PROJECT_NAME)
			db.save_commits(commit_list)
	

	def get_commit_dic(self):
		return self.__commit_dic

	
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
				self.__commit_dic[i][1], self.__commit_dic[i][2]))

	
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
		

		
