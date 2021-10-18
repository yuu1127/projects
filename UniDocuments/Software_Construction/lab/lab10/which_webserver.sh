#!/bin/sh

for website in "$@"
do
    printf '%s ' "$website"
    # curl -I -s
    value=$(curl -I -s $website | egrep -i '^Server: .*' | sed 's/Server: //i')
    #value=$(curl $website | tr A-Z a-z| grep -E '<[^/> ]+') L
    echo $value
done 