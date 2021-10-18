#!/usr/bin/perl -w

foreach $word (@ARGV){
    @chars = split(//, @word);
    $cnt = 0;
    $flag = 0;
    foreach $char (@chars){
        if($char =~ /[aeiuo]/i){
            $cnt++;
        }
        else{
            $cnt=0;
        }
        if($cnt == 3){
            $flag = 1;
        }
    }
    if($flag == 1){
        print "$word ";
    }
}
print "\n";