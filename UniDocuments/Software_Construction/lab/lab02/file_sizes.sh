#!/bin/sh

s_files=""
m_files=""
l_files=""

for file in *
do
#   size=$(wc -c $file|sed 's/^ *//'|cut -d ' ' -f1)
#   name=$(wc -c $file|sed 's/^ *//'|cut -d ' ' -f2)
  size=$(wc -c $file| sed 's/^ *//'| cut -d ' ' -f1)
  name=$(wc -c $file| sed 's/^ *//'| cut -d ' ' -f2)
  #echo "$size $name"
  if test $size -lt 10
  then
     #echo "nyaaaa"
     s_files+="${name} "
  elif test $size -lt 100
  then
     #echo "unaaa"
     m_files+="${name} "
  else
     l_files+="${name} "
  fi
done
echo "Small files: $s_files"
echo "Medium-sized files: $m_files"
echo "Large files: $l_files"
