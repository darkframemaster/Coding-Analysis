#!/usr/bin/env python3
#-*- coding:utf-8 -*-

''' Global params configuration. '''

import os
import sys

# PROJECTS_PATH: Don't change this. 
# All the download projects's file save in ./projects. 
PROJECTS_PATH = os.path.abspath(os.path.dirname(__file__))+'/local/projects/'
PIC_PATH = os.path.abspath(os.path.dirname(__file__))+'/static/images/projects/'
PIC_REQUEST_PATH = '/static/images/projects/'

# Time format for git.
TIME_FORMAT={
			'GIT_LOG':'%c',
			'GIT_API':'%Y-%m-%dT%H:%M:%SZ',
			'INPUT':'%Y %m %d %H %M %S'
			}

