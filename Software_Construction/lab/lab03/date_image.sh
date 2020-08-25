#!/bin/sh

for filename in "$@"
do 
   TIME=$(ls -l $filename|cut -d ' ' -f6-8)
   #echo "$TIME" 
   convert -gravity south -pointsize 36 -draw "text 0,10 '$TIME'" $filename $filename  
   #display "$filename"
done 
