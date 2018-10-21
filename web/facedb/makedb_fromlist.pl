use Imager;
use Image::Seek qw(loaddb add_image query_id savedb);
use Storable qw/nfreeze thaw/;

$listfile = "./facedata.txt";
my $id       = 1;
my $imgdb    = 'imgseek.db';

loaddb($imgdb);

open (FILE,$listfile);
(@listarray) = (<FILE>);
close (FILE);

foreach $listline (@listarray){
 ($gid,$pname) = split(/\t/,$listline);
 if ($gid eq ""){next;}
 if ($gid =~ /\D/){next;}
 $inputimage = "/data/web/root/imagerawdir/".$gid.".png";
 my $img = Imager->new();
 $img->open( file => $inputimage );
 add_image( $img, $gid );
 print "$id\t$inputimage\n";
 $id++;
}
savedb($imgdb);

