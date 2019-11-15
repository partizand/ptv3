#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, cookielib, urllib, urllib2, time, socket
import settings
#-----------------------------------------

icon = ""
prov = 'ace'
serv_id = '53'
siteUrl = 'pomoyka.win'
httpSiteUrl = 'http://' + siteUrl
sid_file = os.path.join(os.getcwd(), siteUrl+'.sid')

cj = cookielib.FileCookieJar(sid_file) 
hr  = urllib2.HTTPCookieProcessor(cj) 
opener = urllib2.build_opener(hr)
urllib2.install_opener(opener)

try:
	import xbmcaddon
	addon = xbmcaddon.Addon(id='ptv3')
	root_dir = addon.getAddonInfo('path')
except:
	root_dir = os.getcwd()


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
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.118')
	req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8')
	req.add_header('Accept-Encoding', 'gzip, deflate')
	req.add_header('Host', 'pomoyka.win')
	req.add_header('Referer', Referer)
	response = urllib2.urlopen(req)
	content=response.read()
	if 'gzip' in response.info().getheader('Content-Encoding'):
		sys.path.append(root_dir)
		import gzip
		from StringIO import StringIO
		content = gzip.GzipFile(fileobj=StringIO(content)).read()
	response.close()
	return content

def mfindal(http, ss, es):
	L=[]
	while http.find(es)>0:
		s=http.find(ss)
		e=http.find(es)
		i=http[s:e]
		L.append(i)
		http=http[e+2:]
	return L

def mfind(t,s,e):
	r=t[t.find(s)+len(s):]
	r2=r[:r.find(e)]
	return r2

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
	try:
		sys.path.append(root_dir)
		import pomdb
		D={'data': L, 'time':time.time()}
		pomdb.add(n, D)
	except:
		print 'ERR ADD pom_db'

def get_channels(n):
	try:
		sys.path.append(root_dir)
		import pomdb
		D = pomdb.get_info(n)
		return D
	except:
		return {'data': [], 'time':0}

def get_cnl(s):
		fp=xbmc.translatePath(os.path.join(addon.getAddonInfo('path'), 'Channels'+s+'.py'))
		fl = open(fp, "r")
		t=fl.read()
		fl.close()
		L=eval(mfind(t,'Channels=',']')+']')
		return L

def uptm(s):
		fp=xbmc.translatePath(os.path.join(addon.getAddonInfo('path'), 'Channels'+s+'.py'))
		fl = open(fp, "r")
		t=fl.read()
		fl.close()
		tm=eval(mfind(t,'tm=','.')+'.00')
		if time.time()-tm > 7200: return True
		else:                     return False



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

	def Streams(self, url):
		CID=url.replace('trash-'+prov+':','')
		print CID
		prt = '6878'
		srv=settings.get("p2p_serv")
		if srv=='':srv = '127.0.0.1'
		lnk = 'http://'+srv+':'+prt+'/ace/getstream?id='+CID+"&.mp4"
		lnk = 'acestream://'+CID
		return [lnk,]

	def Canals(self, ul=''):
			ch = get_channels(prov)
			tm = time.time()-ch['time']
			if tm<3600: 
				print '== pom_db =='
				return ch['data']
			
			print 'upd trash.tv - '+prov
			LL=[]
			#url='http://pomoyka.lib.emergate.net/trash/ttv-list/'+n+'.json'
			url='http://pomoyka.win/trash/ttv-list/'+prov+'.json'
			url2='http://91.92.66.82/trash/ttv-list/'+prov+'.json'
			
			http=getURL(url)
			
			
			http=http[:http.find(']}')+2]
			http=http.replace(chr(10),'').replace(chr(13),'').replace('\n','')
			L=eval(http)["channels"]
			
			for i in L:
				try:
					cid=i["url"]
					title=i["name"].replace(" (резерв)","").replace('Резерв 1','').replace('Резерв 2','').replace('Резерв 3','').replace('(16:9)','').replace('(4:3)','').replace('[LQ]','').replace('(allfon)','').replace('(alfabass-tv)','').replace('(PlayList 24)','').replace('(рег)','').replace(' Россия','').replace('  ',' ').strip()
					url='trash-'+prov+":"+cid
					gr=ru_gr(upper(i["cat"]))
					LL.append({'url':url, 'img':'', 'title':title, 'group':gr})
				except: pass
			
			
			if LL!=[]: save_channels(prov, LL)
			#else:showMessage('trash.tv', 'Не удалось загрузить trash.tv -'+prov, times = 3000)
			
			return LL


#p=PZL()
#print p.Canals()
