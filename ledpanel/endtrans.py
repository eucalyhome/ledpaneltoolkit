#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random, datetime

class endtrans:
    processpage = 0
    endtranstitlearray = []
    endtranstimearray = []

    def render(self,ledtoolkitobject):
        config = ledtoolkitobject.getconfig("endtrans")
        imagedata = ledtoolkitobject.imagenew()
        datalength = len(self.endtranstitlearray)
        if datalength == 0:
            ledtoolkitobject.fontrender(imagedata,"medium","0","0",u'終電エラー',"#F00","")
            return (imagedata)
        if (datalength % 2) == 1:
            self.endtranstitlearray.append(" ")
            self.endtranstimearray.append(" ")
        if self.processpage >= datalength:
            self.processpage = 0
        viewpage1 = self.processpage
        viewpage2 = self.processpage + 1
        self.processpage = self.processpage + 2
        viewtitle1 = self.endtranstitlearray[viewpage1]
        viewtime1 = self.endtranstimearray[viewpage1]
        if viewpage2 > datalength:
            viewtitle2 = " "
            viewtime2 = " "
        else:
            viewtitle2 = self.endtranstitlearray[viewpage2]
            viewtime2 = self.endtranstimearray[viewpage2]
        ledtoolkitobject.fontrender(imagedata,"large","0","0",u'終電情報',"#400","shadow")
        ledtoolkitobject.fontrender(imagedata,"medium","0","5",viewtitle1,"#FFF","shadowright")
        ledtoolkitobject.fontrender(imagedata,"medium","1","5",viewtitle2,"#FFF","shadowright")
        ledtoolkitobject.fontrender(imagedata,"medium","0","5.5",viewtime1,"#FFF","shadow")
        ledtoolkitobject.fontrender(imagedata,"medium","1","5.5",viewtime2,"#FFF","shadow")
        imagebgdata = ledtoolkitobject.imagenew()
        return (imagedata)

    def checker(self,ledtoolkitobject,forceview=0):
        config = ledtoolkitobject.getconfig("endtrans")
        imagedata = ledtoolkitobject.imagenew()

        now = datetime.datetime.now()
        nowhour = int(now.strftime('%H'))
        if nowhour < 5:
            nowhour = nowhour + 24
        nowmin = nowhour * 60 + int(now.strftime('%M'))
        starthour = int(config["starttime"].split(':')[0])
        if starthour < 5:
            starthour = starthour + 24
        startmin = starthour * 60 + int(config["starttime"].split(':')[1])
        if nowmin < startmin:
            if forceview != 1:
                return "0"
        datetype = "h"
        if now.weekday() == 5:
            if now.hour > 5:
                datetype = "d"
        elif now.weekday() == 6:
            datetype = "d"
            if now.hour > 5:
                datetype = "k"
        elif now.weekday() == 0:
            if now.hour < 5:
                datetype = "k"
        self.endtranstitlearray = []
        self.endtranstimearray = []
        endflag = 1
        for listnumber in range(1,9):
            listtitlekey = datetype + str(listnumber) + "title"
            listtimekey = datetype + str(listnumber) + "value"
            if config[listtitlekey] == "":
                continue
            if config[listtimekey] == "":
                continue
            self.endtranstitlearray.append(config[listtitlekey])
            self.endtranstimearray.append(config[listtimekey])
            endhour = int(config[listtimekey].split(':')[0])
            if endhour < 5:
                endhour = endhour + 24
            endhour = endhour * 60 + int(config[listtimekey].split(':')[1])
            if (endhour > nowmin):
                endflag = 0
        if endflag == 1:
            if forceview != 1:
                return "0"
        return "1"
