#!/bin/sh

directory=$1;
# just show each directory path:wq


for file in $(find $directory)
do
    filename=$(basename $file)
    dir=$(dirname $file)
    #echo $filename
    if test $filename = "Makefile"
    then
        #echo $dir $file
        echo "Running make in $dir"
        #make -C $dir
        # tar.PHONY:=
        if test $# -eq 2
        then
            (cd $dir && make $2)
        else
            (cd $dir && make)
        fi
        #cd $dir && make
    fi
    #echo $filename
done