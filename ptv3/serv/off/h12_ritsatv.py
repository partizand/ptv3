#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, urllib, urllib2, time#, cookielib
#-----------------------------------------

serv_id = '12'
siteUrl = 'ritsatv.ru'
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
	def Streams(self, url):
			try:
				url=url.replace('ritsatv:', httpSiteUrl+'/iframe/')
				print url
				http=GET(url)
				#print http
				if 'ok.ru' in http: 
					url2=urllib.unquote_plus(mfind(http, 'player=', '",'))
					print url2
					http2=GET(url2)
					link = 'https://vsd'+mfind(http, 'https://vsd', '.m3u8?')+'.m3u8'
				else:
					link = mfind(http, '%3Ffile%3D', '.m3u8')+'.m3u8'
					link = urllib.unquote_plus(link)
				print link
				return [link]
			except:
				return []

	def Canals(self):
		LL=[]
		http=GET(httpSiteUrl+'/genre/TV')
		#print http
		L = mfindal(http,'{"@type":',']}}')
		for i in L:
				try:
					#print i
					url   = 'ritsatv:'+mfind(i, 'movie/id', '-')
					img   = mfind(i, 'image":"', '"')
					title = mfind(i, 'name":"', '"').replace(' ТВ','').strip().capitalize()
					LL.append({'url':url, 'img':img, 'title':title})
				except:
					pass
		
		return LL
