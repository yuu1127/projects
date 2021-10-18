#!/bin/dash

# for shurug-log

a=`rm -rf .shrug` > /dev/null

echo "`./test01.sh`"
# should show 2 line msg
echo "`./shrug-log`"
echo "`./test02.sh`"
# should show 1 line msg (2nd one is nothing commit)
echo "`./shrug-log`"