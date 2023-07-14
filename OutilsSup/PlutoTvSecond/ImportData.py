#!/usr/bin/python
# -*- coding: utf-8 -*-
################################### modified by aime_jeux ##################################
#############                           Aout 2021                              #############
############################################################################################
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore',InsecureRequestWarning)
########################################################################
import requests,re,json,time,hashlib,sys
St = requests.Session()
from time import ctime
########################################################################
BASE_API = "https://i.mjh.nz/PlutoTV/app.json"#"https://raw.githubusercontent.com/matthuisman/i.mjh.nz/master/PlutoTV/app.json"#
BASE_Stirr = "https://i.mjh.nz/Stirr/app.json"#"https://raw.githubusercontent.com/matthuisman/i.mjh.nz/master/Stirr/app.json"#
##############################################
def buildHeader_Pluto_Second():
    header_dict = {}
    header_dict["Host"] = "i.mjh.nz"#"raw.githubusercontent.com"#"i.mjh.nz"
    header_dict["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0"
    header_dict["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    header_dict["Accept-Language"] = "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3"
    header_dict["Accept-Encoding"] = "gzip, deflate"
    #header_dict["Alt-Used"] = "i.mjh.nz"
    header_dict["Connection"] = "keep-alive"
    return header_dict
##############################################
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Sptvnw.Config import show_listprogramme,show_Menu_PlutoTv_Stirr
##############################################
class ImportData():
    def __init__(self):
        self.Loading = 'Loading  ...... List Live TV %s.. ' % 'Please wait'
        self.listvodmenu = {}
        self.chapters = {}
        self.menu = []
        self._list = []
        self.list_seasons = []
        self.menu_ = []
        self.Aze = ''
        self.Zer = ''
    def getURL_Pluto_Second(self,url,header):
        try:
            req = requests.get(url,headers=header,verify=False)
            req.raise_for_status()
            return True,req.json()
        except Exception:
            return False,{}
    def getChannels_Pluto(self):
        headers = buildHeader_Pluto_Second()
        a,self.listvodmenu = self.getURL_Pluto_Second(BASE_API, headers)
        if a:return True,self.listvodmenu
        else:return False,self.listvodmenu
    def Programmes_Pluto(self,_Ttl,listos,prox,sid):
        self.listprogramme = []
        self._dons = ''
        self.Aze = listos['regions'][prox]['channels'][str(sid)]
        self.Zer =  self.Aze['programs']
        self.lenlist = len(self.Zer)
        i = 1
        self.listprogramme.append(show_listprogramme('',_Ttl,'premier'))
        self.listprogramme.append(show_listprogramme('Program','Time','second'))
        for items in self.Zer:
            Titles = items[1].encode('utf-8')
            timep  = items[0]
            Tme_   = ctime(timep)
            self._dons += Titles+'  :  '+str(Tme_)+'\n'
            self.listprogramme.append(show_listprogramme(str(i),Titles,Tme_))
            i = i + 1
        return str(self._dons),self.listprogramme
    def getChannels_Pluto_Stirr(self):
        self.myfinalist = []
        self.List_MoviePlayer_1 = []
        headers = buildHeader_Pluto_Second()
        a,self.listvodmenu = self.getURL_Pluto_Second(BASE_Stirr, headers)
        if a:
            i = 1
            for keys in self.listvodmenu['channels'].keys():
                name        = self.listvodmenu['channels'][keys].get('name','').encode('utf-8')#
                description = self.listvodmenu['channels'][keys].get('description','')#
                logo = self.listvodmenu['channels'][keys].get('logo','')#
                url = self.listvodmenu['channels'][keys].get('url','')#
                groups = self.listvodmenu['channels'][keys].get('groups','')#
                programs = self.listvodmenu['channels'][keys].get('programs','')
                self.myfinalist.append(show_Menu_PlutoTv_Stirr(str(i)+'.  '+name,url,logo,groups,description,programs))
                self.List_MoviePlayer_1.append(('',name,name +' .......','',url,'','',logo,'',''))
                i = i + 1
            return True,self.myfinalist,self.List_MoviePlayer_1
        else:return False,self.listvodmenu,self.List_MoviePlayer_1