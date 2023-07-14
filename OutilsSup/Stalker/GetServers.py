#!/usr/bin/python
# -*- coding: utf-8 -*-
################################### modified by aime_jeux ##################################
#############                           Aout 2021                              #############
############################################################################################
####################################################################Add by aime_jeux
# importer infos free_serveurs
import os
import xml.etree.ElementTree as ET
MyFolderIptv = '/etc/enigma2/SupTvNew/Iptv.xml'
if os.path.isfile(MyFolderIptv):
    MyFolderXml = True
else:
    MyFolderXml = False
def get_InfosOXml_Stalker():
    MyListInfosServersIptv = []
    MyListInfosServersStalker = []
    if MyFolderXml:
        tree = ET.parse(MyFolderIptv)
        for element in tree.iter('iptv'):
            try:
                namehost = element.find('namehost').text
                namehost = namehost.encode('utf-8')
            except:namehost = 'Server Iptv'
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
            MyListInfosServersIptv.append((namehost,url))
        for element in tree.iter('stalker'):
            try:
                namehost = element.find('namehost').text
                namehost = namehost.encode('utf-8')
            except:namehost = 'Server Stalker'
            protocol = element.find('protocol').text
            protocol = protocol.encode('utf-8')
            host = element.find('host').text
            host = host.encode('utf-8')
            try:
                port = element.find('port').text
                port = port.encode('utf-8')
            except:port=''
            macc = element.find('mac').text
            macc = macc.encode('utf-8')
            if port!='':url = str(protocol)+'://'+str(host)+':'+str(port)
            else:url = str(protocol)+'://'+str(host)
            MyListInfosServersStalker.append((namehost,url,macc))
    return MyListInfosServersIptv,MyListInfosServersStalker
###############################################################################