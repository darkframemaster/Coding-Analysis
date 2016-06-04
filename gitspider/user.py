#!/usr/bin/env python3

__author__='xuehao'

import logging;logging.basicConfig(level=logging.INFO)
import functools

from .urlhandler import GitApi

class UserApi(GitApi):
	
	def __init__(self):					
		self.__base_url = 'https://api.github.com/users/{username}'
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
				
	def _deal_params(func):
		@functools.wraps(func)
		def wrapper(self, **kw):
			if kw['user_name']:
				kw['user_name'] = ''.join(kw['user_name'].split())
				print(kw)
				url,option = func(self, **kw)

				logging.info("Get {user}'s {option} from {url}".format(
								user = kw['user_name'],
								option = option,
								url = url
								)
							)
				return self.get_source(url)
			else:
				return None
		return wrapper	
	
	def get_users(self, *, users_name=[]):
		tmp_users = {}
		if users_name and isinstance(users_name,list):
			for user_name in users_name:			
				tmp_users[user_name] = self.get_user(user_name)
			return tmp_users
		else:
			return None

	@_deal_params
	def get_user(self, *, user_name=''):
		url = self.__base_url.format(username = user_name)
		return url,'data'

	
	@_deal_params
	def get_followers(self, *, user_name=''):
	"""
		Return a list of the user's followers.
	"""
		url = self.__urls['followers_url'].format(username = user_name)
		return url,'followers'


	@_deal_params
	def get_following(self, *, user_name='', other_user=''):
	"""
		Return a list of the user's followings.
	"""
		url = self.__urls['followings_url'].format(username = user_name,
			other_user = other_user if not other_user else '/'+other_user)
		return url,'followings'


	@_deal_params
	def get_gists(self, user_name='', gist_id = ''):
	"""
		Return a list of the user's gists.
	"""
		url = self.__urls['gists_url'].format(username = user_name,
				gist_id = gist_id if gist_id=='' else '/'+gist_id)
		return url,'gists'
	

	@_deal_params
	def get_starred(self, user_name='', owner='', repo=''):
	"""
		Return a list of the stars that user has given.
	"""
		url = self.__urls['starred_url'].format(username = user_name,
				owner = owner if owner=='' else '/'+owner,
				repo = repo if repo=='' else '/'+repo)
		return url,'starred'


	@_deal_params
	def get_subscript(self, user_name=''):
	"""
		Return a dict subscriptions.
	"""
		url = self.__urls['subscriptions_url'].format(username = user_name)
		return url,'subscriptions'

	@_deal_params
	def get_orgs(self, user_name=''):
	"""
		Return a list of orgnizaions that user in.
	"""
		url = self.__urls['organizations_url'].format(username = user_name)
		return url,'organizations'


	@_deal_params
	def get_repos(self, *, user_name=''):
	"""
		Return a list of the user's repos.
	"""
		url = self.__urls['repos_url'].format(username = user_name)
		return url,'repos'
				

	@_deal_params
	def get_events(self, *, user_name='', privacy = 'public'):
	"""
		Return a list of the user's events.
	"""
		url = self.__urls['events'].format(username = user_name,
				privacy = privacy if privacy=='' else '/'+privacy)
		return url,'events'	



	

		
