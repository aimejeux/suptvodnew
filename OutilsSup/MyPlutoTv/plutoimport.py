#!/usr/bin/python
# -*- coding: utf-8 -*-
################################### modified by aime_jeux ##################################
#############                           Aout 2021                              #############
############################################################################################
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Sptvnw.Config import *
import requests,re,json
from base64 import b64encode,b64decode
from operator import truediv
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore',InsecureRequestWarning)
########################################################################
import requests,re,json,time,hashlib,sys,uuid
St = requests.Session()
import datetime
import json
import os
import uuid
import urllib,urllib2
########################################################################
from collections import OrderedDict
from six.moves.urllib.parse import parse_qsl, quote_plus, urlparse
import traceback
##############################################
from six import PY2 as IS_PY2
import uuid
import collections
sid1_hex = str(uuid.uuid4().hex)
deviceId1_hex = str(uuid.uuid4().hex)
########################################################################
def update_qsd_Pluto(url, qsd=None, safe="", quote_via=quote_plus):
	parsed = urlparse(url)
	current_qsd = OrderedDict(parse_qsl(parsed.query, keep_blank_values=True))
	for key, value in qsd.items():
		if value is not None:
			current_qsd[key] = value
	def dict2query(d):
		query = []
		for key in d.keys():
			query.append("{0}={1}".format(key, d[key]))
		return "&".join(query)
	query = quote_via(dict2query(current_qsd), safe="=&" + safe)
	return parsed._replace(query=query).geturl()
def getUUID_Pluto():
    return sid1_hex, deviceId1_hex
def maybe_encode_Pluto(text, encoding="utf8"):
    if IS_PY2:
        if isinstance(text, unicode):
            return text.encode(encoding)
        else:
            return text
    else:
        return text
##############################################
BASE_API = "https://api.pluto.tv"
GUIDE_URL = "https://service-channels.clusters.pluto.tv/v1/guide"
BASE_GUIDE = BASE_API + "/v2/channels"
BASE_LINEUP = BASE_API + "/v2/channels"
BASE_VOD = BASE_API + "/v3/vod/categories"
SEASON_VOD = BASE_API + "/v3/vod/series/%s/seasons"
BOUQUET = "userbouquet.pluto_tv{0}.tv"
##############################################
# BASE_API = "https://api.pluto.tv"
# GUIDE_URL = "https://service-channels.clusters.pluto.tv/v1/guide?start=%s&stop=%s&%s"
# BASE_GUIDE = BASE_API + "/v2/channels?start=%s&stop=%s&%s"
# BASE_LINEUP = BASE_API + "/v2/channels.json?%s"
# BASE_VOD = BASE_API + "/v3/vod/categories?includeItems=true&deviceType=web&%s"
# SEASON_VOD = BASE_API + "/v3/vod/series/%s/seasons?includeItems=true&deviceType=web&%s"
# BASE_CLIPS = BASE_API + "/v2/episodes/%s/clips.json"
# BOUQUET = "userbouquet.pluto_tv{0}.tv"
##############################################
X_FOR = {"local": 'local',
	"us": '185.236.200.172',
	"uk": '185.86.151.11',
	"de": '85.214.132.117',
	"es": '88.26.241.248',
	"ca": '192.206.151.131',
	"br": '177.47.27.205',
	"mx": '200.68.128.83',
	"fr": '176.31.84.249',
	"at": '2.18.68.0',
	"ch": '5.144.31.245',
	"it": '131.114.130.239'}
##############################################
def buildHeader():
	header_dict = {}
	header_dict["Accept"] = "application/json, text/javascript, */*; q=0.01"
	header_dict["Host"] = "api.pluto.tv"
	header_dict["Connection"] = "keep-alive"
	header_dict["Referer"] = "http://pluto.tv/"
	header_dict["Origin"] = "http://pluto.tv"
	header_dict["User-Agent"] = "Mozilla/5.0 (Windows NT 6.2; rv:24.0) Gecko/20100101 Firefox/24.0"
	return header_dict
def buildHeader_Pluto():
    header_dict = {}
    header_dict["Accept"] = "application/json, text/javascript, */*; q=0.01"
    header_dict["Host"] = "api.pluto.tv"#"service-channels.clusters.pluto.tv"#
    header_dict["Connection"] = "keep-alive"
    header_dict["Referer"] = "http://pluto.tv/"
    header_dict["Origin"] = "http://pluto.tv"
    header_dict["User-Agent"] = "Mozilla/5.0 (Windows NT 6.2; rv:24.0) Gecko/20100101 Firefox/24.0"
    return header_dict
##############################################
class PlutotvNew():
    def __init__(self,prox):
        self.Loading = 'Loading  ...... List Live TV %s.. ' % 'Please wait'
        self.listvodmenu = {}
        self.chapters = {}
        self.menu = []
        self.prox = prox#'fr'#Proxyvalue#
        self._list = []
        self.list_seasons = []
        self.menu_ = []
    def getURL_Pluto(self,url,param={},header={"User-agent": "Mozilla/5.0 (Windows NT 6.2; rv:24.0) Gecko/20100101 Firefox/24.0"},life=datetime.timedelta(minutes=15)):
        try:
            req = requests.get(url, param, headers=header)
            req.raise_for_status()
            return req.json()
        except Exception:
            print("[PlutoDownload] error: {}".format(traceback.format_exc()))
            return {}
    def getChannels_Pluto(self,ch_region):#ch_region='fr'
        headers = buildHeader_Pluto()
        if ch_region in X_FOR:
            headers["X-Forwarded-For"] = X_FOR[ch_region]
            return sorted(self.getURL_Pluto(BASE_LINEUP, header=headers, life=datetime.timedelta(hours=1)),
                          key=lambda i: i["number"])
            # return sorted(self.getURL_Pluto(BASE_LINEUP % ("sid=%s&deviceId=%s" % (getUUID_Pluto())), header=headers, life=datetime.timedelta(hours=1)),
                          # key=lambda i: i["number"])
    ##############################################
    #return self.getURL_Pluto(BASE_VOD % ("sid=%s&deviceId=%s" % (getUUID_Pluto())), header=headers, life=datetime.timedelta(hours=1))
    def getOndemand_Pluto(self):#prox='fr'
        headers = buildHeader_Pluto()
        if self.prox in X_FOR:
            headers["X-Forwarded-For"] = X_FOR[self.prox]
            #return sorted(self.getURL_Pluto(BASE_LINEUP % ("sid=%s&deviceId=%s" % (getUUID_Pluto())), header=headers, life=datetime.timedelta(hours=1)), key=lambda i: i["number"],)
            #return self.getURL_Pluto(BASE_VOD % ("sid=%s&deviceId=%s" % (getUUID_Pluto())), header=headers, life=datetime.timedelta(hours=1))
            return self.getURL_Pluto(BASE_VOD, header=headers, life=datetime.timedelta(hours=1))

    ##############################################
    def buildlist_Pluto(self,categorie):
        name = maybe_encode_Pluto(categorie["name"])
        self.listvodmenu[name] = []
        self.menu.append(name)
        items = categorie.get("items", [])
        for item in iter(items):
            # film = (_id,name,summary,genre,rating,duration,poster,image,type)
            itemid = item.get("_id", "")
            if len(itemid) == 0:
                continue
            itemname = maybe_encode_Pluto(item.get("name", ""))
            itemsummary = maybe_encode_Pluto(item.get("summary", ""))
            itemgenre = maybe_encode_Pluto(item.get("genre", ""))
            itemrating = maybe_encode_Pluto(item.get("rating", ""))
            if itemrating.isdigit():
                itemrating = "{0}".format(itemrating)
            else:
                itemrating = "N/A"
            itemduration = int(item.get("duration", "0") or "0") // 1000  # in seconds
            itemimgs = item.get("covers", [])
            itemtype = item.get("type", "")
            seasons = len(item.get("seasonsNumbers", []))
            itemimage = ""
            itemposter = ""
            urls = item.get("stitched", {}).get("urls", [])
            if len(urls) > 0:
                url = urls[0].get("url", "")
            else:
                continue
            if len(itemimgs) > 2:
                itemimage = itemimgs[2].get("url", "")
            if len(itemimgs) > 1 and len(itemimage) == 0:
                itemimage = itemimgs[1].get("url", "")
            if len(itemimgs) > 0:
                itemposter = itemimgs[0].get("url", "")
            self.listvodmenu[name].append((itemid,itemname,itemsummary,itemgenre,itemrating,itemduration,itemposter,itemimage,itemtype,url,seasons,))
	##################################################################
    def getCategories_Pluto(self):
        self.listvodmenu = {}
        ondemand = self.getOndemand_Pluto()
        menuitems = int(ondemand.get("totalCategories", "0"))
        categories = ondemand.get("categories", [])
        if len(categories) == 0:
            print 'mafihache--------------'
            return False,self._list,self.listvodmenu
        else:
            [self.buildlist_Pluto(categorie) for categorie in categories]
            self._list = []
            for key in self.menu:
                self._list.append(show_Menu_PlutoTv(key, "menu", ""))
            return True,self._list,self.listvodmenu
    def playVOD_Pluto(self, name, sid, url):
        _sid, device_id = getUUID_Pluto()
        url = update_qsd_Pluto(url,{"deviceId": device_id,"sid": device_id,"deviceType": "web","deviceMake": "Firefox","deviceModel": "Firefox",
            "appName": "web",},)
        return url
    def Categories_list_Pluto(self):#chercher liste des donnees
        a,self._list,self.listvodmenu = self.getCategories_Pluto()
        return a,self._list,self.listvodmenu
    def Movies_Categories_list_Pluto(self,cond,Mydict):
        self.Categories_list_ = []
        for infos in Mydict[cond]:
            sid   = infos[0]
            print '---------------------------------------------',sid
            name  = maybe_encode_Pluto(infos[1])
            disc  =  maybe_encode_Pluto(infos[2])
            genre  =  infos[3]
            poster  =  infos[6]
            screenshot  =  infos[7]
            categr = maybe_encode_Pluto(infos[8])
            url   = infos[9]
            self.Categories_list_.append(show_menu_list_catego(name,sid,url,poster,screenshot,disc,genre,categr))
            ###########################
        return self.Categories_list_
    def getVOD(self,epid):#chercher des seasons
        self.list_seasons_dict = {}
        self.list_seasons = {}
        headers = buildHeader_Pluto()
        if self.prox in X_FOR:
            headers["X-Forwarded-For"] = X_FOR[self.prox]
        try: self.list_seasons_dict=self.getURL_Pluto(SEASON_VOD % (epid, "sid=%s&deviceId=%s" % (getUUID_Pluto())), header=headers, life=datetime.timedelta(hours=1))
        except:self.list_seasons_dict={}
        if self.list_seasons_dict!={}:
            self.list_seasons = self.buildchapters(self.list_seasons_dict)
            for key in self.list_seasons.keys():
                print '**************************',key
                sname = str(key)
                stipo = "seasons"
                sid = str(key)
                self.menu_.append(show_Menu_PlutoTv("Season" + " " + sname, stipo, sid))
            print self.menu_
            return True,self.menu_,self.list_seasons
        else:return False,self.menu_,self.list_seasons
    def buildchapters(self, chapters):
        self.chapters.clear()
        items = chapters.get("seasons", [])
        for item in iter(items):
            chs = item.get("episodes", [])
            for ch in iter(chs):
                season = ch.get("season", 0)
                if season != "":
                    if season not in self.chapters:
                        self.chapters[season] = []
                    _id = ch.get("_id", "")
                    name = maybe_encode_Pluto(ch.get("name", ""))
                    number = str(ch.get("number", "0"))
                    summary = maybe_encode_Pluto(ch.get("description", ""))
                    rating = maybe_encode_Pluto(ch.get("rating", ""))
                    duration = int(ch.get("duration", "0") or "0") // 1000
                    genre = maybe_encode_Pluto(ch.get("genre", ""))
                    imgs = ch.get("covers", [])
                    urls = ch.get("stitched", {}).get("urls", [])
                    if len(urls) > 0:
                        url = urls[0].get("url", "")
                    else:
                        continue
                    itemimage = ""
                    itemposter = ""
                    if len(imgs) > 2:
                        itemimage = imgs[2].get("url", "")
                    if len(imgs) > 1 and len(itemimage) == 0:
                        itemimage = imgs[1].get("url", "")
                    if len(imgs) > 0:
                        itemposter = imgs[0].get("url", "")
                    self.chapters[season].append((_id, name, number, summary, rating, duration, genre, itemposter, itemimage, url))
        return self.chapters
#a,Mylist,Mydict = PlutotvNew().Categories_list_Pluto()
#print Mylist
# if a:
    # Chouf = PlutotvNew().Movies_Categories_list_Pluto('Nouveau en VOD',Mydict)
    # print Chouf
# _id = '610a71b0df179f0013163112'
# a,mist,dicseason = PlutotvNew().getVOD(_id)
# print type(dicseason)
# print dicseason[1]
# for keys in dicseason['Season 1']:
    # print keys
    #print "=================================================="