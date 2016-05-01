#!/usr/bin/env python3
#-*- coding:utf-8 -*-


import os

import config
from doshell import Git



if __name__=='__main__':
	print(config.PROJECTS_PATH)
	print(os.path.abspath(__file__))
	print(os.path.dirname(__file__))
	print(os.path.abspath(os.path.dirname(__file__)))
	'''
	directorys=os.popen("ls")
	directorys=directorys.read().strip(' \t\n\r')
	result=os.popen("./getRepo.sh darkframemaster WEBAPP")
	print(directorys)
	print(result)
	
	result=os.system("./getRepo.sh darkframemaster WEBAPP")	
	print(result)
	'''
	#test for doshell
	'''
	get_repo('darkframemaster','Coding-Analysis')	
	'''
	print(Git.log_one('f8caa374'))
	print(Git.log_next('f8caa374'))
	print(Git.show_format(("%an",'f8caa374')))
