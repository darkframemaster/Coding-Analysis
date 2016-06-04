#!/usr/bin/env python3

import os
import logging

import mongodb
from config import PROJECTS_PATH,PROJECT_NAME


def change_repo(*, repo_name):
	"""
	change_repo direction by giving repo_name.

	Params:
		repo_name: The repo you want to use, and it must exits in 
				   PROJECT_PATH.
 	Returns:
		None
	"""
	try:
		working_path=PROJECTS_PATH+'/'+repo_name
		os.chdir(working_path)
		logging.warning('Set working path to:{path}'.format(path=working_path))
	except Exception as e:
		raise e


change_repo(repo_name = PROJECT_NAME)


