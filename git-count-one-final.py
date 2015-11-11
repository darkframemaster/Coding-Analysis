#!/usr/bin/env python3.4
#-*- coding:utf-8 -*-
import re
import json
import os
import sys
import requests


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
		#ignore merge commit
		if(is_merge(m['sha'])):
			continue
		
		#get user and commit data
		git_show_command = "git show -s --format=%an " + m['sha']		
		output = os.popen(git_show_command)
		user = output.read().strip(' \t\n\r')
		
		git_diff_command = "git diff --shortstat "+m['sha'] + " " + m['sha'] + "^"
		output = os.popen(git_diff_command)
		data = output.read()
		print(git_diff_command)
		print(data)
		
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
user_stats={"dummy":{"additions":0,"deletions":0,"total":0}}
tk='f62bc0b33c33a2681d7de2c718239b526220f49b'
payload = {'access_token':tk}

#main program
my_repos=requests.get("https://api.github.com/users/darkframemaster/repos",params=tk)
print(my_repos)
count=0
repos_link=[]
while count<100:
	try:
		count=count+1
		repos_link.append(my_repos.json()[count]['commits_url'][:-6])#用切片取得{/sha}前的串
	except:
		break

print(repos_link)

for i in repos_link:
	repo_link=requests.get(i,params=tk)
	collect_stats(repo_link.json())

print(user_stats)


