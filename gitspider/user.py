#!/usr/bin/env python3

__author__='xuehao'

import logging;logging.basicConfig(level=logging.INFO)
import functools

from .urlhandler import GitApi
from .decorators import get_source

class UserApi(GitApi):
	
	def __init__(self):					
		self.__base_url = 'https://api.github.com/users/{user_name}'
		self.__urls = {
				'followers_url':self.__base_url+'/followers',
				'following_url':self.__base_url + '/following{other_user}',
				'gists_url':self.__base_url + '/gists{gist_id}',
				'starred_url':self.__base_url + '/starred{owner}{repo}',
				'subscriptions_url':self.__base_url + '/subscriptions',
				'organizations_url':self.__base_url + '/orgs',
				'repos_url':self.__base_url + '/repos',
				'events_url':self.__base_url + '/events{privacy}',
				'received_events_url':self.__base_url + '/received_events'
				}
					


	def get_users(self, *, users_name=[]):
		tmp_users = {}
		if users_name and isinstance(users_name,list):
			for user_name in users_name:			
				tmp_users[user_name] = self.get_user(user_name)
			return tmp_users
		else:
			return None

	@get_source
	def get_user(self, *, user_name=''):
		url = self.__base_url.format(user_name = user_name)
		return url,"user's data"

	
	@get_source
	def get_followers(self, *, user_name=''):
		"""
			Return a list of the user's followers.
		"""
		url = self.__urls['followers_url'].format(user_name = user_name)
		return url,"user's followers"


	@get_source
	def get_following(self, *, user_name='', other_user=''):
		"""
			Return a list of the user's followings.
		"""
		url = self.__urls['followings_url'].format(user_name = user_name,
			other_user = other_user if not other_user else '/'+other_user)
		return url,"user's followings"


	@get_source
	def get_gists(self, user_name='', gist_id = ''):
		"""
			Return a list of the user's gists.
		"""
		url = self.__urls['gists_url'].format(user_name = user_name,
				gist_id = gist_id if gist_id=='' else '/'+gist_id)
		return url,"user's gists"
	

	@get_source
	def get_starred(self, user_name='', owner='', repo=''):
		"""
			Return a list of the stars that user has given.
		"""
		
		url = self.__urls['starred_url'].format(user_name = user_name,
				owner = owner if owner=='' else '/'+owner,
				repo = repo if repo=='' else '/'+repo)
		return url,"user's starred"


	@get_source
	def get_subscript(self, user_name=''):
		"""
			Return a dict subscriptions.
		"""
		url = self.__urls['subscriptions_url'].format(user_name = user_name)
		return url,"user's subscriptions"

	@get_source
	def get_orgs(self, user_name=''):
		"""
			Return a list of orgnizaions that user in.
		"""
		url = self.__urls['organizations_url'].format(user_name = user_name)
		return url,"user's organizations"


	@get_source
	def get_repos(self, *, user_name=''):
		"""
			Return a list of the user's repos.
		"""
		url = self.__urls['repos_url'].format(user_name = user_name)
		return url,"user's repos"
				

	@get_source
	def get_events(self, *, user_name='', privacy = 'public'):
		"""
			Return a list of the user's events.
		"""
		url = self.__urls['events'].format(user_name = user_name,
				privacy = privacy if privacy=='' else '/'+privacy)
		return url,"user's events"	



	

		
