
# This is the tester for paresr.py(in python3)
# So we record the test method in a more convenient way.
# wget put the content into local disk file
# curl display the result on screen

use 5.012;
use warnings;
use strict;

my $line = "curl 192.168.0.107:13000/static | python3 ./parser.py";
system($line);
