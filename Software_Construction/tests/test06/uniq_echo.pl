#!/usr/bin/perl -w

@words = @ARGV;

#print "@words";

# foreach $element (@words){
#     if(!$seen{$element}){
#         push(@u_words, $element);
#         $seen{$element}++;
#     }
# }

# foreach $element (@words){
#     if(!$seen{$element}){
#         push(@u_words, $element);
#         $seen{$element}++;
#     }
# }

foreach $element (@words){
    if(!$seen{$element}){
        push(@u_words, $element);
        $seen{element}++;
    }
}

print "@u_words\n";