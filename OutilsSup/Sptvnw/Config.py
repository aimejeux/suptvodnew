#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmap, MultiContentEntryPixmapAlphaTest, MultiContentEntryPixmapAlphaBlend
from enigma import getDesktop, eListboxPythonMultiContent, eListbox, eTimer, gFont, RT_HALIGN_LEFT, RT_HALIGN_RIGHT, RT_HALIGN_CENTER, RT_WRAP, loadPNG
from Components.Input import Input
from Components.MenuList import MenuList
from skin import loadSkin
from urllib2 import urlopen, Request, URLError, HTTPError
import urllib, re
import urllib2
import os
import shutil
from os import system as os_system
from Tools.Directories import fileExists, pathExists
from enigma import getDesktop
dwidth = getDesktop(0).size().width()
##############################################################
#############################################################
import requests,re,json,time
S = requests.Session()
#############################################################
import time 
import sys 
import os 
#######################################################
png1 = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/img/TV.png'
png2 = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/img/VOD.png'
png3 = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/img/_log.png'
png4 = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/img/SERIES.png'
#######################################################
png5 = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/img/playlist/plutocine.png'
png6 = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/img/playlist/plutoseries.png'
png7 = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/img/playlist/pluto.png'
png8 = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/img/playlist/tmdbico.png'
png9 = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/img/playlist/download.png'
class MatchList(MenuList):
    def __init__(self, list):
        MenuList.__init__(self, list, False, eListboxPythonMultiContent)
        self.l.setFont(0, gFont('Regular', 21))
        self.l.setFont(1, gFont('Regular', 26))
        self.l.setItemHeight(50)
class m2list(MenuList):
    def __init__(self, list):
        MenuList.__init__(self, list, False, eListboxPythonMultiContent)
        self.l.setFont(0, gFont('Regular', 10))
        self.l.setFont(1, gFont('Regular', 16))
        self.l.setFont(2, gFont('Regular', 18))
        self.l.setFont(3, gFont('Regular', 20))
        self.l.setFont(4, gFont('Regular', 22))
        self.l.setFont(5, gFont('Regular', 24))
        self.l.setFont(6, gFont('Regular', 26))
        self.l.setFont(7, gFont('Regular', 28))
        self.l.setFont(8, gFont('Regular', 55))
def show_Menu_SuptvodNews(name, link):##, color_sel=0xFFFFFF
    if dwidth == 1280:
        res = [(name, link)]
        res.append(MultiContentEntryText(pos=(5, 2), size=(650, 31), font=3, text=name, flags=RT_HALIGN_LEFT))
        return res
    else:
        res = [(name, link)]
        res.append(MultiContentEntryText(pos=(5, 2), size=(732, 37), font=7, text=name, flags=RT_HALIGN_LEFT))
        return res
def show_Menu_Stalker(name, link,typ):##, color_sel=0xFFFFFF
    res = [(name, link,typ)]
    if dwidth == 1280:
        res.append(MultiContentEntryText(pos=(5, 2), size=(650, 31), font=3, text=name, flags=RT_HALIGN_LEFT))
        return res
    else:
        if typ == 'TV':res.append(MultiContentEntryPixmapAlphaBlend(pos=(5, 2), size=(37, 37), png=loadPNG(png1)))
        elif typ == 'VOD':res.append(MultiContentEntryPixmapAlphaBlend(pos=(5, 2), size=(37, 37), png=loadPNG(png2)))
        else:res.append(MultiContentEntryPixmapAlphaBlend(pos=(5, 2), size=(37, 37), png=loadPNG(png3)))
        res.append(MultiContentEntryText(pos=(47, 2), size=(732, 37), font=7, text=name, flags=RT_HALIGN_LEFT))
        return res
def show_Menu_Stalker_1(name, link,stream,typ):##, color_sel=0xFFFFFF
    res = [(name, link,stream,typ)]
    if dwidth == 1280:
        res.append(MultiContentEntryText(pos=(5, 2), size=(650, 31), font=3, text=name, flags=RT_HALIGN_LEFT))
        return res
    else:
        if typ == 'TV':res.append(MultiContentEntryPixmapAlphaBlend(pos=(5, 2), size=(37, 37), png=loadPNG(png1)))
        elif typ == 'VOD':res.append(MultiContentEntryPixmapAlphaBlend(pos=(5, 2), size=(37, 37), png=loadPNG(png2)))
        else:res.append(MultiContentEntryPixmapAlphaBlend(pos=(5, 2), size=(37, 37), png=loadPNG(png3)))
        res.append(MultiContentEntryText(pos=(47, 2), size=(732, 37), font=7, text=name, flags=RT_HALIGN_LEFT))
        return res
def show_Menu_Stalker_Series(name, link,stream,typ,lists):##, color_sel=0xFFFFFF
    res = [(name, link,stream,typ,lists)]
    if dwidth == 1280:
        res.append(MultiContentEntryText(pos=(5, 2), size=(650, 31), font=3, text=name, flags=RT_HALIGN_LEFT))
        return res
    else:
        if typ == 'TV':res.append(MultiContentEntryPixmapAlphaBlend(pos=(5, 2), size=(37, 37), png=loadPNG(png1)))
        elif typ == 'VOD':res.append(MultiContentEntryPixmapAlphaBlend(pos=(5, 2), size=(37, 37), png=loadPNG(png2)))
        else:res.append(MultiContentEntryPixmapAlphaBlend(pos=(5, 2), size=(37, 37), png=loadPNG(png4)))
        res.append(MultiContentEntryText(pos=(47, 2), size=(732, 37), font=7, text=name, flags=RT_HALIGN_LEFT))
        return res
def show_Menu_Stalker_Vod(name, link,mac,dicto,typ):
    res = [(name, link,mac,dicto,typ)]
    if dwidth == 1280:
        res.append(MultiContentEntryText(pos=(5, 2), size=(650, 31), font=3, text=name, flags=RT_HALIGN_LEFT))
        return res
    else:
        if typ == 'TV':res.append(MultiContentEntryPixmapAlphaBlend(pos=(5, 2), size=(37, 37), png=loadPNG(png1)))
        elif typ == 'VOD':res.append(MultiContentEntryPixmapAlphaBlend(pos=(5, 2), size=(37, 37), png=loadPNG(png2)))
        else:res.append(MultiContentEntryPixmapAlphaBlend(pos=(5, 2), size=(37, 37), png=loadPNG(png3)))
        res.append(MultiContentEntryText(pos=(47, 2), size=(732, 37), font=7, text=name, flags=RT_HALIGN_LEFT))
        return res
def show_Menu_Moved(name, link):##, color_sel=0xFFFFFF
    if dwidth == 1280:
        res = [(name, link)]
        res.append(MultiContentEntryText(pos=(5, 2), size=(650, 31), font=3, text=name, flags=RT_HALIGN_LEFT))
        return res
    else:
        res = [(name, link)]
        res.append(MultiContentEntryText(pos=(5, 15), size=(500, 100), font=8, text=name, flags=RT_HALIGN_CENTER))
        return res
def show_Menu_PlutoTv(name, link,stream):##, color_sel=0xFFFFFF
    res = [(name, link,stream)]
    if dwidth == 1280:
        res.append(MultiContentEntryText(pos=(5, 2), size=(650, 31), font=3, text=name, flags=RT_HALIGN_LEFT))
        return res
    else:
        res.append(MultiContentEntryPixmapAlphaBlend(pos=(5, 6), size=(37, 37), png=loadPNG(png7)))
        res.append(MultiContentEntryText(pos=(45, 2), size=(732, 37), font=7, text=name, flags=RT_HALIGN_LEFT))
        return res
def show_menu_list_catego(name,sid,url,poster,screenshot,disc,genre,categr):##, color_sel=0xFFFFFF
    res = [(name,sid,url,poster,screenshot,disc,genre,categr)]
    if dwidth == 1280:
        res.append(MultiContentEntryText(pos=(5, 2), size=(650, 31), font=3, text=name, flags=RT_HALIGN_LEFT))
        return res
    else:
        if categr == 'movie':res.append(MultiContentEntryPixmapAlphaBlend(pos=(5, 6), size=(37, 37), png=loadPNG(png5)))
        elif categr == 'series':res.append(MultiContentEntryPixmapAlphaBlend(pos=(5, 6), size=(37, 37), png=loadPNG(png6)))
        else:res.append(MultiContentEntryPixmapAlphaBlend(pos=(5, 6), size=(37, 37), png=loadPNG(png7)))
        res.append(MultiContentEntryText(pos=(45, 2), size=(732, 37), font=7, text=name, flags=RT_HALIGN_LEFT))
        return res
def show_menu_list_secondpluto(name,url,url_alt,logo,group,programs,chno,items):##, color_sel=0xFFFFFF
    res = [(name,url,url_alt,logo,group,programs,chno,items)]
    if dwidth == 1280:
        res.append(MultiContentEntryText(pos=(5, 2), size=(650, 31), font=3, text=name, flags=RT_HALIGN_LEFT))
        return res
    else:
        # if categr == 'movie':res.append(MultiContentEntryPixmapAlphaBlend(pos=(5, 6), size=(37, 37), png=loadPNG(png5)))
        # elif categr == 'series':res.append(MultiContentEntryPixmapAlphaBlend(pos=(5, 6), size=(37, 37), png=loadPNG(png6)))
        # else:res.append(MultiContentEntryPixmapAlphaBlend(pos=(5, 6), size=(37, 37), png=loadPNG(png7)))
        res.append(MultiContentEntryText(pos=(45, 2), size=(732, 37), font=7, text=name, flags=RT_HALIGN_LEFT))
        return res
def show_Menu_PlutoTv_episodes(name,img,url,sid):
    res = [(name,img,url,sid)]
    if dwidth == 1280:
        res.append(MultiContentEntryText(pos=(5, 2), size=(650, 31), font=3, text=name, flags=RT_HALIGN_LEFT))
        return res
    else:
        res.append(MultiContentEntryPixmapAlphaBlend(pos=(5, 6), size=(37, 37), png=loadPNG(png7)))
        res.append(MultiContentEntryText(pos=(45, 2), size=(732, 37), font=7, text=name, flags=RT_HALIGN_LEFT))
        return res
def show_listprogramme(name,ttl,cond):
    res = [(name,ttl,cond)]
    if dwidth == 1280:
        res.append(MultiContentEntryText(pos=(5, 2), size=(650, 31), font=3, text=name, flags=RT_HALIGN_LEFT))
        return res
    else:
        #res.append(MultiContentEntryPixmapAlphaBlend(pos=(5, 6), size=(37, 37), png=loadPNG(png7)))
        if cond == 'premier':
            res.append(MultiContentEntryText(pos=(2, 2), size=(1150, 37), font=7, text=ttl,backcolor=0x80000000, flags=RT_HALIGN_CENTER))
        elif cond == 'second':
            res.append(MultiContentEntryText(pos=(0, 2), size=(575, 37), font=7, text=name,backcolor=0x2f07e1 , flags=RT_HALIGN_CENTER))
            res.append(MultiContentEntryText(pos=(577, 2), size=(573, 37), font=7, text=ttl,backcolor=0x047576, flags=RT_HALIGN_CENTER))
        else:
            res.append(MultiContentEntryText(pos=(2, 2), size=(20, 37), font=7, text=name,backcolor=0x2ECCFA , flags=RT_HALIGN_CENTER))
            res.append(MultiContentEntryText(pos=(22, 2), size=(573, 37), font=7, text=ttl, backcolor=0x80000000,flags=RT_HALIGN_CENTER))
            res.append(MultiContentEntryText(pos=(575, 2), size=(600, 37), font=7, text=cond, backcolor=0x137ff9 ,flags=RT_HALIGN_CENTER))
        return res
def show_Menu_PlutoTv_Stirr(name,url,logo,groups,description,programs):
    res = [(name,url,logo,groups,description,programs)]
    if dwidth == 1280:
        res.append(MultiContentEntryText(pos=(5, 2), size=(650, 31), font=3, text=name, flags=RT_HALIGN_LEFT))
        return res
    else:
        res.append(MultiContentEntryPixmapAlphaBlend(pos=(5, 6), size=(37, 37), png=loadPNG(png7)))
        res.append(MultiContentEntryText(pos=(45, 2), size=(732, 37), font=7, text=name, flags=RT_HALIGN_LEFT))
        return res
def show_Menu_MoviesFolder(name,url):
    res = [(name,url)]
    if dwidth == 1280:
        res.append(MultiContentEntryText(pos=(5, 2), size=(650, 31), font=3, text=name, flags=RT_HALIGN_LEFT))
        return res
    else:
        res.append(MultiContentEntryPixmapAlphaBlend(pos=(5, 6), size=(37, 37), png=loadPNG(png7)))
        res.append(MultiContentEntryText(pos=(45, 2), size=(732, 37), font=7, text=name, flags=RT_HALIGN_LEFT))
        return res
def show_Menu_IPTV(chan_counter,name,description,piconname,stream_url,playlist_url,category_id,img_src,description4playlist_html,ts_stream):
    res = [(chan_counter,name,description,piconname,stream_url,playlist_url,category_id,img_src,description4playlist_html,ts_stream)]
    if dwidth == 1280:
        res.append(MultiContentEntryText(pos=(5, 2), size=(650, 31), font=3, text=name, flags=RT_HALIGN_LEFT))
        return res
    else:
        res.append(MultiContentEntryPixmapAlphaBlend(pos=(5, 6), size=(37, 37), png=loadPNG(png7)))
        res.append(MultiContentEntryText(pos=(45, 2), size=(732, 37), font=7, text=name, flags=RT_HALIGN_LEFT))
        return res
def show_Menu_IMDB(original_title,Movies,url_imdb,Img,media_type,original_language,vote_average,vote_count,overview,Trailer):
    res = [(original_title,Movies,url_imdb,Img,media_type,original_language,vote_average,vote_count,overview,Trailer)]
    if dwidth == 1280:
        res.append(MultiContentEntryText(pos=(5, 2), size=(650, 31), font=3, text=name, flags=RT_HALIGN_LEFT))
        return res
    else:
        res.append(MultiContentEntryPixmapAlphaBlend(pos=(5, 6), size=(37, 37), png=loadPNG(png8)))
        res.append(MultiContentEntryText(pos=(45, 2), size=(732, 37), font=6, text=original_title, flags=RT_HALIGN_LEFT))
        return res
def show_Menu_MessagBox(choice1,choice2):
    res = [(choice1,choice2)]
    if dwidth == 1280:
        res.append(MultiContentEntryText(pos=(5, 2), size=(650, 31), font=3, text=name, flags=RT_HALIGN_LEFT))
        return res
    else:
        res.append(MultiContentEntryPixmapAlphaBlend(pos=(5, 6), size=(37, 37), png=loadPNG(png9)))
        res.append(MultiContentEntryText(pos=(45, 2), size=(732, 37), font=6, text=choice1, flags=RT_HALIGN_LEFT))
        return res
def show_Menu2_IMDB(original_title,Movies):
    res = [(original_title,Movies)]
    if dwidth == 1280:
        res.append(MultiContentEntryText(pos=(5, 2), size=(650, 31), font=3, text=name, flags=RT_HALIGN_LEFT))
        return res
    else:
        res.append(MultiContentEntryPixmapAlphaBlend(pos=(5, 6), size=(37, 37), png=loadPNG(png8)))
        res.append(MultiContentEntryText(pos=(45, 2), size=(732, 37), font=5, text=original_title, flags=RT_HALIGN_LEFT))
        return res