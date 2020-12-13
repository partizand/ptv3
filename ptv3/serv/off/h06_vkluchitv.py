#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, urllib2, cookielib
#-----------------------------------------

serv_id = '3'
prov = 'vkluchitv:'
siteUrl = 'vkluchitv15.net'
httpSiteUrl = 'http://' + siteUrl
root_dir = os.path.dirname(os.path.realpath(__file__))
sid_file = os.path.join(root_dir, siteUrl+'.sid')

cj = cookielib.FileCookieJar(sid_file) 
hr  = urllib2.HTTPCookieProcessor(cj) 
opener = urllib2.build_opener(hr) 
urllib2.install_opener(opener) 

def ru(x):return unicode(x,'utf8', 'ignore')

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

class PZL:
	def __init__(self):
		pass

	def Streams(self, url, aceproxy='false'):
			try:
				print url
				cid=url.replace(prov,'')
				http=getURL('http://telecdn.net/web/web.php')
				ss='jwplayer().load([{'
				es='></span>'
				L=mfindal(http,ss,es)
				for i in L:
					link=mfind(i,'file:"', '"}]).play()')
					if cid in link: 
						getURL(link)
						print link
						return [link,]
				return []
			except:
				return []

	def Canals(self):
		LL=[]
		group='ВключиТВ'
		http=getURL('http://telecdn.net/web/web.php')

		ss='jwplayer().load([{'
		es='></span>'
		L=mfindal(http,ss,es)

		for i in L:
			try:
				url=mfind(i,'file:"', '"}]).play()')
				cid = prov+mfind(mfind(url,'://', '.m3u'),'/','/')
				
				title=mfind(i,'" title="','" border="')
				try: title=title.encode('utf-8')
				except:pass
				
				img='http://telecdn.net'+mfind(i,'" src="','" title=')
				
				LL.append({'url':cid, 'img':img, 'title':title, 'group':group})
			except:
				pass

		return LL
