#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, urllib, urllib2, time#, cookielib
#-----------------------------------------

serv_id = '14'
siteUrl = 'domatv.net'
httpSiteUrl = 'http://' + siteUrl

def ru(x):return unicode(x,'utf8', 'ignore')


def GET(url, Referer = httpSiteUrl):
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
			try:
				print url
				http=GET(url)
				link = mfind(http, 'id="srces" style="display:none">', '<')
				print link
				http=GET(link)
				print http
				return [link,]
			except:
				return []

	def Canals(self):
		LL=[]
		url='http://domatv.net/63-tvc.html'
		http=GET(url)
		
		L=http.splitlines()
		
		for i in L:
			if 'ggtwetwygzzzf' in i:
				try:
					#print i
					url   = mfind(i, 'href="', '"')
					img   = httpSiteUrl+mfind(i, 'src="', '"')
					title = mfind(i, 'alt=""/>', '<').strip()
					title=title.replace('Еда ТВ','ЕДА HD')
					LL.append({'url':url, 'img':img, 'title':title})
				except:
					pass
		
		return LL
