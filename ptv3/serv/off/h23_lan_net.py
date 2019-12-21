#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, cookielib, urllib, urllib2, time
import settings

#-----------------------------------------

serv_id = '23'
siteUrl = 'iptv.in-lan.net.ua'
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
		return [url.replace('lan_net:','http://streamer.in-lan.net.ua:8080'),]

	def Canals(self):
		LL=[]
		url='http://iptv.in-lan.net.ua/iptv.m3u'
		http=getURL(url)
		http=http.replace(chr(10),"").replace(chr(13),"").replace("#EXTINF:", "\n#EXTINF:").replace("#EXTGRP:", ", GRP:")
		#debug (http)
		L=http.splitlines()
		for i in L:
			t = i[i.rfind(','):]
			if 'http://'  in t: s1='http://'
			if 'https://' in t: s1='https://'
			if 'rtmp://'  in t: s1='rtmp://'
			if 'udp://'   in t: s1='udp://'
			try:
				url='lan_net:'+t[t.find('/ch'):]
				#print url
				if 'GRP:' in i: s1=', GRP:'
				tmp = i[:i.rfind(s1)]
				title=tmp[tmp.rfind(',')+1:].strip()
				#print title
				LL.append({'url':url, 'img':'', 'title':title})
			except:
				pass
				
		return LL
