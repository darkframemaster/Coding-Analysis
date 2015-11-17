#!/usr/bin/env python3.4
#-*- coding:utf-8 -*-
import re
import json
import os
import sys
import requests

def if_connect(r):
	response=re.compile("(\d+)")
	Type=response.search(r.headers['status'])
	Type=Type.group(1)
	if Type==str(200):
		print('200 OK')
	else:
		print(Type)
		print('CHECK YOUR CONNECTION!')
		exit()

def get_link(h): 
	pattern = re.compile("<(\S+)>; rel=\"next\"")
	try:
		result = pattern.search(h['link'])
	except:
		print('no "link" in r.header')
		exit()
	return result	

def is_merge(commit_sha):
	cmd = "git show --oneline " + commit_sha
	output = os.popen(cmd)
	title = output.read()
	p_merge = re.compile("Merge")
	if(p_merge.search(title) is not None):
		return True
	else:
		return False


def collect_stats(commit_list):
	for m in commit_list:
		if(is_merge(m['sha'])):
			continue
		
		#print('commit:'+m['sha'])
	
		git_show_command = "git show -s --format=%an " + m['sha']#return username of the commit m['sha']
		output = os.popen(git_show_command)
		user = output.read().strip(' \t\n\r')
		
		git_diff_command = "git diff --shortstat "+m['sha'] + " " + m['sha'] + "^"
		#return in command line like(1 files changed, 1 insertions(+), 1 deletion(-))
		#git diff --shortstat commit1 commit2
		#compare commit1 to commit2 and show the changes
		output = os.popen(git_diff_command)
		data = output.read()
		
		p_ins = re.compile("(\d+) insertion")
		r_ins = p_ins.search(data)
		#r_ins:<_sre.SRE_Match object; span=(18, 31), match='157 insertion'>
		#match='157 insertion'

		ins_data = 0
		del_data = 0

		if(r_ins is not None):
		  ins_str = r_ins.group(1)#group(1)='157' group(0)=mathc(all)=match
		  ins_data = int(ins_str)
		  #print ins_data

		p_del = re.compile("(\d+) deletion")
		r_del = p_del.search(data)

		if(r_del is not None):
		  del_str = r_del.group(1)
		  del_data = int(del_str)
		  #print del_data 

		if(ins_data + del_data > 5000):
		  print(user)
		  print('ins:'+str(ins_data))
		  print('del:'+str(del_data))
		  ins_data = 0
		  del_data = 0
		if(user in user_stats):
		  stats = user_stats[user]
		  stats['additions'] += ins_data
		  stats['deletions'] += del_data
		  stats['total'] += (ins_data + del_data)
		  user_stats[user] = stats
		else:
		  new_stat = {'additions':ins_data, 'deletions':del_data, 'total':ins_data+del_data}
		  user_stats[user] = new_stat


#data
tk='f62bc0b33c33a2681d7de2c718239b526220f49b'
payload = {'since':'2015-01-01T00:00:00Z','until':'2015-10-01T00:00:00Z','access_token':tk}
token = {'access_token':tk}
user_stats={"darkframemaster":{"additions":0,"deletions":0,"total":0}}

#main program
r = requests.get("https://api.github.com/repos/darkframemaster/learngit/commits",params=payload)
if_connect(r)	#check connect

#count the data in the repo
collect_stats(r.json())
print(user_stats)

#count the data in other repo
h = r.headers
print(h)
print(h['X-RateLimit-Remaining'])
result=get_link(h)

while(result is not None):
	next_url=result.group(1)
	
	r=request.get(next_url,params=token)
	collect_stats(r.json())
	
	h=r.headers
	print(h['link'])
	result=get_link(h)
	
	print(r.headers['X-RateLimit-Remaining'])
	print(user_stats)
