#usr/bin/env python3

from flask  import render_template, flash, redirect, session, url_for, request, g, jsonify

from app import app
from .forms import SearchForm
from .local.analysis import RepoAnalysis
from .local.doshell import change_repo

result = {}
repo_ana = None

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
	global repo_ana

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
		)

@app.route('/get/repo/data')
def get_repo_data():
	global result

	params = request.args
	return_json = params.get('return_json')

	if not result:
		return redirect(url_for('settings'))
	else:
		if return_json:
			return jsonify(
				users = result.get('users', []),
				commit = result.get('commits', []),
				repo_data = result.get('repo_data', []),
				user_rank = result.get('user_rank', []),	
				contributors = result.get('contributors', []),
			)
		else:
			return render_template("graph.html")


@app.route('/get/commit/times/by/time')
def get_commit_times_by_time():
	global repo_ana

	if not repo_ana:
		return redirect(url_for('settings'))
	
	params = request.args
	year  = params.get('year')
	month = params.get('month')
	return_json = params.get('return_json')

	try:
		year  = int(year) if year else year
		month = int(month) if month else month
		if not year and not month:
			return jsonify(status = 'failed',msg = 'invalid time data')
	except:
		return jsonify(
			status = 'failed',
			msg = 'invalid time data',
		)

	repo_commit_count  = repo_ana.get_repo_commit_times_count(year, month)

	if return_json:
		return jsonify(
			repo_commit_count  = repo_commit_count,
		)
	else:
		return render_template("graph.html")


@app.route('/users/contributions')
def get_users_contributions():
	global repo_ana
	
	if not repo_ana:
		return redirect(url_for('settings'))

	user_contrib_count = repo_ana.get_users_contributions_count()
	
	params = request.args
	return_json = params.get('return_json')
	if return_json:
		return jsonify(
			user_contrib_count = user_contrib_count,
		)
	else:
		return render_template("graph.html")
