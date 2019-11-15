#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, cookielib, urllib, urllib2, time
import settings
#-----------------------------------------

serv_id = '11'
siteUrl = 'only-tv.org'
httpSiteUrl = 'http://' + siteUrl
sid_file = os.path.join(os.getcwd(), siteUrl+'.sid')

cj = cookielib.FileCookieJar(sid_file) 
hr  = urllib2.HTTPCookieProcessor(cj) 
#opener = urllib2.build_opener(hr) 
#urllib2.install_opener(opener) 

def ru(x):return unicode(x,'utf8', 'ignore')

def showMessage(heading, message, times = 3000):
	print message


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
		try:pt=float(__settings__.getSetting("proxy_time"))
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

#urllib2.install_opener(opener)

def getURL(url, Referer = httpSiteUrl, noproxy=False):
	if noproxy: urllib2.install_opener(urllib2.build_opener(hr))
	else: urllib2.install_opener(opener)
	
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
			#try:
				print url
				http=getURL(url)
				#print http
				Lphp=mfindal(http, 'name="frame" src="', '" scrolling="no"')
				Lout=[]
				for p in Lphp:
					php=p.replace('name="frame" src="', '')
					print php
					if 'cdnpotok' in php:
						#php = http[http.find('name="frame" src="')+18:http.find('" scrolling="no"')]
						#print php
						http2=getURL(php, noproxy=True)
						#print http2
						L1=http2.splitlines()
						for i in L1:
							if 'file:"' in i:
								link = i[i.find('file:"')+6:i.find('"});')]
								Lout.append(link)
								#return [link,]
					'''
					if 'youtvonlinefree' in php:
						#php = http[http.find('name="frame" src="')+18:http.find('" scrolling="no"')]
						print php
						http2=getURL(php)
						print http2
						L1=http2.splitlines()
						for i in L1:
							if 'file:"' in i:
								link = i[i.find('file:"')+6:i.find('"});')]
								Lout.append(link)
								#return [link,]
					'''
				
				if 'suppor1u' in http:
						php = http[http.find('<iframe src="')+13:http.find('" width="680" height="450"')]
						http2=getURL(php, noproxy=True)
						#print http2
						L1=http2.splitlines()
						for i in L1:
							if 'file: ' in i:
								link = i[i.find('file: ')+7:i.find("',")]
								Lout.append(link)
								#return [link,]
				return Lout
					#return []
			#except:
			#	return []

	def Canals(self):
		LL=[]
		url='http://only-tv.org'
		http=getURL(url)
		#print http
		http=http[http.find('<td style="text-align: center;'):]
		ss='<td style="text-align: center;'
		es='</div>'
		L=mfindal(http,ss,es)
		Lu=[]
		for i in L:
			try:
				if 'title=' in i:
					ss='<a href="'
					es='.html'
					url='http://only-tv.org'+mfindal(i,ss,es)[0][len(ss):]+es
					
					ss='src="'
					es='" alt="'
					img='http://only-tv.org'+mfindal(i,ss,es)[0][len(ss):]
					
					ss='title="'
					es='" width='
					title=mfindal(i,ss,es)[0][len(ss):][:-30]
					title=title.replace('Еда ТВ','ЕДА HD')
					if url not in Lu:
						Lu.append(url)
						LL.append({'url':url, 'img':img, 'title':title})
			except:
					print i
		#if LL!=[]:save_channels(serv_id, LL)
		#else:showMessage('only-tv.org', 'Не удалось загрузить каналы', times = 3000)
				
		return LL

#p=PZL()
#print p.Canals()