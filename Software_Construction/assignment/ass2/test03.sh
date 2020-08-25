#!/bin/dash

#argv -- test

arg1=$1
arg2=$2
arg3=$3

sum=$(($arg1 + $arg2 + $arg3))
echo "$sum"

number=$arg1;
while test $number -le $arg3
do
    echo "$number"
    number=`expr $number + 1`
done
#echo "$number"