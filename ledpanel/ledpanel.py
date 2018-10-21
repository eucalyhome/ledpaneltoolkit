#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ledtoolkit, ledrender, time, os, datetime, random, remoteir


def main():
    ledtoolkitobject = ledtoolkit.ledtoolkit()
    ledrenderobject  = ledrender.ledrender()
    remotedataobject = remoteir.remoteir()
    ledtoolkitobject.init()
    ledtoolkitobject.ledinit()
    ledrenderobject.init(ledtoolkitobject)
    remotedataobject.init(ledtoolkitobject)

    randomprev = {}
    while True:
        config = ledtoolkitobject.getconfig("configdata")
        if config["reload"] == 1:
            config_viewoption = ledtoolkitobject.getconfig("viewoption")
            config_anniverse = ledtoolkitobject.getconfig("anniverse")
            config_endtrans = ledtoolkitobject.getconfig("endtrans")
            config_tokoyami = ledtoolkitobject.getconfig("tokoyami")
            config_boueigun = ledtoolkitobject.getconfig("boueigun")
            config_faceicon = ledtoolkitobject.getconfig("faceicon")
            config_freeword = ledtoolkitobject.getconfig("freeword")
            config_logo = ledtoolkitobject.getconfig("logo")
            config_clock = ledtoolkitobject.getconfig("clock")
            listarray = []
            if config_tokoyami["enable"] == "on":
                listarray.append("tokoyami")
            if config_boueigun["enable"] == "on":
                listarray.append("boueigun")
            if config_faceicon["enable"] == "on":
                listarray.append("faceicon")
            if config_freeword["enable"] == "on":
                listarray.append("freeword")
            if config_logo["enable"] == "on":
                listarray.append("logo")
            if config_clock["enable"] == "on":
                listarray.append("clock")

            intpriority = 4
            if config_viewoption["intpriority"] == "veryhigh":
                intpriority = 8
            elif config_viewoption["intpriority"] == "high":
                intpriority = 7
            elif config_viewoption["intpriority"] == "middle":
                intpriority = 5
            elif config_viewoption["intpriority"] == "low":
                intpriority = 3
            else:
                intpriority = 1

        remotedataobject.remoteexec(ledtoolkitobject,ledrenderobject)

        rand = random.randrange(10)
        if rand < intpriority:
            if config_endtrans["enable"] == "on":
                endtransflag = ledrenderobject.checker(ledtoolkitobject,"endtrans")
                if endtransflag == "1":
                    ledrenderobject.render(ledtoolkitobject,"endtrans")
                    continue
            if config_anniverse["enable"] == "on":
                anniverseflag = ledrenderobject.checker(ledtoolkitobject,"anniverse")
                if anniverseflag == "1":
                    ledrenderobject.render(ledtoolkitobject,"anniverse")
                    continue

        if len(listarray) == 0:
            ledrenderobject.rendererror(ledtoolkitobject)
            continue
        randflag = 0
        for randtemp in range(20):
            rand = random.randrange(len(listarray))
            try:
                randomprev[rand]
            except KeyError:
                randomprev[rand] = 0
            if randomprev[rand] != 1:
                randomprev[rand] = 1
                randflag = 1
                break
            if randflag == 0:
                randomprev = {}
        ledrenderobject.render(ledtoolkitobject,listarray[rand])

if __name__ == '__main__':
    main()
