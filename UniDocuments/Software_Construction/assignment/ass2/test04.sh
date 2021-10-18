#!/bin/dash

#function and $(()) test

is_odd_even() {
    local n i
    n=$1
    i=2
    test $((n % 2)) -eq 0 && return 1
    return 0
}

i=1
while test $i -le 10
do
    is_odd_even $i && echo "$i odd! "
    is_odd_even $i || echo "$i even! "
    i=$((i + 1))
done
