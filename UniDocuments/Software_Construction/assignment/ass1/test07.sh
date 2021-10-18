#!/bin/dash

# for shrug-rm force

a=`rm -rf .shrug` > /dev/null

echo "`./shrug-init`"
echo "`echo 'line 1' > a`"
echo "`echo 'line 1' > b`"
echo "`./shrug-add a b`"
echo "`./shrug-commit -m First Commit`"
echo "`echo 'line 2' >> a`"
echo "`./shrug-add a`"
# this should show error
echo "`./shrug-rm --force a`"
# this works
echo "`echo 'line 10' > a`"
echo "`./shrug-add a`"
# this works
echo "`./shrug-rm --force --cached a`"
echo "`./shrug-commit -m Second Commit`"