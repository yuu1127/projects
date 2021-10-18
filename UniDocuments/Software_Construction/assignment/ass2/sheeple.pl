#!/usr/bin/perl -w

# z5186797 Yuta Sato

# this is useful syntax hash dictionary for shell -> perl
my %syntax_hash = ("=" => "eq", "eq" => "==", "-eq" => "==", "nq" => "!=", "-nq" => "!=", "-le" => "<=", "-lt" => "<", "-ge" => ">=", "-gt" => ">", "&&" => "and", "||" => "or");
# sub flag to check whether the current line is inside sub or not
$sub_flag = 0;
while ($line = <>){

    # process for only space line
    if($line =~ /^\n$/){
        print $line;
        #print "This is 0!!\n";
        next;
    }

    # process for #!/bin/sh
    # from andrew lecture code
    elsif($line =~ /#!.*/){
        $line =~ s?^#!.*?#!/usr/bin/perl -w?;
        #print "This is 1!!\n";
    }

    # process for only comment # line
    elsif($line =~ /^#.*/){
        print $line;
        #print "This is 2!!\n";
        next;
    }

    # process for echo
    # from andrew lecture code
    elsif($line =~ /echo (.*)/){
        # echo for single quotes
        if ($line =~ /\'.*\'/){
            $line =~ s/\'//g;
            if ($line =~ /\".*\"/){
                $line =~ s/\"/\\"/g;
            }
        }
        # echo for double quotes
        elsif ($line =~ /\".*\"/){
            if ($line =~ /\'.*\'/){
                $line =~ s/\'/\\'/g;
            }
        }
        if($line =~ /echo (".*")/){
            $line =~ s/\"//g;
        }
        $line =~ s?echo (.*)?print "$1\\n";?;
        #print "This is 3!!\n";
        #if this is inside sub print tab to make space (readlibility)
        if($sub_flag == 1){
                print "\t";
        }
    }
    
    # process for variable=
    elsif($line =~ /\S+=.*/){
        @line_array = split(/=/, $line);
        $len = @line_array;
        if($len > 2){
            $value = join(',', $line_array[1..$#line_array]);
        }
        else{
            $value = $line_array[1];
            $value =~ s/\n//;
        }

        # process for expr
        if($value =~ /\`expr .*\`/){
            $value =~ s/\`//g;
            $value =~ s/expr//;
        }
        # if only words need to put ''
        elsif($value !~ /^\d+$/ && $value !~ /^\$.*/){
            $value = "'$value'";
        }

        $variable = $line_array[0];
        $line_array[0] =~ s/ //g;
        $variable =~ s/$line_array[0]/\$$line_array[0]/;

        $line = "$variable" . " " . "=" . " " . "$value;\n";
        #print "This is 4!!\n";
    }

    # process for cd
    elsif($line =~ /cd\s+(.*)/){
        @line_array = split(/ /, $line);
        $plcd = $line_array[0];
        $plcd =~ s/cd/chdir/;
        $value = $line_array[1];
        $value =~ s/\n//;
        $line = "$plcd" . " " . "'$value';\n";
        #print "This is 5!!\n";
    }

    # process for "for loop"
    elsif($line =~ /for\s+(.*)\s+in\s+(.*)/){
        $line =~  s/^\s+//;
        @line_array = split(/ /, $line);
        $value = "";
        foreach my $word (@line_array[3..$#line_array]){
            if($word =~ /\d/){
                $value .= $word
            }

            elsif($word =~ /\*/){
                $value .= "glob(" . "\"$word\"" . ")";
            }

            else{
                $value .= "'$word'";
            }
            $value .= ", ";
        }
        $value = substr($value, 0, -2);
        $value =~ s/\n//;
        $value = "(" . $value . ") {";
        $line = "foreach" . " " . "\$$line_array[1]" . " " . "$value\n";
        #print "This is 6!!\n";
    }

    # process for "for(while) loop's do done"
    elsif($line =~ /do\n?/ || $line =~ /done\n?/){
        $line =~  s/^\s+//;
        if($line eq "do\n"){
            #print "This is 7!!\n";
            next;
        }
        else{
            if($sub_flag == 1){
                print "\t";
            }
            $line = "}\n";
        }
        #print "This is 7!!\n";
    }

    # process for exit
    elsif($line =~ /exit/){
        $line =~ s/\n//;
        $line .= ";\n";

        #print "This is 8!!\n";
    }

    # process for read
    elsif($line =~ /read .+/){
        $line =~ s/ //g;
        $line =~ s/\n//;
        $len = length($line);
        $value = substr($line, 4, $len);
        $line = "    \$$value" . " " . "=" . " " . "<STDIN>;\n";
        $line .= "    chomp \$$value;\n";
        #print "This is 9!!\n";
    }

    # process for if elif 
    elsif($line =~ /if|elif/){
        $line =~  s/^\s+//;
        @line_array = split(/ /, $line);
        $if_elif = $line_array[0];
        if($if_elif eq "elif"){
            $if_elif = "} elsif";
        }
        $v1 = $line_array[2];
        $syntax = $line_array[3];
        $v2 = $line_array[4];

        if ($v1 =~ /-./){
            $syntax =~ s/\n//;
            $line = "$if_elif (" . "$v1" . " " . "'$syntax'" . ") {\n";
        }

        else{
            $v2 =~ s/\n//;
            $p_syntax = $syntax_hash{$syntax};
            $line = "$if_elif (" . "'$v1'" . " " . "$p_syntax" . " " . "'$v2'" . ") {\n";
        }

        #print "This is 10!!\n";
    }

    # process for if elif's then ,else, fi
    elsif($line =~ /then\n/ || $line =~ /else\n/ || $line =~ /fi\n/){
        if($line =~ /then\n/){
            next;
        }
        elsif($line =~ /else\n/){
            $line = "}else {\n";
        }
        else{
            $line = "}\n";
        }
        #print "This is 11!!\n";
    }

    # process for while loop
    elsif($line =~ /while .*/){
        $line =~  s/^\s+//;
        @line_array = split(/ /, $line);
        $while_ = $line_array[0];
        $v1 = $line_array[2];
        $syntax = $line_array[3];
        $v2 = $line_array[4];
        $v2 =~ s/\n//;
        $line = "$while_" . " " . "($v1 $syntax_hash{$syntax} $v2){\n";
        if($sub_flag == 1){
                print "\t";
        }

        #print "This is 12!!\n";
    }

    # process for function -> sub
    elsif($line =~ /.*(){/){
        $line =~ s/\(//;
        $line =~ s/\)//;
        $line = "sub " . "$line";
        $sub_flag = 1;
        #print "This is 13!!\n";
    }

    # process for local -> my
    elsif($line =~ /local /){
        $line =~ s/local/my/;
        $line =~ s/^\s+//;
        @line_array = split(/ /, $line);
        $value = "";
        foreach my $var (@line_array[1..$#line_array]){
            $value .= "\$$var";
            $value .= ", ";
        }
        $value = substr($value, 0, -2);
        $value =~ s/\n//;
        $value = "(" . $value . ");";
        if($sub_flag == 1){
            print "\t";
        }
        $line = "$line_array[0]" . " " . "$value\n";
        #print "This is 14!!\n";
    }

    # process for end of function
    elsif($line =~ /^}\n$/){
        $sub_flag = 0;
        #print "This is 15!!\n";
    }

    # process for test
    elsif($line =~ /test .*/){
        $line =~  s/^\s+//;
        $line =~  s/test//;
        @line_array = split(/ /, $line);
        for my $key (@line_array){
            if (exists $syntax_hash{$key}){
                $line =~ s/$key/$syntax_hash{$key}/;
            }
        }
        if($sub_flag == 1){
                print "\t";
        }

        if($line =~ /return (0|1)/){
            $line=~ s/\n//;
            $line = $line . ";\n";
            #print "This is 1666!!\n";
        }
        
    }

    # process for return 0 and return 1
    elsif($line =~ /return (0|1)/){
        $line=~ s/\n//;
        $line = $line . ";\n";
        #print "This is 1666!!\n";
    }

    # process for systems (such as ls, pwd, mkdir ...)
    else{
        $line =~ s/\n//;
        $line = "system " . "\"$line\"" . "\;\n";
        #print "This is 13!!\n";
    }

    # ARGV process
    if($line =~ /\$(\d+)/){
        $value = $1 - 1;
        if($sub_flag == 0){
            $line =~ s/\$$1/\$ARGV[$value]/;
        }
        else{
            $line =~ s/\$$1/\$_[$value]/;
        }
    }

    # $@ process
    if($line =~ /\$\@/){
        if($line =~ /"\$\@"/){
            $line =~ s/"\$\@"/\@ARGV/;
        }
        else{
            $line =~ s/\$\@/\@ARGV/;
        }
    }

    # process for comment out ## but with other implemention 
    # some syntax + comment in same line
    if($line =~ /^.+# *\S+/){
        @line_array = split(/#/, $line);
        $line_array[1] =~ s/;//;
        $line = $line_array[0] . "; #" . $line_array[1];
    }

    # process for $() and $(())
    if($line =~ /\$\(.+\)/){
        if($line =~ /\$\(\(.+\)\)/){
            $line =~ s/\(//;
            $line =~ s/\)//;
        }
        ($cal) = $line =~ m/\$\(.+\)/g;
        $cal =~ s/\$\(//;
        $cal =~ s/\)//;
        @cal_array = split(/ /, $cal);
        $new_cal = "";
        foreach my $var (@cal_array){
            if($var =~ /\w+/ && $var !~ /[0-9]+/){
                $var = "\$" . $var;
            }
            $new_cal .= $var . " ";
        }
        $new_cal = substr($new_cal, 0, -1);
        $line =~ s/\$\(.+\)/$new_cal/;
    }

    # process for && and || except calculaion
    if($line =~ /(\&\&|\|\|)/){
        $line =~ s/\&\&/or/;
        $line =~ s/\|\|/and/;
    }

    # if test syntax left ,remove it
    if($line =~ /test/){
        $line =~ s/test//;
    }

    print $line;
}