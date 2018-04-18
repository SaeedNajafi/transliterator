use warnings;
use strict;

binmode(STDIN,':utf8');
binmode(STDOUT,':utf8');

while (<STDIN>) {
  chomp;
  my ($i, $o) = split(/\t+/);
  $i = lc($i);
  print join(' ', split(//,$i)), "\t", join(' ', split(//,$o)), "\n";
}
