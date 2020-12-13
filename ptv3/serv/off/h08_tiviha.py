#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2, time
#-----------------------------------------

serv_id = '8'
siteUrl = 'tiviha.ru'
httpSiteUrl = 'https://' + siteUrl

def GET(url, Referer = httpSiteUrl):
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
	def Streams(self, url):
		http=GET(url)
		if 'file:"' in http: st=mfind(http,'file:"','"')
		else: st=mfind(http,'mpegurl" src="','"')
		return [st,]

	def Canals(self):
		http=GET(httpSiteUrl+'/tivihа')
		LL=[]
		ss='<td class="views-field views-field-field'
		es='class="image-style-thumbnail'
		L=mfindal(http,ss,es)
		for i in L:
			try:
				url   = httpSiteUrl+mfind(i,'href="','"')
				print url
				tmp = GET(url)
				if 'file:"' in tmp or 'mpegurl" src="' in tmp:
					img   = httpSiteUrl+mfind(i,'src="','"')
					title = mfind(i,'title="','"')
					LL.append({'url':url, 'img':img, 'title':title})
			except:
				pass
		#print LL
		return LL

#p=PZL()
#p.Canals()
#print p.Streams('00000000http://oxax.tv/fap-tv-2.html')
#time.sleep(30)