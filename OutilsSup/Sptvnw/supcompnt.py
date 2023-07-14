#!/usr/bin/python
# -*- coding: utf-8 -*-
################################### modified by aime_jeux ##################################
#############                           Aout 2021                              #############
############################################################################################
from enigma import eTimer, RT_HALIGN_LEFT, RT_HALIGN_RIGHT, RT_HALIGN_CENTER, RT_VALIGN_CENTER, eListboxPythonMultiContent, gFont, getDesktop, ePicLoad, eServiceReference, iPlayableService
from Components.MenuList import MenuList
from httplib import HTTPException
import nVars
from Components.ActionMap import ActionMap
from Screens.Screen import Screen
from enigma import eTimer, iPlayableService
from Components.ServiceEventTracker import ServiceEventTracker
import base64
from Screens.MessageBox import MessageBox
import os
from os import system as os_system
from time import time
import sys
from xml.etree.cElementTree import fromstring, ElementTree
import urllib2
from datetime import datetime
import re
from skin import loadSkin
from Components.Task import Task, Job, job_manager as JobManager, Condition
from Components.config import config
from os import system
import socket
#####################################################################
if os.path.exists('/var/lib/dpkg/status'):
    enigmaos = 'oe2.2'
else:
    enigmaos = 'oe2.0'
#####################################################################MOD BY AIME_JEUX
CHANNEL_NUMBER = nVars.CHANNEL_NUMBER
CHANNEL_NAME = nVars.CHANNEL_NAME
FONT_0 = nVars.FONT_0
FONT_1 = nVars.FONT_1
BLOCK_H = nVars.BLOCK_H
NTIMEOUT = nVars.NTIMEOUT
#####################################################################
def channelEntryIPTVplaylist(entry):
    menu_entry = [entry, (eListboxPythonMultiContent.TYPE_TEXT,CHANNEL_NUMBER[0],CHANNEL_NUMBER[1],CHANNEL_NUMBER[2],
      CHANNEL_NUMBER[3],CHANNEL_NUMBER[4],RT_HALIGN_CENTER,'%s' % entry[0]), (eListboxPythonMultiContent.TYPE_TEXT,
      CHANNEL_NAME[0],CHANNEL_NAME[1],CHANNEL_NAME[2],CHANNEL_NAME[3],CHANNEL_NAME[4],RT_HALIGN_LEFT,entry[1])]
    return menu_entry
#####################################################################
session = None
def get_adrs_image():
    return config.plugins.SupTVoDNeWConfig.Posters.value
class iptv_streamse():
    def __init__(self):
        global MODUL
        self.iptv_list = []
        self.plugin_version = ''
        self.list_index = 0
        self.username = ''
        self.password = ''
        self.iptv_list_tmp = []
        self.list_index_tmp = 0
        self.playlistname_tmp = ''
        self.video_status = False
        self.groups = []
        self.server_oki = True
        self.user_mac = ''
        self.playlistname = ''
        self.next_page_url = ''
        self.next_page_text = ''
        self.prev_page_url = ''
        self.prev_page_text = ''
        self.portal = ''
        self.url = ''
        self.trial = ''
        self.trial_time = 30
        self.NR1JwTlhSYVV6a3lZakpS = ''
        self.use_rtmpw = False
        self.esr_id = 4097
        self.play_vod = False
        self.go_back = False
        self.film_info = []
        self.xml_error = ''
        self.ar_id_start = 0
        self.ar_id_player = 0
        self.iptv_list_history = []
        self.iptv_list_Tlker = []
        self.ar_exit = True
        self.ar_start = True
        self.ar_id_end = 0
        self.clear_url = ''
        self.my_favorites = []
        self.img_loader = False
        self.images_tmp_path = get_adrs_image()+'/'
        self.moviefolder = '/hdd/MovieSuptvod'#'/hdd/movie'
        self.meldung = ''
        self.trial = ''
        self.banned_text = ''
        self.trial_time = 30
        self.timeout_time = 10
        self.security_param = ''
        self.password = '1234'
        self.cont_play = False
        self.systems = ''
        self.playhack = ''
        self.url_tmp = ''
        self.security_key = ''
        self.delete_images = ''
        self.next_page_url_tmp = ''
        self.next_page_text_tmp = ''
        self.prev_page_url_tmp = ''
        self.prev_page_text_tmp = ''
        self.disable_audioselector = False
        self.oldServiceK = ''
        MODUL = html_parser_moduls()
    def getValue(self, definitions, default):
        ret = ''
        Len = len(definitions)
        return Len > 0 and definitions[Len - 1].text or default
    def read_config(self):
        try:
            tree = ElementTree()
            sone = base64.b64decode('WVVoU01HTklUVFpNZVRsNlpGaENNR1JwTlhSYVV6a3lZakpSZGxwWE5IbE1ia0p2WTBFOVBRPT0=')
            stow = base64.b64decode(sone)
            stre = base64.b64decode(stow)
            NR1JwTlhSYVV6a3lZakpS = stre
            if NR1JwTlhSYVV6a3lZakpS and NR1JwTlhSYVV6a3lZakpS != '':
                self.NR1JwTlhSYVV6a3lZakpS = NR1JwTlhSYVV6a3lZakpS
                self.url = self.NR1JwTlhSYVV6a3lZakpS
            plugin_version = ''
            if plugin_version and plugin_version != '':
                self.plugin_version = plugin_version
            mymcodes = open('/etc/code', 'r')
            iscodes = mymcodes.read()
            username = iscodes
            if username and username != '':
                self.username = username
            mymacs = open('/tmp/mac', 'r')
            ismacs = mymacs.read()
            password = ismacs
            if password and password != '':
                self.password = password
            esr_id = ''
            if esr_id and esr_id != '':
                self.esr_id = int(esr_id)
            ar_id = ''
            if ar_id and ar_id != '':
                self.ar_id_player = int(ar_id)
            else:
                self.ar_id_player = self.ar_id_start
                self.ar_start = False
            ar_id_end = ''
            if ar_id_end and ar_id_end != '':
                self.ar_id_end = int(ar_id_end)
            else:
                self.ar_exit = False
            self.img_loader = self.getValue(xml.findall('images_tmp'), False)
            self.images_tmp_path = self.getValue(xml.findall('images_tmp_path'), self.images_tmp_path)
            self.moviefolder = self.getValue(xml.findall('moviefolder'), self.moviefolder)
            self.disable_audioselector = self.getValue(xml.findall('disable_audioselector'), self.disable_audioselector)
        except Exception as ex:
            print '++++++++++ERROR READ CONFIG+++++++++++++'
            print ex
    def reset_buttons(self):
        self.kino_title = ''
        self.next_page_url = None
        self.next_page_text = ''
        self.prev_page_url = None
        self.prev_page_text = ''
        return
    def get_list(self, url = None):
        self.xml_error = ''
        self.url = url
        self.clear_url = url
        self.list_index = 0
        self.iptv_list = []
        self.iptv_list_temp = []
        xml = None
        self.next_request = 0
        try:
            print '!!!!!!!!-------------------- URL %s' % url
            if url.find('username') > -1:
                self.next_request = 1
            if any([url.find('.ts') > -1, url.find('.mp4') > -1]):
                self.next_request = 2
            xml = self._request(url)
            if xml:
                self.next_page_url = ''
                self.next_page_text = ''
                self.prev_page_url = ''
                self.prev_page_text = ''
                self.playlistname = xml.findtext('playlist_name').encode('utf-8')
                self.next_page_url = xml.findtext('next_page_url')
                next_page_text_element = xml.findall('next_page_url')
                if next_page_text_element:
                    self.next_page_text = next_page_text_element[0].attrib.get('text').encode('utf-8')
                self.prev_page_url = xml.findtext('prev_page_url')
                prev_page_text_element = xml.findall('prev_page_url')
                if prev_page_text_element:
                    self.prev_page_text = prev_page_text_element[0].attrib.get('text').encode('utf-8')
                chan_counter = 1
                for channel in xml.findall('channel'):
                    name = channel.findtext('title').encode('utf-8')
                    name = base64.b64decode(name)
                    if 'All'.lower() in name.lower():continue
                    piconname = channel.findtext('logo')
                    description = channel.findtext('description')
                    desc_image = channel.findtext('desc_image')
                    img_src = ''
                    if description != None:
                        description = description.encode('utf-8')
                        if desc_image:
                            img_src = desc_image
                        description = base64.b64decode(description)
                        description = description.replace('<br>', '\n')
                        description = description.replace('<br/>', '\n')
                        description = description.replace('</h1>', '</h1>\n')
                        description = description.replace('</h2>', '</h2>\n')
                        description = description.replace('&nbsp;', ' ')
                        description4playlist_html = description
                        text = re.compile('<[\\/\\!]*?[^<>]*?>')
                        description = text.sub('', description)
                    stream_url = channel.findtext('stream_url')
                    playlist_url = channel.findtext('playlist_url')
                    category_id = channel.findtext('category_id')
                    ts_stream = channel.findtext('ts_stream')
                    chan_tulpe = (chan_counter,name,description,piconname,stream_url,playlist_url,category_id,
                        img_src,description4playlist_html,ts_stream)
                    self.iptv_list_temp.append(chan_tulpe)
                    chan_counter = chan_counter + 1
        except Exception as ex:
            print ex
            self.xml_error = ex
            print '!!!!!!!!!!!!!!!!!! ERROR: XML to LISTE'
        if len(self.iptv_list_temp):
            self.iptv_list = self.iptv_list_temp
        else:
            print 'ERROR IPTV_LIST_LEN = %s' % len(self.iptv_list_temp)
        return
    def Copy_Donnees(self,what,pth):
        Milef = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/Cfg/'+pth
        if os.path.isfile(Milef):
            file_write = open(Milef, 'w')
            file_write.write(what)
            file_write.close()
    def _request(self, url):
        url = url.strip(' \t\n\r')
        if self.next_request == 1:
            url = url
        elif self.next_request == 0:
            url = url + '?' + 'username=' + self.username + '&password=' + self.password
        else:
            url = url
        print url
        try:
            req = urllib2.Request(url, None, {'User-agent': 'SupVod En2',
             'Connection': 'Close'})
            if self.server_oki == True:
                xmlstream = urllib2.urlopen(req, timeout=NTIMEOUT).read()
                Copy_xmls(str(xmlstream))
            res = fromstring(xmlstream)
        except Exception as ex:
            print ex
            print 'REQUEST Exception'
            res = None
            self.xml_error = ex
        return res
    def get_Infos_Abonnement(self):#Add by aime_jeux
        if not os.path.isfile('/etc/code'):
            pass
        A1,A2,A3 = '','',''
        if os.path.isfile('/etc/uniqid'):
            system("ifconfig eth0 | awk '/HWaddr/ {printf $5}' > /tmp/mac")
            mac1 = open('/tmp/mac', 'r')
            mac = mac1.read()
            code = open('/etc/code', 'r')
            mycode = code.read()
            PATH = '/etc/uniqid'
            if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
                unicid = open('/etc/uniqid', 'r')
                myunicid = unicid.read()
                get_url = 'http://enigma.suptv.me/e2/info.php?co=%s&ma=%s&hash=%s&core=openpli' % (mycode, mac, myunicid)
                try:
                    mx = urllib2.urlopen(get_url)
                    getpage = mx.read()
                    view = getpage
                    Copy_line(view)
                    A1,A2,A3 = Get_line()
                except (urllib2.URLError, HTTPException, socket.error):
                    Copy_line('',a='Account Status:Inactive')
        else:Copy_line('',a='Account Status:Inactive')
    def get_Infos_UrlFreeAbonnement(self,url):#Add by aime_jeux
        Free_serv,name,password,Host = '','','',''
        url = url
        try:name = re.findall('username=(.+?)&',url)[0]
        except:name='nada'
        try:
            if '&type=' in url:password = re.findall('password=(.+?)&',url)[0]
            else:password = url.split('password=')[1]
        except:password='nada'
        try:Host = url.split('//')[1].split('/')[0]
        except:Host='nada'
        if name !='nada' and password !='nada' and Host !='nada':Free_serv = 'http://'+Host+'/player_api.php?username='+str(name)+'&password='+str(password)
        else:Free_serv='nada'
        return Free_serv
    def get_Infos_FreeAbonnement(self,url):#Add by aime_jeux
        status,exp_date,max_connections,Free_Host,_Donnees = '','','','',''
        import requests,json
        from time import ctime
        Href = self.get_Infos_UrlFreeAbonnement(url)
        if Href != 'nada':
		try:
		    data            = requests.get(Href).json()
		except:
		    data = 'nada'
		if data!='nada':
		    try:
		        status          = 'status : '+str(data['user_info']['status'])
		    except:
		        status          = 'status : None'
		    try:
		        exp_date        = 'exp_date : '+str(ctime(int(data['user_info']['exp_date'])))
		    except:
		        exp_date        = 'exp_date : None'
		    try:
		        max_connections = 'max_connections : '+str(data['user_info']['max_connections'])
		    except:
		        max_connections = 'max_connections : None'
		    try:
		        Free_Host       = 'Free_Host : '+str(data['server_info']['url'])
		    except:
		        Free_Host       = 'Free_Host : None'
		    _Donnees            = Free_Host+'\n'+status+'\n'+exp_date+'\n'+max_connections
		    _Donnees            = str(Href)+'\n'+_Donnees
		else:_Donnees = str(Href)+'\n makach'
		return _Donnees
try:
    from Tools.Directories import fileExists, pathExists
    from Components.Network import iNetwork
except Exception as ex:
    print ex
    print 'IMPORT ERROR'
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
def debug(obj, text = ''):
    print datetime.fromtimestamp(time()).strftime('[%H:%M:%S]')
    print text + ' %s\n' % obj
class downloadJob(Job):
    def __init__(self, toolbox, cmdline, filename, filetitle):
        Job.__init__(self, 'Download: %s' % filetitle)
        self.filename = filename
        self.toolbox = toolbox
        self.retrycount = 0
        downloadTask(self, cmdline, filename)
    def retry(self):
        self.retrycount += 1
        self.restart()
    def cancel(self):
        self.abort()
class downloadTask(Task):
    ERROR_CORRUPT_FILE, ERROR_RTMP_ReadPacket, ERROR_SEGFAULT, ERROR_SERVER, ERROR_UNKNOWN = range(5)
    def __init__(self, job, cmdline, filename):
        Task.__init__(self, job, _('Downloading ...'))
        self.postconditions.append(downloadTaskPostcondition())
        self.setCmdline(cmdline)
        self.filename = filename
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
                os_system('rm -f %s' % self.filename)
            else:
                self.error = self.ERROR_UNKNOWN
        elif line.startswith('wget:'):
            if line.find('server returned error') != -1:
                self.error = self.ERROR_SERVER
        elif line.find('Segmentation fault') != -1:
            self.error = self.ERROR_SEGFAULT
    def afterRun(self):
        if self.getProgress() == 0 or self.getProgress() == 100:
            message = 'Movie successfully transfered to your HDD!' + '\n' + self.filename
            web_info(message)
from urllib import quote_plus
def web_info(message):
    try:
        message = quote_plus(str(message))
        cmd = "wget -qO - 'http://127.0.0.1/web/message?type=2&timeout=10&text=%s' 2>/dev/null &" % message
        debug(cmd, 'CMD -> Console -> WEBIF')
        os.popen(cmd)
    except:
        print 'web_info ERROR'
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
VIDEO_ASPECT_RATIO_MAP = {0: '4:3 Letterbox',
 1: '4:3 PanScan',
 2: '16:9',
 3: '16:9 Always',
 4: '16:10 Letterbox',
 5: '16:10 PanScan',
 6: '16:9 Letterbox'}
####################################################################
def Copy_line(what,a=None,b=None,c=None):
    Milef = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/Cfg/Server'
    if a == None:
        if os.path.isfile(Milef):
            file_write = open(Milef, 'w')
            file_write.write(what)
            file_write.close()
    else:
        file_write = open(Milef, 'w')
        file_write.write(a)
        file_write.close()
def Get_line(cond=None):
    A1,A2,A3 = '','',''
    Milef = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/Cfg/Server'
    if os.path.isfile(Milef):
        f = file(Milef,"r")
        file_read = f.readlines()
        if cond!=None:return (str(file_read)).replace("[","").replace("]","").replace("'","").replace(",","").replace("\n\n","\n")
        for line in file_read:
            if 'Account Status' in line:
                A1 = line.replace('\n','')
            if 'Expir Date' in line:
                A2 = line.replace('\n','')
            if 'Remaining' in line:
                A3 = line.replace('\n','')
        f.close()
    return A1,A2,A3
####################################################################Add by aime_jeux
def Copy_lineFilms(what,ouktoub):
    Milef = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/Cfg/index'
    A1 = ''
    if os.path.isfile(Milef):
        if ouktoub == '' and what != '':
            file_write = open(Milef, 'w')
            file_write.write(what)
            file_write.close()
            A1 = 'kotibet'
        else:
            f = file(Milef,"r")
            file_read = f.readlines()
            for line in file_read:
                if 'IndexFilms:' in line:
                    A1 = line.replace('\n','')
                    A1 = int(A1.split(':')[1])
            f.close()
    return A1
def Copy_xmls(what):
    Milef = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/Cfg/Donnees'
    A1 = ''
    if os.path.isfile(Milef):
        file_write = open(Milef, 'w')
        file_write.write(what)
        file_write.close()
##################################################################
def debug(obj, text = ''):
    print datetime.fromtimestamp(time()).strftime('[%H:%M:%S]')
    print '%s' % text + ' %s\n' % obj
class html_parser_moduls():
    def __init__(self):
        self.video_list = []
        self.next_page_url = ''
        self.next_page_text = ''
        self.prev_page_url = ''
        self.prev_page_text = ''
        self.search_text = ''
        self.search_on = ''
        self.active_site_url = ''
        self.playlistname = ''
        self.playlist_cat_name = ''
        self.kino_title = ''
        self.category_back_url = ''
        self.error = ''
    def reset_buttons(self):
        self.kino_title = ''
        self.next_page_url = None
        self.next_page_text = ''
        self.prev_page_url = None
        self.prev_page_text = ''
        self.search_text = ''
        self.search_on = None
        return
    def get_list(self, url):
        debug(url, 'MODUL URL: ')
        self.reset_buttons()
##############################################################
def is_ascii(s):
    try:
        s.decode('ascii')
    except UnicodeDecodeError:
        try:s.decode('utf-8')
        except UnicodeDecodeError:
            return False
    else:
        return True
def colorize(txt,selcolor='white',marker1=":",marker2="]"):
    if enigmaos == "oe2.2" or  is_ascii(txt)==False:
        return txt
    colors={'black':'\c00000000','white':'\c00??????','grey':'\c00808080',
    'blue':'\c000000??','green':'\c0000??00','red':'\c00??0000','ivory':"\c0???????",
    'yellow':'\c00????00','cyan':'\\c0000????','magenta':'\c00??00??'}
    color=colors.get(selcolor,'\c0000????')
    color1=colors.get('cyan','\c0000????')
    try:
        if not marker1 in txt :
            return color+" "+txt
        txtparts=txt.split(marker1)
        txt1=txtparts[0]
        txt2=txtparts[1]
        if marker2 in txt:
            txt3=txt2.split(marker2)#[0]
            if len(txt3)>=2:
                if txt3[1]!='':
                    txt3,txt4 = txt3[0],txt3[1]
                    ftxt=txt1+" "+color+marker1+txt3+color1+txt4
                else:
                    txt3= txt3[0]
                    ftxt=txt1+" "+color+marker1+txt3#+marker2
        else:
            txt3=txt2
            ftxt=txt1+" "+color+marker1+txt3#+marker2
        return ftxt
    except:
        return txt
def colorize_1(txt,selcolor='white',marker1="[",marker2="]"):
    if enigmaos == "oe2.2" or  is_ascii(txt)==False:
        return txt
    colors={'black':'\c00000000','white':'\c00??????','grey':'\c00808080',
    'blue':'\c000000??','green':'\c0000??00','red':'\c00??0000','ivory':"\c0???????",
    'yellow':'\c00????00','cyan':'\\c0000????','magenta':'\c00??00??'}
    color=colors.get('cyan','\c0000????')
    return color+txt
####################################################################Add by aime_jeux
import fileinput,sys
PATH_SKINS = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/Skins'
def ImportSkinwithimag():
    Line_1 = ''
    Line_2 = ''
    Mege = ImportNumImaG()
    n = 5
    x = 1
    A = int(Mege)
    if A == n:
        WriteNumImage('1')
        for line in fileinput.input(PATH_SKINS + '/nPlaylistFHD.xml', inplace=1):
            if 'main_supvod' + str(A) in line:
                line = line.replace('main_supvod' + str(A), 'main_supvod1')
            sys.stdout.write(line)
    else:
        WriteNumImage(str(A + 1))
        for line in fileinput.input(PATH_SKINS + '/nPlaylistFHD.xml', inplace=1):
            if 'main_supvod' + str(A) in line:
                line = line.replace('main_supvod' + str(A), 'main_supvod' + str(A + 1))
            sys.stdout.write(line)
def ImportNumImaG():
    H = ''
    Path_1 = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/Cfg/NumImag'
    ptfile = open(Path_1, 'r')
    data = ptfile.readlines()
    ptfile.close()
    H = data[0].replace('\n', '').replace('\t', '').replace('\r', '')
    return H
def WriteNumImage(numimag):
    f = file('/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/Cfg/NumImag', 'w')
    f.write(numimag)
    f.close()
####################################################################Add by aime_jeux
# importer infos free_serveurs
import os
Fold = '/media/hdd'
Fold_0 = '/media/hdd/SupTvNew'
Fold_1 = "/tmp/SupTvNew"
MyFolderIptv = '/etc/enigma2/SupTvNew/Iptv.xml'
if os.path.exists(Fold) and os.path.ismount(Fold):
    if os.path.exists(Fold_0):
        MyFolder = True
    else:
        os.mkdir(Fold_0)
        MyFolder = True
else:
    if os.path.exists(Fold_1):
        MyFolder = False
    else:
        os.mkdir(Fold_1)
        MyFolder = False
if os.path.isfile(MyFolderIptv):
    MyFolderXml = True
else:
    MyFolderXml = False
def get_InfosOXml():
        import xml.etree.ElementTree as ET
        MyListInfosiptvstalker = []
        if MyFolderXml:
            tree = ET.parse(MyFolderIptv)
            for element in tree.iter('iptv'):
                namehost = element.find('namehost').text
                namehost = namehost.encode('utf-8')
                protocol = element.find('protocol').text
                protocol = protocol.encode('utf-8')
                host = element.find('host').text
                host = host.encode('utf-8')
                port = element.find('port').text
                port = port.encode('utf-8')
                usr = element.find('usr').text
                usr = usr.encode('utf-8')
                passw = element.find('passw').text
                passw = passw.encode('utf-8')
                url = str(protocol)+'://'+str(host)+':'+str(port)+'/enigma2.php?username='+str(usr)+'&password='+str(passw)
                MyListInfosiptvstalker.append((namehost,url))
                # for t in range(8):
                    # T +=MyListInfosiptvstalker[indx][t]+'\n'
        return MyListInfosiptvstalker
###############################################################################
def get_journalsat():
    import requests,re,time
    St = requests.Session()
    m3u,data = 'nada',400
    href = 'http://iptv.journalsat.com/index.php'
    llnk = 'http://iptv.journalsat.com/get.php'
    uro = 'http://iptv.journalsat.com/get.php?do=cccam'
    hdr = {'Host': 'iptv.journalsat.com',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
           'Accept-Encoding': 'gzip, deflate',
           'Content-Type': 'application/x-www-form-urlencoded',
           'Content-Length': '24',
           'Origin': 'http://iptv.journalsat.com',
           'Connection': 'keep-alive',
           'Referer': 'http://iptv.journalsat.com/get.php?do=cccam',
           'Upgrade-Insecure-Requests': '1'}
    prm = {"do": "cccam","doccam": "generate"}
    try:data = St.post(href,headers=hdr,verify=False).status_code
    except:data=400
    if data == 200:
        try:data1 = St.get(llnk,headers=hdr,verify=False).status_code
        except:data1=400
        if data1 == 200:
            try:tata = St.post(uro,headers=hdr,data=prm,verify=False).content
            except:tata='nada'
            if tata!='nada':
                try:
                    m3u = re.findall("href='(.+?)&type=m3u&output=mpegts'",tata)[0]
                    m3u = re.findall('username=(.+?)&',m3u)[0]
                except:m3u='nada'
    if m3u!='nada':return change_xml_element(m3u)
    else:return 'nada'
def change_xml_element(elem):
    if elem == 'nada':return elem
    import xml.etree.ElementTree as ET
    filename = "/etc/enigma2/SupTvNew/Iptv.xml"
    xmlTree = ET.parse(filename)
    rootElement = xmlTree.getroot()
    for element in rootElement.findall("iptv"):
        if element.find('namehost').text == 'journalsat' :
            element.find('usr').text = elem       
    xmlTree.write(filename,encoding='UTF-8',xml_declaration=True)
    return str(elem)