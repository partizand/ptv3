#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, cookielib, urllib, urllib2, time
#-----------------------------------------

serv_id = '9'
prov = 'asd'
siteUrl = 'asd:'
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


def ru(x):return unicode(x,'utf8', 'ignore')
def fs_enc(path):
    sys_enc = sys.getfilesystemencoding() if sys.getfilesystemencoding() else 'utf-8'
    return path.decode('utf-8').encode(sys_enc)

def fs_dec(path):
    sys_enc = sys.getfilesystemencoding() if sys.getfilesystemencoding() else 'utf-8'
    return path.decode(sys_enc).encode('utf-8')

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


def BL(name):
	bl=['iptvzone','spacetv.in', 'myott.tv', 'ott.watch', '.ottv.info', 'suklakakl.ru', '127.0.0.1']#, '91.231.219.145'
	for i in bl:
		if i in name: return False
	return True


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


class PZL:
	def __init__(self):
		pass

	def Streams(self, url):
		return [url[4:],]

	def Canals(self):
		ch = get_channels(prov)
		tm = time.time()-ch['time']
		if tm<3600: 
			print '== pom_db =='
			#return ch['data']
			ret=[]
			for i in ch['data']:
				if BL(i['url'])==True: ret.append(i)
			return ret
		
		LL=[]
		url='http://pomoyka.win/trash/ttv-list/as.direct.m3u'
		http=getURL(url)
		http=http.replace(chr(10),"").replace(chr(13),"").replace("#EXTINF:", "\n#EXTINF:")
		
		L=http.splitlines()
		for i in L:
			if 'http://' in i: s1='http://'
			if 'https://' in i: s1='https://'
			if 'rtmp://' in i: s1='rtmp://'
			try:
				url='asd:'+i[i.find(s1):]
				#print url
				s2=','
				title=mfindal(i,s2,s1)[0][len(s2):]
				#print title
				if BL(url)==False: LL.append({'url':url, 'img':'', 'title':title})
			except:
				pass
		
		if LL!=[]: save_channels(prov, LL)
		return LL

