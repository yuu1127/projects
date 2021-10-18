#!/usr/bin/perl -w

$word_count = 0;
$sp_word = shift @ARGV;

#die "Usage: $0 <word>\n" if @ARGV != 1;

foreach $line ( <> ) {
    # @fields = split(/\|/, $enrollment);
    @s_lines = split(/[^a-zA-Z]/, $line);
    print "@s_lines\n";
    #@es_lines = grep(s/\s*$//g, @s_lines);
    foreach $word (@s_lines){
        if ($word =~ /^$sp_word$/i){
            #print $word;
            $word_count++;
        }
    }
}

print "$sp_word occurred $word_count times\n";