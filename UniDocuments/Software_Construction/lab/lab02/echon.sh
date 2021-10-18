#!/bin/sh

n=$1
m=$2
if (($# == 2))
then
  #if test $1 -ge 0 && [$1 =~ ^[0-9]+$]
  #if [[ $n =~ ^[0-9]+$ ]]
  if [[ $n =~ ^[0-9]+$ ]]
  then
      while test $n -gt 0 
      do
          echo "$m"
          n=$((n - 1))
      done
  else
     echo "./echon.sh: argument 1 must be a non-negative integer" 
  fi
else
   echo "Usage: ./echon.sh <number of lines> <string>"
fi
