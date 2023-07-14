#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests,re,json,zlib
from base64 import b64encode,b64decode
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
import datetime
import json
import os
import uuid
import urllib,urllib2
from GetServers import get_InfosOXml_Stalker
global _InfosSrvers
_InfosSrvers = get_InfosOXml_Stalker()
##############################################################################################
os_platform = sys.platform
print 'os_platform = ',os_platform
if os_platform == 'win32':
    Player_U_AGENT = ' :http_user-agent="Lavf/57.83.100"'
elif os_platform == 'win64':
    Player_U_AGENT = ' --http-user-agent "Kodi/18.9 (Linux; Android 7.1.1; E6633 Build/32.4.A.1.54) Android/7.1.1 Sys_CPU/armv8l App_Bitness/32 Version/18.9-(18.9.0)-Git:20201023-0655c2c718"'
else:
    Player_U_AGENT = '#User-Agent: Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 2 rev: 250 Safari/533.3'
##############################################################################################
link_dat_expr = "/server/load.php?type=account_info&action=get_main_info&JsHttpRequest=1-xml"
##############################################################################################
class Stalker():
    def __init__(self):
        self.stalker_list = []
        self.Iptv_list = []
        self.Stalker_list_Catgt = []
        self.genres_ITV_List = []
        self._InfosSrvers = _InfosSrvers
        self.Tokn = False
        self.get_Stalker()
        self._Headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0 (QtEmbedded; U; Linux; C)',
                    'Cookie': 'mac=00:1A:79:0D:1F:49; stb_lang=en; timezone=Europe/Amsterdam;'}
        #############################
        self.Host = ''
        self.Mac = ''
        self.token = ''
        self.timezone = ''
        self.lang = ''
        #############################
    def get_Stalker(self):
        self.stalker_list=self._InfosSrvers
        self.stalker_list = self.stalker_list[1]
        return self.stalker_list
    def _Host_Mac_Head_Stalker(self,indx):
        try:
            self.Host=self.stalker_list[indx][1]
            self.Mac = self.stalker_list[indx][2]
            self.Mac = self.Mac.replace(':','%3A')
        except:return False
        self._Headers.update({'Cookie': 'mac='+self.Mac+'; stb_lang=en; timezone=Europe/Amsterdam;'})
        lnk = self.Host+'/portal.php?type=stb&action=handshake&JsHttpRequest=1-xml'
        try:
            data = St.get(lnk,headers=self._Headers,verify=False,timeout=2).json()
            self.token = data['js']['token']
            self._Headers.update({'Authorization': 'Bearer '+self.token})
        except:
            self.token = 'nada'
        if self.token != 'nada':
            return self._lan_timezone()
        else:return False
    def _lan_timezone(self):
        href = self.Host+'/portal.php?type=stb&action=get_profile&JsHttpRequest=1-xml'
        try:
            _dat = St.get(href,headers=self._Headers,verify=False,timeout=2).json()
            self.lang = _dat["js"]["stb_lang"]
            self.timezone = _dat["js"]['default_timezone'].replace('\\','').replace('/','%2F')
            self._Headers.update({'Cookie': 'mac='+self.Mac+'; stb_lang='+self.lang+'; timezone='+self.timezone})
            print 'Password = ',_dat["js"]["password"]
            print 'login = ',_dat["js"]["login"]
            print 'stb_type = ',_dat["js"]["stb_type"]
        except:_dat = 'nada'
        if _dat != 'nada':return True
        else:return False
    def _lan_Dat_Exprt(self,indx):
        date = ''
        if self._Host_Mac_Head_Stalker(indx):
            linkos = self.Host+link_dat_expr
            try:
                data = St.get(linkos,headers=self._Headers,verify=False,timeout=2).json()
                date = data['js']['phone']
            except:date = 'nada'
            if date !='nada':return date
            else:return 'N/A'
        else:return 'N/A_[Prbl Token]'