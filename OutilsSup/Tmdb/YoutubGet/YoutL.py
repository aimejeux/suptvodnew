#!/usr/bin/python
# -*- coding: utf-8 -*-
########## Coded by mfaraj57 and yassinov ##########
import requests,re,json,zlib,base64
from compat import *
########################################################################
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore',InsecureRequestWarning)
########################################################################
import requests,re,json,time
St = requests.Session()
#########################################################################
YTB_HDR_={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
          'accept-language':'fr-,fr,en-US;q=0.8,en;q=0.6',
          'Accept-Encoding':'gzip, deflate'}
HDR_SEARCH={'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; en-us; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36',
            'x-youtube-page-cl': '347645126',
            'x-youtube-client-version': '2.20201215.05.01',
            'accept-language': 'fr',
            'x-youtube-page-label': 'youtube.mobile.web.client_20201215_05_RC01',
            'x-youtube-client-name': '2',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip'}
hdr={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) QtWebEngine/5.9.9 Chrome/56.0.2924.122 Safari/537.36',
     'Accept': '*/*',
     'Referer':'https://app.strem.io/shell-v4.4/',
     'Accept-Encoding': 'gzip, deflate'}
#########################################################################
def get_youtube_headers():
    data=St.get('https://www.youtube.com',headers=YTB_HDR_,verify=False).content
    regx='interfaceVersion":"(.*?)"'
    try:
        client_version=re.findall(regx,data, re.M|re.I)[0]
    except:pass
    regx='PAGE_CL":(.*?),'
    try:
        page_cl=re.findall(regx,data, re.M|re.I)[0]
    except:pass
    regx='PAGE_BUILD_LABEL":"(.*?)"'
    try:
        page_label=re.findall(regx,data, re.M|re.I)[0]
    except:pass
    regx='countryLocationInfo":{"countryCode":"(.*?)"'
    try:
        #print '----------------------',re.findall(regx,data, re.M|re.I)
        country_code=re.findall(regx,data, re.M|re.I)[0]
    except:
        regx='"countryCode":"(.*?)",'
        try:
            country_code=re.findall(regx,data, re.M|re.I)[0]
        except:pass
    return client_version,page_cl,page_label,country_code
client_version,page_cl,page_label,country_code=get_youtube_headers()
#print "Country Code:",country_code  
SEARCH_Engine_HDR={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
                   'x-youtube-client-version':client_version,
                   'accept-language':str(country_code.lower()),
                   'x-youtube-page-cl':page_cl,
                   'x-youtube-page-label':page_label,
                   'x-youtube-client-name':'1',
                   'Accept-Encoding':'gzip, deflate'}
################################################ HEADERS
################################################
PRIORITY_VIDEO_FORMAT = []
DASHMP4_FORMAT = ['133', '134', '135', '136', '137', '138','160', '212', '264', '266', '298', '299',
		'248', '303', '271', '313', '315', '272', '308']
################################################
def createPriorityFormats():
	global PRIORITY_VIDEO_FORMAT
	video_format = {'38':['38', '266', '264', '138', '313', '315', '272', '308'],  # 4096x3072
			'37':['37', '96', '301', '137', '299', '248', '303', '271'],  # 1920x1080
			'22':['22', '95', '300', '136', '298'],  # 1280x720
			'35':['35', '59', '78', '94', '135', '212'],  # 854x480
			'18':['18', '93', '34', '6', '134'],  # 640x360
			'5':['5', '36', '92', '132', '133'],  # 400x240
			'17':['17', '91', '13', '151', '160']  # 176x144
		}
	for itag in ['17', '5', '18', '35', '22', '37', '38']:
		PRIORITY_VIDEO_FORMAT = video_format[itag] + PRIORITY_VIDEO_FORMAT
		if itag == "37":#config.TSmedia.youtube_vidqual.value:
			break
createPriorityFormats()
################################################
IGNORE_VIDEO_FORMAT = ['43', '44', '45', '46',  # webm
		'82', '83', '84', '85',  # 3D
		'100', '101', '102',  # 3D
		'167', '168', '169',  # webm
		'170', '171', '172',  # webm
		'218', '219',  # webm
		'242', '243', '244', '245', '246', '247',  # webm
		'249', '250', '251',  # webm
		'302'  # webm
	]
################################################
def try_get(src, getter, expected_type=None):
	if not isinstance(getter, (list, tuple)):
		getter = [getter]
	for get in getter:
		try:
			v = get(src)
		except (AttributeError, KeyError, TypeError, IndexError):
			pass
		else:
			if expected_type is None or isinstance(v, expected_type):
				return v
def url_or_none(url):
    if not url or not isinstance(url, compat_str):
        return None
    url = url.strip()
    return url if re.match(r'^(?:[a-zA-Z][\da-zA-Z.+-]*:)?//', url) else None
################################################
def selectVidoeFormats(streaming_formats):
    #print 'stformats',streaming_formats[0]
    formats = []
    url_map_str = []
    url=''
    for fmt in streaming_formats:
        url_map = {'url': None,'format_id': None,'cipher': None,'url_data': None}
        if fmt.get('drmFamilies') or fmt.get('drm_families'):
            continue
        url_map['url'] = url_or_none(fmt.get('url'))
        if not url_map['url']:
            url_map['cipher'] = fmt.get('cipher') or fmt.get('signatureCipher')
            if not url_map['cipher']:
                continue
            url_map['url_data'] = compat_parse_qs(url_map['cipher'])
            url_map['url'] = url_or_none(try_get(url_map['url_data'], lambda x: x['url'][0], compat_str))
            #print "cipher url_map",url_map
            if not url_map['url']:
                continue
        else:
            url_map['url_data'] = compat_parse_qs(compat_urlparse(url_map['url']).query)
        stream_type = try_get(url_map['url_data'], lambda x: x['stream_type'][0])
        # Unsupported FORMAT_STREAM_TYPE_OTF
        #print "stream_type",stream_type
        if stream_type == 3:
            continue
        url_map['format_id'] = fmt.get('itag') or url_map['url_data']['itag'][0]
        if not url_map['format_id']:
            continue
        url_map['format_id'] = compat_str(url_map['format_id'])
        formats.append(url_map)
        #print "formats",len(formats),formats[0]
    # If priority format changed in config, recreate priority list
    if PRIORITY_VIDEO_FORMAT[0] != "37":#config.TSmedia.youtube_vidqual.value:
        createPriorityFormats()
    # Find the best format from our format priority map
    for our_format in PRIORITY_VIDEO_FORMAT:
        #print "our_format",our_format
        for url_map in formats:
            if url_map['format_id'] == our_format:
                url_map_str.append(url_map)
                break
        if url_map_str:
            break
    # If DASH MP4 video add link also on Dash MP4 Audio
    if url_map_str and our_format in DASHMP4_FORMAT:
        for our_format in ['141', '140', '139','258', '265', '325', '328']:
            for url_map in formats:
                if url_map['format_id'] == our_format:
                    url_map_str.append(url_map)
                    break
            if len(url_map_str) > 1:
                break
    # If anything not found, used first in the list if it not in ignore map
    if not url_map_str:
        for url_map in formats:
            if url_map['format_id'] not in IGNORE_VIDEO_FORMAT:
                url_map_str.append(url_map)
                break
    if not url_map_str and formats:
        url_map_str.append(formats[0])
    #print "url_map***",url_map
    for url_map in url_map_str:
        if url:
            url += '&suburi='
        url += url_map['url']
        if url_map['cipher']:
            #print "url_map_cipher",url_map['cipher']
            url=addSigniture(url_map['cipher'])
        #print "final_url",url
        return str(url)
###############################################################################
def Write_Js_2(txt):
    path = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/OutilsSup/Tmdb/NewYout.js'
    with open(path,'w') as chcfg:
        json.dump(txt, chcfg,ensure_ascii=False)
    print "OK"
def getStreams(videoID):
    url='https://www.youtube.com/watch?v=%s&pbj=1'%videoID
    jsdata=St.get(url,headers=SEARCH_Engine_HDR).json()
    Write_Js_2(jsdata)
    #get formats for selected video
    formats=jsdata[2]['playerResponse']['streamingData']['formats']
    video_url=selectVidoeFormats(formats)
    return video_url
#print getStreams('M2qITlNnaxE')
##############################################################################
##############################################################################
def json_request(url,headers,params,method):
    try:
        if method=='POST':
            r = St.post(url, headers=headers,json=params,verify=False)
        else:
            r = St.get(url, headers=headers,verify=False)
    except:
        pass
    return r.json()
def get_videoinfo(video_Id):
    jsdata=json_request('https://www.youtube.com/watch?v='+video_Id+'&pbj=1',SEARCH_Engine_HDR,'','GET')
    jsdata_=jsdata[3]['response']['contents']['twoColumnWatchNextResults']['results']['results']['contents']
    Title        =jsdata_[0]['videoPrimaryInfoRenderer']['title']['runs'][0]['text']
    Release_Date =jsdata_[0]['videoPrimaryInfoRenderer']['dateText']['simpleText']
    Duration     =jsdata[2]['playerResponse']['videoDetails']['lengthSeconds']
    formats=jsdata[2]['playerResponse']['streamingData']['formats']
    video_url=selectVidoeFormats(formats)
    print 'video_url = ',video_url
    for item in jsdata_:
        for dt in item.keys():
            try:
                Views_Count     =item[dt]['viewCount']['videoViewCountRenderer']['shortViewCount']['simpleText'] #Short Format                       
                Likes_Count     =item[dt]['videoActions']['menuRenderer']['topLevelButtons'][0]['toggleButtonRenderer']['defaultText']['simpleText'] #Short Format
                Dislikes_Count  =item[dt]['videoActions']['menuRenderer']['topLevelButtons'][1]['toggleButtonRenderer']['defaultText']['simpleText']
            except KeyError:
                pass
            return video_url,Title,Release_Date,Duration,Views_Count,Likes_Count,Dislikes_Count 
# video_url,Title,Release_Date,Duration,Views_Count,Likes_Count,Dislikes_Count=get_videoinfo('w0HgHet0sxg')
# print "video_url:",video_url
# print "Video Title:",Title
# print "Release Data:",Release_Date
# print "Duration:",Duration
# print "Views Count:",Views_Count
# print "Likes Count:",Likes_Count
# print "DisLikes Count :",Dislikes_Count