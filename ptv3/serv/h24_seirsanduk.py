#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, cookielib, urllib, urllib2, time
import settings

#-----------------------------------------

serv_id = '24'
siteUrl = 'www.seirsanduk.us'
httpSiteUrl = 'http://' + siteUrl

urllib2.install_opener(urllib2.build_opener()) 

def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return xbmc.translatePath(x)
def fs_enc(path):
    sys_enc = sys.getfilesystemencoding() if sys.getfilesystemencoding() else 'utf-8'
    return path.decode('utf-8').encode(sys_enc)

def fs_dec(path):
    sys_enc = sys.getfilesystemencoding() if sys.getfilesystemencoding() else 'utf-8'
    return path.decode(sys_enc).encode('utf-8')

def showMessage(heading, message, times = 3000):
	xbmc.executebuiltin('XBMC.Notification("%s", "%s", %s, "%s")'%(heading, message, times, icon))

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

def mfind(t,s,e):
	r=t[t.find(s)+len(s):]
	r2=r[:r.find(e)]
	return r2


class PZL:
	def Streams(self, url):
		h=getURL(url)
		stream = mfind(h,'file:"','"')
		return [stream,]

	def Canals(self):
		LL=[]
		http=getURL(httpSiteUrl)
		#debug (http)
		L=http.splitlines()
		for i in L:
			if '<li id=' in i:
				try:
					url=mfind(i,'<a href="','"')
					#print url
					img = httpSiteUrl+"/"+mfind(i,'<img src="','"')
					title=mfind(i,'"/>', '<')
					#print title
					LL.append({'url':url, 'img':img, 'title':title})
				except:
					pass
				
		return LL
