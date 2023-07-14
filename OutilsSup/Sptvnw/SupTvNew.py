#!/usr/bin/python
# -*- coding: utf-8 -*-
################################### modified by aime_jeux ##################################
#############                           Aout 2021                              #############
############################################################################################
from Components.Sources.StaticText import StaticText
import copy
from Tools.Directories import fileExists
from Tools.BoundFunction import boundFunction
from supcompnt import *
from Setup import SupTVoDNeW_Config
from Plugins.Plugin import PluginDescriptor
from Components.ActionMap import ActionMap, HelpableActionMap, NumberActionMap
from Screens.Screen import Screen
from Components.Sources.List import List
from enigma import eTimer, RT_HALIGN_LEFT, RT_HALIGN_RIGHT, RT_HALIGN_CENTER, RT_VALIGN_CENTER, eListboxPythonMultiContent, gFont, getDesktop, ePicLoad, eServiceReference, iPlayableService
from Components.MenuList import MenuList
from Tools.LoadPixmap import LoadPixmap
from Components.Pixmap import Pixmap
from Components.Label import Label
from Components.ServiceEventTracker import ServiceEventTracker, InfoBarBase
from Screens.InfoBarGenerics import InfoBarSeek, InfoBarAudioSelection, InfoBarSubtitleSupport
from Screens.MessageBox import MessageBox
import os
from os import listdir as os_listdir, path as os_path, system as os_system
from time import time
import sys
from datetime import datetime
from Screens.Console import Console
import re
from twisted.web.client import downloadPage
from enigma import eAVSwitch
from Components.AVSwitch import AVSwitch
from skin import loadSkin
import hashlib
from Components.Task import Task, Job, job_manager as JobManager, Condition
from Screens.TaskView import JobView
from urllib import quote_plus
from Screens.InputBox import InputBox
from Components.Input import Input
from Screens.Standby import Standby
from os import system
import socket
socket.setdefaulttimeout(NTIMEOUT)
system("ifconfig eth0 | awk '/HWaddr/ {printf $5}' > /tmp/mac")
PLUGIN_PATH = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW'
PATH_SKINS = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/Skins'
#loadSkin(PLUGIN_PATH + '/skin.xml')
from enigma import addFont
# try:
    # addFont('%s/MyriadPro-Regular.otf' % PLUGIN_PATH, 'RegularIPTV', 100, 1)
# except Exception as ex:
    # print ex
# try:
    # import commands
# except Exception as ex:
    # print ex
# try:
    # import servicewebts
    # print 'OK servicewebts'
# except Exception as ex:
    # print ex
    # print 'ERROR servicewebts'
#####################################################################MOD BY AIME_JEUX
global STREAMS
STREAMS = iptv_streamse()
dwidth = getDesktop(0).size().width()
def nextAR():
    try:
        STREAMS.ar_id_player += 1
        if STREAMS.ar_id_player > 6:
            STREAMS.ar_id_player = 0
        eAVSwitch.getInstance().setAspectRatio(STREAMS.ar_id_player)
        print 'STREAMS.ar_id_player NEXT %s' % VIDEO_ASPECT_RATIO_MAP[STREAMS.ar_id_player]
        return VIDEO_ASPECT_RATIO_MAP[STREAMS.ar_id_player]
    except Exception as ex:
        print ex
        return 'nextAR ERROR %s' % ex
def prevAR():
    try:
        STREAMS.ar_id_player -= 1
        if STREAMS.ar_id_player == -1:
            STREAMS.ar_id_player = 6
        eAVSwitch.getInstance().setAspectRatio(STREAMS.ar_id_player)
        print 'STREAMS.ar_id_player PREV %s' % VIDEO_ASPECT_RATIO_MAP[STREAMS.ar_id_player]
        return VIDEO_ASPECT_RATIO_MAP[STREAMS.ar_id_player]
    except Exception as ex:
        print ex
        return 'prevAR ERROR %s' % ex
ChangeImage = True
class nPlaylist_New(Screen):
    def __init__(self, session,urliptv):
        if config.plugins.SupTVoDNeWConfig.notification.value == 'enabled' and config.plugins.SupTVoDNeWConfig.Activskin.value == 'yes':
            ImportSkinwithimag()
            with open(PATH_SKINS + '/nPlaylistFHD.xml', 'r') as f:
                self.skin = f.read()
                f.close()
        else:
            if dwidth == 1280:
                with open(PATH_SKINS + '/nPlaylistFHD.xml', 'r') as f:
                    self.skin = f.read()
                    f.close()
            else:
                with open(PATH_SKINS + '/nPlaylistFHD.xml', 'r') as f:
                    self.skin = f.read()
                    f.close()
        Screen.__init__(self, session)
        self.session = session
        self.urliptv = urliptv
        self.urlsecour = urliptv
        self['InfosServer'] = Label()
        self['InfosServer1'] = Label()
        self['InfosServer2'] = Label()
        f1,f2,f3 = '','',''
        if self.urliptv == 'Suptvod':
            f1,f2,f3 = Get_line()
            f1 = colorize(f1,selcolor='cyan')
            f2 = colorize(f2,selcolor='cyan')
            f3 = colorize(f3.replace('Remaining','Remaining:'),selcolor='cyan')
        else:
            _dons = STREAMS.get_Infos_FreeAbonnement(self.urliptv)
            if 'makach' not in str(_dons):
                H = str(_dons).split('\n')
                f1 = colorize(H[2],selcolor='cyan')
                f2 = colorize(H[3],selcolor='cyan')
                f3 = colorize(H[4],selcolor='cyan')
            else:
                f1 = colorize('status : None',selcolor='cyan')
                f2 = colorize('exp_date : None',selcolor='cyan')
                f3 = colorize('max_connections : None',selcolor='cyan')
        self['InfosServer'].setText(f1.replace(']',''))
        self['InfosServer1'].setText(f2.replace(']',''))
        self['InfosServer2'].setText(f3.replace(']',''))
        if self.urliptv == 'Suptvod':
            STREAMS.read_config()
            STREAMS.get_Infos_Abonnement()
        self.KeyYellow()
        self.ExtChanel_List = []
        self.MyListHistoriqIndx = []
        self.NextListIptv = []
        self.Len_list = 0
        self.index = STREAMS.list_index
        self.banned = False
        self.TocToc = False
        self.banned_text = ''
        self.mlist = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
        self.mlist.l.setFont(0, gFont(FONT_0[0], FONT_0[1]))
        self.mlist.l.setFont(1, gFont(FONT_1[0], FONT_1[1]))
        self.mlist.l.setItemHeight(BLOCK_H)
        self['feedlist'] = self.mlist
        self.mlist.setList(map(channelEntryIPTVplaylist, self.channel_list))
        self.mlist.onSelectionChanged.append(self.update_description)
        self['description'] = StaticText()
        self['playlist'] = Label()
        self['playlist'].setText(STREAMS.playlistname)
        self['info'] = Label()
        self['NbrFilms'] = Label()
        self['backtovideo'] = Label()
        self['backtovideo'].setText('Retour à la vidéo')
        self['exit_menu'] = Label()
        self['exit_menu'].setText('Exit / Menu')
        self['green_infsrvr'] = Label()
        self['green_infsrvr'].setText('Infos Serveur')
        self['yellow_config'] = Label()
        self['yellow_config'].setText('Paramètres / Settings')
        self['TitleFilms'] = Label()
        self.UrlCategory = ''
        self.List_Url_Cond = ''
        self.onShown.append(self.show_all)
        self['poster'] = Pixmap()
        self['poster'].hide()
        self.picload = ePicLoad()
        self.picfile = ''
        self.update_desc = True
        self.pass_ok = False
        self.oldService = self.session.nav.getCurrentlyPlayingServiceReference()
        STREAMS.oldServiceK = self.oldService
        self['actions'] = HelpableActionMap(self,'nStreamPlayerPlaylist', {'homePlaylist': self.start_portal,
            'retourservice': self.testretourservice,
            'ok': self.ok,
            'InfosOXml': self.getmesinfosxml,
            'getinfosserver': self.getinfosserver,
            'MyConfig': self.configsuptvod,
            'backToVideo': self.back_to_video,
            'exitPlugin': self.exit_box,
            'prevPlaylist': self.prevPlaylist,
            'nextPlaylist': self.nextPlaylist,
            'moreInfo': self.show_more_info,
            'power': self.power}, -1)
        self.temp_index = 0
        self.indexHisCat = 0
        self.temp_channel_list = None
        self.temp_playlistname = None
        self.url_tmp = None
        self.video_back = False
        self.passwd_ok = False
        self.kharja = False
        self.IndxCategory = 0
        self.IndxStream = 0
        self.IndxMovies = 0
        return
    def testretourservice(self):
        self.session.open(MessageBox, str(self.channel_list), type=MessageBox.TYPE_INFO)
    def showIMDB(self,txt=None):
        if txt:#'.mp4' in self.url or '.mkv' in self.url or '.flv' in self.url or '.avi' in self.url:
            if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/TMBD/plugin.pyo"):
                from Plugins.Extensions.TMBD.plugin import TMBD
                text_clear = txt
                text = charRemove(text_clear)
                self.session.open(TMBD, text, False)
            elif os.path.exists("/usr/lib/enigma2/python/Plugins/Extensions/IMDb/plugin.pyo"):
                from Plugins.Extensions.IMDb.plugin import IMDB
                text_clear = txt
                text = charRemove(text_clear)
                HHHHH = text
                self.session.open(IMDB, HHHHH)
            else:
                text_clear = txt
                self.session.open(MessageBox, _('Prochainement \n'+text_clear), MessageBox.TYPE_WARNING)
        else:
            self.session.open(MessageBox, _('Only VOD Movie allowed!!!'), MessageBox.TYPE_WARNING)
    def getmesinfosxml(self):
        _Donneesxml = get_InfosOXml()
        self.session.open(MessageBox, str(_Donneesxml), type=MessageBox.TYPE_INFO)
    def KeyYellow(self,cond=None):
        if self.urliptv == 'Suptvod':self.urliptv = STREAMS.NR1JwTlhSYVV6a3lZakpS
        else:
            if cond:self.urliptv = self.urlsecour
            else:self.urliptv = self.urliptv
        STREAMS.get_list(self.urliptv)
        self.channel_list = STREAMS.iptv_list
        self.new_list_0 = copy.copy(self.channel_list)
        #self.update_channellist()#######################################################################################################
    def getinfosserver(self):
        text_server = ''
        if self.urliptv == 'Suptvod':
            text_server = Get_line(cond='hy')
        else:
			text_server = STREAMS.get_Infos_FreeAbonnement(self.urliptv)
        self.session.open(MessageBox, str(text_server), type=MessageBox.TYPE_INFO)
    def configsuptvod(self):
        self.session.open(SupTVoDNeW_Config)
    def show_more_info(self):
        selected_channel = self.channel_list[self.mlist.getSelectionIndex()]
        text = re.compile('<[\\/\\!]*?[^<>]*?>')
        text_clear = ''
        text_clear = text.sub('', selected_channel[2])
        self.session.open(MessageBox, text_clear, type=MessageBox.TYPE_INFO)
    def prevPlaylist(self):
        if STREAMS.prev_page_url != None:
            STREAMS.get_list(STREAMS.prev_page_url)
            self.update_channellist()
        return
    def nextPlaylist(self):
        if STREAMS.next_page_url != None:
            STREAMS.get_list(STREAMS.next_page_url)
            self.update_channellist()
        return
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
            print 'ERROR showImage'
    def image_downloaded(self, id):
        self.decodeImage()
    def exit_box(self):
        adad = 'IndexFilms:'+str(0)
        Copy_lineFilms(adad,'')
        self.session.nav.playService(self.oldService)# a corrige plus tard
        self.close()
    def exit(self, message = None):
        if message:
            self.session.nav.playService(self.oldService)# a corrige plus tard
            self.close()
    def update_description(self):
        TextFils = ''
        self.index = self.mlist.getSelectionIndex()
        try:
            Titles = self.channel_list[self.index][1]
            Titles = colorize(Titles,selcolor='cyan')
            Titles = Titles.replace(']','')
            self['TitleFilms'].setText('TiTrEs :  '+str(Titles))
        except:self['TitleFilms'].setText('')
        self.Len_list = str(len(STREAMS.iptv_list))
        if self.Len_list !='0' and self.channel_list[0][1] == 'Nouveau':TextFils = self.Len_list+':  Category'
        if self.Len_list !='0' and self.channel_list[0][1] == 'VOD':TextFils = ''
        if self.Len_list !='0' and self.channel_list[0][1] != 'VOD' and self.channel_list[0][1] != 'Nouveau':TextFils = 'CoOl  : '+self.Len_list+'  Data'
        TextFils = colorize(TextFils,selcolor='cyan')
        TextFils = TextFils.replace(']','')
        self['NbrFilms'].setText(TextFils)
        if self.update_desc:
            try:
                self['info'].setText('')
                self['description'].setText('')
                self['poster'].instance.setPixmapFromFile(PLUGIN_PATH + '/img/clear.png')
                selected_channel = self.channel_list[self.index]
                if selected_channel[7] != '':
                    if selected_channel[7].find('http') == -1:
                        self.picfile = PLUGIN_PATH + '/img/playlist/' + selected_channel[7]
                        self.decodeImage()
                        print 'LOCAL DESCR IMG'
                    else:
                        if STREAMS.img_loader == False:
                            self.picfile = '%s/nstream_tmp_pic.jpg' % STREAMS.images_tmp_path
                        else:
                            m = hashlib.md5()
                            m.update(selected_channel[7])
                            cover_md5 = m.hexdigest()
                            self.picfile = '%s/%s.jpg' % (STREAMS.images_tmp_path, cover_md5)
                        if os.path.exists(self.picfile) == False or STREAMS.img_loader == False:
                            downloadPage(selected_channel[7], self.picfile).addCallback(self.image_downloaded)
                        else:
                            self.decodeImage()
                if selected_channel[2] != None:
                    description = selected_channel[2]
                    description_2 = description.split(' #-# ')
                    if description_2:
                        self['description'].setText(description_2[0])
                        if len(description_2) > 1:
                            self['info'].setText(description_2[1])
                    else:
                        self['description'].setText(description)
            except Exception as ex:
                print ex
                print 'exe update_description'
        return
    def start_portal(self):
        self.Url_Final = ''
        if  self.List_Url_Cond == '' or len(self.channel_list) == 0:
            self.exit_box()
        else:
            self.AAAA = self.channel_list[0][5]
            self.BBBB = self.channel_list[0][4]
            if self.AAAA != None:
                if 'streams' in self.AAAA:
                    STREAMS.get_list(self.urliptv)#
                    self.channel_list = STREAMS.iptv_list
                    self.index = self.IndxCategory
                    self.update_channellist()
                    indexto = Return_Index('indexcategories=')
                    self.mlist.moveToIndex(int(indexto))
                else:self.exit_box()
            elif self.BBBB != None:
                playlist_url = self.List_Url_Cond_cat
                STREAMS.get_list(playlist_url)
                self.update_channellist_2(self.new_list_1)
                self.index = self.indexstreams
                self.update_channellist()
                indexto = Return_Index('indexstreams=')
                self.mlist.moveToIndex(int(indexto))
    def update_channellist_2(self,ListIptv):
        print '--------------------- UPDATE CHANNEL LIST ----------------------------------------'
        if STREAMS.xml_error != '':
            print '### update_channellist ######URL#############'
            print STREAMS.clear_url
        self.update_desc = False
        self.channel_list = ListIptv
        self.mlist.setList(map(channelEntryIPTVplaylist, self.channel_list))
        self.mlist.moveToIndex(self.index)
        self.update_desc = True
        self.update_description()
    def update_channellist(self):
        print '--------------------- UPDATE CHANNEL LIST ----------------------------------------'
        if STREAMS.xml_error != '':
            print '### update_channellist ######URL#############'
            print STREAMS.clear_url
        self.channel_list = STREAMS.iptv_list
        self.update_desc = False
        self.mlist.setList(map(channelEntryIPTVplaylist, self.channel_list))
        if self.channel_list[0][1] == 'Nouveau':
            self.indexHisCat=self.indexHisCat
            self.mlist.moveToIndex(self.indexHisCat)
        else:self.mlist.moveToIndex(0)
        self.update_desc = True
        self['playlist'].setText(STREAMS.playlistname)
        self.update_description()
    def show_all_corrected (self):
        chan_tulpe = ('','Not Found','','','','','','','','')
        self.channel_list.append(chan_tulpe)
    def show_all(self):
        try:
            if self.passwd_ok == False:
                self.channel_list = STREAMS.iptv_list
                if self.channel_list[0][1] != 'Nouveau' and self.channel_list[0][1] != 'VOD':
                    self.index=Copy_lineFilms('','tt')
                    self.mlist.moveToIndex(self.index)
                else:
                    self.index=self.index
                if self.channel_list[0][1] == '':
                    self.show_all_corrected()
                    self.mlist.setList(map(channelEntryIPTVplaylist, self.channel_list))
                else:
                    self.mlist.setList(map(channelEntryIPTVplaylist, self.channel_list))
                    self.mlist.selectionEnabled(1)
                    self.mlist.moveToIndex(self.index)
                    self.decodeImage()
            self.passwd_ok = False
        except Exception as ex:
            print ex
            print 'EXX showall'
    def back_to_video(self):
        try:
            if STREAMS.video_status:
                self.video_back = False
                self.load_from_tmp()
                self.channel_list = STREAMS.iptv_list
                self.session.open(Xtream_Player_New)
            else:self.session.open(MessageBox, "Pas De Lien Pour Le Film Demandé ", type=MessageBox.TYPE_INFO)
        except Exception as ex:
            self.session.open(MessageBox, "Pas De Lien Pour Le Film Demandé ", type=MessageBox.TYPE_INFO)
    def ok(self):
        if len(self.channel_list) == 0:
            self.session.open(MessageBox, 'Ooops Not Found\n What Are You Looking For With An Empty List !!!!! ', type=MessageBox.TYPE_INFO)
            self.KeyYellow(cond='coucou')
        selected_channel_history = []
        if STREAMS.xml_error != '':
            self.index_tmp = self.mlist.getSelectionIndex()
        else:
            selected_channel = self.channel_list[self.mlist.getSelectionIndex()]
            STREAMS.list_index = self.mlist.getSelectionIndex()
            title = selected_channel[1]
            if self.channel_list[0][1] == 'Nouveau':self.indexHisCat=self.mlist.getSelectionIndex()
            selected_channel_history = (STREAMS.list_index,title,selected_channel[4])
            STREAMS.iptv_list_history.append(selected_channel_history)
            self.temp_index = -1
            if selected_channel[9] != None:
                self.temp_index = self.index
            else:
                self.ok_checked()
    def ok_checked(self):
        self.bibitou = ''
        try:
            if self.temp_index > -1:
                self.index = self.temp_index
            selected_channel = STREAMS.iptv_list[self.index]
            stream_url = selected_channel[4]
            playlist_url = selected_channel[5]
            self.bibitou = selected_channel[1]
            if playlist_url != None:
                if 'categories' in playlist_url:
                    self.IndxCategory = self.index
                    STREAMS.get_list(playlist_url)
                    self.List_Url_Cond_cat = playlist_url
                    self.List_Url_Cond = playlist_url
                    self.indexcategories = self.mlist.getSelectionIndex()
                    NNN = Replace_Index('indexcategories=',self.indexcategories)
                    self.index = self.index
                    self.kharja = True
                    self.update_channellist()
                    self.new_list_1 = copy.copy(self.channel_list)#self.channel_list
                if 'streams' in playlist_url:
                        STREAMS.get_list(playlist_url)
                        self.List_Url_Cond = playlist_url
                        self.indexstreams = self.mlist.getSelectionIndex()
                        NNN = Replace_Index('indexstreams=',self.indexstreams)
                        self.index = self.index
                        self.update_channellist()
                        self.new_list_2 = copy.copy(self.channel_list)#self.channel_list
                else:
                    if '.ts' not in playlist_url and 'mp4' not in playlist_url:
                        STREAMS.get_list(playlist_url)
                        self.List_Url_Cond = playlist_url
                        self.indexstreams = self.mlist.getSelectionIndex()
                        NNN = Replace_Index('indexstreams=',self.indexstreams)
                        self.update_channellist()
            elif stream_url != None:
                if 'vod.suptv' in stream_url:
                    self.indexTS = self.mlist.getSelectionIndex()
                    NNN = Replace_Index('indexTs=',self.indexTS)
                    self.set_tmp_list()
                    STREAMS.video_status = True
                    STREAMS.play_vod = False
                    self.session.open(Xtream_Player_New)
                else:
                    if stream_url.find('.ts') > 0:
                        self.set_tmp_list()
                        STREAMS.video_status = True
                        STREAMS.play_vod = False
                        self.List_Url_Cond = stream_url
                        self.indexTS = self.mlist.getSelectionIndex()
                        NNN = Replace_Index('indexTs=',self.indexTS)
                        self.update_indexTS = False
                        self.update_channellist_2(self.new_list_2)
                        self.session.open(Xtream_Player_New)
                    else:
                        self.indexTS = self.mlist.getSelectionIndex()
                        NNN = Replace_Index('indexTs=',self.indexTS)
                        self.update_indexTS = False
                        self.set_tmp_list()
                        STREAMS.video_status = True
                        STREAMS.play_vod = True
                        self.update_channellist_2(self.new_list_2)
                        self.session.open(Xtream_Player_New)
                    adad = 'IndexFilms:'+str(self.indexTS)
                    Copy_lineFilms(adad,'')
        except Exception as ex:
            print ex
            print 'ok_checked'
    def myPassInput(self):
        self.passwd_ok = True
        self.session.openWithCallback(self.checkPasswort, InputBox, title='Please enter a passwort', text='****', maxSize=4, type=Input.PIN)
    def checkPasswort(self, number):
        a = '%s' % number
        b = '%s' % STREAMS.password
        if a == b:
            debug(self.passwd_ok, 'self.passwd_ok')
            self.ok_checked()
        else:
            self.passwd_ok = False
            self.session.open(MessageBox, 'WRONG PASSWORD', type=MessageBox.TYPE_ERROR, timeout=5)
    def check_standby(self, myparam = None):
        debug(myparam, 'check_standby')
        if myparam:
            self.power()
    def power(self):
        self.session.nav.stopService()
        self.session.open(Standby)
    def set_tmp_list(self):
        self.index = self.mlist.getSelectionIndex()
        STREAMS.list_index = self.index
        STREAMS.list_index_tmp = STREAMS.list_index
        STREAMS.iptv_list_tmp = STREAMS.iptv_list
        STREAMS.playlistname_tmp = STREAMS.playlistname
        STREAMS.url_tmp = STREAMS.url
        STREAMS.next_page_url_tmp = STREAMS.next_page_url
        STREAMS.next_page_text_tmp = STREAMS.next_page_text
        STREAMS.prev_page_url_tmp = STREAMS.prev_page_url
        STREAMS.prev_page_text_tmp = STREAMS.prev_page_text
    def load_from_tmp(self):
        debug('load_from_tmp')
        STREAMS.iptv_list = STREAMS.iptv_list_tmp
        STREAMS.list_index = STREAMS.list_index_tmp
        STREAMS.playlistname = STREAMS.playlistname_tmp
        STREAMS.url = STREAMS.url_tmp
        STREAMS.next_page_url = STREAMS.next_page_url_tmp
        STREAMS.next_page_text = STREAMS.next_page_text_tmp
        STREAMS.prev_page_url = STREAMS.prev_page_url_tmp
        STREAMS.prev_page_text = STREAMS.prev_page_text_tmp
        self.index = STREAMS.list_index
##########################################################################################################################
def selectPlayer():
    defaultPlayer = 'systemplayer'
    serviceApp = False
    try:
        if os.path.exists('/usr/lib/enigma2/python/Plugins/SystemPlugins/ServiceApp'):
            from Plugins.SystemPlugins.ServiceApp.plugin import config_serviceapp
            if config_serviceapp.servicemp3.replace.value:
                defaultPlayer = config_serviceapp.servicemp3.player.value
            else:
                defaultPlayer = 'systemPlayer'
            serviceApp = True
        else:
            defaultPlayer = 'systemPlayer'
    except:
        defaultPlayer = 'systemPlayer'
    return (defaultPlayer, serviceApp)
class Xtream_Player_New(Screen, InfoBarBase, IPTVInfoBarShowHide, InfoBarSeek, InfoBarAudioSelection, InfoBarSubtitleSupport):
    STATE_IDLE = 0
    STATE_PLAYING = 1
    STATE_PAUSED = 2
    ENABLE_RESUME_SUPPORT = True
    ALLOW_SUSPEND = True
    def __init__(self, session, recorder_sref = None,liste=None,indxto=None,Oldservice=None):
        if dwidth == 1280:
            with open(PATH_SKINS + '/Xtream_PlayerFHD.xml', 'r') as f:
                self.skin = f.read()
                f.close()
        else:
            with open(PATH_SKINS + '/Xtream_PlayerFHD.xml', 'r') as f:
                self.skin = f.read()
                f.close()
        Screen.__init__(self, session)
        InfoBarBase.__init__(self, steal_current_service=True)
        IPTVInfoBarShowHide.__init__(self)
        InfoBarSeek.__init__(self, actionmap='InfobarSeekActions')
        if STREAMS.disable_audioselector == False:
            InfoBarAudioSelection.__init__(self)
        InfoBarSubtitleSupport.__init__(self)
        self.InfoBar_NabDialog = Label()
        self['Descriptions'] = Label()
        self.session = session
        self.Oldservice = Oldservice
        self.service = None
        self['state'] = Label('')
        self['cont_play'] = Label('')
        self.cont_play = STREAMS.cont_play
        self.film_quality = None
        ret = '-'
        sert = '/h'
        self.recorder_sref = None
        self['cover'] = Pixmap()
        self['cover_'] = Pixmap()
        self['cover_'].hide()
        mer = 'R'
        self.picload = ePicLoad()
        self.picfile = ''
        sew = 'r'
        if recorder_sref:
            self.recorder_sref = recorder_sref
            self.session.nav.playService(recorder_sref)
        else:
            frt = 'd/*'
            if liste!=None and indxto!=None:
                STREAMS.iptv_list = liste
                STREAMS.list_index = indxto
                self.Oldservice = Oldservice
            self.vod_entry = STREAMS.iptv_list[STREAMS.list_index]
            self.vod_url = self.vod_entry[4]
            self.title = self.vod_entry[1]
            self.descr = self.vod_entry[2]
            Copy_TouTou(str(STREAMS.list_index)+'\n'+str(self.vod_url)+'\n'+str(self.title))
        self.TrialTimer = eTimer()
        self.TrialTimer.callback.append(self.trialWarning)
        print 'evEOF=%d' % iPlayableService.evEOF
        self.__event_tracker = ServiceEventTracker(screen=self, eventmap={iPlayableService.evSeekableStatusChanged: self.__seekableStatusChanged,
            iPlayableService.evStart: self.__serviceStarted,
            iPlayableService.evEOF: self.__evEOF})
        self['actions'] = HelpableActionMap(self, 'nStreamPlayerVOD', {'exitVOD': self.exit,
            'moreInfoVOD': self.show_more_info,
            'playnPreviousvideo_box': self.playnPreviousvideo_box,
            'playnextvideo_box': self.playnextvideo_box,
            'nextAR': self.nextAR,
            'prevAR': self.prevAR,
            'stopVOD': self.stopnew,
            'timeshift_autoplay': self.timeshift_autoplay,
            'timeshift': self.timeshift,
            'autoplay': self.autoplay,
            'prevVideo': self.prevVideo,
            'nextVideo': self.nextVideo,
            'power': self.power_off}, -1)
        self.get_player()
        self.onFirstExecBegin.append(self.play_vod)
        self.onShown.append(self.setCover)
        self.onPlayStateChanged.append(self.__playStateChanged)
        self.StateTimer = eTimer()
        self.StateTimer.callback.append(self.trialWarning)
        if STREAMS.trial != '':
            self.StateTimer.start(STREAMS.trial_time * 1000, True)
        self.state = self.STATE_PLAYING
        self.timeshift_url = None
        self.timeshift_title = None
        self.onShown.append(self.show_info)
        self.error_message = ''
        return
    def get_player(self):
        self.rds = 4097
        defaultPlayer,serviceApp = selectPlayer()
        if serviceApp:
            if defaultPlayer == 'gstplayer':self.rds = 5001
            elif defaultPlayer == 'exteplayer3':self.rds = 5002
        return self.rds
    def showAfterSeek(self):
        if isinstance(self, IPTVInfoBarShowHide):
            self.doShow()
    def timeshift_autoplay(self):
        if self.timeshift_url:
            try:
                self.reference = eServiceReference(self.rds, 0, self.timeshift_url)
                self.reference.setName(self.timeshift_title)
                self.session.nav.playService(self.reference)
            except Exception as ex:
                print ex
                print 'EXC timeshift 1'
        else:
            if self.cont_play:
                self.cont_play = False
                self['cont_play'].setText('Continue play OFF')
                self.session.open(MessageBox, 'Continue play OFF', type=MessageBox.TYPE_INFO, timeout=3)
            else:
                self.cont_play = True
                self['cont_play'].setText('Continue play ON')
                self.session.open(MessageBox, 'Continue play ON', type=MessageBox.TYPE_INFO, timeout=3)
            STREAMS.cont_play = self.cont_play
    def timeshift(self):
        if self.timeshift_url:
            try:
                self.reference = eServiceReference(self.rds, 0, self.timeshift_url)
                self.reference.setName(self.timeshift_title)
                self.session.nav.playService(self.reference)
            except Exception as ex:
                print ex
                print 'EXC timeshift 2'
    def autoplay(self):
        if self.cont_play:
            self.cont_play = False
            self['cont_play'].setText('Continue play OFF')
            self.session.open(MessageBox, 'Continue play OFF', type=MessageBox.TYPE_INFO, timeout=3)
        else:
            self.cont_play = True
            self['cont_play'].setText('Continue play ON')
            self.session.open(MessageBox, 'Continue play ON', type=MessageBox.TYPE_INFO, timeout=3)
        STREAMS.cont_play = self.cont_play
    def show_info(self):
        if STREAMS.play_vod == True:
            self['state'].setText(' PLAY     >')
        self.hideTimer.start(5000, True)
        if self.cont_play:
            self['cont_play'].setText('Continue play ON')
        else:
            self['cont_play'].setText('Continue play OFF')
    def playnextvideo_box(self):
        index = STREAMS.list_index + 1
        video_counter = len(STREAMS.iptv_list)
        if index < video_counter and STREAMS.iptv_list[index][4] != None:
            descr = ''
            if STREAMS.iptv_list[index][2]:
                descr = STREAMS.iptv_list[index][2]
            title = STREAMS.iptv_list[index][1] + '\n\n' + str(descr)
            self.session.openWithCallback(self.playnextvideo, MessageBox, _('PLAY NEXT VIDEO?\n%s') % title, type=MessageBox.TYPE_YESNO)
        return
    def playnPreviousvideo_box(self):
        index = STREAMS.list_index - 1
        video_counter = len(STREAMS.iptv_list)
        if index >= -1 and STREAMS.iptv_list[index][4] != None:
            descr = ''
            if STREAMS.iptv_list[index][2]:
                descr = STREAMS.iptv_list[index][2]
            title = STREAMS.iptv_list[index][1] + '\n\n' + str(descr)
            self.session.openWithCallback(self.playPreviousvideo, MessageBox, _('PLAY PREVIOUS VIDEO?\n%s') % title, type=MessageBox.TYPE_YESNO)
        return
    def playnextvideo(self, message = None):
        if message:
            try:
                self.nextVideo()
            except Exception as ex:
                print ex
                print 'EXC playnextvideo'
    def playPreviousvideo(self, message = None):#Add By aime_jeux
        if message:
            try:
                self.prevVideo()
            except Exception as ex:
                print ex
                print 'EXC playPreviousvideo'
    def nextVideo(self):
        try:
            if STREAMS.list_index == len(STREAMS.iptv_list)-1:index = 0#Add by aime_jeux
            else:index = STREAMS.list_index + 1#Add by aime_jeux
            video_counter = len(STREAMS.iptv_list)
            if index < video_counter:
                if STREAMS.iptv_list[index][4] != None:
                    STREAMS.list_index = index
                    adad = 'IndexFilms:'+str(index)
                    NvIdx = Copy_lineFilms(adad,'')
                    self.player_helper()
        except Exception as ex:
            print ex
            print 'EXC nextVideo'
        return
    def prevVideo(self):
        try:
            if STREAMS.list_index == 0:index = len(STREAMS.iptv_list)-1#Add by aime_jeux
            else:index = STREAMS.list_index - 1#Add by aime_jeux
            if index > -1:
                if STREAMS.iptv_list[index][4] != None:
                    STREAMS.list_index = index
                    adad = 'IndexFilms:'+str(index)
                    NvIdx = Copy_lineFilms(adad,'')
                    self.player_helper()
        except Exception as ex:
            print ex
            print 'EXC prevVideo'
        return
    def player_helper(self):
        self.show_info()
        if self.vod_entry:
            self.vod_entry = STREAMS.iptv_list[STREAMS.list_index]
            self.vod_url = self.vod_entry[4]
            self.title = self.vod_entry[1]
            self.descr = self.vod_entry[2]
        self.session.nav.stopService()
        STREAMS.play_vod = False
        STREAMS.list_index_tmp = STREAMS.list_index
        self.setCover()
        self.play_vod()
    def setCover(self):
        try:
            vod_entry = STREAMS.iptv_list[STREAMS.list_index]
            self['cover'].instance.setPixmapFromFile(PLUGIN_PATH + '/img/clear.png')
            if self.vod_entry[7] != '':#Mod By aime_jeux
                if vod_entry[7].find('http') == -1:#Mod By aime_jeux
                    self.picfile = PLUGIN_PATH + '/img/playlist/' + vod_entry[7]#Mod By aime_jeux
                    self.decodeImage()
                    print 'LOCAL IMG VOD'
                else:
                    if STREAMS.img_loader == False:
                        self.picfile = '%s/nstream_tmp_pic.jpg' % STREAMS.images_tmp_path
                    else:
                        m = hashlib.md5()
                        m.update(self.vod_entry[7])#Mod By aime_jeux
                        cover_md5 = m.hexdigest()
                        self.picfile = '%s/%s.jpg' % (STREAMS.images_tmp_path, cover_md5)
                    if os.path.exists(self.picfile) == False or STREAMS.img_loader == False:
                        downloadPage(self.vod_entry[7], self.picfile).addCallback(self.image_downloaded).addErrback(self.image_error)#Mod By aime_jeux
                    else:
                        self.decodeImage()
                try:
                    description = self.vod_entry[2]########################################################
                    self['Descriptions'].setText(str(description))
                except:self['Descriptions'].setText('....')
        except Exception as ex:
            print ex
            print 'update COVER'
    def decodeImage(self):
        try:
            x = self['cover'].instance.size().width()
            y = self['cover'].instance.size().height()
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
        self['cover'].show()
        try:
            ptr = self.picload.getData()
            if ptr:
                self['cover'].instance.setPixmap(ptr.__deref__())
        except Exception as ex:
            print ex
            print 'ERROR showImage'
    def image_downloaded(self, id):
        self.decodeImage()
    def image_error(self, id):
        i = 0
    def LastJobView(self):
        currentjob = None
        for job in JobManager.getPendingJobs():
            currentjob = job
        if currentjob is not None:
            self.session.open(JobView, currentjob)
        return
    def createMetaFile(self, filename):
        try:
            text = re.compile('<[\\/\\!]*?[^<>]*?>')
            text_clear = ''
            if self.vod_entry[2] != None:
                text_clear = text.sub('', self.vod_entry[2])
            serviceref = eServiceReference(self.rds, 0, STREAMS.moviefolder + '/' + filename)
            metafile = open('%s/%s.meta' % (STREAMS.moviefolder, filename), 'w')
            metafile.write('%s\n%s\n%s\n%i\n' % (serviceref.toString(),self.title.replace('\n', ''),
                text_clear.replace('\n', ''),time()))
            metafile.close()
        except Exception as ex:
            print ex
            print 'ERROR metaFile'
        return
    def __evEOF(self):
        if self.cont_play:
            self.nextVideo()
    def __seekableStatusChanged(self):
        print 'seekable status changed!'
    def __serviceStarted(self):
        self['state'].setText(' PLAY     >')
        self['cont_play'].setText('Continue play OFF')
        self.state = self.STATE_PLAYING
    def doEofInternal(self, playing):
        if not self.execing:
            return
        if not playing:
            return
        print 'doEofInternal EXIT OR NEXT'
    def stopnew(self):
        if STREAMS.playhack == '':
            self.session.nav.stopService()
            STREAMS.play_vod = False
            if self.Oldservice:self.session.nav.playService(self.Oldservice)
            else:self.session.nav.playService(STREAMS.oldServiceK)
            self.exit()
    def nextAR(self):
        message = nextAR()
        self.session.open(MessageBox, message, type=MessageBox.TYPE_INFO, timeout=3)
    def prevAR(self):
        message = prevAR()
        self.session.open(MessageBox, message, type=MessageBox.TYPE_INFO, timeout=3)
    def trialWarning(self):
        self.StateTimer.start(STREAMS.trial_time * 1000, True)
        self.session.open(MessageBox, STREAMS.trial, type=MessageBox.TYPE_INFO, timeout=STREAMS.trial_time)
    def show_more_info(self):
        self.session.open(MessageBox, self.vod_url, type=MessageBox.TYPE_INFO)
    def __playStateChanged(self, state):
        self.hideTimer.start(5000, True)
        print 'self.seekstate[3] ' + self.seekstate[3]
        text = ' ' + self.seekstate[3]
        if self.seekstate[3] == '>':
            text = ' PLAY     >'
        if self.seekstate[3] == '||':
            text = 'PAUSE   ||'
        if self.seekstate[3] == '>> 2x':
            text = '    x2     >>'
        if self.seekstate[3] == '>> 4x':
            text = '    x4     >>'
        if self.seekstate[3] == '>> 8x':
            text = '    x8     >>'
        self['state'].setText(text)
    def play_vod(self):
        try:
            if self.vod_url != '' and self.vod_url != None and len(self.vod_url) > 5:
                if self.vod_url.find('.ts') > 0:
                    print '------------------------ LIVE ------------------'
                    self.session.nav.stopService()
                    self.reference = eServiceReference(1, 0, self.vod_url)
                    print self.reference
                    self.reference.setName(self.title)
                    self.session.nav.playService(self.reference)
                else:
                    print '------------------------ movie ------------------'
                    self.session.nav.stopService()
                    self.reference = eServiceReference(self.rds, 0, self.vod_url)
                    self.reference.setName(self.title)
                    self.session.nav.playService(self.reference)
            else:
                if self.error_message:
                    self.session.open(MessageBox, self.error_message.encode('utf-8'), type=MessageBox.TYPE_ERROR)
                else:
                    self.session.open(MessageBox, 'NO VIDEOSTREAM FOUND'.encode('utf-8'), type=MessageBox.TYPE_ERROR)
                self.close()
        except Exception as ex:
            print 'vod play error 2'
            print ex
        return
    def parse_url(self):
        if STREAMS.playhack != '':
            self.vod_url = STREAMS.playhack
        print '++++++++++parse_url+++++++++++'
        try:
            url = self.vod_url
        except Exception as ex:
            print 'ERROR+++++++++++++++++parse_url++++++++++++++++++++++ERROR'
            print ex
    def power_off(self):
        self.close(1)
    def exit(self):
        if STREAMS.playhack == '':
            self.close()
################################################################"
def Replace_Index(a,b):
        AT = ''
        Ay = ''
        Path_1 = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/Cfg/index.txt'
        outfile =  open(Path_1, 'r')
        data=outfile.readlines()
        outfile.close()
        AT = data[0].split('=')[1:][0].replace('\t','').replace('\n','').replace('\r','')
        AY = data[1].split('=')[1:][0].replace('\t','').replace('\n','').replace('\r','')
        AS = data[2].split('=')[1:][0].replace('\t','').replace('\n','').replace('\r','')
        f = file(Path_1,"r")
        chaine = f.read()
        f.close()
        if a == 'indexcategories=':
            result=chaine.replace(a+str(AT),a+str(b))
        if a == 'indexstreams=':
            result=chaine.replace(a+str(AY),a+str(b))
        if a == 'indexTs=':
            result=chaine.replace(a+str(AS),a+str(b))
        f = file(Path_1,"w")
        f.write(result)
        f.close()
        return str(AT)+'\n'+str(AY)
def Return_Index(a):
        Path_1 = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/Cfg/index.txt'
        outfile =  open(Path_1, 'r')
        data=outfile.readlines()
        outfile.close()
        AT = data[0].split('=')[1:][0].replace('\t','').replace('\n','').replace('\r','')
        AY = data[1].split('=')[1:][0].replace('\t','').replace('\n','').replace('\r','')
        AS = data[2].split('=')[1:][0].replace('\t','').replace('\n','').replace('\r','')
        if a == 'indexcategories=':
            return str(AT)
        if a == 'indexstreams=':
            return str(AY)
        if a == 'indexTs=':
            return str(AS)
################################################
def charRemove(text):
    char = ["1080p",
            "2018",
            "2019",
            "2020",
            "480p",
            "4K",
            "720p",
            "ANIMAZIONE",
            "APR",
            "AVVENTURA",
            "BIOGRAFICO",
            "BDRip",
            "BluRay",
            "CINEMA",
            "COMMEDIA",
            "DOCUMENTARIO",
            "DRAMMATICO",
            "FANTASCIENZA",
            "FANTASY",
            "FEB",
            "GEN",
            "GIU",
            "HDCAM",
            "HDTC",
            "HDTS",
            "LD",
            "MAFIA",
            "MAG",
            "MARVEL",
            "MD",
            "ORROR",
            "NEW_AUDIO",
            "POLIZ",
            "R3",
            "R6",
            "SD",
            "SENTIMENTALE",
            "TC",
            "TEEN",
            "TELECINE",
            "TELESYNC",
            "THRILLER",
            "Uncensored",
            "V2",
            "WEBDL",
            "WEBRip",
            "WEB",
            "WESTERN",
            "-",
            "_",
            ".",
            "+",
            "[",
            "]"]
    myreplace = text
    for ch in char:
        myreplace = myreplace.replace(ch, "").replace("  ", " ").replace("       ", " ").strip()
    return myreplace
def Copy_TouTou(what):
    Milef = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/Cfg/hbal'
    if os.path.isfile(Milef):
            file_write = open(Milef, 'w')
            file_write.write(what)
            file_write.close()