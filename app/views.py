#usr/bin/env python3

from flask  import render_template, flash, redirect, session, url_for, request, g

from app import app
from .forms import SearchForm
from .local.analysis import RepoAnalysis
from .local.doshell import change_repo

result = {}

@app.route('/')
@app.route('/index')
def index():
	return render_template("index.html",
			title = 'welcome to SIOS')

@app.route('/aboutus')
def aboutus():
	return render_template("aboutus.html",title = 'Home page')


'''
	Local works:
		This part can work without internet
'''
@app.route('/settings', methods=['GET', 'POST'])
def settings():
	form = SearchForm()	
	global result

	if form.validate_on_submit():
		repo_name = form.searching.data
		if change_repo(repo_name)==False:
			flash('Oh, no such repo in project path!')
			return redirect(url_for('settings'))
		else:
			repo_ana = RepoAnalysis(repo_name)
			result['contributors'] = repo_ana.user_stats
			result['commits'] = repo_ana.commit_dic
			result['users'] = repo_ana.contributors()
			result['repo_data'] = repo_ana.repo_level()
			result['user_rank'] = repo_ana.sort_users() 
			result['picture_locations'] = repo_ana.save_figures()
	return render_template("settings.html",
			title ="settings",
			form = form)

@app.route('/contributors')
def contributors():
	global result

	if 'contributors' not in result:
		flash('chose a repo!')
		return redirect(url_for('settings'))
	return render_template("contributors.html",
		title = "contributors",
		contributors = result['contributors'])

@app.route('/commits')
def commits():
	global result

	if 'commits' not in result:
		flash('chose a repo!')
		return redirect(url_for('settings'))
	return render_template('commits.html',
		title = "commits info",
		commits = result['commits'])
	
@app.route('/report')
def report():
	global result
	
	if 'repo_data' and 'user_rank' not in result:
		flash('chose a repo!')
		return redirect(url_for('settings'))
	return render_template("report.html",
		title = "analysis result",
		users = result['users'],
		repo_data = result['repo_data'],
		user_rank = result['user_rank'],
		picture_locations = result['picture_locations'])
