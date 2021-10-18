#!/usr/bin/perl -w

use LWP::Simple;

$prefix=$ARGV[0];
$base_url="http://www.timetable.unsw.edu.au/current/".$prefix."KENS.html";
$web_page = get($base_url) or die "Unable to get $base_url";
my %s_courses = ();
foreach my $course ($web_page =~ /($prefix[0-9][0-9][0-9][0-9].*)/g){
    #$tag =~ /<\/?(\w+)/;
    #$course =~ s/.*\($prefix[0-9][0-9][0-9][0-9]\)\.html[^>]*> *\([^<]*\).*/$1 $2/;
    $course =~ s/.html">/ /;
    $course =~ s/<\/.><\/.*>//;
    #print "$course\n";
    @courses = split(/ /,$course, 2);
    #print "@courses\n";
    #@courses.push($course);
    if($courses[1] !~ /(\w{4})(\d{4})/){
        #print "@courses\n";
        $s_courses{$courses[0]} = $courses[1];
    }
}

foreach $key (sort(keys %s_courses)){
    print "$key $s_courses{$key}\n"
}