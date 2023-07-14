#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests,re,json,zlib,base64
########################################################################
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore',InsecureRequestWarning)
########################################################################
import requests,re,json,time
St = requests.Session()
token = 'k_7nggq46b'
Api_search = 'https://imdb-api.com/en/API/SearchMovie/%s/%s'
Api_Trailer= 'https://imdb-api.com/en/API/Trailer/%s/%s'
Api_Trailer_Youtub= 'https://imdb-api.com/API/YouTube/%s/%s'
class Imdb_Suptvod():
    def __init__(self,search=None):
        self.Token = token
        self.Search= search
        self.ListImdb = []
    def Headers(self):
        self.headers={'Host': 'imdb-api.com',
                      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
                      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                      'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
                      'Accept-Encoding': 'gzip, deflate',
                      'Connection': 'keep-alive'}
        return self.headers
    def get_search(self):
        url = Api_search % (self.Token,self.Search)
        try:
            data = St.get(url,verify=False,headers = self.Headers(),timeout=10).json()
        except:data=''
        if data!=0:
            _dat = data['results']
            for items in _dat:
                image = items['image']
                title = items['title']
                _id = items['id']
                description = items['description']
                self.ListImdb.append((title,image,_id,description))
            return True,self.ListImdb
        else:return True,self.ListImdb
    def get_Trailer(self,_id):
        url = Api_Trailer % (self.Token,_id)
        try:
            data = St.get(url,verify=False,headers = self.Headers(),timeout=10).json()
        except:data=''
        if data!='':
            try:
                return True,data['linkEmbed']
            except:return False,'nada'
        else:return False,'nada'
    def get_Trailer_Videos(self,url):
        try:
            data = St.get(url,verify=False,timeout=10).content
        except:data=''
        if data!='':
            try:
                regx = '''"videoUrl"\:"(.+?)"'''
                Videos = re.findall(regx,data)
                return True,Videos
            except:return False,'nada'
        else:return False,'nada'
    def get_Trailer_Videos_Youtub(self,_id):
        self.Mylist_youtub = []
        url = Api_Trailer_Youtub %(self.Token,_id)
        try:
            data = St.get(url,verify=False,timeout=10).json()
        except:data=''
        if data!='':
            title = data['title']
            description = data['description'].replace('\r\n\r\n','\n')
            duration = data['duration']
            uploadDate = data['uploadDate']
            image = data['image']
            try:
                Videos = data['videos']
                for items in Videos:
                    quality   = items['quality']
                    extension = items['extension']
                    url = items['url']
                    Qlt = str(quality) + '__' + str(extension) 
                    self.Mylist_youtub.append((title,Qlt,url,description,duration,uploadDate,image))
                return True,self.Mylist_youtub
            except:return False,self.Mylist_youtub
        else:return False,self.Mylist_youtub
def get_Mysearch():                
    a,Mylist = Imdb_Suptvod('equalizer').get_search()
    if a:
        for X in Mylist:
            print X[0]
            print X[1]
            print X[2]
            b,link_trailer = Imdb_Suptvod().get_Trailer(X[2])
            if b:
                print "-------------",Imdb_Suptvod().get_Trailer_Videos(link_trailer)
            print X[3]
            print "======================="
def get_Myvideos():
    print Imdb_Suptvod().get_Trailer_Videos_Youtub('8hP9D6kZseM')
print get_Myvideos()
