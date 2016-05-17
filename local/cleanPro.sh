#!/bin/bash

#run this shell script before commit to clean up the directory ./projects

__author__='xuehao'


echo "clean up..."
if test -e ./projects
then 
	cd projects
	if test -e __warning__
	then
		mv __warning__ ..
		sudo rm -r *
		mv ../__warning__ .
	else
		sudo rm -r *
	fi
fi

echo "finish!"

exit 0
