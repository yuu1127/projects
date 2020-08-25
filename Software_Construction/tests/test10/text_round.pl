#!/usr/bin/perl -w

# use Math::Round;

# @lines = <STDIN>;

# foreach my $line (@lines){
#     #print "$word\n";
#     @line_ = split(/ /, $line);
#     foreach my $word (@line_){
#         if($word =~ /[0-9]+\.?[0-9]*/){
#             $word =~ s/\D//g;
#             printf "%.0f", $word;
#         }
#         else{
#             print "$word ";
#         }
#     }
# }
# print round(15.5);

# caz this round absolutely \d+\.\d+

# while ($line = <>) {
#     my @numbers = $line =~ /(\d+\.\d+)/g;
#     foreach $number (@numbers) {
#         my $rounded_number = int($number + 0.5);
#         $line =~ s/$number/$rounded_number/;
#     }
#     print $line;
# }

# while ($line = <>){
#     my @numbers = $line =~ /(\d+\.\d+)/g;
#     foreach $number (@numbers){
#         my $rounded_number = int($number + 0.5);
#         $line =~ s/$number/$rounded_number/;
#     }
#     print $line;
# }

while($line = <>){
    #my @numbers = $line =~ /(\d+\.\d+)/g;
    my @numbers = $line =~ /(\d+\.\d+)/g;
    foreach $number (@numbers){
        #my $rounded_number = int($number + 0.5);
        my $rounded_number = int($number + 0.5);
        $line =~ s/$number/$rounded_number/;
    }
    print $line;
}