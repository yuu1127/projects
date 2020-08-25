#!/bin/sh

f_directory=$1;
s_directory=$2;

for f_file in "./$f_directory"/*
do
    filename=$(basename "$f_file")
    #echo $filename
    if test -e "./$s_directory/$filename"
    then
        if diff "$f_file" "./$s_directory/$filename" >/dev/null
        then
            echo "$filename"
        fi
    fi
done
