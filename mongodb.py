#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import pymongo

class Db():
	def __init__(self, reponame, **kw):
		self.__connection = pymongo.MongoClient(**kw)
		self.__db = self.__connection[str(reponame)]
		
	def drop_commit(self):
		self.__db.drop_collection('commit')
	
	def drop_user(self):
		self.__db.drop_collection('user')
		
	def save_user(self, insert_data={}):
		collection = self.__db['user']
		collection.insert_one(insert_data)	

	def save_users(self, insert_data=[]):
		collection = self.__db['user']
		collection.insert_many(insert_data)
			 
	def save_commit(self, insert_data={}):
		collection = self.__db['commit']
		collection.insert_one(insert_data)

	def save_commits(self, insert_data={}):
		collection = self.__db['commit']
		collection.insert_many(insert_data)

	def find_user(self, find_data={}):
		collection = self.__db['user']
		return collection.find_one(find_data)

	def find_users(self, find_data={}):
		collection = self.__db['user']
		return collection.find(find_data)

	def find_commit(self, find_data={}):
		collection = self.__db['commit']
		return collection.find_one(find_data)

	def find_commits(self, find_data={}):
		collection = self.__db['commit']
		return collection.find(find_data)


