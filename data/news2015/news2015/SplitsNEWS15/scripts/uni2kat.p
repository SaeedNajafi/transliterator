#!/usr/bin/perl -w

# for converting Katakana Unicode into readable ascii and back
# usage: cat dev.uni | <this>.p -v2 -f > dev2.kat
#        cat dev2.kat | <this>.p -v2
# written: Mar/Apr 2009

use strict;
use utf8;
use Encode;
use Getopt::Std;

my %opts;
getopts('flv:s:', \%opts);

my $forward = 0;			# from unicode to chars
$forward = 1 if $opts{f};		# from chars to unicode

my $letter = 0;				# from letters to chars
$letter = 1 if $opts{l};		# from chars to unicode

my $version = 3;		
$version = $opts{v} if $opts{v};        # preprocessing version

my $sep = "";
$sep = $opts{s} if $opts{s};		# output separator
my @R;

my $error_code = chr(0x0021);	
my $long = "#";			# prolonged sound mark
my $sokuon = "tu";

my $merge_long;			# merge the long mark with the previous symbol
my $merge_sokuon;		# merge the sokuon with the next symbol

if ($version eq "3") {
  $merge_long = 0;		# minimal preprocessing
  $merge_sokuon = 0;
} elsif ($version eq "2") {
  $merge_long = 1;		# more preprocessing
  $merge_sokuon = 0;
} elsif ($version eq "1") {
  $merge_long = 1;		# most preprocessing
  $merge_sokuon = 1;
} else {
  die "unknown version\n";
}

mapR();

#main loop
while (<>) {
  if ($forward) {				# forward conversion
      chomp;
      my $kat = decode('UTF-8', $_);
      printf "%s\n", uni2kat($kat);
  } elsif ($letter) {				# reconstruct kat from letters
      chomp;
      ## next unless $_;
      unless ($_)
      {
        print "\n";
        next;
      }
      s/[_|.]//g;
      my $kat = let2kat($_);
      my $uni = kat2uni($kat);
#      print $_, "\t", $kat; print "\t", "!!!" if $uni eq $error_code;
      printf "%s", encode('UTF-8', $uni);
      print "\n";
  } else {					# back conversion
      chomp;
      my $uni = kat2uni($_);
      printf "%s\n", encode('UTF-8', $uni);
  }
}

#-------------------------------------------------------------------------
sub let2kat {
  my @out = ();
  foreach (split //, $_[0]) {
    if ($_ =~ /[aeiouAEIOU#N]/) {
      push @out, $_;
      push @out, ".";
    } else {
      push @out, $_;
    }
  }

  pop @out if $out[-1] eq ".";
  my $sout = join "", @out;
#  return join "", @out;
  $sout =~ s/N\.([AEIOU])/N$1/g;
  return $sout;
}

#-------------------------------------------------------------------------
sub kat2uni {
  my @out = ();
  foreach (split /\./, $_[0]) {
    if (/^$long./) {
      $_ =~ s/^$long//;
      push @out, chr(0x30C3);
    }
    if (/.$long$/) {
      $_ =~ s/$long$//;
      my $c = find_code($_);
      return $error_code unless $c;
      push @out, chr($c);
      push @out, chr(0x30FC);
    } else {
      my $c = find_code($_);
      return $error_code unless $c;
      push @out, chr($c);
    }
  }
  return join "", @out;
}

sub find_code {
  my $let = $_[0];
  for (my $i = 0x30A1; $i <= 0x30FA; $i++) {
    return $i if $R[$i] eq $let;
  }
  return 0x30FC if $R[0x30FC] eq $let;
#  die "unknown letter: $let\n";
  return "";
}

#-------------------------------------------------------------------------
sub uni2kat {
  my @out = ();
  my $s_flag = 0;
  foreach (split //, $_[0]) {
    my $code = ord($_);
    die "unknown code: $code line $. \n" unless defined $R[$code];
    if (($R[$code] eq $long) && $merge_long) {
      my $last = pop @out;
      die unless $last;
      $last .= $long;
      push @out, $last;
    } elsif (($R[$code] eq $sokuon) && $merge_sokuon) {
      $s_flag = 1;
    } elsif ($s_flag) {
      push @out, $long . $R[$code];
      $s_flag = 0;
    } else {
      push @out, $R[$code];
    }
  }
  die if $s_flag;
  return join $sep, @out;
}

#-------------------------------------------------------------------------
# http://www.alanwood.net/unicode/katakana.html
sub mapR {
  $R[0x21] = "!";
  $R[0x2F] = "/";
#  $R[0x30A0] = "?"; 		# DOUBLE HYPHEN
  $R[0x30A1] = "a";
  $R[0x30A2] = "A";
  $R[0x30A3] = "i";
  $R[0x30A4] = "I";
  $R[0x30A5] = "u";
  $R[0x30A6] = "U";
  $R[0x30A7] = "e";
  $R[0x30A8] = "E";
  $R[0x30A9] = "o";
  $R[0x30AA] = "O";

  $R[0x30AB] = "KA";
  $R[0x30AC] = "GA";
  $R[0x30AD] = "KI";
  $R[0x30AE] = "GI";
  $R[0x30AF] = "KU";
  $R[0x30B0] = "GU";
  $R[0x30B1] = "KE";
  $R[0x30B2] = "GE";
  $R[0x30B3] = "KO";
  $R[0x30B4] = "GO";
  $R[0x30B5] = "SA";
  $R[0x30B6] = "ZA";
  $R[0x30B7] = "SI";
  $R[0x30B8] = "ZI";
  $R[0x30B9] = "SU";
  $R[0x30BA] = "ZU";
  $R[0x30BB] = "SE";
  $R[0x30BC] = "ZE";
  $R[0x30BD] = "SO";
  $R[0x30BE] = "ZO";
  $R[0x30BF] = "TA";
  $R[0x30C0] = "DA";
  $R[0x30C1] = "TI";
  $R[0x30C2] = "DI";
  $R[0x30C3] = $sokuon;
  $R[0x30C4] = "TU";
  $R[0x30C5] = "DU";
  $R[0x30C6] = "TE";
  $R[0x30C7] = "DE";
  $R[0x30C8] = "TO";
  $R[0x30C9] = "DO";
  $R[0x30CA] = "NA";
  $R[0x30CB] = "NI";
  $R[0x30CC] = "NU";
  $R[0x30CD] = "NE";
  $R[0x30CE] = "NO";
  $R[0x30CF] = "HA";
  $R[0x30D0] = "BA";
  $R[0x30D1] = "PA";
  $R[0x30D2] = "HI";
  $R[0x30D3] = "BI";
  $R[0x30D4] = "PI";
  $R[0x30D5] = "HU";
  $R[0x30D6] = "BU";
  $R[0x30D7] = "PU";
  $R[0x30D8] = "HE";
  $R[0x30D9] = "BE";
  $R[0x30DA] = "PE";
  $R[0x30DB] = "HO";
  $R[0x30DC] = "BO";
  $R[0x30DD] = "PO";
  $R[0x30DE] = "MA";
  $R[0x30DF] = "MI";
  $R[0x30E0] = "MU";
  $R[0x30E1] = "ME";
  $R[0x30E2] = "MO";
  $R[0x30E3] = "ya";
  $R[0x30E4] = "YA";
  $R[0x30E5] = "yu";
  $R[0x30E6] = "YU";
  $R[0x30E7] = "yo";
  $R[0x30E8] = "YO";
  $R[0x30E9] = "RA";
  $R[0x30EA] = "RI";
  $R[0x30EB] = "RU";
  $R[0x30EC] = "RE";
  $R[0x30ED] = "RO";
  $R[0x30EE] = "wa";
  $R[0x30EF] = "WA";
  $R[0x30F0] = "WI";
  $R[0x30F1] = "WE";
  $R[0x30F2] = "WO";
  $R[0x30F3] = "N";
  $R[0x30F4] = "VU";
  $R[0x30F5] = "ka";
  $R[0x30F6] = "ke";
  $R[0x30F7] = "VA";
  $R[0x30F8] = "VI";
  $R[0x30F9] = "VE";
  $R[0x30FA] = "VO";

#  $R[0x30FB] = "?"; 		# MIDDLE DOT
  $R[0x30FC] = $long; 		# PROLONGED SOUND MARK
#  $R[0x30FD] = "?"; 		# ITERATION MARK
#  $R[0x30FE] = "?"; 		# VOICED ITERATION MARK
#  $R[0x30FF] = "?"; 		# DIGRAPH KOTO
}

