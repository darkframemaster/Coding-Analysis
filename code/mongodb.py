#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import pymongo

connection=pymongo.MongoClient()	#建立连接
tdb=connection.test	#创建数据库
post_info=tdb.table	#创建table 

'''
在mongo命令下进行操作
db.table.find()
db.table.insert()
db.table.remove()
'''

xuehao={'name':u'xuehao','age':'21','skill':'Python'}
chenxi={'name':u'chenxi','age':'21','skill':'create','game':'dota'}

post_info.insert(xuehao)
user=post_info.find()
print(user)
#post_info.remove(xuehao)
user=post_info.find()
print(user)
print('finished')
