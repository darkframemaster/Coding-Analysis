#!/usr/bin/env python3

__author__='xuehao'

import logging;logging.basicConfig(level=logging.INFO)

from .urlhandler import GitApi
from .decorators import get_source

# Some url cannot be found in gitapi v3,They are not concerned: 
#   keys_url
#  	teams_url
#	hooks_url
#	blobs_url
#	git_tags_url	
#	git_commits_url
# 	notifications_url
# Check https://api.github.com

class RepoApi(GitApi):
	
	def __init__(self):
		# assignees_url :The users who contribute to the repo.
		# contents_url :The information about the files in the repo.
		
		self.__base_url = 'https://api.github.com/repos/{user_name}/{repo_name}'
		self.__urls = {
			'forks_url':self.__base_url + '/forks',
			'collaborators_url':self.__base_url + '/collaborators',
			'issue_events_url':self.__base_url + '/issues/events{number}',
			'events_url':self.__base_url + '/events',
			'assignees_url':self.__base_url + '/assignees{user}',
			'branches_url':self.__base_url + '/branches{branch}',
			'tags_url':self.__base_url + '/tags',
			'git_refs_url':self.__base_url + '/git/refs{sha}',
			'trees_url':self.__base_url + '/git/trees/{sha}',
			'statuses_url':self.__base_url + '/statuses/{sha}',
			'languages_url':self.__base_url + '/languages',
			'stargazers_url':self.__base_url + '/stargazers',
			'contributors_url':self.__base_url + '/contributors',
			'subscribers_url':self.__base_url + '/subscribers',
			'subscription_url':self.__base_url + '/subscription',
			'commits_url':self.__base_url + '/commits{sha}',
			'comments_url':self.__base_url + '/comments{number}',
			'issue_comment_url':self.__base_url + '/issues/commens{number}',
			'contents_url':self.__base_url + '/contents/{path}',
			'compare_url':self.__base_url + '/{base}...{head}',
			'merges_url':self.__base_url + '/merges',
			'archive_url':self.__base_url + '/{archive_format}{ref}',
			'downloads':self.__base_url + '/downloads',
			'issues_url':self.__base_url + '/issues{number}',
			'pulls_url':self.__base_url + '/pulls{number}',
			'milestones_url':self.__base_url + '/milestones{number}',
			'labels_url':self.__base_url + '/labels{number}',
			'releases_url':self.__base_url + '/releases{id}',
			'deployments_url':self.__base_url + '/deployments'
			}

	@get_source
	def get_repo(self, *, user_name='', repo_name=''):
		url = self.__base_url.format(user_name = user_name, \
									repo_name = repo_name)		
		return url,"repo's data"

	@get_source
	def get_forks(self, *, user_name='', repo_name=''):
		url = self.__urls['forks_url'].format(user_name = user_name, \
									repo_name = repo_name)
		return url,"repo's forks"

	@get_source
	def get_languages(self, *, user_name='', repo_name=''):		
		url = self.__urls['languages_url'].format(user_name = user_name, \
									repo_name = repo_name)

		return url,"repo's languages"

	@get_source
	def get_stargazers(self, *, user_name='', repo_name=''):
		url = self.__urls['stargazers_url'].format(user_name = user_name, \
									repo_name = repo_name)
		return url,"repo's stargazers"

	@get_source
	def get_contributors(self, *, user_name='', repo_name=''):
		url = self.__urls['contributors_url'].format(user_name = user_name, \
									repo_name = repo_name)
		return url,"repo's contributors"
	
	
