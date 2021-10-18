#!/usr/bin/perl -w

use File::Basename;

die "Usage: $0 <word>\n" if @ARGV != 1;

$sp_word = shift @ARGV;
$music_directory = "lyrics/";

foreach $filename (glob "$music_directory/*.txt") {
    open my $F, '<', $filename or
	die "$0: open of $filename failed: $!\n";
    @lines = <$F>;
    $word_count = 0;
    $frequency_{$filename}{lc($sp_word)} = 0;
    foreach $line (@lines) {
        @s_lines = split(/[^a-zA-Z]/, $line);
        foreach $word (@s_lines){
            if ($word =~ /^[a-zA-Z]+$/){
                $word_count++;
                if ($word =~ /^$sp_word$/i){
                    $frequency_{$filename}{lc($word)}++;
                }
            }
        }
    }
    $rate = $frequency_{$filename}{$sp_word} / $word_count;
    $filename_ = $filename =~ s/$music_directory\///r;
    $filename_ =~ s/\.txt//;
    $filename_ =~ s/_/ /g;
    printf "%4d/%6d = %.9f %s\n", $frequency_{$filename}{$sp_word}, $word_count, $rate, $filename_;
    close $F;
}