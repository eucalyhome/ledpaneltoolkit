#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random, datetime

class anniverse:
    anniversefilenamearray = []

    def render(self,ledtoolkitobject):
        baseconfig = ledtoolkitobject.getbaseconfig()
        self.uploaddir = baseconfig["uploaddir"]
        config = ledtoolkitobject.getconfig("anniverse")
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
        rand = random.randrange(len(self.anniversefilenamearray))
        imagelogofile = self.uploaddir + str(self.anniversefilenamearray[rand])
        imagelogo = ledtoolkitobject.imageload(imagelogofile)
        return (imagelogo,bgmorfoption)


    def checker(self,ledtoolkitobject,forceview=0):
        config = ledtoolkitobject.getconfig("anniverse")
        imagedata = ledtoolkitobject.imagenew()

        now = datetime.datetime.now()
        nowday = int(now.strftime('%d'))
        nowweek = int(now.weekday())
        self.anniversefilenamearray = []
        for listnumber in range(1,9):
            listenablekey = str(listnumber) + "enable"
            listfilenamekey = str(listnumber) + "filename"
            listdaykey = str(listnumber) + "day"
            listweekkey = str(listnumber) + "week"
            if config[listenablekey] == "":
                continue
            if config[listfilenamekey] == "":
                continue
            apflag = 0
            if config[listdaykey] != "":
                if int(config[listdaykey]) == int(nowday):
                    apflag = 1
            if config[listweekkey] != "":
                if int(config[listweekkey]) == nowweek:
                    apflag = 1
            if forceview == 1:
                apflag = 1
            if apflag == 1:
                self.anniversefilenamearray.append(config[listfilenamekey])
        if len(self.anniversefilenamearray) == 0:
            return "0"
        return "1"
