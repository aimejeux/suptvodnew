#!/usr/bin/python
# -*- coding: utf-8 -*-
################################### modified by aime_jeux ##################################
#############                           Aout 2021                              #############
############################################################################################
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Stalker.InfobarStalker import Xtream_Player_New,Copy_Volum
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Sptvnw.Config import show_Menu_PlutoTv,show_menu_list_secondpluto
from Plugins.Extensions.SupTVoDNeW.OutilsSup.PlutoTvSecond.ImportData import ImportData
from Plugins.Extensions.SupTVoDNeW.OutilsSup.MyPlutoTv.plutoimport import PlutotvNew
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Sptvnw.MesImports import MesImports
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Sptvnw.Config import *
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Sptvnw.Setup import *
from Plugins.Extensions.SupTVoDNeW.OutilsSup.Sptvnw.Setup import SupTVoDNeW_Config
Version = 'SupTVoDNeW V_1.0'
PATH_SKINS = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/Skins'
PLUGIN_PATH = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW'
############################################################################################
import requests,shutil
from time import ctime
from Tools.Directories import fileExists
from Components.config import config
from time import gmtime, localtime, strftime, time
from Components.Sources.StaticText import StaticText
from enigma import eServiceReference
from enigma import ePoint, eSize, eTimer
from enigma import eTimer,ePicLoad
from Components.AVSwitch import AVSwitch
from twisted.web.client import downloadPage
from Tools.BoundFunction import boundFunction
import os,sys,time
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.Label import Label
from Components.ActionMap import ActionMap, HelpableActionMap, NumberActionMap
from Components.Pixmap import Pixmap
from enigma import getDesktop
dwidth = getDesktop(0).size().width()
###########################################################################################
global Lis_Clean
Lis_Clean_0 = ['mtv','music','clubbing tv','isra','israel','adult','adulte','adults','xxx','xx','porn','18','hard','sex',
               'hard','ado','blowjob','lesbie','travest','anal','frisson']
Lis_Clean_1 = ['sex','xxl','hotclub','venus','playb','hust','libid','penthouse','spice','platinum','amatix','xx',
               'vivid','brazzers','colmax','daring','lover','man-x','man x','manx','pink_x','pink-x','pink x','pinkx','reality kings','stars xxx',
               'pink show','pink-show','pink_show','pinkshow','porn','brazz','lov','adult','hust','candy']
Lis_Clean = Lis_Clean_0+Lis_Clean_1
###########################################################################################
####################################### Menu Servers ######################################
###########################################################################################
from datetime import datetime
def get_Loading():
    T = 'Loading  ...... List Live TV %s.. ' % 'Please wait'
    return True,T
def log(data):
	now = datetime.now().strftime('%Y-%m-%d %H:%M')
	open('/tmp/SupTVoDNeW.log', 'a').write(now+' : '+str(data)+'\r\n')
class Screen_MyPlutoTvNew_Second(Screen):
    def __init__(self, session):
        ########################Session_Skin############################
        if dwidth == 1280:
            with open(PATH_SKINS + '/PlutoTv_Second_FHD.xml', 'r') as f:
                self.skin = f.read()
                f.close()
        else:
            with open(PATH_SKINS + '/PlutoTv_Second_FHD.xml', 'r') as f:
                self.skin = f.read()
                f.close()
        self.session = session
        Screen.__init__(self, session)
        self['actions'] = ActionMap(['DirectionActions','SetupActions','ColorActions'], {'ok': self.ok,
            'cancel': self.Exit_plug,
            'red': self.Exit_plug,
            '2': self.Chouff,
            '1': self.showhide_listprogramme,
            'yellow': self.Settings,
            'blue': self.show_hide_menu,
            'green': self.ok,
            'up': self.keyUp,
            'down': self.keyDown,
            'left': self.left,
            'right': self.right
            }, -1)
        self.proxyvalue = ''
        self.initialservice = self.session.nav.getCurrentlyPlayingServiceReference()
        self.onShown.append(self.show_all_chang)
        self.samsungtv = config.plugins.SupTVoDNeWConfig.Plutotvsamsung.value
        self.Headers = ''
        self.List_MoviePlayer_1 = []
        self['Infos'] = Label()
        self['Title'] = Label()
        self['Infoselect'] = Label()
        self['myproxy'] = Label()
        self['Infodiscript'] = Label()
        self['menu_Plutotv_Second'] = m2list([])
        self['menu_list_catego'] = m2list([])
        self['menu_list_catego'].hide()
        self['listprogramme'] = m2list([])
        self['listprogramme'].hide()
        self.Chouf,self.Mylist,self.Mydict = [],[],{}
        self['poster'] = Pixmap()
        self.picload = ePicLoad()
        self.imports = False
        self.secondlist = False
        self.showhide = False
        self.hidden = False
        self.sh_hd=False
        self.TXT = ''
        self.idx = 0
        # for x in range(5):
            # if x == 0:self['Info_'+str(x)] =StaticText()
            # else:self['Info_'+str(x)] = Label()
        self.get_ListIptvFnl()
    def Chouff(self):
        self.session.open(MessageBox, str(self['menu_Plutotv_Second'].getCurrent()[0][1]), MessageBox.TYPE_INFO)
    def get_ListIptvFnl(self):
        self.Mylist,self.Mydict = [],{}
        a,self.Mydict =  ImportData().getChannels_Pluto()
        i = 1
        if a:
            self.imports = True
            self.Headers = self.Mydict['headers'].get('user-agent','')
            self.dons = self.Mydict['regions']
            for keys in self.dons:
                name_ = keys.encode('utf-8')
                title = self.dons[keys].get('name','').encode('utf-8')
                logo = self.dons[keys].get('logo','').encode('utf-8')
                self.Mylist.append(show_Menu_PlutoTv(str(i)+'.  '+title,logo,name_))
                i = i + 1
        else:
            self.Mylist.append(show_Menu_PlutoTv('Not Found', 'menu', ''))
        self['menu_Plutotv_Second'].show()
        self['menu_Plutotv_Second'].l.setList(self.Mylist)
        self['menu_Plutotv_Second'].l.setItemHeight(37)
        self.currentList = 'menu_Plutotv_Second'
        self['menu_Plutotv_Second'].selectionEnabled(1)
        self['menu_Plutotv_Second'].moveToIndex(0)
        self['Title'].setText('Pluto Tv Second')
        self.Get_Infos_select()
    def Get_Infos_select(self):
        Hd = self.Nety_txt(self[self.currentList].getCurrent()[0][0])
        self['Infoselect'].setText(Hd)
        if self.currentList == 'menu_Plutotv_Second':
            self['Title'].setText(self['menu_Plutotv_Second'].getCurrent()[0][0])
            self.proxyvalue = self['menu_Plutotv_Second'].getCurrent()[0][2]
            Txts = MesImports()._colorize_('Your Proxy=='+str(self.proxyvalue),selcolor='cyan')
            self['myproxy'].setText(Txts)
            self.Download_Image()
        else:
            self.get_infos_movies()
            ddx = len(self.Chouf)
            self['Title'].setText(self['menu_Plutotv_Second'].getCurrent()[0][0]+' ['+str(ddx)+' Data]')
            self.Download_Image()
            #self.Get_Changement()
    def get_infos_movies(self):
        if self.imports and self.secondlist:
            self.listprogramme = []
            _Ttl = self['menu_list_catego'].getCurrent()[0][0]
            _sid = self['menu_list_catego'].getCurrent()[0][7]
            discrpt,self.listprogramme = ImportData().Programmes_Pluto(_Ttl,self.Mydict,str(self.proxyvalue),_sid)
            self['Infodiscript'].setText(str(discrpt))
            self['listprogramme'].l.setList(self.listprogramme)
            self['listprogramme'].l.setItemHeight(37)
            self.sh_hd=True
    def showhide_listprogramme(self):
        if self.imports and self.secondlist:
            if self.sh_hd:
                self['listprogramme'].show()
                self.sh_hd = False
            else:
                self['listprogramme'].hide()
                self.sh_hd = True
    def Nety_txt(self,txt):
        if '.  ' in txt:
            txt = txt.split('.  ')[1]
        return txt
    def ok(self):
        Link_stream = ''
        self.Chouf = []
        self.idx = self['menu_Plutotv_Second'].getSelectionIndex()
        namet = self.Nety_txt(self['menu_Plutotv_Second'].getCurrent()[0][0])
        if namet=='Not Found':
            self.session.open(MessageBox, 'Mafihache hihi\n Change Your Proxy', MessageBox.TYPE_INFO)
            return
        elif self.imports and not self.secondlist:
            self.listsuprm = ['mtv','music','clubbing tv']
            self.List_MoviePlayer_1 = []
            MyListDict_ =  self.Mydict['regions'][self.proxyvalue]['channels']
            i = 1
            for items in MyListDict_:
                group = MyListDict_[items]['group'].encode('utf-8')
                name = MyListDict_[items]['name'].encode('utf-8')
                programs = MyListDict_[items]['programs']
                url = MyListDict_[items]['url']
                chno = MyListDict_[items]['chno']
                logo = MyListDict_[items]['logo']
                url_alt = MyListDict_[items]['url_alt']
                if name.lower() in Lis_Clean:continue
                self.Chouf.append(show_menu_list_secondpluto(str(i)+'. '+name,url,url_alt,logo,group,programs,chno,items))
                if self.samsungtv=='without':Link_stream=url_alt
                else:Link_stream=url
                self.List_MoviePlayer_1.append(('',name,name +' .......','',Link_stream,'','',logo,'',''))
                i = i + 1
            self['menu_list_catego'].l.setList(self.Chouf)
            self['menu_list_catego'].l.setItemHeight(37)
            self['menu_list_catego'].show()
            self['menu_list_catego'].selectionEnabled(1)
            self.currentList = 'menu_list_catego'
            self['menu_list_catego'].moveToIndex(0)
            self['menu_Plutotv_Second'].selectionEnabled(0)
            self['menu_Plutotv_Second'].hide()
            self.secondlist = True
            self.Get_Infos_select()
        elif self.imports and self.secondlist:
            self.Play_Videos()
        else:pass
    def Exit_plug(self):
        if self.secondlist:
            self['menu_Plutotv_Second'].show()
            self['menu_Plutotv_Second'].selectionEnabled(1)
            self.currentList = 'menu_Plutotv_Second'
            #######################################
            self['menu_list_catego'].hide()
            self['menu_list_catego'].selectionEnabled(0)
            self.secondlist = False
            self.Get_Infos_select()
        else:self.close()
    def Recovery_indx(self):
        H = '0'
        Milef = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/Cfg/indexfil'
        if os.path.isfile(Milef):
            file_write = open(Milef, 'r')
            data = file_write.readlines()
            file_write.close()
            H = data[0].replace('\n', '').replace('\t', '').replace('\r', '')
            H = H.split('=')[1].replace(' ','')
            Y = data[1].replace('\n', '').replace('\t', '').replace('\r', '')
            Y = Y.split('=')[1].replace(' ','')
        return H,Y
    def show_all_chang(self):
        H,Y =self.Recovery_indx()
        self.samsungtv = config.plugins.SupTVoDNeWConfig.Plutotvsamsung.value
        if str(Y)== 'True':
            try:
                index_=H
                self['menu_list_catego'].moveToIndex(int(index_))
                Copy_Volum('indexfil='+str(H)+'\ndakhla=False','indexfil')
                img = self['menu_list_catego'].getCurrent()[0][3]#.replace('https','http')
                _cond = str(img.split('/')[-2])+'.png'
                self.picfile = config.plugins.SupTVoDNeWConfig.Posters.value+_cond
                if os.path.exists(self.picfile):
                    self.picfile = self.picfile
                    self.decodeImage()
            except Exception as ex:
                print ex
    def Get_Changement(self):
        # for t in range(5):
            # self['Info_'+str(t)].setText('')
        self.picfile = PLUGIN_PATH + '/img/playlist/logoplutotv.png'
        self['Title'].setText('Pluto Tv Second')
        self.Download_Image()
    def keyDown(self):
        self[self.currentList].down()
        self.Get_Infos_select()
    def keyUp(self):
        self[self.currentList].up()
        self.Get_Infos_select()
    def left(self):
        self[self.currentList].pageUp()
        self.Get_Infos_select()
    def right(self):
        self[self.currentList].pageDown()
        self.Get_Infos_select()
    def Settings(self):
        self.session.open(SupTVoDNeW_Config)
    def image_downloaded(self, id):
        self.decodeImage()
    def Download_Image(self):
        self.img,self._cond = '',''
        if self.currentList == 'menu_Plutotv_Second':
            self.img = self['menu_Plutotv_Second'].getCurrent()[0][1]#.replace('https','http')
            self._cond = self.img.split('/')[-1]
            self.picfile = config.plugins.SupTVoDNeWConfig.Posters.value+self._cond
            if fileExists(self.picfile):
                self.decodeImage()
                return
        else:
            self.img = self['menu_list_catego'].getCurrent()[0][3]#.replace('https','http')
            self._cond = self.Nety_txt(self['menu_list_catego'].getCurrent()[0][0])+'.png'#str(self.img.split('/')[-2])+'.png'
            self.picfile = config.plugins.SupTVoDNeWConfig.Posters.value+self._cond
            if fileExists(self.picfile):
                self.decodeImage()
                return
        MesImports().Download_Image(self.img,self['poster'],stirr=self._cond)
        # if img.find('http') == -1:
            # self.picfile = PLUGIN_PATH + '/img/playlist/logoplutotv.png'
            # self.decodeImage()
        # else:
            # self.picfile = config.plugins.SupTVoDNeWConfig.Posters.value+_cond
            
            # try:
                # response = requests.get(img,stream=True,verify=False)
                # with open(self.picfile, 'wb') as out_file:
                    # shutil.copyfileobj(response.raw, out_file)
                # del response
                # self.decodeImage()
            # except:
                # self.picfile = PLUGIN_PATH + '/img/playlist/logoplutotv.png'
                # self.decodeImage()
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
    def Play_Videos(self):
        '''(chan_counter,name,description,piconname,stream_url,playlist_url,category_id,
            img_src,description4playlist_html,ts_stream)'''
        Idx = self['menu_list_catego'].getSelectionIndex()
        name,sid,url,categr,self.Mylistessai = '','','','',[]
        if self.imports and self.secondlist:
            self.session.open(Xtream_Player_New,recorder_sref=None,liste=self.List_MoviePlayer_1,indxto=Idx,Oldservice=self.initialservice,server=0,_type='plutotv')
        else:pass
    def show_hide_menu(self):
        if not self.showhide:
            if self.hidden:
                self.show()
            else:
                self.hide()
            self.hidden = not self.hidden
class Screen_MyPlutoTvNew_Stirr(Screen):
    def __init__(self, session):
        ########################Session_Skin############################
        if dwidth == 1280:
            with open(PATH_SKINS + '/PlutoTv_Stirr_FHD.xml', 'r') as f:
                self.skin = f.read()
                f.close()
        else:
            with open(PATH_SKINS + '/PlutoTv_Stirr_FHD.xml', 'r') as f:
                self.skin = f.read()
                f.close()
        self.session = session
        Screen.__init__(self, session)
        self['actions'] = ActionMap(['DirectionActions','SetupActions','ColorActions'], {'ok': self.ok,
            'cancel': self.Exit_plug,
            'red': self.Exit_plug,
            'yellow': self.Settings,
            'blue': self.show_hide_menu,
            'green': self.ok,
            'up': self.keyUp,
            'down': self.keyDown,
            'left': self.left,
            'right': self.right
            }, -1)
        self.proxyvalue = ''
        self.initialservice = self.session.nav.getCurrentlyPlayingServiceReference()
        self.onShown.append(self.show_all_chang)
        self.Headers = ''
        self.List_MoviePlayer_1 = []
        self['Infos'] = Label()
        self['Title'] = Label()
        self['Infoselect'] = Label()
        self['myproxy'] = Label()
        self['Infodiscript'] = Label()
        self['menu_Plutotv_Stirr'] = m2list([])
        self.Chouf,self.Mylist,self.Mydict = [],[],{}
        self['poster'] = Pixmap()
        self.picload = ePicLoad()
        self.imports = False
        self.secondlist = False
        self.showhide = False
        self.hidden = False
        self.TXT = ''
        self.idx = 0
        self.get_ListIptvFnl()
    def get_ListIptvFnl(self):
        self.Mylist,self.Mydict = [],{}
        a,self.myfinalist,self.List_MoviePlayer_1 =  ImportData().getChannels_Pluto_Stirr()
        if a:
            self.Mylist = self.myfinalist
            self.imports =True
            self.secondlist = True
        else:
            self.Mylist.append(show_Menu_PlutoTv_Stirr('Not Found', 'menu', '','','',''))
        self['menu_Plutotv_Stirr'].show()
        self['menu_Plutotv_Stirr'].l.setList(self.Mylist)
        self['menu_Plutotv_Stirr'].l.setItemHeight(37)
        self.currentList = 'menu_Plutotv_Stirr'
        self['menu_Plutotv_Stirr'].selectionEnabled(1)
        self['menu_Plutotv_Stirr'].moveToIndex(0)
        self['Title'].setText('Pluto Tv Second')
        self.Get_Infos_select()
    def Get_Infos_select(self):
        Hd = self.Nety_txt(self[self.currentList].getCurrent()[0][0])
        self['Infoselect'].setText(Hd)
        self['Title'].setText(self['menu_Plutotv_Stirr'].getCurrent()[0][0])
        self.proxyvalue = self['menu_Plutotv_Stirr'].getCurrent()[0][3]
        Txts = MesImports()._colorize_('Genres=='+str(self.proxyvalue),selcolor='cyan')
        self['myproxy'].setText(Txts)
        self.Download_Image()
    def Nety_txt(self,txt):
        if '.  ' in txt:
            txt = txt.split('.  ')[1]
        return txt
    def Recovery_indx(self):
        H = '0'
        Milef = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/Cfg/indexfil'
        if os.path.isfile(Milef):
            file_write = open(Milef, 'r')
            data = file_write.readlines()
            file_write.close()
            H = data[0].replace('\n', '').replace('\t', '').replace('\r', '')
            H = H.split('=')[1].replace(' ','')
            Y = data[1].replace('\n', '').replace('\t', '').replace('\r', '')
            Y = Y.split('=')[1].replace(' ','')
        return H,Y
    def show_all_chang(self):
        H,Y =self.Recovery_indx()
        if str(Y)== 'True':
            try:
                index_=H
                self['menu_Plutotv_Stirr'].moveToIndex(int(index_))
                Copy_Volum('indexfil='+str(H)+'\ndakhla=False','indexfil')
                img = self.Nety_txt(self['menu_Plutotv_Stirr'].getCurrent()[0][0])
                _cond = img+'.png'
                self.picfile = config.plugins.SupTVoDNeWConfig.Posters.value+_cond
                if os.path.exists(self.picfile):
                    self.picfile = self.picfile
                    self.decodeImage()
            except Exception as ex:
                print ex
    def ok(self):
        self.Play_Videos()
    def Exit_plug(self):
        self.close()
    def keyDown(self):
        self[self.currentList].down()
        self.Get_Infos_select()
    def keyUp(self):
        self[self.currentList].up()
        self.Get_Infos_select()
    def left(self):
        self[self.currentList].pageUp()
        self.Get_Infos_select()
    def right(self):
        self[self.currentList].pageDown()
        self.Get_Infos_select()
    def Settings(self):
        self.session.open(SupTVoDNeW_Config)
    def image_downloaded(self, id):
        self.decodeImage()
    def Download_Image(self):
        img,_cond = '',''
        img = self['menu_Plutotv_Stirr'].getCurrent()[0][2]#.replace('https','http')
        #name = self['menu_Plutotv_Stirr'].getCurrent()[0][0]
        _cond = self.Nety_txt(self['menu_Plutotv_Stirr'].getCurrent()[0][0])+'.png'#img.split('/')[-1]
        self.picfile = config.plugins.SupTVoDNeWConfig.Posters.value+_cond
        if fileExists(self.picfile):
            self.decodeImage()
            return
        MesImports().Download_Image(img,self['poster'],stirr=_cond)
        # if img.find('http') == -1:
            # self.picfile = PLUGIN_PATH + '/img/playlist/stirrlogo.png'
            # self.decodeImage()
        # else:
            # self.picfile = config.plugins.SupTVoDNeWConfig.Posters.value+_cond
            
            # try:
                # response = requests.get(img,stream=True,verify=False)
                # with open(self.picfile, 'wb') as out_file:
                    # shutil.copyfileobj(response.raw, out_file)
                # del response
                # self.decodeImage()
            # except:
                # self.picfile = PLUGIN_PATH + '/img/playlist/stirrlogo.png'
                # self.decodeImage()
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
    def Play_Videos(self):
        '''(chan_counter,name,description,piconname,stream_url,playlist_url,category_id,
            img_src,description4playlist_html,ts_stream)'''
        Idx = self['menu_Plutotv_Stirr'].getSelectionIndex()
        name,sid,url,categr,self.Mylistessai = '','','','',[]
        if self.imports and self.secondlist:
            self.session.open(Xtream_Player_New,recorder_sref=None,liste=self.List_MoviePlayer_1,indxto=Idx,Oldservice=self.initialservice,server=0,_type='plutotv')
        else:pass
    def show_hide_menu(self):
        if not self.showhide:
            if self.hidden:
                self.show()
            else:
                self.hide()
            self.hidden = not self.hidden