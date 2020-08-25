#!/bin/sh

# filename=$1;

# echo $contetns_a

egrep "name" $1| cut -d \" -f4| sort | uniq