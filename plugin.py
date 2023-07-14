#!/usr/bin/python
# -*- coding: utf-8 -*-
################################### modified by aime_jeux ##################################
#############                           Aout 2021                              #############
############################################################################################
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Menu.MainMenu import Screen_MyNewMenu
Version = 'SupTVoDNeW V_1.0'
def return_version():
    return Version
Txt_go = 'Access'
Txt_go_1 = 'الدخول'
############################################################################################Tests
########################################################################
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore',InsecureRequestWarning)
########################################################################
############################################################################################
from enigma import RT_HALIGN_LEFT, RT_HALIGN_RIGHT, RT_HALIGN_CENTER, RT_VALIGN_CENTER
from Screens.ChannelSelection import ChannelSelection
import os
############################################################################################
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Sptvnw.MesImports import FullHD,showlist,MesImports
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Iptv.Iptvdons import Screen_MyIptvInfos
from Plugins.Extensions.SupTVoDNeW.OutilsSup.PlutoTvSecond.SecondPlutotv import Screen_MyPlutoTvNew_Second,Screen_MyPlutoTvNew_Stirr
from Plugins.Extensions.SupTVoDNeW.OutilsSup.MyPlutoTv.PlutoNew import Screen_MyPlutoTvNew
from Plugins.Extensions.SupTVoDNeW.OutilsSup.MyConfig.iptvstalkerconf import Screen_Iptv_stalker_config
from OutilsSup.Sptvnw.supcompnt import *
from OutilsSup.Sptvnw.SupTvNew import nPlaylist_New
from OutilsSup.Sptvnw.Config import *
from OutilsSup.Sptvnw.Setup import SupTVoDNeW_Config,get_IpConnec
from OutilsSup.Stalker.logTools import  printD,printE,delLog
from OutilsSup.Stalker.StalkerIptv import Screen_MyStalkerIptv
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Stalker.InfobarStalker import Xtream_Player_New,Copy_Volum
#############################################################################################
from Tools.BoundFunction import boundFunction
from Components.Pixmap import Pixmap
from Components.AVSwitch import AVSwitch
from enigma import ePoint, eSize, eTimer,ePicLoad
from skin import parseColor, parseFont
############################################################################################Tests
#delLog()
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.Label import Label
from Components.Sources.StaticText import StaticText
from Components.ActionMap import ActionMap, HelpableActionMap, NumberActionMap
from Plugins.Plugin import PluginDescriptor
PATH_SKINS = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/Skins'
global STREAMS
STREAMS = iptv_streamse()
class Screen_MyServersIptv(Screen):
    def __init__(self, session,cond):
        ########################Session_Skin############################
        if dwidth == 1280:
            with open(PATH_SKINS + '/MyServersIptvFHD.xml', 'r') as f:
                self.skin = f.read()
                f.close()
        else:
            with open(PATH_SKINS + '/MyServersIptvFHD.xml', 'r') as f:
                self.skin = f.read()
                f.close()
        self.session = session
        Screen.__init__(self, session)
        self['actions'] = ActionMap(['DirectionActions','SetupActions','ColorActions'], {'ok': self.ok,
            'yellow': self.Settings,
            'blue': self.get_InfoIptvserver,
            '1': self.get_journalsatserver,
            'cancel': self.close,
            'red': self.close,
            'green': self.ok,
            'up': self.keyUp,
            'down': self.keyDown,
            'left': self.left,
            'right': self.right
            }, -1)
        self.initialservice = self.session.nav.getCurrentlyPlayingServiceReference()
        self.cond = cond
        self['Infos'] = Label()
        self['Infoselect'] = Label()
        self['Infoserveriptv'] = Label()
        self['Infoserveriptv'].hide()
        self['Version'] = Label(_(Version))
        self["blue"] = Label(_('Info Server Iptv'))
        self["blue"].hide()
        self['menu'] = m2list([])
        self.get_ListIptvFnl()
    def get_InfoIptvserver(self):
        '''get only infos server iptv'''
        _iptv = self['menu'].getCurrent()[0][0]
        url   = self['menu'].getCurrent()[0][1]
        if '[IPTV]' in _iptv:
            self['Infoserveriptv'].show()
            _dons = STREAMS.get_Infos_FreeAbonnement(url)
            self['Infoserveriptv'].setText(_dons)
    def get_ListIptvFnl(self):
        '''('suptvod', _('Suptvod')), ('freeiptv', _('Freeiptv')),('stalker', _('Stalker')),('all'''
        self.MyFolderXml = []
        ListIptv = get_InfosOXml()
        i = 0
        if self.cond == 'all':
            self.MyFolderXml.append(show_Menu_SuptvodNews(' 1.  Suptvod','Suptvod'))
            self.MyFolderXml.append(show_Menu_SuptvodNews(' 2.  Iptv','Iptv'))
            self.MyFolderXml.append(show_Menu_SuptvodNews(' 3.  Stalker','Stalker'))
        elif self.cond == 'freeiptv+stalker':
            self.MyFolderXml.append(show_Menu_SuptvodNews(' 1.  Iptv','Iptv'))
            self.MyFolderXml.append(show_Menu_SuptvodNews(' 2.  Stalker','Stalker'))
        elif self.cond == 'freeiptv':
            self.MyFolderXml.append(show_Menu_SuptvodNews(' 1.  Iptv','Iptv'))
        elif self.cond == 'suptvod':
            self.MyFolderXml.append(show_Menu_SuptvodNews(' 1.  Suptvod','Suptvod'))
        else:
            self.MyFolderXml.append(show_Menu_SuptvodNews(' 1.  Stalker','Stalker'))
        self['menu'].l.setList(self.MyFolderXml)
        self['menu'].l.setItemHeight(37)
        self.currentList = 'menu'
        self['Infos'].setText(self['menu'].getCurrent()[0][1])
    def get_journalsatserver(self):#
        Nvjournalsat = get_journalsat()
        self.get_ListIptvFnl()
    def ok(self):
        url = self['menu'].getCurrent()[0][1]
        if url == 'Stalker':
            self.session.open(Screen_MyStalkerIptv)
        elif url == 'Iptv':
            self.session.open(Screen_MyIptvInfos,'freeiptv')
        else:
            self.session.open(nPlaylist_New,url)
    def Settings(self):
        self.session.open(SupTVoDNeW_Config)
    def Get_Len_List(self):
        self.session.open(MessageBox, 'coucou', MessageBox.TYPE_INFO)
    def keyDown(self):
        self['menu'].down()
        self['Infos'].setText(self['menu'].getCurrent()[0][1])
        self.Get_Infos_select()
    def keyUp(self):
        self['menu'].up()
        self['Infos'].setText(self['menu'].getCurrent()[0][1])
        self.Get_Infos_select()
    def left(self):
        self['menu'].pageUp()
        self['Infos'].setText(self['menu'].getCurrent()[0][1])
        self.Get_Infos_select()
    def right(self):
        self['menu'].pageDown()
        self['Infos'].setText(self['menu'].getCurrent()[0][1])
        self.Get_Infos_select()
    def Get_Infos_select(self):
        if '[IPTV]' in self['menu'].getCurrent()[0][0]:self["blue"].show()
        else:
            self["blue"].hide()
            self['Infoserveriptv'].hide()
        Hd = MesImports().Nety_txt(self['menu'].getCurrent()[0][0])
        self['Infoselect'].setText(Hd)
####################################################### My Test
class Screen_MyServersTest(Screen):
    def __init__(self, session):
        ########################Session_Skin############################
        if dwidth == 1280:
            with open(PATH_SKINS + '/MyServersTestFHD.xml', 'r') as f:
                self.skin = f.read()
                f.close()
        else:
            with open(PATH_SKINS + '/MyServersTestFHD.xml', 'r') as f:
                self.skin = f.read()
                f.close()
        self.session = session
        Screen.__init__(self, session)
        self['actions'] = ActionMap(['DirectionActions','SetupActions','ColorActions'], {'ok': self.ok,
            'yellow': self.Infos_history,
            '1': self.information,
            '2': self.moveUp_chanl,
            '5': self.moveDown_chanl,
            '6': self.remove_Images,
            '3': self.NewScreean,
            'cancel': self.Exit_Plugin,
            'red': self.Exit_Plugin,
            'green': self.ok,
            'blue': self.show_hide_menu,
            'up': self.keyUp,
            'down': self.keyDown,
            'left': self.left,
            'right': self.right
            }, -1)
        self.servicelist = self.session.instantiateDialog(ChannelSelection)
        self.initialservice = self.session.nav.getCurrentlyPlayingServiceReference()
        self.condimg = config.plugins.SupTVoDNeWConfig.ChoosIptv.value
        self.onShown.append(self.affich_imag_cond)
        self['poster'] = Pixmap()
        self.picload = ePicLoad()
        self.picfile = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/img/'
        self['Infos_Download'] = StaticText()
        self['infoss1'] = Label()
        self['Tail_Image'] = Label()
        self['Infos'] = Label()
        self['Explic'] = Label()
        self['Explic_1'] = Label()
        self['Infoselect'] = Label()
        self['Infoserveriptv'] = Label()
        self['Infoserveriptv'].hide()
        self['Version'] = Label(_(Version))
        self["blue"] = Label(_('Info Server Iptv'))
        self["blue"].hide()
        for x in range(9):
            self['Txt_'+str(x)] = Label()
        self.showhide = False
        self.hidden = False
        try:
            t_2=get_IpConnec()
            t_2 = MesImports()._colorize_('My Ip Connect=='+str(t_2),selcolor='cyan')
        except:t_2=''
        self['Txt_1'].setText(t_2)
        self.i = 1
        self.a = 500
        self['menu'] = m2list([])
        self['list'] = m2list([])
        self.affich_imag()
        self.Infos_Box()
        self.get_ListIptvFnl()
    def NewScreean(self):
        self.session.open(Screen_MyNewMenu)
    def Scan_Movies(self):
        self.MoviesFile = []
        self.MoviesFileView = []
        source = '/media/hdd/'
        for root,dirs,files in os.walk(source):
            for file_name in files:
                if file_name.endswith(('.mkv', '.avi', '.mp4','.flv')):
                    '''(chan_counter,name,description,piconname,stream_url,playlist_url,category_id,
                    img_src,description4playlist_html,ts_stream)'''
                    Adress = os.path.join(root,file_name)
                    name = file_name.replace('.mkv', '').replace('.avi', '').replace('.mp4','')
                    self.MoviesFile.append(show_Menu_MoviesFolder(name,Adress))
                    _datas = ('',name,'My Movies','',Adress,'','','','','')
                    self.MoviesFileView.append(_datas)
        if len(self.MoviesFile)!=0:
            return True,self.MoviesFile
        else:
            return False,self.MoviesFile#self.session.open(Screen_MoviesFolder,self.MoviesFile)
    def affich_imag(self):
        for x in range(6):
            self['Img_'+str(x)] = Pixmap()
            self['Img_'+str(x)].hide()
        self.affich_imag_cond()
    def affich_imag_cond(self):
        self.fort    = config.plugins.SupTVoDNeWConfig.notification.value
        self.condimg = config.plugins.SupTVoDNeWConfig.ChoosIptv.value
        if self.fort == 'disabled':
            self['Img_0'].hide()####
            self['Img_2'].hide()####
            self['Img_4'].hide()####
            ################## show
            self['Img_1'].show()
            self['Img_3'].show()
            self['Img_5'].show()
            return
        if self.condimg == 'all':
            self['Img_0'].show()####
            self['Img_2'].show()####
            self['Img_4'].show()####
            ################## hide
            self['Img_1'].hide()
            self['Img_3'].hide()
            self['Img_5'].hide()
        if self.condimg == 'suptvod':
            self['Img_0'].show()####
            self['Img_3'].show()
            self['Img_5'].show()
            ################## hide
            self['Img_1'].hide()
            self['Img_2'].hide()
            self['Img_4'].hide()
        if self.condimg == 'freeiptv':
            self['Img_1'].show()
            self['Img_2'].show()####
            self['Img_5'].show()
            ################## hide
            self['Img_0'].hide()
            self['Img_3'].hide()
            self['Img_4'].hide()
        if self.condimg == 'stalker':
            self['Img_1'].show()
            self['Img_3'].show()
            self['Img_4'].show()####
            ################## hide
            self['Img_0'].hide()
            self['Img_2'].hide()
            self['Img_5'].hide()
        if self.condimg == 'freeiptv+stalker':
            self['Img_1'].show()
            self['Img_2'].show()
            self['Img_4'].show()####
            ################## hide
            self['Img_0'].hide()
            self['Img_3'].hide()
            self['Img_5'].hide()
        self.Infos_Box()
    def get_ListIptvFnl(self):
        '''('suptvod', _('Suptvod')), ('freeiptv', _('Freeiptv')),('stalker', _('Stalker')),('all'''
        self.MyFolderXml = []
        MYList = ['GO','SUPTV','IPTV','STALKER','PLUTO TV','PLUTO TV Segnd','STIRR','M3U','Movies','SETTINGS']
        for i in range(10):
            self.MyFolderXml.append(show_Menu_Moved(MYList[i],MYList[i].lower()))
        self['menu'].l.setList(self.MyFolderXml)
        self['menu'].l.setItemHeight(100)
        self.currentList = 'menu'#.instance.position()
        self.deplace = 37*len(self.MyFolderXml)
        self['Infos'].setText(self['menu'].getCurrent()[0][1])
        self['Explic'].setText(Txt_go)
        self['Explic_1'].setText(Txt_go_1)
        self.decodeImage()
    def ok(self):
        #('suptvod', _('Suptvod')), ('freeiptv', _('Freeiptv')),('stalker', _('Stalker')),('all', _('All')
        cond = self['menu'].getCurrent()[0][1]
        if cond == 'settings':self.session.open(SupTVoDNeW_Config)
        ########################################
        elif cond == 'go':
            if config.plugins.SupTVoDNeWConfig.notification.value == 'enabled':
                if self.condimg == 'all':
                    self.session.open(Screen_MyServersIptv,'all')
                elif self.condimg == 'freeiptv':
                    self.session.open(Screen_MyServersIptv,'freeiptv')
                elif self.condimg == 'suptvod':
                    self.session.open(Screen_MyServersIptv,'suptvod')
                elif self.condimg == 'freeiptv+stalker':
                    self.session.open(Screen_MyServersIptv,'freeiptv+stalker')
                else:self.session.open(Screen_MyServersIptv,'stalker')
            else:self.session.open(SupTVoDNeW_Config)
        else:
            if cond == 'iptv':self.session.open(Screen_Iptv_stalker_config,'iptv')
            elif cond == 'stalker':self.session.open(Screen_Iptv_stalker_config,'stalker')
            elif cond == 'pluto tv':self.session.open(Screen_MyPlutoTvNew)
            elif cond == 'pluto tv segnd':self.session.open(Screen_MyPlutoTvNew_Second)
            elif cond == 'stirr':self.session.open(Screen_MyPlutoTvNew_Stirr)
            elif cond == 'movies':
                a,listmovies = self.Scan_Movies()
                if a:
                    self.session.open(Screen_MoviesFolder,listmovies,self.MoviesFileView)
                else:
                    self.session.open(MessageBox, 'No Movies Found', MessageBox.TYPE_INFO)
            elif cond == 'm3u':
                path = '/media/hdd/movie/tv_channels_Localgermany_plus.m3u'
                self.session.open(Userm3u3,path)
            else:
                self.Get_Len_List()
    def movelist(self):#position="19,164"
        self.i = self['menu'].getSelectionIndex()
        self.a = 500-100*self.i
        self['menu'].instance.move(ePoint(680, self.a))
        self.decodeImage()
    def Get_Len_List(self):
        self.session.open(MessageBox, 'قريبا ان شاء الله', MessageBox.TYPE_INFO)
    def keyDown(self):
        self['menu'].down()
        self['Infos'].setText(self['menu'].getCurrent()[0][1])
        self.Get_Infos_select()
    def keyUp(self):
        self['menu'].up()
        self['Infos'].setText(self['menu'].getCurrent()[0][1])
        self.Get_Infos_select()
    def left(self):
        self['menu'].pageUp()
        self['Infos'].setText(self['menu'].getCurrent()[0][1])
        self.Get_Infos_select()
    def right(self):
        self['menu'].pageDown()
        self['Infos'].setText(self['menu'].getCurrent()[0][1])
        self.Get_Infos_select()
    def Get_Infos_select(self):
        self.movelist()
        Mytxt,Mytxt_1 = '',''
        Hd = self['menu'].getSelectionIndex()
        Mytxt,Mytxt_1 =MesImports().Get_Infos_selected(Hd)
        self['Explic'].setText(Mytxt)
        self['Explic_1'].setText(Mytxt_1)
    def decodeImage(self):
        try:
            x = self['poster'].instance.size().width()
            y = self['poster'].instance.size().height()
            At = self['menu'].getCurrent()[0][1]
            if At=='settings':At='settings_1'
            if At=='pluto tv segnd':At='pluto tv'
            if At=='movies':At='movies'
            picture = self.picfile+At+'.png'
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
    def Infos_Box(self):
        t_1,t_2,t_3='','',''
        if config.plugins.SupTVoDNeWConfig.notification.value == 'enabled':
            t_1=config.plugins.SupTVoDNeWConfig.IpBox.value
            t_3=config.plugins.SupTVoDNeWConfig.MacAdress.value
            t_1 = MesImports()._colorize_('Ip Box=='+str(t_1),selcolor='cyan')
            t_3 = MesImports()._colorize_('Mac Adress=='+str(t_3),selcolor='cyan')
            self['Txt_0'].setText(t_1)
            self['Txt_2'].setText(t_3)
            ######################
            l_0=config.plugins.SupTVoDNeWConfig.Plutotv.value
            l_1 = MesImports()._colorize_('Pluto Tv=='+str(l_0),selcolor='cyan')
            self['Txt_3'].setText(l_1)
            l_2=config.plugins.SupTVoDNeWConfig.Plutotvsamsung.value
            l_3 = MesImports()._colorize_('Plutotv SamsungTv=='+str(l_2),selcolor='cyan')
            self['Txt_4'].setText(l_3)
            l_4=config.plugins.SupTVoDNeWConfig.M3u.value
            l_5 = MesImports()._colorize_('Adress M3u File=='+str(l_4),selcolor='cyan')
            self['Txt_5'].setText(l_5)
            l_6=config.plugins.SupTVoDNeWConfig.Posters.value
            l_7 = MesImports()._colorize_('Adress Poster File=='+str(l_6),selcolor='cyan')
            self['Txt_6'].setText(l_7)
            if config.plugins.SupTVoDNeWConfig.Tmdb.value == 'enabled':
                l_8=config.plugins.SupTVoDNeWConfig.TmdbToken.value
                l_9 = MesImports()._colorize_('Tmdb Token=='+str(l_8),selcolor='cyan')
                self['Txt_7'].setText(str(l_9))
                l_10=config.plugins.SupTVoDNeWConfig.TmdbLang.value
                l_11 = MesImports()._colorize_('Tmdb Token=='+str(l_10),selcolor='cyan')
                self['Txt_8'].setText(l_11)
        else:
            self['Txt_0'].setText('Ip Box : ')
            self['Txt_1'].setText('My Ip Connect : ')
            self['Txt_2'].setText('Mac Adress : ')
            self['Txt_3'].setText('Pluto Tv : ')
            self['Txt_4'].setText('Plutotv SamsungTv : ')
            self['Txt_5'].setText('Adress M3u File : ')
            self['Txt_6'].setText('Adress Poster File : ')
            self['Txt_7'].setText('Tmdb Token : ')
            self['Txt_8'].setText('Tmdb Token : ')
        T_11 = MesImports()._colorize_('Poster File Size =='+str(MesImports().get_Taille()),selcolor='cyan')
        self['Tail_Image'].setText(T_11)
    def Infos_history(self):
        self.session.execDialog(self.servicelist)
    def moveDown_chanl(self):
        self.servicelist.moveUp()
        self.servicelist.zap()
    def moveUp_chanl(self):
        self.servicelist.moveDown()
        self.servicelist.zap()
    def information(self):
        from ServiceReference import ServiceReference
        if self.session.nav.getCurrentlyPlayingServiceReference():
            name = ServiceReference(self.session.nav.getCurrentlyPlayingServiceReference()).getServiceName()
            refstr = self.session.nav.getCurrentlyPlayingServiceReference().toString()
            self.session.open(MessageBox, str(name)+'\n'+str(refstr), type=MessageBox.TYPE_INFO)
    def show_hide_menu(self):
        if not self.showhide:
            if self.hidden:
                self.show()
            else:
                self.hide()
            self.hidden = not self.hidden
    def remove_Images(self):
        MesImports().remove_ImagesT()
        self.affich_imag_cond()
    def Exit_Plugin(self):
        self.session.nav.stopService()
        self.session.nav.playService(self.initialservice)
        self.close()
#####################################################################################
class Screen_MoviesFolder(Screen):
    def __init__(self, session,Mylist,MoviesFileView):
        ########################Session_Skin############################
        if dwidth == 1280:
            with open(PATH_SKINS + '/MoviesFolderFHD.xml', 'r') as f:
                self.skin = f.read()
                f.close()
        else:
            with open(PATH_SKINS + '/MoviesFolderFHD.xml', 'r') as f:
                self.skin = f.read()
                f.close()
        self.session = session
        Screen.__init__(self, session)
        self['actions'] = ActionMap(['DirectionActions','SetupActions','ColorActions'], {'ok': self.ok,
            'yellow': self.Settings,
            'cancel': self.close,
            'red': self.close,
            'green': self.ok,
            'up': self.keyUp,
            'down': self.keyDown,
            'left': self.left,
            'right': self.right
            }, -1)
        self.initialservice = self.session.nav.getCurrentlyPlayingServiceReference()
        self.onShown.append(self.show_all_chang)
        self.MoviesFileView = MoviesFileView
        self.Mylist = Mylist
        self['Infos'] = Label()
        self['Infoselect'] = Label()
        self['Infoserveriptv'] = Label()
        self['Infoserveriptv'].hide()
        self['Version'] = Label(_(str(len(self.Mylist))+' [data]'))
        self["blue"] = Label(_('Info Server Iptv'))
        self["blue"].hide()
        self['menu'] = m2list([])
        self.get_ListIptvFnl()
    def get_ListIptvFnl(self):
        self['menu'].l.setList(self.Mylist)
        self['menu'].l.setItemHeight(37)
        self.currentList = 'menu'
        self['Infos'].setText(self['menu'].getCurrent()[0][1])
    def ok(self):
        Idx = self['menu'].getSelectionIndex()
        self.session.open(Xtream_Player_New,recorder_sref=None,liste=self.MoviesFileView,indxto=Idx,Oldservice=self.initialservice,server=0,_type='MyVideos')
    def Settings(self):
        self.session.open(SupTVoDNeW_Config)
    def keyDown(self):
        self['menu'].down()
        self['Infos'].setText(self['menu'].getCurrent()[0][1])
        self.Get_Infos_select()
    def keyUp(self):
        self['menu'].up()
        self['Infos'].setText(self['menu'].getCurrent()[0][1])
        self.Get_Infos_select()
    def left(self):
        self['menu'].pageUp()
        self['Infos'].setText(self['menu'].getCurrent()[0][1])
        self.Get_Infos_select()
    def right(self):
        self['menu'].pageDown()
        self['Infos'].setText(self['menu'].getCurrent()[0][1])
        self.Get_Infos_select()
    def Get_Infos_select(self):
        Hd = MesImports().Nety_txt(self['menu'].getCurrent()[0][0])
        self['Infoselect'].setText(Hd)
    def show_all_chang(self):
        H,Y =MesImports().Recovery_indx()
        if str(Y)== 'True':
            try:
                index_=H
                self['menu'].moveToIndex(int(index_))
                Copy_Volum('indexfil='+str(H)+'\ndakhla=False','indexfil')
                self['Infos'].setText(self['menu'].getCurrent()[0][1])
            except Exception as ex:
                print ex
###################################################################################
class Userm3u3(Screen): 
    def __init__(self, session, name):
        self.skin = FullHD.skin
        Screen.__init__(self, session)
        self.list = []
        self['list'] = m2list([])
        self['setupActions'] = ActionMap(['SetupActions', 'ColorActions', 'TimerEditActions'], {'red': self.close,
            'green': self.okClicked,
            'cancel': self.cancel,
            'ok': self.okClicked}, -2)
        self['text'] = Label('')
        self['text'].setText('')
        self.initialservice = session.nav.getCurrentlyPlayingServiceReference()
        self.name = name
        self.srefOld = self.session.nav.getCurrentlyPlayingServiceReference()
        self.onLayoutFinish.append(self.openTest)
    def openTest(self):
        self.names = []
        self.urls = []
        f1 = open(self.name, 'r+')
        fpage = f1.read()
        regexcat = 'EXTINF.*?,(.*?)\\n(.*?)\\n'
        match = re.compile(regexcat, re.DOTALL).findall(fpage)
        i = 0
        for name, url in match:
            url = url.replace(' ', '')
            url = url.replace('\\n', '')
            self.names.append(name)
            self.urls.append(url)
            i = i + 1
            if i>50:break
        from Plugins.Extensions.SupTVoDNeW.OutilsSup.Sptvnw.MesImports import showlist
        showlist(self.names, self['list'])
        self['text'].setText(str(len(self.names)) + ' TV Channel')
    def okClicked(self):
        from Screens.InfoBar import InfoBar, MoviePlayer
        idx = self['list'].getSelectionIndex()
        if idx is None:
            return None
        if 'sex' in str(self['list'].getCurrent()[0]).lower() or 'xxl' in str(self['list'].getCurrent()[0]).lower() or 'hotclub' in str(self['list'].getCurrent()[0]).lower() or 'venus' in str(self['list'].getCurrent()[0]).lower() or 'playb' in str(self['list'].getCurrent()[0]).lower() or 'hust' in str(self['list'].getCurrent()[0]).lower() or '+18' in str(self['list'].getCurrent()[0]).lower() or 'libid' in str(self['list'].getCurrent()[0]).lower() or 'penthouse' in str(self['list'].getCurrent()[0]).lower() or 'spice' in str(self['list'].getCurrent()[0]).lower() or 'platinum' in str(self['list'].getCurrent()[0]).lower() or 'amatix' in str(self['list'].getCurrent()[0]).lower() or 'xx' in str(self['list'].getCurrent()[0]).lower() or 'vivid' in str(self['list'].getCurrent()[0]).lower() or 'brazzers' in str(self['list'].getCurrent()[0]).lower() or 'colmax' in str(self['list'].getCurrent()[0]).lower() or 'daring' in str(self['list'].getCurrent()[0]).lower() or 'lover' in str(self['list'].getCurrent()[0]).lower() or 'man-x' in str(self['list'].getCurrent()[0]).lower() or 'man x' in str(self['list'].getCurrent()[0]).lower() or 'manx' in str(self['list'].getCurrent()[0]).lower() or 'pink_x' in str(self['list'].getCurrent()[0]).lower() or 'pink-x' in str(self['list'].getCurrent()[0]).lower() or 'pink x' in str(self['list'].getCurrent()[0]).lower() or 'pinkx' in str(self['list'].getCurrent()[0]).lower() or 'reality kings' in str(self['list'].getCurrent()[0]).lower() or 'stars xxx' in str(self['list'].getCurrent()[0]).lower() or 'pink show' in str(self['list'].getCurrent()[0]).lower() or 'pink-show' in str(self['list'].getCurrent()[0]).lower() or 'pink_show' in str(self['list'].getCurrent()[0]).lower() or 'pinkshow' in str(self['list'].getCurrent()[0]).lower() or 'porn' in str(self['list'].getCurrent()[0]).lower() or 'xxx' in str(self['list'].getCurrent()[0]).lower() or 'brazz' in str(self['list'].getCurrent()[0]).lower() or 'lov' in str(self['list'].getCurrent()[0]).lower() or 'erot' in str(self['list'].getCurrent()[0]).lower():
            self.session.open(MessageBox, 'Not with this plugin....', type=MessageBox.TYPE_INFO)
            return None
        if 'canal play' in str(self['list'].getCurrent()[0]).lower() or 'a la cart' in str(self['list'].getCurrent()[0]).lower() or 'primafila' in str(self['list'].getCurrent()[0]).lower() or 'taquill' in str(self['list'].getCurrent()[0]).lower() or 'adult' in str(self['list'].getCurrent()[0]).lower() or 'erot' in str(self['list'].getCurrent()[0]).lower():
            self.session.open(MessageBox, 'Not with this plugin....', type=MessageBox.TYPE_INFO)
            return None
        else:
            from enigma import eServiceReference
            name = self.names[idx]
            url = self.urls[idx].replace('\n','')
            ref = eServiceReference(4097, 0, url)
            ref.setName(str(url)+' '+name)
            self.session.open(MessageBox, str(name)+'\n'+str(url), type=MessageBox.TYPE_INFO)
            self.session.open(MoviePlayer,ref)
        return None
    def backToIntialService(self, ret = None):
        self.session.nav.stopService()
        self.session.nav.playService(self.initialservice)
    def cancel(self):
        self.backToIntialService()
        Screen.close(self, False)
############################################################
def menu(menuid, **kwargs):
    if menuid == 'mainmenu':
        return [('SupTVoDNeW',Start_iptv_palyer,'SupTVoDNeW',4)]
    return []
def Start_iptv_palyer(session, **kwargs):
    session.open(Screen_MyServersTest)
    #session.open(Screen_MyNewMenu)
def Plugins(**kwargs):
    return [PluginDescriptor(name='SupTVoDNeW (Mod By Aime_jeux)', 
           description=Version+'  VOD_SUPTV Mod By Aime_Jeux', where=PluginDescriptor.WHERE_MENU, fnc=menu), 
           PluginDescriptor(name=Version, description='VOD_SUPTV Mod By Aime_Jeux', 
           where=PluginDescriptor.WHERE_PLUGINMENU, fnc=Start_iptv_palyer, icon='plugin.png')]