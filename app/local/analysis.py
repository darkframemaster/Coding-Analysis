#!/usr/bin/env python3

import logging
from functools import reduce
from datetime import datetime

from .collectors.repo import Collector
from .visualize import Draw

class RepoAnalysis:
	def __init__(self, repo_name='', *, st_time=None, ed_time=None):
		'''
		Analysis is depends on the datas we collected. You can use the
		st_time and ed_time to set the time range of the datas. 

		Params:
			datetime st_time: Start get data from this time.
			datetime ed_time: End by this time.

		.The params st_time and ed_time should be instance of datetime,
		if not the params would be useless.
		'''
		self.repo_name = repo_name
		self.draw = Draw(repo_name)
		self.collector = Collector(repo_name, st_time, ed_time)
		self.collector.init_data()
		self.user_stats = self.collector.get_users()
		self.commit_dic = self.collector.get_commits()
		self.__user_rank = [] 


	def contributors(self):
		email_user_dict = {}
		for user in self.user_stats:
			for email in user['email']:
				if email in email_user_dict.keys():
					email_user_dict[email].append(user['name'])
				else:
					email_user_dict[email] = [user, ]

		users = []
		for email in email_user_dict:
			info = {}
			info['users'] = email_user_dict[email]
			info['email'] = email
			users.append(info)
		return users
				
		
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
	
		actual_lines = [user['stats']['actual'] for user in self.user_stats]
		total_lines = reduce(lambda x,y: x+y, actual_lines)
		top_range = 10 if len(self.user_stats) >= 10 else len(self.user_stats) 
		result = {
			'commit_times':len(self.commit_dic),
			'contributors':len(self.user_stats),
			'total_lines':total_lines,
			'best_10':self.__user_rank[0:10],
			'max_contributor':self.__user_rank[0]
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
		if self.__user_rank:
			return self.__user_rank

		for user in self.user_stats:
			additions = user['stats']['additions']
			deletions = user['stats']['deletions']
			total     = user['stats']['total']
			actual    = user['stats']['actual']
			commit_times = user['stats']['commit_times']
			if func is None:
				contributions = (additions*1.6 + deletions*1.4 - total)
			else:
				kw = {'commit_times': commit_times,
					'additions': additions,
					'deletions':deletions,
					'total':total,
					'actual':actual}
				contributions = func()		
			mean_contributions = contributions/commit_times

			self.__user_rank.append({
						'user':user,
						'contributions':contributions,
						'mean_contributions':mean_contributions,
						})
		if by_mean_value:
			self.__user_rank = sorted(self.__user_rank, 
						key = lambda user:user['contributions'],
						reverse = True)
		else:
			self.__user_rank = sorted(self.__user_rank,
						key = lambda user:user['mean_contributions'],
						reverse = True)
		print(self.__user_rank)
		return self.__user_rank
	

	def save_figures(self):
		'''
		Use the visualize.py to draw and save the figures about the repo.
		'''	
		locations = {}
		locations['hist'] = self.__save_hist()
		locations['explode'] = self.__save_explode()
		locations['scatter'] = self.__save_scatter()
		return locations
		

	def __save_hist(self):

		time_list = self.collector.get_time_list()		
		month_commit = [x.month for x in time_list]
		day_commit = [x.day for x in time_list]

		return self.draw.hist(
			figure_name = 'commits-month', 
			data = month_commit,
			buckets = 12,
			x_label = 'month', y_label = 'commit times'
			),	self.draw.hist(
			figure_name = 'commits-day',
			data = day_commit,
			buckets = 31,
			x_label = 'day in month', y_label = 'commit times'
			)
		
		
	def __save_explode(self):
		
		users_commits   = [user['stats']['commit_times'] 
				for user in self.user_stats]
		users_additions = [user['stats']['additions']
				for user in self.user_stats]
		users_deletions = [user['stats']['deletions']
				for user in self.user_stats]
		users_total     = [user['stats']['total']
				for user in self.user_stats]
		explode = [0.1 for user in self.user_stats]
		users   = [user['name'] for user in self.user_stats]

		return 	self.draw.explode('users-commits', 
			data = users_commits, explode = explode,
			labels = users, title = 'users commits'
			),	self.draw.explode('users-addtions',
			data = users_additions, explode = explode,
			labels = users, title = 'users addtions'
			),	self.draw.explode('users-deletions',
			data = users_deletions, explode = explode,
			labels = users, title = 'users deletions'
			),	self.draw.explode('users-total',
			data = users_total, explode = explode,
			labels = users, title = 'users total')	
		
			
	def __save_scatter(self):
		return ()
	

	def get_repo_commit_times_count(self, year = datetime.now().year, month = datetime.now().month):
		time_list = self.collector.get_time_list()
		month_count = {}
		day_count   = {}

		for commit_time in time_list:
			if year and commit_time.year == year:	
				if commit_time.month in month_count.keys():
					month_count[commit_time.month] += 1
				else:
					month_count[commit_time.month] = 1

			if month and commit_time.month == month:
				if commit_time.day in day_count.keys():
					day_count[commit_time.day] += 1
				else:
					day_count[commit_time.day] = 1
				
		return dict(month_count = month_count, day_count = day_count)


	def get_users_contributions_count(self, ):
		users_commits   = [user['stats']['commit_times'] 
				for user in self.user_stats]
		users_additions = [user['stats']['additions']
				for user in self.user_stats]
		users_deletions = [user['stats']['deletions']
				for user in self.user_stats]
		users_total     = [user['stats']['total']
				for user in self.user_stats]
		users   = [user['name'] for user in self.user_stats]
		return dict(
					users = users,
					commit = users_commits,
					addition = users_additions,
					deletion = users_deletions,
					total = users_total,
				)
