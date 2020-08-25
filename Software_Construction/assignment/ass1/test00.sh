#!/bin/dash

# for shurug-init
# check shrug add or other shrug-not work 

a=`rm -rf .shrug` > /dev/null

echo "`echo "line 1" > a`"
echo "`./shrug-add a`"
#this should show error
echo "`./shrug-init`"
echo "`./shrug-add a`"
echo "`./shrug-commit -m First Commit`"
#this should works