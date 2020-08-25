#!/usr/bin/perl

$filename = $ARGV[0];

# take every contents line of file
open my $F, '<', $filename or
	die "$0: open of $filename failed: $!\n";
    @lines = <$F>;
close $F;

open my $F, '>', $filename or
	die "$0: open of $filename failed: $!\n";
    foreach $line(@lines){
        $line =~ s/[0-9]/#/gi;
        print $F "$line";
    }
close $F;