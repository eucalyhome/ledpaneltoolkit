#!/usr/bin/perl

use Imager;
use Image::Seek qw(loaddb add_image query_id savedb);
use Storable qw/nfreeze thaw/;

$imagelist = "/data/web/facedb/facedata.txt";
open (FILE,$imagelist);
(@listarray) = (<FILE>);
close (FILE);

my $imgdb    = '/data/web/facedb/imgseek.db';

loaddb($imgdb);

$randbaseimageseed = int(rand($#listarray));
$randbaseimageid = $listarray[$randbaseimageseed];
print "baseid:$randbaseimageseed-$randbaseimageid\n\n";

@results = query_id($randbaseimageid, 100); 
foreach(@results){
   foreach (@$_){
      if ($gid == ""){
       $gid = $_;
       next;
      }
      $gvec = $_;
   }
   print "$gid\t$gvec\n";
   $gid = "";
   $gvec = "";
}

exit;
