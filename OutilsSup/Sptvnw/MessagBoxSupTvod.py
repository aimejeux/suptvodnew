#!/usr/bin/python
# -*- coding: utf-8 -*-
################################### modified by aime_jeux ##################################
#############                           Aout 2021                              #############
############################################################################################
############################################################################################
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Sptvnw.Config import m2list,show_Menu_MessagBox
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Sptvnw.MesImports import MesImports
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.Sources.StaticText import StaticText
from Components.MenuList import MenuList
from enigma import eTimer
from enigma import getDesktop, eListboxPythonMultiContent, eListbox, eTimer, gFont, RT_HALIGN_LEFT, RT_HALIGN_RIGHT, RT_HALIGN_CENTER, RT_WRAP, loadPNG
PATH_SKINS = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/Skins'
T_1 = 'هذا الاختيار يستعمل فيه التحميل بواسطة الجوب ويمكن بواسطته تحميل اكثر من فيلم'
T_2 = 'This Option Is Used To Download Via The Job, And It Is Possible To Download More Than One Movie'
T_3 = 'هذا الاختيار يستعمل فيه التحميل بواسطة ملف خارجي ويمكن بواسطته تحميل فيلم واحد في كل استعمال'
T_4 = 'This Option Is Used To Download By An External File And By Which One Movie Can Be Downloaded Per Use'
class MessagBoxSupTvod(Screen):
    TYPE_YESNO = 0
    TYPE_INFO = 1
    TYPE_WARNING = 2
    TYPE_ERROR = 3
    TYPE_MESSAGE = 4
    def __init__(self, session, text, text1, text2, text3,text4,text5,text6,timeout = -1, close_on_any_key = False, type = TYPE_YESNO, default = True, picon = None, list = [], enable_input = True, timeout_default = None):
        self.type = type
        with open(PATH_SKINS + '/MessagBoxSupTvodFHD.xml', 'r') as f:
            self.skin = f.read()
            f.close()
        Screen.__init__(self, session)
        self['actions'] = ActionMap(['DirectionActions','SetupActions'], {'ok': self.ok,
            'cancel': self.cancel,
            #'red': self.close,
            # 'green': self.ok,
            'up': self.up,
            'down': self.down,
            'left': self.left,
            'right': self.right
            }, -1)
        self.T_1 = T_1
        self.T_2 = T_2
        self.T_3 = T_3
        self.T_4 = T_4
        self['list'] = m2list([])
        self['info1'] = Label(self.T_1)
        self['info2'] = Label(self.T_2)
        self['text'] = Label(text)
        self['text1'] = Label(text1)
        self['text2'] = Label(text2)
        text3= MesImports()._colorize_(str(text3),selcolor='cyan')
        self['text3'] = Label(text3)
        text4 = MesImports()._colorize_(str(text4),selcolor='cyan')
        self['text4'] = Label(text4)
        text5 = MesImports()._colorize_(str(text5),selcolor='cyan')
        self['text5'] = Label(text5)
        self['text6'] = Label(text6)
        self['selectedChoice'] = Label()
        self.text = text
        self.text1 = text1
        self.text2 = text2
        self.A = [('  1/-   ' + self.text, 'A1'), ('  2/-   ' + self.text1, 'A2')]
        self['ErrorPixmap'] = Pixmap()
        self['QuestionPixmap'] = Pixmap()
        self['QuestionPixmap'].hide()
        self['ErrorPixmap'].hide()
        self['InfoPixmap'] = Pixmap()
        picon = picon or type
        if picon != self.TYPE_YESNO:
            self['QuestionPixmap'].hide()
        self.title = self.type < self.TYPE_MESSAGE and ['Question','Information','Warning','Error'][self.type] or 'Message'
        if type == self.TYPE_YESNO:
            if list:
                self.list = list
            elif default == True:
                self.list = []
                for X in self.A:
                    self.list.append(show_Menu_MessagBox(X[0],X[1]))
            else:
                self.list = []
                for X in self.A:
                    self.list.append(show_Menu_MessagBox(X[0],X[1]))
        else:
            self.list = []
        self['list'].l.setList(self.list)
        self['list'].l.setItemHeight(37)
        if self.list:
            self['selectedChoice'].setText(self.Cleartxt(self['list'].getCurrent()[0][0]))
        else:
            self['list'].hide()
        self.onLayoutFinish.append(self.layoutFinished)
    def layoutFinished(self):
        self.setTitle(_(self.text2))
    def cancel(self):
        self.close(False)
    def ok(self):
        if self.list:
            self.close(self['list'].getCurrent()[0][1])
        else:
            self.close(True)
    def alwaysOK(self):
        self.close(True)
    def get_Infos_select(self):
        v = self['list'].getSelectionIndex()
        if v == 0:
            self['info1'].setText(self.T_1)
            self['info2'].setText(self.T_2)
        else:
            self['info1'].setText(self.T_3)
            self['info2'].setText(self.T_4)
    def get_Infos(self):
        _don = self['list'].getCurrent()[0][0]
        Txt  = self.Cleartxt(_don)
        self['selectedChoice'].setText(Txt)
        self.get_Infos_select()
    def up(self):
        u = self['list'].getSelectionIndex()
        if u == 0:
            self['list'].moveToIndex(1)
        else:self['list'].up()
        self.get_Infos()
    def down(self):
        u = self['list'].getSelectionIndex()
        if u == 1:self['list'].moveToIndex(0)
        else:self['list'].down()
        self.get_Infos()
    def left(self):
        self['list'].pageUp()
        self.get_Infos()
    def right(self):
        self['list'].pageDown()
        self.get_Infos()
    def Cleartxt(self,txt):
        txt = txt.replace('  1/-   ','').replace('  2/-   ','')
        return txt