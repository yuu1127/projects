#!/usr/bin/perl -w


use List::MoreUtils qw(uniq);


@words = @ARGV;

# foreach my $word (@words){
#     print "$word\n";
# }

my @unique_words = uniq @words;

foreach my $word (@unique_words){
    print "$word ";
}
print "\n";