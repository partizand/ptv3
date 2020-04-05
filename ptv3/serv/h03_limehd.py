#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, cookielib, urllib, urllib2, time

serv_id = '3'
siteUrl = 'limehd.tv'
httpSiteUrl = 'https://' + siteUrl

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
	def Streams(self, url):
		print url
		id=url[7:]
		try:
			hp=getURL(httpSiteUrl+'/ajax/get-channels-menu')
			link = mfind(hp, "("+id+", '", "'")
			try:
				pref=link[:link.rfind('/')+1]
				pl=getURL(link)
				L=pl.splitlines()
				LL=[]
				for i in L:
					if '.m3u8' in i: 
						LL.append(pref+i)
				if LL==[]: return [link]
				LL.reverse()
				return LL
			except:
				return [link]
		except:
			return []
	
	def Canals(self):
		hp=getURL(httpSiteUrl+'/ajax/get-channels-menu')
		hp=hp[hp.find('<ul class="inner channels-data">'):]
		L=mfindal(hp,'<li class="channels-item','</li>')
		LL=[]
		for i in L:
			if 'm3u' in i:
				try:
					url   = 'limehd:'+mfind(i,'data-playlist="','"')
					img   = mfind(i,'channel-icon" src="','"')
					title = mfind(i,'channel-text">','<')
					LL.append({'url':url, 'img':img, 'title':title, 'group':''})
				except: pass
		return LL

#p=PZL()
#print p.Canals()