#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import timeit
from datetime import datetime

from local.collectors.commit import CommitInfo
from local.collectors.user import UserInfo
from local.collectors.repo import Collector
from local.visualize import Draw

class Test(object):
	@classmethod
	def test_collector(cls):
		st_time=datetime(2015,1,1)
		ed_time=datetime.now()	
		info=CommitInfo()
		data=info.get_data_by_time(st_time,ed_time)
		
		user=UserInfo()	
		user.collect_user_stats(data)
		user.show_users()

		data=[x.month for x in info.get_time_list(st_time,ed_time)]
		Draw.hist(data=data,buckets=12,x_label='month',y_label='commit times/month')		
	
	@classmethod
	def test_collector_repo(cls):
		st_time=datetime(2015,1,1)
		ed_time=datetime.now()	
		info=Collector()
		#data=info.get_dic_by_time(st_time,ed_time)
		#user=info.collect_user_stats(data)
		'''	
		info=CommitInfo()
		data=info.get_data_by_time(st_time,ed_time)
		
		user=UserInfo()	
		user.collect_stats(data)
		user.sort_coder()
		user.show_users()		
		'''
		monthes=[x.month for x in info.get_time_list(st_time,ed_time)]	
		data=[]
		for i in range(1,13):
			count=0
			for j in monthes:
				if j == i:
					count+=1
			data.append(count)				
		explode=[0.1 for x in data]	
		labels=[str(x) for x in range(1,13)]
		print(data,len(data))
		print(explode,len(explode))
		print(labels,len(labels))

		Draw.explode(data, explode, labels, title='commit times/month')


if __name__=='__main__':
	print(timeit.timeit('Test.test_collector()','from run import Test',number=1))
	#print(timeit.timeit('Test.test_collector_repo()','from run import Test',number=1))
		
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
