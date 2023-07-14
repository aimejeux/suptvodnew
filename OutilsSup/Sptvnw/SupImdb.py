#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests,re,json
########################################################################
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore',InsecureRequestWarning)
########################################################################
import requests,re,json,time
St = requests.Session()
try:
    import htmlentitydefs
    from urllib import quote_plus
    iteritems = lambda d: d.iteritems()
except ImportError as ie:
    from html import entities as htmlentitydefs
    from urllib.parse import quote_plus
    iteritems = lambda d: d.items()
    unichr = chr
def quoteEventName(eventName, safe = '/()' + ''.join(map(chr, range(192, 255)))):
    try:
        text = eventName.decode('utf8').replace(u'\x86', u'').replace(u'\x87', u'').encode('utf8')
    except:
        text = eventName

    return quote_plus(text, safe=safe)
def get_video_tril(url):
    rgx = '''application/x-mpegurl","url":"(.+?)"'''
    data = St.get(url,verify=False).content
    data = data.replace("\\", "")
    mpegurl = re.findall(rgx,data)
    return mpegurl
def get_im_imdb(urlo):
    data1 = St.get(urlo,verify=False).content
    try:
        im = re.findall('primaryImage":\{"id":"(.+?)"',data1)[0]
        im = urlo+'/mediaviewer/'+str(im)+'/?ref_=tt_ov_i'
    except:im = 'nada'
    try:
        triler = re.findall('href="/video/(.+?)ref_=tt_ov_vi" aria-label="Watch \{VideoTitle\}">',data1)[0]
        triler = triler.replace('amp;','')
        triler = 'https://www.imdb.com/video/'+str(triler)+'&ref_=tt_ov_vi'
        linvideo = get_video_tril(triler)
    except:
        triler='nada'
        linvideo = 'nada2'
    return im,triler,linvideo
eventName = 'aladdin'
def _nbsp():
    NBSP = unichr(htmlentitydefs.name2codepoint['nbsp']).encode('utf8')
    return NBSP
def get_Infos_Imdb(eventName):
    url = 'http://imdb.com/find?q=' + quoteEventName(eventName) + '&s=tt&site=aka'
    print url
    data = St.get(url,verify=False)
    #print data
    data = data.content
    data = data.decode('latin-1').encode('utf8')
    if re.search('<title>Find - IMDb</title>', data):
        pos = data.find('<table class="findList">')
        pos2 = data.find('</table>', pos)
        findlist = data[pos:pos2]
        #print findlist
        searchresultmask = re.compile('<tr class="findResult (?:odd|even)">.*?<td class="result_text"> (<a href="/title/(tt\\d{7,7})/.*?"\\s?>(.*?)</a>.*?)</td>', re.DOTALL)
        #print searchresultmask
        searchresults = searchresultmask.finditer(findlist)
        #print searchresults
        htmltags = re.compile('<.*?>', re.DOTALL)
        titlegroup = 1
        resultlist = [ (' '.join(htmltags.sub('', x.group(titlegroup)).replace(NBSP, ' ').split()), x.group(2)) for x in searchresults ]
        i = 0
        for dons in resultlist:
            title = dons[0]
            link = 'https://www.imdb.com/title/'+dons[1]
            Img,Video,linvideo = get_im_imdb(link)
            print i
            print 'title = ',title
            print 'link = ',link
            print 'Img = ',Img
            print 'Video = ',Video
            print 'linvideo = ',linvideo
            print "========================="
            i = i + 1
            if i>=3:break