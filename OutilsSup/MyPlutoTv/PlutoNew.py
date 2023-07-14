#!/usr/bin/python
# -*- coding: utf-8 -*-
################################### modified by aime_jeux ##################################
#############                           Aout 2021                              #############
############################################################################################
from Components.config import config
from time import gmtime, localtime, strftime, time

from Components.Sources.StaticText import StaticText
from enigma import eServiceReference
from enigma import ePoint, eSize, eTimer
from enigma import eTimer,ePicLoad
from Components.AVSwitch import AVSwitch
from twisted.web.client import downloadPage
from Tools.BoundFunction import boundFunction
import os,sys,time
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.Label import Label
from Components.ActionMap import ActionMap, HelpableActionMap, NumberActionMap
from Components.Pixmap import Pixmap
###########################################################################################
from Plugins.Extensions.SupTVoDNeW.OutilsSup.MyPlutoTv.plutoimport import PlutotvNew
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Sptvnw.MesImports import MesImports
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Sptvnw.Config import *
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Sptvnw.Setup import *
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Sptvnw.Setup import SupTVoDNeW_Config
Version = 'SupTVoDNeW V_1.0'
PATH_SKINS = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/Skins'
PLUGIN_PATH = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW'
###########################################################################################
from enigma import getDesktop
dwidth = getDesktop(0).size().width()
global Lis_Clean
Lis_Clean_0 = ['isra','israel','adult','adulte','adults','xxx','xx','porn','18','hard','sex',
               'hard','ado','blowjob','lesbie','travest','anal','frisson']
Lis_Clean_1 = ['sex','xxl','hotclub','venus','playb','hust','libid','penthouse','spice','platinum','amatix','xx',
               'vivid','brazzers','colmax','daring','lover','man-x','man x','manx','pink_x','pink-x','pink x','pinkx','reality kings','stars xxx',
               'pink show','pink-show','pink_show','pinkshow','porn','brazz','lov','adult','hust','candy']
Lis_Clean = Lis_Clean_0+Lis_Clean_1
###########################################################################################
####################################### Menu Servers ######################################
###########################################################################################
from datetime import datetime
def get_Loading():
    T = 'Loading  ...... List Live TV %s.. ' % 'Please wait'
    return True,T
def log(data):
	now = datetime.now().strftime('%Y-%m-%d %H:%M')
	open('/tmp/SupTVoDNeW.log', 'a').write(now+' : '+str(data)+'\r\n')
class Screen_MyPlutoTvNew(Screen):
    def __init__(self, session):
        ########################Session_Skin############################
        if dwidth == 1280:
            with open(PATH_SKINS + '/PlutoTv_FHD.xml', 'r') as f:
                self.skin = f.read()
                f.close()
        else:
            with open(PATH_SKINS + '/PlutoTv_FHD.xml', 'r') as f:
                self.skin = f.read()
                f.close()
        self.session = session
        Screen.__init__(self, session)
        self['actions'] = ActionMap(['DirectionActions','SetupActions','ColorActions'], {'ok': self.ok,
            'cancel': self.Exit_plug,
            'red': self.Exit_plug,
            #'1': self.show_all_chang,
            'yellow': self.Settings,
            #'blue': self.get_categorie_select,
            'green': self.ok,
            'up': self.keyUp,
            'down': self.keyDown,
            'left': self.left,
            'right': self.right
            }, -1)
        self.proxyvalue = config.plugins.SupTVoDNeWConfig.Plutotv.value
        self.initialservice = self.session.nav.getCurrentlyPlayingServiceReference()
        self.onShown.append(self.show_all_chang)
        self['Infos'] = Label()
        self['Title'] = Label()
        self['Infoselect'] = Label()
        self['myproxy'] = Label()
        self['menu_Plutotv'] = m2list([])
        self['menu_list_catego'] = m2list([])
        self['menu_list_catego'].hide()
        self.Chouf,self.Mylist,self.Mydict = [],[],{}
        self['poster'] = Pixmap()
        self.picload = ePicLoad()
        self.imports = False
        self.secondlist = False
        self.TXT = ''
        self.idx = 0
        for x in range(5):
            if x == 0:self['Info_'+str(x)] =StaticText()
            else:self['Info_'+str(x)] = Label()
        self.get_ListIptvFnl()
    def get_ListIptvFnl(self):
        self.Mylist,self.Mydict = [],{}
        a,self.Mylist,self.Mydict =  PlutotvNew(self.proxyvalue).Categories_list_Pluto()
        if a:
            self.Mylist = self.Mylist
            self.Mydict = self.Mydict
            self.imports = True
        else:
            self.Mylist.append(show_Menu_PlutoTv('Not Found', 'menu', ''))
        self['menu_Plutotv'].show()
        self['menu_Plutotv'].l.setList(self.Mylist)
        self['menu_Plutotv'].l.setItemHeight(37)
        self.currentList = 'menu_Plutotv'
        self['menu_Plutotv'].selectionEnabled(1)
        self['menu_Plutotv'].moveToIndex(0)
        self['Title'].setText('Pluto Tv')
        Txts = MesImports()._colorize_('Your Proxy=='+str(self.proxyvalue),selcolor='cyan')
        self['myproxy'].setText(Txts)
        self.Get_Infos_select()
    def get_infos_movies(self):
        _cond = self['menu_Plutotv'].getCurrent()[0][0]
        self.idx = self['menu_list_catego'].getSelectionIndex()
        Mydons =self.Mydict[_cond][self.idx]
        discrpt = Mydons[2]
        discrpt = MesImports()._colorize_('DISCR=='+str(discrpt),selcolor='cyan')
        genres_ = Mydons[3]
        genres_ = MesImports()._colorize_('GENRE=='+str(genres_),selcolor='cyan')
        _rat = Mydons[4]
        _rat = MesImports()._colorize_('RAT=='+str(_rat),selcolor='cyan')
        duration = Mydons[5]
        duration = strftime("%Hh %Mm", gmtime(int(duration)))
        duration = MesImports()._colorize_('DURAT=='+str(duration),selcolor='cyan')
        _catgr = Mydons[8]
        _catgr = MesImports()._colorize_('CTGR=='+str(_catgr),selcolor='cyan')
        self['Info_0'].setText(discrpt)
        self['Info_1'].setText(genres_)
        self['Info_2'].setText(_rat)
        self['Info_3'].setText(duration)
        self['Info_4'].setText(_catgr)
    def Nety_txt(self,txt):
        #txt = txt.split('.  ')[1]
        return txt
    def ok(self):
        self.Chouf = []
        self.idx = self['menu_Plutotv'].getSelectionIndex()
        namet = self.Nety_txt(self['menu_Plutotv'].getCurrent()[0][0])
        if namet=='Not Found':
            self.session.open(MessageBox, 'Mafihache hihi\n Change Your Proxy', MessageBox.TYPE_INFO)
            return
        elif self.imports and not self.secondlist:
            self.Chouf =  PlutotvNew(self.proxyvalue).Movies_Categories_list_Pluto(namet,self.Mydict)
            self['menu_list_catego'].l.setList(self.Chouf)
            self['menu_list_catego'].l.setItemHeight(37)
            self['menu_list_catego'].show()
            self['menu_list_catego'].selectionEnabled(1)
            self.currentList = 'menu_list_catego'
            self['menu_list_catego'].moveToIndex(0)
            self['menu_Plutotv'].selectionEnabled(0)
            self['menu_Plutotv'].hide()
            self.secondlist = True
            self.Get_Infos_select()
        elif self.imports and self.secondlist:
            categr=self['menu_list_catego'].getCurrent()[0][7]
            if categr=='movie':self.Play_Videos()
            else:
                _id = str(self['menu_list_catego'].getCurrent()[0][1])
                a,self.mist,self.dicseason = PlutotvNew(self.proxyvalue).getVOD(_id)
                if a:
                    name_ep = self['menu_list_catego'].getCurrent()[0][0]
                    self.session.open(Screen_MyPlutoTvNew_season_episode,self.mist,self.dicseason,name_ep)
                else:self.session.open(MessageBox, '3awad kach nhar hihihi...', MessageBox.TYPE_INFO)
        else:pass
    def Exit_plug(self):
        if self.secondlist:
            self['menu_Plutotv'].show()
            self['menu_Plutotv'].selectionEnabled(1)
            self.currentList = 'menu_Plutotv'
            #######################################
            self['menu_list_catego'].hide()
            self['menu_list_catego'].selectionEnabled(0)
            self.secondlist = False
            self.Get_Infos_select()
        else:self.close()
    def show_all_chang(self):#
        msg = ''
        if self.proxyvalue==config.plugins.SupTVoDNeWConfig.Plutotv.value:
            pass
        else:
            self.proxyvalue=config.plugins.SupTVoDNeWConfig.Plutotv.value
            Txts = MesImports()._colorize_('Your Proxy=='+str(self.proxyvalue),selcolor='cyan')
            self['myproxy'].setText(Txts)
            self.imports = False
            self.secondlist = False
            self['menu_list_catego'].hide()
            self.get_ListIptvFnl()
            self.Get_Changement()
    def Get_Changement(self):
        for t in range(5):
            self['Info_'+str(t)].setText('')
        self.picfile = PLUGIN_PATH + '/img/playlist/logoplutotv.png'
        self['Title'].setText('Pluto Tv')
        self.decodeImage()
    def Get_Infos_select(self):
        Hd = self.Nety_txt(self[self.currentList].getCurrent()[0][0])
        self['Infoselect'].setText(Hd)
        if self.currentList == 'menu_list_catego':
            self.get_infos_movies()
            self['Title'].setText(self['menu_Plutotv'].getCurrent()[0][0])
            self.Download_Image()
        else:
            self.Get_Changement()
    def keyDown(self):
        self[self.currentList].down()
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
    def Settings(self):
        self.session.open(SupTVoDNeW_Config)
    def image_downloaded(self, id):
        self.decodeImage()
    def Download_Image(self):
        img = self['menu_list_catego'].getCurrent()[0][3].encode('utf-8').replace('https','http')
        if img.find('http') == -1:
            self.picfile = PLUGIN_PATH + '/img/playlist/logoplutotv.png'
            self.decodeImage()
        else:
            self.picfile = '%splutoTv_pic.jpg' % config.plugins.SupTVoDNeWConfig.Posters.value
            downloadPage(img, self.picfile).addCallback(self.image_downloaded)
    def decodeImage(self):
        try:
            x = self['poster'].instance.size().width()
            y = self['poster'].instance.size().height()
            picture = self.picfile
            picload = self.picload
            sc = AVSwitch().getFramebufferScale()
            picload.setPara((x,y,sc[0],sc[1],0,0,'#00000000'))
            l = picload.PictureData.get()
            del l[:]
            l.append(boundFunction(self.showImage))
            picload.startDecode(picture)
        except Exception as ex:
            print ex
            print 'ERROR decodeImage'
    def showImage(self, picInfo = None):
        self['poster'].show()
        try:
            ptr = self.picload.getData()
            if ptr:
                self['poster'].instance.setPixmap(ptr.__deref__())
        except Exception as ex:
            print ex
    def Play_Videos(self):
        from Screens.InfoBar import InfoBar, MoviePlayer
        name,sid,url,categr,self.Mylistessai = '','','','',[]
        if self.imports and self.secondlist:
            name,sid,url,categr=self['menu_list_catego'].getCurrent()[0][0],self['menu_list_catego'].getCurrent()[0][1],self['menu_list_catego'].getCurrent()[0][2],self['menu_list_catego'].getCurrent()[0][7]
            if categr == 'movie':
                stream_url = PlutotvNew(self.proxyvalue).playVOD_Pluto(name, sid, url)
                self.reference = eServiceReference(5002, 0, stream_url.encode('utf-8'))
                self.reference.setName(name)
                self.session.open(MoviePlayer,self.reference)
        else:pass
###########################################################################################
class Screen_MyPlutoTvNew_season_episode(Screen):
    def __init__(self, session,mist,dicseason,name):
        ########################Session_Skin############################
        if dwidth == 1280:
            with open(PATH_SKINS + '/PlutoTv_season_episode_FHD.xml', 'r') as f:
                self.skin = f.read()
                f.close()
        else:
            with open(PATH_SKINS + '/PlutoTv_season_episode_FHD.xml', 'r') as f:
                self.skin = f.read()
                f.close()
        self.session = session
        Screen.__init__(self, session)
        self['actions'] = ActionMap(['DirectionActions','SetupActions','ColorActions'], {'ok': self.ok,
            'cancel': self.Exit_plug,
            'red': self.Exit_plug,
            #'1': self.show_all_chang,
            'yellow': self.Settings,
            #'blue': self.get_categorie_select,
            'green': self.ok,
            'up': self.keyUp,
            'down': self.keyDown,
            'left': self.left,
            'right': self.right
            }, -1)
        self.mist,self.dicseason,self.name=mist,dicseason,name
        self.proxyvalue = config.plugins.SupTVoDNeWConfig.Plutotv.value
        self.initialservice = self.session.nav.getCurrentlyPlayingServiceReference()
        self.onShown.append(self.show_all_chang)
        self['Infos'] = Label()
        self['Title'] = Label()
        self['Infoselect'] = Label()
        self['myproxy'] = Label()
        self['menu_Plutotv'] = m2list([])
        self['menu_list_catego'] = m2list([])
        self['menu_list_catego'].hide()
        self.Chouf,self.Mylist,self.Mydict = [],[],{}
        self['poster'] = Pixmap()
        self.picload = ePicLoad()
        self.imports = False
        self.secondlist = False
        self.TXT = ''
        self.idx = 0
        for x in range(5):
            if x == 0:self['Info_'+str(x)] =StaticText()
            else:self['Info_'+str(x)] = Label()
        self.get_ListIptvFnl()
    def get_ListIptvFnl(self):
        self.Mylist,self.Mydict = [],{}
        self.Mylist = self.mist
        self.Mydict = self.dicseason
        self.imports = True
        self['menu_Plutotv'].show()
        self['menu_Plutotv'].l.setList(self.Mylist)
        self['menu_Plutotv'].l.setItemHeight(37)
        self.currentList = 'menu_Plutotv'
        self['menu_Plutotv'].selectionEnabled(1)
        self['menu_Plutotv'].moveToIndex(0)
        self['Title'].setText(self.name)
        Txts = MesImports()._colorize_('Your Proxy=='+str(self.proxyvalue),selcolor='cyan')
        self['myproxy'].setText(Txts)
        #self.Get_Infos_select()
    def get_infos_movies(self):
        _cond = self['menu_Plutotv'].getCurrent()[0][0]
        self.idx = self['menu_list_catego'].getSelectionIndex()
        Mydons =self.Mydict[_cond][self.idx]
        discrpt = Mydons[2]
        discrpt = MesImports()._colorize_('DISCR=='+str(discrpt),selcolor='cyan')
        genres_ = Mydons[3]
        genres_ = MesImports()._colorize_('GENRE=='+str(genres_),selcolor='cyan')
        _rat = Mydons[4]
        _rat = MesImports()._colorize_('RAT=='+str(_rat),selcolor='cyan')
        duration = Mydons[5]
        duration = strftime("%Hh %Mm", gmtime(int(duration)))
        duration = MesImports()._colorize_('DURAT=='+str(duration),selcolor='cyan')
        _catgr = Mydons[8]
        _catgr = MesImports()._colorize_('CTGR=='+str(_catgr),selcolor='cyan')
        self['Info_0'].setText(discrpt)
        self['Info_1'].setText(genres_)
        self['Info_2'].setText(_rat)
        self['Info_3'].setText(duration)
        self['Info_4'].setText(_catgr)
    def Nety_txt(self,txt):
        #txt = txt.split('.  ')[1]
        return txt
    def ok(self):
        self.list_dons = []
        indxt = self['menu_Plutotv'].getCurrent()[0][2].replace(' ','').replace('\n','')
        infosto = self.Mydict[int(indxt)]
        self.Chouf = []
        namet = self.Nety_txt(self['menu_Plutotv'].getCurrent()[0][0])
        if namet=='Not Found':
            self.session.open(MessageBox, 'Mafihache hihi\n Change Your Proxy', MessageBox.TYPE_INFO)
            return
        elif self.imports and not self.secondlist:
            for (sid,name,a,disc,b,c,genre,img,screan,url) in infosto:
                self.list_dons.append(show_Menu_PlutoTv_episodes(name,img,url,sid))
            self.Chouf =  self.list_dons
            self['menu_list_catego'].l.setList(self.Chouf)
            self['menu_list_catego'].l.setItemHeight(37)
            self['menu_list_catego'].show()
            self['menu_list_catego'].selectionEnabled(1)
            self.currentList = 'menu_list_catego'
            self['menu_list_catego'].moveToIndex(0)
            self['menu_Plutotv'].selectionEnabled(0)
            self['menu_Plutotv'].hide()
            self.secondlist = True
            #self.Get_Infos_select()
        elif self.imports and self.secondlist:
            self.Play_Videos()
        else:pass
    def Exit_plug(self):
        if self.secondlist:
            self['menu_Plutotv'].show()
            self['menu_Plutotv'].selectionEnabled(1)
            self.currentList = 'menu_Plutotv'
            #######################################
            self['menu_list_catego'].hide()
            self['menu_list_catego'].selectionEnabled(0)
            self.secondlist = False
            self.Get_Infos_select()
        else:self.close()
    def show_all_chang(self):#
        msg = ''
        if self.proxyvalue==config.plugins.SupTVoDNeWConfig.Plutotv.value:
            pass
        else:
            self.close()
            # self.proxyvalue=config.plugins.SupTVoDNeWConfig.Plutotv.value
            # Txts = _colorize_('Your Proxy=='+str(self.proxyvalue),selcolor='cyan')
            # self['myproxy'].setText(Txts)
            # self.imports = False
            # self.secondlist = False
            # self['menu_list_catego'].hide()
            # self.get_ListIptvFnl()
            # self.Get_Changement()
    def Get_Changement(self):
        for t in range(5):
            self['Info_'+str(t)].setText('')
        self.picfile = PLUGIN_PATH + '/img/playlist/logoplutotv.png'
        #self['Title'].setText('Pluto Tv')
        self.decodeImage()
    def Get_Infos_select(self):
        Hd = self.Nety_txt(self[self.currentList].getCurrent()[0][0])
        self['Infoselect'].setText(Hd)
        if self.currentList == 'menu_list_catego':
            #self.get_infos_movies()
            #self['Title'].setText(self['menu_Plutotv'].getCurrent()[0][0])
            self.Download_Image()
        else:
            self.Get_Changement()
    def keyDown(self):
        self[self.currentList].down()
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
    def Settings(self):
        self.session.open(SupTVoDNeW_Config)
    # def image_downloaded(self, id):
        # self.decodeImage()
    def Download_Image(self):
        # MyIdx = self['menu_list_catego'].getSelectionIndex()
        # self.img = self._New_2[MyIdx][1].encode('utf-8').replace('https','http')
        # MesImports().Download_Image(self.img,self['poster'])
        img = self['menu_list_catego'].getCurrent()[0][1].encode('utf-8').replace('https','http')
        MesImports().Download_Image(img,self['poster'])
        # if img.find('http') == -1:
            # self.picfile = PLUGIN_PATH + '/img/playlist/logoplutotv.png'
            # self.decodeImage()
        # else:
            # self.picfile = '%splutoTv_pic.jpg' % config.plugins.SupTVoDNeWConfig.Posters.value
            # downloadPage(img, self.picfile).addCallback(self.image_downloaded)
    # def decodeImage(self):
        # try:
            # x = self['poster'].instance.size().width()
            # y = self['poster'].instance.size().height()
            # picture = self.picfile
            # picload = self.picload
            # sc = AVSwitch().getFramebufferScale()
            # picload.setPara((x,y,sc[0],sc[1],0,0,'#00000000'))
            # l = picload.PictureData.get()
            # del l[:]
            # l.append(boundFunction(self.showImage))
            # picload.startDecode(picture)
        # except Exception as ex:
            # print ex
            # print 'ERROR decodeImage'
    # def showImage(self, picInfo = None):
        # self['poster'].show()
        # try:
            # ptr = self.picload.getData()
            # if ptr:
                # self['poster'].instance.setPixmap(ptr.__deref__())
        # except Exception as ex:
            # print ex
    def Play_Videos(self):
        from Screens.InfoBar import InfoBar, MoviePlayer
        name,sid,url,categr,self.Mylistessai = '','','','',[]
        if self.imports and self.secondlist:#(name,img,url,sid)
            name=self['menu_list_catego'].getCurrent()[0][0]
            sid=self['menu_list_catego'].getCurrent()[0][3]
            url=self['menu_list_catego'].getCurrent()[0][2]
            stream_url = PlutotvNew(self.proxyvalue).playVOD_Pluto(name, sid, url)
            self.reference = eServiceReference(5002, 0, stream_url.encode('utf-8'))
            self.reference.setName(name)
            self.session.open(MoviePlayer,self.reference)
        else:pass
###########################################################################################
#####################################  Menu Show TV #######################################
###########################################################################################
import os, cPickle
def loadResumePoints():
    try:
        file = open('/etc/enigma2/resumepoints.pkl', 'rb')
        PickleFile = cPickle.load(file)
        file.close()
        return PickleFile
    except Exception as ex:
        print '[InfoBar] Failed to load resumepoints:', ex
        return {}
from Screens.InfoBar import InfoBar, MoviePlayer
from Screens.InfoBarGenerics import *
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