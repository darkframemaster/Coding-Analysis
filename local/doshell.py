#!/usr/bin/env python3
#-*- coding:utf-8 -*-

''' This script for operations do with shell.
All the operarions done with shell should be added in here.
'''

__author__='xuehao'

import os
import functools


''' use this func to run getRepo.sh. return True when successed'''
def get_repo(owner=None,repo_name=None):
	if owner==None or repo_name==None:
		return False
	else:
		try:
			command='./downloadRepo.sh '+str(owner)+" "+str(repo_name)
			if(os.system(command)==0):
				return True
			return False
		except ValueError as e:
			raise e



''' func(*args,**kw)=decorator(command)func(*args,**kw) '''
''' wrapper will be return as a new func '''
def os_popen(func):
	@functools.wraps(func)
	def wrapper(cls,**kw):
		new_kw={}
		for key in kw:
			if key in ['sha','format_','sha1','sha2']:
				new_kw[key]=kw[key]

		cmd=func(cls, **new_kw)
		
		output=os.popen(cmd)
		info=output.read()
		return info
	return wrapper

class Git(object):
	#"git log" for listing out commit data	
	@classmethod	
	@os_popen
	def log_one(cls, *, sha=''):
		cmd='git log -1 {sha}'.format(sha=sha)
		return cmd

	@classmethod
	@os_popen
	def log_next(cls, *, sha=''):
		cmd='git log -1 {sha}^'.format(sha=sha)
		return cmd

	@classmethod
	@os_popen
	def show_format(cls, *, format_='%an', sha=''):
		cmd='git show -s --format={format_} {sha}'.format(format_=format_, sha=sha)
		return cmd
	
	@classmethod
	@os_popen
	def diff_short(cls, *, sha1='',sha2=''):
		cmd='git diff --shortstat {sha1} {sha2}'.format(sha1=sha1,sha2=sha2)
		return cmd	

