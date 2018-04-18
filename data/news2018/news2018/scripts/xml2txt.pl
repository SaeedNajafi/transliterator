# Reads an xml file from standard input, prints a cleaner, one-instance-per-line format.

use warnings;
use strict;

binmode(STDIN,':utf8');
binmode(STDOUT,':utf8');

my $current_source = '';
my $current_target = '';

while (<STDIN>) {
  chomp;
  my $line = $_;

  if ($line =~ /\<SourceName\>(.+)\<\/SourceName\>/) {
    $current_source = $1;
  }
  elsif ($line =~ /\<TargetName ID="1"\>(.+)\<\/TargetName\>/) {
    $current_target = $1;
    if ($current_source) {
      print "$current_source\t$current_target\n";
    }
  }
}
