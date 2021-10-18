#!/bin/sh

begin=$1
end=$2
filename=$3
for ((i=$begin;i<=$end;i++))
do
	echo $i
done >$filename
