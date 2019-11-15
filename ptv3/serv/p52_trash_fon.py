#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, cookielib, urllib, urllib2, time, socket
import settings
#-----------------------------------------

prov = 'allfon'
serv_id = '52'
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

def GET(url):
	head = mfind(url, '://', '/')
	tail = url[url.find(head)+len(head):]
	import httplib
	conn = httplib.HTTPConnection(head)
	conn.request("GET", tail, headers={"User-Agent": 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)'})
	r1 = conn.getresponse()
	data = r1.read()
	conn.close()
	return data

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
		CID=url.replace('trash-fon:','')
		print CID
		#prt = '6878'
		srv=settings.get("p2p_serv")
		if srv=='': srv = '127.0.0.1'
		lnk = 'http://'+srv+':6878/ace/getstream?id='+CID+"&.mp4"
		lnk = 'http://127.0.0.1:8185/acestream/'+CID
		lnk = 'acestream://'+CID
		return [lnk,]

	def Canals(self, ul=''):
			ch = get_channels(prov)
			tm = time.time()-ch['time']
			if tm<3600: 
				print '== pom_db =='
				return ch['data']
			
			print 'обновление trash.tv - '+prov
			LL=[]
			#url='http://pomoyka.lib.emergate.net/trash/ttv-list/'+n+'.json'
			url='http://pomoyka.win/trash/ttv-list/'+prov+'.json'
			url2='http://91.92.66.82/trash/ttv-list/'+prov+'.json'
			
			#print url
			http=getURL(url)
			#print http
			if '"channels":' not in http: 
				time.sleep(1)
				http=getURL(url2)
			
			http=http[:http.find(']}')+2]
			http=http.replace(chr(10),'').replace(chr(13),'').replace('\n','')
			L=eval(http)["channels"]
			
			for i in L:
				cid=i["url"]
				title=i["name"].replace(" (резерв)","").replace('Резерв 1','').replace('Резерв 2','').replace('Резерв 3','').replace('(16:9)','').replace('(4:3)','').replace('[LQ]','').replace('(allfon)','').replace('(alfabass-tv)','').replace('(PlayList 24)','').replace('(рег)','').replace('  ',' ').strip()
				url='trash-fon:'+cid
				gr=ru_gr(upper(i["cat"]))
				LL.append({'url':url, 'img':'', 'title':title, 'group':gr})
			
			if LL!=[]: save_channels(prov, LL)
			#else:showMessage('trash.tv', 'Не удалось загрузить trash.tv -'+prov, times = 3000)
			return LL

#p=PZL()
#print p.Streams('trash-fon:74458127c30b4b55b1cbeaef8f474b83ef62c88a')


