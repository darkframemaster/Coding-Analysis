#!/usr/bin/env python3

import os
import logging

import mongodb
from config import PROJECTS_PATH,PROJECT_NAME

try:
	working_path=PROJECTS_PATH+'/'+PROJECT_NAME
	os.chdir(working_path)
	logging.warning('Set working path to:{path}'.format(path=working_path))
except Exception as e:
	raise e





