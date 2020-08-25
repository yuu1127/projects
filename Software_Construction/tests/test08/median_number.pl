#!/usr/bin/perl

@numbers = @ARGV;
#print "@numbers\n"
@s_numbers = sort {$a <=> $b} (@numbers);
#print "@s_numbers\n";
$m_index = int(@numbers / 2);
$m_number = @s_numbers[$m_index];
print "$m_number\n";