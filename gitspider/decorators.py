#!/usr/bin/env python3

import logging;logging.basicConfig(level=logging.INFO)
import functools

def get_source(func):
		@functools.wraps(func)
		def wrapper(self, **kw):
			for key in kw:
				if key in ['user_name','owner','other_user']:
					kw[key] = ''.join(kw[key].split())
				elif key in ['repo_name']:
					kw[key] = '-'.join(kw[key].split())
				else:
					continue
				
			print(kw)
			url,option = func(self, **kw)

			logging.info("Get {option} from {url}".format(
							option = option,
							url = url
							)
						)
			return self.get_source(url)
		return wrapper
