#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, cookielib, urllib, urllib2, time

serv_id = '06'
siteUrl = 'tele.smotr.online'
httpSiteUrl = 'http://' + siteUrl

def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return xbmc.translatePath(x)


def getURL(url, Referer = httpSiteUrl, prx=False):
	if prx:
		proxy = 'http://proxy-nossl.antizapret.prostovpn.org:29976'
		proxy_support = urllib2.ProxyHandler({"http" : proxy, "https": proxy})
		opener = urllib2.build_opener(proxy_support)
		urllib2.install_opener(opener)
	else:
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
	if prx: urllib2.install_opener(urllib2.build_opener())
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


def test(url):
		url = url.replace('smotr:',httpSiteUrl+'/')
		h=getURL(url)
		if 'RKN' in h: h=getURL(url, prx=True)
		if '"file":"' in h: return True
		else: return False


class PZL:

	def Streams(self, url):
		url = url.replace('smotr:',httpSiteUrl+'/')
		print url
		h=getURL(url)
		if 'RKN' in h or '.rkn.' in h: h=getURL(url, prx=True)
		#print h
		h=h.replace('.mpd','.m3u8')
		L=mfindal(h,'"file":"', '.m3u8')
		LL=[]
		print L
		for i in L:
			if '/out/u/' not in i: 
				strm = i.replace('"file":"','')+'.m3u8'
				#print getURL(strm)
				LL.append(strm)
		return LL


	def Canals(self):
		h=getURL(httpSiteUrl)
		L=mfindal(h, '<div class="channel">', '%;"></div></div></div>')
		LL=[]
		LLL=[]
		for i in L:
				try:
					#print i
					url   = 'smotr:'+mfind(i,'<a href="/','">')
					if test(url):
						img   =  httpSiteUrl+mfind(i,'src="','"')
						title =  mfind(i,'alt="','"').strip()#.replace('Смотреть','').replace('смотреть','').replace('онлайн','').replace('прямой эфир','')
						print title
						if url not in LLL:
							LLL.append(url)
							LL.append({'url':url, 'img':img, 'title':title, 'group':''})
				except:
					pass
		return LL

#p=PZL()
#p.Canals()
#print p.Streams('http://tele.smotr.online/discovery')
#time.sleep(10)