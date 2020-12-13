#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, urllib, urllib2, time#, cookielib
#-----------------------------------------

serv_id = '13'
siteUrl = 'standart.tv'
httpSiteUrl = 'http://' + siteUrl

def ru(x):return unicode(x,'utf8', 'ignore')

def GET(url, Referer = httpSiteUrl):
	urllib2.install_opener(urllib2.build_opener())
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36 OPR/72.0.3815.320')
	req.add_header('Accept', 'text/html, application/xml, application/xhtml+xml, */*')
	req.add_header('Accept-Language', 'ru,en;q=0.9')
	#req.add_header('Referer', Referer)
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

def convert(url):
	import base64
	redir='http://prx.afkcz.eu/prx/index.php?q='+urllib.quote_plus(base64.b64encode(url))+'&hl=8'
	return redir

#print GET(convert('http://standart.tv/channel-4-discovery-science'))
#time.sleep(30)

class PZL:
	def Streams(self, url):
			try:
				print url
				http=GET(url)
				#print http
				if 'file: "' not in http: 
					#url = 'http://prx.afkcz.eu/prx/index.php?q='+urllib.quote_plus(url)+'&hl=a1'
					#print url
					http=GET(convert(url))
					#print http
					if 'file: "' not in http:
						print 'no stream'
						return []
				link = mfind(http, 'file: "', '"')
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
		L = mfindal(http,'class="channel-item channel-item-','<div class="channel-item__title">')
		for i in L:
				try:
					print i
					url   = mfind(i, 'href="', '"')
					img   = httpSiteUrl+mfind(i, 'data-lazy="', '"')
					title = mfind(mfind(i, '<div href=', 'div>'),'">','<').strip()
					LL.append({'url':url, 'img':img, 'title':title})
				except:
					pass
		
		return LL
