#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import timeit
from datetime import datetime

#from local.collectors.commit import CommitInfo
#from local.collectors.user import UserInfo
from local.analysis import Analysis
from local.visualize import Draw
#from gitspider.repohandler import RepoApi

class Test(object):
	@classmethod
	def test_collector(cls):
		'''Using local.collectors to collect data from local repo in ./local/project.
		'''
		#st_time=datetime(2015,1,1)
		#ed_time=datetime.now()	
		info=CommitInfo()
		info.init_commits()
		data = info.get_commits()
		#print(len(info.get_commits()))
		#data=info.get_commits_by_time(st_time,ed_time)
		
		user=UserInfo()	
		user.init_users(data)
		'''
		data=[x.month for x in info.get_time_list(st_time,ed_time)]
		Draw.hist(data=data,buckets=12,x_label='month',y_label='commit times/month')

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

		Draw.explode(data, explode, labels, title='commit times/month')
		'''
	
	@classmethod
	def test_Analysis(cls):
		ana = Analysis()
		print(ana.sort_users())
		print(ana.repo_level())
		
	@classmethod
	def test_gitapi(cls):
		'''Using gitapi.gitspider to collect data from gitapi.
		'''
		test = RepoApi(user='darkframemaster', repo='Coding-Analysis')
		test.show()

if __name__=='__main__':
	#print(timeit.timeit('Test.test_collector()','from run import Test',number=1))
	print(timeit.timeit('Test.test_Analysis()','from run import Test',number=1))
	#Test.test_collector()
	#Test.test_gitapi()

