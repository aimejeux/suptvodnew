#!/usr/bin/python
# -*- coding: utf-8 -*-
################################### modified by aime_jeux ##################################
#############                           Aout 2021                              #############
############################################################################################
Version = 'SupTVoDNeW V_1.0'
def return_version():
    return Version
global Lis_Clean
Lis_Clean_0 = ['isra','israel','adult','adulte','adults','xxx','xx','porn','+18','hard','sex',
               'ado','blowjob','lesbie','travest','frisson']
Lis_Clean_1 = ['sex','xxl','hotclub','venus','playb','hust','libid','penthouse','spice','platinum','amatix','xx',
               'vivid','brazzers','colmax','daring','lover','man-x','man x','manx','pink_x','pink-x','pink x','pinkx','reality kings','stars xxx',
               'pink show','pink-show','pink_show','pinkshow','porn','brazz','lov','adult','hust','candy']
Lis_Clean = Lis_Clean_0+Lis_Clean_1
############################################################################################Tests
Txt_go = 'Access'
Txt_go_1 = 'الدخول'
Txt_suptv = 'This option is for suptv subscribers '
Txt_suptv_1='هذا الاختيار خاص بالمشتركين في سوب تيفي'
Txt_iptv = 'This Choice For a Free Link For Iptv You Need Host, Port, Username, Password'
Txt_iptv_1='هذا الاختيار تحتاج فيه الى وضع الهوست والبور واسم المستخدم كذا كلمة السر'
Txt_stalker = 'With This Choice, You Must Set The Protocol, Host, Port And Mac '
Txt_stalker_1='هذا الاختيار يتوجب عليك وضع البروتوكول و الهوست والبور و الماك'
Txt_m3u = 'This Option Is For M3u'
Txt_m3u_1='M3u هذا الاختيار خاص بملفات المشاهدة'
Txt_settings = 'This Option Is For Settings'
Txt_settings_1='هذا الاختيار خاص بالاعدادات'
Txt_plutotv = 'This Option Is For PlutoTv'
Txt_plutotv_1='هذا الاختيار لمشاهدة بلوتو تيفي'
Txt_plutotvsecond = 'This Option Is For Second PlutoTv'
Txt_plutotvsecond_1='هذا الاختيار لمشاهدة بلوتو تيفي الثاني'
Stirr = 'This Option Is For Free Stirr'
Stirr_1='هذا الاختيار لمشاهدة ستير المجانية'
foldmovies = 'This Option Is For Watching Movies On Your Device'
foldmovies_1='هذا الاختيار لمشاهدة الافلام الموجودة على جهازك'
PLUGIN_PATH = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW'
############################################################################################
from enigma import RT_HALIGN_LEFT, RT_HALIGN_RIGHT, RT_HALIGN_CENTER, RT_VALIGN_CENTER
from Screens.ChannelSelection import ChannelSelection
import os
############################################################################################
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Stalker.InfobarStalker import Xtream_Player_New,Copy_Volum
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Iptv.IptvInfos import IptvInfos,get_Category
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Sptvnw.supcompnt import *
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Sptvnw.Config import *
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Sptvnw.Setup import SupTVoDNeW_Config
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Stalker.logTools import  printD,printE,delLog
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Stalker.StalkerIptv import Screen_MyStalkerIptv
#############################################################################################
from Tools.BoundFunction import boundFunction
from Components.Pixmap import Pixmap
from Components.AVSwitch import AVSwitch
from enigma import ePoint, eSize, eTimer,ePicLoad
from skin import parseColor, parseFont
from Components.Sources.StaticText import StaticText
from twisted.web.client import downloadPage
############################################################################################Tests
delLog()
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.Label import Label
from Components.ActionMap import ActionMap, HelpableActionMap, NumberActionMap
from Plugins.Plugin import PluginDescriptor
PATH_SKINS = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/Skins'
global STREAMS
STREAMS = iptv_streamse()
########################################################################
from enigma import getDesktop
dwidth = getDesktop(0).size().width()
class Screen_MyIptvInfos(Screen):
    def __init__(self, session,cond):
        ########################Session_Skin############################
        if dwidth == 1280:
            with open(PATH_SKINS + '/MyIptvInfosFHD.xml', 'r') as f:
                self.skin = f.read()
                f.close()
        else:
            with open(PATH_SKINS + '/MyIptvInfosFHD.xml', 'r') as f:
                self.skin = f.read()
                f.close()
        self.session = session
        Screen.__init__(self, session)
        self['actions'] = ActionMap(['DirectionActions','SetupActions','ColorActions'], {'ok': self.ok,
            'yellow': self.Settings,
            'blue': self.get_InfoIptvserver,
            '1': self.get_journalsatserver,
            # '2': self.backToIntialService,
            'cancel': self.Exit_plug,
            'red': self.Exit_plug,
            'green': self.ok,
            'up': self.keyUp,
            'down': self.keyDown,
            'left': self.left,
            'right': self.right
            }, -1)
        self.initialservice = self.session.nav.getCurrentlyPlayingServiceReference()
        self.cond = cond
        self.category = False
        self.categorylivestreams = False
        self['Titlet'] = Label()
        self['Infos'] = Label()
        self['Infoselect'] = Label()
        self['Infoserveriptv'] = Label()
        self['Version'] = Label(_(Version))
        self['menu'] = m2list([])
        self['menu_category'] = m2list([])
        self['menu_category'].hide()
        self.get_ListIptvFnl()
        self.MylistCategory = []#
    def Exit_plug(self):
        if self.category:
            self['menu'].show()
            self['menu'].selectionEnabled(1)
            self.currentList = 'menu'
            self['menu_category'].moveToIndex(0)
            self['menu_category'].selectionEnabled(0)
            self['menu_category'].hide()
            self.category = False
        else:self.close()
    def get_InfoIptvserver(self):
        '''get only infos server iptv'''
        _iptv = self['menu'].getCurrent()[0][0]
        url   = self['menu'].getCurrent()[0][1]
        if '[IPTV]' in _iptv and self.currentList == 'menu':
            self._dons = STREAMS.get_Infos_FreeAbonnement(url)
            self['Infoserveriptv'].setText(self._dons)
    def get_ListIptvFnl(self):
        '''('suptvod', _('Suptvod')), ('freeiptv', _('Freeiptv')),('stalker', _('Stalker')),('all'''
        self.MyFolderXml = []
        ListIptv = get_InfosOXml()
        i = 1
        if self.cond == 'freeiptv':
            for name,url in ListIptv:
                self.MyFolderXml.append(show_Menu_SuptvodNews(' '+str(i)+'.  '+name+' [IPTV]',url))
                i = i + 1
        self['menu'].l.setList(self.MyFolderXml)
        self['menu'].l.setItemHeight(37)
        self.currentList = 'menu'
        self['Infos'].setText(self['menu'].getCurrent()[0][1])
    def get_journalsatserver(self):#
        Nvjournalsat = get_journalsat()
        self.get_ListIptvFnl()
    def ok(self):
        '''menu_category'''
        '''(chan_counter,name,description,piconname,stream_url,playlist_url,category_id,
            img_src,description4playlist_html,ts_stream)'''
        if self.currentList == 'menu':
            self.MylistCategory = []
            url = self['menu'].getCurrent()[0][1]
            a,self.MylistCategory = get_Category(url,Category='categ')
            if a:
                self['menu_category'].show()
                self['menu_category'].l.setList(self.MylistCategory)
                self['menu_category'].l.setItemHeight(37)
                self.currentList = 'menu_category'
                self['menu_category'].selectionEnabled(1)
                self['menu'].hide()
                self['menu'].selectionEnabled(0)
                self['Titlet'].setText(self['menu_category'].getCurrent()[0][1])
                self.category = True
            else:self.session.open(MessageBox, 'No Data Found Try Again', MessageBox.TYPE_INFO)
        elif self.currentList == 'menu_category' and self.category:
            self.MyNewlist = []
            Categ = self.Get_infos_go()
            if Categ!='':
                Title = self['menu_category'].getCurrent()[0][1]
                _urlo =self['menu'].getCurrent()[0][1]
                for nom in Lis_Clean:
                    if nom.lower() in Title.lower():
                        self.session.open(MessageBox,'A movie suspected of pornography ', MessageBox.TYPE_INFO)
                        return
                a,self.MyNewlist = get_Category(self.Url,Category=Categ)
                if a and len(self.MyNewlist)!=0 and Categ=='get_live_categories':self.session.open(Screen_MyIptv_LiveStreams,self.MyNewlist,Title,_urlo)
                elif a and len(self.MyNewlist)!=0 and Categ=='get_series_categories':self.session.open(Screen_MyIptv_LiveSries,self.MyNewlist,Title,_urlo)
                else:self.session.open(MessageBox, 'No Data Found Try Again', MessageBox.TYPE_INFO)
            else:self.session.open(MessageBox, 'No Data Found Try Again', MessageBox.TYPE_INFO)
        else:pass
    def Get_infos_go(self):
        self.conds_ = ''
        try:self.Url = self['menu_category'].getCurrent()[0][5]
        except:self.conds_ = ''
        if 'get_live' in self.Url or 'get_vod_categories' in self.Url:self.conds_ = 'get_live_categories'
        elif 'get_series' in self.Url:self.conds_ = 'get_series_categories'
        else:self.conds_ = ''
        return self.conds_
    def Settings(self):
        self.session.open(SupTVoDNeW_Config)
    def Get_Len_List(self):
        if self.currentList == 'menu':self['Infos'].setText(self['menu'].getCurrent()[0][1])
        else:
            self['Infos'].setText(self['menu_category'].getCurrent()[0][5])
            self['Titlet'].setText(self['menu_category'].getCurrent()[0][1])
    def keyDown(self):
        self[self.currentList].down()
        self['Infos'].setText(self['menu'].getCurrent()[0][1])
        self.Get_Len_List()
        self.Get_Infos_select()
    def keyUp(self):
        self[self.currentList].up()
        self.Get_Len_List()#self['Infos'].setText(self['menu'].getCurrent()[0][1])
        self.Get_Infos_select()
    def left(self):
        self[self.currentList].pageUp()
        self.Get_Len_List()#self['Infos'].setText(self['menu'].getCurrent()[0][1])
        self.Get_Infos_select()
    def right(self):
        self[self.currentList].pageDown()
        self.Get_Len_List()#self['Infos'].setText(self['menu'].getCurrent()[0][1])
        self.Get_Infos_select()
    def Nety_txt(self,txt):
        if '.  ' in txt:
            txt = txt.split('.  ')[1]
        return txt
    def Get_Infos_select(self):
        Hd = ''
        self['Infoserveriptv'].setText('')
        if self.currentList == 'menu':
            Hd = self.Nety_txt(self['menu'].getCurrent()[0][0])
        else:
            Hd = self.Nety_txt(self['menu_category'].getCurrent()[0][1])
        self['Infoselect'].setText(Hd)
######################################### get_live get_vod_categories #################################################
class Screen_MyIptv_LiveStreams(Screen):
    def __init__(self, session,MyNewlist,Title,_urlo):
        ########################Session_Skin############################
        if dwidth == 1280:
            with open(PATH_SKINS + '/MyIptv_LiveStreamsFHD.xml', 'r') as f:
                self.skin = f.read()
                f.close()
        else:
            with open(PATH_SKINS + '/MyIptv_LiveStreamsFHD.xml', 'r') as f:
                self.skin = f.read()
                f.close()
        self.session = session
        Screen.__init__(self, session)
        self['actions'] = ActionMap(['DirectionActions','SetupActions','ColorActions'], {'ok': self.ok,
            'yellow': self.Settings,
            'cancel': self.Exit_plug,
            'red': self.Exit_plug,
            'green': self.ok,
            'blue': self.show_hide_menu,
            'up': self.keyUp,
            'down': self.keyDown,
            'left': self.left,
            'right': self.right
            }, -1)
        self.initialservice = self.session.nav.getCurrentlyPlayingServiceReference()
        self.onShown.append(self.show_all_chang)
        self.MyNewlist = MyNewlist
        self.Titlet = Title
        self._urlo = _urlo
        self['Titlet'] = Label()
        self['Titlet'].setText(self.Titlet)
        self.category = False
        self.dakhla = False
        self.showhide = False
        self.hidden = False
        self.picfile = ''
        self['poster'] = Pixmap()
        self['poster'].hide()
        self.picload = ePicLoad()
        self['serveriptv'] = Label()
        self['Infos'] = Label()
        self['Infoselect'] = Label()
        self['Infoserveriptv'] = StaticText()
        self['Version'] = Label(_(Version))
        self['menu'] = m2list([])
        self['menu_category'] = m2list([])
        self['menu_category'].hide()
        self.get_ListIptvFnl()
        self.MylistCategory = []##
    def Exit_plug(self):
        if self.category:
            self['menu'].show()
            self['menu'].selectionEnabled(1)
            self.currentList = 'menu'
            self['menu_category'].moveToIndex(0)
            self['menu_category'].selectionEnabled(0)
            self['menu_category'].hide()
            self.category = False
        else:self.close()
    def Recovery_indx(self):
        H = '0'
        Milef = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/Cfg/indexfil'
        if os.path.isfile(Milef):
            file_write = open(Milef, 'r')
            data = file_write.readlines()
            file_write.close()
            H = data[0].replace('\n', '').replace('\t', '').replace('\r', '')
            H = H.split('=')[1].replace(' ','')
            Y = data[1].replace('\n', '').replace('\t', '').replace('\r', '')
            Y = Y.split('=')[1].replace(' ','')
        return H,Y
    def show_all_chang(self):
        H,Y =self.Recovery_indx()
        if str(Y)== 'True':
            try:
                index_=H
                self['menu_category'].moveToIndex(int(index_))
                Copy_Volum('indexfil='+str(H)+'\ndakhla=False','indexfil')
                self.picfile = '%sMyIptvNew_pic.jpg' % config.plugins.SupTVoDNeWConfig.Posters.value
                if os.path.exists(self.picfile):
                    self.picfile = self.picfile
                else:self.picfile = PLUGIN_PATH + '/img/playlist/default.jpg'
                self.decodeImage()
            except Exception as ex:
                print ex
    def get_ListIptvFnl(self):
        self['menu'].l.setList(self.MyNewlist)
        self['menu'].l.setItemHeight(37)
        self.currentList = 'menu'
        self['Infos'].setText(self['menu'].getCurrent()[0][5])
        self.get_InfoIptvserver()
    def get_journalsatserver(self):#
        Nvjournalsat = get_journalsat()
        self.get_ListIptvFnl()
    def ok(self):
        '''menu_category'''
        '''(chan_counter,name,description,piconname,stream_url,playlist_url,category_id,
            img_src,description4playlist_html,ts_stream)'''
        if self.currentList == 'menu':
            self.MylistCategory = []
            url = self['menu'].getCurrent()[0][5]
            for nom in Lis_Clean:
                if nom.lower() in self['menu'].getCurrent()[0][1].lower():
                    self.session.open(MessageBox,'A movie suspected of pornography ', MessageBox.TYPE_INFO)
                    return
            a,self.MylistCategory = get_Category(url,Category='get_live_categories')#get_Category(url)
            if a:
                self['menu_category'].show()
                self['menu_category'].l.setList(self.MylistCategory)
                self['menu_category'].l.setItemHeight(37)
                self.currentList = 'menu_category'
                self['menu_category'].selectionEnabled(1)
                self['menu'].hide()
                self['menu'].selectionEnabled(0)
                self.category = True
                self.Get_Len_List()
                self.Download_Image()
            else:self.session.open(MessageBox, 'No Data Found Try Again', MessageBox.TYPE_INFO)
        elif self.currentList == 'menu_category' and self.category:
            Idx = self['menu_category'].getSelectionIndex()
            self.List_MoviePlayer_1 = []
            if len(self.MylistCategory)!=0:
                for nom in Lis_Clean:
                    if nom.lower() in self['menu_category'].getCurrent()[0][1].lower():
                        self.session.open(MessageBox,'A movie suspected of pornography ', MessageBox.TYPE_INFO)
                        return
                Y = ''
                for X in self.MylistCategory:
                    self.List_MoviePlayer_1.append((X[0][0],X[0][1],X[0][2],X[0][3],X[0][4],X[0][5],X[0][6],X[0][7],X[0][8],X[0][9]))
                self.session.open(Xtream_Player_New,recorder_sref=None,liste=self.List_MoviePlayer_1,indxto=Idx,Oldservice=self.initialservice,server=0,_type='MyIptv')
            else:self.session.open(MessageBox, 'No Data Found Try Again', MessageBox.TYPE_INFO)
        else:pass
    def Settings(self):
        self.session.open(SupTVoDNeW_Config)
    def Get_Len_List(self):
        if self.currentList == 'menu':self['Infos'].setText(self['menu'].getCurrent()[0][5])
        else:
            self['Infos'].setText(self['menu_category'].getCurrent()[0][4])
            discrpt = self['menu_category'].getCurrent()[0][2].encode('utf-8')
            discrpt = discrpt.replace('\n\n','')
            #self.session.open(MessageBox, str(discrpt), MessageBox.TYPE_INFO)
            self['Infoserveriptv'].setText(str(discrpt))
    def keyDown(self):
        self[self.currentList].down()
        self['Infos'].setText(self['menu'].getCurrent()[0][1])
        self.Get_Len_List()
        self.Get_Infos_select()
    def keyUp(self):
        self[self.currentList].up()
        self.Get_Len_List()#self['Infos'].setText(self['menu'].getCurrent()[0][1])
        self.Get_Infos_select()
    def left(self):
        self[self.currentList].pageUp()
        self.Get_Len_List()#self['Infos'].setText(self['menu'].getCurrent()[0][1])
        self.Get_Infos_select()
    def right(self):
        self[self.currentList].pageDown()
        self.Get_Len_List()#self['Infos'].setText(self['menu'].getCurrent()[0][1])
        self.Get_Infos_select()
    def Nety_txt(self,txt):
        if '.  ' in txt:
            txt = txt.split('.  ')[1]
        return txt
    def Get_Infos_select(self):
        Hd = ''
        #self['Infoserveriptv'].setText('')
        if self.currentList == 'menu':
            Hd = self.Nety_txt(self['menu'].getCurrent()[0][1])
        else:
            Hd = self.Nety_txt(self['menu_category'].getCurrent()[0][1])
            self.Download_Image()
        self['Infoselect'].setText(Hd)
    def show_hide_menu(self):
        if not self.showhide:
            if self.hidden:
                self.show()
            else:
                self.hide()
            self.hidden = not self.hidden
    def get_InfoIptvserver(self):
        self._dons = STREAMS.get_Infos_FreeAbonnement(self._urlo)
        self['serveriptv'].setText(self._dons)
    #################################################### Image
    def image_downloaded(self, id):
        self.decodeImage()
    def Download_Image(self):
        img = ''
        try:img = self['menu_category'].getCurrent()[0][7].encode('utf-8').replace('https','http').replace('\n','')
        except:img=''
        if len(img)==0:
            self.picfile = PLUGIN_PATH + '/img/playlist/default.jpg'
            self.decodeImage()
            return
        elif img.find('http') == -1:
            self.picfile = PLUGIN_PATH + '/img/playlist/default.jpg'
            self.decodeImage()
            return
        else:
            self.picfile = '%sMyIptvNew_pic.jpg' % config.plugins.SupTVoDNeWConfig.Posters.value
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
    def show_hide_menu(self):
        if not self.showhide:
            if self.hidden:
                self.show()
            else:
                self.hide()
            self.hidden = not self.hidden
######################################### get_series_categories get_series #################################################
class Screen_MyIptv_LiveSries(Screen):
    def __init__(self, session,MyNewlist,Title,_urlo):
        ########################Session_Skin############################
        if dwidth == 1280:
            with open(PATH_SKINS + '/MyIptv_LiveSriesFHD.xml', 'r') as f:
                self.skin = f.read()
                f.close()
        else:
            with open(PATH_SKINS + '/MyIptv_LiveSriesFHD.xml', 'r') as f:
                self.skin = f.read()
                f.close()
        self.session = session
        Screen.__init__(self, session)
        self['actions'] = ActionMap(['DirectionActions','SetupActions','ColorActions'], {'ok': self.ok,
            'yellow': self.Settings,
            'cancel': self.Exit_plug,
            'red': self.Exit_plug,
            'green': self.ok,
            'blue': self.show_hide_menu,
            'up': self.keyUp,
            'down': self.keyDown,
            'left': self.left,
            'right': self.right
            }, -1)
        self.initialservice = self.session.nav.getCurrentlyPlayingServiceReference()
        #self.onShown.append(self.show_all_chang)
        self.MyNewlist = MyNewlist
        self.Titlet = Title
        self._urlo = _urlo
        self['Titlet'] = Label()
        self['Titlet'].setText(self.Titlet)
        self.category = False
        self.dakhla = False
        self.showhide = False
        self.hidden = False
        self.picfile = ''
        self['poster'] = Pixmap()
        self['poster'].hide()
        self.picload = ePicLoad()
        self['serveriptv'] = Label()
        self['Infos'] = Label()
        self['Infoselect'] = Label()
        self['Infoserveriptv'] = StaticText()
        self['Version'] = Label(_(Version))
        self['menu'] = m2list([])
        self['menu_category'] = m2list([])
        self['menu_category'].hide()
        self.get_ListIptvFnl()
        self.MylistCategory = []##
    def Exit_plug(self):
        if self.category:
            self['menu'].show()
            self['menu'].selectionEnabled(1)
            self.currentList = 'menu'
            self['menu_category'].moveToIndex(0)
            self['menu_category'].selectionEnabled(0)
            self['menu_category'].hide()
            self.category = False
        else:self.close()
    def Recovery_indx(self):
        H = '0'
        Milef = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/Cfg/indexfil'
        if os.path.isfile(Milef):
            file_write = open(Milef, 'r')
            data = file_write.readlines()
            file_write.close()
            H = data[0].replace('\n', '').replace('\t', '').replace('\r', '')
            H = H.split('=')[1].replace(' ','')
            Y = data[1].replace('\n', '').replace('\t', '').replace('\r', '')
            Y = Y.split('=')[1].replace(' ','')
        return H,Y
    def show_all_chang(self):
        H,Y =self.Recovery_indx()
        if str(Y)== 'True':
            try:
                index_=H
                self['menu_category'].moveToIndex(int(index_))
                Copy_Volum('indexfil='+str(H)+'\ndakhla=False','indexfil')
                # self.picfile = '%sMyIptvNewSeries_pic.jpg' % config.plugins.SupTVoDNeWConfig.Posters.value
                # if os.path.exists(self.picfile):
                    # self.picfile = self.picfile
                # else:self.picfile = PLUGIN_PATH + '/img/playlist/default.jpg'
                # self.decodeImage()
            except Exception as ex:
                print ex
    def get_ListIptvFnl(self):
        self['menu'].l.setList(self.MyNewlist)
        self['menu'].l.setItemHeight(37)
        self.currentList = 'menu'
        self['Infos'].setText(self['menu'].getCurrent()[0][5])
        self.get_InfoIptvserver()
    def get_journalsatserver(self):#
        Nvjournalsat = get_journalsat()
        self.get_ListIptvFnl()
    def ok(self):
        '''menu_category'''
        '''(chan_counter,name,description,piconname,stream_url,playlist_url,category_id,
            img_src,description4playlist_html,ts_stream)'''
        if self.currentList == 'menu':
            self.MylistCategory = []
            url = self['menu'].getCurrent()[0][5]
            for nom in Lis_Clean:
                if nom.lower() in self['menu'].getCurrent()[0][1].lower():
                    self.session.open(MessageBox,'A movie suspected of pornography ', MessageBox.TYPE_INFO)
                    return
            a,self.MylistCategory = get_Category(url,Category='get_live_categories')#get_Category(url)
            if a:
                self['menu_category'].show()
                self['menu_category'].l.setList(self.MylistCategory)
                self['menu_category'].l.setItemHeight(37)
                self.currentList = 'menu_category'
                self['menu_category'].selectionEnabled(1)
                self['menu'].hide()
                self['menu'].selectionEnabled(0)
                self.category = True
                self.Get_Len_List()
                #self.Download_Image()
            else:self.session.open(MessageBox, 'No Data Found Try Again', MessageBox.TYPE_INFO)
        elif self.currentList == 'menu_category' and self.category:
            self.MylistSeason = []
            self.getUrl = self['menu_category'].getCurrent()[0][5]
            for nom in Lis_Clean:
                if nom.lower() in self['menu_category'].getCurrent()[0][1].lower():
                    self.session.open(MessageBox,'A movie suspected of pornography ', MessageBox.TYPE_INFO)
                    return
            a,self.MylistSeason = get_Category(self.getUrl,Category='get_live_categories')
            if a and len(self.MylistSeason)!=0:
                Title = self['menu_category'].getCurrent()[0][1]
                _urlo =self.getUrl
                self.session.open(Screen_MyIptv_LiveSeasonEpisodes,self.MylistSeason,Title,_urlo)
            else:self.session.open(MessageBox, 'No Data Found Try Again', MessageBox.TYPE_INFO)
        else:pass
    def Settings(self):
        self.session.open(SupTVoDNeW_Config)
    def Get_Len_List(self):
        if self.currentList == 'menu':self['Infos'].setText(self['menu'].getCurrent()[0][5])
        else:
            self['Infos'].setText(self['menu_category'].getCurrent()[0][5])
    def keyDown(self):
        self[self.currentList].down()
        self['Infos'].setText(self['menu'].getCurrent()[0][1])
        self.Get_Len_List()
        self.Get_Infos_select()
    def keyUp(self):
        self[self.currentList].up()
        self.Get_Len_List()#self['Infos'].setText(self['menu'].getCurrent()[0][1])
        self.Get_Infos_select()
    def left(self):
        self[self.currentList].pageUp()
        self.Get_Len_List()#self['Infos'].setText(self['menu'].getCurrent()[0][1])
        self.Get_Infos_select()
    def right(self):
        self[self.currentList].pageDown()
        self.Get_Len_List()#self['Infos'].setText(self['menu'].getCurrent()[0][1])
        self.Get_Infos_select()
    def Nety_txt(self,txt):
        if '.  ' in txt:
            txt = txt.split('.  ')[1]
        return txt
    def Get_Infos_select(self):
        Hd = ''
        #self['Infoserveriptv'].setText('')
        if self.currentList == 'menu':
            Hd = self.Nety_txt(self['menu'].getCurrent()[0][1])
        else:
            Hd = self.Nety_txt(self['menu_category'].getCurrent()[0][1])
            #self.Download_Image()
        self['Infoselect'].setText(Hd)
    def show_hide_menu(self):
        if not self.showhide:
            if self.hidden:
                self.show()
            else:
                self.hide()
            self.hidden = not self.hidden
    def get_InfoIptvserver(self):
        self._dons = STREAMS.get_Infos_FreeAbonnement(self._urlo)
        self['serveriptv'].setText(self._dons)
    #################################################### Image
    def image_downloaded(self, id):
        self.decodeImage()
    def Download_Image(self):
        img = ''
        try:img = self['menu_category'].getCurrent()[0][7].encode('utf-8').replace('https','http').replace('\n','')
        except:img=''
        if len(img)==0:
            self.picfile = PLUGIN_PATH + '/img/playlist/default.jpg'
            self.decodeImage()
            return
        elif img.find('http') == -1:
            self.picfile = PLUGIN_PATH + '/img/playlist/default.jpg'
            self.decodeImage()
            return
        else:
            self.picfile = '%sMyIptvNewSeries_pic.jpg' % config.plugins.SupTVoDNeWConfig.Posters.value
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
    def show_hide_menu(self):
        if not self.showhide:
            if self.hidden:
                self.show()
            else:
                self.hide()
            self.hidden = not self.hidden
######################################### get_season get_episode #################################################
class Screen_MyIptv_LiveSeasonEpisodes(Screen):
    def __init__(self, session,MyNewlist,Title,_urlo):
        ########################Session_Skin############################
        if dwidth == 1280:
            with open(PATH_SKINS + '/LiveSeasonEpisodesFHD.xml', 'r') as f:
                self.skin = f.read()
                f.close()
        else:
            with open(PATH_SKINS + '/LiveSeasonEpisodesFHD.xml', 'r') as f:
                self.skin = f.read()
                f.close()
        self.session = session
        Screen.__init__(self, session)
        self['actions'] = ActionMap(['DirectionActions','SetupActions','ColorActions'], {'ok': self.ok,
            'yellow': self.Settings,
            'cancel': self.Exit_plug,
            'red': self.Exit_plug,
            'green': self.ok,
            'blue': self.show_hide_menu,
            'up': self.keyUp,
            'down': self.keyDown,
            'left': self.left,
            'right': self.right
            }, -1)
        self.initialservice = self.session.nav.getCurrentlyPlayingServiceReference()
        self.onShown.append(self.show_all_chang)
        self.MyNewlist = MyNewlist
        self.Titlet = Title
        self._urlo = _urlo
        self['Titlet'] = Label()
        self['Titlet'].setText(self.Titlet)
        self.category = False
        self.dakhla = False
        self.showhide = False
        self.hidden = False
        self.picfile = ''
        self['poster'] = Pixmap()
        self['poster'].hide()
        self.picload = ePicLoad()
        self['serveriptv'] = Label()
        self['Infos'] = Label()
        self['Infoselect'] = Label()
        self['Infoserveriptv'] = StaticText()
        self['Version'] = Label(_(Version))
        self['menu'] = m2list([])
        self['menu_category'] = m2list([])
        self['menu_category'].hide()
        self.get_ListIptvFnl()
        self.MylistCategory = []##
    def Exit_plug(self):
        if self.category:
            self['menu'].show()
            self['menu'].selectionEnabled(1)
            self.currentList = 'menu'
            self['menu_category'].moveToIndex(0)
            self['menu_category'].selectionEnabled(0)
            self['menu_category'].hide()
            self.category = False
        else:self.close()
    def Recovery_indx(self):
        H = '0'
        Milef = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/Cfg/indexfil'
        if os.path.isfile(Milef):
            file_write = open(Milef, 'r')
            data = file_write.readlines()
            file_write.close()
            H = data[0].replace('\n', '').replace('\t', '').replace('\r', '')
            H = H.split('=')[1].replace(' ','')
            Y = data[1].replace('\n', '').replace('\t', '').replace('\r', '')
            Y = Y.split('=')[1].replace(' ','')
        return H,Y
    def show_all_chang(self):
        H,Y =self.Recovery_indx()
        if str(Y)== 'True':
            try:
                index_=H
                self['menu_category'].moveToIndex(int(index_))
                Copy_Volum('indexfil='+str(H)+'\ndakhla=False','indexfil')
                self.picfile = '%sMyIptvSeriesNew_pic.jpg' % config.plugins.SupTVoDNeWConfig.Posters.value
                if os.path.exists(self.picfile):
                    self.picfile = self.picfile
                else:self.picfile = PLUGIN_PATH + '/img/playlist/default.jpg'
                self.decodeImage()
            except Exception as ex:
                print ex
    def get_ListIptvFnl(self):
        self['menu'].l.setList(self.MyNewlist)
        self['menu'].l.setItemHeight(37)
        self.currentList = 'menu'
        self['Infos'].setText(self['menu'].getCurrent()[0][5])
        self.get_InfoIptvserver()
    def get_journalsatserver(self):#
        Nvjournalsat = get_journalsat()
        self.get_ListIptvFnl()
    def ok(self):
        '''menu_category'''
        '''(chan_counter,name,description,piconname,stream_url,playlist_url,category_id,
            img_src,description4playlist_html,ts_stream)'''
        if self.currentList == 'menu':
            self.MylistCategory = []
            url = self['menu'].getCurrent()[0][5]
            for nom in Lis_Clean:
                if nom.lower() in self['menu'].getCurrent()[0][1].lower():
                    self.session.open(MessageBox,'A movie suspected of pornography ', MessageBox.TYPE_INFO)
                    return
            a,self.MylistCategory = get_Category(url,Category='get_live_categories')#get_Category(url)
            if a:
                self['menu_category'].show()
                self['menu_category'].l.setList(self.MylistCategory)
                self['menu_category'].l.setItemHeight(37)
                self.currentList = 'menu_category'
                self['menu_category'].selectionEnabled(1)
                self['menu'].hide()
                self['menu'].selectionEnabled(0)
                self.category = True
                self.Get_Len_List()
                self.Download_Image()
            else:self.session.open(MessageBox, 'No Data Found Try Again', MessageBox.TYPE_INFO)
        elif self.currentList == 'menu_category' and self.category:
            Idx = self['menu_category'].getSelectionIndex()
            self.List_MoviePlayer_1 = []
            if len(self.MylistCategory)!=0:
                for nom in Lis_Clean:
                    if nom.lower() in self['menu_category'].getCurrent()[0][1].lower():
                        self.session.open(MessageBox,'A movie suspected of pornography ', MessageBox.TYPE_INFO)
                        return
                Y = ''
                for X in self.MylistCategory:
                    self.List_MoviePlayer_1.append((X[0][0],self.Titlet+' ['+X[0][1]+']',X[0][2],X[0][3],X[0][4],X[0][5],X[0][6],X[0][7],X[0][8],X[0][9]))
                self.session.open(Xtream_Player_New,recorder_sref=None,liste=self.List_MoviePlayer_1,indxto=Idx,Oldservice=self.initialservice,server=0,_type='MyIptv')
            else:self.session.open(MessageBox, 'No Data Found Try Again', MessageBox.TYPE_INFO)
        else:pass
    def Settings(self):
        self.session.open(SupTVoDNeW_Config)
    def Get_Len_List(self):
        if self.currentList == 'menu':self['Infos'].setText(self['menu'].getCurrent()[0][5])
        else:
            self['Infos'].setText(self['menu_category'].getCurrent()[0][4])
            discrpt = self['menu_category'].getCurrent()[0][2].encode('utf-8')
            discrpt = discrpt.replace('\n\n','')
            #self.session.open(MessageBox, str(discrpt), MessageBox.TYPE_INFO)
            self['Infoserveriptv'].setText(str(discrpt))
    def keyDown(self):
        self[self.currentList].down()
        self['Infos'].setText(self['menu'].getCurrent()[0][1])
        self.Get_Len_List()
        self.Get_Infos_select()
    def keyUp(self):
        self[self.currentList].up()
        self.Get_Len_List()#self['Infos'].setText(self['menu'].getCurrent()[0][1])
        self.Get_Infos_select()
    def left(self):
        self[self.currentList].pageUp()
        self.Get_Len_List()#self['Infos'].setText(self['menu'].getCurrent()[0][1])
        self.Get_Infos_select()
    def right(self):
        self[self.currentList].pageDown()
        self.Get_Len_List()#self['Infos'].setText(self['menu'].getCurrent()[0][1])
        self.Get_Infos_select()
    def Nety_txt(self,txt):
        if '.  ' in txt:
            txt = txt.split('.  ')[1]
        return txt
    def Get_Infos_select(self):
        Hd = ''
        #self['Infoserveriptv'].setText('')
        if self.currentList == 'menu':
            Hd = self.Nety_txt(self['menu'].getCurrent()[0][1])
        else:
            Hd = self.Nety_txt(self['menu_category'].getCurrent()[0][1])
            self.Download_Image()
        self['Infoselect'].setText(Hd)
    def show_hide_menu(self):
        if not self.showhide:
            if self.hidden:
                self.show()
            else:
                self.hide()
            self.hidden = not self.hidden
    def get_InfoIptvserver(self):
        self._dons = STREAMS.get_Infos_FreeAbonnement(self._urlo)
        self['serveriptv'].setText(self._dons)
    #################################################### Image
    def image_downloaded(self, id):
        self.decodeImage()
    def Download_Image(self):
        img = ''
        try:img = self['menu_category'].getCurrent()[0][7].encode('utf-8').replace('https','http').replace('\n','')
        except:img=''
        if len(img)==0:
            self.picfile = PLUGIN_PATH + '/img/playlist/default.jpg'
            self.decodeImage()
            return
        elif img.find('http') == -1:
            self.picfile = PLUGIN_PATH + '/img/playlist/default.jpg'
            self.decodeImage()
            return
        else:
            self.picfile = '%sMyIptvSeriesNew_pic.jpg' % config.plugins.SupTVoDNeWConfig.Posters.value
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
    def show_hide_menu(self):
        if not self.showhide:
            if self.hidden:
                self.show()
            else:
                self.hide()
            self.hidden = not self.hidden