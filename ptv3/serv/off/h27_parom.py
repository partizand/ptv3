#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, cookielib, urllib, urllib2, time

serv_id = '27'
siteUrl = 'parom.tv'
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

class PZL:

	def Streams(self, url):
		CID = url.replace('parom:','')
		h=getURL('http://www.parom.tv/ru/playerdata.json').replace('\\/','/')
		true = True
		false = False
		null = None
		L=eval(h)['channels']
		LL=[]
		for i in L:
				try:
					if CID == str(i['id']): 
						stream = i['hls_uri']
						return [stream,]
				except: pass
		return []

	def Canals(self):
		print 'parom'
		h=getURL('http://www.parom.tv/ru/playerdata.json').replace('\\/','/')
		true = True
		false = False
		null = None
		L=eval(h)['channels']
		LL=[]
		for i in L:
				try:
					#print i
					url   = 'parom:'+str(i['id'])
					img   = ''
					title = i['name']
					LL.append({'url':url, 'img':img, 'title':title, 'group':''})
				except:
					pass
		return LL

#p=PZL()
#print p.Canals()