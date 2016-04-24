#!/usr/bin/env python3


######## 格式说明 ###########
#类名称为首字母大写
#类方法名称为首字母小写
#类变量名称为首字母小写
#变量及方法名称单词长度大于5个的按习惯取单词首部


import time
import re
import json
import os
import sys
import requests
import gitTime



###public function:
def isTimeStr(str_time):
	str_time=str_time.split()
	if len(str_time)<6:
		return False
	try:
		year=int(str_time[0])
		month=int(str_time[1])
		date=int(str_time[2])
		hour=int(str_time[3])
		minute=int(str_time[4])
		second=int(str_time[5])
	except:
		return False
	print(year,month,date,hour,minute,second)
	if year>2100 or year<=0 or month<=0 or month>12 or date<1 or date>366 or hour<0 or hour>23 or minute>59 or minute<0 or second>59 or second<0:
			return False
	elif year%4==0 and year%100!=0:
		if month==2:
			if date>29:
				return False
		elif month==4 or month==6 or month==9 or month==11:
			if date>30:
				return False
		return True
	else:
		if month==2:
			if date>28:	
				return False
		elif month==4 or month==6 or month==9 or month==11:
			if date>30:
				return False
		return True
	return True
	
	

###########################################	
#	classes  
#	Time:to do some operate of the commit time
##########################################
class Time():
	year=0
	month=0
	date=0
	hour=0
	minute=0
	second=0
	
	####
	#	initial functions 
	#	
	####
	def ex_month(self,M):
		if(M=='Jan'): 	return 1
		if(M=='Feb'):	return 2
		if(M=='Mar'):	return 3
		if(M=='Apr'):	return 4
		if(M=='May'):	return 5
		if(M=='Jun'): 	return 6
		if(M=='Jul'):	return 7
		if(M=='Aug'):	return 8
		if(M=='Sep'):	return 9
		if(M=='Sept'):  return 9
		if(M=='Oct'):	return 10
		if(M=='Nov'):	return 11
		if(M=='Dec'):	return 12 
		else: 
			assert 1<=int(M)<=12,'month error! in Time FUN ex_month'
			return int(M)
	def set(self,Y=2010,M=1,D=1,h=0,m=0,s=0):
		self.year=int(Y)
		self.month=self.ex_month(M)
		self.date=int(D)
		self.hour=int(h)
		self.minute=int(m)
		self.second=int(s)	
			
	def isTime(self):
		if self.year>2100 or self.year<=0 or self.month<=0 or self.month>12 or self.date<0 or self.date>366 or self.hour<0 or self.hour>23 or self.minute>59 or self.minute<0 or self.second>59 or self.second<0:
			return False
		elif self.year%4==0 and self.year%100!=0:
			if self.month==2:
				if self.date>29:
					return False
			if self.month==4 or self.month==6 or self.month==9 or self.month==11:
				if self.date>30:
					return False
			return True
		else:
			if self.month==2:
				if self.date>28:
					return False
			elif self.month==4 or self.month==6 or self.month==9 or self.month==11:
				if self.date>30:
					return False
			return True
	 
	def set_str(self,str_time):
		p_time = re.compile("(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)")
		cp_time=p_time.search(str_time)
		self.set(cp_time.group(1),cp_time.group(2),cp_time.group(3),cp_time.group(4),cp_time.group(5),cp_time.group(6))
	def set_comm(self,com_time):
		p_time = re.compile("(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\:(\S+)\:(\S+)\s+(\S+)")
		cp_time=p_time.search(com_time)		
		self.set(cp_time.group(7),cp_time.group(2),cp_time.group(3),cp_time.group(4),cp_time.group(5),cp_time.group(6))
	def is_empty(self):
		if self.year==self.month==self.date==self.hour==self.minute==self.second==0:
			return True	
		else:
			return False


	#####################
	#	2.compare time with other_time.   if self>other_time return TURE else return FALSE
	#####################	
	def cmp_with(self,other_time):
		if(other_time.year>self.year):
			return False
		elif(other_time.year<self.year):
			return True
		else:#other_time.year==self.year
			if(other_time.month>self.month):
				return False
			elif(other_time.month<self.month):
				return True
			else:
				if(other_time.date>self.date):
					return False
				elif(other_time.date<self.date):
					return True
				else:
					if(other_time.hour>self.hour):
						return False
					elif(other_time.hour<self.hour):
						return True
					else:
						if(other_time.minute>self.minute):
							return False
						elif(other_time.minute<self.minute):
							return True
						else:
							if(other_time.second>self.second):
								return False
							elif(other_time.second<self.second):
								return True
							else:
								return False
	def is_same(self,other_time):
		if(self.year==other_time.year and self.month==other_time.month and self.date==other_time.date and self.hour==other_time.hour and self.minute==other_time.minute and self.second==other_time.second):
			return True
		else:
			return False


	##################
	#	3.compute the difference of the time between the two commit,and return diff as result. 
	##################	
	def diff(self,other_time):
		diff=0
		if(self.cmp_with(other_time)==False):
			diff=-1
		if(self.year != other_time.year or self.month != other_time.month):	
				if(self.year-other_time.year==1 and self.month==1 and other_time.month==12):
					diff=(31-self.date+other_time.date)*86400+(other_time.hour-self.hour)*3600+(other_time.minute-self.minute)*60+(other_time.second-self.second)	
				else:
					diff=-1		#diff -1 means there is a long time between this two commit.
				if(diff == 0): diff=0.000001
				return diff
		else:
			diff=(int(self.date)-int(other_time.date))*86400+(int(self.hour)-int(other_time.hour))*3600+(int(self.minute)-int(other_time.minute))*60+int(self.second)-int(other_time.second)
		#assert diff!=0,"diff cannot be zore! error in class Time,FUN diff(other_time)"
		if(diff == 0): diff=0.000001		
		return diff	
	
	###########################
	#	4.print time
	###########################
	def show(self):
		print(self.year,self.month,self.date,self.hour,self.minute,self.second)	
		
	def reStr(self):
		return str(str(self.year)+' '+str(self.month)+' '+str(self.date)+' '+str(self.hour)+' '+str(self.minute)+' '+str(self.second))




