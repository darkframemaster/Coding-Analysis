#!/usr/bin/env python3

from flask.ext.wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators  import DataRequired

'''
DataRequired for checking the data field is not empty.
'''
class SearchForm(Form):
	searching = TextField('searching', validators = [DataRequired()])
