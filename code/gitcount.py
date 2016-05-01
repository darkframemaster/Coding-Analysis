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
from doshell import Git


class Info(object):
# Class Info:Collecting the informations of the commit in the local repo.

	def __init__(self):
		# Datastructure of commit_dic:
		# {'id_bytime':[commit,time,email,diff]}
		# 	
		# Initial operations.
		
		self.__commit_dic={}				
		self.__init_commit_dic()	

	
	''' @Non-public function '''
	def __init_commit_dic(self):	
		# Function get_commit_dic: Collecting all the commit's sha,commit's time
		# ,committer's email,and the time between two commits	
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
				info = Git.log_next(sha)
			else:
				info = Git.log_one(sha)		
			try:	
				sha = p_commit.search(info).group(1)
				email = p_email.search(info).group(0)
				time = datetime.strptime(p_date.search(info).group(1),TIME_FORMAT['GIT_LOG'])
				commit_list.append(sha)
				time_list.append(time)
				email_list.append(email)			
			except:
				print("First commit")	
				break
	
		if(len(commit_list) != len(time_list)!=len(user_email)):
			logging.warning("Missing data in collecting!")

		lenth=len(commit_list)
		for i in range(0,lenth):
			if i<lenth-1:
				self.__commit_dic[lenth-i] = [commit_list[i], time_list[i], email_list[i], (time_list[i]-time_list[i+1]).total_seconds()]
			else:
				self.__commit_dic[lenth-i] = [commit_list[i], time_list[i], email_list[i],-1]

		
	def get_data_by_time(self,st_time,ed_time):
		# Get data from st_time to ed_time 
			
		temp={}
		for key in self.__commit_dic:
			if(st_time <= self.__commit_dic[key][1] <= (ed_time)):
					temp[key] = self.__commit_dic[key]	
		return temp
		
  
	def show_commit_dic(self):
		for i in self.__commit_dic:
			print(str(i)+": %s %s %s"%(self.__commit_dic[i][0],self.__commit_dic[i][1].__reStr__(),self.__commit_dic[i][2]))
			
	def get_commit_dic(self):
		return self.__commit_dic
	

class Coder(object):	
# class coder: Collecting user's informations.

	def __init__(self):
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
		self.__user_stats={}		
	

	''' Filters: Setting filters to ignore commits 
		All filters should return False for ignoring the commit.	
	'''
	def merge_filter(self,sha):
		# Filter merge_filter: Ignore those commits that has 'Merge' mark.

		title = Git.log_one(sha)
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


	def collect_stats(self,commit_dic):
		# Function collect_stats: Collecting user's information from the commit_dic.
		#		
		# The information includes:
		# additions,deletions,total codelines,commit times,email and contribute.
	
		print("collecting user's data...")
		p_ins = re.compile("(\d+) insertion")
		p_del = re.compile("(\d+) deletion")
		
		for key in commit_dic:						
			''' filters works in here '''

			ins_data = 0
			del_data = 0
			sha = commit_dic[key][0]
			time_diff = commit_dic[key][-1]
			
			user = Git.show_format(('%an',sha)).strip(' \t\n\r')
			if(sha == commit_dic[1][0]):
				data = Git.diff_short((sha,""))
			else:
				data = Git.diff_short((sha,sha+"^"))
			
			r_ins = p_ins.search(data)
			r_del = p_del.search(data)
			if(r_ins is not None):
				ins_str = r_ins.group(1)
				ins_data = int(ins_str)
			if(r_del is not None):
				del_str = r_del.group(1)
				del_data = int(del_str)

			#########----------------------------how to calculate contribute----------------------------###########	
			if(user in self.__user_stats):
				stats = self.__user_stats[user]
				stats['additions'] += ins_data
				stats['deletions'] += del_data
				stats['total'] += (ins_data + del_data)
				stats['contribute'] += (ins_data*0.7 + del_data*0.3)
				stats['commit_times'] += 1
				p_email=re.compile(commit_dic[key][2])
				if(p_email.search(stats['email']) == None):
					stats['email'] = " ".join([stats['email'],commit_dic[key][2]])
				self.__user_stats[user] = stats
			else:
				new_stat = {'additions':ins_data, 
							'deletions':del_data, 
							'total':ins_data+del_data, 
							'contribute':ins_data*0.7+del_data*0.3, 
							'commit_times':1,
							'email':commit_dic[key][2]
							}
				self.__user_stats[user] = new_stat
		

	def sort_coder(self):
		# Function sort_coder: Sorting users by contribute. 
		# Return a list of users.

		temp=[]
		for i in self.__user_stats:
			temp.append([i,
						"add:"+str(self.__user_stats[i]['additions']),
						"del:"+str(self.__user_stats[i]['deletions']),
						"tot:"+str(self.__user_stats[i]['total']),
						self.__user_stats[i]['contribute'],
						"commit_times:"+str(self.__user_stats[i]['commit_times']),
						"email:"+str(self.__user_stats[i]['email'])
						])
		temp.sort(key=lambda x:x[4],reverse=True)
		return temp

	def get_user_stats(self):
		return self.__user_stats

	def show_users(self):
		for i in self.__user_stats:
			print(i,': ',self.__user_stats[i])



if __name__=='__main__':
	#init time
	st_time = datetime(2010,12,1,0,0,0)
	ed_time = datetime(2016,7,1,0,0,0)
	 
	#init commit 
	commit = Info()
	temp = commit.get_data_by_time(st_time,ed_time)
	
	#init user info
	user = Coder()
	user.collect_stats(temp)
	user.sort_coder()
	user.show_users()	


