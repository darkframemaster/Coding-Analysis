#!/usr/bin/env python3
#-*- coding:utf-8 -*-

''' Global params configuration. '''

__author__='xuehao'

import os
import sys

# For local repo collections,setting this to the repo name you need.
PROJECT_NAME = 'swift'

# PROJECTS_PATH: All the download projects's file save in ./projects. 
PROJECTS_PATH = os.path.abspath(os.path.dirname(__file__))+'/local/projects'

# Github token for authorization
ACCESS_TOKEN = '3c70cf072a9ebc2fa338618a9fb39a2b517a83b6'

# Time format for git.
TIME_FORMAT={
			'GIT_LOG':'%c',
			'GIT_API':'%Y-%m-%dT%H:%M:%SZ',
			'INPUT':'%Y %m %d %H %M %S'
			}


