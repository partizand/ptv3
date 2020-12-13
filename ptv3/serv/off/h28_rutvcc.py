#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, urllib, urllib2, time#, cookielib
#-----------------------------------------

serv_id = '13'
siteUrl = 'rutv.cc'
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
				print url
				http=GET(url.replace('rutvcc:', 'http://rutv.cc/'))
				#print http
				if 'file:"' not in http: 
					print 'no stream'
					return []
				link = mfind(http, 'file:"', '"')
				if ']' in link: link=link[link.find(']')+1:]
				print link
				return [link]
			except:
				return []

	def Canals(self):
		LL=[]
		#print 'tvua.biz'
		#http=''
		#for n in range(10):
		http=GET(httpSiteUrl)#+'/1-channels?sort=views_count&direction=desc&page='+str(n+1))
		#print http
		#L = mfindal(http,'<div class="channel-block">','<div class="channel-info__right">')
		L = mfindal(http,'<li>','</li>')
		for i in L:
				try:
					print i
					url   = 'rutvcc:'+mfind(i, 'href="', '"')
					img   = httpSiteUrl+'/'+mfind(i, 'image: url(', ')')
					title = mfind(i, '<h3>','<').strip()
					LL.append({'url':url, 'img':img, 'title':title})
				except:
					pass
		
		return LL
