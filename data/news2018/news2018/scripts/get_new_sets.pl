# Reads a data file, one instance per line, from standard input.
# Takes as command line arguments a hold-out count C, and two file names.
# Takes C lines at random from the input, and puts them in the second file.
# Puts the remaining lines in the first file.
# This was used to create our new-train and tuning sets.

use warnings;
use strict;

srand(1234567890);

binmode(STDIN,':utf8');
binmode(STDOUT,':utf8');

my ($count, $newtrain, $newtune) = @ARGV;

my @lines = ();
my @line_numbers = ();

while (<STDIN>) {
  chomp;
  push @line_numbers, scalar(@lines);
  push @lines, $_;
}

shuffle(\@line_numbers);
if (@line_numbers > $count) {
  @line_numbers = @line_numbers[0 .. $count-1];
}
#print "@line_numbers\n";

my %is_tune = ();
foreach my $l (@line_numbers) {
  $is_tune{$l} = 1;
}

open(NEWTRAIN, '>', $newtrain) || die $!;
binmode(NEWTRAIN,':utf8');
open(NEWTUNE, '>', $newtune) || die $!;
binmode(NEWTUNE, ':utf8');
for (my $i = 0; $i < @lines; $i++) {
  if ($is_tune{$i}) {
    print NEWTUNE "$lines[$i]\n";
  }
  else {
    print NEWTRAIN "$lines[$i]\n";
  }
}
close(NEWTRAIN) || die $!;
close(NEWTUNE) || die $!;



sub shuffle {
  my ($list) = @_;
  for (my $i = 0; $i < @$list; $i++) {
    my $j = int(rand(scalar(@$list)));
    ($list->[$i],$list->[$j]) = ($list->[$j],$list->[$i]);
  }
}
