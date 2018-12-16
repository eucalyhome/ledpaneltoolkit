#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime,time

class dqxcalender:
    tokoyamipage = 0

    def boueigunrender(self,ledtoolkitobject):
        baseconfig = ledtoolkitobject.getbaseconfig()
        self.boueigunresourcedir = baseconfig["boueigunresourcedir"]
        self.mosaicdir = baseconfig["mosaicdir"]

        now = datetime.datetime.now()
        unixtime = int(time.mktime(now.timetuple()))
        btime = int((unixtime - 1543676400) / 3600 % 7)
        if btime == 0:
            bnow = "k"
            bnext = "m"
        elif btime == 1:
            bnow = "m"
            bnext = "b"
        elif btime == 2:
            bnow = "b"
            bnext = "s"
        elif btime == 3:
            bnow = "s"
            bnext = "m"
        elif btime == 4:
            bnow = "m"
            bnext = "r"
        elif btime == 5:
            bnow = "r"
            bnext = "j"
        else:
            bnow = "j"
            bnext = "k"
        imagedata = ledtoolkitobject.imagenew()
        bfilenamenow = self.boueigunresourcedir + bnow + ".png"
        imagebnow = ledtoolkitobject.imageload(bfilenamenow)
        bfilenamenext = self.boueigunresourcedir + bnext + ".png"
        imagebnext = ledtoolkitobject.imageload(bfilenamenext)

        imagedata = ledtoolkitobject.imagecopy(imagedata,imagebnow,"northeast")
        bname = self.boueigunname(bnow)
        ledtoolkitobject.fontrender(imagedata,"medium","0","2",bname,"#FFF","shadow")
        ledtoolkitobject.fontrender(imagedata,"small","1","14",u'兵団',"#FFF","shadow")
        hourdata = datetime.datetime.now().strftime("%H")
        hourdata = unicode(hourdata)
        ledtoolkitobject.fontrender(imagedata,"medium","0","0",hourdata,"#FFF","shadow")
        ledtoolkitobject.fontrender(imagedata,"small","1","2",u'時',"#FFF","shadow")

        imagedata = ledtoolkitobject.imagecopy(imagedata,imagebnext,"southeast")
        bname = self.boueigunname(bnext)
        ledtoolkitobject.fontrender(imagedata,"medium","1","2",bname,"#FFF","shadow")
        ledtoolkitobject.fontrender(imagedata,"small","3","14",u'兵団',"#FFF","shadow")
        hourdata = (datetime.datetime.now() + datetime.timedelta(hours=1)).strftime("%H")
        hourdata = unicode(hourdata) + u': '
        ledtoolkitobject.fontrender(imagedata,"medium","1","0",hourdata,"#FFF","shadow")
        ledtoolkitobject.fontrender(imagedata,"small","3","2",u'時',"#FFF","shadow")

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
        tokosh2 = int((tokosh + 2) % 3)

        self.tokoyamipage = self.tokoyamipage + 1
        if self.tokoyamipage == 2:
            self.tokoyamipage = 0

        imagedata = ledtoolkitobject.imagenew()
        if self.tokoyamipage == 0:
            filename = self.tokoyamiresourcedir + "0_" + str(tokor) + ".png"
            imagetokor = ledtoolkitobject.imagefitload(filename,"v")
            filename = self.tokoyamiresourcedir + "1_" + str(tokod) + ".png"
            imagetokod = ledtoolkitobject.imagefitload(filename,"v")
            filename = self.tokoyamiresourcedir + "2_" + str(tokom) + ".png"
            imagetokom = ledtoolkitobject.imagefitload(filename,"v")
            imagedata.paste(imagetokor,(16,0))
            imagedata.paste(imagetokod,(48,0))
            imagedata.paste(imagetokom,(80,0))

        if self.tokoyamipage == 1:
            filename = self.tokoyamiresourcedir + "shugo/0_" + str(tokosh) + ".png"
            imagetokosh = ledtoolkitobject.imagefitload(filename,"v")
            filename = self.tokoyamiresourcedir + "shugo/1_" + str(tokosh2) + ".png"
            imagetokosh2 = ledtoolkitobject.imagefitload(filename,"v")
            imagedata.paste(imagetokosh,(32,0))
            imagedata.paste(imagetokosh2,(64,0))

        return (imagedata)

    def boueigunname(self,i):
        if i == "j":
            return (u'闇朱の獣牙')
        elif i == "s":
            return (u'蒼怨の屍獄')
        elif i == "k":
            return (u'紫炎の鉄機')
        elif i == "b":
            return (u'深碧の造魔')
        elif i == "m":
            return (u'銀甲の凶蟲')
        return (u'？？？？？？？')
