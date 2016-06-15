#!/usr/bin/env python3

import logging

from .collectors.repo import Collector
from functools import reduce

class Analysis:
	def __init__(self, st_time=None, ed_time=None):
		'''
		Analysis is depends on the datas we collected. You can use the
		st_time and ed_time to set the time range of the datas. 

		Params:
			datetime st_time: Start get data from this time.
			datetime ed_time: End by this time.

		.The params st_time and ed_time should be instance of datetime,
		if not the params would be useless.
		'''
		self.collector = Collector(st_time, ed_time)
		self.collector.init_data()
		self.user_stats = self.collector.get_users()
		self.commit_dic = self.collector.get_commits()
		self.__user_rank = [] 


	def contributors(self):
		email_user = {}
		for user in self.user_stats:
			for email in self.user_stats[user]['email']:
				if email in email_user.keys():
					email_user[email].append(user)
				else:
					email_user[email] = [user]
		return email_user
				
				
			
		
	def repo_level(self):
		'''
		Using some datas we can get from the self.user_stats and 
		self.commit_dic to define a method of using this datas to 
		computer a repo's level.
		.You should not set the st_time and ed_time when using this	
		function.
	
		Params:

		Return:
				
		'''
		if self.collector.st_time and self.collect.ed_time:
			logging.warning('you should not set time!')
		if not self.__user_rank:
			self.sort_users()
	
		actual_lines = [self.user_stats[user]['stats']['actual'] \
						for user in self.user_stats]
		total_lines = reduce(lambda x,y: x+y, actual_lines)
		result = {
			'commit_times':len(self.commit_dic),
			'contributors':len(self.user_stats),
			'total_lines':total_lines,
			'best_10':self.__user_rank[0:10],
			'max_contributor':self.__user_rank[0:10][1]
		}
		return result
		


	def sort_users(self, by_mean_value = False, *, func=None):
		'''
		Make a User_list by the contributions.
		Params:
			self.user_stats:	
				The user's data. get this data use 'collector.repo'
			by_mean_value:	
				Sorted the users by the mean value of the contributions. 					
				.By default the value will be set in False.		
			func:	
				You can design a func to compute the contributions
		 		the way you like, just to pass it to this 'sort_users'
				func as a key param.
				.You can use the values below to design your func,use
				the key params:

				[commit_tims[,additions[,deletions[,total[,actual]]]]
				Example:
					def func(*, commit_times, addtions, deletions, total)

				.By default we compute the contribution using:
					(additions*0.6 + deletions*0.4 - total)
		Return:
			A list of the user sort by contributions or mean value of
			contributions, depends on the param 'by_mean_value'.
		'''
		for user in self.user_stats:
			additions = self.user_stats[user]['stats']['additions']
			deletions = self.user_stats[user]['stats']['deletions']
			total = self.user_stats[user]['stats']['total']
			actual = self.user_stats[user]['stats']['actual']
			commit_times = self.user_stats[user]['stats']['commit_times']
			if func is None:
				contributions = (additions*0.6 + deletions*0.4 - total)
			else:
				kw = {'commit_times': commit_times,
					'additions': additions,
					'deletions':deletions,
					'total':total,
					'actual':actual}
				contributions = func()		
			mean_contributions = contributions/commit_times

			self.__user_rank.append((user,
							contributions,
							mean_contributions,
							self.user_stats[user]['stats'],
							self.user_stats[user]['email']
							))
		if by_mean_value:
			self.__user_rank = sorted(self.__user_rank, 
								key = lambda user:user[2],
								reverse = True)
		else:
			self.__user_rank = sorted(self.__user_rank,
								key = lambda user:user[1],
								reverse = True)
		return self.__user_rank
	


		
		
	

