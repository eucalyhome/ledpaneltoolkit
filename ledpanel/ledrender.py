#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ledtoolkit, faceicon, logo, freeword, anniverse, endtrans, dqxcalender, time, os, datetime, random, ledclock, bgimage, remoteir

class ledrender:

    def init(self,ledtoolkitobject):
        self.facedata = faceicon.faceicon()
        self.logodata = logo.logo()
        self.bgimagedata = bgimage.bgimage()
        self.freeworddata = freeword.freeword()
        self.anniversedata = anniverse.anniverse()
        self.endtransdata = endtrans.endtrans()
        self.dqxcal = dqxcalender.dqxcalender()
        self.clock = ledclock.ledclock()

        self.facedata.init(ledtoolkitobject)


    def render(self,ledtoolkitobject,target):
        if target == "tokoyami":
            (imagedata) = self.dqxcal.tokoyamirender(ledtoolkitobject)
            ledtoolkitobject.wipe(imagedata)
        elif target == "boueigun":
            (imagedata) = self.dqxcal.boueigunrender(ledtoolkitobject)
            ledtoolkitobject.wipe(imagedata)
        elif target == "faceicon":
            (imagedata) = self.facedata.render(ledtoolkitobject)
            (background) = self.bgimagedata.render(ledtoolkitobject)
            ledtoolkitobject.bgmorf(imagedata,background)
        elif target == "freeword":
            self.freeworddata.render(ledtoolkitobject)
        elif target == "logo":
            (imagedata,bgmorfoption) = self.logodata.render(ledtoolkitobject)
            (background) = self.bgimagedata.render(ledtoolkitobject)
            ledtoolkitobject.bgmorf(imagedata,background,bgmorfoption)
        elif target == "clock":
            (imagedata,bgmorfoption) = self.clock.render(ledtoolkitobject)
            (background) = self.bgimagedata.render(ledtoolkitobject)
            ledtoolkitobject.bgmorf(imagedata,background,bgmorfoption)
        elif target == "endtrans":
            (imagedata) = self.endtransdata.render(ledtoolkitobject)
            ledtoolkitobject.wipe(imagedata)
        elif target == "anniverse":
            (imagedata,bgmorfoption) = self.anniversedata.render(ledtoolkitobject)
            (background) = self.bgimagedata.render(ledtoolkitobject)
            ledtoolkitobject.bgmorf(imagedata,background,bgmorfoption)
        else:
            self.execerror(ledtoolkitobject)

    def rendererror(self,ledtoolkitobject):
        imagedata = ledtoolkitobject.imagenew()
        ledtoolkitobject.fontrender(imagedata,"medium","0","0",u'表示エラー',"#F00","")
        ledtoolkitobject.wipe(imagedata)

    def checker(self,ledtoolkitobject,target,forceview=0):
        if target == "endtrans":
            endtransflag = self.endtransdata.checker(ledtoolkitobject,forceview)
            return (endtransflag)
        elif target == "anniverse":
            anniverseflag = self.anniversedata.checker(ledtoolkitobject,forceview)
            return (anniverseflag)
