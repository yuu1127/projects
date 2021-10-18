#!/bin/dash

# nest for loop
# should be 27 combination

for word1 in Andrew John Eric
do
    for word2 in Eric Andrew John
    do
        for word3 in John Eric Andrew
        do
            echo $word1 $word2 $word3
        done
    done
done
