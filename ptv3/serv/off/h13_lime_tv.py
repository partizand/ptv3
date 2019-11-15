#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, cookielib, urllib, urllib2, time

serv_id = '13'
siteUrl = 'lime-tv.ru'
httpSiteUrl = 'http://' + siteUrl

def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return xbmc.translatePath(x)


def getURL(url, Referer = httpSiteUrl):
	urllib2.install_opener(urllib2.build_opener()) 
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

def mfind(t,s,e):
	r=t[t.find(s)+len(s):]
	r2=r[:r.find(e)]
	return r2

class PZL:
	def __init__(self):
		pass

	def Streams(self, url):
		#try:
		hp=getURL(url)
		link = mfind(hp, 'file=', '"')
		return [link]
		#except:
		#	return []

	def Canals(self):
		print ''
		http=getURL(httpSiteUrl)
		ss='<div class="short">'
		es='<div class="short-ya">'
		L=mfindal(http,ss,es)
		LL=[]
		for i in L:
			try:
				url   = mfind(i,'<a href="','"')
				img   = 'http://lime-tv.ru'+mfind(i,'<img src="','"')
				title = mfind(i,'title="','"')
				title = title.replace('Смотреть','').replace('онлайн','').strip()
				#title=title.replace('Еда ТВ','ЕДА HD')
				
				LL.append({'url':url, 'img':img, 'title':title, 'group':''})
			except:
				pass
		
		return LL

#p=PZL()
#print p.Canals()