#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, cookielib, urllib, urllib2, time

serv_id = '16'
siteUrl = 'pokaz.me'
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
		link = mfind(hp, '<span id="srces1" style="display:none">', '<')
		print getURL(link)#, url)
		print link
		return [link]
		#except:
		#	return []

	def Canals(self):
		print 'nmzzzwer'
		h1=getURL(httpSiteUrl)
		h2=getURL(httpSiteUrl+'/page/2/')
		h3=getURL(httpSiteUrl+'/page/3/')
		h4=getURL(httpSiteUrl+'/page/4/')
		http=h1+h2+h3+h4
		#print http
		L=http.splitlines()
		LL=[]
		for i in L:
			if 'nmzzzwer' in i:
				try:
					print i
					url   = mfind(i,'<a href="','"')
					img   = httpSiteUrl+mfind(i,' src="','"')
					title = mfind(i,'title="','"')
					title = title.strip()
					#title=title.replace('Еда ТВ','ЕДА HD').replace('Смотреть','').replace('онлайн','')
					
					LL.append({'url':url, 'img':img, 'title':title, 'group':''})
				except:
					pass
		
		return LL

#p=PZL()
#print p.Canals()