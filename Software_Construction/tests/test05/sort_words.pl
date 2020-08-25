#!/usr/bin/perl

#@lines = <STDIN>;
@lines = <STDIN>;

foreach $line(@lines){
    # @s_lines = split(' ', $line);
    # @s_lines = sort(@s_lines);
    # print "@s_lines\n";
    @s_lines = split(' ', $line);
    @s_lines = sort(@s_lines);
    print "@s_lines\n";
    # $sorted_line = join(' ', @s_lines);
    # print "$sorted_line";
}

#@n_lines = sort split(@lines);

#print "@n_lines";