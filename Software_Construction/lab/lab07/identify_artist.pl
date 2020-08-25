#!/usr/bin/perl -w

use File::Basename;
use List::MoreUtils qw(uniq);

foreach $song_file (@ARGV) {
    #print "$song_file\n";
    open my $F, '<', $song_file or
	die "$0: open of $song_file failed: $!\n";
    @lines = <$F>;
    foreach $line (@lines) {
        @s_lines = split(/[^a-zA-Z]/, $line);
        push(@{$text_data{"$song_file"}}, @s_lines);
    }
    #$text_data{$song_file} = @s_lines;
    #print "nayaaaa\n";
    #print "@{$text_data{$song_file}}[0]\n";
    close $F;
}

$music_directory = "lyrics/";

sub re_log_probability{
    @words = @{$_[0]};
    #print "@words[0]\n";
    $filename = $_[1];
    open my $F, '<', $filename or
    die "$0: open of $filename failed: $!\n";
    @lines = <$F>;
    close $F;
    $rate = 0;
    $singer_length = 0;
    foreach $sp_word (@words) {
        $word_count = 0;
        #next if $seen{$zid};
        #print "$sp_word\n";
        $frequency_{$filename}{lc($sp_word)} = 0;
        # if (!$frequency_{$filename}{lc($sp_word)}){
        #     $frequency_{$filename}{lc($sp_word)} = 0;
        # }

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
        if ($singer_length == 0){
            $singer_length = $word_count;
        }
        #print "the number of words $singer_length frequency $frequency_{$filename}{lc($sp_word)}\n";
        $rate += log(($frequency_{$filename}{lc($sp_word)} + 1) / $word_count);
    }
    # @u_words = uniq(@words);
    # foreach $sp_word (@u_words) {
    #     $times = $seen{lc($sp_word)};
    #     print "the number of $sp_word is $times aaa $singer_length \n";
    #     #$rate += $seen{lc($sp_word)} * log(($frequency_{$filename}{lc($sp_word)} + 1) / $singer_length);
    # }
    return $rate;
}

foreach $song_file (@ARGV) {
    foreach $filename (glob "$music_directory/*.txt") {
        #print "$text_data{$song_file}[0]";
        # pass by reference array \@
        $song_rate = re_log_probability(\@{$text_data{$song_file}}, $filename);
        $filename_ = $filename =~ s/$music_directory\///r;
        $filename_ =~ s/\.txt//;
        $filename_ =~ s/_/ /g;
        #printf "%s: log_probability of %.1f for %s\n", $song_file, $song_rate, $filename_;
        $song_sing{$filename_} = $song_rate;
    }

    # foreach $file (sort { $song_sing{$a} <=> $song_sing{$b}}) keys %song_sing){
    #     printf "%s: log_probability of %.1f for %s\n", $song_file, $song_sing, $file;
    # }
    foreach $file (sort { $song_sing{$a} <=> $song_sing{$b}} keys %song_sing) {
        printf "%s: log_probability of %.1f for %s\n", $song_file, $song_sing{$file}, $file;
    }

    my @sort_singer = sort {$song_sing{$a} <=> $song_sing{$b}} keys %song_sing;
    my $singer = $sort_singer[-1];
    my $final_rate = $song_sing{$singer};
    printf "%s  most resembles the work of %s (log-probability=%.1f)\n", $song_file, $singer, $final_rate;
}