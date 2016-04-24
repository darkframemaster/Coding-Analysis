#!/usr/bin/env python3
#-*- coding:utf-8 -*-

'''this script for operations do with shell'''
'''for all the operarions done with shell,please add in here'''

__author__='xuehao'

import os
import functools


''' use this func to run getRepo.sh. return True when successed'''
def get_repo(owner=None,repo_name=None):
	if owner==None or repo_name==None:
		return False
	else:
		try:
			command='./getRepo.sh '+str(owner)+" "+str(repo_name)
			if(os.system(command)==0):
				return True
			return False
		except ValueError:
			print('ValueError')
			return False

''' func(*args,**kw)=decorator(command)func(*args,**kw) '''
''' wrapper will be return as a new func '''
def os_popen(command):
	def decorator(func):
		@functools.wraps(func)
		def wrapper(args=()):
			cmd=command%args
			output=os.popen(cmd)
			info=output.read()
			return info
		return wrapper
	return decorator

class Git(object):
	#"git log" for listing out commit data	
	@os_popen("git log -1 %s")
	def log_one():
		pass

	@os_popen("git log -1 %s^")
	def log_next():
		pass

	@os_popen("git show -s --format=%s %s")
	def show_format():
		pass

	@os_popen("git diff --shortstat %s %s")
	def diff_short():
		pass
	

