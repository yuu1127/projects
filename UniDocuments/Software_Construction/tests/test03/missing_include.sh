#!/bin/sh

for filename in "$@"
do
	lines=$(egrep "#include" $filename|egrep -v "<.+\.h>"|sed 's/#include //'|sed 's/"//g')
	#echo "$lines"
	for h_file in $lines
	do
		#echo "$line"
		if test ! -e $h_file
		then
			echo "$h_file included into $filename does not exist"
		fi
	done
done
