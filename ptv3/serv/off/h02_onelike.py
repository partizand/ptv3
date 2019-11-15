#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, cookielib, urllib, urllib2, time

serv_id = '2'
siteUrl = 'onelike.tv'
httpSiteUrl = 'http://' + siteUrl
sid_file = os.path.join(os.getcwd(), siteUrl+'.sid')

cj = cookielib.FileCookieJar(sid_file) 
hr  = urllib2.HTTPCookieProcessor(cj) 
opener = urllib2.build_opener(hr) 
urllib2.install_opener(opener) 

def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return xbmc.translatePath(x)


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


class PZL:
	def __init__(self):
		pass

	def Streams(self, url):
		#print url
		try:
			pl=url.replace('.html', '.php').replace('onelike.tv', 'oneliketv.com')
			#print pl
			
			http2=getURL(pl)
			
			#print http2
			if 'new Playerjs' in http2:
				ss='file:"'
				es='"'
			else:
				ss=";file="
				es='"'
			tmp=http2[http2.find(ss)+len(ss):]
			st=tmp[:tmp.find(es)]
			
			L=[st,]
			return L
		except:
			return []

	def Canals(self):
		print 'поиск каналов'
		tsentralnye   =getURL('http://onelike.tv/tsentralnye.html')
		razvlekatelnye=getURL('http://onelike.tv/razvlekatelnye.html')
		muzhskie      =getURL('http://onelike.tv/muzhskie-kanaly.html')
		sportivnye    =getURL('http://onelike.tv/sportivnye.html')
		film          =getURL('http://onelike.tv/kanaly-filmov-i-serialov.html')
		novostnye     =getURL('http://onelike.tv/novostnye.html')
		zhenskie      =getURL('http://onelike.tv/zhenskie-kanaly.html')
		muzykalnye    =getURL('http://onelike.tv/muzykalnye.html')
		poznavatelnye =getURL('http://onelike.tv/poznavatelnye.html')
		detskie       =getURL('http://onelike.tv/detskie-kanaly.html')
		print 'группы загружены'
		LL=[]
		url='http://onelike.tv'
		http=getURL(url)
		ss='<td style="text-align: center;">'
		es='height="95" /></a></td>'
		L=mfindal(http,ss,es)
		for i in L:
			try:
				ss='<a href="'
				es='.html'
				furl=mfindal(i,ss,es)[0][len(ss):]
				url='http://onelike.tv'+furl+'.html'
				
		
				ss='src="'
				es='.png"'
				img='http://onelike.tv'+mfindal(i,ss,es)[0][len(ss):]+'.png'

				ss='title="'
				es='" width="95"'
				title=mfindal(i,ss,es)[0][len(ss):].replace(' смотреть онлайн','').strip()
				title=title.replace('Еда ТВ','ЕДА HD')
				#print title
				
				gr = ''
				if furl in tsentralnye   : gr='ОБЩИЕ'
				if furl in razvlekatelnye: gr='РАЗВЛЕКАТЕЛЬНЫЕ'
				if furl in muzhskie      : gr='МУЖСКИЕ'
				if furl in sportivnye    : gr='СПОРТ'
				if furl in film          : gr='ФИЛЬМЫ'
				if furl in novostnye     : gr='НОВОСТНЫЕ'
				if furl in zhenskie      : gr='ЖЕНСКИЕ'
				if furl in muzykalnye    : gr='МУЗЫКА'
				if furl in poznavatelnye : gr='ПОЗНАВАТЕЛЬНЫЕ'
				if furl in detskie       : gr='ДЕТСКИЕ'
				
				LL.append({'url':url, 'img':img, 'title':title, 'group':gr})
			except:
				pass
			
		
		return LL

#p=PZL()
#print p.Canals()