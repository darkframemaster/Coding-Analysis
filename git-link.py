#!/usr/bin/env python3.4
#-*- coding:utf-8 -*-
import re
import json
import os
import sys
import requests

ex=requests.get("https://api.github.com/repos/cocos2d/cocos2d-x/commits")
my=requests.get("https://api.github.com/repos/darkframemaster/learngit/commits")#my是一个

#我自己的repos
print("my:",my)#输出响应状态
print(my.headers)#输出my的头

try:
	print(my.headers['link'])
except:
	print("there is no link in my.headers!")

my_json=my.json()
#my_json 变成了 list my本身没有变化
#print("my.json():",my.json())#输出get的内容
#print(my_json.headers)会出现list类型中没有headers关键字的错误

#blog的repos
print("ex:",ex)
print(ex.headers)
print(ex.headers['link'])

#加上params
tk='f62bc0b33c33a2681d7de2c718239b526220f49b'
payload = {'since':'2015-01-01T00:00:00Z','until':'2015-10-01T00:00:00Z','access_token':tk}
token = {'access_token':tk}

my_param = requests.get("https://api.github.com/repos/darkframemaster/learngit/commits", params = payload)
print("my_param:",my_param)
print(my_param.headers)

