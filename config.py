#!/usr/bin/env python3
#-*- coding:utf-8 -*-

''' Global params configuration. '''

__author__='xuehao'

import os
import sys

# LOCAL part
# For local repo collections,setting this to the repo name you need.
PROJECT_NAME = 'vpn'

# PROJECTS_PATH: All the download projects's file save in ./projects. 
PROJECTS_PATH = os.path.abspath(os.path.dirname(__file__))+'/local/projects'


# API part
# Github token for authorization
ACCESS_TOKEN = '17abdeb721a6016b4c6ab3a4884e437f70c70713'
# Settings using in Api authentications.
CLIENT_ID = '9ccbc60de523f3be5091'
CLIENT_SECRET = ''
FINGERPRINT = ''

# Time format for git.
TIME_FORMAT={
			'GIT_LOG':'%c',
			'GIT_API':'%Y-%m-%dT%H:%M:%SZ',
			'INPUT':'%Y %m %d %H %M %S'
			}


