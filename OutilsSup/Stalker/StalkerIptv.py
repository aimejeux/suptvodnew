#!/usr/bin/python
# -*- coding: utf-8 -*-
################################### modified by aime_jeux ##################################
#############                           Aout 2021                              #############
############################################################################################
########################################################################
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore',InsecureRequestWarning)
########################################################################
from Screens.TaskView import JobView
from Components.Task import Task, Job, job_manager as JobManager, Condition
from Tools import Notifications, ASCIItranslit
import re,json
from Screens.InputBox import InputBox
from Components.Input import Input
############################################################################################
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Tmdb.Tmdb import Tmdb_Suptvod,Screen_MyTMDB_SupTvod
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Sptvnw.MesImports import MesImports,downloadJob
from Components.Sources.StaticText import StaticText
from enigma import eServiceReference
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Stalker.InfobarStalker import Xtream_Player_New,Copy_Volum
from enigma import ePoint, eSize, eTimer
from operator import truediv
from Tools.BoundFunction import boundFunction
from stalker_portal_New import *
from enigma import eTimer,ePicLoad
from Components.AVSwitch import AVSwitch
from twisted.web.client import downloadPage
import os,sys,time
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.Label import Label
from Components.ActionMap import ActionMap, HelpableActionMap, NumberActionMap
from Components.Pixmap import Pixmap
from GetServers import get_InfosOXml_Stalker
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Sptvnw.Config import *
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Sptvnw.Setup import SupTVoDNeW_Config
Version = 'SupTVoDNeW V_1.0'
from Plugins.Extensions.SupTVoDNeW.plugin import return_version
PATH_SKINS = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/Skins'
PLUGIN_PATH = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW'
from stalker_portal import *
global MyImport
MyImport = Stalker()
###########################################################################################
global Lis_Clean
Lis_Clean_0 = ['isra','israel','adult','adulte','adults','xxx','xx','porn','+18','hard','sex',
               'ado','blowjob','lesbie','travest','frisson']
Lis_Clean_1 = ['sex','xxl','hotclub','venus','playb','hust','libid','penthouse','spice','platinum','amatix','xx',
               'vivid','brazzers','colmax','daring','lover','man-x','man x','manx','pink_x','pink-x','pink x',
               'pinkx','reality kings','stars xxx',
               'pink show','pink-show','pink_show','pinkshow','porn','brazz','lov','adult','hust','candy']
Lis_Clean = Lis_Clean_0+Lis_Clean_1
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Sptvnw.supcompnt import *
from skin import loadSkin
loadSkin(PATH_SKINS + '/Xtream_StalkerFHD.xml')
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
class Screen_MyStalkerIptv(Screen):
    def __init__(self, session):
        self.session = session
        Screen.__init__(self, session)
        self['actions'] = ActionMap(['DirectionActions','SetupActions','ColorActions'], {'ok': self.ok,
            'cancel': self.close,
            'red': self.close,
            'yellow': self.Settings,
            'blue': self.get_Infos_Servers,
            'green': self.ok,
            'up': self.keyUp,
            'down': self.keyDown,
            'left': self.left,
            'right': self.right
            }, -1)
        self.initialservice = self.session.nav.getCurrentlyPlayingServiceReference()
        self['Infos'] = Label()
        self['Infoselect'] = Label()
        self['Dat_Exprt'] = Label()
        self['Dat_Exprt'].hide()
        self['menu_servers'] = m2list([])
        self.MyFolderXml = []
        self.TXT = ''
        self.idx = 0
        self.get_ListIptvFnl()
    def Settings(self):
        self.session.open(SupTVoDNeW_Config)
    def get_ListIptvFnl(self):
        ListIptv = get_InfosOXml_Stalker()[1]
        i = 1
        for name,url,mac in ListIptv:
            self.MyFolderXml.append(show_Menu_Stalker(' '+str(i)+'.  '+name+' [ Stalker ]',url,mac))
            i = i + 1
        self['menu_servers'].l.setList(self.MyFolderXml)
        self['menu_servers'].l.setItemHeight(37)
        self.currentList = 'menu_servers'
        self.Get_Infos_select()
    def ok(self):
        self.actualizaimg()
        self.idx = self['menu_servers'].getSelectionIndex()
        name = MesImports().Nety_txt(self['menu_servers'].getCurrent()[0][0])
        self.get_Infos_Servers()
        self.session.open(Screen_MyStalkerIptv_Menu_Stalker,self.idx,name,self.TXT)#.addCallback(self.actualizaimg)
    def actualizaimg(self):
        self['Dat_Exprt'].show()
        self['Dat_Exprt'].setText('Patientez......')
    def get_Infos_Servers(self):
        self['Dat_Exprt'].show()
        self.idx = self['menu_servers'].getSelectionIndex()
        self.TXT = 'Expiration Date : '+str(MyImport._lan_Dat_Exprt(self.idx))
        self['Dat_Exprt'].setText(self.TXT)
    def Get_Infos_select(self):
        self['Dat_Exprt'].show()
        self['Infos'].setText(self['menu_servers'].getCurrent()[0][1]+'/c?mac='+str(self['menu_servers'].getCurrent()[0][2]))
        self['Dat_Exprt'].hide()
        Hd = MesImports().Nety_txt(self['menu_servers'].getCurrent()[0][0])
        self['Infoselect'].setText(Hd)
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
###########################################################################################
#####################################  Menu Servers #######################################
###########################################################################################
# from Plugins.Extensions.SupTVoDNeW.OutilsSup.Sptvnw.Spinner import Spinner,startspinner,buildBilder
from enigma import gPixmapPtr
class Screen_MyStalkerIptv_Menu_Stalker(Screen):
    def __init__(self, session,idx,name,d_expr):
        self.session = session
        Screen.__init__(self, session)
        self['actions'] = ActionMap(['DirectionActions','SetupActions','ColorActions'], {'ok': self.ok,
            'cancel': self.Exit_Stlk,
            'red': self.Exit_Stlk,
            'yellow': self.Settings,
            'blue': self.back_to_video,
            'up': self.keyUp,
            'down': self.keyDown,
            'left': self.left,
            'right': self.right
            }, -1)
        self.initialservice = self.session.nav.getCurrentlyPlayingServiceReference()
        self.idx,self.name,self.d_expr= idx,name,d_expr
        self['Infos'] = Label()
        self['Infos_selct'] = Label()
        self['Infos_selct'].setText(self.name)
        self['Dat_Exprt'] = Label()
        self['loading'] = Label(_(Stalker_New().Loading))
        self['loading'].hide()
        self['Dat_Exprt'].setText(self.d_expr)
        self._L_Stalker_ = []
        self['menu_stalker_2'] = m2list([])
        self._L_Stalker = [('Live TV','Channel'),('Videos Ondemande','Vod'),('TV Show','Series')]
        self.spinner_running = False
        self.timer = eTimer()
        self.show_all()
    def Settings(self):
        self.session.open(SupTVoDNeW_Config)
    def back_to_video(self):
        H,Y = '',''
        Milef = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/Cfg/Recup'
        if os.path.isfile(Milef):
            file_write = open(Milef, 'r')
            data = file_write.readlines()
            file_write.close()
            H = data[0].replace('\n', '').replace('\t', '').replace('\r', '')
            H = H.split('=')[1].replace(' ','')
            Y = data[1].replace('\n', '').replace('\t', '').replace('\r', '')
            Y = Y.split('===')[1].replace(' ','')
        self.session.open(MessageBox, str(H)+'\n'+str(Y), MessageBox.TYPE_INFO)
        a,stream_url = get_donnees_Stalker_New(int(H),indxstream=Y)
        self.session.open(MessageBox, str(H)+'\n'+str(Y)+'\n'+str(a)+'\n'+str(stream_url), MessageBox.TYPE_INFO)
        if a:
            self.rds = MesImports().get_player()
            self.reference = eServiceReference(self.rds, 0, stream_url.encode('utf-8'))
            self.reference.setName('back_to_video')
            self.session.open(ServiceAppPlayer,self.reference)
    def Exit_Stlk(self):
        self.close()
    def show_all(self):
        self._L_Stalker_ = []
        s = 1
        for a in self._L_Stalker:
            self._L_Stalker_.append(show_Menu_Stalker(' '+str(s)+'.  '+a[0],a[1],''))
            s = s + 1
        self['menu_stalker_2'].l.setList(self._L_Stalker_)
        self['menu_stalker_2'].l.setItemHeight(37)
        self.currentList = 'menu_stalker_2'
        self.Get_Infos_select()
    def _Show(self):
        self['loading'].show()
        return True
    def ok(self):
        self._Channelsss = []
        cond = self['menu_stalker_2'].getCurrent()[0][1]
        Myselect = self['menu_stalker_2'].getCurrent()[0][0]
        if cond == 'Channel':
            a,self._Channelsss = get_donnees_Stalker_New(self.idx,_list='list',mode='TV')
            if a:
                self.session.open(Screen_MyStalkerIptv_Menu_Stalker_Channel,self.idx,self.name,self.d_expr,self._Channelsss)
            else:
                self.session.open(MessageBox, 'List [ Live TV ] Not Found\n Check Expiration Date\nOr\nTry Again ', MessageBox.TYPE_INFO)
        elif cond == 'Vod':
            a,self._Channelsss = get_donnees_Stalker_New(self.idx,_list='list',mode='VOD')
            if a:
                self.session.open(Screen_MyStalkerIptv_Menu_Stalker_VOD,self.idx,self.name,self.d_expr,self._Channelsss)
            else:
                self.session.open(MessageBox, 'List [ VOD ] Not Found\n Check Expiration Date\nOr\nTry Again ', MessageBox.TYPE_INFO)
        else:
            a,self._Channelsss = get_donnees_Stalker_New(self.idx,_list='list',mode='SERIES')
            if a:
                self.session.open(Screen_MyStalkerIptv_Menu_Stalker_SERIES,self.idx,self.name,self.d_expr,self._Channelsss)
            else:
                self.session.open(MessageBox, 'List [ VOD ] Not Found\n Check Expiration Date\nOr\nTry Again ', MessageBox.TYPE_INFO)
        #Screen_MyStalkerIptv_Menu_Stalker_SERIES
    def hid(self):
        self['loading'].show()
    def Get_Infos_select(self):
        txt = MesImports().Nety_txt(self['menu_stalker_2'].getCurrent()[0][0])
        self['Infos'].setText(txt)
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
###########################################################################################
#####################################  Menu Live TV #######################################
###########################################################################################
class Screen_MyStalkerIptv_Menu_Stalker_Channel(Screen):
    def __init__(self, session,idx,name,d_expr,_New_1):
        self.session = session
        Screen.__init__(self, session)
        self['actions'] = ActionMap(['DirectionActions','SetupActions','ColorActions'], {'ok': self._Show,
            'cancel': self.Exit_Stlk,
            'red': self.Exit_Stlk,
            'up': self.keyUp,
            'down': self.keyDown,
            'left': self.left,
            'right': self.right
            }, -1)
        self.initialservice = self.session.nav.getCurrentlyPlayingServiceReference()
        self._New_1 = []
        self.idx,self.name,self.d_expr,self._New_1 = idx,name,d_expr,_New_1
        self.Total=self.page=1
        self['Infos'] = Label()
        self['Infos_selct'] = Label()
        self['Infos_selct'].setText('Server : '+self.name)
        self['Dat_Exprt'] = Label()
        self['Dat_Exprt'].setText(self.d_expr)
        self['menu_stalker_Channel'] = m2list([])
        self._L_Stalker_ = []
        self.menu_Channels_1 = []
        #self.timer = eTimer()
        self["loading"] = Label()
        self.show_all()
    def Exit_Stlk(self):
        self.session.nav.playService(self.initialservice)
        self.close()
    def show_all(self):
        self._L_Stalker_ = []
        s = 1
        for a in self._New_1:#(title,_id,'')
            title,_id = a[0],a[1]
            self._L_Stalker_.append(show_Menu_Stalker(' '+str(s)+'.  '+title,_id,'TV'))
            s = s + 1
        self['menu_stalker_Channel'].l.setList(self._L_Stalker_)
        self['menu_stalker_Channel'].l.setItemHeight(37)
        self['menu_stalker_Channel'].show()
        self.currentList = 'menu_stalker_Channel'
    def _Show(self):
        c,G = get_Loading()
        self["loading"].setText(G)
        log('Screen_MyStalkerIptv_Menu_Stalker_Channel')
        self.ok()
    def ok(self):
        self._Channelsts = []
        MyIdx = self['menu_stalker_Channel'].getSelectionIndex()
        name = self['menu_stalker_Channel'].getCurrent()[0][0]
        for nom in Lis_Clean:
            if nom.lower() in name.lower():
                self.session.open(MessageBox,'A movie suspected of pornography ', MessageBox.TYPE_INFO)
                return
        a,self._Channelsts,self.Total = get_donnees_Stalker_New(self.idx,stream=str(MyIdx),pg=1,mode='TV')
        if a:
            cord = self.Total
            self.session.open(Screen_MyStalkerIptv_Menu_Stalker_Channel_List,self.idx,self.name,self.d_expr,self._Channelsts,cord,MyIdx)
        else:
            self.session.open(MessageBox, 'List [ Live TV ] Not Found\n Check Expiration Date\nOr\nTry Again ', MessageBox.TYPE_INFO)
        self.hid()
    def hid(self):
        self["loading"].setText('')
    def Get_Infos_select(self):
        txt = MesImports().Nety_txt(self['menu_stalker_Channel'].getCurrent()[0][0])
        self['Infos'].setText(txt)
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
###########################################################################################
#####################################  Menu Video Ondemande  ##############################
###########################################################################################
class Screen_MyStalkerIptv_Menu_Stalker_Channel_List(Screen):
    def __init__(self, session,idx,name,d_expr,_New_2,cord,MyIdx):
        self.session = session
        Screen.__init__(self, session)
        self['actions'] = HelpableActionMap(self,'StalkerPlayerPlaylist', {'ok': self.ok,
            'cancel_Stalk': self.exit_box,
            'show_hide': self.show_hide_menu,
            'up': self.keyUp,
            'down': self.keyDown,
            'left': self.left,
            'right': self.right
            }, -1)
        self.initialservice = self.session.nav.getCurrentlyPlayingServiceReference()
        self.onShown.append(self.show_all_chang)
        self._New_2 = []
        self.idx,self.name,self.d_expr,self._New_2 = idx,name,d_expr,_New_2
        self['Infos'] = Label()
        self['Infos_selct'] = Label()
        self['Infos_selct'].setText('Server : '+self.name)
        self['Dat_Exprt'] = Label()
        self['Total'] = Label()
        self['Page'] = Label()
        self['Dat_Exprt'].setText(self.d_expr)
        self['menu_stalker_Channel_List'] = m2list([])
        self._L_Stalker_1 = []
        self.menu_Channels_1 = []
        self.List_MoviePlayer_1 = []
        self['poster'] = Pixmap()
        self['poster'].hide()
        self.picload = ePicLoad()
        self.Nextpage = 1
        self.s = 1
        self.Az = 1
        self.H = ''
        self.Total = cord
        self.showhide = False
        self.hidden = False
        if self.Total !='nada':
            self.Az = truediv(int(self.Total),14)
            self.Az = round(self.Az)
            t = str(self.Az).split('.')[1]
            if t !='0':self.Az = int(str(self.Az).split('.')[0])+1
            else:self.Az = int(str(self.Az).split('.')[0])
        self.MyIdx = MyIdx
        self.show_all()
    def exit_box(self):
        self.session.nav.playService(self.initialservice)
        self.close()
    def show_all_chang(self):
        H,Y =MesImports().Recovery_indx()
        if str(Y)== 'True':
            try:
                index_=H
                self['menu_stalker_Channel_List'].moveToIndex(int(index_))
                Copy_Volum('indexfil='+str(H)+'\ndakhla=False','indexfil')
                MesImports().Download_Image(self.img,self['poster'])
            except Exception as ex:
                print ex
    def get_pag_select(self):
        if int(self.Total)%14!=0:self.H=(int(self.Total)/14) + 1
        else:self.H=int(self.Total)/14
        Txt = 'Page  '+str(self.Nextpage)+'/ '+str(self.H)
        self['Total'].setText(Txt+'   ['+str(self.Total)+' Data ]')
    def show_all(self):
        self._L_Stalker_1 = []
        self.List_MoviePlayer_1 = []
        self.s = self.s
        T = len(self._New_2)
        for (name,img,stream) in self._New_2:#(title,_id,'')
            for nom in Lis_Clean:
                if nom.lower() in name.lower():continue 
            self._L_Stalker_1.append(show_Menu_Stalker_1(' '+str(self.s)+'.  '+name,img,stream,'TV'))
            '''(chan_counter,name,description,piconname,stream_url,playlist_url,category_id,
                img_src,description4playlist_html,ts_stream)'''
            self.List_MoviePlayer_1.append(('',name,name +' .......','',stream,'','',img,'',''))
            self.s = self.s + 1
        self._L_Stalker_1.append(show_Menu_Stalker_1(' \tNext Page','','',''))
        self['menu_stalker_Channel_List'].l.setList(self._L_Stalker_1)
        self['menu_stalker_Channel_List'].l.setItemHeight(37)
        self['menu_stalker_Channel_List'].show()
        self.currentList = 'menu_stalker_Channel_List'
        self['menu_stalker_Channel_List'].moveToIndex(0)
        self.get_pag_select()
    def get_NextPag(self):#######################"
        if self.Total == 'nada':pass
        else:
            cond = 14*self.Nextpage
            if cond < self.Total:
                self.Nextpage = self.Nextpage + 1
            else:
                self.Nextpage = 1
                self.s = 1
            self.get_pag_select()
    def T_NextPag(self,page):
        self._New_2 = []
        a,self._New_2,self.Total = get_donnees_Stalker_New(self.idx,stream=str(self.MyIdx),pg=page,mode='TV')
        if a:
            self.show_all()
        else:pass
    def get_Second_Page(self):################################################################################
        u = self['menu_stalker_Channel_List'].getSelectionIndex()
        V = len(self._New_2)
        chart = self['menu_stalker_Channel_List'].getCurrent()[0][0]
        if self['menu_stalker_Channel_List'].getCurrent()[0][0] != ' \tNext Page' and u!=0:pass
        else:
            if chart == ' \tNext Page':#DOWN
                if int(self.H)== 1:self['menu_stalker_Channel_List'].moveToIndex(0)
                else:
                    if self.Nextpage == int(self.H):
                        self.Nextpage=self.s = 1
                        self.T_NextPag(self.Nextpage)
                    else:
                        self.Nextpage = self.Nextpage + 1
                        self.s = self.s
                        self.T_NextPag(self.Nextpage)
            else:#UP
                if int(self.H)== 1:self['menu_stalker_Channel_List'].moveToIndex(13)
                else:
                    if self.Nextpage == 1:
                        self.Nextpage = int(self.H)
                        self.s = 14*(int(self.H)- 1) + 1
                        self.T_NextPag(self.Nextpage)
                    else:
                        self.Nextpage = self.Nextpage - 1
                        self.s = self.s - (14 + V)
                        self.T_NextPag(self.Nextpage)
    def ok(self):
        Idx = self['menu_stalker_Channel_List'].getSelectionIndex()
        lala = self['menu_stalker_Channel_List'].getCurrent()[0][0]
        name = MesImports().Nety_txt(self['menu_stalker_Channel_List'].getCurrent()[0][0])
        for nom in Lis_Clean:
            _name = name.lower().replace('canal','')
            if nom.lower() in _name:
                self.session.open(MessageBox,'A movie suspected of pornography \n'+nom.lower()+'\n'+name.lower(), MessageBox.TYPE_INFO)
                return
        if lala == ' \tNext Page':pass
        img = self._New_2[Idx][1]
        Url = self._New_2[Idx][2]
        self.session.open(Xtream_Player_New,recorder_sref=None,liste=self.List_MoviePlayer_1,indxto=Idx,Oldservice=self.initialservice,server=self.idx,_type='iptv')
    def Get_Infos_select(self):
        if self['menu_stalker_Channel_List'].getCurrent()[0][0] != ' \tNext Page':
            txt = MesImports().Nety_txt(self['menu_stalker_Channel_List'].getCurrent()[0][0])
            self['Infos'].setText(txt)
            self.Download_Image()
    def keyDown(self):
        self[self.currentList].down()
        self.get_Second_Page()
        self.Get_Infos_select()
    def keyUp(self):
        if self['menu_stalker_Channel_List'].getSelectionIndex() ==0:self.get_Second_Page()
        else:self[self.currentList].up()
        self.Get_Infos_select()
    def left(self):
        self['menu_stalker_Channel_List'].moveToIndex(0)
        self.Get_Infos_select()
    def right(self):
        mov = len(self._New_2)-1 
        self['menu_stalker_Channel_List'].moveToIndex(mov)
        self.Get_Infos_select()
    def image_downloaded(self, id):
        self.decodeImage()
    def Download_Image(self):
        MyIdx = self['menu_stalker_Channel_List'].getSelectionIndex()
        self.img = self._New_2[MyIdx][1].encode('utf-8').replace('https','http')
        MesImports().Download_Image(self.img,self['poster'])
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
    def show_hide_menu(self):
        if not self.showhide:
            if self.hidden:
                self.show()
            else:
                self.hide()
            self.hidden = not self.hidden
###########################################################################################
###########################################################################################
#####################################  Menu List VOD #######################################
###########################################################################################
class Screen_MyStalkerIptv_Menu_Stalker_VOD(Screen):
    def __init__(self, session,idx,name,d_expr,_New_3):
        self.session = session
        Screen.__init__(self, session)
        self['actions'] = ActionMap(['DirectionActions','SetupActions','ColorActions'], {'ok': self._Show,
            'cancel': self.Exit_Stlk,
            'red': self.Exit_Stlk,
            'up': self.keyUp,
            'down': self.keyDown,
            'left': self.left,
            'right': self.right
            }, -1)
        self._New_3 = []
        self.initialservice = self.session.nav.getCurrentlyPlayingServiceReference()
        self.idx,self.name,self.d_expr,self._New_3 = idx,name,d_expr,_New_3
        self.Total=self.page=1
        self['Infos'] = Label()
        self['Infos_selct'] = Label()
        self['Infos_selct'].setText('Server : '+self.name)
        self['Dat_Exprt'] = Label()
        self['Dat_Exprt'].setText(self.d_expr)
        self['menu_stalker_Stalker_VOD'] = m2list([])
        self._L_Stalker_2 = []
        self.menu_Channels_1 = []
        #self.timer = eTimer()
        self["loading"] = Label(_('Loading  ...... List Channel Live TV %s.. ' % 'Please wait'))
        self["loading"].hide()
        self.show_all()
    def Exit_Stlk(self):
        self.session.nav.playService(self.initialservice)
        self.close()
    def show_all(self):
        self._L_Stalker_2 = []
        s = 1
        for a in self._New_3:#(title,_id,'')
            title,_id = a[0],a[1]
            self._L_Stalker_2.append(show_Menu_Stalker(' '+str(s)+'.  '+title,_id,'VOD'))
            s = s + 1
        self['menu_stalker_Stalker_VOD'].l.setList(self._L_Stalker_2)
        self['menu_stalker_Stalker_VOD'].l.setItemHeight(37)
        self['menu_stalker_Stalker_VOD'].show()
        self.currentList = 'menu_stalker_Stalker_VOD'
    def _Show(self):
        self.ok()
    def ok(self):
        self._Channelsts = []
        MyIdx = self['menu_stalker_Stalker_VOD'].getSelectionIndex()
        name = MesImports().Nety_txt(self['menu_stalker_Stalker_VOD'].getCurrent()[0][0])
        for nom in Lis_Clean:
            if nom.lower() in name.lower():
                self.session.open(MessageBox,'A movie suspected of pornography ', MessageBox.TYPE_INFO)
                return
        a,self._Channelsts,self.Total = get_donnees_Stalker_New(self.idx,stream=str(MyIdx),pg=1,mode='VOD')
        if a:
            cord = self.Total
            self.session.open(Screen_MyStalkerIptv_Menu_Stalker_Channel_List_VOD,self.idx,self.name,self.d_expr,self._Channelsts,cord,MyIdx)
        else:
            self.session.open(MessageBox, 'List [ Live TV ] Not Found\n Check Expiration Date\nOr\nTry Again ', MessageBox.TYPE_INFO)
            #self.timer.stop()
            self["loading"].hide()
    def hid(self):
        #self.timer.stop()
        self["loading"].hide()
    def Get_Infos_select(self):
        txt = MesImports().Nety_txt(self['menu_stalker_Stalker_VOD'].getCurrent()[0][0])
        self['Infos'].setText(txt)
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
###########################################################################################
class Screen_MyStalkerIptv_Menu_Stalker_Channel_List_VOD(Screen):
    def __init__(self, session,idx,name,d_expr,_New_4,cord,MyIdx):
        self.session = session
        Screen.__init__(self, session)
        self['actions'] = HelpableActionMap(self,'StalkerPlayerPlaylist', {'ok': self.ok,
            'get_Tmdb': self.get_Tmdb,
            'Downloadvideo': self.get_DownloadMovies_choice,
            'cancel_Stalk': self.exit_box,
            'show_hide': self.show_hide_menu,
            'Go_To_Pg': self.GoToPage,
            'up': self.keyUp,
            'down': self.keyDown,
            'left': self.left,
            'right': self.right
            }, -1)
        self.initialservice = self.session.nav.getCurrentlyPlayingServiceReference()
        self.onShown.append(self.show_all_chang)
        for u in range(8):
            self['Infos_Mov_'+str(u+1)] = Label()
        self._New_4 = []
        self.idx,self.name,self.d_expr,self._New_4 = idx,name,d_expr,_New_4
        self['Infos'] = Label()
        self['Infos_selct'] = Label()
        self.rating = 0
        self['rating'] =StaticText()
        self['Infos_Mov'] = StaticText()
        self['Infos_selct'].setText('Server : '+self.name)
        self['Dat_Exprt'] = Label()
        self['connect'] = Label()
        self['connect'].setText('Stay Connected')
        self['Total'] = Label()
        self['Page'] = Label()
        self['Dat_Exprt'].setText(self.d_expr)
        self['menu_stalker_Channel_List_VOD'] = m2list([])
        self._L_Stalker_3 = []
        self.menu_Channels_1 = []
        self.List_MoviePlayer_2 = []
        self['poster'] = Pixmap()
        self['poster'].hide()
        self.picload = ePicLoad()
        self.Nextpage = 1
        self.s = 1
        self.H = ''
        self.Total = cord
        self.dakhla = False
        self.showhide = False
        self.hidden = False
        self.lang = 'fr'
        self.img = PLUGIN_PATH + '/img/playlist/tmdb_default.png'
        if self.Total !='nada':
            self.Az = truediv(int(self.Total),14)
            self.Az = round(self.Az)
            t = str(self.Az).split('.')[1]
            if t !='0':self.Az = int(str(self.Az).split('.')[0])+1
            else:self.Az = int(str(self.Az).split('.')[0])
        self.MyIdx = MyIdx
        self.show_all_VOD()
    def exit_box(self):
        self.session.nav.playService(self.initialservice)
        self.close()
    def show_all_chang(self):
        H,Y =MesImports().Recovery_indx()
        if str(Y)== 'True':
            try:
                index_=H
                self['menu_stalker_Channel_List_VOD'].moveToIndex(int(index_))
                Copy_Volum('indexfil='+str(H)+'\ndakhla=False','indexfil')
                MesImports().Download_Image(self.img,self['poster'])
                #self.img
                self.Get_Infos_select()
                # if os.path.exists('%sStalker_tmp_pic.jpg' % config.plugins.SupTVoDNeWConfig.Posters.value):
                    # self.picfile = '%sStalker_tmp_pic.jpg' % config.plugins.SupTVoDNeWConfig.Posters.value
                    # self.decodeImage()
            except Exception as ex:
                print ex
    def get_pag_select(self):
        if int(self.Total)%14!=0:self.H=(int(self.Total)/14) + 1
        else:self.H=int(self.Total)/14
        Txt = 'Page  '+str(self.Nextpage)+'/ '+str(self.H)
        self['Total'].setText(Txt+'   ['+str(self.Total)+' Data ]')
    def show_all_VOD(self):
        if not self.dakhla:
            self._L_Stalker_3 = []
            self.List_MoviePlayer_2 = []
            self.s = self.s
            T = len(self._New_4)#title,logo,stream_url,MylistVod
            for (name,img,stream,MylistVod) in self._New_4:#(title,_id,'')
                for nom in Lis_Clean:
                    if nom.lower() in name.lower():continue 
                self._L_Stalker_3.append(show_Menu_Stalker_Vod(' '+str(self.s)+'.  '+name,img,stream,MylistVod,'VOD'))
                '''(chan_counter,name,description,piconname,stream_url,playlist_url,category_id,
                    img_src,description4playlist_html,ts_stream)'''
                self.List_MoviePlayer_2.append(('',name,MylistVod,'',stream,'','',img,'',''))
                self.s = self.s + 1
            self._L_Stalker_3.append(show_Menu_Stalker_Vod(' \tNext Page','','','',''))
            self['menu_stalker_Channel_List_VOD'].l.setList(self._L_Stalker_3)
            self['menu_stalker_Channel_List_VOD'].l.setItemHeight(37)
            self['menu_stalker_Channel_List_VOD'].show()
            self.currentList = 'menu_stalker_Channel_List_VOD'
            self['menu_stalker_Channel_List_VOD'].moveToIndex(0)
            self.dakhla = True
            self.get_pag_select()
            self.Get_Infos_select()
            self.Download_Image()
        else:self.session.open(MessageBox, 'show_all_VOD', MessageBox.TYPE_INFO)
    def get_NextPag(self):#######################"
        if self.Total == 'nada':pass
        else:
            cond = 14*self.Nextpage
            if cond < self.Total:
                self.Nextpage = self.Nextpage + 1
            else:
                self.Nextpage = 1
                self.s = 1
            self.get_pag_select()
    def T_NextPag(self,page):
        self._New_4 = []
        a,self._New_4,self.Total = get_donnees_Stalker_New(self.idx,stream=str(self.MyIdx),pg=page,mode='VOD')
        if a:
            self.dakhla = False
            self.show_all_VOD()
        else:pass
    def get_Second_Page(self):################################################################################
        u = self['menu_stalker_Channel_List_VOD'].getSelectionIndex()
        V = len(self._New_4)
        chart = self['menu_stalker_Channel_List_VOD'].getCurrent()[0][0]
        if self['menu_stalker_Channel_List_VOD'].getCurrent()[0][0] != ' \tNext Page' and u!=0:pass
        else:
            if chart == ' \tNext Page':#DOWN
                if int(self.H)== 1:self['menu_stalker_Channel_List_VOD'].moveToIndex(0)
                else:
                    if self.Nextpage == int(self.H):
                        self.Nextpage=self.s = 1
                        self.T_NextPag(self.Nextpage)
                    else:
                        self.Nextpage = self.Nextpage + 1
                        self.s = self.s
                        self.T_NextPag(self.Nextpage)
            else:#UP
                if int(self.H)== 1:self['menu_stalker_Channel_List_VOD'].moveToIndex(13)
                else:
                    if self.Nextpage == 1:
                        self.Nextpage = int(self.H)
                        self.s = 14*(int(self.H)- 1) + 1
                        self.T_NextPag(self.Nextpage)
                    else:
                        self.Nextpage = self.Nextpage - 1
                        self.s = self.s - (14 + V)
                        self.T_NextPag(self.Nextpage)
            self.Get_Infos_select()
            self.Download_Image()
    def get_Tmdb(self):
        if config.plugins.SupTVoDNeWConfig.Tmdb.value == 'enabled':self.lang=config.plugins.SupTVoDNeWConfig.TmdbLang.value
        self.Tmdb_Resultat = []
        name_title = MesImports().Nety_txt(self['menu_stalker_Channel_List_VOD'].getCurrent()[0][0])
        a = Tmdb_Suptvod(searchtitle=name_title,lang=self.lang).get_infos_search()
        if a:
            self.session.open(Screen_MyTMDB_SupTvod,name_title)
        else:self.session.open(MessageBox, 'Unsuccessful Research', MessageBox.TYPE_INFO)
    def ok(self):
        if self['menu_stalker_Channel_List_VOD'].getCurrent()[0][0] == ' \tNext Page':
            self.session.open(MessageBox, 'Use Button Down ', MessageBox.TYPE_INFO)
            return
        Idx = self['menu_stalker_Channel_List_VOD'].getSelectionIndex()
        lala = self['menu_stalker_Channel_List_VOD'].getCurrent()[0][0]
        name = MesImports().Nety_txt(self['menu_stalker_Channel_List_VOD'].getCurrent()[0][0])
        for nom in Lis_Clean:
            if nom.lower() in name.lower():
                self.session.open(MessageBox,'A movie suspected of pornography ', MessageBox.TYPE_INFO)
                return
        if lala == ' \tNext Page':pass
        img = self._New_4[Idx][1]
        Url = self._New_4[Idx][2]
        self.session.open(Xtream_Player_New,recorder_sref=None,liste=self.List_MoviePlayer_2,indxto=Idx,Oldservice=self.initialservice,server=self.idx,_type='vod')
    def Get_Infos_Movies(self):
        Idx = self['menu_stalker_Channel_List_VOD'].getSelectionIndex()
        rat,added,genres_str,age,director,actors,year,desc = 'N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A'
        Dict_Movies = self['menu_stalker_Channel_List_VOD'].getCurrent()[0][3]
        try:rat = str(Dict_Movies[Idx][0])
        except:rat = 'N/A'
        try:added = Dict_Movies[Idx][1]
        except:added = 'N/A'
        try:genres_str = Dict_Movies[Idx][2]
        except:genres_str = 'N/A'
        try:age = Dict_Movies[Idx][3]
        except:age = 'N/A'
        try:director = Dict_Movies[Idx][4]
        except:director = 'N/A'
        try:actors = Dict_Movies[Idx][5]
        except:actors = 'N/A'
        try:year = str(Dict_Movies[Idx][6])
        except:year = 'N/A'
        try:desc = Dict_Movies[Idx][7].encode('utf-8')
        except:desc = 'N/A'
        """_colorize_('My Ip Connect=='+str(t_2),selcolor='cyan')"""
        t1 = MesImports()._colorize_('RAT == '+str(rat),selcolor='cyan')
        self['Infos_Mov_1'].setText(t1)
        t2 = MesImports()._colorize_('ADD == '+str(added),selcolor='cyan')
        self['Infos_Mov_2'].setText(t2)
        t3 = MesImports()._colorize_('GENRE == '+str(genres_str),selcolor='cyan')
        self['Infos_Mov_3'].setText(t3)
        t4 = MesImports()._colorize_('AGE == '+str(age),selcolor='cyan')
        self['Infos_Mov_4'].setText(t4)
        t5 = MesImports()._colorize_('DIRECTOR == '+str(director),selcolor='cyan')
        self['Infos_Mov_5'].setText(t5)
        t6 = MesImports()._colorize_('ACTORS == '+str(actors),selcolor='cyan')
        self['Infos_Mov_6'].setText(t6)
        t7 = MesImports()._colorize_('YEAR == '+str(year),selcolor='cyan')
        self['Infos_Mov_7'].setText(t7)
        t8 = MesImports()._colorize_('DESCR == '+str(desc),selcolor='cyan')
        self['Infos_Mov'].setText(t8)
        if rat!='N/A':self['rating'].setText(rat)
        else:self['rating'].setText('1')
    def Get_Infos_select(self):
        if self['menu_stalker_Channel_List_VOD'].getCurrent()[0][0] != ' \tNext Page':
            txt = MesImports().Nety_txt(self['menu_stalker_Channel_List_VOD'].getCurrent()[0][0])
            self['Infos'].setText(txt)
            self.Download_Image()
        self.Get_Infos_Movies()
    def keyDown(self):
        self[self.currentList].down()
        self.get_Second_Page()
        self.Get_Infos_select()
    def keyUp(self):
        if self['menu_stalker_Channel_List_VOD'].getSelectionIndex() ==0:self.get_Second_Page()
        else:self[self.currentList].up()
        self.Get_Infos_select()
    def left(self):
        self['menu_stalker_Channel_List_VOD'].moveToIndex(0)
        self.Get_Infos_select()
    def right(self):
        mov = len(self._New_4)-1 
        self['menu_stalker_Channel_List_VOD'].moveToIndex(mov)
        self.Get_Infos_select()
    def image_downloaded(self, id):
        self.decodeImage()
    def dataError(self):
        self.session.open(MessageBox, 'login problem try again later', MessageBox.TYPE_INFO, timeout=10)
    def Download_Image(self):
        MyIdx = self['menu_stalker_Channel_List_VOD'].getSelectionIndex()
        self.img = self._New_4[MyIdx][1].encode('utf-8').replace('https','http')
        MesImports().Download_Image(self.img,self['poster'])
    def show_hide_menu(self):
        if not self.showhide:
            if self.hidden:
                self.show()
            else:
                self.hide()
            self.hidden = not self.hidden
    ####################################################### Test Download Movies
    def get_DownloadMovies_choice(self):
        from Plugins.Extensions.SupTVoDNeW.OutilsSup.Sptvnw.MessagBoxSupTvod import MessagBoxSupTvod
        self.MFolder = config.plugins.SupTVoDNeWConfig.M3u.value + 'movie'
        txt = MesImports().Nety_txt(self['menu_stalker_Channel_List_VOD'].getCurrent()[0][0])
        server_ = 'Server=='+self.name
        self.session.openWithCallback(self.userIsSure_1, MessagBoxSupTvod, _('Download With JobManager'), _('Download With FreeDownloadYano'), _('Download Choice Menu    ' + return_version()),_('Your Download Folder==' + self.MFolder), _('You Have Chosen == '+txt), _(server_),  _(self.d_expr), MessagBoxSupTvod.TYPE_YESNO, enable_input = False, default=True)
    def userIsSure_1(self, answer):
        if answer is None:
            self.cancelWizzard()
        if answer == 'A1':
            self.check_download_vod()
        if answer == 'A2':
            self.Download_with_FreeDownloadYano()
        else:
            self.cancelWizzard()
        return
    def cancelWizzard(self):
        pass
    def get_Donnees_Movies(self):
        u = self['menu_stalker_Channel_List_VOD'].getSelectionIndex()
        self.newpath = config.plugins.SupTVoDNeWConfig.M3u.value + 'movie'
        if not os.path.exists(self.newpath):
            os.makedirs(self.newpath)
        self.a,self._url = False,''
        self.vod_entry = self.List_MoviePlayer_2[u]    
        selected_channel = self.List_MoviePlayer_2[u]
        self.stream_url = selected_channel[4]
        playlist_url = selected_channel[5]    
        self.title = selected_channel[1]
        self.a,self._url = get_donnees_Stalker_New(self.idx,indxstream=self.stream_url,mode='VOD')
        return self.a,self._url
    def check_download_vod(self):
        self.get_Donnees_Movies()
        if self.a:
            if self.stream_url != None:
                self.vod_url = self._url
                if '.ts' not in self.vod_url: 
                   self.session.openWithCallback(self.download_vod, MessageBox, _('DOWNLOAD VIDEO?\n%s' % self.title) , type=MessageBox.TYPE_YESNO, timeout = 15, default = False)
                else:
                    message = (_('Only Play'))
                    MesImports().web_info(message)
            else:
                message = (_('No Video to Download\Record!!'))
                MesImports().web_info(message)
        else:
            message = (_('No Video to Download\Record!!'))
            MesImports().web_info(message)
    def download_vod(self, result):#
        if result:
            try: 
                movie = self.newpath+'/'
                self.ende = MesImports().get_Ext_Vod(self._url)
                useragent,filename = MesImports().get_stalker_filename(self.title,self._url)
                cmd = "wget %s -c '%s' -O '%s%s'" % (useragent, self.vod_url, movie, filename)
                JobManager.AddJob(downloadJob(self, cmd, movie + filename, self.title))
                self.createMetaFile(filename)
                self.LastJobView()
                self.session.open(MessageBox, '[DOWNLOAD] ' + self.title+'\n'+self.vod_url.encode('utf-8'), MessageBox.TYPE_INFO, timeout=10)
            except Exception as ex:
                print ex
                print 'ERROR download_vod'
        return 
    def LastJobView(self):
        currentjob = None
        for job in JobManager.getPendingJobs():
            currentjob = job
        if currentjob is not None:
            self.session.open(JobView, currentjob)
        return
    def createMetaFile(self, filename):
        try:
            movie = self.newpath+'/'
            text = re.compile('<[\\/\\!]*?[^<>]*?>')
            text_clear = ''
            if self.vod_entry[2] != None:
                text_clear = text.sub('', self.vod_entry[2])
            serviceref = eServiceReference(4097, 0, movie + filename)
            metafile = open('%s%s.meta' % (movie, filename), 'w') 
            metafile.write('%s\n%s\n%s\n%i\n' % (serviceref.toString(),self.title.replace('\n', ''),text_clear.replace('\n', ''),time()))
            metafile.close()
        except Exception as ex:
            print ex
            print 'ERROR metaFile'
        return
    def Download_with_FreeDownloadYano(self):
        try:
            from Components.Converter.FreeDownloadYano import FreeDownloadYano
            self.ImportYano = True
        except:self.ImportYano = False
        self.MyDictJs = {}
        self.get_Donnees_Movies()
        if self.a:
            self.ende = MesImports().get_Ext_Vod(self._url)
            self.MyDictJs['url']= self._url.encode('utf-8')
            self.MyDictJs['filename']= self.newpath+'/[SupTVoDNeW_'+str(MesImports().get_date())+'] '+MesImports().get_correct_name(self.title)+'.'+self.ende#config.plugins.SupTVoDNeWConfig.M3u.value + 'movie/'
            MesImports().Write_Js(self.MyDictJs)
            if self.ImportYano==True:FreeDownloadYano('download')
            else:self.session.open(MessageBox, 'File FreeDownloadYano Not Found', MessageBox.TYPE_INFO, timeout=10)
        else:self.session.open(MessageBox, 'Link Movie Not Found', MessageBox.TYPE_INFO, timeout=10)
    #################################################################################################choix Page
    def GoToPage(self):
        self.session.openWithCallback(self.Condition,InputBox, title=_('Enter The Page Number '+str(1)+'_'+str(self.H)), windowTitle=_('SupTVoDNeW'), text='', maxSize=False, type=Input.NUMBER)
    def Condition(self,_repns):
        self.Ngrps = MesImports(Indx=_repns).Condition_2(self.H)
        if self.Ngrps == 'nada':pass
        elif self.Ngrps == 'hihi':
            self.session.open(MessageBox, 'Wrong Choice', MessageBox.TYPE_INFO, timeout=5)
        else:
            self.Nextpage=self.Ngrps
            self.s = 14*(int(self.Nextpage)- 1) + 1
            self.T_NextPag(self.Nextpage)
#################################################################################################
########################################################################################## SERIES
class Screen_MyStalkerIptv_Menu_Stalker_SERIES(Screen):
    def __init__(self, session,idx,name,d_expr,_New_1):
        self.session = session
        Screen.__init__(self, session)
        self['actions'] = ActionMap(['DirectionActions','SetupActions','ColorActions'], {'ok': self._Show,
            'cancel': self.Exit_Stlk,
            'red': self.Exit_Stlk,
            'up': self.keyUp,
            'down': self.keyDown,
            'left': self.left,
            'right': self.right
            }, -1)
        self.initialservice = self.session.nav.getCurrentlyPlayingServiceReference()
        self._New_1 = []
        self.idx,self.name,self.d_expr,self._New_1 = idx,name,d_expr,_New_1
        self['Infos'] = Label()
        self['Infos_selct'] = Label()
        self['Infos_selct'].setText('Server : '+self.name)
        self['Dat_Exprt'] = Label()
        self['Dat_Exprt'].setText(self.d_expr)
        self['menu_stalker_Channel_series'] = m2list([])
        self._L_Stalker_ = []
        self.menu_Channels_1 = []
        #self.timer = eTimer()
        self["loading"] = Label()
        self.show_all()
    def Exit_Stlk(self):
        self.session.nav.playService(self.initialservice)
        self.close()
    def show_all(self):
        self._L_Stalker_ = []
        s = 1
        for a in self._New_1:#(title,_id,'')
            title,_id = a[0],a[1]
            self._L_Stalker_.append(show_Menu_Stalker(' '+str(s)+'.  '+title,_id,'SERIES'))
            s = s + 1
        self['menu_stalker_Channel_series'].l.setList(self._L_Stalker_)
        self['menu_stalker_Channel_series'].l.setItemHeight(37)
        self['menu_stalker_Channel_series'].show()
        self.currentList = 'menu_stalker_Channel_series'
    def _Show(self):
        c,G = get_Loading()
        self["loading"].setText(G)
        log('Screen_MyStalkerIptv_Menu_Stalker_Channel')
        self.ok()
    def ok(self):
        self._Channelsts = []
        MyIdx = self['menu_stalker_Channel_series'].getSelectionIndex()
        name = self['menu_stalker_Channel_series'].getCurrent()[0][0]
        for nom in Lis_Clean:
            if nom.lower() in name.lower():
                self.session.open(MessageBox,'A movie suspected of pornography ', MessageBox.TYPE_INFO)
                return
        a,self._Channelsts,self.Total = get_donnees_Stalker_New(self.idx,stream=str(MyIdx),pg=1,mode='SERIES')
        if a:
            cord = self.Total
            self.session.open(Screen_MyStalkerIptv_Menu_Stalker_SERIES_List,self.idx,self.name,self.d_expr,self._Channelsts,cord,MyIdx)
        else:
            self.session.open(MessageBox, 'List [ Live TV ] Not Found\n Check Expiration Date\nOr\nTry Again ', MessageBox.TYPE_INFO)
        self.hid()
    def hid(self):
        self["loading"].setText('')
    def Get_Infos_select(self):
        txt = MesImports().Nety_txt(self['menu_stalker_Channel_series'].getCurrent()[0][0])
        self['Infos'].setText(txt)
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
class Screen_MyStalkerIptv_Menu_Stalker_SERIES_List(Screen):
    def __init__(self, session,idx,name,d_expr,_New_2,cord,MyIdx):
        self.session = session
        Screen.__init__(self, session)
        self['actions'] = HelpableActionMap(self,'StalkerPlayerPlaylist', {'ok': self.ok,
            'cancel_Stalk': self.exit_box,
            'up': self.keyUp,
            'down': self.keyDown,
            'left': self.left,
            'right': self.right
            }, -1)
        self.initialservice = self.session.nav.getCurrentlyPlayingServiceReference()
        self.onShown.append(self.show_all_chang)
        self._New_2 = []
        self.idx,self.name,self.d_expr,self._New_2 = idx,name,d_expr,_New_2
        self['Infos'] = Label()
        self['Infos_selct'] = Label()
        self['Infos_selct'].setText('Server : '+self.name)
        self['Dat_Exprt'] = Label()
        self['Total'] = Label()
        self['Page'] = Label()
        self['Infos_Mov'] = StaticText()
        self['Dat_Exprt'].setText(self.d_expr)
        self['menu_stalker_Channel_List_series'] = m2list([])
        self._L_Stalker_1 = []
        self.menu_Channels_1 = []
        self.List_MoviePlayer_1 = []
        self['poster'] = Pixmap()
        self['poster'].hide()
        self.picload = ePicLoad()
        self.Nextpage = 1
        self.s = 1
        self.Az = 1
        self.H = ''
        self.Total = cord
        for u in range(8):
            self['Infos_Mov_'+str(u+1)] = Label()
        self.rating = 0
        self['rating'] =StaticText()
        if self.Total !='nada':
            self.Az = truediv(int(self.Total),14)
            self.Az = round(self.Az)
            t = str(self.Az).split('.')[1]
            if t !='0':self.Az = int(str(self.Az).split('.')[0])+1
            else:self.Az = int(str(self.Az).split('.')[0])
        self.MyIdx = MyIdx
        self.show_all()
    def exit_box(self):
        self.session.nav.playService(self.initialservice)
        self.close()
    def show_all_chang(self):
        H,Y =MesImports().Recovery_indx()
        if str(Y)== 'True':
            try:
                index_=H
                self['menu_stalker_Channel_List_series'].moveToIndex(int(index_))
                Copy_Volum('indexfil='+str(H)+'\ndakhla=False','indexfil')
                MesImports().Download_Image(self.img,self['poster'])
            except Exception as ex:
                print ex
    def get_pag_select(self):
        if int(self.Total)%14!=0:self.H=(int(self.Total)/14) + 1
        else:self.H=int(self.Total)/14
        Txt = 'Page  '+str(self.Nextpage)+'/ '+str(self.H)
        self['Total'].setText(Txt+'   ['+str(self.Total)+' Data ]')
    def show_all(self):
        self._L_Stalker_1 = []
        self.List_MoviePlayer_1 = []
        self.s = self.s
        T = len(self._New_2)
        for (name,img,stream,ListInfosFilms) in self._New_2:#(title,logo,stream_url,ListInfosFilms)
            for nom in Lis_Clean:
                if nom.lower() in name.lower():continue 
            self._L_Stalker_1.append(show_Menu_Stalker_Series(' '+str(self.s)+'.  '+name,img,stream,ListInfosFilms,'SERIES'))
            '''(chan_counter,name,description,piconname,stream_url,playlist_url,category_id,
                img_src,description4playlist_html,ts_stream)'''
            self.List_MoviePlayer_1.append(('',name,name +' .......','',stream,'','',img,'',''))
            self.s = self.s + 1
        self._L_Stalker_1.append(show_Menu_Stalker_Series(' \tNext Page','','','',''))
        self['menu_stalker_Channel_List_series'].l.setList(self._L_Stalker_1)
        self['menu_stalker_Channel_List_series'].l.setItemHeight(37)
        self['menu_stalker_Channel_List_series'].show()
        self.currentList = 'menu_stalker_Channel_List_series'
        self['menu_stalker_Channel_List_series'].moveToIndex(0)
        self.get_pag_select()
        self.Get_Infos_Movies()
        self.Download_Image()
    def get_NextPag(self):#######################"
        if self.Total == 'nada':pass
        else:
            cond = 14*self.Nextpage
            if cond < self.Total:
                self.Nextpage = self.Nextpage + 1
            else:
                self.Nextpage = 1
                self.s = 1
            self.get_pag_select()
    def T_NextPag(self,page):
        self._New_2 = []
        a,self._New_2,self.Total = get_donnees_Stalker_New(self.idx,stream=str(self.MyIdx),pg=page,mode='SERIES')#get_donnees_Stalker_New(self.idx,stream=str(self.MyIdx),pg=page,mode='SERIES')
        if a:
            self.show_all()
        else:pass
    def get_Second_Page(self):################################################################################
        u = self['menu_stalker_Channel_List_series'].getSelectionIndex()
        V = len(self._New_2)
        chart = self['menu_stalker_Channel_List_series'].getCurrent()[0][0]
        if self['menu_stalker_Channel_List_series'].getCurrent()[0][0] != ' \tNext Page' and u!=0:pass
        else:
            if chart == ' \tNext Page':#DOWN
                if int(self.H)== 1:self['menu_stalker_Channel_List_series'].moveToIndex(0)
                else:
                    if self.Nextpage == int(self.H):
                        self.Nextpage=self.s = 1
                        self.T_NextPag(self.Nextpage)
                    else:
                        self.Nextpage = self.Nextpage + 1
                        self.s = self.s
                        self.T_NextPag(self.Nextpage)
            else:#UP
                if int(self.H)== 1:self['menu_stalker_Channel_List_series'].moveToIndex(13)
                else:
                    if self.Nextpage == 1:
                        self.Nextpage = int(self.H)
                        self.s = 14*(int(self.H)- 1) + 1
                        self.T_NextPag(self.Nextpage)
                    else:
                        self.Nextpage = self.Nextpage - 1
                        self.s = self.s - (14 + V)
                        self.T_NextPag(self.Nextpage)
            self.Get_Infos_select()
            self.Download_Image()
    def Get_Infos_Movies(self):
        Idx = self['menu_stalker_Channel_List_series'].getSelectionIndex()
        rat,added,genres_str,age,director,actors,year,desc = 'N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A'
        Dict_Movies = self['menu_stalker_Channel_List_series'].getCurrent()[0][3]
        try:rat = str(Dict_Movies[Idx][0])
        except:rat = 'N/A'
        try:added = Dict_Movies[Idx][1]
        except:added = 'N/A'
        try:genres_str = Dict_Movies[Idx][2]
        except:genres_str = 'N/A'
        try:age = Dict_Movies[Idx][3]
        except:age = 'N/A'
        try:director = Dict_Movies[Idx][4]
        except:director = 'N/A'
        try:actors = Dict_Movies[Idx][5]
        except:actors = 'N/A'
        try:year = str(Dict_Movies[Idx][6])
        except:year = 'N/A'
        try:desc = Dict_Movies[Idx][7].encode('utf-8')
        except:desc = 'N/A'
        """_colorize_('My Ip Connect=='+str(t_2),selcolor='cyan')"""
        t1 = MesImports()._colorize_('RAT == '+str(rat),selcolor='cyan')
        self['Infos_Mov_1'].setText(t1)
        t2 = MesImports()._colorize_('ADD == '+str(added),selcolor='cyan')
        self['Infos_Mov_2'].setText(t2)
        t3 = MesImports()._colorize_('GENRE == '+str(genres_str),selcolor='cyan')
        self['Infos_Mov_3'].setText(t3)
        t4 = MesImports()._colorize_('AGE == '+str(age),selcolor='cyan')
        self['Infos_Mov_4'].setText(t4)
        t5 = MesImports()._colorize_('DIRECTOR == '+str(director),selcolor='cyan')
        self['Infos_Mov_5'].setText(t5)
        t6 = MesImports()._colorize_('ACTORS == '+str(actors),selcolor='cyan')
        self['Infos_Mov_6'].setText(t6)
        t7 = MesImports()._colorize_('YEAR == '+str(year),selcolor='cyan')
        self['Infos_Mov_7'].setText(t7)
        t8 = MesImports()._colorize_('DESCR == '+str(desc),selcolor='cyan')
        self['Infos_Mov'].setText(t8)
        if rat!='N/A':self['rating'].setText(rat)
        else:self['rating'].setText('1')
    def ok(self):#name,img,stream,ListInfosFilms
        if self['menu_stalker_Channel_List_series'].getCurrent()[0][0] == ' \tNext Page':
            self.session.open(MessageBox, 'Use Button Down ', MessageBox.TYPE_INFO)
            return
        raqm = self['menu_stalker_Channel_List_series'].getSelectionIndex()
        Dict_Movies = self['menu_stalker_Channel_List_series'].getCurrent()[0][3]
        self._Channelsts = []
        lala = self['menu_stalker_Channel_List_series'].getCurrent()[0][0]
        name = MesImports().Nety_txt(lala)
        img = self['menu_stalker_Channel_List_series'].getCurrent()[0][1]
        stream = str(self['menu_stalker_Channel_List_series'].getCurrent()[0][2])
        ListInfosFilms = self['menu_stalker_Channel_List_series'].getCurrent()[0][3]
        a,self._Channelsts = get_donnees_Stalker_New(self.idx,mode='SERIES',url=stream)
        if a:
            cord = self.Total
            self.session.open(Screen_MyStalkerIptv_Menu_Stalker_SERIES_Season,self.idx,self.name,self.d_expr,self._Channelsts,cord,ListInfosFilms[raqm],name,self.MyIdx)
        else:
            self.session.open(MessageBox, 'List [ SERIES TV ] Not Found\n Check Expiration Date\nOr\nTry Again ', MessageBox.TYPE_INFO)
    def Get_Infos_select(self):
        if self['menu_stalker_Channel_List_series'].getCurrent()[0][0] != ' \tNext Page':
            txt = MesImports().Nety_txt(self['menu_stalker_Channel_List_series'].getCurrent()[0][0])
            self['Infos'].setText(txt)
            self.Download_Image()
            self.Get_Infos_Movies()
    def keyDown(self):
        self[self.currentList].down()
        self.get_Second_Page()
        self.Get_Infos_select()
    def keyUp(self):
        if self['menu_stalker_Channel_List_series'].getSelectionIndex() ==0:self.get_Second_Page()
        else:self[self.currentList].up()
        self.Get_Infos_select()
    def left(self):
        self['menu_stalker_Channel_List_series'].moveToIndex(0)
        self.Get_Infos_select()
    def right(self):
        mov = len(self._New_2)-1 
        self['menu_stalker_Channel_List_series'].moveToIndex(mov)
        self.Get_Infos_select()
    def image_downloaded(self, id):
        self.decodeImage()
    def Download_Image(self):
        MyIdx = self['menu_stalker_Channel_List_series'].getSelectionIndex()
        self.img = self._New_2[MyIdx][1].encode('utf-8').replace('https','http')
        MesImports().Download_Image(self.img,self['poster'])
####################
class Screen_MyStalkerIptv_Menu_Stalker_SERIES_Season(Screen):
    def __init__(self, session,idx,name,d_expr,_New_2,cord,ListInfosFilms,nameT,MyIdx):
        self.session = session
        Screen.__init__(self, session)
        self['actions'] = HelpableActionMap(self,'StalkerPlayerPlaylist', {'ok': self.ok,
            'cancel_Stalk': self.exit_box,
            'show_hide': self.show_hide_menu,
            'up': self.keyUp,
            'down': self.keyDown,
            'left': self.left,
            'right': self.right
            }, -1)
        self.initialservice = self.session.nav.getCurrentlyPlayingServiceReference()
        self.onShown.append(self.show_all_chang)
        self._New_2 = []
        self.idx,self.name,self.d_expr,self._New_2,self.InfosFilms,self.NmSerie = idx,name,d_expr,_New_2,ListInfosFilms,nameT
        self['Infos'] = Label()
        self['Infos_selct'] = Label()
        self['Infos_selct'].setText('Server : '+self.name)
        self['Dat_Exprt'] = Label()
        self['Total'] = Label()
        self['Page'] = Label()
        self['Dat_Exprt'].setText(self.d_expr)
        self['menu_stalker_Channel_List_season'] = m2list([])
        self['menu_stalker_Series_season'] = m2list([])
        self['menu_stalker_Series_season'].hide()
        self._L_Stalker_1 = []
        self.menu_Channels_1 = []
        self.List_MoviePlayer_1 = []
        self['poster'] = Pixmap()
        self['poster'].hide()
        self['Infos_Mov'] = StaticText()
        self.picload = ePicLoad()
        self.nextlist = False
        self.showhide = False
        self.hidden = False
        for u in range(8):
            self['Infos_Mov_'+str(u+1)] = Label()
        self.rating = 0
        self['rating'] =StaticText()
        self.Total = cord
        self.MyIdx = MyIdx
        self.show_all()
    def show_all_chang(self):
        if not self.nextlist:pass
        H,Y =MesImports().Recovery_indx()
        if str(Y)== 'True':
            try:
                index_=H
                self['menu_stalker_Series_season'].moveToIndex(int(index_))
                Copy_Volum('indexfil='+str(H)+'\ndakhla=False','indexfil')
                self.Get_Infos_select()
                MesImports().Download_Image(self.img,self['poster'])
                if os.path.exists('%sSupTVoDNeW_pic.jpg' % config.plugins.SupTVoDNeWConfig.Posters.value):
                    self.picfile = '%sSupTVoDNeW_pic.jpg' % config.plugins.SupTVoDNeWConfig.Posters.value
                    self.decodeImage()
            except Exception as ex:
                print ex
    def exit_box(self):
        if self.nextlist:
            self['menu_stalker_Channel_List_season'].show()
            self['menu_stalker_Series_season'].hide()
            self.currentList = 'menu_stalker_Channel_List_season'
            self['menu_stalker_Channel_List_season'].selectionEnabled(1)
            self['menu_stalker_Series_season'].selectionEnabled(0)
            self.nextlist = False
        else:
            self.session.nav.playService(self.initialservice)
            self.close()
    def show_all(self):
        self._L_Stalker_1 = []
        self.s = 1
        T = len(self._New_2)
        for (name,img,stream,ListInfosFilms) in self._New_2:#(title,logo,stream_url,ListInfosFilms)
            for nom in Lis_Clean:
                if nom.lower() in name.lower():continue 
            self._L_Stalker_1.append(show_Menu_Stalker_Series(' '+str(self.s)+'.  '+self.NmSerie+' ['+name+']',img,stream,ListInfosFilms,'SERIES'))
            '''(chan_counter,name,description,piconname,stream_url,playlist_url,category_id,
                img_src,description4playlist_html,ts_stream)'''
            #self.List_MoviePlayer_1.append(('',name,name +' .......','',stream,'','',img,'',''))
            self.s = self.s + 1
        self['menu_stalker_Channel_List_season'].l.setList(self._L_Stalker_1)
        self['menu_stalker_Channel_List_season'].l.setItemHeight(37)
        self['menu_stalker_Channel_List_season'].show()
        self.currentList = 'menu_stalker_Channel_List_season'
        self['menu_stalker_Channel_List_season'].moveToIndex(0)
        self.Get_Infos_Movies()
        self.Download_Image()
    def get_Mylist_Seasons(self):
        self._Channel_ = []
        self.List_MoviePlayer_1 = []
        lala = self['menu_stalker_Channel_List_season'].getCurrent()[0][0]
        image = self['menu_stalker_Channel_List_season'].getCurrent()[0][0]
        name = MesImports().Nety_txt(lala)
        stream = str(self['menu_stalker_Channel_List_season'].getCurrent()[0][2])
        NewList = self['menu_stalker_Channel_List_season'].getCurrent()[0][3]
        self.MyDict = Stalker_New().get_Stalker_Infos(self.idx)
        self.api = self.MyDict['prothost']
        '''(chan_counter,name,description,piconname,stream_url,playlist_url,category_id,
            img_src,description4playlist_html,ts_stream)'''
        #self.List_MoviePlayer_1.append(('',name,name +' .......','',stream,'','',img,'',''))
        for ep in NewList:
            episode=str(ep)
            ep_url = MesImports().get_url_stal_epis(self.api,stream,episode)
            self._Channel_.append(show_Menu_Stalker_Series(name+' ep_'+episode,ep_url,'','','SERIES'))
            self.List_MoviePlayer_1.append(('',name+' ep_'+episode,self.InfosFilms,'',ep_url,'','',image,'',''))
        self['menu_stalker_Channel_List_season'].hide()
        self['menu_stalker_Series_season'].l.setList(self._Channel_)
        self['menu_stalker_Series_season'].l.setItemHeight(37)
        self['menu_stalker_Series_season'].show()
        self.currentList = 'menu_stalker_Series_season'
        self['menu_stalker_Series_season'].selectionEnabled(1)
        self['menu_stalker_Channel_List_season'].selectionEnabled(0)
        self['menu_stalker_Series_season'].moveToIndex(0)
        self.nextlist = True
    def ok(self):####
        if not self.nextlist:
            self.get_Mylist_Seasons()
        else:
            Idx = self['menu_stalker_Series_season'].getSelectionIndex()
            ep_url = self['menu_stalker_Series_season'].getCurrent()[0][1]
            a,stream_url = get_donnees_Stalker_New(int(self.idx),indxstream=ep_url)
            if a:
                self.session.open(Xtream_Player_New,recorder_sref=None,liste=self.List_MoviePlayer_1,indxto=Idx,Oldservice=self.initialservice,server=self.idx,_type='vod_serie')
            else:
                self.session.open(MessageBox, 'Mafihache hihi', MessageBox.TYPE_INFO)
    def Get_Infos_Movies(self):
        rat,added,genres_str,age,director,actors,year,desc = 'N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A'
        Dict_Movies = self.InfosFilms
        try:rat = str(Dict_Movies[0])
        except:rat = 'N/A'
        try:added = Dict_Movies[1]
        except:added = 'N/A'
        try:genres_str = Dict_Movies[2]
        except:genres_str = 'N/A'
        try:age = Dict_Movies[3]
        except:age = 'N/A'
        try:director = Dict_Movies[4]
        except:director = 'N/A'
        try:actors = Dict_Movies[5]
        except:actors = 'N/A'
        try:year = str(Dict_Movies[6])
        except:year = 'N/A'
        try:desc = Dict_Movies[7].encode('utf-8')
        except:desc = 'N/A'
        """_colorize_('My Ip Connect=='+str(t_2),selcolor='cyan')"""
        t1 = MesImports()._colorize_('RAT == '+str(rat),selcolor='cyan')
        self['Infos_Mov_1'].setText(t1)
        t2 = MesImports()._colorize_('ADD == '+str(added),selcolor='cyan')
        self['Infos_Mov_2'].setText(t2)
        t3 = MesImports()._colorize_('GENRE == '+str(genres_str),selcolor='cyan')
        self['Infos_Mov_3'].setText(t3)
        t4 = MesImports()._colorize_('AGE == '+str(age),selcolor='cyan')
        self['Infos_Mov_4'].setText(t4)
        t5 = MesImports()._colorize_('DIRECTOR == '+str(director),selcolor='cyan')
        self['Infos_Mov_5'].setText(t5)
        t6 = MesImports()._colorize_('ACTORS == '+str(actors),selcolor='cyan')
        self['Infos_Mov_6'].setText(t6)
        t7 = MesImports()._colorize_('YEAR == '+str(year),selcolor='cyan')
        self['Infos_Mov_7'].setText(t7)
        t8 = MesImports()._colorize_('DESCR == '+str(desc),selcolor='cyan')
        self['Infos_Mov'].setText(t8)
        if rat!='N/A':self['rating'].setText(rat)
        else:self['rating'].setText('1')
    def Get_Infos_select(self):
        txt = ''
        if self.nextlist:txt = self['menu_stalker_Series_season'].getCurrent()[0][0]
        else:
            txt = MesImports().Nety_txt(self['menu_stalker_Channel_List_season'].getCurrent()[0][0])
            self.Download_Image()
        self['Infos'].setText(txt)
        self.Get_Infos_Movies()
    def keyDown(self):
        self[self.currentList].down()
        self.Get_Infos_select()
    def keyUp(self):
        self[self.currentList].up()
        self.Get_Infos_select()
    def left(self):
        if self.nextlist:self['menu_stalker_Series_season'].moveToIndex(0)
        else:
            self['menu_stalker_Channel_List_season'].moveToIndex(0)
        self.Get_Infos_select()
    def right(self):
        if self.nextlist:
            mov = len(self._Channel_)-1
            self['menu_stalker_Series_season'].moveToIndex(mov)
        else:
            mov = len(self._New_2)-1 
            self['menu_stalker_Channel_List_season'].moveToIndex(mov)
        self.Get_Infos_select()
    def image_downloaded(self, id):
        self.decodeImage()
    def Download_Image(self):
        MyIdx = self['menu_stalker_Channel_List_season'].getSelectionIndex()
        self.img = self._New_2[MyIdx][1].encode('utf-8').replace('https','http')
        MesImports().Download_Image(self.img,self['poster'])
    def show_hide_menu(self):
        if not self.showhide:
            if self.hidden:
                self.show()
            else:
                self.hide()
            self.hidden = not self.hidden
###########################################################################################
#####################################  Menu Show TV #######################################
###########################################################################################
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
#############################################################################################