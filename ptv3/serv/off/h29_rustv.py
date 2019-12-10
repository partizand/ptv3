#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, cookielib, urllib, urllib2, time

serv_id = '29'
siteUrl = 'www.rustv-player.ru'
httpSiteUrl = 'http://' + siteUrl

def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return xbmc.translatePath(x)


def getURL(url, Referer = httpSiteUrl):
	urllib2.install_opener(urllib2.build_opener()) 
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Opera/10.60 (X11; openSUSE 11.3/Linux i686; U; ru) Presto/2.6.30 Version/10.60')
	#req.add_header('User-Agent', 'DuneHD/1.0.3')
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

class PZL:

	def Streams(self, url):
		CID = url.replace('rustv:','')
		h=getURL('https://www.rustv-player.ru/tv/'+CID+'.php')
		stream = mfind(h,'file: "','"')
		return [stream,]

	def Canals(self):
		print 'rustv'
		h1=getURL('https://www.rustv-player.ru/tv/js/massiv-jtv.js')
		h2=getURL('https://www.rustv-player.ru/0/go/pl.xml')
		L1 = h1.splitlines()
		L2 = mfindal(h2, '<ch>', '</ch>')
		
		LL=[]
		for i in L1:
			if 'url[' in i:
				try:
					n     = int(mfind(i,'url[',']'))
					t     = L2[n]
					url   = 'rustv:'+mfind(i,'= "','"')
					img   = 'https://www.rustv-player.ru/tv/images/icon/'+str(n)+'.png'
					title = mfind(t,'<a>','</a>')
					LL.append({'url':url, 'img':img, 'title':title, 'group':''})
				except:
					pass
		return LL

#p=PZL()
#print p.Canals()