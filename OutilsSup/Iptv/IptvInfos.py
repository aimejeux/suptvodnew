#!/usr/bin/python
# -*- coding: utf-8 -*-
################################### modified by aime_jeux ##################################
#############                           Aout 2021                              #############
############################################################################################
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Sptvnw.Config import show_Menu_IPTV
from xml.etree.cElementTree import fromstring
from base64 import b64encode,b64decode
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore',InsecureRequestWarning)
########################################################################
import requests,re,json,time,sys,os,datetime
St = requests.Session() 
########################################################################
import traceback
##############################################
BASE_API = "%senigma2.php?username=%s&password=%s"
#http://m.speedtestcm.com:80/enigma2.php?username=Hwpbej7aPC&password=OSvTY8J6I5
##############################################
class IptvInfos():
    def __init__(self):
        self.Loading = 'Loading  ...... List Live TV %s.. ' % 'Please wait'
        self.menu = []
        self._list = []
        self.list_seasons = []
        self.menu_ = []
    def getURL(self,url):
        print self.Loading
        try:
            req = requests.get(url,verify=False)
            req.raise_for_status()
            return True,req.content
        except Exception:
            print("[getURL] error: {}".format(traceback.format_exc()))
            return False,''
    def decode_discription(self,description):
        description = b64decode(description)
        description = description.replace('<br>', '\n')
        description = description.replace('<br/>', '\n')
        description = description.replace('</h1>', '</h1>\n')
        description = description.replace('</h2>', '</h2>\n')
        description = description.replace('&nbsp;', ' ')
        description4playlist_html = description
        text = re.compile('<[\\/\\!]*?[^<>]*?>')
        description = text.sub('', description)
        return description
    def get_donnees_enigma(self,xml):
        self.iptv_list_temp = []
        self.next_page_url = ''
        self.next_page_text = ''
        self.prev_page_url = ''
        self.prev_page_text = ''
        self.playlistname = xml.findtext('playlist_name').encode('utf-8')
        self.next_page_url = xml.findtext('next_page_url')
        self.next_page_text_element = xml.findall('next_page_url')
        if self.next_page_text_element:
            self.next_page_text = self.next_page_text_element[0].attrib.get('text').encode('utf-8')
        self.prev_page_url = xml.findtext('prev_page_url')
        self.prev_page_text_element = xml.findall('prev_page_url')
        if self.prev_page_text_element:
            self.prev_page_text = self.prev_page_text_element[0].attrib.get('text').encode('utf-8')
        chan_counter = 1
        if len(xml.findall('channel'))==0:return False,[]
        for channel in xml.findall('channel'):
            name = channel.findtext('title').encode('utf-8')
            name = b64decode(name)
            if 'All'.lower() in name.lower():continue
            piconname = channel.findtext('logo')
            description = channel.findtext('description')
            desc_image = channel.findtext('desc_image')
            img_src = ''
            if description != None:
                description = description.encode('utf-8')
                if desc_image:
                    img_src = desc_image
                description = self.decode_discription(description)
                description4playlist_html = description
            stream_url = channel.findtext('stream_url')
            playlist_url = channel.findtext('playlist_url')
            category_id = channel.findtext('category_id')
            ts_stream = channel.findtext('ts_stream')
            chan_tulpe = show_Menu_IPTV(chan_counter,name,description,piconname,stream_url,playlist_url,category_id,
                        img_src,description4playlist_html,ts_stream)
            self.iptv_list_temp.append(chan_tulpe)
            chan_counter = chan_counter + 1
        return True,self.iptv_list_temp
    def get_url_enigma(self,host,usr,passw):
        URL = BASE_API%(host,usr,passw)
        print "URL = ",URL
        a,data = self.getURL(URL)
        if a:
            data = fromstring(data)
            return self.get_donnees_enigma(data)
        else:
            return False,[]
    def get_url_enigma_type(self,lnk):
        print "URL = ",lnk
        a,data = self.getURL(lnk)
        if a:
            data = fromstring(data)
            return self.get_donnees_enigma(data)
        else:
            return False,[]
def get_MyInfosIptv(url,Category=None):
    Mylist = []
    _Get = IptvInfos()
    if Category=='categ':
        host = url.split('enigma2.php')[0]
        usr  = re.findall('username=(.+?)&',url)[0]
        passw= re.findall('password=(.+?)\Z',url)[0]
        _Url = BASE_API % (host,usr,passw)
        print host,usr,passw,_Url
        a,Mylist = _Get.get_url_enigma(host,usr,passw)
        if a:return True,Mylist
        else:return False,Mylist
    else:
        print "Category = ",Category
        a,Mylist = _Get.get_url_enigma_type(url)
        if a:return True,Mylist
        else:return False,Mylist
################################################Live Streams###############################################
def get_Category(url,Category=''):
    '''(chan_counter,name,description,piconname,stream_url,playlist_url,category_id,
                        img_src,description4playlist_html,ts_stream)'''
    a,Mylist = get_MyInfosIptv(url,Category=Category)
    return a,Mylist
################################################Vod#############################################
def get_VOD(url,Category=''):
    '''(chan_counter,name,description,piconname,stream_url,playlist_url,category_id,
                        img_src,description4playlist_html,ts_stream)'''
    a,Mylist = get_MyInfosIptv(url,Category=Category)
    return a,Mylist
################################################TV Series###############################################
def get_SERIES(url,Category=''):
    '''(chan_counter,name,description,piconname,stream_url,playlist_url,category_id,
                        img_src,description4playlist_html,ts_stream)'''
    a,Mylist = get_MyInfosIptv(url,Category=Category)
    return a,Mylist