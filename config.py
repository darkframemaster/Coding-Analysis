#!/usr/bin/env python3
#-*- coding:utf-8 -*-

''' Global params configuration. '''

__author__='xuehao'

import os
import sys

# LOCAL part
# For local repo collections,setting this to a repo name you need.
PROJECT_NAME = 'vpn'

# PROJECTS_PATH: Don't change this. 
# All the download projects's file save in ./projects. 
PROJECTS_PATH = os.path.abspath(os.path.dirname(__file__))+'/local/projects'



# API part
# API for authentication
# Github token for authorization
ACCESS_TOKEN = ''
#CLIENT_ID = ''
#CLIENT_SECRET = ''
#FINGERPRINT = ''


# Share
# Time format for git.
TIME_FORMAT={
			'GIT_LOG':'%c',
			'GIT_API':'%Y-%m-%dT%H:%M:%SZ',
			'INPUT':'%Y %m %d %H %M %S'
			}

REPO_LEVEL={
	'popularity':{
		0:"oh,you need some companies!",
		1:"not that bad",
		2:"just soso",
		3:"populor",
		4:"very populor",
		5:"It's cool enough!",
		6:"unbelievable",
		7:"Oh,My god!"
	},
	'size':{
		0:"new born",
		1:"pocket-size",
		2:"medium-size",
		3:"large",
		4:"very large",
		5:"unbelievable",
		6:"Oh,My god!"
	}			
}
