#!/usr/bin/perl -w

$filename = $ARGV[0];

open my $F, '<', $filename or
	die "$0: open of $filename failed: $!\n";
    @lines = <$F>;
close $F;

# length s return string length
@sorted = sort { length $a <=> length $b } @lines;

foreach $line (@sorted) {
    print "$line";
}