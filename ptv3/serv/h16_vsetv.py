#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2, time
#-----------------------------------------

serv_id = '16'
siteUrl = 'vsetv.cc'
httpSiteUrl = 'http://' + siteUrl
ttm=0
token=''

def getURL(url, Referer = httpSiteUrl):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0')
	req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
	req.add_header('Accept-Language', 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3')
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


def get_stream(url):
			global ttm, token
			import base64
			http=getURL(url)
			pl=mfind(http,'file:y("','"')
			print pl
			st=base64.b64decode(pl)
			print st
			if 'peers' in st:
				if token == '' or time.time()-ttm>3600:
					token=mfind(getURL('https://peers.tv/otvrus/'),"window.AUTH_TOKEN = '","';")
					ttm=time.time()
				tail = '&token='+token
				st=st+tail
			return st

class PZL:
	def Streams(self, url):
			st=get_stream(url)
			print st
			return [st,]

	def Canals(self):
		LL=[]
		
		http=getURL(httpSiteUrl)
		ss='<div class="chanblock">'
		es='</span></div></div>'
		L=mfindal(http,ss,es)

		for i in L:
			try:
				url=httpSiteUrl+mfind(i,'href="','"')
				get_stream(url)
				img=httpSiteUrl+mfind(i,'<img src="','"')
				title=mfind(i,'alt="','"')
				LL.append({'url':url, 'img':img, 'title':title})
			except:
				pass

		return LL
