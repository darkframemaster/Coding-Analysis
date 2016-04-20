#!/usr/bin/env python3.4
#-*- coding:utf-8 -*-

__author__='xuehao'

import re
import tkinter
import tkinter.simpledialog
import tkinter.messagebox
import gitTime
import gitCount
import time


'''
class myEntry:
	def __init__(self,root,Type,showInfo,width=None,sign=None):
		self.root=root
		if Type=='entry' or Type=='Entry':
			if sign!=None:
				entry=tkinter.Entry(self.root,show=sign)
				entry=insert(1.0,showInfo)
				entry.pack()				
			else:
				entry=tkinter.Entry(self.root)
				entry.insert(1.0,showInfo)
				entry.pack()
		elif Type=='text' or Type=='Text':
			edit=tkinter.Text(self.root,background='white')
			edit.insert(1.0,str(showInfo))
			edit.pack()
'''

class myListBox(object):
	def __init__(self,root,info=[]):
		#一个带有两个滑动框的listbox
		self.root=root
		self.scrollbarY=tkinter.Scrollbar(root)
		self.scrollbarY.pack(side='left',fill='y')
				
		self.listbox=tkinter.Listbox(self.root,fg='white',bg='black',selectbackground='gray',width=150,height=30,yscrollcommand=self.scrollbarY.set)
		item=len(info)-1
		while item>=0:
			print(item)
			self.listbox.insert(0,info[item])
			item-=1
		self.listbox.pack(side='left',fill='both')
		self.scrollbarY.config(command=self.listbox.yview)		
		
		self.label=tkinter.Label(self.root,text='All lines:  '+str(self.listbox.size()))
		self.label.pack()
		
		
		#button=tkinter.Button(self.root,text='coder_list',bg='gray',)
		#按钮实现list的显示

class initDia(object):
	def __init__(self,root):
		self.root=root
		self.top=tkinter.Toplevel(root)
		self.label=tkinter.Label(self.top,text='请输入你要查看的时间区间',fg='white',bg='black',width=40,height=5,justify=tkinter.CENTER)
		self.label.pack()
		
		self.label1=tkinter.Label(self.top,text='input start time(ex:year month day)',width=40)
		self.label1.pack()

		self.entry=tkinter.Entry(self.top,width=30)
		self.entry.insert(1,'2010 12 1 0 0 0')
		self.entry.pack()
		self.entry.focus()

		self.label2=tkinter.Label(self.top,text='input end time',width=40)
		self.label2.pack()

		self.entry1=tkinter.Entry(self.top,width=30)
		self.entry1.insert(1,'2016 1 1 0 0 0')
		self.entry1.pack()	
		
		self.button=tkinter.Button(self.top,text='Ok',bg='gray',width=37,command=self.Ok)
		self.button.pack()
		self.input=None
		
	def Ok(self):
		self.input=[self.entry.get(),self.entry1.get()]
		if len(self.entry.get())==0 and len(self.entry1.get())==0:
			 self.input=None
		self.top.destroy()
		

	def Get(self):	
		if self.input:		
			return self.input
		else:
			return

class dataDia(object):
	def __init__(self,root):
		self.root=root
		self.top=tkinter.Toplevel(self.root)
	
		self.r=tkinter.StringVar()	
		self.r.set('0')
		
		radio=tkinter.Radiobutton(self.top,variable=self.r,value='0',text='commit list')
		radio.pack()
		radio1=tkinter.Radiobutton(self.top,variable=self.r,value='1',text='time list')
		radio1.pack()
		radio2=tkinter.Radiobutton(self.top,variable=self.r,value='2',text='commit dic')
		radio2.pack()
		
		self.button=tkinter.Button(self.top,text='Ok',bg='gray',width=37,command=self.Ok)
		self.button.pack()
	
	def Ok(self):
		self.top.destroy()
	
	def Get(self):
		return	self.r.get() 

class mainDialog(object):	#主窗体 
	def __init__(self,root):#一个label 两个按钮
		self.root=root

		self.label1=tkinter.Label(self.root,bg='black',fg='white',text='welcome using git-count',width=30,height=5)
		self.label1.pack()
		

		self.buttonInit=tkinter.Button(self.root,text='init data',bg='gray',width=27,command=self.initDia)	#绑定了Create这个事件
		self.buttonInit.pack()
		
		self.buttonDataChoose=tkinter.Button(self.root,text='other Data',bg='gray',width=27,command=self.dataDia)
		self.buttonDataChoose.pack()


		self.buttonQuit=tkinter.Button(self.root,text='Quit',bg='gray',width=27,command=self.Quit)
		self.buttonQuit.pack()
		
		#初始化gitCount的变量
		self.st_time=None
		self.ed_time=None
		self.commit=None
		self.user=None
	
	def Main(self,stTime,edTime):	#主程序入口
		if len(stTime)==0:
			stTime='2000 1 1 0 0 0'
		if len(edTime)==0:
			edTime=time.strftime('%Y %m %d %H %M %S',time.localtime())
		
		#初始化gitCount的变量
		self.st_time=gitTime.Time()
		self.ed_time=gitTime.Time()
		self.st_time.set_str(stTime)
		self.ed_time.set_str(edTime)
		if self.st_time.cmp_with(self.ed_time)==True:
			tkinter.messagebox.showerror('git count','start time bigger than end time!')
			return 
		
		self.comInfo=gitCount.Info()
		self.user=gitCount.Coder()
		self.comInfo.get_commit_dic(self.st_time,self.ed_time)
		
		self.user.collect_stats(self.comInfo.commit_dic)
		self.user.sort_coder()
		
		listroot=tkinter.Tk()
		listbox=myListBox(listroot,self.user.user_sort)

	def initDia(self):	#init 按钮绑定的事件
		d=initDia(self.root)
		self.buttonInit.wait_window(d.top)
		#self.buttonDataChoose.wait_window(d.top)
		#self.buttonQuit.wait_window(d.top)

		if d.Get()!=None:
			if len(d.Get()[0])!=0:
				if gitTime.isTimeStr(d.Get()[0])==False:
					tkinter.messagebox.showerror('git count','input time error in start time!')
					return 
			if len(d.Get()[1])!=0:
				if gitTime.isTimeStr(d.Get()[1])==False:
					tkinter.messagebox.showerror('git count','input time error in end time!')
					return
			self.Main(d.Get()[0],d.Get()[1])
		else:
			self.Main('2000 1 1 0 0 0',time.strftime('%Y %m %d %H %M %S',time.localtime()))

	def dataDia(self):
		d=dataDia(self.root)
		self.buttonInit.wait_window(d.top)
		#self.buttonDataChoose.wait_window(d.top)
		#self.buttonQuit.wait_window(d.top)

		if self.st_time==None or self.ed_time==None or self.user==None or self.comInfo==None:
			tkinter.messagebox.showerror('git count','please init data first!')			
			return
				
		listroot=tkinter.Tk()	
		if d.Get()=='0':
			listbox=myListBox(listroot,self.comInfo.commit_list)
		elif d.Get()=='1':
			tmp=[]
			for i in self.comInfo.time_list:
				tmp.append(i.reStr())
			listbox=myListBox(listroot,tmp)
		else:
			listbox=myListBox(listroot,self.comInfo.commit_dic)
		

	def Quit(self):
		self.root.quit()
					
#main program	
if __name__=="__main__":
	root=tkinter.Tk()	#生成root主窗口
	button=mainDialog(root)
	root.mainloop()		#进入消息循环


