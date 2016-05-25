#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from datetime import datetime

from local.collectors.commit import CommitInfo
from local.collectors.user import UserInfo
from local.visualize import Draw

class Test(object):
	
	@classmethod
	def testall(cls):
		st_time=datetime(2015,1,1)
		ed_time=datetime.now()

		info=CommitInfo()
		data=info.get_data_by_time(st_time,ed_time)
		
		user=UserInfo()	
		user.collect_stats(data)
		user.sort_coder()
		user.show_users()

		data=[x.month for x in info.get_time_list(st_time,ed_time)]
		Draw.hist(data=data,buckets=12,x_label='month',y_label='commit times')		
	


if __name__=='__main__':
	Test.testall()
		
	'''
	print(config.PROJECTS_PATH)
	print(os.path.abspath(__file__))
	print(os.path.dirname(__file__))
	print(os.path.abspath(os.path.dirname(__file__)))
	
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
	print(Git.log_one('f8caa374'))
	print(Git.log_next('f8caa374'))
	print(Git.show_format(("%an",'f8caa374')))
	'''
