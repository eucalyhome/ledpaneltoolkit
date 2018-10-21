#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageOps, ImageFont, ImageFilter, ImageChops, ImageColor
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import time, re, copy, os, codecs, random, datetime

class ledtoolkit:
    manageconfigfile = '/data/web/cgi/manageled.config'

    def init(self):
        self.loadconfig()
        self._selfinit()

    def _selfinit(self):
        baseconfig = self.getbaseconfig()
        self.fontdir = baseconfig["fontdir"]
        self.imagedir = baseconfig["imagedir"]
        self.fontinit()

    def loadconfig(self):
        filemtime = os.stat(self.manageconfigfile).st_mtime
        try:
            self.prevfilemtime
        except AttributeError:
            self.prevfilemtime = 0
        if filemtime == self.prevfilemtime:
            self.configdata["configdata"]["reload"] = 0
            return
        self.prevfilemtime = filemtime
        self.configdata = {}
        self.configdata["configdata"] = {}
        self.configdata["configdata"]["reload"] = 1
        with codecs.open(self.manageconfigfile,"r", encoding='UTF-8') as f: 
            for line in f:
                elements = re.split('\t',line,2)
                try:
                    elements[1]
                except IndexError:
                    elements.append("")
                elements[1] = elements[1].rstrip()
                elementskey = elements[0].split('-',2)
                try:
                    elementskey[1]
                except IndexError:
                    continue
                try:
                    self.configdata[elementskey[0]]
                except KeyError:
                    self.configdata[elementskey[0]] = {}
                self.configdata[elementskey[0]][elementskey[1]] = elements[1]
        self._selfinit()

    def getconfig(self,primarykey):
        return (self.configdata[primarykey])

    def getbaseconfig(self):
        return (self.configdata["base"])

    def putconfig(self,primarykey,key,value):
        self.configdata[primarykey][key] = value

    def fontinit(self):
        configdata = self.getconfig("viewoption")
        self.fontlarge = ImageFont.truetype(self.fontdir + configdata["fontselect"], 32,encoding='unic')
        self.fontmedium = ImageFont.truetype(self.fontdir + configdata["fontselect"], 16,encoding='unic')
        self.fontsmall  = ImageFont.truetype(self.fontdir + configdata["fontsmallselect"], 8,encoding='unic')

    def fontrender(self,canvasdata,size,rows,cols,messagedata,color,option):
        ledcanvasdraw = ImageDraw.Draw(canvasdata)
        if size == "small":
            textsize = 8
            textfontset = self.fontsmall
        elif size == "medium":
            textsize = 16
            textfontset = self.fontmedium
        else:
            textsize = 32
            textfontset = self.fontlarge
        size = ledcanvasdraw.textsize(messagedata, font=textfontset)
        textrow = int(float(rows) * float(textsize))
        textrow = textrow - size[1] + textsize - 1
        textcol = int(float(cols) * float(textsize))
        if re.compile("right").search(option):
            textcol = textcol - size[0]
        textshadowflag = 0
        if re.compile("shadow").search(option):
            textshadowflag = 1
        if textshadowflag == 1:
            ledcanvasdraw.text((int(textcol)+1, int(textrow)+1), messagedata, font=textfontset, fill="#000")
        textfontcolor = "fill=\"" + color + "\""
        ledcanvasdraw.text((int(textcol), int(textrow)), messagedata, font=textfontset, fill=color)

    def textscroll(self,messagedata,color,bgcolor,option):
        self.loadconfig()
        configdata = self.getconfig("viewoption")
        tempimage = self.imagenew()
        ledcanvasdraw = ImageDraw.Draw(tempimage)
        textsize = 32
        textfontset = self.fontlarge
        size = ledcanvasdraw.textsize(messagedata, font=textfontset)
        textcol = self.ledoptions_cols
        textrow = 0
        textrow = textrow - size[1] + textsize - 1
        scrollimagecols = size[0] + (int(self.ledoptions_cols) * 2)
        scrollbgcolor = ImageColor.getrgb(bgcolor)
        scrollimage = Image.new('RGB', (scrollimagecols, self.ledoptions_rows), scrollbgcolor)
        ledcanvasdraw = ImageDraw.Draw(scrollimage)
        textshadowflag = 0
        if re.compile("shadow").search(option):
            textshadowflag = 1
        if textshadowflag == 1:
            ledcanvasdraw.text((int(textcol)+1, int(textrow)+1), messagedata, font=textfontset, fill="#000")
        textfontcolor = "fill=\"" + color + "\""
        ledcanvasdraw.text((int(textcol), int(textrow)), messagedata, font=textfontset, fill=color)
        beginimage = Image.new('RGB', (self.ledoptions_cols, self.ledoptions_rows), scrollbgcolor)
        self.wipe(beginimage,"instant")
        scrollrange = scrollimagecols - int(self.ledoptions_cols)
        for xposp in range(scrollrange):
            xpos = 0 - xposp
            tempimage.paste(scrollimage, (xpos, 0))
            self.ledoutput(tempimage)
            time.sleep(float(configdata["scrollspeed"]))

    def bgmorf(self,canvasdata,bgdata,option=""):
        self.loadconfig()
        configdata = self.getconfig("viewoption")
        if option != "":
            copyoption = option
        elif option == "morfdisable":
            self.wipe(canvasdata)
            return
        else:
            copyoption = "alpha"
        anix = bgdata.width - canvasdata.width
        aniy = bgdata.height - canvasdata.height
        randomexpseed = random.randrange(10)
        randomxseed = random.randrange(10)
        randomyseed = random.randrange(10)
        expflag = 0
        offflag = 0
        if configdata["bgmorftype"] == "exp":
            if randomexpseed > 5:
                randomexpseed = 10
            else:
                randomexpseed = 5
        elif configdata["bgmorftype"] == "move":
            randomexpseed = 0
        elif configdata["bgmorftype"] == "off":
            offflag = 1
        if randomexpseed > 7:
            expflag = 1
        elif randomexpseed > 4:
            expflag = -1
        if randomxseed > 6:
            randomx = 1
        elif randomxseed > 2:
            randomx = -1
        else:
            randomx = 0
        if randomyseed > 6:
            randomy = 1
        elif randomyseed > 2:
            randomy = -1
        else:
            randomy = 0
        if offflag == 1:
            randomx = 0
            randomy = 0
        posx = 0
        posy = 0
        if randomx == -1:
            posx = anix
        if randomy == -1:
            posy = aniy
        anispeed = int(float(configdata["contspeed"]) / 0.01)
        aniinter = int(configdata["bgmorfspeed"])
        aniwait = int(configdata["bgmorfwait"])
        animoveint = float(anispeed)
        pcount = 0
        timebefore = datetime.datetime.now()
        aniintflag = 0
        for pcounttemp in range(anispeed):
            if aniinter != 0:
                counttemp = pcounttemp % aniinter
                if counttemp != 0:
                    time.sleep(0.01)
                    continue
            pcount = pcount + 1
            if aniwait != 0:
                counttemp = pcount % aniwait
                if counttemp != 0:
                    time.sleep(0.01)
                    continue
            if expflag == 0:
                if randomx == 1:
                    cropx = posx + int(float(anix) / animoveint * float(pcount))
                elif randomx == -1:
                    cropx = posx - int(float(anix) / animoveint * float(pcount))
                else:
                    cropx = 0
                if randomy == 1:
                    cropy = posy + int(float(aniy) / animoveint * float(pcount))
                elif randomy == -1:
                    cropy = posy - int(float(aniy) / animoveint * float(pcount))
                else:
                    cropy = 0
                cropendx = cropx + canvasdata.width
                cropendy = cropy + canvasdata.height

            if expflag == 0:
                bgcropdata = bgdata.crop((int(cropx),int(cropy),int(cropendx),int(cropendy)))
            else:
                if expflag == 1:
                    resizeexp = (float(bgdata.width) / float(self.ledoptions_cols) - 1) * float(pcount) / float(animoveint) + 1
                else:
                    resizeexp = (float(bgdata.width) / float(self.ledoptions_cols) - 1) * (float(animoveint) - float(pcount)) / float(animoveint) + 1
                resizex = int(float(bgdata.width) * resizeexp)
                resizey = int(float(bgdata.height) * resizeexp)
                bgexpdata = bgdata.resize((resizex, resizey))
                cropx = 0
                cropy = 0
                if randomx == 1:
                    cropx = resizex - self.ledoptions_cols
                if randomy == 1:
                    cropy = resizey - self.ledoptions_rows
                cropendx = cropx + canvasdata.width
                cropendy = cropy + canvasdata.height
                bgcropdata = bgexpdata.crop((int(cropx),int(cropy),int(cropendx),int(cropendy)))
            bgcropdata = self.imagecopy(bgcropdata,canvasdata,copyoption)
            bgcropdata = bgcropdata.convert('RGB')
            if aniintflag == 0:
                self.wipe(bgcropdata,"instant")
                aniintflag = 1
            else:
                self.ledoutput(bgcropdata)
            timeafter = datetime.datetime.now()
            timedelay = (float(timeafter.microsecond) - float(timebefore.microsecond)) / float(1000000)
            if timedelay < 0:
                timedelay = 0.01
            timesleep = float(0.01) - timedelay
            if timesleep > 0:
                time.sleep(timesleep)
            timebefore = datetime.datetime.now()
        self.ledcanvasprev = copy.copy(bgcropdata)
    def wipe(self,canvasdata,option=''):
        self.loadconfig()
        configdata = self.getconfig("viewoption")
        self.wipeexec(canvasdata,configdata["wipeselect"],configdata["wipespeed"],"")
        if re.compile("instant").search(option):
            return
        time.sleep(float(configdata["contspeed"]))

    def wipeexec(self,canvasdata,type,speed,option):
        speed = float(speed)
        if type == "randomfade":
            listarray = ["crossfade","tile"]
            type = listarray[random.randrange(len(listarray))]
        elif type == "random":
            listarray = ["crossfade","tile","tinytile","slide","slideh"]
            type = listarray[random.randrange(len(listarray))]
        if type == "crossfade":
            speed = speed / 50
            for i in range(50):
                j = i + 1
                j = float(1) / float(50) * float(j)
                self.crosscanvas = Image.blend(self.ledcanvasprev, canvasdata, j)
                self.ledoutput(self.crosscanvas)
                time.sleep(speed)
        elif type == "tile":
            speed = speed / 32
            masktilebase = Image.new("L", (8,40), 0)
            draw = ImageDraw.Draw(masktilebase)
            draw.rectangle((0, 32, 7, 39), fill=(255), outline=(255))
            for i in range(24):
                j = i + 8
                k = int ( float (255) / float (24) * float (j))
                draw.rectangle((0, j, 7, j), fill=k, outline=k)
            for i in range(32):
                mask = Image.new("L", (canvasdata.width,canvasdata.height), 0)
                masktile = Image.new("L", (16,32), 0)
                j = i + 8
                masktilebase_crop = masktilebase.crop((0, i, 8, j))
                masktile.paste(masktilebase_crop, (0, 0))
                masktilebase_crop = ImageOps.flip(masktilebase_crop)
                masktile.paste(masktilebase_crop, (8, 0))
                for k in range(4):
                    l = k * 8
                    masktile.paste(masktile, (0, l))
                for k in range(8):
                    l = k * 16
                    mask.paste(masktile, (l, 0))
                self.crosscanvas = Image.composite(canvasdata, self.ledcanvasprev, mask)
                self.ledoutput(self.crosscanvas)
                time.sleep(speed)
        elif type == "tinytile":
            speed = speed / 8
            for i in range(8):
                j = i + 1
                mask = Image.new("L", canvasdata.size, 0)
                masktile = Image.new("L", (16,32), 0)
                draw = ImageDraw.Draw(masktile)
                draw.rectangle((0, 0, 7, j), fill=(255), outline=(255))
                j = 8 - j
                draw.rectangle((8, 7, 15, j), fill=(255), outline=(255))
                for k in range(4):
                    l = k * 8
                    masktile.paste(masktile, (0, l))
                for k in range(8):
                    l = k * 16
                    mask.paste(masktile, (l, 0))
                self.crosscanvas = Image.composite(canvasdata, self.ledcanvasprev, mask)
                self.ledoutput(self.crosscanvas)
                time.sleep(speed)
        elif type == "slide":
            speed = speed / self.ledoptions_cols
            canvasmaskbase = Image.new('RGB', ((int(self.ledoptions_cols)*2), self.ledoptions_rows), (0, 0, 0))
            canvasmaskbase.paste(self.ledcanvasprev, (0, 0))
            canvasmaskbase.paste(canvasdata, (self.ledoptions_cols, 0))
            for i in range(self.ledoptions_cols):
                cropx = i + self.ledoptions_cols
                self.crosscanvas = canvasmaskbase.crop((i, 0,cropx , (int(self.ledoptions_rows))))
                self.ledoutput(self.crosscanvas)
                time.sleep(speed)
        elif type == "slideh":
            speed = speed / self.ledoptions_rows
            canvasmaskbase = Image.new('RGB', (self.ledoptions_cols, (int(self.ledoptions_rows)*2)), (0, 0, 0))
            canvasmaskbase.paste(self.ledcanvasprev, (0, 0))
            canvasmaskbase.paste(canvasdata, (0,self.ledoptions_rows))
            for i in range(self.ledoptions_rows):
                cropy = i + self.ledoptions_rows
                self.crosscanvas = canvasmaskbase.crop((0,i,(int(self.ledoptions_cols)),cropy))
                self.ledoutput(self.crosscanvas)
                time.sleep(speed)
        else:
            self.ledoutput(canvasdata)
        self.ledoutput(canvasdata)
        self.ledcanvasprev = copy.copy(canvasdata)

    def imageprevcopy(self,imagedata):
        self.ledcanvasprev = copy.copy(imagedata)

    def imagefitload(self,imagepath,option):
        imagedata = Image.open(imagepath, 'r').convert('RGBA')
        if re.compile("c").search(option):
            cropdata = imagedata.split()[1].getbbox()
            imagedata = imagedata.crop(cropdata)
        if re.compile("h").search(option):
            resizex = self.ledoptions_cols
            resizey = self.ledoptions_cols
        elif re.compile("v").search(option):
            resizex = self.ledoptions_rows
            resizey = self.ledoptions_rows
        else:
            resizex = self.ledoptions_cols
            resizey = self.ledoptions_rows
        if re.compile("b").search(option):
            resizex = int(float(resizex) * float(1.5))
            resizey = int(float(resizey) * float(1.5))
        imagethumbflag = 0
        if imagedata.width < int(resizex):
            resizey = int(float(imagedata.height) * float(resizex) / float(imagedata.width))
            imagethumbflag = 1
        if imagedata.height < int(resizey):
            resizex = int(float(imagedata.width) * float(resizey) / float(imagedata.height))
            imagethumbflag = 1
        if imagethumbflag == 0:
            imagedata.thumbnail((resizex, resizey), Image.ANTIALIAS)
        else:
            imagedata = imagedata.resize((int(resizex),int(resizey)), Image.LANCZOS)
        return (imagedata)

    def imagecopy(self,outputimagedata,imagedata,option):
        pastex = 0
        pastey = 0
        if re.compile("north").search(option):
            pastey = 0
        elif re.compile("south").search(option):
            pastey = self.ledoptions_rows - imagedata.height
        else:
            pastey = int((float(self.ledoptions_rows) / float(2)) - (float(imagedata.height) / float(2)))
        if re.compile("east").search(option):
            pastex = 0
        elif re.compile("west").search(option):
            pastex = self.ledoptions_cols - imagedata.width
        else:
            pastex = int((float(self.ledoptions_cols) / float(2)) - (float(imagedata.width) / float(2)))
        if re.compile("alpha").search(option):
            outputimagedata.paste(imagedata, (pastex, pastey),mask=imagedata)
        elif re.compile("diff").search(option):
            outputimagedata = ImageChops.difference(outputimagedata.convert("RGB"), imagedata.convert("RGB"))
        elif re.compile("add").search(option):
            outputimagedata = ImageChops.add(outputimagedata.convert("RGB"), imagedata.convert("RGB"))
        elif re.compile("subtract").search(option):
            outputimagedata = ImageChops.subtract(outputimagedata.convert("RGB"), imagedata.convert("RGB"))
        elif re.compile("multiply").search(option):
            outputimagedata = ImageChops.multiply(outputimagedata.convert("RGB"), imagedata.convert("RGB"))
        elif re.compile("screen").search(option):
            outputimagedata = ImageChops.screen(outputimagedata.convert("RGB"), imagedata.convert("RGB"))
        elif re.compile("lighter").search(option):
            outputimagedata = ImageChops.lighter(outputimagedata.convert("RGB"), imagedata.convert("RGB"))
        elif re.compile("darker").search(option):
            outputimagedata = ImageChops.darker(outputimagedata.convert("RGB"), imagedata.convert("RGB"))
        else:
            outputimagedata.paste(imagedata, (pastex, pastey))
        return (outputimagedata)

    def imagenew(self,option=""):
        imagecolorspace = 'RGB'
        imagecolorfill = (0, 0, 0)
        imagesizex = self.ledoptions_cols
        imagesizey = self.ledoptions_rows
        if re.compile("alpha").search(option):
            imagecolorspace = 'RGBA'
            imagecolorfill = (0, 0, 0, 0)
        if re.compile("bg").search(option):
            imagesizex = int(float(imagesizex) * float(1.5))
            imagesizey = int(float(imagesizey) * float(1.5))
        image = Image.new(imagecolorspace, (imagesizex, imagesizey), imagecolorfill)
        return (image)

    def ledoutput(self,handle):
        self.matrix.SetImage(handle)

    def ledinit(self):
        configdata = self.getconfig("ledoption")
        self.options = RGBMatrixOptions()
        self.options.hardware_mapping = configdata["hardwaremapping"]
        self.options.led_rgb_sequence = configdata["rgbsequence"]
        self.options.rows = int(configdata["rows"])
        self.options.chain_length = int(configdata["chainlength"])
        self.options.parallel = int(configdata["parallel"])
        self.options.pwm_bits = int(configdata["pwmbits"])
        self.options.brightness = int(configdata["brightness"])
        self.options.pwm_lsb_nanoseconds = int(configdata["pwmlsbnanoseconds"])
        self.options.gpio_slowdown = int(configdata["slowdowngpio"])
        self.ledoptions_rows = int(configdata["rows"])
        self.ledoptions_cols = int(configdata["chainlength"]) * 32
        self.matrix = RGBMatrix(options = self.options)
        self.ledcanvasprev = Image.new('RGB', (self.ledoptions_cols, self.ledoptions_rows), (0, 0, 0))

    def imagesave(self,canvasdata):
        timenowsaveimage = str(time.time())
        canvasdata.save(self.imagedir + 'ledimagedata' + timenowsaveimage + ".png")

    def imageload(self,imagepath):
        canvasdata = Image.open(imagepath, 'r').convert('RGB')
        return (canvasdata)

    def testimagesave(self,canvasdata):
        timenowsaveimage = str(time.time())
        canvasdata.save(self.imagedir + 'ledimagedata' + timenowsaveimage + ".png")
