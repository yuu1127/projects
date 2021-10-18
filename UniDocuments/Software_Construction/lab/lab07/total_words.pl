#!/usr/bin/perl -w


$word_count = 0;
@lines = <>;

foreach $line (@lines) {
    # @fields = split(/\|/, $enrollment);
    @s_lines = split(/[^a-zA-Z]/, $line);
    #@es_lines = grep(s/\s*$//g, @s_lines);
    foreach $word (@s_lines){
        if ($word =~ /^[a-zA-Z]+$/){
            #print $word;
            $word_count++;
        }
    }
}

print "$word_count words\n";