#!/usr/bin/perl -w

$N = 10;

foreach $arg (@ARGV) {
	# print "$arg\n";
    if ($arg eq "--version") {
        print "$0: version 0.1\n";
        exit 0;
    # handle other options
    # ...
    }
	elsif ($arg =~ /^-[0-9]+$/) {
		$N = -1 * $arg;
		#print "$N\n";
	} 
	else {
		#if ($arg =~ /^<.+$/){
		#  	print "haaa\n";
		# 	$arg = $arg =~ s/<//r; 
		#}
        push @files, $arg;
    }
}


foreach $file (@files) {
	# < is read , > is write
    open my $F, '<', $file or die "$0: Can't open $file\n";

    # process F
	$count = `wc -l < $file`;
	chomp($count);

	if ($#files > 1){
		print "==> $file <==\n";
		print "file lines is $count N is $N\n";
	}

	$i = 1;
	while ($line = <$F>){
		# or print pop
		if ($count < $N){
			print "$line";
		}
		elsif ($i > $count - $N){
			print "$line";
		}
		$i++;
	}
	close $F;
}


if (@files == 0) {
	#my $file = <STDIN>;
	#$count = `wc -l < $file`;
	#chomp($count);
	
	push @lines, <STDIN>;
	#print "pls define @files \n";
	#foreach $line (@lines){
	#	# or print pop
	#	print "$line\n";
	#}
	$count = @lines;
	for($i = 0; $i < @lines; $i++){
		if ($count < $N){
			print "$lines[$i]";
		}
		elsif ($i >= $count - $N){
			print "$lines[$i]";
		}
	}
}

