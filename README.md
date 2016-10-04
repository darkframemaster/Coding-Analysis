#pyrepo
A way to find data behind your repo.

##About
This is a tool use to analyse datas from git-repositories.

It was developed using python and flask, but it is used as a local tool, since we just use flask to build the UI part.

To use this tool to analyse your repo, you must have a .git folder and copy the folder to the `<path_to_pyrepo>/app/local/projects` directory.

###About the dirs.
```
pyrepo/
|
+- app/				<--Where the flask-related code located
|	|
|	+- local/
|		|
|		+- collectors/			<--Data collectors	
|		|
|		+- projects				<--Place to store your .git folder
|
|
+- flask_config.py	<--This is the configuration for flask.
|
+- docs/			<--related documents
|
+- LICENSE
|
+- requirements.txt
|
+- README.mkd
|
+- setup.py(empty)
|
+- Makefile(empty)
|
/
```
