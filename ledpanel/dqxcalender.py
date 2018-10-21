#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime,time

class dqxcalender:

    def boueigunrender(self,ledtoolkitobject):
        baseconfig = ledtoolkitobject.getbaseconfig()
        self.boueigunresourcedir = baseconfig["boueigunresourcedir"]
        self.mosaicdir = baseconfig["mosaicdir"]

        now = datetime.datetime.now()
        unixtime = int(time.mktime(now.timetuple()))
        btime = int((unixtime - 1535814000) / 3600 % 7)
        if btime == 0:
            bnow = "s"
            bnext = "k"
        elif btime == 1:
            bnow = "k"
            bnext = "b"
        elif btime == 2:
            bnow = "b"
            bnext = "s"
        elif btime == 3:
            bnow = "s"
            bnext = "r"
        elif btime == 4:
            bnow = "r"
            bnext = "r"
        elif btime == 5:
            bnow = "r"
            bnext = "j"
        else:
            bnow = "j"
            bnext = "s"
        imagedata = ledtoolkitobject.imagenew()
        bfilenamenow = self.boueigunresourcedir + bnow + ".png"
        imagebnow = ledtoolkitobject.imageload(bfilenamenow)
        bfilenamenext = self.boueigunresourcedir + bnext + ".png"
        imagebnext = ledtoolkitobject.imageload(bfilenamenext)

        imagedata = ledtoolkitobject.imagecopy(imagedata,imagebnow,"northeast")
        bname = self.boueigunname(bnow)
        ledtoolkitobject.fontrender(imagedata,"small","1","9",bname,"#FFF","shadow")
        hourdata = datetime.datetime.now().strftime("%H")
        hourdata = unicode(hourdata) + u'時'
        ledtoolkitobject.fontrender(imagedata,"medium","0","0",hourdata,"#FFF","shadow")

        imagedata = ledtoolkitobject.imagecopy(imagedata,imagebnext,"southeast")
        bname = self.boueigunname(bnext)
        ledtoolkitobject.fontrender(imagedata,"small","3","9",bname,"#FFF","shadow")
        hourdata = (datetime.datetime.now() + datetime.timedelta(hours=1)).strftime("%H")
        hourdata = unicode(hourdata) + u'時'
        ledtoolkitobject.fontrender(imagedata,"medium","1","0",hourdata,"#FFF","shadow")

        return (imagedata)

    def tokoyamirender(self,ledtoolkitobject):
        baseconfig = ledtoolkitobject.getbaseconfig()
        self.tokoyamiresourcedir = baseconfig["tokoyamiresourcedir"]
        self.mosaicdir = baseconfig["mosaicdir"]

        now = datetime.datetime.now()
        unixtime = int(time.mktime(now.timetuple()))
        btime = int((unixtime - 1510434000) / 86400 % 4)
        tokor = btime + 1
        tokod = (btime + 2) % 4 + 1
        tokom = (btime + 1) % 4 + 1
        tokosh = int((unixtime - 1524430800) / 86400 % 3) + 1


        imagedata = ledtoolkitobject.imagenew()
        filename = self.tokoyamiresourcedir + "0_" + str(tokor) + ".png"
        imagetokor = ledtoolkitobject.imagefitload(filename,"v")
        filename = self.tokoyamiresourcedir + "1_" + str(tokod) + ".png"
        imagetokod = ledtoolkitobject.imagefitload(filename,"v")
        filename = self.tokoyamiresourcedir + "2_" + str(tokom) + ".png"
        imagetokom = ledtoolkitobject.imagefitload(filename,"v")
        filename = self.tokoyamiresourcedir + "shugo/0_" + str(tokosh) + ".png"
        imagetokosh = ledtoolkitobject.imagefitload(filename,"v")
        imagedata.paste(imagetokor,(0,0))
        imagedata.paste(imagetokod,(32,0))
        imagedata.paste(imagetokom,(64,0))
        imagedata.paste(imagetokosh,(96,0))
        return (imagedata)

    def boueigunname(self,i):
        if i == "j":
            return (u'闇朱の獣牙兵団')
        elif i == "s":
            return (u'蒼怨の屍獄兵団')
        elif i == "k":
            return (u'紫炎の鉄機兵団')
        elif i == "b":
            return (u'深碧の造魔兵団')
        return (u'？？？？？？？')
