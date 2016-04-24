#!/usr/bin/env python3
#-*- coding:utf-8 -*-

'''this scrpt for collecting the data from .git directory'''

__author__='xuehao'


import re
import os
import sys
from gitTime import *
from doshell import *


##########################
#	class Info
#	to save the informations of the commit in the repo.
###########################

class Info(object):
	def __init__(self):
		''' data in commit_dic={1:[commit,time,email,diff]} '''
		self.commit_dic={}	
		self.get_commit_dic()
	

	#######################################################################################################################################
	#	1. INIT FUNCTION. 
	# 	get_commit_dic(self,st_time,ed_time):for each commit get the commit_id and commit_time and return two list. 
	#######################################################################################################################################
	def get_commit_dic(self):	
		#notice the last commit is commit_list[0]
		print('collecting commit data...')
		p_commit = re.compile("commit (\w+)")
		p_date = re.compile("Date:\s+(\S+ \S+ \S+ \S+ \S+)")
		p_email = re.compile("<\S+@\S+>")
		sha=""
		commit_list=[]
		time_list=[]
		email_list=[]

		while(sha!=None):
			if sha:
				info = Git.log_next(sha)
			else:
				info = Git.log_one(sha)		
			try:	
				sha=p_commit.search(info).group(1)
				email=p_email.search(info).group(0)
				time=Time()
				time.set_comm(p_date.search(info).group(1))
				commit_list.append(sha)
				time_list.append(time)
				email_list.append(email)			
			except:
				print("First commit")	
				break
	
		if(len(commit_list)!=len(time_list)!=len(user_email)):
			print("miss data in Info FUN get_commit_dic!")
			exit()

		lenth=len(commit_list)
		for i in range(0,lenth):
			if i<lenth-1:
				self.commit_dic[lenth-i]=[commit_list[i],time_list[i],email_list[i],time_list[i].diff(time_list[i+1])]
			else:
				self.commit_dic[lenth-i]=[commit_list[i],time_list[i],email_list[i],-1]
		

	''' get data from st_time to ed_time '''
	def get_data_by_time(self,st_time,ed_time):
		temp={}
		for key in self.commit_dic:
			if(st_time.cmp_with(self.commit_dic[key][1])==False):
				if(self.commit_dic[key][1].cmp_with(ed_time)==False):
					temp[key]=self.commit_dic[key]	
				else:
					continue		
		return temp
		

	#################################################################################################################
	#		2.show_commit_dic(diff)  
	#	diff = true : show more information											
	#################################################################################################################
	def show_commit_dic(self):
		for i in self.commit_dic:
			print(str(i)+": %s %s %s"%(self.commit_dic[i][0],self.commit_dic[i][1].__reStr__(),self.commit_dic[i][2]))
			
	
	

################################
#	class coder
################################
class Coder(object):
	def __init__(self):
		#user info:
		self.user_stats={}
		self.user_num=0
	
	
	####################################################################
	#	filters: if 
	####################################################################
	def merge_filter(self,sha):
		title=Git.log_one(sha)
		p_merge = re.compile("Merge")
		if(p_merge.search(title) is not None):
			print('Merge!')
			return True
		else:
			return False


	def time_filter(self,diff,limit=3600):
		print(type(diff))
		if(diff==-1 or diff==-1):
			return False			
		elif(diff<limit):
			return False
		else:
			print('Time')
			return True


	###################################################################
	#	INIT FUNC
	#	1.collect_stats:for each commit get commit informations.
	# 	information include lines of code in each commit 
	###################################################################
	def collect_stats(self,commit_dic,**kw):
		print("collecting user's data...")
		p_ins = re.compile("(\d+) insertion")
		p_del = re.compile("(\d+) deletion")
		
		for key in commit_dic:
			ins_data = 0
			del_data = 0
			sha=commit_dic[key][0]
			time_diff=commit_dic[key][-1]
			
			user = Git.show_format(('%an',sha)).strip(' \t\n\r')
			if(sha==commit_dic[1][0]):
				data=Git.diff_short((sha,""))
			else:
				data=Git.diff_short((sha,sha+"^"))
			
			r_ins = p_ins.search(data)
			r_del = p_del.search(data)
			if(r_ins is not None):
				ins_str = r_ins.group(1)
				ins_data = int(ins_str)
			if(r_del is not None):
				del_str = r_del.group(1)
				del_data = int(del_str)
					
			''' filters works in here '''

						
			#save the data
			#########----------------------------how to count contribute----------------------------###########	
			if(user in self.user_stats):
				stats = self.user_stats[user]
				stats['additions'] += ins_data
				stats['deletions'] += del_data
				stats['total'] += (ins_data + del_data)
				stats['contribute'] += (ins_data*0.7+del_data*0.3)
				stats['commit_times'] += 1
				p_email=re.compile(commit_dic[key][2])
				if(p_email.search(stats['email']) == None):
					stats['email'] = stats['email'] +commit_dic[key][2]
				self.user_stats[user] = stats
			else:
				new_stat = {'additions':ins_data, 'deletions':del_data, 'total':ins_data+del_data, 'contribute':ins_data*0.7+del_data*0.3, 'email':commit_dic[key][2], 'commit_times':1}
				self.user_stats[user] = new_stat
		


	#################################################################################################################
	#		2.sort_coder()
	#################################################################################################################
	def sort_coder(self):
		temp=[]
		for i in self.user_stats:
			temp.append(  [i,"add:"+str(self.user_stats[i]['additions']),"del:"+str(self.user_stats[i]['deletions']),"tot:"+str(self.user_stats[i]['total']),self.user_stats[i]['contribute'],"commit_times:"+str(self.user_stats[i]['commit_times']),"email:"+str(self.user_stats[i]['email'])]  )
		temp.sort(key=lambda x:x[4],reverse=True)
		return temp
		

	#################################################################################################################
	#		3.show_users
	#################################################################################################################
	def show_users(self):
		for i in self.user_stats:
			print(i,': ',self.user_stats[i])


###################################################################
#	main program
###################################################################
if __name__=='__main__':
	#init time
	st_time=Time()
	ed_time=Time()
	st_time.set(2010,12,1,0,0,100)
	ed_time.set(2016,7,1,0,0,0)
	 
	#init commit 
	commit=Info()
	temp=commit.get_data_by_time(st_time,ed_time)
	
	#init user info
	user=Coder()
	user.collect_stats(temp)
	user.sort_coder()
	user.show_users()	
	
	##########################################
	#	result
	##########################################
	#commit.show_commit_dic(False)
	#commit.show_commit_list()
	#commit.show_time_list()





