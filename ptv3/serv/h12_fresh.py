#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, cookielib, urllib, urllib2, time

serv_id = '02'
siteUrl = 'tv-fresh.org'
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
		#print url
		h=getURL(url)
		url2 = mfind(h,'scrolling="no" src="','"')
		#print url2
		h2=getURL(url2)
		#print h2
		#stream = mfind(h2,'source: "','"')
		stream = mfind(h2,'file=','"')
		#print '============'
		#print stream
		return [stream,]


	def Canals(self):
		h=''
		for p in range(1,6):
			print p
			h=h+getURL(httpSiteUrl+'/page/'+str(p))
		L=h.splitlines()
		LL=[]
		LLL=[]
		for i in L:
				try:
					if 'dremmkol' in i:
						#print i
						url   =  mfind(i,'href="','"')
						img   =  ''
						title =  mfind(i,'title="','"').replace('Смотреть','').replace('смотреть','').replace('онлайн','').replace('прямой эфир','').strip()
						if url not in LLL:
							LLL.append(url)
							LL.append({'url':url, 'img':img, 'title':title, 'group':''})
				except:
					pass
		return LL

#p=PZL()
#print p.Canals()