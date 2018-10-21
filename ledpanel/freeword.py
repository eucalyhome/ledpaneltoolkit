#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

class freeword:
    randprev = 0

    def render(self,ledtoolkitobject):
        config = ledtoolkitobject.getconfig("freeword")
        listvaluearray = []
        listcolorarray = []
        listshadowarray = []
        listbgcolorarray = []
        for listnumber in range(1,9):
            listenablekey = str(listnumber) + "enable"
            listvaluekey = str(listnumber) + "value"
            listcolorkey = str(listnumber) + "color"
            listshadowkey = str(listnumber) + "shadow"
            listbgcolorkey = str(listnumber) + "bgcolor"
            if config[listenablekey] == "":
                continue
            if config[listvaluekey] == "":
                continue
            listvaluearray.append(config[listvaluekey])
            listcolorarray.append(config[listcolorkey])
            listshadowarray.append(config[listshadowkey])
            listbgcolorarray.append(config[listbgcolorkey])
        if len(listvaluearray) == 0:
            imagedata = ledtoolkitobject.imagenew()
            ledtoolkitobject.fontrender(imagedata,"medium","0","0",u'FWエラー',"#F00","")
            imagebgdata = ledtoolkitobject.imagenew()
            return (imagedata,imagebgdata)
        for randomtry in range(10):
            rand = random.randrange(len(listvaluearray))
            if rand != self.randprev:
                self.randprev = rand
                break
        option = ""
        if listshadowarray[rand] == "on":
            option = "shadow"
        fontcolor = listcolorarray[rand].encode('ascii')
        bgcolor = listbgcolorarray[rand].encode('ascii')
        ledtoolkitobject.textscroll(listvaluearray[rand],fontcolor,bgcolor,option)
        return ()
