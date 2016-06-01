#!/usr/bin/env python3

__author__='xuehao'

import threading

import pylab
import matplotlib.pyplot as plt

class Draw(object):
	
	@classmethod
	def hist(cls, data=[], buckets=10, x_label='count', y_label='Number range'):
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
		
		pylab.hist(data, buckets)
		pylab.xlabel(x_label)
		pylab.ylabel(y_label)
		pic = target = pylab.show()

	@classmethod
	def explode(cls, data=[], explode=[], labels=(), title='a graph'):
		"""
			Use this function to visualize data as a explode

			Params:
				data: The data will be visualized.
				explode: The distance between each bucket of the data.
						 explode should be len(data) sequence or None.
				labels: The labels shows next to the bucket of the data.
				title: The title of the graph.
			Returns:
				None  
		"""
		#Make the graph a square.
		pylab.figure(1, figsize=(6,6))
		ax = pylab.axes([0.1, 0.1, 0.8, 0.8])
		
		pylab.title(title)
		pylab.pie(data, explode = explode, labels = labels,
			autopct = '%1.1f%%', startangle = 0)
		pic = pylab.show()

	@classmethod
	def scatter(cls, data1=[], data2=[], color='indigo', alpha=0.3, edgecolors='white', label='label'):
		"""
			User this function to visualize data as a scatter
	
			Params:
				data1: The data will be list at x axis.
				data2: The data will be list at y axis. 
				color: The point color that shows on the graph
				alpha: The color's alpha value.
				edgecolors: Edge's color.
				label: the label shows in the graph.
		"""
		print(type(data1), isinstance(data1,list))
		if len(data1)==len(data2):
			plt.scatter(data1, data2, color = color, alpha = alpha, 
				edgecolors = edgecolors, label = label)
			plt.legend()
			pic = plt.show()
		else:
			raise ValueError("x and y must be the same size")
				
	
