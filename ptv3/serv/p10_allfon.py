#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, cookielib, urllib, urllib2, time, socket
import settings
#-----------------------------------------

serv_id = '10'
siteUrl = 'allfon-tv.com'
httpSiteUrl = 'http://' + siteUrl
sid_file = os.path.join(os.getcwd(), siteUrl+'.sid')

cj = cookielib.FileCookieJar(sid_file) 
hr  = urllib2.HTTPCookieProcessor(cj) 
opener = urllib2.build_opener(hr) 

def clean_opener():
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
	urllib2.install_opener(opener)

def GETvpn():
	import httplib
	conn = httplib.HTTPConnection("antizapret.prostovpn.org")
	conn.request("GET", "/proxy.pac", headers={"User-Agent": 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)'})
	r1 = conn.getresponse()
	data = r1.read()
	conn.close()
	return data

def proxy_update():
	try:
		print 'proxy_update'
		#url='https://antizapret.prostovpn.org/proxy.pac'
		pac=GETvpn()#GET(url)
		#print pac
		prx=pac[pac.find('PROXY ')+6:pac.find('; DIRECT')]
		settings.set("proxy_serv", prx)
		settings.set("proxy_time", str(time.time()))
	except: 
		print 'except get proxy'

if settings.get("unlock")!='false':
	try:
		try:pt=float(settings.get("proxy_time"))
		except:pt=0
		print pt
		if time.time()-pt > 36000: proxy_update()
		prx=settings.get("proxy_serv")
		print prx
		if prx.find('http')<0 : prx="http://"+prx
		proxy_support = urllib2.ProxyHandler({"http" : prx})
		opener = urllib2.build_opener(proxy_support, hr)
	except:
		print 'except set proxy'



def GET(url, Referer = httpSiteUrl):
	urllib2.install_opener(opener)
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Opera/10.60 (X11; openSUSE 11.3/Linux i686; U; ru) Presto/2.6.30 Version/10.60')
	req.add_header('Accept', 'text/html, application/xml, application/xhtml+xml, */*')
	req.add_header('Accept-Language', 'ru,en;q=0.9')
	req.add_header('Referer', Referer)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link


def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return xbmc.translatePath(x)

def showMessage(heading, message, times = 3000):
	xbmc.executebuiltin('XBMC.Notification("%s", "%s", %s, "%s")'%(heading, message, times, icon))

def unmark(nm):
	for i in range (0,20):
		nm=nm.replace(" #"+str(i),"")
	return nm


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


def getURL(url, Referer = httpSiteUrl):
	urllib2.install_opener(opener)
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

def get_ttv(url):
		http=getURL(url)
		
		prt = '6878'
		srv=settings.get("p2p_serv")
		if srv=='': srv = '127.0.0.1'
		
		ss='acestream://'
		es='"><img class="opacity"'
		try:
				if ss in http:
					CID=mfindal(http,ss,es)[0][len(ss):]
					print CID
					lnk='http://'+srv+':'+prt+'/ace/getstream?id='+CID
					lnk='http://127.0.0.1:8185/acestream/'+CID
					lnk = 'acestream://'+CID
					if len(CID)<30:lnk=''
					return lnk
				else: return ""
		except:
				return ""


def save_channels(ns, L):
		fp=xbmc.translatePath(os.path.join(addon.getAddonInfo('path'), 'Channels'+ns+'.py'))
		fl = open(fp, "w")
		fl.write('# -*- coding: utf-8 -*-\n')
		fl.write('Channels=[\n')
		for i in L:
			fl.write(repr(i)+',\n')
		fl.write(']\n')
		fl.close()




class PZL:
	def __init__(self):
		pass

	def Streams(self, url):
		try:
			print url
			trst=get_ttv(url)
			#settings.set("test", trst)
			if trst=="":return []
			else:return [trst,]
		except:
			return []

	def Canals(self):
		url='http://allfon-tv.com'
		http=getURL(url)
		ss='<figure class="img">'
		es='</figure>'
		L=mfindal(http, ss, es)
		LL=[]
		Lu=[]
		for i in L:
			title = i[i.find('<figcaption>')+12:i.find('</figcaption>')]
			print title
			url   = 'http://allfon-tv.com'+i[i.find('<a href="')+9:i.find('"><img class')]
			img   = 'http://allfon-tv.com'+i[i.find('src="')+5:i.find('" alt=')]
			if url not in Lu:
				LL.append({'url':url, 'img':img, 'title':title})
				Lu.append(url)

		#if LL!=[]: save_channels(serv_id, LL)
		#else: showMessage('torrent-tv.ru', 'Не удалось загрузить каналы', times = 3000)

		return LL

#p=PZL()
#print p.Canals()