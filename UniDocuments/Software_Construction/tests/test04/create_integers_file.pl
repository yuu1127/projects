#!/usr/bin/perl -w

$begin = $ARGV[0];
$end = $ARGV[1];
$filename = $ARGV[2];

open my $F, '>', $filename or
	die "$0: open of $filename failed: $!\n";

    for($i = $begin;$i <= $end;$i++){
        #print $F "$i\n"
        print $F "$i\n"
    }

close $F;