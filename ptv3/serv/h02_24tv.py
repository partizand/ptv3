#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, urllib, urllib2, time, cookielib, settings
#-----------------------------------------

serv_id = '2'
siteUrl = '24tv.org'
httpSiteUrl = 'https://' + siteUrl

def ru(x):return unicode(x,'utf8', 'ignore')


sid_file = os.path.join(os.getcwd(), siteUrl+'.sid')

cj = cookielib.FileCookieJar(sid_file) 
hr  = urllib2.HTTPCookieProcessor(cj) 
opener = urllib2.build_opener(hr) 

def clean_opener():
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
	urllib2.install_opener(opener)

def GETvpn():
	import httplib
	conn = httplib.HTTPConnection("antizapret.prostovpn.org")
	conn.request("GET", "/proxy.pac", headers={"User-Agent": 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)'})
	r1 = conn.getresponse()
	data = r1.read()
	conn.close()
	return data

def proxy_update():
	try:
		print 'proxy_update'
		#url='https://antizapret.prostovpn.org/proxy.pac'
		pac=GETvpn()#GET(url)
		#print pac
		prx=pac[pac.find('PROXY ')+6:pac.find('; DIRECT')]
		settings.set("proxy_serv", prx)
		settings.set("proxy_time", str(time.time()))
	except: 
		print 'except get proxy'

if settings.get("unlock")!='false':
	try:
		try:pt=float(settings.get("proxy_time"))
		except:pt=0
		print pt
		if time.time()-pt > 36000: proxy_update()
		prx=settings.get("proxy_serv")
		print prx
		if prx.find('http')<0 : prx="http://"+prx
		proxy_support = urllib2.ProxyHandler({"http" : prx})
		opener = urllib2.build_opener(proxy_support, hr)
	except:
		print 'except set proxy'



def getURL(url, Referer = httpSiteUrl):
	urllib2.install_opener(opener)
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Opera/10.60 (X11; openSUSE 11.3/Linux i686; U; ru) Presto/2.6.30 Version/10.60')
	req.add_header('Accept', 'text/html, application/xml, application/xhtml+xml, */*')
	req.add_header('Accept-Language', 'ru,en;q=0.9')
	req.add_header('Referer', Referer)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	#clean_opener()
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
			#try:
				url = url.replace('24tv:', httpSiteUrl+'/')
				print url
				http=getURL(url)
				print http
				url2 = httpSiteUrl+mfind(http,'id="player" src="','"')
				print url2
				http=getURL(url2)
				print http
				link = mfind(http, 'file:"', '"')
				print link
				return [link]
			#except:
			#	return []

	def Canals(self):
		LL=[]
		#print '24tv'
		http=getURL(httpSiteUrl)
		#print http
		L = http.splitlines()
		
		for i in L:
			if '<!--' not in i and 'class="tvlink"' in i:
				try:
					#print i
					url   = '24tv:'+mfind(i, 'href="/', '/')
					img   = httpSiteUrl+mfind(i, 'src="', '"')
					title = mfind(i, '<p>', '<').strip()
					LL.append({'url':url, 'img':img, 'title':title})
				except:
					pass
		
		return LL
