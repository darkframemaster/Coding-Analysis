#!/bin/bash
#run this script to commit

__author__='xuehao'
information=${0}

if test -e projects
then
	mv projects ~
fi

if test ! -e projects
then
	echo "git commit -m ${information}"
	git add --all
	git commit -m ${information}
fi

mv ~/projects .
