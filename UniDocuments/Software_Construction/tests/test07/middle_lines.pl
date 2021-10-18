#!/usr/bin/perl -w

$filename = $ARGV[0];

open my $F, '<', $filename or
	die "$0: open of $filename failed: $!\n";

    @lines = <$F>;

close $F;


if (@lines % 2 == 0){
    $even = @lines / 2;
    #print "$even\n";
    $cnt = 0;
    foreach $line (@lines){
        if ($cnt == $even || $cnt == $even - 1){
            print "$line";
        }
        $cnt ++;
    }
}
else{
    $odd = int(@lines / 2);
    #print "$odd\n";
    $cnt = 0;
    foreach $line (@lines){
        if ($cnt == $odd){
            print "$line";
        }
        $cnt ++;
    }
}
