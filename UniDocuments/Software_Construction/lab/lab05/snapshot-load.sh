#!/bin/dash

if test $# != 1
then
	echo "usage $0 <Argument>"
	exit 1
fi
file_number=$1
base_directory="$(dirname $0)"
#echo "$(dirname $0)"
#base_directory="./"
$base_directory/snapshot-save.sh
r_directory=".snapshot.$1"
#echo $r_directory
for file in $r_directory/* 
do
	if test "$file" != "snapshot-save.sh" && test "$file" != "snapshot-load.sh"
	then
		#echo "$file to $base_directory"
		cp $file "./"
	fi
done
echo "Restoring snapshot $1"
