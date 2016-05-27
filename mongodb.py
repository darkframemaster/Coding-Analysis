#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import pymongo

class Db():
	def __init__(self, reponame, **kw):
		self.name = str(reponame)	# Name of the database
		self.__connection = pymongo.MongoClient(**kw)
		self.__db = self.__connection[str(reponame)]
		
	def save_committer(self, insert_data={}):
		collection = self.__db['committer']
		collection.insert_one(insert_data)	

	def save_committers(self, insert_data=[]):
		collection = self.__db['committer']
		collection.insert_many(insert_data)
			 
	def save_commit(self, insert_data={}):
		collection = self.__db['commit']
		collection.insert_one(insert_data)

	def save_commits(self, insert_data={}):
		collection = self.__db['commit']
		collection.insert_many(insert_data)

	def find_committer(self, find_data={}):
		collection = self.__db['committer']
		return collection.find_one(find_data)

	def find_committers(self, find_data={}):
		collection = self.__db['committer']
		return collection.find(find_data)

	def find_commit(self, find_data={}):
		collection = self.__db['commit']
		return collection.find_one(find_data)

	def find_commits(self, find_data={}):
		collection = self.__db['commit']
		return collection.find(find_data)


