#!/bin/dash

directory_name="snapshot"
number=0
new_directory="${directory_name}.${number}"
while test -e .$new_directory
do
	number=$(($number + 1))
	new_directory="${directory_name}.${number}"
done
#echo "$new_directory"
mkdir .$new_directory
echo "Creating $directory_name $number"
#cp !(.*|$0|snapshot-load.sh) ./$new_directory
# dont't use ls to get file
#files=$(ls)
this_file=$(echo $0 | sed 's/\.\///')
#echo "$this_file"
for file in * 
do
	if test "$file" != "snapshot-save.sh" && test "$file" != "snapshot-load.sh"
	#&& [[ ! "$file" =~ "^\..+" ]]
	then
		#echo "aaa\n"
		#echo "$this_file\n"
		#echo "$file"
		cp $file ./.$new_directory
	fi
done
