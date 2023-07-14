#!/usr/bin/python
# -*- coding: utf-8 -*-
################################### modified by aime_jeux ##################################
#############                           Aout 2021                              #############
############################################################################################
############################################################################################
from Screens.TaskView import JobView
from Components.Task import Task, Job, job_manager as JobManager, Condition
from Tools import Notifications, ASCIItranslit
import re,json
############################################################################################
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Sptvnw.Setup import get_Posters,get_TMDB,get_IMDB
PLUGIN_PATH = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW'
###########################################################################
import json
import os
import sys
from os import listdir
from urllib import quote_plus
from Components.MultiContent import MultiContentEntryText
from Screens.InputBox import InputBox
from Components.Input import Input
from Screens.MessageBox import MessageBox
from Components.AVSwitch import AVSwitch
from Tools.BoundFunction import boundFunction
from enigma import ePoint, eSize, eTimer,ePicLoad
from Tools.Directories import fileExists
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmap, MultiContentEntryPixmapAlphaTest, MultiContentEntryPixmapAlphaBlend
from enigma import getDesktop, eListboxPythonMultiContent, eListbox, eTimer, gFont, RT_HALIGN_LEFT, RT_HALIGN_RIGHT, RT_HALIGN_CENTER, RT_WRAP, loadPNG
###########################################################################
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
###########################################################################
from Screens.Screen import Screen
class FullHD(Screen):
    skin = '<screen name="Userm3u3" position="0,0" size="1056,1080" title="IPTVworld" flags="wfNoBorder" backgroundColor="transparent"><widget name="list" position="11,79" size="800,700" zPosition="4" scrollbarMode="showNever" /><widget name="text" position="11,10" size="800,65" zPosition="0" font="Regular;30" halign="center" valign="center" transparent="0" foregroundColor="#f4df8d" backgroundColor="#41000000" /></screen>'
def show_Userm3u(letter):
    print letter
    if dwidth == 1280:
        res = [letter]
        res.append(MultiContentEntryText(pos=(2, 2), size=(450, 31), font=3, text=letter, backcolor=1118481, flags=RT_HALIGN_LEFT))
        return res
    else:
        res = [letter]
        res.append(MultiContentEntryText(pos=(2, 2), size=(800, 31), font=5, text=letter, backcolor_sel=26214, backcolor=1090519040, flags=RT_HALIGN_CENTER))
        return res
def showlist(data, list):
    icount = 0
    plist = []
    for line in data:
        name = data[icount]
        plist.append(show_Userm3u(name))
        icount = icount + 1
    list.setList(plist)
###########################################################################
if os.path.exists('/var/lib/dpkg/status'):
    enigmaos = 'oe2.2'
else:
    enigmaos = 'oe2.0'
#################################################################################
from enigma import getDesktop
dwidth = getDesktop(0).size().width()
################################################################################################
class MesImports():
    def __init__(self,Indx=None):
        self.FolderPoster = get_Posters()
        self.Milef = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/Cfg/indexfil'
        self.Indx = Indx
        self.IndxReturn = 'nada'
        self.picload = ePicLoad()
        self.default = PLUGIN_PATH + '/img/playlist/tmdb_default.png'
        #########################################
    def Recovery_indx(self):
        H = '0'
        if os.path.isfile(self.Milef):
            file_write = open(self.Milef, 'r')
            data = file_write.readlines()
            file_write.close()
            H = data[0].replace('\n', '').replace('\t', '').replace('\r', '')
            H = H.split('=')[1].replace(' ','')
            Y = data[1].replace('\n', '').replace('\t', '').replace('\r', '')
            Y = Y.split('=')[1].replace(' ','')
        return H,Y
    def is_ascii(self,s):
        try:
            s.decode('ascii')
        except UnicodeDecodeError:
            try:s.decode('utf-8')
            except UnicodeDecodeError:
                return False
        else:
            return True
    def _colorize_(self,txt,selcolor='white',marker="=="):
        if enigmaos == "oe2.2" or  self.is_ascii(txt)==False:
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
    def get_Taille(self):
        folder_size = 0
        folder = self.FolderPoster
        for (path, dirs, files) in os.walk(folder):
            for file in files:
                filn_ = os.path.join(path, file)
                folder_size += os.path.getsize(filn_)
        Taille = "%0.3f MB" % (folder_size/(1024*1024.0))
        return str(Taille)
    def web_info(self,message):
        try:
            message = quote_plus(str(message))
            cmd = "wget -qO - 'http://127.0.0.1/web/message?type=1&timeout=3&text=%s' 2>/dev/null &" % message
            os.popen(cmd)
        except:
            print 'web_info ERROR'
    def Nety_txt(self,txt):
        if '.  ' in txt:
            txt = txt.split('.  ')[1]
        return txt
    def Get_Infos_selected(self,Hd):
        Mytxt,Mytxt_1 = '',''
        self.Hd = Hd
        if self.Hd == 0:
            Mytxt = Txt_go
            Mytxt_1 = Txt_go_1
        elif self.Hd == 1:
            Mytxt = Txt_suptv
            Mytxt_1 = Txt_suptv_1
        elif self.Hd == 2:
            Mytxt = Txt_iptv
            Mytxt_1 = Txt_iptv_1
        elif self.Hd == 3:
            Mytxt = Txt_stalker
            Mytxt_1 = Txt_stalker_1
        elif self.Hd == 4:
            Mytxt = Txt_plutotv
            Mytxt_1 = Txt_plutotv_1
        elif self.Hd == 5:
            Mytxt = Txt_plutotvsecond
            Mytxt_1 = Txt_plutotvsecond_1
        elif self.Hd == 6:
            Mytxt = Stirr
            Mytxt_1 = Stirr_1
        elif self.Hd == 7:
            Mytxt = Txt_m3u
            Mytxt_1 = Txt_m3u_1
        elif self.Hd == 8:
            Mytxt = foldmovies
            Mytxt_1 = foldmovies_1
        else:
            Mytxt=Txt_settings
            Mytxt_1=Txt_settings_1
        return Mytxt,Mytxt_1
    def remove_ImagesT(self):
        fname1 = self.FolderPoster
        test=os.listdir(fname1)
        for item in test:
            for v in ['.jpg','.png']:
                if item.endswith(v):
                    os.remove(fname1+item)
    def get_correct_name(self,txt):
        txt = re.sub("[\(\[].*?[\)\]]", "", txt)#suprim entre parenth
        txt = re.sub(r"\b\d+\b", "", txt).strip()#suprim int
        txt = txt.replace('  ','')
        return txt
    def get_Ext_Vod(self,_url):#
        self._url = _url
        self.ende = 'mp4'
        if '.mkv' in self._url:
            self.ende = 'mkv'
        elif '.mp4' in self._url:
            self.ende = 'mp4'
        elif '.avi' in self._url:
            self.ende = 'avi'
        elif '.flv' in self._url:
            self.ende = 'flv'
        return self.ende
    def get_stalker_filename(self,title,_url):#
        self.title = title
        self._url = _url
        useragent = "--header='User-Agent: QuickTime/7.6.2 (qtver=7.6.2;os=Windows NT 5.1Service Pack 3)'"
        title_translit = self.get_correct_name(self.title)
        filn_ = ASCIItranslit.legacyEncode(title_translit + '.') + self.get_Ext_Vod(self._url)
        filn_ = filn_.replace('(', '_')
        filn_ = filn_.replace(')', '_')
        filn_ = filn_.replace('#', '')
        filn_ = filn_.replace('+', '_')
        filn_ = filn_.encode('utf-8')
        return useragent,filn_
    def Write_Js(self,txt):
        path = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/Cfg/DownloadMovies.js'
        with open(path,'w') as chcfg:
            json.dump(txt, chcfg,ensure_ascii=False)
        print "OK"
    def get_date(self):
        from datetime import date
        today = date.today()
        self.datim = today.strftime("%d_%m_%Y")
        return self.datim
    def get_url_stal_epis(self,api,stream,episode):
        self.ep_url=api+'/portal.php?type=vod&action=create_link&cmd='+stream+'&series='+episode+'&forced_storage=&disable_ad=0&download=0&force_ch_link_check=0&JsHttpRequest=1-xml'
        return self.ep_url
    def get_player(self):
        self.rds = 4097
        defaultPlayer,serviceApp = self.selectPlayer()
        if serviceApp:
            if defaultPlayer == 'gstplayer':self.rds = 5001
            elif defaultPlayer == 'exteplayer3':self.rds = 5002
        return self.rds
    def selectPlayer(self):
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
    ########################################################## go to page Stalker video VOD
    def Condition_2(self,Nmbr):
        if self.Indx is None:
            self.IndxReturn = 'nada'
        elif str(self.Indx) == '':
            self.IndxReturn = 'nada'
        else:
            self.Indx = str(self.Indx).replace(' ','')
            if int(self.Indx) > int(Nmbr):
                self.IndxReturn = 'hihi'
            elif int(self.Indx) == 0:
                self.IndxReturn = 1
            else:
                self.IndxReturn = int(self.Indx)
        return self.IndxReturn
    ########################################################## Download Image with wget
    def Copy_Donnees(self,what):
        Milef = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/Cfg/foldImag'
        if os.path.isfile(Milef):
            file_write = open(Milef, 'w')
            file_write.write(str(what))
            file_write.close()
    def image_downloaded(self):
        if 'None' in self.picfile:
            os.remove(self.picfile)
            self.picfile = self.default
        elif self.picfile==self.FolderPoster:
            self.picfile = self.default
        else:
            self.picfile = self.picfile
        return self.picfile
    def Download_Image(self,img,Poster,stirr=None):
        self.cond = ''
        if stirr:
            if '.png' in img.split('/')[-1]:self.cond=stirr+'.png'
            elif '.jpg' in img.split('/')[-1]:self.cond=stirr+'.jpg'
            else:self.cond=img.split('/')[-1]
        else:self.cond=img.split('/')[-1]
        self.Poster = Poster
        if fileExists(self.FolderPoster + self.cond):
            self.picfile = self.FolderPoster + self.cond
            self.decodeImage()
            return
        self.cmdlist = []
        from os import system as os_system
        self.wget = '/usr/bin/wget --no-check-certificate'
        try:
            self.picfile=self.FolderPoster + self.cond
            a="%s -O '" % self.wget + self.picfile+"' -c '" + img + "'"
            os_system(a)
        except:
            self.picfile = self.default
        self.decodeImage()
    def decodeImage(self):
        try:
            # x = self['poster'].instance.size().width()
            # y = self['poster'].instance.size().height()
            x = self.Poster.instance.size().width()
            y = self.Poster.instance.size().height()
            picture = self.image_downloaded()#self.picfile
            self.Copy_Donnees(picture)
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
        #self['poster'].show()
        self.Poster.show()
        try:
            ptr = self.picload.getData()
            if ptr:
                #self['poster'].instance.setPixmap(ptr.__deref__())
                self.Poster.instance.setPixmap(ptr.__deref__())
        except Exception as ex:
            print ex
####################################################################################
# DOWNLOAD MANAGER
class downloadJob(Job):
    def __init__(self, toolbox, cmdline, filn_, filetitle):
        Job.__init__(self, 'SupTVoDNeW Download: %s' % filetitle)
        self.filn_ = filn_
        self.toolbox = toolbox
        self.retrycount = 0
        downloadTask(self, cmdline, filn_)
    def retry(self):
        self.retrycount += 1
        self.restart()
    def cancel(self):
        self.abort()
# DOWNLOAD TASKS
class downloadTask(Task):
    ERROR_CORRUPT_FILE, ERROR_RTMP_ReadPacket, ERROR_SEGFAULT, ERROR_SERVER, ERROR_UNKNOWN = range(5)
    def __init__(self, job, cmdline, filn_):
        Task.__init__(self, job, _('SupTVoDNeW Downloading ...'))
        self.postconditions.append(downloadTaskPostcondition())
        self.setCmdline(cmdline)
        self.filn_ = filn_
        self.toolbox = job.toolbox
        self.error = None
        self.lasterrormsg = None
        return
    def processOutput(self, data):
        try:
            if data.endswith('%)'):
                startpos = data.rfind('sec (') + 5
                if startpos and startpos != -1:
                    self.progress = int(float(data[startpos:-4]))
            elif data.find('%') != -1:
                tmpvalue = data[:data.find('%')]
                tmpvalue = tmpvalue[tmpvalue.rfind(' '):].strip()
                tmpvalue = tmpvalue[tmpvalue.rfind('(') + 1:].strip()
                self.progress = int(float(tmpvalue))
            else:
                Task.processOutput(self, data)
        except Exception as errormsg:
            print 'Error processOutput: ' + str(errormsg)
            Task.processOutput(self, data)
    def processOutputLine(self, line):
        line = line[:-1]
        self.lasterrormsg = line
        if line.startswith('ERROR:'):
            if line.find('RTMP_ReadPacket') != -1:
                self.error = self.ERROR_RTMP_ReadPacket
            elif line.find('corrupt file!') != -1:
                self.error = self.ERROR_CORRUPT_FILE
                system('rm -f %s' % self.filn_)
            else:
                self.error = self.ERROR_UNKNOWN
        elif line.startswith('wget:'):
            if line.find('server returned error') != -1:
                self.error = self.ERROR_SERVER
        elif line.find('Segmentation fault') != -1:
            self.error = self.ERROR_SEGFAULT
    def afterRun(self):
        if self.getProgress() == 0 or self.getProgress() == 100:
            message = 'SupTVoDNeW \nMovie Successfully Transfered To Your HDD!' + '\n' + self.filn_
            MesImports().web_info(message)
# DOWNLOAD RECOVERY
class downloadTaskPostcondition(Condition):
    RECOVERABLE = True
    def check(self, task):
        if task.returncode == 0 or task.error is None:
            return True
        else:
            return False
            return
    def getErrorMessage(self, task):
        return {task.ERROR_CORRUPT_FILE: _('Video Download Failed!\n\nCorrupted Download File:\n%s' % task.lasterrormsg),
         task.ERROR_RTMP_ReadPacket: _('Video Download Failed!\n\nCould not read RTMP-Packet:\n%s' % task.lasterrormsg),
         task.ERROR_SEGFAULT: _('Video Download Failed!\n\nSegmentation fault:\n%s' % task.lasterrormsg),
         task.ERROR_SERVER: _('Video Download Failed!\n\nServer returned error:\n%s' % task.lasterrormsg),
         task.ERROR_UNKNOWN: _('Video Download Failed!\n\nUnknown Error:\n%s' % task.lasterrormsg)}[task.error]