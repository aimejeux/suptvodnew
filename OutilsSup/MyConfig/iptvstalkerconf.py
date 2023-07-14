#!/usr/bin/python
# -*- coding: utf-8 -*-
################################### modified by aime_jeux ##################################
#############                           Aout 2021                              #############
############################################################################################
global Az
Az ='''    <stalker>
	    <namehost>%s</namehost>
	    <protocol>%s</protocol>
	    <host>%s</host>
	    <port>%s</port>
	    <mac>%s</mac>
    </stalker>
</iptvod>'''
import re
from Screens.InputBox import InputBox
from Components.Input import Input
from Plugins.Extensions.SupTVoDNeW.plugin import return_version
from Screens.ChannelSelection import ChannelSelection
import os
if os.path.exists('/var/lib/dpkg/status'):
    enigmaos = 'oe2.2'
else:
    enigmaos = 'oe2.0'
def is_ascii(s):
    try:
        s.decode('ascii')
    except UnicodeDecodeError:
        try:s.decode('utf-8')
        except UnicodeDecodeError:
            return False
    else:
        return True
def _colorize_(txt,selcolor='white',marker="=="):
    if enigmaos == "oe2.2" or  is_ascii(txt)==False:
        return txt
    colors={'black':'\c00000000','white':'\c00??????','grey':'\c00808080',
    'blue':'\c000000??','green':'\c0000??00','red':'\c00??0000','ivory':"\c0???????",
    'yellow':'\c00????00','cyan':'\\c0000????','magenta':'\c00??00??'}
    color=colors.get(selcolor,'\c0000????')
    try:
        txtparts=txt.split(marker)
        txt1=txtparts[0]
        txt2=txtparts[1]
        ftxt=txt1+" : "+color+txt2
        return ftxt
    except:
        return txt

############################################################################################
from Tools.BoundFunction import boundFunction
from Components.Pixmap import Pixmap
from Components.AVSwitch import AVSwitch
from enigma import ePoint, eSize, eTimer,ePicLoad
from skin import parseColor, parseFont
############################################################################################Tests
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Stalker.GetServers import get_InfosOXml_Stalker
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Stalker.StalkerIptv import Screen_MyStalkerIptv
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Stalker.logTools import  printD,printE,delLog
delLog()
from Screens.Screen import Screen
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Stalker.StalkerIptv import Screen_MyStalkerIptv
from Screens.MessageBox import MessageBox
from Components.Label import Label
from Components.ActionMap import ActionMap, HelpableActionMap, NumberActionMap
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Sptvnw.supcompnt import *
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Sptvnw.SupTvNew import nPlaylist_New
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Sptvnw.Config import *
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Sptvnw.Setup import SupTVoDNeW_Config
from Plugins.Plugin import PluginDescriptor
PATH_SKINS = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/Skins'
global STREAMS
STREAMS = iptv_streamse()
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Stalker.stalker_portal import *
global MyImport
MyImport = Stalker()
from Plugins.Extensions.SupTVoDNeW.OutilsSup.MyConfig.getxml import getxml
from enigma import getDesktop
dwidth = getDesktop(0).size().width()
class Screen_Iptv_stalker_config(Screen,getxml):
    def __init__(self, session,cond):
        getxml.__init__(self)
        ########################Session_Skin############################
        if dwidth == 1280:
            with open(PATH_SKINS + '/MyIptvConfigFHD.xml', 'r') as f:
                self.skin = f.read()
                f.close()
        else:
            with open(PATH_SKINS + '/MyIptvConfigFHD.xml', 'r') as f:
                self.skin = f.read()
                f.close()
        self.session = session
        Screen.__init__(self, session)
        self['actions'] = ActionMap(['DirectionActions','SetupActions','ColorActions'], {
            #'ok': self.ok,
            'yellow': self.Delet_Video_list,
            'blue': self.get_InfoIptvserver,
            '1': self.get_journalsatserver,
            # '2': self.backToIntialService,
            'cancel': self.close,
            'red': self.close,
            'green': self.Add_Videoxml,
            'up': self.keyUp,
            'down': self.keyDown,
            'left': self.left,
            'right': self.right
            }, -1)
        self.initialservice = self.session.nav.getCurrentlyPlayingServiceReference()
        self.cond = cond
        self._title,self.namehost,self.protocol,self.host,self.port,self.mac = '','','','','',''
        self['Infos'] = Label()
        self['Infoselect'] = Label()
        self['Infoserveriptv'] = Label()
        self['Infoserveriptv'].hide()
        if self.cond == 'stalker':self['Version'] = Label(_(return_version()+' [Config Stalker]'))
        else:self['Version'] = Label(_(return_version()+' [Config Iptv]'))
        self["blue"] = Label(_('Info Server'))
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
        else:
            self['Infoserveriptv'].show()
            self.idx = self['menu'].getSelectionIndex()
            self.TXT = 'Expiration Date : '+str(MyImport._lan_Dat_Exprt(self.idx))
            self['Infoserveriptv'].setText(self.TXT)
    def get_ListIptvFnl(self):
        self.MyFolderXml = []
        ListIptv = []
        i = 1
        if self.cond == 'stalker':
            ListIptv = get_InfosOXml_Stalker()[1]
            for (namehost,url,macc) in ListIptv:
                self.MyFolderXml.append(show_Menu_SuptvodNews(' '+str(i)+'.  '+namehost+' [Stalker]',url))
                i = i + 1
        else:
            ListIptv = get_InfosOXml()
            for name,url in ListIptv:
                self.MyFolderXml.append(show_Menu_SuptvodNews(' '+str(i)+'.  '+name+' [IPTV]',url))
                i = i + 1
        self['menu'].l.setList(self.MyFolderXml)
        self['menu'].l.setItemHeight(37)
        self.currentList = 'menu'
        self['Infos'].setText(self['menu'].getCurrent()[0][1])
    def get_journalsatserver(self):#
        Nvjournalsat = get_journalsat()#supcompnt
        self.get_ListIptvFnl()
    def ok(self):
        url = self['menu'].getCurrent()[0][1]
        if url == 'Stalker':
            self.session.open(Screen_MyStalkerIptv)
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
        self['Infoserveriptv'].hide()
        Hd = self.Nety_txt(self['menu'].getCurrent()[0][0])
        self['Infoselect'].setText(Hd)
    def Delet_Video_list(self):
        name = self.Nety_txt(self['menu'].getCurrent()[0][0])
        self.session.openWithCallback(self.userIsSure, MessageBox, _('Are You Sure ?\n' + 'You Want To Delete\n%s' % name), MessageBox.TYPE_YESNO)
    def userIsSure(self, answer):
        if answer is None:
            self.cancelCondition()
        if answer is False:
            self.cancelCondition()
        else:self.Delet_Video()
    def MessageConfirm(self,msg):
        self.session.open(MessageBox,msg, MessageBox.TYPE_INFO)
    def Delet_Video(self):
        G = self['menu'].getCurrent()[0][0]
        Nme = self.Nety_txt(G)
        Messg,Titl = self.Delt_Video_xml_File(Nme,self.cond)
        self.MessageConfirm(Titl)
        if Messg == 'OK':self.get_ListIptvFnl()
    def Add_Videoxml(self,conds=None):
        if conds=='protocol':self._title = 'Protocol'
        elif conds=='host':self._title = 'Host'
        elif conds=='port':self._title = 'Port'
        elif conds=='mac':self._title = 'Mac'
        elif conds=='usr':self._title = 'Usr'
        elif conds=='passw':self._title = 'Passw'
        else:self._title = 'Host name'
        self.session.openWithCallback(self.Condition, InputBox, title=_(self._title), windowTitle=_(return_version()), text='', maxSize=False, type=Input.TEXT)
    def Condition(self,Npage):
        if Npage is None:
            self.cancelCondition()
        elif str(Npage) == '':
            self.cancelCondition()
        else:
            if self.cond =='stalker':####################################### stalker
                if self._title == 'Host name':
                    self.namehost = Npage
                    self.Add_Videoxml(conds='protocol')
                elif self._title == 'Protocol':
                    self.protocol = Npage
                    self.Add_Videoxml(conds='host')
                elif self._title == 'Host':
                    self.host = Npage
                    self.Add_Videoxml(conds='port')
                elif self._title == 'Port':
                    self.port = Npage
                    self.Add_Videoxml(conds='mac')
                else:####################################### iptv
                    self.mac = Npage
                    self._Add_Video_xml_File('stalker')
            else:
                if self._title == 'Host name':
                    self.namehost = Npage
                    self.Add_Videoxml(conds='protocol')
                elif self._title == 'Protocol':
                    self.protocol = Npage
                    self.Add_Videoxml(conds='host')
                elif self._title == 'Host':
                    self.host = Npage
                    self.Add_Videoxml(conds='port')
                elif self._title == 'Port':
                    self.port = Npage
                    self.Add_Videoxml(conds='usr')
                elif self._title == 'Usr':
                    self.usr = Npage
                    self.Add_Videoxml(conds='passw')
                else:
                    self.passw = Npage
                    self._Add_Video_xml_File('iptv')
        return
    def _Add_Video_xml_File(self,condY):
        Messg,msg = '',''
        if condY == 'stalker':
            Messg = self.Add_Video_xml_File(condY,self.namehost,self.protocol,self.host,self.port,self.mac,'','')
            if Messg == 'OK':
                msg = 'Your Data\n%s\n%s\n%s\n%s\n%s'% (self.namehost,self.protocol,self.host,str(self.port),self.mac)
        else:
            Messg = self.Add_Video_xml_File(condY,self.namehost,self.protocol,self.host,self.port,'',self.usr,self.passw)
            if Messg == 'OK':
                msg = 'Your Data\n%s\n%s\n%s\n%s\n%s\n%s'% (self.namehost,self.protocol,self.host,str(self.port),self.usr,self.passw)
        if Messg == 'OK':
            self.MessageConfirm(msg)
            self.get_ListIptvFnl()
        else:self.MessageConfirm('Unfinished Request ')