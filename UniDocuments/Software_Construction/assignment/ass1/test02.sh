#!/bin/dash

# for shurug-add (change contents for second commit -> nothing to commit)

a=`rm -rf .shrug` > /dev/null

echo "`./shrug-init`"
echo "`echo 'line 1' > a`"
echo "`echo 'line 1' > b`"
echo "`./shrug-add a b`"
# should success
echo "`./shrug-commit -m First Commit`"
echo "`./shrug-add a b`"
# should show nothing to commit
echo "`./shrug-commit -m Second Commit`"