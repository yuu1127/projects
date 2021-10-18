#!/bin/sh

# while read INPUT
# do
#   echo $INPUT |tr '[01234]' '<' | tr '[6789]' '>'
# done

while read input
do
  echo $input |tr '[01234]' '<' | tr '[6789]' '>'
done