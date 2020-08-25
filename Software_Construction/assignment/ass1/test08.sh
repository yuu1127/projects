#!/bin/dash

# for shrug-status

a=`rm -rf .shrug` > /dev/null

echo "`./shrug-init`"
echo "`echo 'line 1' > a`"
echo "`echo 'line 1' > b`"
echo "`echo 'line 1' > c`"
# everything untracked
echo "`./shrug-status`"
echo "`./shrug-add a b`"
echo "`./shrug-commit -m First Commit`"
# a b is same as repo
echo "`./shrug-status`"
echo "`echo 'line 2' >> a`"
echo "`echo 'line 2' >> c`"
# c is never added so untraced, a content changed but not staged
echo "`./shrug-status`"
