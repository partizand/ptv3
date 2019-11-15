#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, cookielib, urllib, urllib2, time
#-----------------------------------------

serv_id = '15'
siteUrl = 'strm.yandex.ru'
httpSiteUrl = 'http://' + siteUrl
sid_file = os.path.join(os.getcwd(), siteUrl+'.sid')

cj = cookielib.FileCookieJar(sid_file) 
hr  = urllib2.HTTPCookieProcessor(cj) 
opener = urllib2.build_opener(hr) 
urllib2.install_opener(opener) 

def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return xbmc.translatePath(x)


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
			if '/kal/' not in url: return [url,]
			hp=getURL(url)
			print hp
			L=hp.splitlines()
			link=''
			LL=[]
			for i in L:
				if '.m3u8' in i and 'redundant' not in i: 
					#print i
					if '/dvr/' in url:
						pref=url[:url.rfind('/')+1]
						link=pref+i
					else:
						link='https://strm.yandex.ru'+i
					#print link
					LL.append(link)
			LL.reverse()
			return LL
		except:
			return []

	def Canals(self):
		url='https://www.yandex.ru/portal/tvstream_json/channels?locale=ru&from=morda'#&_=1511244624627
		hp=getURL(url).replace('\\"','')
		
		null=''
		true=True
		false=False
		print '--1--'
		L=eval(hp)['set']
		print '--2--'
		LL=[]
		for i in L:
			try:
				title = i["title"]
				url=i["content_url"]
				try:img='http:'+i["logo"]
				except: img='null'
				if 'null' in img: 
					try:    img='http:'+i["thumbnail"]
					except: img='null'
				if 'null' in img: img=''
				if '1tv' not in url and '/kal/' in url: LL.append({'url':url, 'img':img, 'title':title, 'group':""})
			except:
				print i

		#if LL!=[]: save_channels(serv_id, LL)
		#else: showMessage('yandex.ru', 'Не удалось загрузить каналы', times = 3000)

		return LL

