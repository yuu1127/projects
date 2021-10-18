#!/usr/bin/perl -w

$num_of_line = $ARGV[0];
$filename = $ARGV[1];

open my $F, '<', $filename or
	die "$0: open of $filename failed: $!\n";

@lines = <$F>;
$cnt = 1;
foreach $line(@lines){
    if($cnt == $num_of_line){
        print $line;
    }
    $cnt++;
}


close $F;