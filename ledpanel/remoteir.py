#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime,os,time,socket,copy

class remoteir:
    prevfilemtime = {}
    remoteflag = 0
    funcarray = ["anniverse","endtrans","freeword","logo","clock","faceicon","tokoyami","boueigun"]
    speedarray = ["0.5","2","5","10","20","30","60","120"]

    def init(self,ledtoolkitobject):
        baseconfig = ledtoolkitobject.getbaseconfig()
        self.irdir = baseconfig["irdir"]
        self.resourcedir = baseconfig["resourcedir"]
        switchflag = self._getmtime("play")
        switchflag = self._getmtime("plus")
        switchflag = self._getmtime("minus")
        switchflag = self._getmtime("ff")
        switchflag = self._getmtime("rr")
        switchflag = self._getmtime("menu")

    def remoteexec(self,ledtoolkitobject,ledrenderobject):
        config = ledtoolkitobject.getconfig("remote")
        if config["enable"] != "on":
            return
        switchflag = self._getmtime("play")
        if switchflag == 1:
            self.remoteflag = 1
        switchflag = self._getmtime("menu")
        if switchflag == 1:
            self.remoteflag = 1

        if self.remoteflag == 1:
            imagebgdata = ledtoolkitobject.imageload(self.resourcedir + "ledpanellogo.png")
#            imagebgdata = ledtoolkitobject.imagenew()
            ledtoolkitobject.wipe(imagebgdata,"instant")
            menuposition = 0
            scposition = 0
            scpositionmax = 99
            reloadflag = 0
            screloadflag = 0
            while True:
                switchflag = self._getmtime("menu")
                if switchflag == 1:
                    self.init(ledtoolkitobject)
                    self.remoteflag = 0
                    ledtoolkitobject.imageprevcopy(imageoutput)
                    break
                if menuposition == 0:
                    outputmenup = "LEDPANEL CTRL"
                    outputmenus = "+-:SEL MENU:EXIT"
                elif menuposition == 1:
                    ipdata = self._getip()
                    outputmenup = "IP ADDRESS"
                    outputmenus = ipdata
                elif menuposition == 2:
                    outputmenup = "STATIC VIEW"
                    scpositionmax = len(self.funcarray) - 1
                elif menuposition == 3:
                    outputmenup = "CHANGE SPEED"
                    scpositionmax = len(self.speedarray) - 1

                imagebg = copy.copy(imagebgdata)
                imagedata = ledtoolkitobject.imagenew("alpha")
                ledtoolkitobject.fontrender(imagedata,"medium","0","0",outputmenup,"#FFF","shadow")
                ledtoolkitobject.fontrender(imagedata,"medium","1","0",outputmenus,"#FFF","shadow")
                imageoutput = ledtoolkitobject.imagecopy(imagebg,imagedata,"alpha")
                ledtoolkitobject.ledoutput(imageoutput)

                reloadflag = 0
                switchflag = self._getmtime("plus")
                if switchflag == 1:
                    menuposition = menuposition + 1
                    reloadflag = 0
                switchflag = self._getmtime("minus")
                if switchflag == 1:
                    menuposition = menuposition - 1
                    reloadflag = 0
                if menuposition < 0:
                    menuposition = 3
                elif menuposition > 3:
                    menuposition = 0
                if reloadflag == 1:
                    self.init(ledtoolkitobject)
                    scposition = 0
                    continue

                screloadflag = 0
                switchflag = self._getmtime("ff")
                if switchflag == 1:
                    scposition = scposition + 1
                    screloadflag = 1
                switchflag = self._getmtime("rr")
                if switchflag == 1:
                    scposition = scposition - 1
                    screloadflag = 1
                if scposition < 0:
                    scposition = scpositionmax
                if scposition > scpositionmax:
                    scposition = 0

                if menuposition == 2:
                    outputmenus = self.funcarray[scposition]
                    switchflag = self._getmtime("play")
                    if switchflag == 1:
                        ledtoolkitobject.imageprevcopy(imageoutput)
                        while True:
                            endtransflag = ledrenderobject.checker(ledtoolkitobject,"endtrans",1)
                            anniverseflag = ledrenderobject.checker(ledtoolkitobject,"anniverse",1)
                            ledrenderobject.render(ledtoolkitobject,self.funcarray[scposition])
                            switchflag = self._getmtime("play")
                            if switchflag == 1:
                                ledtoolkitobject.wipe(imagebgdata,"instant")
                                break
                            switchflag = self._getmtime("menu")
                            if switchflag == 1:
                                ledtoolkitobject.wipe(imagebgdata,"instant")
                                break
                if menuposition == 3:
                    outputmenus = self.speedarray[scposition]
                    if screloadflag == 1:
                        ledtoolkitobject.putconfig("viewoption","contspeed",self.speedarray[scposition])
                time.sleep(0.1)

    def _getmtime(self,flag):
        filename = self.irdir + "remote_" + flag
        try:
            filemtime = os.stat(filename).st_mtime
        except OSError:
            return 0
        try:
            self.prevfilemtime[flag]
        except KeyError:
            self.prevfilemtime[flag] = filemtime
            return 1
        if filemtime != self.prevfilemtime[flag]:
            self.prevfilemtime[flag] = filemtime
            return 1
        return 0

    def _getip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect( ("8.8.8.8", 80) )
        ipdata =s.getsockname()[0]
        s.close()
        return (ipdata)
