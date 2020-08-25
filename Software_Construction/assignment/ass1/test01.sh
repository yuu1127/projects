#!/bin/dash

# for shurug-add (change contents for second commit)

a=`rm -rf .shrug` > /dev/null

echo "`./shrug-init`"
echo "`echo 'line 1' > a`"
echo "`echo 'line 1' > b`"
echo "`./shrug-add a`"
# should success
echo "`./shrug-commit -m First Commit`"
echo "`echo 'line 2' >> a`"
echo "`./shrug-add a b`"
# should success
echo "`./shrug-commit -m Second Commit`"