#!/usr/bin/env python3

description = '''
	In this script, we use gitapi to crawling a user's data.
	Including:

	 	1.Base infomation:

		Include:
			id,
			avatar: Pic for user in github.com
		M	starred repos,
			name,
			company,
			blog,
		M	location,
			email,
			followers,
		M	following,
			public repos count,
			The time for using github.

		2.All repos the user owned,and for each repos,the data should
	
		Include:
		M	languages, 
		M	stargazers_count, watchers_count, forks_count, 
			open_issues_count, 
			network_count,
			subscribers_count,
			repo's size.
			
			has_wiki: true / false
			has_page: true / false
		
		What for:	
		We can use the repos information to...:
			1.Help we analysis the user's coding skills.
			2.Help the user to publish it to public.
			3.Give other users a suggest for join the repo or not.
			

		3.All following
		
		4.All stared

		Using the last two part to analysis what kind of things the
		user prefer doing.		
'''
