#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, urllib, urllib2, time#, cookielib
#-----------------------------------------

serv_id = '4'
siteUrl = 'telecdn.net'
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
				id = url.replace('telecdn:','')
				http=getURL('http://telecdn.net/web/web.php')
				
				ss='class="wday"'
				es='width="50" height="50"></span>'
				L=mfindal(http,ss,es)
				
				for i in L:
					if id in i:
						return  [mfind(i, 'file:"', '"'),]
				return []
			except:
				return []

	def Canals(self):
		LL=[]
		url='http://telecdn.net/web/web.php'
		http=getURL(url)
		
		ss='class="wday"'
		es='width="50" height="50"></span>'
		L=mfindal(http,ss,es)
		#print len(L)
		for i in L:
			try:
				#print i
				url   = 'telecdn:'+mfind(i, '/img/', '.png')
				img   = httpSiteUrl+mfind(i, 'src="', '"')
				title = mfind(i, 'title="', '"').strip()
				title=title.replace('Еда ТВ','ЕДА HD')
				LL.append({'url':url, 'img':img, 'title':title})
			except:
				pass
		#if LL!=[]:save_channels(serv_id, LL)
		#else:showMessage('ok-tv.org', 'Не удалось загрузить каналы', times = 3000)
		
		return LL
