#!/usr/bin/env python3

description = '''
	In this script, we use gitapi to crawling a user's data.
	Just by giving user_name we can giving a analysis file.

	Including:

	 	1.Base infomation:

		Include:
			id,
			avatar: Pic for user in github.com
		M	starred repos,
			name,
			company,
			blog,
		M	location,
			email,
			followers,
		M	following,
			public repos count,
			The time for using github.

		2.All repos the user owned,and for each repos,the data should
	
		Include:
		M	languages, 
		M	stargazers_count, watchers_count, forks_count, 
			open_issues_count, 
			network_count,
			subscribers_count,
			repo's size.
			
			has_wiki: true / false
			has_page: true / false
		
		What for:	
		We can use the repos information to...:
			1.Help we analysis the user's coding skills.
			2.Help the user to publish it to public.
			3.Give other users a suggest for join the repo or not.
			

		3.All following
		
		4.All stared

		Using the last two part to analysis what kind of things the
		user prefer doing.		
	
'''

extend = '''
	If user is new in github and in coding.
	We can provide a suggestion file for the user by using the
 	search api for repo and org.
	Just by known the kind of skills the user want to master.
'''

from .user import UserApi
from .repo import RepoApi

class User():
	def __init__(self, *, user_name):
		self.user_name = user_name
		self.basic_info = None
		# List objects.
		self.repos = None
		self.following = None
		self.stared = None

	def get_data(self):
		user_api = UserApi()
	
		self.basic_info = user_api.get_user(user_name = self.user_name)
		self.repos = user_api.get_repos(user_name = self.user_name)
		self.following = user_api.get_following(user_name = self.user_name)
		self.stared = user_api.get_starred(user_name = self.user_name)
		
		# For each repo get languages info.
		for repo in self.repos:
			params = {'user_name':self.user_name,'repo_name':repo['name']}
			repo_api = RepoApi()
			repo['languages'] = repo_api.get_languages(**params)

	


