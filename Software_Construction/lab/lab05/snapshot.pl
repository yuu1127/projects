#!/usr/bin/perl -w

#die "Usage: cp <source> <destination>\n" if @ARGV != 1 or @ARGV != 2;
$directory_name="snapshot";
$number=0;
$new_directory="${directory_name}.${number}";
use File::Basename;
#print "$new_directory\n"
sub save_files{
    while(-e ".$new_directory"){
        $number++;
        $new_directory="${directory_name}.${number}";
    }
    #print "$new_directory\n";
    mkdir ".$new_directory";
    print "Creating $directory_name $number\n";
    #print "this file is $0\n";
    @files = <*>;
    foreach $file (@files){
        if($file ne $0){
            #print "$file\n";
            system('cp', $file, "./.$new_directory");
        }
    }
}


if($ARGV[0] eq "save"){
    save_files;
}
elsif($ARGV[0] eq "load"){
    save_files;
    $file_number = $ARGV[1];
    #$base_directory = dirname($0);
    $base_directory = "./";
    $r_directory = ".snapshot.$file_number";
    @files = glob("$r_directory/*");
    foreach $file (@files){
        #print "recover $file to $base_directory\n";
        system('cp', $file, $base_directory);
    }
    print "Restoring snapshot $file_number\n"
}
# else{
#     die "Usage: $0 save or load \n"
# }