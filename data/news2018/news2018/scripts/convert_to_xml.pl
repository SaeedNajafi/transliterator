use warnings;
use strict;

my $input_file = shift(@ARGV) || die "NO FILE.\n";

my $dtl_file = $input_file.'.dtl';

my $xml_file = $input_file;
$xml_file =~ s/\.out$//g;
$xml_file .= '.xml';

# convert the file to an intermediate "DTL-like" format
my $command1 = "cat $input_file | perl scripts/convert_to_dtl.pl > $dtl_file";
#print "RUNNING:\t$command1\n";
system "$command1";

# produce the XML file
my $command2 = "python2 scripts/XMLize.py $dtl_file $xml_file";
#print "RUNNING:\t$command2\n";
system "$command2\n";

