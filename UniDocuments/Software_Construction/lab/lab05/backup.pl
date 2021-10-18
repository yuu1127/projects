#!/usr/bin/perl -w

die "Usage: cp <source> <destination>\n" if @ARGV != 1;
$filename = $ARGV[0];
#print "$filename\n";
@file_array = split(/\./, $filename);
#print "$file_array[0]";
# foreach $i (@file_array){
#     print "$i\n";
# }
$lastchar = $file_array[-1];
#print "$lastchar\n";
unless ($lastchar =~ /^[0-9]+$/){
    $filename_ = $filename;
    $lastchar = "0";
    $new_filename = ".$filename" . "." . $lastchar;
 }
else{
    $filename_ = join('', @file_array[0..$#file_array-1]);
    $lastchar = $lastchar + 1;
    $new_filename = ".$filename_" . "." . $lastchar;
 }

while(-e $new_filename){
    $lastchar = $lastchar + 1;
    $new_filename = ".$filename_" . "." . $lastchar;
}
system('cp', $filename, $new_filename);
print "Backup of '$filename' saved as '$new_filename'\n";