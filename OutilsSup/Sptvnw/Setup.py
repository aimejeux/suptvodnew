#!/usr/bin/python
# -*- coding: utf-8 -*-
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Sptvnw.ConfigListSupt import ConfigListSuptScreen
from supcompnt import *
from Screens.Standby import TryQuitMainloop
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from enigma import eTimer
from Components.Label import Label
from Components.ConfigList import ConfigList, ConfigListScreen
from Components.config import config, NoSave,ConfigSelection, getConfigListEntry, ConfigSubsection, configfile, ConfigText,ConfigDirectory
from Tools.Directories import fileExists, pathExists
from Components.ActionMap import NumberActionMap, ActionMap
import os
import re
from Screens.LocationBox import LocationBox
###############################################################################
Version = 'Vrs_1.0'
_VERSION_ = '1.0'
ChIptv_1 = 'This Choice For a Free Link For Iptv You Need Host, Port, Username, Password'+'\n'+'هذا الاختيار تحتاج فيه الى وضع الهوست والبور واسم المستخدم كذا كلمة السر'
ChIptv_2 = 'This option is for suptv subscribers '+'\n'+'هذا الاختيار خاص بالمشتركين في سوب تيفي'
ChIptv_4 = 'With This Choice, You Must Set The Protocol, Host, Port And Mac '+'\n'+'هذا الاختيار يتوجب عليك وضع البروتوكول و الهوست والبور و الماك'
ChIptv_5 = 'This Option Means To Use All Of Them'+'\n'+'هذا الاخيار يعني استعمالها كلها'
ChIptv_6 = 'This Choice Is For The Use Of The Plugin Reader'+'\n'+'هذا الاختيار لاستعمال القارئ التابع للبلوغين'
ChIptv_6_1 = 'This option Means Mo Use The MoviePlayer Reader If It Is Present In The Image Used'+'\n'+'هذا الاختيار يعني استعمال القارئ موفيبلاير ان كان موجودا في الصورة المستعملة'
ChIptv_7 = 'This Choice Means Accepting The Change Of Entry Skin'+'\n'+'هذا الاختيار يعني قبول تغيير سكين الدخول'
ChIptv_3 = 'This Choice Is To Keep You Informed Of a New Version'+'\n'+'هذا الاختيار لموافاتك بوجود نسخة جديدة'
ChIptv_3_1 = 'This Option Is To Disable Your Notification Of A New Version '+'\n'+'هذا الاختيار لتعطيل موافاتك بوجود نسخة جديدة'
Pluttvtxt = 'This Option Selects The Proxy To Fetch The Data '+'\n'+'هذا الاختيار لتحديد الوكيل لجلب البيانات'
def SearchIpBox():
    Doss = '/etc/network/interfaces'
    IpBox = ''
    if fileExists(Doss):
        ecmf = open(Doss, 'rb')
        ecm = ecmf.readlines()
        try:
            for line in ecm:
                if 'address' in line:
                    IpBox = line.split(' ')[1].replace('\n', '').replace('\t', '').replace(' ', '').replace('\r', '').replace('\\s', '')
        except:
            IpBox = 'Not Find'
    return IpBox
def get_IpConnec():
    import requests
    _Ip,data = '',''
    url='http://checkip.amazonaws.com/'
    try:
        data=requests.get(url,timeout=10).content
    except:data='nada'
    if data!='nada' and data!='':_Ip = data.replace('\n','')
    else:_Ip = 'not Found'
    return _Ip
def selectPlayer():#thk's faraj
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
def get_Adrs_mac():
    mac = ''
    try:
        import uuid
        mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        mac = mac.replace('\n', '').replace('\t', '').replace('\r', '').replace('\\s', '').replace('\\d', '').replace(' ', '')
    except:
        mac = 'Not Found'
    return mac
def ImportDonneeServer(ind,nme):
    H = ''
    Path_1 = '/tmp/SuptvServer'
    if fileExists(Path_1):
        ptfile = open(Path_1, 'r')
        data = ptfile.readlines()
        ptfile.close()
        try:
            H = data[ind].replace('\n', '').replace('\t', '').replace('\r', '')
            H = H.split('=')[1]
        except:H=nme
    else:H=nme
    return H
def get_Infos_FreeAbonnement(host,port,name,passw):#Add by aime_jeux
    status,exp_date,max_connections,Free_Host,_Donnees,Infos = '','','','','',''
    import requests,json
    from time import ctime
    host = host.replace(' ','')
    port = port.replace(' ','')
    name = name.replace(' ','')
    passw = passw.replace(' ','')
    A1 = colorize('Host : '+str(host),selcolor='cyan')
    A2 = colorize('Port : '+str(port),selcolor='cyan')
    A3 = colorize('username : '+str(name),selcolor='cyan')
    A4 = colorize('password : '+str(passw),selcolor='cyan')
    Infos = A1+'\n'+A2+'\n'+A3+'\n'+A4
    Href = 'http://'+host+':'+str(port)+'/player_api.php?username='+str(name)+'&password='+str(passw)
    try:
        data             = requests.get(Href).json()
    except:
        data = 'nada'
    if data!='nada':
        try:
            status       = 'status : '+str(data['user_info']['status'])
            status       = colorize(status,selcolor='cyan')
        except:
            status       = 'status : None'
            status       = colorize(status,selcolor='cyan')
        try:
            exp_date     = 'exp_date : '+str(ctime(int(data['user_info']['exp_date'])))
            exp_date     = colorize(exp_date,selcolor='cyan')
        except:
            exp_date     = 'exp_date : None'
            exp_date     = colorize(exp_date,selcolor='cyan')
        try:
            max_connections = 'max_connections : '+str(data['user_info']['max_connections'])
            max_connections = colorize(max_connections,selcolor='cyan')
        except:
            max_connections = 'max_connections : None'
            max_connections = colorize(max_connections,selcolor='cyan')
        try:
            Free_Host       = 'Free_Host : '+str(data['server_info']['url'])
            Free_Host       = colorize(Free_Host,selcolor='cyan')
        except:
            Free_Host       = 'Free_Host : None'
            Free_Host       = colorize(Free_Host,selcolor='cyan')
        _Donnees            = Free_Host+'\n'+status+'\n'+exp_date+'\n'+max_connections
        _Donnees            = Infos+'\n'+_Donnees
    else:_Donnees = Infos+'\n makach'
    return _Donnees
###############################################################################
config.plugins.SupTVoDNeWConfig = ConfigSubsection()
config.plugins.SupTVoDNeWConfig.notification = ConfigSelection(default='disabled', choices=[('disabled', _('Disabled')), 
    ('enabled', _('Enabled'))])
config.plugins.SupTVoDNeWConfig.ChoosIptv = ConfigSelection(default='all', choices=[('suptvod', _('Suptvod')), ('freeiptv', _('Freeiptv')),('stalker', _('Stalker')),('freeiptv+stalker', _('Freeiptv+Stalker')),('all', _('All'))])
config.plugins.SupTVoDNeWConfig.ChoosLecteurMedia = ConfigSelection(default='suptvod', choices=[('suptvod', _('Suptvod')), ('moviePlayer', _('MoviePlayer'))])
config.plugins.SupTVoDNeWConfig.Host = ConfigText(default=ImportDonneeServer(0,'Your Host'), visible_width=50, fixed_size=False)
config.plugins.SupTVoDNeWConfig.Port = ConfigText(default=ImportDonneeServer(1,'Your Port'), visible_width=50, fixed_size=False)
config.plugins.SupTVoDNeWConfig.Username = ConfigText(default=ImportDonneeServer(2,'Your Username'), visible_width=50, fixed_size=False)
config.plugins.SupTVoDNeWConfig.Password = ConfigText(default=ImportDonneeServer(3,'Your Password'), visible_width=50, fixed_size=False)
config.plugins.SupTVoDNeWConfig.Activskin = ConfigSelection(default='yes', choices=[('yes', _('Yes')), ('no', _('No'))])
config.plugins.SupTVoDNeWConfig.IpBox = ConfigText(default=SearchIpBox(), visible_width=50, fixed_size=False)
config.plugins.SupTVoDNeWConfig.Plutotv = ConfigSelection(default='fr', choices=[('fr', _('FR')), ('uk', _('UK')),('us', _('US')),('it', _('IT')),('es', _('ES')),('de', _('DE'))])
config.plugins.SupTVoDNeWConfig.Plutotvsamsung = ConfigSelection(default='with', choices=[('without', _('Without SamsungTv')), ('with', _('With SamsungTv'))])
config.plugins.SupTVoDNeWConfig.MacAdress = ConfigText(default=get_Adrs_mac(), visible_width=50, fixed_size=False)
config.plugins.SupTVoDNeWConfig.ActivUpdattime = ConfigSelection(default='yes', choices=[('yes', _('Yes')), ('no', _('No'))])
config.plugins.SupTVoDNeWConfig.M3u = ConfigDirectory(default='/tmp/')
config.plugins.SupTVoDNeWConfig.Posters = ConfigDirectory(default='/tmp/')
config.plugins.SupTVoDNeWConfig.Tmdb = ConfigSelection(default='disabled', choices=[('disabled', _('Disabled')),('enabled', _('Enabled'))])
config.plugins.SupTVoDNeWConfig.TmdbToken = ConfigText(default='Your Token', visible_width=50, fixed_size=False)
config.plugins.SupTVoDNeWConfig.TmdbLang = ConfigSelection(default='fr', choices=[('fr', _('FR')), ('en', _('EN')),('us', _('US')),('it', _('IT')),('es', _('ES')),('de', _('DE'))])
config.plugins.SupTVoDNeWConfig.Imdb = ConfigSelection(default='disabled', choices=[('disabled', _('Disabled')),('enabled', _('Enabled'))])
config.plugins.SupTVoDNeWConfig.ImdbToken = ConfigText(default='k_7nggq46b', visible_width=50, fixed_size=False)
config.plugins.SupTVoDNeWConfig.ImdbLang = ConfigSelection(default='fr', choices=[('fr', _('FR')), ('uk', _('UK')),('us', _('US')),('it', _('IT')),('es', _('ES')),('de', _('DE'))])
PATH_SKINS = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/Skins'
def get_Posters():
    return config.plugins.SupTVoDNeWConfig.Posters.value
def get_TMDB():
    A = config.plugins.SupTVoDNeWConfig.TmdbToken.value
    B = config.plugins.SupTVoDNeWConfig.TmdbLang.value
    if config.plugins.SupTVoDNeWConfig.Tmdb.value == 'enabled':
        return A,B
    else:
        return '','fr'
def get_IMDB():
    A = config.plugins.SupTVoDNeWConfig.ImdbToken.value
    B = config.plugins.SupTVoDNeWConfig.ImdbLang.value
    if config.plugins.SupTVoDNeWConfig.Imdb.value == 'enabled':
        return A,B
    else:
        return '','fr'
def get_Tmdbvalue():
    return config.plugins.SupTVoDNeWConfig.Tmdb.value
class SupTVoDNeW_Config(Screen, ConfigListSuptScreen):
    def __init__(self, session):
        with open(PATH_SKINS + '/SetupFHD.xml', 'r') as f:
            self.skin = f.read()
            f.close()
        self.session = session
        Screen.__init__(self, session)
        self.onChangedEntry = []
        self.list = []
        ConfigListSuptScreen.__init__(self, self.list, session=self.session, on_change=self.changedEntry)
        self['setupActions'] = ActionMap(['SetupActions', 'ColorActions', 'DirectionActions','MenuActions'], {'green': self.keySave,
         #'blue': self.KeyBlue,
         #'yellow': self.KeyYellow,
         'red': self.keyClose,
         'cancel': self.keyClose,
         'ok': self.ok,
         'left': self.keyLeft,
         'right': self.keyRight,
         'up': self.up,
         'down': self.down
         }, -2)
        for x in range(1,20):
            self['Box_'+str(x)] = Label()
        self.ListFreeServer = ['Your Host','Your Port','Your Username','Your Password']
        self.runSetupVod()
    def KeyBlue(self):
        config.plugins.SupTVoDNeWConfig.Host.value = ImportDonneeServer(0,'Your Host')
        config.plugins.SupTVoDNeWConfig.Port.value = ImportDonneeServer(1,'Your Port')
        config.plugins.SupTVoDNeWConfig.Username.value = ImportDonneeServer(2,'Your Username')
        config.plugins.SupTVoDNeWConfig.Password.value = ImportDonneeServer(3,'Your Password')
        self.runSetupVod()
    def KeyYellow(self):
        _Donnees = ''
        if config.plugins.SupTVoDNeWConfig.notification.value == 'enabled' and config.plugins.SupTVoDNeWConfig.ChoosIptv.value == 'freeiptv':
            host = config.plugins.SupTVoDNeWConfig.Host.value
            port = config.plugins.SupTVoDNeWConfig.Port.value
            name = config.plugins.SupTVoDNeWConfig.Username.value
            passw = config.plugins.SupTVoDNeWConfig.Password.value
            if host!='Your Host' and port!='Your Port' and name!='Your Username' and passw!='Your Password':
                _Donnees = get_Infos_FreeAbonnement(host,port,name,passw)
            else:_Donnees ='Vérifiez Vos Données ... \n'+'Check Your Data ...'
        else:_Donnees ='Vous Trouverez Vos Données Dans MainMenu ... \n'+'You Will Find Your Data In MainMenu ...'
        self['Box_2'].setText(_Donnees)
    def ImportSkinwithimag(self):
        Line_1 = ''
        Line_2 = ''
        Mege = ImportNumImaG()
        n = 4
        x = 1
        A = int(Mege)
        if A == n:
            WriteNumImage('1')
            for line in fileinput.input(PLUGIN_PATH + '/SetupFHD.xml', inplace=1):
                if 'main_supvod' + str(A) in line:
                    line = line.replace('main_supvod' + str(A), 'Freeservers_1')
                sys.stdout.write(line)
        else:
            WriteNumImage(str(A + 1))
            for line in fileinput.input(PLUGIN_PATH + '/SetupFHD.xml', inplace=1):
                if 'main_supvod' + str(A) in line:
                    line = line.replace('main_supvod' + str(A), 'main_supvod' + str(A + 1))
                sys.stdout.write(line)
        with open(PLUGIN_PATH + '/SetupFHD.xml', 'r') as f:
            self.skin = f.read()
            f.close()
    def runSetupSupNew(self):
        self.list = []
        self.list.append(getConfigListEntry(_('Notify on_off'), config.plugins.SupTVoDNeWConfig.notification))
        self['config'].list = self.list
        self['config'].setList(self.list)
        self['Box_3'].setText('')
        self['Box_1'].setText('Notify Disable')
    def runSetupVod(self):
        self.list.append(getConfigListEntry(_('Notify'), config.plugins.SupTVoDNeWConfig.notification))
        self.list = []
        self.list.append(getConfigListEntry(_('Notify'), config.plugins.SupTVoDNeWConfig.notification))
        if config.plugins.SupTVoDNeWConfig.notification.value == 'enabled':
            self.list.append(getConfigListEntry(_('Choix IPTV'), config.plugins.SupTVoDNeWConfig.ChoosIptv))
            self.list.append(getConfigListEntry(_('Choix Mediaplayer'), config.plugins.SupTVoDNeWConfig.ChoosLecteurMedia)) 
            self.list.append(getConfigListEntry(_('Skin Change'), config.plugins.SupTVoDNeWConfig.Activskin))
            self.list.append(getConfigListEntry(_('Ip Box'), config.plugins.SupTVoDNeWConfig.IpBox))
            self.list.append(getConfigListEntry(_('Pluto Tv'), config.plugins.SupTVoDNeWConfig.Plutotv))
            self.list.append(getConfigListEntry(_('Plutotv SamsungTv'),config.plugins.SupTVoDNeWConfig.Plutotvsamsung))
            self.list.append(getConfigListEntry(_('Mac Adress'), config.plugins.SupTVoDNeWConfig.MacAdress))
            self.list.append(getConfigListEntry(_('AutoUpdat'), config.plugins.SupTVoDNeWConfig.ActivUpdattime))
            self.list.append(getConfigListEntry(_('Adress M3u File'), config.plugins.SupTVoDNeWConfig.M3u))
            self.list.append(getConfigListEntry(_('Adress Poster File'), config.plugins.SupTVoDNeWConfig.Posters))
            self.list.append(getConfigListEntry(_('TMDB'),config.plugins.SupTVoDNeWConfig.Tmdb))
            if config.plugins.SupTVoDNeWConfig.Tmdb.value == 'enabled':
                self.list.append(getConfigListEntry(_('Tmdb Token'),config.plugins.SupTVoDNeWConfig.TmdbToken))
                self.list.append(getConfigListEntry(_('Tmdb Lang'),config.plugins.SupTVoDNeWConfig.TmdbLang))
            self.list.append(getConfigListEntry(_('IMDB'),config.plugins.SupTVoDNeWConfig.Imdb))
            if config.plugins.SupTVoDNeWConfig.Imdb.value == 'enabled':
                self.list.append(getConfigListEntry(_('Imdb Token'),config.plugins.SupTVoDNeWConfig.ImdbToken))
                self.list.append(getConfigListEntry(_('Imdb Lang'),config.plugins.SupTVoDNeWConfig.ImdbLang))
            self['config'].list = self.list
            self['config'].setList(self.list)
            if config.plugins.SupTVoDNeWConfig.ActivUpdattime.value == 'yes':
                Updattime = 'Active'
                self['Box_3'].setText('      AutoUpdate..Time... ' + str(Updattime))
            else:
                self['Box_3'].setText('      AutoUpdat Time ... Disabled')
            self.Index_Infos_1()
    def Index_Infos_1(self):
        DH = '\n/etc/enigma2/SupTvNew/Iptv.xml'
        HH = self['config'].l.getCurrentSelectionIndex()
        ADS = self['config'].list[HH][0]
        ADS_1 = self['config'].list[HH][1].value
        if config.plugins.SupTVoDNeWConfig.notification.value == 'enabled':
            if ADS == 'Notify':
                self['Box_1'].setText('Notify Enable')
            elif config.plugins.SupTVoDNeWConfig.ChoosIptv.value == 'freeiptv' and ADS == 'Choix IPTV':
                self['Box_1'].setText(ChIptv_1+DH)
            elif config.plugins.SupTVoDNeWConfig.ChoosIptv.value == 'suptvod' and ADS == 'Choix IPTV':
                self['Box_1'].setText(ChIptv_2+DH)
            elif config.plugins.SupTVoDNeWConfig.ChoosIptv.value == 'stalker' and ADS == 'Choix IPTV':
                self['Box_1'].setText(ChIptv_4+DH)
            elif config.plugins.SupTVoDNeWConfig.ChoosIptv.value == 'all' and ADS == 'Choix IPTV':
                self['Box_1'].setText(ChIptv_5+DH)
            elif config.plugins.SupTVoDNeWConfig.ChoosLecteurMedia.value == 'suptvod' and ADS == 'Choix Mediaplayer':
                self['Box_1'].setText(ChIptv_6)
            elif config.plugins.SupTVoDNeWConfig.ChoosLecteurMedia.value == 'moviePlayer' and ADS == 'Choix Mediaplayer':
                self['Box_1'].setText(ChIptv_6_1)
            elif config.plugins.SupTVoDNeWConfig.Activskin.value == 'yes' and ADS == 'Skin Change':
                self['Box_1'].setText(ChIptv_7)
            elif config.plugins.SupTVoDNeWConfig.ActivUpdattime.value == 'yes'  and ADS == 'AutoUpdat':
                self['Box_1'].setText(ChIptv_3)
            elif config.plugins.SupTVoDNeWConfig.ActivUpdattime.value == 'no'  and ADS == 'AutoUpdat':
                self['Box_1'].setText(ChIptv_3_1)
            elif ADS == 'Pluto Tv':
                self['Box_1'].setText(Pluttvtxt)
            elif ADS == 'Plutotv SamsungTv':
                self['Box_1'].setText('With Or Without SamsungTv \n'+'لاستعمال أو بدون استعمال سامسونغ تيفي')
            elif ADS == 'Adress M3u File':
                self['Box_1'].setText('Press OK to change location\n'+'اضغط على زر اوكي لتحديد مسار الملف')
            elif ADS == 'Adress Poster File':
                self['Box_1'].setText('Press OK to change location\n'+'اضغط على زر اوكي لتحديد مسار الملف')
            elif ADS == 'TMDB':
                self['Box_1'].setText('This Is The Option To Set The Movie Database\n'+'هذا الاختيار لوضع قاعدة بيانات الفيلم')
            elif ADS == 'Tmdb Token':
                self['Box_1'].setText('This Is The Choice For Setting The Search Token\n'+'هذا الختيار لوضع التوكن الخاص بالبحث')
            elif ADS == 'Tmdb Lang':
                self['Box_1'].setText('This Option Selects The Search Language\n'+'هذا الاختيار لتحديد لغة البحث')
			####################"
            elif ADS == 'IMDB':
                self['Box_1'].setText('This Is The Option To Set Internet Movie Database\n'+'هذا الاختيار لوضع قاعدة بيانات الأفلام على الإنترنت')
            elif ADS == 'Imdb Token':
                self['Box_1'].setText('This Is The Choice For Setting The Search Token\n'+'هذا الختيار لوضع التوكن الخاص بالبحث')
            elif ADS == 'Imdb Lang':
                self['Box_1'].setText('This Option Selects The Search Language\n'+'هذا الاختيار لتحديد لغة البحث')
            else:self['Box_1'].setText(ADS + '  '+str(ADS_1))
        # elif config.plugins.SupTVoDNeWConfig.notification.value == 'disabled':self['Box_1'].setText('Notify Disable')
        # else:self['Box_1'].setText('.......')
    def up(self):
        Indx = self['config'].l.getCurrentSelectionIndex()
        if Indx == 0:
            #self['config'].pageDown()
            self['config'].setCurrentIndex(len(self.list)-1)
        else:
            self['config'].moveUp()
        self.Index_Infos_1()
    def down(self):
        Indx = self['config'].l.getCurrentSelectionIndex()
        if Indx == len(self.list)-1:
            #self['config'].pageUp()
            self['config'].setCurrentIndex(0)
        else:
            self['config'].moveDown()
        self.Index_Infos_1()
    def keyLeft(self):
        ConfigListSuptScreen.keyLeft(self)
        if config.plugins.SupTVoDNeWConfig.notification.value == 'enabled':
            self.runSetupVod()
        else:
            self.runSetupSupNew()
    def keyRight(self):
        ConfigListSuptScreen.keyRight(self)
        if config.plugins.SupTVoDNeWConfig.notification.value == 'enabled':
            self.runSetupVod()
        else:
            self.runSetupSupNew()
    def keySave(self):
            for x in self['config'].list:
                if x[0] == 'Ip Connect':continue
                x[1].save()
            configfile.save()
            if config.plugins.SupTVoDNeWConfig.notification.value == 'enabled':
                mesageboxint = ''
                if config.plugins.SupTVoDNeWConfig.ActivUpdattime.value == 'yes':
                    Updattime = 'Active'
                    self['Box_3'].setText('You Have Chosen..Time\n' + str(Updattime) + '\n To Update Your Servers')
                else:
                    self['Box_3'].setText('AutoUpdat Time ... Disabled')
            else:
                self['Box_3'].setText('')
            self.session.openWithCallback(self.restartenigma, MessageBox, _('SupTVoDNeW  ' + Version+'\nDo You Want To Restart Igu \n'+'هل تريد اعادة تشغيل الانغما'), MessageBox.TYPE_YESNO)
    def restartenigma(self, result):
        if result:
            self.session.open(TryQuitMainloop, 3)
    def keyClose(self):
        for x in self['config'].list:
            x[1].cancel()
        self.close()
    def ok(self):
        sel = self['config'].getCurrent()[1]
        if sel and sel == config.plugins.SupTVoDNeWConfig.M3u:
            self.setting = 'adrsm3u'
            self.openDirectoryBrowser(config.plugins.SupTVoDNeWConfig.M3u.value)
        if sel and sel == config.plugins.SupTVoDNeWConfig.Posters:
            self.setting = 'adrsposter'
            self.openDirectoryBrowser(config.plugins.SupTVoDNeWConfig.Posters.value)
        ConfigListSuptScreen.keyOK(self)
    def openDirectoryBrowser(self, path):
        try:
            self.session.openWithCallback(
                self.openDirectoryBrowserCB,
                LocationBox,
                windowTitle=_('Choose Directory:'),
                text=_('Choose directory'),
                currDir=str(path),
                bookmarks=config.movielist.videodirs,
                autoAdd=False,
                editDir=True,
                inhibitDirs=['/bin', '/boot', '/dev', '/home', '/lib', '/proc', '/run', '/sbin', '/sys', '/var'],
                minFree=15)
        except Exception as e:
            print("[jmxSettings] openDirectoryBrowser get failed: %s" % e)
        """
        except:
            pass
            """
    def openDirectoryBrowserCB(self, path):
        if path is not None:
            if self.setting == 'adrsm3u':
                config.plugins.SupTVoDNeWConfig.M3u.setValue(path)
            if self.setting == 'adrsposter':
                config.plugins.SupTVoDNeWConfig.Posters.setValue(path)
        return