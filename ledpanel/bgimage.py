#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

class bgimage:

    def render(self,ledtoolkitobject):
        baseconfig = ledtoolkitobject.getbaseconfig()
        self.mosaicdir = baseconfig["mosaicdir"]
        imagemosaicfilename = self.randommosaic()
        imagemosaic = ledtoolkitobject.imagefitload(imagemosaicfilename,"hb")
        return (imagemosaic)

    def randommosaic(self):
        rand1 = random.randrange(9)
        rand2 = random.randrange(3)
        rand3 = random.randrange(34)
        rand4 = random.randrange(30)
        mosaicfilename = self.mosaicdir + "zoom_" + str(rand1) + "_" + str(rand2) + "_" + str(rand3) + "_" + str(rand4) + ".png"
        return (mosaicfilename)
