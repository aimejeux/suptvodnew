from Components.MenuList import MenuList
import io
from Components.Label import Label
from Plugins.Plugin import PluginDescriptor
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Screens.ChoiceBox import ChoiceBox
from Components.ActionMap import ActionMap, NumberActionMap
from Components.Sources.StaticText import StaticText
from Components.Sources.List import List
from Components.AVSwitch import AVSwitch
from Components.config import config, Config, ConfigSelection, ConfigSubsection, ConfigText, getConfigListEntry, ConfigYesNo, ConfigIP, ConfigNumber, ConfigLocations
from Components.config import KEY_DELETE, KEY_BACKSPACE, KEY_LEFT, KEY_RIGHT, KEY_HOME, KEY_END, KEY_TOGGLEOW, KEY_ASCII, KEY_TIMEOUT
from Components.ConfigList import ConfigListScreen
from Components.ServiceEventTracker import ServiceEventTracker, InfoBarBase
from Tools.Directories import pathExists, fileExists, resolveFilename, SCOPE_PLUGINS, SCOPE_SKIN_IMAGE, SCOPE_HDD, SCOPE_CURRENT_PLUGIN, SCOPE_CURRENT_SKIN
from Tools.LoadPixmap import LoadPixmap
from enigma import eTimer, quitMainloop, eListbox, ePoint, RT_HALIGN_LEFT, RT_HALIGN_RIGHT, RT_VALIGN_CENTER, eListboxPythonMultiContent, eListbox, gFont, getDesktop, ePicLoad, eServiceCenter, iServiceInformation, eServiceReference, iSeekableService, iServiceInformation, iPlayableService, iPlayableServicePtr
from os import path as os_path, system as os_system, unlink, stat, mkdir, popen, makedirs, listdir, access, rename, remove, W_OK, R_OK, F_OK
from twisted.web import client
from twisted.internet import reactor
from time import time
from Screens.InfoBarGenerics import InfoBarShowHide, InfoBarSeek, InfoBarNotifications, InfoBarServiceNotifications
from Screens.InfoBarGenerics import InfoBarShowHide, NumberZap, InfoBarSeek, InfoBarAudioSelection, InfoBarSubtitleSupport
dwidth = getDesktop(0).size().width()
class StalkerStream(Screen, InfoBarNotifications):
    STATE_IDLE = 0
    STATE_PLAYING = 1
    STATE_PAUSED = 2
    ENABLE_RESUME_SUPPORT = True
    ALLOW_SUSPEND = True
    PLAYER_STOPS = 3
    skinfhd = '<screen name="StalkerStream" flags="wfNoBorder" position="0,0" size="1920,1080" title="StalkerStream" backgroundColor="transparent"><widget source="session.CurrentService" render="Label" position="193,826" size="1450,250" font="Regular; 35" backgroundColor="#263c59" shadowColor="#1d354c" shadowOffset="-1,-1" transparent="1" zPosition="1" halign="center"><convert type="ServiceName">Name</convert></widget><widget source="global.CurrentTime" render="Label" position="13,9" size="250,100" font="Regular; 28" halign="left" backgroundColor="black" transparent="1"><convert type="ClockToText">Format:%d.%m.%Y</convert></widget><ePixmap position="388,217" size="1000,600" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/ALAJRE/Cimages/Demar.png" zPosition="-1" transparent="1" alphatest="blend" /></screen>'
    skinhd = '<screen name="LiveSoccerStream" flags="wfNoBorder" position="0,0" size="1280,720" title="LiveSoccerStream" backgroundColor="transparent"><widget source="session.CurrentService" render="Label" position="-2,616" size="1280,100" font="Regular; 20" backgroundColor="#263c59" shadowColor="#1d354c" shadowOffset="-1,-1" transparent="1" zPosition="1" halign="center"><convert type="ServiceName">Name</convert></widget><widget source="global.CurrentTime" render="Label" position="3,5" size="150,100" font="Regular; 24" halign="left" backgroundColor="black" transparent="1"><convert type="ClockToText">Format:%d.%m.%Y</convert></widget><ePixmap position="165,15" size="1000,600" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/ALAJRE/Cimages/Demar.png" zPosition="-1" transparent="1" alphatest="blend" /></screen>'
    def __init__(self, session, service):
        Screen.__init__(self, session)
        if dwidth == 1280:
            self.skin = StalkerStream.skinhd
        else:
            self.skin = StalkerStream.skinfhd
        InfoBarNotifications.__init__(self)
        self.session = session
        self.service = service
        self.screen_timeout = 1000
        self.__event_tracker = ServiceEventTracker(screen=self, eventmap={iPlayableService.evSeekableStatusChanged: self.__seekableStatusChanged,
         iPlayableService.evStart: self.__serviceStarted,
         iPlayableService.evEOF: self.__evEOF})
        self['actions'] = ActionMap(['OkCancelActions',
         'InfobarSeekActions',
         'ColorActions',
         'MediaPlayerActions',
         'MovieSelectionActions'], {'ok': self.leavePlayer,
         'cancel': self.leavePlayer,
         'stop': self.leavePlayer}, -2)
        self['pauseplay'] = Label(_('Play'))
        self.hidetimer = eTimer()
        self.repeter = True
        self.state = self.STATE_PLAYING
        self.onPlayStateChanged = []
        self.play()
        self.onClose.append(self.__onClose)
    def __onClose(self):
        self.session.nav.stopService()
    def __evEOF(self):
        self.STATE_PLAYING = True
        self.state = self.STATE_PLAYING
        self.session.nav.playService(self.service)
        if self.session.nav.stopService():
            self.state = self.STATE_PLAYING
            self.session.nav.playService(self.service)
        else:
            self.leavePlayer()
    def __setHideTimer(self):
        self.hidetimer.start(self.screen_timeout)
    def ok(self):
        self.leavePlayer()
    def playNextFile(self):
        self.session.open(MessageBox, 'only to watch not play Next and Prev File', MessageBox.TYPE_INFO)
    def playPrevFile(self):
        self.session.open(MessageBox, 'only to watch not play Next and Prev File', MessageBox.TYPE_INFO)
    def playService(self, newservice):
        if self.state == self.STATE_IDLE:
            self.play()
        self.service = newservice
    def play(self):
        self.state = self.STATE_PLAYING
        self['pauseplay'].setText('PLAY')
        self.session.nav.playService(self.service)
        self.__evEOF
    def __seekableStatusChanged(self):
        service = self.session.nav.getCurrentService()
        if service is not None:
            seek = service.seek()
            if seek is None or not seek.isCurrentlySeekable():
                self.setSeekState(self.STATE_PLAYING)
                self.__evEOF
        return
    def __serviceStarted(self):
        self.state = self.STATE_PLAYING
        self.__evEOF
    def setSeekState(self, wantstate):
        print 'setSeekState'
        if wantstate == self.STATE_PAUSED:
            print 'trying to switch to Pause- state:', self.STATE_PAUSED
        elif wantstate == self.STATE_PLAYING:
            print 'trying to switch to playing- state:', self.STATE_PLAYING
        service = self.session.nav.getCurrentService()
        if service is None:
            print 'No Service found'
            return False
        else:
            pauseable = service.pause()
            if pauseable is None:
                print 'not pauseable.'
                self.state = self.STATE_PLAYING
            if pauseable is not None:
                print 'service is pausable'
                if wantstate == self.STATE_PAUSED:
                    print 'WANT TO PAUSE'
                    pauseable.pause()
                    self.state = self.STATE_PAUSED
                    if not self.shown:
                        self.hidetimer.stop()
                        self.show()
                elif wantstate == self.STATE_PLAYING:
                    print 'WANT TO PLAY'
                    pauseable.unpause()
                    self.state = self.STATE_PLAYING
                    if self.shown:
                        self.__setHideTimer()
            for c in self.onPlayStateChanged:
                c(self.state)

            return True
            return
    def handleLeave(self):
        self.close()
    def leavePlayer(self):
        self.close()