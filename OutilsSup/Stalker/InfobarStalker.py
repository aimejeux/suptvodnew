#!/usr/bin/python
# -*- coding: utf-8 -*-
from Plugins.Extensions.SupTVoDNeW.plugin import return_version
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Stalker.stalker_portal_New import get_donnees_Stalker_New
from twisted.web.client import downloadPage
import os
from Screens.TaskView import JobView
from Tools.BoundFunction import boundFunction
from Components.AVSwitch import AVSwitch
import hashlib
from Components.Task import Task, Job, job_manager as JobManager, Condition
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.ServiceEventTracker import ServiceEventTracker, InfoBarBase
from Screens.InfoBarGenerics import InfoBarSeek, InfoBarAudioSelection, InfoBarSubtitleSupport
from Components.ActionMap import ActionMap, HelpableActionMap, NumberActionMap
from enigma import eTimer,eListboxPythonMultiContent, gFont, getDesktop, ePicLoad, eServiceReference, iPlayableService,eDVBVolumecontrol
from Components.Pixmap import Pixmap
from Components.Label import Label
from Components.config import config
PATH_SKINS = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/Skins'
PLUGIN_PATH = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW'
ChangeImage = True
dwidth = getDesktop(0).size().width()
from logTools import printD,printE,delLog
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
def get_ImageVrs():
    Milef = '/etc/image-version'
    openatv = False
    if os.path.isfile(Milef):
        f = file(Milef,"r")
        file_read = f.readlines()
        for line in file_read:
            if 'openATV' in line:openatv = True
        f.close()
    return openatv
class IPTVInfoBarShowHide():
    """ InfoBar show/hide control, accepts toggleShow and hide actions, might start
    fancy animations. """
    STATE_HIDDEN = 0
    STATE_HIDING = 1
    STATE_SHOWING = 2
    STATE_SHOWN = 3
    def __init__(self):
        self['ShowHideActions'] = ActionMap(['InfobarShowHideActions'], {'toggleShow': self.toggleShow,
         'hide': self.hide}, 1)
        self.__event_tracker = ServiceEventTracker(screen=self, eventmap={iPlayableService.evStart: self.serviceStarted})
        self.__state = self.STATE_SHOWN
        self.__locked = 0
        self.hideTimer = eTimer()
        self.hideTimer.callback.append(self.doTimerHide)
        self.hideTimer.start(5000, True)
        self.onShow.append(self.__onShow)
        self.onHide.append(self.__onHide)
    def serviceStarted(self):
        if self.execing:
            if config.usage.show_infobar_on_zap.value:
                self.doShow()
    def __onShow(self):
        self.__state = self.STATE_SHOWN
        self.startHideTimer()
    def startHideTimer(self):
        if self.__state == self.STATE_SHOWN and not self.__locked:
            idx = config.usage.infobar_timeout.index
            if idx:
                self.hideTimer.start(idx * 1000, True)
    def __onHide(self):
        self.__state = self.STATE_HIDDEN
    def doShow(self):
        self.show()
        self.startHideTimer()
    def doTimerHide(self):
        self.hideTimer.stop()
        if self.__state == self.STATE_SHOWN:
            self.hide()
    def toggleShow(self):
        if self.__state == self.STATE_SHOWN:
            self.hide()
            self.hideTimer.stop()
        elif self.__state == self.STATE_HIDDEN:
            self.show()
    def lockShow(self):
        self.__locked = self.__locked + 1
        if self.execing:
            self.show()
            self.hideTimer.stop()
    def unlockShow(self):
        self.__locked = self.__locked - 1
        if self.execing:
            self.startHideTimer()
class Xtream_Player_New(Screen, InfoBarBase, IPTVInfoBarShowHide, InfoBarSeek, InfoBarAudioSelection, InfoBarSubtitleSupport):
    STATE_IDLE = 0
    STATE_PLAYING = 1
    STATE_PAUSED = 2
    ENABLE_RESUME_SUPPORT = True
    ALLOW_SUSPEND = True
    def __init__(self, session, recorder_sref = None,liste=None,indxto=None,Oldservice=None,server=None,_type=None):
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
        InfoBarAudioSelection.__init__(self)
        InfoBarSubtitleSupport.__init__(self)
        self.InfoBar_NabDialog = Label()
        self['Descriptions'] = Label()
        self.session = session
        self.Oldservice = Oldservice
        self.server = server
        self.service = None
        self._type = _type
        self['state'] = Label('')
        self['cont_play'] = Label('')
        self.cont_play = False
        self.trial_time = 30
        self.film_quality = None
        ret = '-'
        sert = '/h'
        self.recorder_sref = recorder_sref
        self['cover'] = Pixmap()
        self['cover_'] = Pixmap()
        self['cover_'].hide()
        mer = 'R'
        self.picload = ePicLoad()
        self.picfile = ''
        sew = 'r'
        self.playhack = ''
        self.img_loader = False
        if recorder_sref!=None:
            self.recorder_sref = recorder_sref
            self.session.nav.playService(recorder_sref)
            #return
        self.iptv_list = liste
        self.list_index = indxto
        self.Oldservice = Oldservice
        self.vod_entry = self.iptv_list[self.list_index]
        self.vod_url = self.vod_entry[4]
        self.title = self.vod_entry[1]
        self.descr = 'makache'#self.vod_entry[2]
        #Copy_Volum(str(indxto)+'\ndakhla=True','indexfil')
        Copy_Volum('indexfil='+str(indxto)+'\ndakhla=True','indexfil')
        #Copy_TouTou(str(STREAMS.list_index)+'\n'+str(self.vod_url)+'\n'+str(self.title))
        self.TrialTimer = eTimer()
        self.TrialTimer.callback.append(self.trialWarning)
        print 'evEOF=%d' % iPlayableService.evEOF
        self.__event_tracker = ServiceEventTracker(screen=self, eventmap={iPlayableService.evSeekableStatusChanged: self.__seekableStatusChanged,
            iPlayableService.evStart: self.__serviceStarted,
            iPlayableService.evEOF: self.__evEOF})
        self['actions'] = HelpableActionMap(self, 'nStreamPlayerVOD', {'exitVOD': self.exit,
            'get_link': self.show_link,
            'get_resum': self.resume_movie,
            'moreInfoVOD': self.show_more_info,
            'playnPreviousvideo_box': self.playnPreviousvideo_box,
            'playnextvideo_box': self.playnextvideo_box,
            'stopVOD': self.stopnew,
            'timeshift_autoplay': self.timeshift_autoplay,
            'timeshift': self.timeshift,
            'autoplay': self.autoplay,
            'prevVideo': self.prevVideo,
            'nextVideo': self.nextVideo,
            'power': self.power_off}, -1)
        self.get_player()
        self.onFirstExecBegin.append(self.play_vod_Stalker)
        self.onShown.append(self.setCover)
        self.onPlayStateChanged.append(self.__playStateChanged)
        self.StateTimer = eTimer()
        self.StateTimer.callback.append(self.trialWarning)
        self.play_vod = False
        self.state = self.STATE_PLAYING
        self.timeshift_url = None
        self.timeshift_title = None
        self.onShown.append(self.show_info)
        self.error_message = 'llalalalalala'
        return
    def resume_movie (self):
        #self.session.nav.playService(self.reference)
        self.player_helper()
    def show_link(self):
        self.session.open(MessageBox, 'Url Stream\n'+self._url.encode('utf-8'), type=MessageBox.TYPE_INFO)
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
            self.cont_play = self.cont_play
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
        self.cont_play = self.cont_play
    def show_info(self):
        if self.play_vod == True:
            self['state'].setText(' PLAY     >')
        self.hideTimer.start(5000, True)
        if self.cont_play:
            self['cont_play'].setText('Continue play ON')
        else:
            self['cont_play'].setText('Continue play OFF')
    def playnextvideo_box(self):
        index = self.list_index + 1
        video_counter = len(self.iptv_list)
        if index < video_counter and self.iptv_list[index][4] != None:
            descr = ''
            if self.iptv_list[index][2]:
                descr = self.iptv_list[index][2]
            title = self.iptv_list[index][1] + '\n\n' + str(descr)
            #Copy_Volum(str(index)+'\ndakhla=True','indexfil')
            Copy_Volum('indexfil='+str(index)+'\ndakhla=True','indexfil')
            self.session.openWithCallback(self.playnextvideo, MessageBox, _('PLAY NEXT VIDEO?\n%s') % title, type=MessageBox.TYPE_YESNO)
        return
    def playnPreviousvideo_box(self):
        index = self.list_index - 1
        video_counter = len(self.iptv_list)
        if index >= -1 and self.iptv_list[index][4] != None:
            descr = ''
            if self.iptv_list[index][2]:
                descr = self.iptv_list[index][2]
            title = self.iptv_list[index][1] + '\n\n' + str(descr)
            #Copy_Volum(index+'\ndakhla=True','indexfil')
            Copy_Volum('indexfil='+str(index)+'\ndakhla=True','indexfil')
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
    def Only_Back(self):#################
        self.session.open(MessageBox, 'Only ..... Back To Video', MessageBox.TYPE_INFO)
    def nextVideo(self):#################
        if self.recorder_sref:
            self.Only_Back()
            return
        self['cover_'].show()
        try:
            if self.list_index == len(self.iptv_list)-1:index = 0#Add by aime_jeux
            else:index = self.list_index + 1#Add by aime_jeux
            video_counter = len(self.iptv_list)
            if index < video_counter:
                if self.iptv_list[index][4] != None:
                    self.list_index = index
                    self.player_helper()
        except Exception as ex:
            print ex
            print 'EXC nextVideo'
        #Copy_Volum(index+'\ndakhla=True','indexfil')
        Copy_Volum('indexfil='+str(index)+'\ndakhla=True','indexfil')
    def prevVideo(self):
        if self.recorder_sref:
            self.Only_Back()
            return
        self['cover_'].show()
        try:
            if self.list_index == 0:index = len(self.iptv_list)-1#Add by aime_jeux
            else:index = self.list_index - 1#Add by aime_jeux
            if index > -1:
                if self.iptv_list[index][4] != None:
                    self.list_index = index
                    self.player_helper()
        except Exception as ex:
            print ex
            print 'EXC prevVideo'
        #Copy_Volum(index+'\ndakhla=True','indexfil')
        Copy_Volum('indexfil='+str(index)+'\ndakhla=True','indexfil')
    def player_helper(self):
        self.show_info()
        if self.vod_entry:
            self.vod_entry = self.iptv_list[self.list_index]
            self.vod_url = self.vod_entry[4]
            self.title = self.vod_entry[1]
            self.descr = self.vod_entry[2]
            #self.session.open(MessageBox, 'player_helper', type=MessageBox.TYPE_INFO)
        self.play_vod = False
        self.setCover()
        self.play_vod_Stalker()
    def setCover(self):
        # vod_entry = self.iptv_list[self.list_index]
        # self.session.open(MessageBox, 'setCover'+'\n'+str(self.vod_entry[7]), type=MessageBox.TYPE_INFO)
        try:
            vod_entry = self.iptv_list[self.list_index]
            self['cover'].instance.setPixmapFromFile(PLUGIN_PATH + '/img/clear.png')
            if self.vod_entry[7] != '':#Mod By aime_jeux
                if vod_entry[7].find('http') == -1:#Mod By aime_jeux
                    self.picfile = PLUGIN_PATH + '/img/playlist/' + vod_entry[7]#Mod By aime_jeux
                    self.decodeImage()
                    print 'LOCAL IMG VOD'
                    #self.session.open(MessageBox, 'LOCAL IMG VOD', type=MessageBox.TYPE_INFO)
                else:
                    if self.img_loader == False:
                        self.picfile = '%s/Stalker_tmp_pic.jpg' % '/tmp'
                        #self.session.open(MessageBox, self.picfile, type=MessageBox.TYPE_INFO)
                    else:
                        m = hashlib.md5()
                        m.update(self.vod_entry[7])#Mod By aime_jeux
                        cover_md5 = m.hexdigest()
                        self.picfile = '%s/%s.jpg' % ('/tmp', cover_md5)
                        #self.session.open(MessageBox, str(self.picfile), type=MessageBox.TYPE_INFO)
                    if os.path.exists(self.picfile) == False or self.img_loader == False:
                        #self.session.open(MessageBox, self.vod_entry[7].encode('utf-8')+'\n'+'coucou', type=MessageBox.TYPE_INFO)
                        Imgs = self.vod_entry[7].encode('utf-8').replace('https','http')
                        downloadPage(Imgs, self.picfile).addCallback(self.image_downloaded).addErrback(self.image_error)#Mod By aime_jeux
                    else:
                        self.decodeImage()
                if self._type == 'vod_serie':
                    try:
                        description = self.vod_entry[2][7]
                        self['Descriptions'].setText(str(description))
                    except:
                        self['Descriptions'].setText('....')
                else:
                    try:
                        description = self.vod_entry[2][self.list_index][7].encode('utf-8')
                        self['Descriptions'].setText(str(description))
                    except:
                        self['Descriptions'].setText('....')
        except Exception as ex:
            self.session.open(MessageBox, 'No update COVER', type=MessageBox.TYPE_INFO)
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
    def __evEOF(self):
        AE = eDVBVolumecontrol.getInstance().getVolume()
        Copy_Volum(AE,'volum')
        if not eDVBVolumecontrol.getInstance().isMuted():
            eDVBVolumecontrol.getInstance().volumeUnMute()
        else:
            eDVBVolumecontrol.getInstance().volumeUnMute()
            eDVBVolumecontrol.getInstance().setVolume(AE, AE)
    def __seekableStatusChanged(self):
        print 'seekable status changed!'
    def __serviceStarted(self):
        self['state'].setText(' PLAY     >')
        self['cont_play'].setText('Continue play OFF')
        self.state = self.STATE_PLAYING
        self.__evEOF()
    def doEofInternal(self, playing):
        if not self.execing:
            return
        if not playing:
            return
        print 'doEofInternal EXIT OR NEXT'
    def stopnew(self):
        if self.playhack == '':
            self.session.nav.stopService()
            self.play_vod = False
            self.session.nav.playService(self.Oldservice)
            self.exit()
    def trialWarning(self):
        self.StateTimer.start(self.trial_time * 1000, True)
        self.session.open(MessageBox, 'wait ...', type=MessageBox.TYPE_INFO, timeout=self.trial_time)
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
    def play_vod_Stalker(self):
        a,self._url = False,''
        try:
            if self.vod_url != '' and self.vod_url != None and len(self.vod_url) > 5:
                if self.vod_url.find('.ts') > 0:
                    print '------------------------ LIVE ------------------'
                    if self._type == 'iptv':a,self._url = get_donnees_Stalker_New(self.server,indxstream=self.vod_url,mode='TV')
                    elif self._type == 'MyIptv':a,self._url = True,self.vod_url.encode('utf-8')
                    else:a,self._url = get_donnees_Stalker_New(self.server,indxstream=self.vod_url,mode='VOD')
                    if a:
                        print str(eDVBVolumecontrol.getInstance().isMuted())
                        self.reference = eServiceReference(1, 0, self._url.encode('utf-8'))
                        self.reference.setName(self.title.encode('utf-8'))
                        self.session.nav.playService(self.reference)
                        self['cover_'].hide()
                else:
                    print '------------------------ movie ------------------'
                    printD('play_vod_Stalker','_type='+str(self._type))
                    if self._type == 'plutotv':a,self._url = True,self.vod_url
                    elif self._type == 'MyVideos':a,self._url = True,self.vod_url
                    elif self._type == 'MyIptv':a,self._url = True,self.vod_url.encode('utf-8')
                    elif self._type == 'iptv':a,self._url = get_donnees_Stalker_New(self.server,indxstream=self.vod_url,mode='TV')
                    else:a,self._url = get_donnees_Stalker_New(self.server,indxstream=self.vod_url,mode='VOD')
                    if a:
                        Copy_Volum('indexserv='+str(self.server)+'\nindxstream==='+self.vod_url,'Recup')
                        if get_ImageVrs():
                            self.session.open(MessageBox, 'Movie\nYou Are Now Watching\n'+'أنت تشاهد الان'.encode('utf-8')+'\n'+self.title.encode('utf-8'),type='',windowTitle=return_version(), timeout=3)
                        self.session.nav.stopService()
                        self.reference = eServiceReference(self.rds, 0, self._url.encode('utf-8'))
                        self.reference.setName(self.title.encode('utf-8'))
                        self.session.nav.playService(self.reference)
                        self['cover_'].hide()
                    else:
                        self.session.open(MessageBox, 'Movie\nNO VIDEOSTREAM FOUND\n'+ self.title.encode('utf-8'), type=MessageBox.TYPE_INFO)
                        self['cover_'].hide()
            else:
                if self.error_message:
                    self.session.open(MessageBox, self.error_message.encode('utf-8'), type=MessageBox.TYPE_ERROR)
                else:
                    self.session.open(MessageBox, 'NO VIDEOSTREAM FOUND'.encode('utf-8'), type=MessageBox.TYPE_ERROR)
                self.close()
        except Exception as ex:
            self.session.open(MessageBox, 'Not Found .....Tbahrna', type=MessageBox.TYPE_INFO)
            print ex
        return
    def parse_url(self):
        if self.playhack != '':
            self.vod_url = self.playhack
        print '++++++++++parse_url+++++++++++'
        try:
            url = self.vod_url
        except Exception as ex:
            print 'ERROR+++++++++++++++++parse_url++++++++++++++++++++++ERROR'
            print ex
    def power_off(self):
        self.close(1)
    def exit(self):
        # if self.playhack == '':
            # #Copy_Volum('indexfil='+str(index)+'\ndakhla=')
        self.close()
def Copy_Volum(what,cond):
    Milef = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/Cfg/'+cond
    if os.path.isfile(Milef):
        file_write = open(Milef, 'w')
        if cond == 'volum':file_write.write(cond+' = '+str(what))
        else:file_write.write(what)
        file_write.close()