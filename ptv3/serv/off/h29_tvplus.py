#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, cookielib, urllib, urllib2, time

serv_id = '29'
siteUrl = 'www.tvplusonline.ru'
httpSiteUrl = 'https://' + siteUrl

def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return xbmc.translatePath(x)


def getURL(url, Referer = httpSiteUrl):
	urllib2.install_opener(urllib2.build_opener()) 
	req = urllib2.Request(url)
	#req.add_header('User-Agent', 'Opera/10.60 (X11; openSUSE 11.3/Linux i686; U; ru) Presto/2.6.30 Version/10.60')
	req.add_header('User-Agent', 'TV+Android/1.1.5.2 (Linux;Android 7.1.1) ExoPlayerLib/2.9.1')
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

def mfind(t,s,e):
	r=t[t.find(s)+len(s):]
	r2=r[:r.find(e)]
	return r2

m3u = ''

class PZL:

	def Streams(self, url):
		global m3u
		CID = url.replace('tvplus:','')
		if m3u == '':
			m3u=getURL('https://www.tvplusonline.ru/getinfov4/tvmobilemax.txt').replace('-x/','-abr/')
		
		for i in m3u.splitlines():
			id, t_url = i.split(',')
			if id == CID:
				#print t_url
				stream1 = 'http://'+getURL('https://www.tvplusonline.ru/getsignedurl.php?url='+t_url.replace('http://',''))
				#print stream1
				m = getURL(stream1)
				for j in m.splitlines():
					if '#' not in j: stream='http://193.124.177.175:8081/'+j
				
				stream=stream.replace('-sound/chunks','/chunks').replace('-x/','-abr/')
				
				#print stream
				return [stream,]#+'|User-Agent=TV+Android/1.1.5.2 (Linux;Android 7.1.1) ExoPlayerLib/2.9.1'
		return []

	def Canals(self):
		h=getURL('https://www.tvplusonline.ru/api2/v1/channels').replace('\\/','/')
		true = True
		false = False
		null = None
		L=eval(h)
		LL=[]
		for i in L:
				try:
					url   = 'tvplus:'+i['name']
					img   = 'https://www.tvplusonline.ru'+i['image_url'][1:]
					title = i['title']
					LL.append({'url':url, 'img':img, 'title':title, 'group':''})
				except:
					pass
		return LL

#p=PZL()
#print p.Canals()