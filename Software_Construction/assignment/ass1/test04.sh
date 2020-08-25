#!/bin/dash

# for shurug-show

a=`rm -rf .shrug` > /dev/null

echo "`./shrug-init`"
echo "`echo 'line 1' > a`"
echo "`./shrug-add a`"
echo "`./shrug-commit -m First Commit`"
echo "`echo 'line 1' > b`"
echo "`./shrug-add b`"
echo "`./shrug-commit -m Second Commit`"
echo "`echo 'line 1' > c`"
echo "`./shrug-add c`"
echo "`./shrug-commit -m Third Commit`"

# no error
echo "`./shrug-show 0:a`"
echo "`./shrug-show 1:a`"
echo "`./shrug-show 2:a`"
echo "`./shrug-show :a`"

# only 1st line error
echo "`./shrug-show 0:b`"
echo "`./shrug-show 1:b`"
echo "`./shrug-show 2:b`"
echo "`./shrug-show :b`"

# 1st and Second line error
echo "`./shrug-show 0:c`"
echo "`./shrug-show 1:c`"
echo "`./shrug-show 2:c`"
echo "`./shrug-show :c`"