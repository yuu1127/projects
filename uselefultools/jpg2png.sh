#!/bin/sh

for filename in *
do
    new_filename=$(echo $filename|sed 's/.jpg/.png/')
    #alternative of if
    test "$filename" = "$new_filename" && continue
    #test -e exist or not
    if test -e "$new_filename"
    then
        echo "$new_filename already exists"
        exit 1
    fi
    cp "$filename" "$new_filename"
    rm "$filename"
done
