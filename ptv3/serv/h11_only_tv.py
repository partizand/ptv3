#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, cookielib, urllib, urllib2, time
import settings
#-----------------------------------------

serv_id = '11'
siteUrl = 'only-tv.net'
httpSiteUrl = 'http://' + siteUrl

def ru(x):return unicode(x,'utf8', 'ignore')

def showMessage(heading, message, times = 3000):
	print message


def GET():
	import httplib
	conn = httplib.HTTPConnection("only-tv.net")
	conn.request("GET", "/", headers={"User-Agent": 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)'})
	r1 = conn.getresponse()
	data = r1.read()
	conn.close()
	return data


def getURL(url, Referer = httpSiteUrl, noproxy=False):
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
		#print url
		php = 'http://cdnpotok.com/onlytv/'+mfind(url,'.org/','.htm')+'.php'
		#print php
		http2=getURL(php, noproxy=True)
		#print http2
		L1=http2.splitlines()
		for i in L1:
				if 'file:"' in i:
					link = i[i.find('file:"')+6:i.find('"});')]
					return [link,]
		return []

	def Canals(self):
		LL=[]
		url='http://td-soft.narod.ru/list/only.tv'
		http=getURL(url)
		#http = GET()
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
					img='http://only-tv.net'+mfindal(i,ss,es)[0][len(ss):]
					
					ss='title="'
					es='" width='
					title=mfindal(i,ss,es)[0][len(ss):][:-30]
					title=title.replace('Еда ТВ','ЕДА HD')
					if url not in Lu:
						Lu.append(url)
						LL.append({'url':url, 'img':img, 'title':title})
			except:
					print i
				
		return LL

#p=PZL()
#print p.Canals()