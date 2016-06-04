#!/usr/bin/env python3

class test:
	def __init__(self):
		self.name = 'xuehao'

	def __change_name(self,name):
		self.name = name
		
	def dec(func):
		def wrapper(self):
			self.__change_name('you')
			print('This class named:')
			func(self)
		return wrapper

	@dec
	def show_name(self):
		print(self.name)


if __name__ == '__main__':
	
	a = test()
	a.show_name()
