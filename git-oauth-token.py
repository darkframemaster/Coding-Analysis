#!/usr/bin/env python3.4
import sys
import json
import requests
from requests.auth import HTTPBasicAuth

data ='{"scopes":["pub_repo"]}'

user = sys.argv[1]
pw = sys.argv[2]
r = requests.post("https://api.github.com/authorizations",data=data,auth=HTTPBasicAuth(user, pw))
res = r.json()
if('token' in res.keys()):
	print(res['token'])
else:
	print(res['message'])
