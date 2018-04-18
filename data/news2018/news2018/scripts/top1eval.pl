use warnings;
use strict;

binmode(STDIN,':utf8');
binmode(STDOUT,':utf8');

my $correct = 0;
my $total = 0;
while (<STDIN>) {
  chomp;
  my ($x, $y) = split(/\t+/, lc($_));
  my $result = 0;
  if ($x eq $y) {
    $correct++;
    $result = 1;
  }
  $total++;
  print "$x\t$y\t$result\n";
}
printf("\n$correct / $total = %1.2f\n",100*$correct/$total);
