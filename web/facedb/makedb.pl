use Imager;
use Image::Seek qw(loaddb add_image query_id savedb);
use Storable qw/nfreeze thaw/;

my $id       = 1;
my $imgdb    = 'imgseektmp.db';

loaddb($imgdb);

opendir (DIR,"/data/web/root/imagerawdir/");
(@dirarray) = readdir(DIR);
closedir (DIR);

foreach $dirline (@dirarray){
 if ($dirline !~ /png/){next;}
 $gid = $dirline;
 $gid =~ s/\D//g;
 $inputimage = "/data/web/root/imagerawdir/".$gid.".png";
 my $img = Imager->new();
 $img->open( file => $inputimage );
 add_image( $img, $gid );
 print "$id\t$inputimage\n";
 $id++;
}
savedb($imgdb);

