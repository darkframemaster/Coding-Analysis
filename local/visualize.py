#!/usr/bin/env python3

__author__='xuehao'

import pylab

class Draw(object):
	
	@classmethod
	def hist(cls,data=[],buckets=10,x_label='count',y_label='Number range'):
	"""
		Use this function to visualize data as a hist.
		
		Params:
			data: The data will be visualized.
			buckets: The number of the buckets in x.
			x_label: Words will shows up in x.
			y_label: Words will shows up in y.
		Returns:
			None
	"""
		pylab.hist(data,buckets)
		pylab.xlabel(x_label)
		pylab.ylabel(y_label)
		pylab.show()

	
