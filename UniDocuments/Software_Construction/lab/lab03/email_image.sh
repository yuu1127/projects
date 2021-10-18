#!/bin/sh

for filename in "$@"
do
	display $filename 
	#echo "$filename"
	echo "Address to e-mail this image to?"
	read ADDRESS
	echo "Message to accompany image?"
	read MSG
	echo "$MSG"|mutt -s 'try_mail!' -e 'set copy=no' -a $filename -- $ADDRESS 
	echo "$filename sent to $ADDRESS"
done
