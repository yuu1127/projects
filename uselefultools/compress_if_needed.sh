#!/bin/sh

for file in $@
do
    #echo $file
    xz -k $file
    size=$(ls -l $file| tr -s ' '| cut -d ' ' -f5)
    c_size=$(ls -l "$file.xz"| tr -s ' '| cut -d ' ' -f5)
    #echo "$c_size naniii"
    if (($size >= $c_size))
    then
        echo "$file $size bytes, compresses to $c_size bytes, compressed"
        rm $file
    else
        echo "$file $size bytes, compresses to $c_size bytes, left uncompressed"
        rm "$file.xz"
    fi
done

