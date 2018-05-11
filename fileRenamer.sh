#!/bin/bash

if [ -z $1 ]
then
	echo "Please input a directory for renaming"	
	exit 1
fi

a=1
for i in $1/*$2; do
	new=$(printf "%04d$3" "$a") #04 pad to length of 4
	mv -i -- "$i" "$1/$new"
	let a=a+1
done
