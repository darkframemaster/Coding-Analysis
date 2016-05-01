#!/bin/bash
# run this script to commit

__author__='xuehao'
information=${0}

if test -e projects
then
	mv projects ~
fi

if test ! -e projects
then
	echo "git add -all"
	git add --all
fi

mv ~/projects .
