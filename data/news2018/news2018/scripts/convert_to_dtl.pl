# Takes simple tab-separated input/output data from standard input, and prints it
# in a DTL-like four-field format, for use with XMLize.py
# Note that this scripts assumes that only the top 1 output is provided, with no
# n-best list.

use warnings;
use strict;

binmode(STDIN,':utf8');
binmode(STDOUT,':utf8');

while (<STDIN>) {
  chomp;
  s/ //g;
  print "$_\t1\t1\n";
}
