#!/bin/sh

filename=$1

if test ! -e $filename
then
	echo "there is not such file"
	exit 1
fi
#echo "$filename";
filename_=$(echo $filename|sed -E 's/.[0-9]+$//')
#echo "$filename";
lastchar=$(echo $filename|rev|cut -d '.' -f 1|rev)
#echo "$lastchar";
new_filename="${filename_}.0"
#echo "$new_filename"
#if [[ ! $lastchar =~ ^[0-9]+$ ]]
#if test ! -e $new_filename
#then
	#new_filename="${filename}.0"
#	echo "$new_filename";
#else
while test -e ".$new_filename"
do
	lastchar=$(($lastchar + 1))
	#echo "$lastchar"
	#filename_=$(echo $filename|sed -E 's/.[0-9]+$//')
	new_filename="${filename_}.${lastchar}"
	#echo "$new_filename"
done
cp $filename ".$new_filename"
echo "Backup of '$filename' saved as '.$new_filename'";
#fi
