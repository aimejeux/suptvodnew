#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests,re,json,zlib,base64,time,shutil,os
from Tools.BoundFunction import boundFunction
from Components.Pixmap import Pixmap
from Components.AVSwitch import AVSwitch
from enigma import ePoint, eSize, eTimer,ePicLoad
from skin import parseColor, parseFont
from Components.Sources.StaticText import StaticText
from twisted.web.client import downloadPage
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.Label import Label
from Components.ActionMap import ActionMap, HelpableActionMap, NumberActionMap
from Tools.Directories import fileExists
########################################################################
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore',InsecureRequestWarning)
########################################################################
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Sptvnw.Setup import get_Tmdbvalue,SupTVoDNeW_Config,get_Posters,get_TMDB
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Sptvnw.MesImports import MesImports
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Sptvnw.Config import *
from Plugins.Extensions.SupTVoDNeW.plugin import return_version
########################################################################
from enigma import getDesktop
dwidth = getDesktop(0).size().width()
PLUGIN_PATH = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW'
PATH_SKINS  = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/OutilsSup/Tmdb'
St = requests.Session()
'''original_title,Movies,Img,media_type,original_language,vote_average,vote_count,overview'''
URLS = {'movie': '/movie','collection': '/collection','tv': '/tv',
        'person': '/person','company': '/company','keyword': '/keyword','multi': '/multi'}
class Screen_MyTMDB_SupTvod(Screen):
    def __init__(self, session,name_title):
        ########################Session_Skin############################
        if dwidth == 1280:
            with open(PATH_SKINS + '/MyTMDB_SupTvod.xml', 'r') as f:
                self.skin = f.read()
                f.close()
        else:
            with open(PATH_SKINS + '/MyTMDB_SupTvod.xml', 'r') as f:
                self.skin = f.read()
                f.close()
        self.session = session
        Screen.__init__(self, session)
        self['actions'] = ActionMap(['DirectionActions','SetupActions','ColorActions'], {
            'cancel': self.Exit_plug,
            'red': self.Exit_plug,
            'green': self.ok,
            'blue': self.show_hide_menu,
            'yellow': self.Settings,
            'up': self.keyUp,
            'down': self.keyDown,
            'left': self.left,
            'right': self.right
            }, -1)
        self.initialservice = self.session.nav.getCurrentlyPlayingServiceReference()
        self.onShown.append(self.show_all_chang)
        self.name_title = name_title
        self['Titlet'] = Label()
        self['Infos'] = Label()
        self['Data'] = Label()
        self['ttltrailer'] = Label()
        self['Searchlang'] = Label()
        self['ttltrailer'].hide()
        self.picfile = ''
        self['Titlet'].setText('TMDB')
        self.timer = eTimer()
        self.showhide = False
        self.hidden = False
        self.TrailerCond = False
        self['rating'] =StaticText()
        for x in range(9):
            if x!=8:self['TxT_'+str(x)] = Label()
            else:self['TxT_'+str(x)] = StaticText()
        self.picfile = ''
        self['poster'] = Pixmap()
        self['poster'].hide()
        self.picload = ePicLoad()
        self['Version'] = Label(_(return_version()))
        # self.a,self.b = get_TMDB()
        # self.b = MesImports()._colorize_('search language == '+self.b,selcolor='cyan')
        # self['Searchlang'] = Label(_(self.b))
        self['menu'] = m2list([])
        self['menuTrailer'] = m2list([])
        self['menu'].hide()
        self['menuTrailer'].hide()
        self.Fix_Infos()
    def Settings(self):
        self.session.open(SupTVoDNeW_Config)
    def show_all_chang(self):
        if get_Tmdbvalue() == 'enabled':
            self.lang=get_TMDB()[1]
        else:self.lang='fr'
        a = Tmdb_Suptvod(searchtitle=self.name_title,lang=self.lang).get_infos_search()
        if a:
            self.TrailerCond = False
            self.Fix_Infos()
        else:
            self.session.open(MessageBox, 'Unsuccessful Research', MessageBox.TYPE_INFO)
            self.close()
    def Fix_Infos(self):
        self.MyNewlist = []
        self.MyNewlist = Tmdb_Suptvod().Ready_Js()
        self.b = get_TMDB()[1]
        self.b = MesImports()._colorize_('search language == '+self.b,selcolor='cyan')
        self['Searchlang'].setText(self.b)
        self.get_ListIptvFnl()
    def Exit_plug(self):
        if self.TrailerCond:
            self['menuTrailer'].hide()
            self['menuTrailer'].selectionEnabled(0)
            self.currentList = 'menu'
            self['menu'].show()
            self['menu'].selectionEnabled(1)
            self['ttltrailer'].hide()
            self.TrailerCond = False
        else:self.close()
    def get_ListIptvFnl(self):
        #self.timer.stop()
        self['menu'].show()
        self['menu'].l.setList(self.MyNewlist)
        self['menu'].l.setItemHeight(37)
        self.currentList = 'menu'
        self['menu'].selectionEnabled(1)
        self['menuTrailer'].hide()
        self['menuTrailer'].selectionEnabled(0)
        self['Infos'].setText(self['menu'].getCurrent()[0][0])
        data = MesImports()._colorize_('Data Found == '+str(len(self.MyNewlist)),selcolor='cyan')
        self['Data'].setText(data)
        self.Get_Infos_select()
    def get_Trailer(self):
        self.Trailer = self['menu'].getCurrent()[0][9].encode('utf-8')
        if self.Trailer!='' and self.Trailer!='N/A':
            a,self.link = Tmdb_Suptvod().get_imdb_videos(self.Trailer)
            if a:self.link = self.link
            else:self.link = '...'
        else:self.link = '...'
        return self.link
    def ok(self):
        if self.TrailerCond:self.PlayVideo_1()
        else:
            self.ListTrailer = []
            
            from Plugins.Extensions.SupTVoDNeW.OutilsSup.Tmdb.YoutubGet.YoutL import getStreams
            if self.TrailerT =='...':
                self.session.open(MessageBox,'No Youtube Link', MessageBox.TYPE_INFO,timeout=5)
                return
            try:
                if self.link!='...':
                    idyout = self.link.split('v=')[1]
                    name = self['menu'].getCurrent()[0][0].encode('utf-8')
                    self.video_url = getStreams(idyout)
                    self.ListTrailer.append(show_Menu2_IMDB(name+' [YoutL]',self.video_url))
                    self['menuTrailer'].l.setList(self.ListTrailer)
                    self['menuTrailer'].l.setItemHeight(37)
                    self.TrailerCond = True
                    self.PlayVideo()
                    return
                else:
                    try:
                        from Plugins.Extensions.SupTVoDNeW.OutilsSup import pafy
                        video = pafy.new(self.link)
                    except:video = ''
                    if video != '':
                        TiTle = video.title
                        TiTle = TiTle.encode('utf-8')
                        streams = video.streams
                        for s in streams:
                            self.Ae = s.url
                            self.Af = s.resolution
                            self.ListTrailer.append(show_Menu2_IMDB(TiTle+' ['+str(self.Af)+']',self.Ae))
                        self['menuTrailer'].l.setList(self.ListTrailer)
                        self['menuTrailer'].l.setItemHeight(37)
                        self.TrailerCond = True
                        self.PlayVideo()
                        return
                    else:
                        _id = self['menu'].getCurrent()[0][2]
                        name = self['menu'].getCurrent()[0][0].encode('utf-8')
                        if str(_id).endswith('/'):_id=str(_id).split('/')[-2]
                        else:_id=str(_id).split('/')[-1]
                        a,self.ListTrailer = Tmdb_Suptvod().get_imdb_videos_2(_id,name)
                        if a:
                            self['menuTrailer'].l.setList(self.ListTrailer)
                            self['menuTrailer'].l.setItemHeight(37)
                            self.TrailerCond = True
                            self.PlayVideo()
                            return
                    #else:
                        
                            #else:self.session.open(MessageBox,'Error_0 Import Youtube Stream\nTry Again ...', MessageBox.TYPE_INFO,timeout=5)
                        #else:self.session.open(MessageBox,'Error_1 Import Youtube Stream\nTry Again ...', MessageBox.TYPE_INFO,timeout=5)
            except:self.session.open(MessageBox,'Error__ Import Youtube Stream', MessageBox.TYPE_INFO,timeout=5)
    def PlayVideo(self):
        self['menuTrailer'].show()
        self['menuTrailer'].selectionEnabled(1)
        self.currentList = 'menuTrailer'
        self['menu'].hide()
        self['menu'].selectionEnabled(0)
        self['ttltrailer'].show()
        self['ttltrailer'].setText(self['menuTrailer'].getCurrent()[0][0])
    def PlayVideo_1(self):
        from enigma import eServiceReference
        self.rds = MesImports().get_player()
        stream_url=self['menuTrailer'].getCurrent()[0][1]
        self.reference = eServiceReference(self.rds, 0, stream_url.encode('utf-8'))
        Name = self['menuTrailer'].getCurrent()[0][0]
        self.reference.setName(Name)
        self.session.open(ServiceAppPlayer,self.reference)
    def keyDown(self):
        self[self.currentList].down()
        self['Infos'].setText(self['menu'].getCurrent()[0][0])
        self.Get_Infos_select()
    def keyUp(self):
        self[self.currentList].up()
        self.Get_Infos_select()
    def left(self):
        self[self.currentList].pageUp()
        self.Get_Infos_select()
    def right(self):
        self[self.currentList].pageDown()
        self.Get_Infos_select()
    def Get_Infos_select(self):
        if self.TrailerCond:
            #self.timer.stop()
            self['ttltrailer'].setText(self['menuTrailer'].getCurrent()[0][0])
            return
        "original_title,Movies,url_imdb,Img,media_type,original_language,vote_average,vote_count,overview"
        "_colorize_('RAT == '+str(rat),selcolor='cyan')"
        original_title = MesImports()._colorize_('Original Title == '+self['menu'].getCurrent()[0][0],selcolor='cyan')
        self['TxT_0'].setText(original_title)
        Movies = MesImports()._colorize_('url imdb == '+self['menu'].getCurrent()[0][2],selcolor='cyan')
        self['TxT_1'].setText(Movies.encode('utf-8'))
        media_type = MesImports()._colorize_('Category == '+self['menu'].getCurrent()[0][4],selcolor='cyan')
        self['TxT_2'].setText(media_type.encode('utf-8'))
        original_language = MesImports()._colorize_('Original Language == '+self['menu'].getCurrent()[0][5],selcolor='cyan')
        self['TxT_3'].setText(original_language.encode('utf-8'))
        vote_average = MesImports()._colorize_('Vote Average == '+str(self['menu'].getCurrent()[0][6]),selcolor='cyan')
        self['TxT_4'].setText(vote_average)
        vote_count = MesImports()._colorize_('Vote Count == '+str(self['menu'].getCurrent()[0][7]),selcolor='cyan')
        self['TxT_5'].setText(vote_count)
        overview = MesImports()._colorize_('Discription == '+self['menu'].getCurrent()[0][8],selcolor='cyan')
        self['TxT_8'].setText(overview)
        Rating = self['menu'].getCurrent()[0][6]
        if Rating!='N/A':self['rating'].setText(str(Rating))
        else:self['rating'].setText('1')
        self.TrailerT = self.get_Trailer()
        self.TrailerT = MesImports()._colorize_('Trailer == '+self.TrailerT,selcolor='cyan')
        self['TxT_6'].setText(self.TrailerT)
        #self.timer.stop()
        self.Download_Image()
    #################################################### Image
    def Copy_Donnees(self,what):
        Milef = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/Cfg/foldImag'
        if os.path.isfile(Milef):
            file_write = open(Milef, 'w')
            file_write.write(str(what))
            file_write.close()
    def image_downloaded(self):
        if 'None' in self.picfile:
            os.remove(self.picfile)
            self.picfile = PLUGIN_PATH + '/img/playlist/tmdb_default.png'
        elif self.picfile==get_Posters():
            self.picfile = PLUGIN_PATH + '/img/playlist/tmdb_default.png'
        else:
            self.picfile = self.picfile
        return self.picfile
    def Download_Image(self):
        img = self['menu'].getCurrent()[0][3].encode('utf-8').replace('https','http')
        MesImports().Download_Image(img,self['poster'])
    def show_hide_menu(self):
        if not self.showhide:
            if self.hidden:
                self.show()
            else:
                self.hide()
            self.hidden = not self.hidden
from Screens.InfoBar import InfoBar, MoviePlayer
class ServiceAppPlayer(MoviePlayer):
    def __init__(self, session, service):
        MoviePlayer.__init__(self, session, service)
        self.skinName = ["ServiceAppPlayer", "MoviePlayer"]
        self.servicelist = InfoBar.instance and InfoBar.instance.servicelist
    def handleLeave(self, how):
        if how == "ask":
            self.session.openWithCallback(self.leavePlayerConfirmed,MessageBox, _("Stop playing this movie?"))
        else:
            self.close()
    def leavePlayerConfirmed(self, answer):
        if answer:
            self.close()
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Stalker.logTools import printD,printE,delLog
class Tmdb_Suptvod():
    def __init__(self,searchtitle=None,token=None,lang=None):
        self.MyList_donnees = []
        self.Loading = 'Loading  ...... List Live TV %s.. ' % 'Please wait'
        self.apikey_imdb = 'k_7nggq46b'
        self.Mytoken = token
        self.lang = lang
        self.token = "69c14667145c334b46692cda360a29dd"#"ZUp6enk4cko4ZzBKTlBMTFNxN3djd25MOHEzeU5Zak1Bdkd6S3lPTmdqSjhxeUxMSTBNOFRhUGNBMjBCVmxBTzlBPT0K"
        self.searchtitle = searchtitle
        if searchtitle:self.correct_search()
    def get_correct_name(self,txt):
        txt = re.sub("[\(\[].*?[\)\]]", "", txt)#suprim entre parenth
        txt = re.sub(r"\b\d+\b", "", txt).strip()#suprim int
        txt = txt.replace('  ','')
        txt = txt.replace('FR - ','')
        txt = txt.replace('FR -','').replace('TOP-','').replace('S01','')
        return txt
    def correct_search(self):
        self.searchtitle = self.get_correct_name(self.searchtitle)
        self.searchtitle = self.searchtitle.replace(' ','+').replace(':','%3A')
        self.searchurl = 'http://api.themoviedb.org/3/search/multi?api_key=' + str(self.token) + '&query=%22' + str(self.searchtitle) + '%22&language='+self.lang+'&page=1&include_adult=false&'
    def check(self):
        result = base64.b64decode(self.token)
        result = zlib.decompress(base64.b64decode(result))
        result = base64.b64decode(result).decode()
        return result
    def decheck(self):
        result = base64.b64encode(self.token)
        result = zlib.compress(result)
        result = base64.b64encode(result)
        result = base64.b64encode(result)
        return result
    def Ready_Js(self):
        '''(original_title,Movies,url_imdb,Img,media_type,original_language,vote_average,vote_count,overview)'''#
        self.MyList_donnees = []
        path = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/OutilsSup/Tmdb/themoviedb.js'
        i = 0
        with open(path) as jsf:
            urljsdata=json.load(jsf)
        d = len(urljsdata)
        # print type(urljsdata['1'])
        # print len(urljsdata['1'])
        if d == 0:
            self.MyList_donnees.append(show_Menu_IMDB('Not Found','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A'))
            return self.MyList_donnees
        for h in range(d):
            for name in urljsdata[str(h)]:
                original_title = name[0].encode('utf-8')
                Movies = name[1]
                url_imdb = name[2]
                Img = name[3]
                media_type = name[4]
                original_language = name[5]
                vote_average = name[6]
                vote_count = name[7]
                overview = name[8].encode('utf-8')
                Trailer = name[9].encode('utf-8')
                self.MyList_donnees.append(show_Menu_IMDB(original_title,Movies,url_imdb,Img,media_type,original_language,vote_average,vote_count,overview,Trailer))
        return self.MyList_donnees
    def Write_Js(self,txt):
        path = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/OutilsSup/Tmdb/themoviedb.js'
        with open(path,'w') as chcfg:
            json.dump(txt, chcfg,ensure_ascii=True)
        print "OK"
    def get_imdb_search(self,lnk):
        url_imdb = ''
        try:
            data = St.get(lnk,verify=False).json()
            imdb = data['imdb_id']
            if 'tt' in imdb:url_imdb = "https://www.imdb.com/title/%s/" % imdb
            if 'nm' in imdb:url_imdb = "https://www.imdb.com/name/%s/" % imdb
            return url_imdb
        except:return '....'
    #Dogface%3A+A+TrapHouse+Horror    
    def get_infos_search(self):
        MyList = []
        MyDict = {}
        searchresult = {}
        printD('self.searchurl======================= '+str(self.searchurl))
        try:
            data = St.get(self.searchurl,verify=False).content
            searchresult = json.loads(data)
        except:searchresult={}
        if len(searchresult)==0:
            MyDict[str(0)] = MyList.append(show_Menu_IMDB('Not Found','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A'))
            self.Write_Js(MyDict)
            return False
        print type(searchresult)
        Xx = len(searchresult['results'])
        for u in range(Xx):
            exec 'MyList_'+str(u)+' = []'
        i = 0
        for keys in searchresult['results']:
            try:original_title = keys['original_title'].encode('utf-8')
            except:original_title = keys['name']
            try:id_= keys['id']
            except:id_=''
            try:media_type = keys['media_type']
            except:media_type=''
            try:original_language = keys['original_language']
            except:original_language=''
            try:overview = keys['overview'].encode('utf-8')
            except:overview='...'
            if media_type!='':
                Movies     = "https://api.themoviedb.org/3/"+str(media_type)+"/"+str(id_)+"?api_key=" + str(self.token) + "&language="+self.lang
                url_imdb   = self.get_imdb_search(Movies)
            else:Movies,url_imdb='',''
            try:poster_path = keys['poster_path']
            except:
                try:poster_path = keys['backdrop_path']
                except:poster_path=''
            try:vote_average = keys['vote_average']
            except:vote_average='N/A'
            try:vote_count  = keys['vote_count']
            except:vote_count='N/A'
            if poster_path!='':
                Img = 'https://www.themoviedb.org/t/p/w600_and_h900_bestv2'+str(poster_path)
            else:Img=''
            try:Trailer = "https://api.themoviedb.org/3/movie/"+str(id_)+"/videos?api_key="+str(self.token)+"&language="+original_language
            except:Trailer=''
            exec 'MyList_'+str(i)+'.append((original_title,Movies,url_imdb,Img,media_type,original_language,vote_average,vote_count,overview,Trailer))'
            exec 'MyDict[str(i)] = MyList_'+str(i)
            i = i + 1
        self.Write_Js(MyDict)
        return True
    def get_imdb_videos(self,lnk):
        Trailer = ''
        try:
            data = St.get(lnk,verify=False, timeout=10).json()
            _Dats = data['results'][0]
            site = _Dats['site']
            key  = _Dats['key']
            if 'youtub' in site.lower():
                Trailer = "https://www.youtube.com/watch?v="+str(key)
                return True,Trailer
            else:return False,''
        except:return False,''
    def get_imdb_videos_2(self,_id,name):
        self.Trailer = []
        link1 = 'https://imdb-api.com/en/API/YouTubeTrailer/'+self.apikey_imdb+'/'+_id
        print link1
        lnk = 'https://imdb-api.com/en/API/YouTube/'+self.apikey_imdb+'/%s'
        try:
            data = St.get(link1,verify=False, timeout=10).json()
            _Dats = data['videoId']
            print _Dats
            lnk = lnk %_Dats
            print "----",lnk
            data1 = St.get(lnk,verify=False, timeout=10).json()
            _dat2 = data1['videos']
            print _dat2
            print "*************************************************"
            for items in _dat2:
                print "================================",items
                quality = items['quality']
                print 'quality = ',quality
                url  = items['url']
                print 'url = ',url
                self.Trailer.append(show_Menu_IMDB(name+'  IMDB ['+str(quality)+']',url,'N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A'))
            return True,self.Trailer
        except:return False,self.Trailer	