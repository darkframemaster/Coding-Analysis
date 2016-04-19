# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class testPipeline(object):
	def __init__(self):
		pass

    	def process_item(self, item, spider):
		with open('test.txt','w+') as file:
			city=item['city'][0].encode('utf-8')
			file.write('city:'+str(city)+'\n\n')
	
			date=item['date']
			
			desc=item['dayDesc']
			dayDesc=desc[1::2] 
			nightDesc=desc[0::2] 
			
			dayTemp=item['dayTemp']
			gititem=zip(date,dayDesc,nightDesc,dayTemp)
		
			for i in range(len(gititem)):
				item=gititem[i]
				d=item[0]
				dd=item[1]
				nd=item[2]
				ta=item[3].split('/')
				dt=ta[0]
				try:
					nt=ta[1]
				except:
					nt=''
					print('night lost in: %s'% d)
					 				
				txt='date:{0}\t\tday:{1}({2})\t\tnight:{3}({4})\n\n'.format(d,dd.encode('utf-8'),dt.encode('utf-8'),nd.encode('utf-8'),nt.encode('utf-8'))
				  
				file.write(txt) 		
		return item
	

