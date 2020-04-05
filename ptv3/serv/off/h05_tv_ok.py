#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, urllib, urllib2, time, cookielib
#-----------------------------------------

serv_id = '5'
siteUrl = 'tv-ok.org'#'ok-tv.org'

httpSiteUrl = 'http://' + siteUrl
#sid_file = os.path.join(os.getcwd(), siteUrl+'.sid')

#cj = cookielib.FileCookieJar(sid_file) 
#hr  = urllib2.HTTPCookieProcessor(cj) 
#opener = urllib2.build_opener(hr) 
#urllib2.install_opener(opener) 

def ru(x):return unicode(x,'utf8', 'ignore')


def getURL(url, Referer = httpSiteUrl):
	urllib2.install_opener(urllib2.build_opener())
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Opera/10.60 (X11; openSUSE 11.3/Linux i686; U; ru) Presto/2.6.30 Version/10.60')
	req.add_header('Accept', 'text/html, application/xml, application/xhtml+xml, */*')
	req.add_header('Accept-Language', 'ru,en;q=0.9')
	req.add_header('Referer', Referer)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def mfind(t,s,e):
	r=t[t.find(s)+len(s):]
	r2=r[:r.find(e)]
	return r2

def mfindal(http, ss, es):
	L=[]
	while http.find(es)>0:
		s=http.find(ss)
		e=http.find(es)
		i=http[s:e]
		L.append(i)
		http=http[e+2:]
	return L

def save_channels(n, L):
		ns=str(n)
		fp=xbmc.translatePath(os.path.join(addon.getAddonInfo('path'), 'Channels'+ns+'.py'))
		fl = open(fp, "w")
		fl.write('# -*- coding: utf-8 -*-\n')
		fl.write('Channels=[\n')
		for i in L:
			fl.write(repr(i)+',\n')
		fl.write(']\n')
		fl.close()

class PZL:
	def __init__(self):
		pass

	def Streams(self, url):
			try:
				#print url
				http=getURL(url)
				#print http
				ss='file='
				es='"'
				pl=mfind(http,ss,es)
				#print pl
				return [pl,]
			except:
				return []

	def Canals(self):
		LL=[]
		http=getURL(httpSiteUrl+'/sitemap.html')
		http=http.replace(' class="root"', '')
		ss='<li'
		es='</li>'
		L=mfindal(http,ss,es)
		print len(L)
		for i in L:
			try:
				#print i
				url  = mfind(i, 'href="', '"')
				title= mfind(i, 'html">', '<')
				#try: title=title.decode('windows-1251')
				#except:pass
				try: title=title.encode('utf-8')
				except:pass
				#print title
				#print url
				title=title.replace('смотреть','').replace('Cмотреть','').replace('онлайн','').replace('прямой эфир','').replace('прямо эфир','').replace('прямую трансляцию','').replace('бесплатно','').strip()
				title=title.replace('Еда тв','ЕДА HD')
				title=title.replace('\xd0\xa1\xd0\xbc\xd0\xbe\xd1\x82\xd1\x80\xd0\xb5\xd1\x82\xd1\x8c','').strip()
				
				if 'http' in url: LL.append({'url':url, 'img':'', 'title':title})
			except:
				pass
				print 'err'
		
		return LL
