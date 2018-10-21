#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime,time

class ledclock:

    def render(self,ledtoolkitobject):
        config = ledtoolkitobject.getconfig("clock")
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
        imagedata = ledtoolkitobject.imagenew()
        now = datetime.datetime.now()
        renderdate = '{0:%m/%d}'.format(now)
        ledtoolkitobject.fontrender(imagedata,"medium","0","0",renderdate,"#FFF","shadow")
        rendertime = '{0:%H:%M}'.format(now)
        ledtoolkitobject.fontrender(imagedata,"large","0","1.5",rendertime,"#FFF","shadow")

        return (imagedata,bgmorfoption)
