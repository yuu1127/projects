#!/bin/sh

for filename in *.htm
do
	#echo "$filename"
	new_filename=$(echo $filename|sed 's/.htm/.html/')
	#new_filename=$(echo $filename|tr '.htm' '.html')
	if test -e "$new_filename"
	then
		echo "$new_filename exists"
		exit 1
	fi
	cp "$filename" "$new_filename"
	rm "$filename"
done
