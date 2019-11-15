#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
#-----------------------------------------

serv_id = '7'
siteUrl = 'oxax.tv'
httpSiteUrl = 'http://' + siteUrl

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
				http=getURL(url[8:])
				ss='$.get("pley",{kes:\''
				es='\'},function(data){$('
				pl=httpSiteUrl+'/pley?kes='+mfindal(http,ss,es)[0][len(ss):]

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
		img=''
		http=getURL(httpSiteUrl+'/spisok')

		ss='<div class="tv_sp"'
		es='<span><p style="background-position:'
		L=mfindal(http,ss,es)

		for i in L:
			try:
				ss='href="'
				es='.html'
				url='oxax-tv:'+httpSiteUrl+mfindal(i,ss,es)[0][len(ss):]+es

				ss='title="'
				es='"><a href='
				title=mfindal(i,ss,es)[0][len(ss):]
				try: title=title.encode('utf-8')
				except:pass

				LL.append({'url':url, 'img':img, 'title':title, 'group':group})
			except:
				pass

		return LL
