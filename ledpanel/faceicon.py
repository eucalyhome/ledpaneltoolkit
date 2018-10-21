#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random, codecs

class faceicon:

    def init(self,imageexec):
        baseconfig = imageexec.getbaseconfig()
        self.icondir = baseconfig["icondir"]
        self.pukulistfile = baseconfig["pukulistfile"]
        self.dwalistfile = baseconfig["dwalistfile"]

        myfile = codecs.open(self.pukulistfile,"r", encoding='UTF-8')
        self.pukulistarray = myfile.readlines()
        myfile.close()
        myfile = codecs.open(self.dwalistfile,"r", encoding='UTF-8')
        self.dwalistarray = myfile.readlines()
        myfile.close()
        self.iconuse = {}

    def render(self,ledtoolkitobject):
        config = ledtoolkitobject.getconfig("faceicon")
        primarylist = []
        if config["listenable"] == "on":
            primarylist.append("l")
        if config["pukuenable"] == "on":
            primarylist.append("p")
        if config["dwaenable"] == "on":
            primarylist.append("d")
        if len(primarylist) == 0:
            imagedata = ledtoolkitobject.imagenew()
            ledtoolkitobject.fontrender(imagedata,"medium","0","0",u'フェイスエラー',"#F00","shadow")
            imagebgdata = ledtoolkitobject.imagenew()
            return (imagedata,imagebgdata)
        rand = random.randrange(len(primarylist))
        if primarylist[rand] == "p":
            listarray = self.pukulistarray
        if primarylist[rand] == "d":
            listarray = self.dwalistarray
        if primarylist[rand] == "l":
            listarray = []
            for listnumber in range(1,49):
                listenablekey = "list" + str(listnumber) + "enable"
                listnamekey = "list" + str(listnumber) + "name"
                listiconkey = "list" + str(listnumber) + "icon"
                if config[listenablekey] == "":
                    continue
                if config[listiconkey] == "":
                    config[listiconkey] = 14235
                listarray.append("////////" + config[listiconkey] + ".png\t" + config[listnamekey])
            if len(primarylist) == 0:
                listarray.append("////////14235.png\tゆうかり")
        listresetflag = 0
        for listnumber in range(50):
            rand = random.randrange(len(listarray))
            try:
                self.iconuse[rand]
            except KeyError:
                self.iconuse[rand] = 1
                listresetflag = 1
                break
            if self.iconuse[rand] != 1:
                listresetflag = 1
                break
        if listresetflag == 0:
            self.iconuse = {}
        (imagedata) = self._renderexec(listarray[rand],ledtoolkitobject)
        return (imagedata)

    def _renderexec(self,icondata,imageexec):
        target = icondata.split()
        targetimage = target[0].split("/")
        targetimage = targetimage[8]
        imagedata = imageexec.imagenew("alpha")
        imagepath = self.icondir + targetimage
        imageicon = imageexec.imagefitload(imagepath,"vc")
        imagedata = imageexec.imagecopy(imagedata,imageicon,"southwestalpha")
        imagename = target[1]
        imagenamespace = 6 - len(imagename)
        for i in range(imagenamespace):
            imagename = u'　' + imagename
        imageexec.fontrender(imagedata,"medium","1","0",imagename,"#FFF","shadow")
        return (imagedata)
