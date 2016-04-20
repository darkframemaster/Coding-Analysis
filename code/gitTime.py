#!/usr/bin/env python3
#-*- coding:utf-8 -*-

__author__='xuehao'

from datetime import datetime,time,date
import re

'''
	datetime
	属性:
		datetime.year
		datetime.month
		datetime.day
		datetime.hour
		datetime.minute
		datetime.second
		datetime.microsecond
		datetime.tzinfo
	类函数:
		datetime.datetime(year=0,day=0,hour=0,minute=0,second=0,microsecond=0,tzinfo=None)	#func __init__
		datetime.now()
		datetime.today()
		datetime.combine(date,time)	#return a datetime object
	方法:
		datetime1<datetime2
		datetime.timetuple()	#获取属性元组

'''
'''
	datetime.timedelta
	type(timedelta)=type(datetime-datetime)
	属性:
		timedelta.days
		timedelta.seconds
		timedelta.microseconds

'''


'''
public functions
'''
def isTimeStr(str_time):
	print(type(str_time))
	str_time=str_time.split()
	print(str_time)
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
	
	if(isTime(year,month,date,hour,minute,second)):
		return True
	return False

	
def isTime(year,month,date,hour,minute,second):
	try:
		datetime(year,month,date,hour,minute,second)
		return True
	except:
		return False
	

###########################################	
#	classes  
#	Time:to do some operate of the commit time
##########################################
class Time(object):
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
	def __init__(self,Y=2010,M=1,D=1,h=0,m=0,s=0):
		self.set(Y,M,D,h,m,s)	

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
		year=int(Y)
		month=int(self.ex_month(M))
		date=int(D)
		hour=int(h)
		minute=int(m)
		second=int(s)
		if isTime(year,month,date,hour,minute,second):
			self.year=year
			self.month=month
			self.date=date
			self.hour=hour
			self.minute=minute
			self.second=second
			return True
		return False				
	 
	'''
		 set value by different param
	'''
	def set_str(self,str_time):
		p_time = re.compile("(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)")
		cp_time=p_time.search(str_time)
		self.set(cp_time.group(1),cp_time.group(2),cp_time.group(3),cp_time.group(4),cp_time.group(5),cp_time.group(6))

	def set_comm(self,com_time):
		p_time = re.compile("(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\:(\S+)\:(\S+)\s+(\S+)")
		cp_time=p_time.search(com_time)		
		self.set(cp_time.group(7),cp_time.group(2),cp_time.group(3),cp_time.group(4),cp_time.group(5),cp_time.group(6))

	def set_api(self,api_time):
		p_time = re.compile("(\S+)-(\S+)-(\S+)T(\S+):(\S+):(\S+)Z")
		cp_time=p_time.search(api_time)
		self.set(cp_time.group(1),cp_time.group(2),cp_time.group(3),cp_time.group(4),cp_time.group(5),cp_time.group(6))

	def is_empty(self):
		if self.year==self.month==self.date==self.hour==self.minute==self.second==0:
			return True	
		else:
			return False


	#####################
	#	2.compare time with other_time.   if self>other_time return TURE else return FALSE
	#####################	
	def cmp_with(self,other_time):
		return datetime(self.year,self.month,self.date,self.hour,self.minute,self.second)>datetime(other_time.year,other_time.month,other_time.date,other_time.hour,other_time.minute,other_time.second)
	
	def is_same(self,other_time):
		return datetime(self.year,self.month,self.date,self.hour,self.minute,self.second)==datetime(other_time.year,other_time.month,other_time.date,other_time.hour,other_time.minute,other_time.second)


	##################
	#	3.calculator the difference of the time between the two commit,and return diff as result. 
	##################	
	def diff(self,other_time):
		diff=0
		one=datetime(self.year,self.month,self.date,self.hour,self.minute,self.second)
		two=datetime(other_time.year,other_time.month,other_time.date,other_time.hour,other_time.minute,other_time.second)
		delta=one-two
		if delta.days>30:
			return -1
		if delta.total_seconds()==0:
			return 0.0001		
		return delta.total_seconds()
	
	###########################
	#	4.print time
	###########################
	def show(self):
		print(self.year,self.month,self.date,self.hour,self.minute,self.second)	
		
	def reStr(self):
		return str(self.year)+'-'+str(self.month)+'-'+str(self.date)+' '+str(self.hour)+':'+str(self.minute)+':'+str(self.second)



if __name__=='__main__':
	one=Time()
	one.set(2016,1,10,23,23,23)
	two=Time()
	two.set(2016,1,10,22,22,22)
	print(one.reStr()+' - '+two.reStr()+' = %s'%one.diff(two))

