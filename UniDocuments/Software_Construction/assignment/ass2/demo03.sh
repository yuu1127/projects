#!/bin/dash

# while + for + if

is_tens() {
    local n
    n=$1
    test $((n % 10)) -eq 0 && return 0
    return 1
}

end=100
number=0

while test $number -le $end
do
    for num in 1 2 3 4 5 6 7 8 9 10
    do
        is_tens $number && echo "$number"
        number=`expr $number + $num`  # increment number
    done
done