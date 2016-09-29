#usr/bin/env python3

from flask  import render_template, flash, redirect, session, url_for, request, g

from app import app
from .forms import SearchForm
from .local.analysis import RepoAnalysis
from .local.doshell import change_repo


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
@app.route('/local', methods=['GET', 'POST'])
def local():
	users = {}
	repo_data = {}
	user_rank = []
	picture_locations = []

	users_rank = None
	form = SearchForm()	
	if form.validate_on_submit():
		repo_name = form.searching.data
		if change_repo(repo_name)==False:
			flash('Oh, no such repo in project path!')
			return redirect(url_for('local'))
		else:
			repo_ana = RepoAnalysis(repo_name)
			users = repo_ana.contributors()
			repo_data = repo_ana.repo_level()
			user_rank = repo_ana.sort_users() 
			picture_locations = repo_ana.save_figures()
	return render_template("local.html",
				title ="localwork",
				form = form,
				users = users,
				repo_data = repo_data,
				user_rank = user_rank,
				picture_locations = picture_locations)
