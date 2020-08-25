#!/usr/bin/perl -w

#@words = @ARGV;

# $num = $words[0] =~ s/\D//gr;
# $word = $words[0] =~ s/^\d//gr;

# $new_word = $word;
# foreach $w (@words[1..@words - 1]){
#     $new_word .= " ";
#     $new_word .= $w;
# }

$num = $ARGV[0];
#$cnt = 0;
while($line=<STDIN>){
    chomp $line;
    # if (!$dic{$line}){
    #     $dic{$line} = 0;
    # }
    $dic{$line}++;
    if ($dic{$line} == $num){
        print("Snap: $line\n");
        last;
    }
}
