#!/bin/sh

mkdir -f /data
mkdir -f /data/ledpanel
mkdir -f /data/web
mkdir -f /data/web/cgi
mkdir -f /data/web/facedb
mkdir -f /data/web/root
mkdir -f /data/web/root/imagerawdir
mkdir -f /data/web/root/uploaddata
mkdir -f /data/ledpanel/fonts
mkdir -f /data/ledpanel/resource
cp -frn ../ledpanel/ /data/
cp -frn ../web/ /data/
