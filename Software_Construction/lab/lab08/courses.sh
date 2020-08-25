#!/bin/dash

prefix=$1
base_url="http://www.timetable.unsw.edu.au/current/"$prefix"KENS.html"
#courses=$(curl --location --silent $base_url)
curl --location --silent $base_url| egrep "$prefix[0-9][0-9][0-9][0-9].html" |
sed "s/.*\($prefix[0-9][0-9][0-9][0-9]\)\.html[^>]*> *\([^<]*\).*/\1 \2/"|
egrep -v "$prefix[0-9][0-9][0-9][0-9] $prefix[0-9][0-9][0-9][0-9]"|
sort|
uniq
