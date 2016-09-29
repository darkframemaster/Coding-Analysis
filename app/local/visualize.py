#!/usr/bin/env python3

__author__='xuehao'

import threading
import os
import logging

import pylab
import matplotlib.pyplot as plt

from ..config import PIC_PATH
from ..config import PIC_REQUEST_PATH

class Draw(object):

	def __init__(self, repo_name = ''):
		self.repo_name = repo_name
		self.save_path = PIC_PATH + repo_name
		self.request_path = PIC_REQUEST_PATH + repo_name
		
		try:
			os.mkdir(self.save_path)		
		except:
			logging.warning('PIC_PATH already exist!')	
		

	def hist(self, figure_name, data=[], buckets=10, x_label='count', y_label='Number range'):
		"""
			Use this function to visualize data as a hist.
		
			Params:
				data: The data will be visualized.
				buckets: The number of the buckets in x.
				x_label: Words will shows up in x.
				y_label: Words will shows up in y.
			Returns:
				save_name: str
					The file location of the result picture
		"""
		try:
			os.mkdir(self.save_path + '/hist')
		except:
			logging.warning('update hist in '+self.save_path)	
		pylab.hist(data, buckets)
		pylab.xlabel(x_label)
		pylab.ylabel(y_label)
		save_name = self.save_path + '/hist/' + figure_name
		pylab.savefig(save_name)
		pylab.clf()

		return self.request_path + '/hist/' + figure_name + '.png'
		

	def explode(self, figure_name, data=[], explode=[], labels=(), title='a graph'):
		"""
			Use this function to visualize data as a explode

			Params:
				data: The data will be visualized.
				explode: The distance between each bucket of the data.
						 explode should be len(data) sequence or None.
				labels: The labels shows next to the bucket of the data.
				title: The title of the graph.
			Returns:
				save_name: str
					The file location of the result picture
		"""
		try:
			os.mkdir(self.save_path + '/explode')
		except:
			logging.warning('update explode in '+self.save_path)
		#Make the graph square.
		pylab.figure(1, figsize=(6,6))
		ax = pylab.axes([0.1, 0.1, 0.8, 0.8])
		pylab.title(title)
		pylab.pie(data, explode = explode, labels = labels,
			autopct = '%1.1f%%', startangle = 0)

		save_name = self.save_path + '/explode/' + figure_name
		pylab.savefig(save_name)
		pylab.clf()

		return self.request_path + '/explode/' + figure_name + '.png'


	def scatter(self, figure_name, data1=[], data2=[], color='indigo', alpha=0.3, edgecolors='white', label='label'):
		"""
			User this function to visualize data as a scatter
	
			Params:
				data1: The data will be list at x axis.
				data2: The data will be list at y axis. 
				color: The point color that shows on the graph
				alpha: The color's alpha value.
				edgecolors: Edge's color.
				label: the label shows in the graph.
			
			Return:
				save_name: str
					The file location of the result picture.
		"""
		try:
			os.mkdir(self.save_path + '/scatter')
		except:
			logging.warning('update scatter in '+self.save_path)
		if len(data1)==len(data2):
			plt.scatter(data1, data2, color = color, alpha = alpha, 
				edgecolors = edgecolors, label = label)
			plt.legend()
			save_name = self.save_path + '/scatter/' + figure_name
			plt.savefig(save_name)
			plt.clf()

			return self.request_path + '/scatter/' + figure_name + '.png'
		else:
			logging.warning('data1 should be the same lenth as data2')
