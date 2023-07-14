#!/usr/bin/python
# -*- coding: utf-8 -*-
################################### modified by aime_jeux ##################################
#############                           Aout 2021                              #############
############################################################################################
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
############################################################################################## platform
os_platform = sys.platform
print 'os_platform = ',os_platform
if os_platform == 'win32':
    Player_U_AGENT = ' :http_user-agent="Lavf/57.83.100"'
elif os_platform == 'win64':
    Player_U_AGENT = ' --http-user-agent "Kodi/18.9 (Linux; Android 7.1.1; E6633 Build/32.4.A.1.54) Android/7.1.1 Sys_CPU/armv8l App_Bitness/32 Version/18.9-(18.9.0)-Git:20201023-0655c2c718"'
else:
    Player_U_AGENT = '#User-Agent=Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 2 rev: 250 Safari/533.3'
##############################################################################################
################################ Links #######################################################
##############################################################################################
Link_0 = '/server/load.php?type=stb&action=handshake&token=&JsHttpRequest=1-xml'
Link_1 = '/portal.php?type=stb&action=handshake&JsHttpRequest=1-xml'
Link_itv_get_genres = '/server/load.php?type=itv&action=get_genres&JsHttpRequest=1-xml'
Link_stb_get_profile = '/server/load.php?type=stb&action=get_profile&JsHttpRequest=1-xml'
Link_itv_get_all_channels = '/server/load.php?type=itv&action=get_all_channels&JsHttpRequest=1-xml'
##############################################################################################
################################ End Links ###################################################
##############################################################################################
def Copy_line(what):
    Milef = 'C:/Users/f_tar/Desktop/SupTVoD/PYTHON/TestApi'
    if os.path.isfile(Milef):
        file_write = open(Milef, 'w')
        file_write.write(what)
        file_write.close()
def getMyJson(url,headers):
    r = ''
    try:
        r = St.get(url, headers=headers,verify=False)
    except:
        r = 'nada'
    if r!='nada':r.json()
    else:returnr
#################################################################################
##############################################################################################
from GetServers import get_InfosOXml_Stalker
global _InfosSrvers
_InfosSrvers = get_InfosOXml_Stalker()
from logTools import printD,printE,delLog
##################################################
def json_request(url,headers,params,method):
    T = ''
    try:
        if method=='POST':
            r = requests.post(url, headers=headers,json=params,verify=False,timeout=10)
            T = r.json()
        else:
            r = requests.get(url, headers=headers,verify=False,timeout=10)
            T = r.json()
    except:
        T =''
    if T!='':return True,T
    else:return False,''
##################################################
def get_token(bhst,ck):
    token = ''
    try:
        HDR={'User-Agent': 'Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 2 rev: 250 Safari/533.3',
             'Accept-Charset': 'UTF-8,*;q=0.8',
             'Referrer': bhst+'/c/',
             'Cookie':ck,
             'X-User-Agent':'Model: MAG250; Link: WiFi',
             'Accept': '*/*',
             'Accept-Encoding': 'gzip'}
        jsdata_=Link_0
        a,jsdata=json_request(bhst+jsdata_,HDR,'','GET')
        if a:
            token=jsdata['js']['token']
    except:
        token = ''
    if token!='':return True,token
    else:return False,token
##################################################### get_headers
def Get_HDR(bhst,tkn,ck):
    HDR_GNR={'User-Agent': 'Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 2 rev: 250 Safari/533.3',
             'Referrer': bhst+'/c/',
             'X-User-Agent':'Model: MAG250; Link: WiFi',
             'Authorization': 'Bearer %s'%tkn,
             'Cookie': ck,
             'Accept-Encoding': 'gzip'}
    return HDR_GNR
##################################################
#from Plugins.Extensions.SupTVoDNeW.OutilsSup.Stalker.thrTools import thrTools
class Stalker_New():
    def __init__(self):
        self.Loading = 'Loading  ...... List Live TV %s.. ' % 'Please wait'
        self.MyDict = {}
        self.stalker_list = []
        self.Iptv_list = []
        self.Stalker_list_Catgt = []
        self.genres_ITV_List = []
        self._InfosSrvers = _InfosSrvers
        self.MyListIptV = []
        self.MyListIptV_1 = []
        self.MyListIptV_2 = []
        self.MyListIptV_3 = []
        self.MyListIptV_Videos = []
        self.MyList_Stalk_Iptv = []
        self.MyList_Stalk_Temp = []
        self._Headers = {'User-Agent': 'Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 2 rev: 250 Safari/533.3',
                         'Cookie': 'mac=00:1A:79:0D:1F:49; stb_lang=en; timezone=Europe/Amsterdam;'}
        #############################
        self.Host = ''
        self.Mac = ''
        self.token = ''
        self.timezone = ''
        self.lang = ''
        self.Wvalue = False
        #############################
    def get_Stalker(self):# get stalker_list
        self.stalker_list = []
        self.stalker_list=self._InfosSrvers
        self.stalker_list = self.stalker_list[1]
        return self.stalker_list
    def get_Stalker_Infos(self,indx):
        self.MyDict = {}
        self.get_Stalker()
        self.stalker_list[indx]
        print self.stalker_list[indx]
        self.prot = self.stalker_list[indx][1].split('://')[0]
        print self.prot
        self.host = self.stalker_list[indx][1].split('//')[1]
        print self.host
        self.mac = self.stalker_list[indx][2]
        print self.mac
        self.mac = 'mac='+self.mac.replace(':','%3A')+"; stb_lang=en; timezone=Europe%2FParis"
        print self.mac
        self.prothost = self.prot+'://'+self.host
        self.MyDict['prot']= self.prot
        self.MyDict['host']= self.host
        self.MyDict['prothost']= self.prothost
        self.MyDict['mac']= self.mac
        printD('get_Stalker_Infos','MyDict='+str(self.MyDict))
        return self.MyDict
    def _Host_Mac_Head_Stalker(self):
        self.Host=self.MyDict['prothost']
        self.Mac = self.MyDict['mac']
        self._Headers.update({'Cookie': self.Mac+'; stb_lang=en; timezone=Europe/Amsterdam;'})
        lnk = self.MyDict['prothost']+Link_1
        try:
            data = St.get(lnk,headers=self._Headers,verify=False).json()
            self.token = data['js']['token']
            self._Headers.update({'Authorization': 'Bearer '+self.token})
        except:
            self.token = 'nada'
        printD('_Host_Mac_Head_Stalker','token='+str(self.token))
        if self.token!='nada':
            self.MyDict['token']=self.token
            return True,self.MyDict
        else:
            self.MyDict['token']=''
            return False,self.MyDict
#################################################################################################### TV
    def _List_IPTV(self):# get_list_iptv
        self.MyListIptV_1 = []
        srv_gnr_lst = Link_itv_get_genres
        api          = self.MyDict['prothost']
        token        = self.MyDict['token']
        mac          = self.MyDict['mac']
        HDR_GNR=Get_HDR(api,token,mac)
        a,jsdata=json_request(api+Link_stb_get_profile,HDR_GNR,'','GET')#test
        if a:
            try:zone = jsdata['js']['default_timezone'].replace('/','%2F')
            except:zone=''
            if zone!='':
                mac = mac.replace('timezone=Europe%2FParis','timezone='+zone)
                HDR_GNR.update({'Cookie': mac})
                self.MyDict['mac']= mac
            b,jsdata=json_request(api+srv_gnr_lst,HDR_GNR,'','GET')
            if b:
                _dat = jsdata['js']
                for kesy in _dat:
                    title = kesy['title'].encode('utf-8')
                    if 'All'.lower() == title.lower():continue
                    _id = kesy['id']
                    self.MyListIptV_1.append((title,_id))
                return True,HDR_GNR,self.MyListIptV_1
            else:return False,'',self.MyListIptV_1
        else:return False,'',self.MyListIptV_1
    def _List_IPTV_Videos(self,indx,pg):#get_list_videos_iptv
        Ah = False
        jsdata_S,Total,Za = '','',''
        stream_url,HDR_GNR,self.MyList_Stalk_Iptv = '','',[]
        nwtok = Link_0
        Tkl   = '/server/load.php?type=itv&action=create_link&cmd='
        self.MyListIptV_Videos = []
        a,b,self.MyListIptV_Videos = self._List_IPTV()
        if a:
            HDR_GNR = b
            Title = self.MyListIptV_Videos[indx][0]
            _id   = self.MyListIptV_Videos[indx][1]
            hw_version_2=uuid.uuid4().hex
            random_=uuid.uuid4().hex
            api = self.MyDict['prothost']
            self.Ty = api+'/portal.php?type=itv&action=get_ordered_list&genre='+str(_id)+'&force_ch_link_check=&fav=0&sortby=number&hd=0&p='+str(pg)+'&JsHttpRequest=1-xml'
            try:Ah,jsdata_S=json_request(self.Ty,HDR_GNR,'','GET')
            except:Ah=False
            mac = self.MyDict['mac']
            v,token = get_token(api,mac)
            if v:
                HDR_GNR.update({'Authorization': u'Bearer '+str(token)})
            try:a,jsdata=json_request(api+'/server/load.php?type=stb&action=get_profile&hd=1&ver=ImageDescription: 0.2.18-r14-pub-250; ImageDate: Fri Jan 15 15:20:44 EET 2016; PORTAL version: 5.1.0; API Version: JS API version: 328; STB API version: 134; Player Engine version: 0x566&num_banks=2&sn=6379DE3CC464E&stb_type=MAG250&image_version=218&video_out=hdmi&device_id=&device_id2=&signature=&auth_second_step=1&hw_version=1.7-BD-00&not_valid_token=0&client_type=STB&hw_version_2='+hw_version_2+'&timestamp=1631982116&api_signature=263&metrics={"mac":'+mac+',"sn":"6379DE3CC464E","model":"MAG250","type":"STB","uid":"","random":'+random_+'}&JsHttpRequest=1-xml',HDR_GNR,'','GET')
            except:a=True
            if a:
                try:
                    a,jsdata=json_request(self.Ty,HDR_GNR,'','GET')
                except:a,jsdata=Ah,jsdata_S
                if not a and len(jsdata)==0:a,jsdata=True,jsdata_S
                if a:
                    try:
                        Total = jsdata['js']['total_items']
                        Az = truediv(int(Total),14)
                        Za = "%0.0f"%round(Az)#.split('.')[0]
                        print  '---------------------------------',type(Az)
                    except:
                        Total='nada'
                        Za   ='nada'
                    print 'Total = ',Total,Za
                    for item in jsdata['js']['data']:
                        if item['tv_genre_id']== _id:
                            try:sec_status=item['nginx_secure_link']
                            except:sec_status='nada'
                            title=item['name'].encode('utf-8')
                            logo =item['logo']
                            stream_url=item['cmd'].replace('ffmpeg ','')
                            if sec_status=='1' and sec_status!='nada':
                                stream_url=api+Tkl+item['cmd']+'&JsHttpRequest=1-xml'
                            else:stream_url=api+Tkl+item['cmd']+'&JsHttpRequest=1-xml'
                            self.MyList_Stalk_Iptv.append((title,logo,stream_url))
                    self.MyList_Stalk_Temp = self.MyList_Stalk_Iptv
                    return True,HDR_GNR,self.MyList_Stalk_Iptv,Total,Za
                else:return False,HDR_GNR,self.MyList_Stalk_Iptv,Total,Za
            else:return False,HDR_GNR,self.MyList_Stalk_Iptv,Total,Za
        else:return False,HDR_GNR,self.MyList_Stalk_Iptv,Total,Za
#################################################################################################### VOD
    def _List_VOD(self):# get_List_VOD
        self.MyListIptV_2 = []
        srv_gnr_lst = '/portal.php?type=vod&action=get_categories&JsHttpRequest=1-xml'#Link_itv_get_genres
        api          = self.MyDict['prothost']
        try:token        = self.MyDict['token']
        except:return False,'',self.MyListIptV_2
        mac          = self.MyDict['mac']
        HDR_GNR=Get_HDR(api,token,mac)
        a,jsdata=json_request(api+Link_stb_get_profile,HDR_GNR,'','GET')#test
        if a:
            try:zone = jsdata['js']['default_timezone'].replace('/','%2F')
            except:zone=''
            if zone!='':
                mac = mac.replace('timezone=Europe%2FParis','timezone='+zone)
                HDR_GNR.update({'Cookie': mac})
                self.MyDict['mac']= mac
            b,jsdata=json_request(api+srv_gnr_lst,HDR_GNR,'','GET')
            if b:
                _dat = jsdata['js']
                for kesy in _dat:
                    title = kesy['title'].encode('utf-8')
                    if 'All'.lower() in title.lower():continue
                    _id = kesy['id']
                    self.MyListIptV_2.append((title,_id))
                return True,HDR_GNR,self.MyListIptV_2
            else:return False,'',self.MyListIptV_2
        else:return False,'',self.MyListIptV_2
    def _List_VOD_Videos(self,indx,pg):
        ListInfosFilms = []
        MylistVod = {}
        Ah = False
        jsdata_S,Total,Za = '','',''
        stream_url,HDR_GNR,self.MyList_Stalk_Iptv_T = '','',[]
        nwtok = Link_0
        Tkl   = '/server/load.php?type=itv&action=create_link&cmd='
        self.MyListIptV_Videos = []
        a,b,self.MyListIptV_Videos = self._List_VOD()
        if a:
            HDR_GNR = b
            Title = self.MyListIptV_Videos[indx][0]
            _id   = self.MyListIptV_Videos[indx][1]
            hw_version_2=uuid.uuid4().hex
            random_=uuid.uuid4().hex
            api = self.MyDict['prothost']
            self.Ty = api+'/portal.php?type=vod&action=get_ordered_list&movie_id=0&season_id=0&episode_id=0&category=%s&fav=0&sortby=added&hd=0&not_ended=0&p=%s&JsHttpRequest=1-xml'%(str(_id),str(pg))
            try:Ah,jsdata_S=json_request(self.Ty,HDR_GNR,'','GET')
            except:Ah=False
            mac = self.MyDict['mac']
            v,token = get_token(api,mac)
            if v:
                HDR_GNR.update({'Authorization': u'Bearer '+str(token)})
            try:a,jsdata=json_request(api+'/server/load.php?type=stb&action=get_profile&hd=1&ver=ImageDescription: 0.2.18-r14-pub-250; ImageDate: Fri Jan 15 15:20:44 EET 2016; PORTAL version: 5.1.0; API Version: JS API version: 328; STB API version: 134; Player Engine version: 0x566&num_banks=2&sn=6379DE3CC464E&stb_type=MAG250&image_version=218&video_out=hdmi&device_id=&device_id2=&signature=&auth_second_step=1&hw_version=1.7-BD-00&not_valid_token=0&client_type=STB&hw_version_2='+hw_version_2+'&timestamp=1631982116&api_signature=263&metrics={"mac":'+mac+',"sn":"6379DE3CC464E","model":"MAG250","type":"STB","uid":"","random":'+random_+'}&JsHttpRequest=1-xml',HDR_GNR,'','GET')
            except:a=True
            if a:
                try:
                    a,jsdata=json_request(self.Ty,HDR_GNR,'','GET')
                except:a,jsdata=Ah,jsdata_S
                if not a and len(jsdata)==0:a,jsdata=True,jsdata_S
                if a:
                    try:
                        Total = jsdata['js']['total_items']
                        Az = truediv(int(Total),14)
                        Za = "%0.0f"%round(Az)#.split('.')[0]
                        print  '---------------------------------',type(Az)
                    except:
                        Total='nada'
                        Za   ='nada'
                    print 'Total = ',Total,Za
                    for item in jsdata['js']['data']:
                        title=item['name'].encode('utf-8')
                        logo =item['screenshot_uri']
                        stream_url=item['cmd'].replace('ffmpeg ','')
                        try:year =item['year']
                        except:year ='N/A'
                        try:rating =item['rating_imdb']
                        except:rating ='N/A'
                        try:actors =item['actors']
                        except:actors ='N/A'
                        try:added =item['added']
                        except:added ='N/A'
                        try:desc =item['description']
                        except:desc ='N/A'
                        try:director =item['director']
                        except:director ='N/A'
                        try:genres_str =item['genres_str']
                        except:genres_str ='N/A'
                        try:age =item['age']
                        except:age ='N/A'
                        stream_url=api+'/portal.php?type=vod&action=create_link&cmd=%s&series=&forced_storage=&disable_ad=0&download=0&force_ch_link_check=0&JsHttpRequest=1-xml'%item['cmd']
                        ListInfosFilms.append((rating,added,genres_str,age,director,actors,year,desc))
                        self.MyList_Stalk_Iptv_T.append((title,logo,stream_url,ListInfosFilms))
                    self.MyList_Stalk_Vod_Temp = self.MyList_Stalk_Iptv_T
                    return True,HDR_GNR,self.MyList_Stalk_Iptv_T,Total,Za
                else:return False,HDR_GNR,self.MyList_Stalk_Iptv_T,Total,Za
            else:return False,HDR_GNR,self.MyList_Stalk_Iptv_T,Total,Za
        else:return False,HDR_GNR,self.MyList_Stalk_Iptv_T,Total,Za
######################################################################################################SERIES
    def _List_SERIES(self):# get_list_iptv
        self.MyListIptV_3 = []
        api          = self.MyDict['prothost']
        token        = self.MyDict['token']
        mac          = self.MyDict['mac']
        macos = mac.split('; stb_lang')[0]
        srv_gnr_lst = '{}/portal.php?type=series&action=get_categories&JsHttpRequest=1-xml'.format(str(api))
        HDR_GNR=Get_HDR(api,token,mac)
        a,jsdata=json_request(api+Link_stb_get_profile,HDR_GNR,'','GET')#test
        if a:
            try:zone = jsdata['js']['default_timezone'].replace('/','%2F')
            except:zone=''
            if zone!='':
                mac = mac.replace('timezone=Europe%2FParis','timezone='+zone)
                HDR_GNR.update({'Cookie': mac})
                self.MyDict['mac']= mac
            b,jsdata=json_request(srv_gnr_lst,HDR_GNR,'','GET')
            if b:
                _dat = jsdata['js']
                for kesy in _dat:
                    title = kesy['title'].encode('utf-8')
                    if 'All'.lower() == title.lower():continue
                    _id = kesy['id']
                    self.MyListIptV_3.append((title,_id))
                return True,HDR_GNR,self.MyListIptV_3
            else:return False,'',self.MyListIptV_3
        else:return False,'',self.MyListIptV_3
    def _List_SERIES_Videos(self,indx,pg):#get_list_videos_iptv
        self.ListInfosFilms = []
        MylistVod = {}
        Ah = False
        jsdata_S,Total,Za,jsdata_SS = '','','',''
        stream_url,HDR_GNR,self.MyList_Stalk_Iptv_V = '','',[]
        nwtok = Link_0
        Tkl   = '/server/load.php?type=itv&action=create_link&cmd='
        self.MyListIptV_Videos = []
        a,b,self.MyListIptV_Videos = self._List_SERIES()
        print "//////////////////////////////////////////////////////////",self.MyListIptV_Videos
        if a:
            HDR_GNR = b
            Title = self.MyListIptV_Videos[indx][0]
            _id   = self.MyListIptV_Videos[indx][1]
            print '_id-- Title',_id,Title
            hw_version_2=uuid.uuid4().hex
            random_=uuid.uuid4().hex
            api = self.MyDict['prothost']
            Link_SERIES_=api+'/portal.php?type=series&action=get_ordered_list&movie_id=0&season_id=0&episode_id=0&category='+str(_id)+'&fav=0&sortby=added&hd=0&not_ended=0&p=%s&JsHttpRequest=1-xml'%str(pg)
            try:ZZ,jsdata_SS=json_request(Link_SERIES_,HDR_GNR,'','GET')
            except:ZZ=False
            self.Ty = api+'/portal.php?type=vod&action=get_ordered_list&movie_id=0&season_id=0&episode_id=0&category=%s&fav=0&sortby=added&hd=0&not_ended=0&p=%s&JsHttpRequest=1-xml'%(str(_id),str(pg))
            try:Ah,jsdata_S=json_request(self.Ty,HDR_GNR,'','GET')
            except:Ah=False
            mac = self.MyDict['mac']
            v,token = get_token(api,mac)
            if v:
                HDR_GNR.update({'Authorization': u'Bearer '+str(token)})
            try:a,jsdata=json_request(api+'/server/load.php?type=stb&action=get_profile&hd=1&ver=ImageDescription: 0.2.18-r14-pub-250; ImageDate: Fri Jan 15 15:20:44 EET 2016; PORTAL version: 5.1.0; API Version: JS API version: 328; STB API version: 134; Player Engine version: 0x566&num_banks=2&sn=6379DE3CC464E&stb_type=MAG250&image_version=218&video_out=hdmi&device_id=&device_id2=&signature=&auth_second_step=1&hw_version=1.7-BD-00&not_valid_token=0&client_type=STB&hw_version_2='+hw_version_2+'&timestamp=1631982116&api_signature=263&metrics={"mac":'+mac+',"sn":"6379DE3CC464E","model":"MAG250","type":"STB","uid":"","random":'+random_+'}&JsHttpRequest=1-xml',HDR_GNR,'','GET')
            except:a=True
            if a:
                try:
                    Link_SERIES_='/portal.php?type=series&action=get_ordered_list&movie_id=0&season_id=0&episode_id=0&category='+str(_id)+'&fav=0&sortby=added&hd=0&not_ended=0&p='+str(pg)+'&JsHttpRequest=1-xml'
                    a,jsdata=json_request(api+Link_SERIES_,HDR_GNR,'','GET')
                except:a,jsdata=Ah,jsdata_S
                if not a and len(jsdata)==0:a,jsdata=True,jsdata_S
                if a:
                    try:
                        Total = jsdata['js']['total_items']
                        Az = truediv(int(Total),14)
                        Za = "%0.0f"%round(Az)#.split('.')[0]
                        print  '---------------------------------',type(Az)
                    except:
                        Total='nada'
                        Za   ='nada'
                    print 'Total = ',Total,Za
                    if Total == 0:
                        jsdata =jsdata_SS
                        try:
                            Total = jsdata_SS['js']['total_items']
                            Az = truediv(int(Total),14)
                            Za = "%0.0f"%round(Az)#.split('.')[0]
                            print  '---------------------------------',type(Az)
                        except:
                            Total='nada'
                            Za   ='nada'
                    print 'Total = ',Total,Za
                    for item in jsdata['js']['data']:
                        serie_id=item['id']
                        print "----------------------",serie_id
                        title=item['name'].encode('utf-8')
                        logo =item['screenshot_uri']
                        stream_url=item['cmd'].replace('ffmpeg ','')
                        try:year =item['year']
                        except:year ='N/A'
                        try:rating =item['rating_imdb']
                        except:rating ='N/A'
                        try:actors =item['actors']
                        except:actors ='N/A'
                        try:added =item['added']
                        except:added ='N/A'
                        try:desc =item['description']
                        except:desc ='N/A'
                        try:director =item['director']
                        except:director ='N/A'
                        try:genres_str =item['genres_str']
                        except:genres_str ='N/A'
                        try:age =item['age']
                        except:age ='N/A'
                        stream_url=api+'/portal.php?type=series&action=get_ordered_list&movie_id=%s&season_id=0&episode_id=0&category=%s&fav=0&sortby=added&hd=0&not_ended=0&p=1&JsHttpRequest=1-xml'%(serie_id,_id)
                        self.ListInfosFilms.append((rating,added,genres_str,age,director,actors,year,desc))
                        self.MyList_Stalk_Iptv_V.append((title,logo,stream_url,self.ListInfosFilms))
                    self.MyList_Stalk_Vod_Temp = self.MyList_Stalk_Iptv_V
                    return True,HDR_GNR,self.MyList_Stalk_Iptv_V,Total,Za
                else:return False,HDR_GNR,self.MyList_Stalk_Iptv_V,Total,Za
            else:return False,HDR_GNR,self.MyList_Stalk_Iptv_V,Total,Za
        else:return False,HDR_GNR,self.MyList_Stalk_Iptv_V,Total,Za
    def _List_SERIES_Episodes(self,url):#get_list_videos_iptv
        self.ListInfosFilms_1 = []
        MylistVod = {}
        Ah = False
        jsdata_S,Total,Za = '','',''
        stream_url,HDR_GNR,self.MyList_Stalk_Iptv = '','',[]
        nwtok = Link_0
        Tkl   = '/server/load.php?type=itv&action=create_link&cmd='
        self.MyListIptV_Videos = []
        a,b,self.MyListIptV_Videos = self._List_SERIES()
        api = self.MyDict['prothost']
        mac = self.MyDict['mac']
        v,token = get_token(api,mac)
        HDR_GNR=Get_HDR(api,token,mac)
        jsdata_=json_request(api+'/server/load.php?type=stb&action=get_profile&JsHttpRequest=1-xml',HDR_GNR,'','GET')
        try:Ah,jsdata_S=json_request(url,HDR_GNR,'','GET')
        except:Ah=False
        if Ah:
            for item in jsdata_S['js']['data']:
                cmd_url=''
                season=item['name'].encode('utf-8')
                poster=item['screenshot_uri']
                cmd_url=item['cmd']
                episodes=item['series']
                self.ListInfosFilms_1.append((season,poster,cmd_url,episodes))
                self.ListInfosFilms_1.reverse()
            return True,self.ListInfosFilms_1
        return False,[]
    def _List_SERIES_Season(self,url):#get_list_videos_iptv
        self.ListInfosFilms_2 = []
        MylistVod = {}
        Ah = False
        jsdata_S,Total,Za = '','',''
        stream_url,HDR_GNR,self.MyList_Stalk_Iptv = '','',[]
        nwtok = Link_0
        Tkl   = '/server/load.php?type=itv&action=create_link&cmd='
        self.MyListIptV_Videos = []
        a,b,self.MyListIptV_Videos = self._List_SERIES()
        api = self.MyDict['prothost']
        mac = self.MyDict['mac']
        v,token = get_token(api,mac)
        HDR_GNR=Get_HDR(api,token,mac)
        try:Ah,jsdata_S=json_request(url,HDR_GNR,'','GET')
        except:Ah=False
        if Ah:
            for item in jsdata_S['js']['data']:
                cmd_url=''
                season=item['name'].encode('utf-8')
                poster=item['screenshot_uri']
                cmd_url=item['cmd']
                episodes=item['series']
                self.ListInfosFilms_2.append((season,poster,cmd_url,episodes))
                self.ListInfosFilms_2.reverse()
            return True,self.ListInfosFilms_2
        return False,[]
###################################################################################################### Get Links
    def getLinks(self,url):#
        url      = url
        print "url ===========",url
        api = self.MyDict['prothost']
        mac = self.MyDict['mac']
        v,token = get_token(api,mac)
        HDR_GNR=Get_HDR(api,token,mac)
        print 'HDR_GNR_ = ',HDR_GNR
        jsdata=json_request(api+Link_stb_get_profile,HDR_GNR,'','GET')##testing
        a,jsdata=json_request(url,HDR_GNR,'','GET')
        if a:
            stream_url=jsdata['js']['cmd'].replace('hffmpeg ','')
            stream_url=jsdata['js']['cmd'].replace('ffmpeg ','').replace('ffmpeg ', '').encode('ascii', 'ignore').decode('ascii')
            stream_url =stream_url+Player_U_AGENT
            return True,stream_url
        else:return False,''
################################################################################# Test
def get_donnees_Stalker_New(indx,_list=None,stream=None,pg=None,indxstream=None,mode='',url=None):
    Cp = Stalker_New()
    a,head,listos,Total,Za = '','','','',''
    mode = mode
    indx = indx
    def get_donnes():
        print Cp.get_Stalker_Infos(indx)
    get_donnes()
    Cp._Host_Mac_Head_Stalker()
    if _list:
        listos = []
        
        if mode == 'TV':a,head,listos = Cp._List_IPTV()
        elif mode == 'VOD':a,head,listos = Cp._List_VOD()
        else:a,head,listos = Cp._List_SERIES()
        if a:return True,listos
        else:return False,''
    if stream:
        listos = []
        #get_donnes()
        if mode == 'TV':a,head,listos,Total,Za = Cp._List_IPTV_Videos(int(stream),pg)
        elif mode == 'VOD':a,head,listos,Total,Za = Cp._List_VOD_Videos(int(stream),pg)
        else:a,head,listos,Total,Za = Cp._List_SERIES_Videos(int(stream),pg)
        if a:return True,listos,Total#,Za
        else:return False,'',Total
################################################
    if url:
        listos = []
        #get_donnes()
        if mode == 'SERIES':a,listos = Cp._List_SERIES_Episodes(url)
        if a:return True,listos
        else:return False,''
    if indxstream:
        #get_donnes()
        printD('get_donnees_Stalker_New_indxstream','indxstream='+str(indxstream))
        a,stream_url = Cp.getLinks(indxstream)
        if a:
            printD('get_donnees_Stalker_New_indxstream','a='+str(a))
            return a,stream_url
        else:
            printD('get_donnees_Stalker_New_indxstream','a='+str(a))
            return False,''
####################################################################################################### TV SHOW
#tek = 'http://portal.geniptv.com:8080/portal.php?type=series&action=get_ordered_list&movie_id=261&season_id=0&episode_id=0&category=775&fav=0&sortby=added&hd=0&not_ended=0&p=1&JsHttpRequest=1-xml'
#rty = 'http://portal.geniptv.com:8080/portal.php?type=vod&action=create_link&cmd=eyJzZXJpZXNfaWQiOjI2MSwic2Vhc29uX251bSI6NCwidHlwZSI6InNlcmllcyJ9&series=13&forced_storage=&disable_ad=0&download=0&force_ch_link_check=0&JsHttpRequest=1-xml'
#print get_donnees_Stalker_New(0,_list='list',mode='SERIES')
#print get_donnees_Stalker_New(0,stream=1,pg=1,mode='SERIES')
#print get_donnees_Stalker_New(0,mode='SERIES',url=tek)
#print get_donnees_Stalker_New(0,indxstream=rty)