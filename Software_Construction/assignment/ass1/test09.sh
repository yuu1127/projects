#!/bin/dash

# for shrug-status + rm

a=`rm -rf .shrug` > /dev/null

echo "`./shrug-init`"
echo "`echo 'line 1' > a`"
echo "`echo 'line 1' > b`"
echo "`echo 'line 1' > c`"
# everything untracked
echo "`./shrug-status`"
echo "`./shrug-add a b c`"
echo "`./shrug-rm --cached c`"
# a,b in index c is untracked
echo "`./shrug-status`"
echo "`./shrug-commit -m First Commit`"
# a,b same as repo
echo "`./shrug-status`"
echo "`echo 'line 2' >> a`"
# should show error since a changed
echo "`./shrug-rm a`"
echo "`./shrug-rm --force --cached b`"
echo "`./shrug-rm --force a`"
# a is deleted from directory and index, b is untracked since not in index
echo "`./shrug-status`"