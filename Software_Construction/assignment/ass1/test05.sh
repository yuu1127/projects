#!/bin/dash

# for shurug-commit -a

a=`rm -rf .shrug` > /dev/null

echo "`./shrug-init`"
echo "`echo 'line 1' > a`"
echo "`./shrug-add a`"
echo "`./shrug-commit -m First Commit`"
echo "`echo 'line 2' >> a`"
echo "`echo 'line 1' > b`"
echo "`./shrug-add b`"
echo "`./shrug-commit -m Second Commit`"
echo "`echo 'line 3' >> a`"
echo "`echo 'line 2' >> b`"
echo "`echo 'line 1' > c`"
echo "`./shrug-add c`"
echo "`./shrug-commit -a -m Third Commit`"

# shoud index upated becasue of -a option
echo "`./shrug-show 0:a`"
echo "---------------------"
echo "`./shrug-show :a`"
echo "---------------------"
echo "`./shrug-show 1:b`"
echo "---------------------"
echo "`./shrug-show :b`"
echo "---------------------"
echo "`./shrug-show 2:c`"
echo "---------------------"
echo "`./shrug-show :c`"