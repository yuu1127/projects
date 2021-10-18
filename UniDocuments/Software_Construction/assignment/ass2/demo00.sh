#!/bin/dash

# nest while loop !!

start=$1
finish=$2
number=$start
finish2=$2 * 3

while test $number -le $finish
do
    while test $number -le $finish2
    do
        echo $number
    done
    number=`expr $number + 1`  # increment number
done