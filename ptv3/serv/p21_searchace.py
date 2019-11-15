#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, cookielib, urllib, urllib2, time
import settings
#-----------------------------------------

serv_id = '21'
siteUrl = 'search.acestream.net'
httpSiteUrl = 'https://' + siteUrl
sid_file = os.path.join(os.getcwd(), siteUrl+'.sid')

cj = cookielib.FileCookieJar(sid_file) 
hr  = urllib2.HTTPCookieProcessor(cj) 
opener = urllib2.build_opener(hr) 
urllib2.install_opener(opener) 

def fs(s):return s.decode('windows-1251').encode('utf-8')
def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return xbmc.translatePath(x)

def CRC32(buf):
		import binascii
		buf = (binascii.crc32(buf) & 0xFFFFFFFF)
		return str("%08X" % buf)

def showMessage(heading, message, times = 3000):
	xbmc.executebuiltin('XBMC.Notification("%s", "%s", %s, "%s")'%(heading, message, times, icon))

def getURL(url, Referer = httpSiteUrl):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Opera/10.60 (X11; openSUSE 11.3/Linux i686; U; ru) Presto/2.6.30 Version/10.60')
	req.add_header('Accept', 'text/html, application/xml, application/xhtml+xml, */*')
	req.add_header('Accept-Language', 'ru,en;q=0.9')
	req.add_header('Referer', Referer)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def mfindal(http, ss, es):
	L=[]
	while http.find(es)>0:
		s=http.find(ss)
		e=http.find(es)
		i=http[s:e]
		L.append(i)
		http=http[e+2:]
	return L

def lower_old(s):
	try:s=s.decode('utf-8')
	except: pass
	try:s=s.decode('windows-1251')
	except: pass
	s=s.lower().encode('utf-8')
	return s

def lower(t):
	RUS={"А":"а", "Б":"б", "В":"в", "Г":"г", "Д":"д", "Е":"е", "Ё":"ё", "Ж":"ж", "З":"з", "И":"и", "Й":"й", "К":"к", "Л":"л", "М":"м", "Н":"н", "О":"о", "П":"п", "Р":"р", "С":"с", "Т":"т", "У":"у", "Ф":"ф", "Х":"х", "Ц":"ц", "Ч":"ч", "Ш":"ш", "Щ":"щ", "Ъ":"ъ", "Ы":"ы", "Ь":"ь", "Э":"э", "Ю":"ю", "Я":"я"}
	for i in range (65,90):
		t=t.replace(chr(i),chr(i+32))
	for i in RUS.keys():
		t=t.replace(i,RUS[i])
	return t

def upper(t):
	RUS={"А":"а", "Б":"б", "В":"в", "Г":"г", "Д":"д", "Е":"е", "Ё":"ё", "Ж":"ж", "З":"з", "И":"и", "Й":"й", "К":"к", "Л":"л", "М":"м", "Н":"н", "О":"о", "П":"п", "Р":"р", "С":"с", "Т":"т", "У":"у", "Ф":"ф", "Х":"х", "Ц":"ц", "Ч":"ч", "Ш":"ш", "Щ":"щ", "Ъ":"ъ", "Ы":"ы", "Ь":"ь", "Э":"э", "Ю":"ю", "Я":"я"}
	for i in RUS.keys():
		t=t.replace(RUS[i],i)
	for i in range (65,90):
		t=t.replace(chr(i+32),chr(i))
	return t

def get_id(name):
	import xid
	xmlid=xid.xmlid
	name=lower(name).replace(" (+1)","").replace(" (+2)","").replace(" (+3)","").replace(" (+4)","").replace(" (+5)","").replace(" (+6)","").replace(" (+7)","").replace(" (резерв)","").strip()
	try:
		id=xmlid[name].replace("ttv","")
	except: 
		print name
		id=''
	return id

def save_channels(n, L):
		ns=str(n)
		fp=xbmc.translatePath(os.path.join(addon.getAddonInfo('path'), 'Channels'+ns+'.py'))
		fl = open(fp, "w")
		fl.write('# -*- coding: utf-8 -*-\n')
		fl.write('Channels=[\n')
		for i in L:
			fl.write(repr(i)+',\n')
		fl.write(']\n')
		fl.write('tm='+str(time.time())+'\n')
		fl.close()

def ru_gr(t):
	gr=t
	if 'EROTIC'        in t : gr='ЭРОТИКА'
	if 'SPORT'         in t : gr='СПОРТ'
	if 'MOVIES'        in t : gr='ФИЛЬМЫ'
	if 'INFORMATIONAL' in t : gr='НОВОСТНЫЕ'
	if 'Мода'          in t : gr='ЖЕНСКИЕ'
	if 'MUSIC'         in t : gr='МУЗЫКА'
	if 'EDUCATIONAL'   in t : gr='ОБРАЗОВАТЕЛЬНЫЕ'
	if 'ENTERTAINING'  in t : gr='ПОЗНАВАТЕЛЬНЫЕ'
	if 'KIDS'          in t : gr='ДЕТСКИЕ'
	if 'REGIONAL'      in t : gr='РЕГИОНАЛЬНЫЕ'
	return gr

class PZL:
	def __init__(self):
		pass
		#try:
		#	from Channels21 import tm
		#	if time.time()-tm > 7200: self.Canals()
		#except:
		#	pass

	def Streams(self, url):
		srv=settings.get("p2p_serv")
		if srv=='': srv = '127.0.0.1'
		prt = '6878'
		
		CID = url[url.find(':')+1:]
		lnk = 'http://'+srv+':'+prt+'/ace/getstream?infohash='+CID
		lnk = 'acestream://'+CID
		
		return [lnk,]

	def Canals(self, ul=''):
		print 'update search.acestream.net'
		url='https://search.acestream.net/all?api_version=1.0&api_key=test_api_key'
		http=getURL(url)
		#http=http[:http.find(']}')+2]
		http=http.replace(chr(10),'').replace(chr(13),'').replace('\n','')
		L=eval(http)#["channels"]
		LL=[]
		L4=[]
		Dat={}
		D={}
		for i in L:
				cid=i["infohash"]
				try:title=eval('u"'+i["name"]+'"').encode('utf-8')
				except: title=i["name"]
				title=title.replace(" (резерв)","").replace('Резерв 1','').replace('Резерв 2','').replace('Резерв 3','').replace('(16:9)','').replace('(4:3)','').replace('[LQ]','').replace('(allfon)','').replace('(alfabass-tv)','').replace('(PlayList 24)','').replace('(рег)','').replace('  ',' ').strip()#.replace('[','(').replace(']',')')
				print title
				url='searchace:'+cid
				try:gr=upper(eval('u"'+i["categories"][0]+'"').encode('utf-8'))
				except: gr=''
				
				try:av=i["availability"]
				except: av=0
				try:at=i["availability_updated_at"]
				except: at=0
				CRC=CRC32(title)

				if av == 1:
					LL.append({'url':url, 'img':'', 'title':title, 'group':ru_gr(gr)})
		
		return LL





























