#!/usr/bin/perl -w

die "Usage: ./echon.pl <number of lines> <string>" if @ARGV != 2;

die "./echon.pl: argument 1 must be a non-negative integer" if $ARGV[0] !~ /^[0-9]+$/;

for ($i = 0; $i < $ARGV[0]; $i++) {
	print "$ARGV[1]\n";
}
