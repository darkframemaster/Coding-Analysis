#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import timeit
from datetime import datetime

from local.collectors.commit import CommitInfo
from local.collectors.user import UserInfo
from local.visualize import Draw
from gitapi.gitspider import Api

class Test(object):
	@classmethod
	def test_collector(cls):
		'''Using local.collectors to collect data from local repo in ./local/project.
		'''
		st_time=datetime(2015,1,1)
		ed_time=datetime.now()	
		info=CommitInfo()
		data=info.get_data_by_time(st_time,ed_time)
		
		user=UserInfo()	
		user.collect_user_stats(data)
		user.show_users()

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
		print(data,len(data))
		print(explode,len(explode))
		print(labels,len(labels))

		Draw.explode(data, explode, labels, title='commit times/month')

	@classmethod
	def test_gitapi(cls):
		'''Using gitapi.gitspider to collecto data from gitapi.
		'''
		test = Api(user='darkframemaster', repo='Coding-Analysis')
		test.show()

if __name__=='__main__':
	#timeit.timeit('Test.test_collector()','from run import Test',number=1)
	#timeit.timeit('Test.test_gitapi()','from run import Test',number=1)
	Test.test_collector()
	Test.test_gitapi()

