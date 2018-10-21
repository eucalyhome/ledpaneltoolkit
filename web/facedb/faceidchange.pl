$listfile = "/data/web/facedb/facedata_original.txt";
$listoutputfile = "/data/web/facedb/facedata.txt";
my $id       = 1;

open (FILE,$listfile);
(@listarray) = (<FILE>);
close (FILE);
open (OUTFILE,">$listoutputfile");

$gpid = 1;
foreach $listline (@listarray){
 ($gid,$pname) = split(/\t/,$listline);
 $pline =~ s/\n//g;
 $pline =~ s/\r//g;

 if ($gid eq ""){next;}
 if ($gid =~ /\D/){next;}
 $inputimage = "/data/web/root/imagerawdir_original/".$gid.".png";
 if (!-e $inputimage){next;}
 print "$gpid\t$inputimage\n";
 print OUTFILE "$gpid\t$pname\t\n";
 $systemcommand = "cp $inputimage /data/web/root/imagerawdir/$gpid.png";
 system($systemcommand);
 $gpid++;
}
close (OUTFILE);


