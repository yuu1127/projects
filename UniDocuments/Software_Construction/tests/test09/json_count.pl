#!/usr/bin/perl -w

$spece = $ARGV[0];
$filename = $ARGV[1];

open my $f, $filename or die "Can not open $filename\n";

    while ($line = <$f>) {
        if ($line =~ /"how_many"/) {
            $line =~ s/ //g;
            $line =~ s/"how_many"://;
            $line =~ s/,//;
            $line =~ s/\n//;
            $value = $line;
            #print "$line"
        }
        elsif ($line =~ /"species"/) {
            $line =~ s/ //g;
            $line =~ s/"species"://;
            $line =~ s/,//;
            $line =~ s/\n//;
            $line =~ s/"//g;
            #$hash{$line}++;
            $hash{$line} += $value;
            #print "$value\n";
            #print "$line\n";
        }
    }
    $spece =~ s/ //g;
    #print "$spece\n";
    print "$hash{$spece}\n";

close $f;