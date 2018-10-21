#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

class logo:

    def render(self,ledtoolkitobject):
        baseconfig = ledtoolkitobject.getbaseconfig()
        self.uploaddir = baseconfig["uploaddir"]

        config = ledtoolkitobject.getconfig("logo")
        bgmorfoption = ""
        if config["bgmorf"] != "on":
            bgmorfoption = "morfdisable"
        elif config["bgmorftype"] == "random":
            rand = random.randrange(7)
            if rand == 1:
                bgmorfoption = "diff"
            elif rand == 2:
                bgmorfoption = "add"
            elif rand == 3:
                bgmorfoption = "subtract"
            elif rand == 4:
                bgmorfoption = "multiply"
            elif rand == 5:
                bgmorfoption = "screen"
            elif rand == 6:
                bgmorfoption = "lighter"
            else:
                bgmorfoption = "darker"
        else:
            bgmorfoption = config["bgmorftype"]
        listarray = []
        for listnumber in range(1,9):
            listenablekey = str(listnumber) + "enable"
            listfilenamekey = str(listnumber) + "filename"
            if config[listenablekey] == "":
                continue
            if config[listfilenamekey] == "":
                continue
            listarray.append(config[listfilenamekey])
        if len(listarray) == 0:
            imagedata = ledtoolkitobject.imagenew()
            ledtoolkitobject.fontrender(imagedata,"medium","0","0",u'ロゴエラー',"#F00","shadow")
            imagebgdata = ledtoolkitobject.imagenew()
            return (imagedata,imagebgdata)
        rand = random.randrange(len(listarray))
        imagelogofile = self.uploaddir + str(listarray[rand])
        imagelogo = ledtoolkitobject.imageload(imagelogofile)
        return (imagelogo,bgmorfoption)
