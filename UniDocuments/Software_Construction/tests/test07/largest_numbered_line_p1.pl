#!/usr/bin/perl -w

@lines = <STDIN>;

foreach $line (@lines){
    $max = 0;

    @nums = $line =~ /\-?(?:\d+\.?\d*)/g;
    foreach $x (@nums){
        $max = $x if $x >= $max;
    }
    $hash{$line} = $max;
    if(!$t_max){
        $t_max = $max;
    }
    else{
        $t_max = $max if $max >= $t_max;
    }
}

foreach $line (@lines){
    print $line if $hash{$line} == $t_max && $t_max != 0;
}
