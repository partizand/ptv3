#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, cookielib, urllib, urllib2, time

serv_id = '02'
siteUrl = 'telehub.org'
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

def ya(url):
			#print url
			if '/kal/' not in url: return [url,]
			hp=getURL(url)
			#print hp
			L=hp.splitlines()
			link=''
			LL=[]
			for i in L:
				if '.m3u8' in i and 'redundant' not in i: 
					#print i
					if '/dvr/' in url:
						pref=url[:url.rfind('/')+1]
						link=pref+i
					else:
						link='https://strm.yandex.ru'+i
					#print link
					LL.append(link)
			LL.reverse()
			return LL


class PZL:

	def Streams(self, url):
		url = url.replace('telehub:',httpSiteUrl+'/')+'.html'
		print url
		h=getURL(url)
		#print h
		url2 = 'http://cdn'+mfind(h,'src="http://cdn','"')
		print url2
		h2=getURL(url2)
		stream = mfind(h2,'file:"','"')
		return [stream,]


	def Canals(self):
		h=getURL(httpSiteUrl)
		L=mfindal(h, '<td style="text-align: center; position: relative;">', '"></div></td>')
		LL=[]
		LLL=[]
		for i in L:
				try:
					print i
					url   = 'telehub:'+mfind(i,'<a href="/','.html')
					img   =  httpSiteUrl+mfind(i,'src="','"')
					title =  mfind(i,'title="','"').replace('Смотреть','').replace('смотреть','').replace('онлайн','').replace('прямой эфир','').strip()
					if url not in LLL:
						LLL.append(url)
						LL.append({'url':url, 'img':img, 'title':title, 'group':''})
				except:
					pass
		return LL

#p=PZL()
#print p.Canals()