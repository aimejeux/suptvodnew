#!/usr/bin/python
# -*- coding: utf-8 -*-
################################### modified by aime_jeux ##################################
#############                           Aout 2021                              #############
############################################################################################
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Sptvnw.Config import *
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.Label import Label
from Components.Sources.StaticText import StaticText
from Components.ActionMap import ActionMap, HelpableActionMap, NumberActionMap
PATH_SKINS = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/Skins'
#################################################################################
from enigma import getDesktop
from enigma import ePoint, eSize, gRGB,eTimer
dwidth = getDesktop(0).size().width()
Version = 'SupTVoDNeW V_1.0'
def return_version():
    return Version
def parseColor(s):
	return gRGB(int(s[1:], 0x10))
################################################################################################
class Screen_MyNewMenu(Screen):
    def __init__(self, session):
        ########################Session_Skin############################
        if dwidth == 1280:
            with open(PATH_SKINS + '/MyNewMenuFHD.xml', 'r') as f:
                self.skin = f.read()
                f.close()
        else:
            with open(PATH_SKINS + '/MyNewMenuFHD.xml', 'r') as f:
                self.skin = f.read()
                f.close()
        self.session = session
        Screen.__init__(self, session)
        self['actions'] = ActionMap(['DirectionActions','SetupActions','ColorActions'], {'ok': self.ok,
            'cancel': self.close,
            'red': self.close,
            'green': self.Toutou,
            'up': self.keyUp,
            'down': self.keyDown,
            'left': self.left,
            'right': self.right
            }, -1)
        self.initialservice = self.session.nav.getCurrentlyPlayingServiceReference()
        self.pagnt = 0
        self.timer = eTimer()
        self['Version'] = Label(_(Version))
        self['menu'] = m2list([])
        self.get_ListIptvFnl()
    def get_ListIptvFnl(self):
        '''('suptvod', _('Suptvod')), ('freeiptv', _('Freeiptv')),('stalker', _('Stalker')),('all'''
        self.MyFolderXml = []
        self.MyFolderXml.append(show_Menu_SuptvodNews('GO','Go'))
        self.MyFolderXml.append(show_Menu_SuptvodNews('Suptvod','Suptvod'))
        self.MyFolderXml.append(show_Menu_SuptvodNews('Iptv','Iptv'))
        self.MyFolderXml.append(show_Menu_SuptvodNews('Stalker','Stalker'))
        self.MyFolderXml.append(show_Menu_SuptvodNews('PLUTO TV','PLUTO TV'))
        self.MyFolderXml.append(show_Menu_SuptvodNews('PLUTO TV Segnd','PLUTO TV Segnd'))
        self.MyFolderXml.append(show_Menu_SuptvodNews('STIRR','STIRR'))
        self.MyFolderXml.append(show_Menu_SuptvodNews('M3U','M3U'))
        self.MyFolderXml.append(show_Menu_SuptvodNews('Movies','Movies'))
        self.MyFolderXml.append(show_Menu_SuptvodNews('SETTING','SETTING'))
        self.MyFolderXml.append(show_Menu_SuptvodNews('COUCOU','COUCOU'))
        self['menu'].l.setList(self.MyFolderXml)
        self['menu'].l.setItemHeight(37)
        self.currentList = 'menu'
        self.create_label()
    def Toutou(self):
        #r = self['TXT_0'].instance.position()
        r = self['TXT_0'].SetFont('35')
        self.session.open(MessageBox, str(r), MessageBox.TYPE_INFO)
    def create_label(self):
        self.Mylist = ['GO','Suptvod','Iptv','Stalker','PLUTO TV','PLUTO TV Segnd','STIRR','M3U','Movies','SETTING','COUCOU']
        for x in range(len(self.MyFolderXml)):
            self['TXT_'+str(x)] = Label()
            self['TXT_'+str(x)].setText(self.Mylist[x])
            #self["TXT_" +str(x)].instance.setForegroundColor(parseColor('#000000'))
            self['TXT_'+str(x)].hide()
        self.show_hide()
    def show_hide(self):
        for x in range(3):
            self['TXT_'+str(x)].show()
        try:
            self.timer.callback.append(self.Get_Infos_select)
        except:
            self.timer_conn = self.timer.timeout.connect(self.Get_Infos_select)
        self.timer.start(100, True)
        #self.Get_Infos_select()
    def movelist(self):#position="19,164"
        self.i = self['menu'].getSelectionIndex()
        self.a = 500-100*self.i
        self['menu'].instance.move(ePoint(680, self.a))
        self.decodeImage()
    def Get_Infos_select(self):
        self.timer.stop()
        self.cond_ = len(self.MyFolderXml)
        self.IndexT = self['menu'].getSelectionIndex()
        if 0<=self.IndexT<3:
            self._rang1 = 0
            self._rang2 = 3
            for x in range(self._rang1,self._rang2):
                self['TXT_'+str(x)].show()
            for x in range(self._rang2,self.cond_):
                self['TXT_'+str(x)].hide()
        elif 3<=self.IndexT<6:
            self._rang1 = 3
            self._rang2 = 6
            for x in range(self._rang1,self._rang2):
                self['TXT_'+str(x)].show()
            for x in range(self._rang2,self.cond_):
                self['TXT_'+str(x)].hide()
            for x in range(0,self._rang1):
                self['TXT_'+str(x)].hide()
        elif 6<=self.IndexT<9:
            self._rang1 = 6
            self._rang2 = 9
            for x in range(self._rang1,self._rang2):
                self['TXT_'+str(x)].show()
            for x in range(0,self._rang1):
                self['TXT_'+str(x)].hide()
            for x in range(self._rang2,self.cond_):
                self['TXT_'+str(x)].hide()
        else:
            for x in range(9,self.cond_):
                self['TXT_'+str(x)].show()
            for x in range(0,9):
                self['TXT_'+str(x)].hide()
        for t in range(self.cond_):
            r = self['TXT_'+str(t)].getPosition()
            if t == self.IndexT:
                self["TXT_" +str(t)].instance.resize(eSize(500, 100))
                self["TXT_" +str(t)].instance.setBackgroundColor(parseColor('#282828'))
                self["TXT_" +str(t)].instance.setForegroundColor(parseColor('#DCE1E3'))
                self["TXT_"+str(t)].instance.move(ePoint(r[0], r[1]-20))
                self["TXT_"+str(t)].instance.invalidate()
            else:
                self["TXT_" +str(t)].instance.resize(eSize(500, 100))
                self["TXT_" +str(t)].instance.setBackgroundColor(parseColor('#4d5656'))
                self["TXT_" +str(t)].instance.setForegroundColor(parseColor('#2980b9'))
                self["TXT_"+str(t)].instance.move(ePoint(r[0], 587))
                self["TXT_"+str(t)].instance.invalidate()
    def ok(self):
        pass
    def Get_Len_List(self):
        self.session.open(MessageBox, 'coucou', MessageBox.TYPE_INFO)
    def keyDown(self):
        self['menu'].down()
        self.Get_Infos_select()
    def keyUp(self):
        self['menu'].up()
        self.Get_Infos_select()
    def left(self):
        self['menu'].up()
        self.Get_Infos_select()
    def right(self):
        self['menu'].down()
        self.Get_Infos_select()
    def Moveframe(self):
        k = self['menu'].getSelectionIndex()
        if 0<=k<3:
            self['frame'].moveTo(160*k+400, 117, 1)
        if 3<=k<6:
            self['frame'].moveTo(160*(k-3)+400, 277, 1)
        if 6<=k<9:
            self['frame'].moveTo(160*(k-6)+400, 437, 1)
        self['frame'].startMoving()