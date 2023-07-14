#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests,re,json,zlib
from base64 import b64encode,b64decode
#!/usr/bin/python
# -*- coding: utf-8 -*-
################################### modified by aime_jeux ##################################
#############                           Aout 2021                              #############
############################################################################################
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore',InsecureRequestWarning)
########################################################################
import requests,re,json,time,hashlib,sys
St = requests.Session()
import datetime
import json
import os
import uuid
import urllib,urllib2
##############################################################################################
import xml.etree.ElementTree as ET
##############################################################################################
global Az
Az ='''    <stalker>
	    <namehost>%s</namehost>
	    <protocol>%s</protocol>
	    <host>%s</host>
	    <port>%s</port>
	    <mac>%s</mac>
    </stalker>
</iptvod>'''
global Za
Za ='''<iptvod>
    <iptv>
	    <namehost>%s</namehost>
	    <protocol>%s</protocol>
	    <host>%s</host>
		<port>%s</port>
		<usr>%s</usr>
		<passw>%s</passw>
    </iptv>'''
class getxml():
    def __init__(self):
        self.a,self.b,self.c = 'iptv','stalker','namehost'
        self._don = ''
        self.namehost,self.protocol,self.protocol,self.host,self.port='','','','',''
        self.mac = ''
        self.usr,self.passw='',''
        self.PATH_Xml = '/etc/enigma2/SupTvNew/Iptv.xml'
        #############################
    def Nety_txt(self,txt):
        txt = txt.split('.  ')[1]
        txt = txt.replace(' [IPTV]','').replace(' [Stalker]','')
        return txt
    def cancelCondition(self):
        pass
    def Delt_Video_xml_File(self,_id,cond):
        self.Tcond = cond
        self._id = _id
        self.name,Messg= '','KO'
        Messg,Titl = '',''
        self._don='iptv' if self.Tcond== 'iptv' else 'stalker'
        if not os.path.exists(self.PATH_Xml):return 'KO','File not found\n'+self.PATH_Xml
        tree = ET.parse(self.PATH_Xml)
        root = tree.getroot()
        for iptv in root.findall(self._don):
            namehost = iptv.find(self.c).text
            if self._id in namehost:
                root.remove(iptv)
                Messg= 'OK'
        if Messg == 'OK':
            tree.write(self.PATH_Xml, encoding="UTF-8")
            message = 'Operation Accomplished Successfully'+'\nHas Been Deleted '+'\n'+self._id
            return 'OK',message.encode('utf-8')
        else:return 'KO','Sorry, The Request Was Not Deleted '
    def Add_Video_xml_File(self,_cond,namehost,protocol,host,port,mac,usr,passw):
        searchExp,replaceExp = '',''
        self.namehost = namehost
        self.protocol = protocol
        self.host = host
        self.port = port
        self.mac = mac
        self.usr = usr
        self.passw = passw
        self._cond = _cond
        Messg,Titl = '',''
        def _replaces_(filePath, text, subs, flags=0 ):
            try:
                with open( filePath, "r+" ) as file:
                    fileContents = file.read()
                    textPattern = re.compile( re.escape( text ), flags )
                    fileContents = textPattern.sub( subs, fileContents )
                    file.seek( 0 )
                    file.truncate()
                    file.write( fileContents )
                return 'OK'
            except:
                return 'KO'
        if self._cond=='stalker':
            searchExp = '</iptvod>'
            replaceExp= Az % (self.namehost,self.protocol,self.host,str(self.port),self.mac)
        else:
            searchExp = '<iptvod>'
            replaceExp= Za % (self.namehost,self.protocol,self.host,str(self.port),str(self.usr),str(self.passw))
        Messg=_replaces_(self.PATH_Xml, searchExp, replaceExp, flags=0 )
        return Messg