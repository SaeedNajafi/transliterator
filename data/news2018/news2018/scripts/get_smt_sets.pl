# Reads a data file, one instance per line, from standard input.
# Takes as command line arguments a hold-out count C, and two file names.
# Takes C lines at random from the input, and puts them in the second file.
# Puts the remaining lines in the first file.
# Unlike get_new_sets.pl however, each new file is split into source (src) and target (trg) files.
# Whitespace delimitters are also inserted between each symbol.
# These were used to prepare the inputs for OpenNMT.

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

open(NEWTRAINS, '>', $newtrain.'.src') || die $!;
binmode(NEWTRAINS,':utf8');
open(NEWTUNES, '>', $newtune.'.src') || die $!;
binmode(NEWTUNES, ':utf8');
open(NEWTRAINT, '>', $newtrain.'.trg') || die $!;
binmode(NEWTRAINT,':utf8');
open(NEWTUNET, '>', $newtune.'.trg') || die $!;
binmode(NEWTUNET, ':utf8');
for (my $i = 0; $i < @lines; $i++) {
  my ($s,$t) = split(/\t+/, $lines[$i]);
  if ($is_tune{$i}) {
    print NEWTUNES join(' ', split(//,$s)),"\n";
    print NEWTUNET join(' ', split(//,$t)),"\n";
  }
  else {
    print NEWTRAINS join(' ', split(//,$s)),"\n";
    print NEWTRAINT join(' ', split(//,$t)),"\n";
  }
}
close(NEWTRAINS) || die $!;
close(NEWTUNES) || die $!;
close(NEWTRAINT) || die $!;
close(NEWTUNET) || die $!;



sub shuffle {
  my ($list) = @_;
  for (my $i = 0; $i < @$list; $i++) {
    my $j = int(rand(scalar(@$list)));
    ($list->[$i],$list->[$j]) = ($list->[$j],$list->[$i]);
  }
}
