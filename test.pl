
# This is the tester for paresr.py(in python3)
# So we record the test method in a more convenient way.
# wget put the content into local disk file
# curl display the result on screen

use 5.012;
use warnings;
use strict;
my $ip = "192.168.23.10";
my $python = 'python3';
$python = 'python' if $^O eq 'msys';
my $line = "curl $ip:13000/static/hash | $python ./parser3.py";
system($line);
