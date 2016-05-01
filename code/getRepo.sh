#!/bin/bash

#this shell script is use for download git_repo from github 
#for the git_repo we get,we just need .git/ direction
#
#the script accept two argument :
#1 for the name of the owner name
#2 for the name of the repo name

GIT=".git"

__author__='xuehao'
#echo ${__author__}


user_name=$1
repo_name=$2
http_repo_url="https://github.com/${user_name}/${repo_name}.git"
ssh_repo_url="git@github.com:${user_name}/${repo_name}.git"


echo "downloading repo  ${user_name}-${repo_name}... "
echo "this may cost a few minutes!"


#projects is the repos direction
if test -e ./projects
then
	cd projects
else
	mkdir projects
	cd projects
fi

if test -e ./${repo_name}
then
	sudo rm -r ${repo_name}
fi
if test -e ./.git
then
	echo "removing .git directory.please input your password"
	sudo rm -r .git
fi


#downloading repo
git clone $http_repo_url

if test -e ./${repo_name}
then
	cd ${repo_name}
	if test -e ./.git
	then
		mv .git ..
		echo "clean up..."
		sudo rm -r *
		sudo rm -r .*
		mv ../.git .
		echo "finish!"
	else
		echo "empty repo!"
	fi
else
	echo "initial failed!!!"
fi

cd ../..
exit 0
