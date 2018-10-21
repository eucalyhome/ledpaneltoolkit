#!/bin/sh

mkdir /data
mkdir /data/ledpanel
mkdir /data/web
mkdir /data/web/cgi
mkdir /data/web/facedb
mkdir /data/web/root
mkdir /data/web/root/imagerawdir
mkdir /data/web/root/uploaddata
mkdir /data/ledpanel/fonts
mkdir /data/ledpanel/resource
cp -rn ../ledpanel/ /data/
cp -rn ../web/ /data/