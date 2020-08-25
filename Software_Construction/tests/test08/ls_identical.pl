#!/usr/bin/perl

use File::Basename;
use File::Compare;

$f_directory=@ARGV[0];
$s_directory=@ARGV[1];

#print "$f_directory";
foreach $f_file (glob "$f_directory/*") {
    $filename = basename("$f_file");
    if(-e "$s_directory/$filename"){
        if(compare("$f_file", "$s_directory/$filename") == 0){
            print "$filename\n";
        }
    }
}