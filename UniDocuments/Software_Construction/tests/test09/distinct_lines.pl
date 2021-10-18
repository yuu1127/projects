#!/usr/bin/perl -w

$max_num = shift @ARGV;
$cnt = 0;
$flag = 0;

while ($line = <>){
    $line =~ tr/A-Z/a-z/;
    $line =~ s/ //g;
    $hash{$line}++;
    #print "$line\n";
    #print "$hash{$line}\n";
    $cnt++;
    $num = keys %hash;
    if($num == $max_num){
        $flag = 1;
        last;
    }
}

if($flag == 1){
    print "$max_num distinct lines seen after $cnt lines read.\n"
}
else{
    print "End of input reached after $cnt lines read - $max_num different lines not seen.\n"
}