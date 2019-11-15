#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, urllib, urllib2, time, cookielib
#-----------------------------------------

serv_id = '4'
siteUrl = 'hochu.tv'
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

class PZL:
	def __init__(self):
		pass

	def Streams(self, url, aceproxy='false'):
			try:
				http=getURL(url[9:])
				ss='" src="http'
				es='php"'
				pl='http'+mfindal(http,ss,es)[0][len(ss):]+'php'
				
				http2=getURL(pl)
				ss='file:"'
				es='"});'
				tmp=http2[http2.find(ss)+len(ss):]
				st=tmp[:tmp.find(es)]
				#print st
				return [st,]
			except:
				return []

	def Canals(self):
		LL=[]
		group='Эротика'
		http=getURL(httpSiteUrl)

		ss='<td style="text-align: center;">'
		es='</a></td>'
		L=mfindal(http,ss,es)

		for i in L:
			try:
				ss='href="'
				es='.html'
				url='hochu-tv:'+httpSiteUrl+mfindal(i,ss,es)[0][len(ss):]+es

				ss='title="'
				es='" alt="'
				title=mfindal(i,ss,es)[0][len(ss):]
				try: title=title.encode('utf-8')
				except:pass
				title=title.replace(' смотреть онлайн','').strip()
			
				ss='src="'
				es='" style="'
				img=httpSiteUrl+mfindal(i,ss,es)[0][len(ss):]

				LL.append({'url':url, 'img':img, 'title':title, 'group':group})
			except:
				pass

		return LL
