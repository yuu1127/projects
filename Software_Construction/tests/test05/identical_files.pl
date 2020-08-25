#!/usr/bin/perl

use File::Compare;
@files = @ARGV;
if(@files == 0){
    print "Usage: ./identical_files.pl <files>";
    exit 0;
}

#print "@files[0]";

for ($i = 0; $i < @files; $i++){
    #print "@files";
    #$j = $i + 1;
    for ($j = 0; $j < @files; $j++){
        #print "@files";
        #print "we compare $files[$i] and $files[$j]";
        if (compare($files[$i],$files[$j]) == 0) {
            next;
        }
        else{
            #$file = @files[$i];
            #print "$i ha $j daaaaaaaaaaaa";
            print "@files[$j] is not identical\n";
            exit;
        }
    }
}
print "All files are identical\n";