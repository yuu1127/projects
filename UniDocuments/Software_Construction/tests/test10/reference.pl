#!/usr/bin/perl -w

@lines = <STDIN>;


# caz last line no \n
# be careful for line just try to understnd inputs

foreach my $line (@lines){
    if($line =~ /\#\d+/){
        $line =~ s/\#//;
        #print "$line\n";
        print $lines[$line - 1];
        if($line-1 == $#lines){
            print "\n";
        }
    }
    else{
        print $line;
    }
}
#print "\n";