#!/bin/sh

filename=$1;
common_name=$(egrep "COMP(2041|9041)" $filename|cut -d '|' -f3|cut -d ' ' -f2|sort|uniq -c|sort|tail -n 1|sed 's/^ *//'|cut -d ' ' -f2)
echo "$common_name"
