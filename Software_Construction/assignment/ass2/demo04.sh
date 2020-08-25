#!/bin/dash

# many sub functions !!

is_odd() {
    local n
    n=$1
    test $((n % 2)) -nq 0 && return 0
    return 1
}

is_even() {
    local n
    n=$1
    test $((n % 2)) -eq 0 && return 0
    return 1
}

is_prime() {
    local n i
    n=$1
    i=2
    while test $i -lt $n
    do
        test $((n % i)) -eq 0 && return 1
        i=$((i + 1))
    done
    return 0
}

for number in 1 2 3 4 5 6 7 8 9 10
do
    test $number == 1 || echo "start !!"
    is_odd $number && echo "$number is odd number"
    is_even $number && echo "$number is even number"
    is_prime $number && echo "$number is prime number"
    test $number == 10 || echo "end !!"
done