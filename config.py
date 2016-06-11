#!/usr/bin/env python3
#-*- coding:utf-8 -*-

''' Global params configuration. '''

__author__='xuehao'

import os
import sys

# LOCAL part
# For local repo collections,setting this to a repo name you need.
PROJECT_NAME = 'requests'

# PROJECTS_PATH: All the download projects's file save in ./projects. 
PROJECTS_PATH = os.path.abspath(os.path.dirname(__file__))+'/local/projects'



# API part
# API for authentication
# Github token for authorization
ACCESS_TOKEN = ''
#CLIENT_ID = ''
#CLIENT_SECRET = ''
#FINGERPRINT = ''


# Share
# Email dic,map each email to a contry.
EMAIL_DIC={}
# Time format for git.
TIME_FORMAT={
			'GIT_LOG':'%c',
			'GIT_API':'%Y-%m-%dT%H:%M:%SZ',
			'INPUT':'%Y %m %d %H %M %S'
			}


