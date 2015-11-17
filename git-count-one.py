#!/usr/bin/env python3.4
#-*- coding:utf-8 -*-
import re
import json
import os
import sys
import requests

#class Time 
#to do some operate of the commit time
class Time():
	year=""
	month=""
	date=""
	hour=""
	minute=""
	second=""
	
	def _init_(self,Y,M,D,h,m,s):
		self.year=Y
		self.month=M
		self.date=D
		self.hour=h
		self.minute=m
		self.second=s
	
	
	def set(self,Y,M,D,h,m,s):
		self.year=Y
		self.month=M
		self.date=D
		self.hour=h
		self.minute=m
		self.second=s
#compute the difference of the time in second between the two commit,and return diff as result. 
	def diff(self,other_time):
		diff=0
		if(self.year != other_time.year or self.month != other_time.month):
			diff=-1		#diff -1 means there is a long time between this two commit.
			return diff
		else:
			diff=(int(self.date)-int(other_time.date))*86400+(int(self.hour)-int(other_time.hour))*3600+(int(self.minute)-int(other_time.minute))*60+int(self.second)-int(other_time.second)
		return diff	
	
	def show(self):
		print(self.year,self.month,self.date,self.hour,self.minute,self.second)	
							



def get_time_diff(time_list):
	p_time = re.compile("(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\:(\S+)\:(\S+)\s+(\S+)")
	i=0
#for each member in time_list we turn it in to Time(class),and set the diff_time as the new member of the time_list 	
	while(i<len(time_list)):
		cp_time=p_time.search(time_list[i])
		time=Time()		
		time.set(cp_time.group(7),cp_time.group(2),cp_time.group(3),cp_time.group(4),cp_time.group(5),cp_time.group(6))
		time_list[i]=time		
		i=i+1
	i=0	
	time_list[i].show()
	while(i<len(time_list)-1):
		time_diff=time_list[i].diff(time_list[i+1])
		time_list[i]=time_diff
		i=i+1
	time_list[i]=-1	#for the first commit we set de diff_time as -1.
	return time_list	


def get_commit_dic():#get commit and commit_time
	commit_list=[]	
	time_list=[]
	commit_dic={}	#return commit and time in this dictionary

	cmd = "git log"	#"git log" for listing out commit data
	output = os.popen(cmd)
	info = output.read()
#get commit in commit_list
	p_commit = re.compile("commit (\S+)")
	for match in p_commit.finditer(info):
		commit=match.group(1)
		if commit is None:	
			print("no commit!")
		else:
			commit_list.append(commit)
#get time in time_list
	p_date = re.compile("Date\:\s+(\S+ \S+ \S+ \S+ \S+)")
	for match in p_date.finditer(info):
		all_time=match.group(1)
		if all_time is None:
			print("end commit!")
		else:
			time_list.append(all_time)	
#compare the lenth of the commit_list and time_list to confirm the lists have the same lenth.	
	if(len(commit_list)!=len(time_list)):
		print("error data!")
		exit()
#change time
	time_list=get_time_diff(time_list)		
	
	i=0
	while(i<len(commit_list)):
		commit_time=[commit_list[i],time_list[i]]
		commit_dic[i]=commit_time
		i=i+1
	return commit_dic
	


def is_merge(commit_sha):
	cmd = "git show --oneline " + commit_sha
	output = os.popen(cmd)
	title = output.read()
	p_merge = re.compile("Merge")
	if(p_merge.search(title) is not None):
		return True
	else:
		return False


def collect_stats(commit_dic):
	for key in commit_dic:
		m=commit_dic[key][0]
		t=commit_dic[key][1]
		#ignore merge commit
		if(is_merge(m)):
			continue
		
		#get user and commit data
		git_show_command = "git show -s --format=%an " + m		
		output = os.popen(git_show_command)
		user = output.read().strip(' \t\n\r')
		
		if(m==commit_dic[len(commit_dic)-1][0]):
			git_diff_command="git diff --shortstat "+m
		else:
			git_diff_command = "git diff --shortstat "+m + " " + m + "^"
		output = os.popen(git_diff_command)
		data = output.read()
		#print(git_diff_command)
		#print(data)
		
		p_ins = re.compile("(\d+) insertion")
		r_ins = p_ins.search(data)

		ins_data = 0
		del_data = 0

		if(r_ins is not None):
		  ins_str = r_ins.group(1)
		  ins_data = int(ins_str)
	

		p_del = re.compile("(\d+) deletion")
		r_del = p_del.search(data)

		if(r_del is not None):
		  del_str = r_del.group(1)
		  del_data = int(del_str)
	 
#ignore those commit which (ins+del) is more than 5000 
		if(ins_data + del_data > 5000):
		  print(user)
		  print('ins:'+str(ins_data))
		  print('del:'+str(del_data))
		  ins_data = 0
		  del_data = 0
#ignore those commit which ins(line)/time(s) is more than 1/60.(assume that a man can code one line in a minute)
		if(t=="-1" or t=='-1'):
		  print("ok!")			
		elif(ins_data/float(t)<float(1/60)):
		  print("ok!")
		else:
		  ins_data = 0
		  del_data = 0
		  print("pass")		
		

		if(user in user_stats):
		  stats = user_stats[user]
		  stats['additions'] += ins_data
		  stats['deletions'] += del_data
		  stats['total'] += (ins_data + del_data)
		  user_stats[user] = stats
		else:
		  new_stat = {'additions':ins_data, 'deletions':del_data, 'total':ins_data+del_data}
		  user_stats[user] = new_stat


def test(commit_dic):
	for key in commit_dic:
		print(commit_dic[key][0])	

#data
user_stats={}

#main program
commit_dic=get_commit_dic()
print(commit_dic)
collect_stats(commit_dic)
print(user_stats)





