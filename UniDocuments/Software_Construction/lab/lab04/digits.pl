#!/usr/bin/perl -w

#$text = <STDIN>;
#print "$text\n";
#chomp $text;
#foreach $c ($text){
#	print "chomp is the best";
#	print "$c\n";
#}

while ($text = <STDIN>){
	$text =~ tr/[0-4]/</;
	$text =~ tr/[6-9]/>/;
	print "$text";
}
