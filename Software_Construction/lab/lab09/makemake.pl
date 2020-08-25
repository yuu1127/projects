#!/usr/bin/perl -w

#$pattern =~ /^\s*(int|void)\s*main\s*\(/;
$m_file = "Makefile";
$date = `date`;
$cc = "gcc";
$cflags = "-Wall -g";
$main_file = "";
#@c_files = {};
#%c_file_hash = {};

print "# $m_file generated at $date";
print "\n";
print "CC = $cc\n";
print "CFLAGS = $cflags";
print "\n";

# store c files(change to o file)
foreach $filename (glob "*.{c}") {
    push (@c_files, $filename);
}


foreach $filename (glob "*.{c,h}") {
    #push (@c_files, $file);
    open my $F, '<', $filename or
	die "$0: open of $filename failed: $!\n";
        @lines = <$F>;
    close $F;
    foreach $line(@lines){
        if($line =~ /^\s*(int|void)\s*main\s*\(/){
            $main_file = $filename;
        }
        # put dependency into hash
        # need to change
        if($line =~ /#include\s*".*"/){
            #$dependencies{$target} = $dependencies;
            $line =~ s/#include\s*//;
            $line =~ s/"//g;
            $filename =~ s/\..//;
            push (@{$dependencies{"$filename"}} ,$line);
            #print "$line\n";
        }
    }
}

print "\n";

$main_file =~ s/\..//;
print "$main_file:   ";
foreach my $key (@c_files)
{
    $key =~ s/\../.o/;
    print "$key ";
}

print "\n";
print "\t\$(CC) \$(CFLAGS) -o \$\@ ";

foreach my $key (@c_files)
{
    $key =~ s/\../.o/;
    print "$key ";
}

print "\n";
print "\n";

foreach my $key (sort(keys %dependencies))
{
    $o_key = $key;
    $o_key = $key . ".o";
    print "$o_key:\t";
    @ds = @{$dependencies{$key}};
    chomp(@ds);
    foreach my $d (@ds){
        print "$d ";
    }
    print "$key.c\n";
    #print "\n";
}
