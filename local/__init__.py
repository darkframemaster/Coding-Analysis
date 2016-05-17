#!/usr/bin/env python3

import os
import logging

from .config import PROJECTS_PATH


project_name='Coding-Analysis'

try:
	working_path=PROJECTS_PATH+'/'+project_name
	os.chdir(working_path)
	logging.warning('Set working path to:{path}'.format(path=working_path))
except Exception as e:
	raise e





