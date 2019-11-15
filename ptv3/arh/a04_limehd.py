#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, cookielib, urllib, urllib2, time
#import settings
#-----------------------------------------

serv_id = '4'
siteUrl = 'limehd.tv'
httpSiteUrl = 'https://' + siteUrl

def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return xbmc.translatePath(x)

def showMessage(heading, message, times = 3000):
	print message


def lower(s):
	try:s=s.decode('utf-8')
	except: pass
	try:s=s.decode('windows-1251')
	except: pass
	s=s.lower().encode('utf-8')
	return s

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

def GET(url, Referer = 'https://m.knigavuhe.ru/'):
	urllib2.install_opener(urllib2.build_opener())
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Opera/10.60 (X11; openSUSE 11.3/Linux i686; U; ru) Presto/2.6.30 Version/10.60')
	req.add_header('Accept', 'text/html, application/xml, application/xhtml+xml, */*')
	req.add_header('Accept-Language', 'ru,en;q=0.9')
	req.add_header('Referer', Referer)
	req.add_header('x-requested-with', 'XMLHttpRequest')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def POST(target, post=None, referer='http://torrentino.net'):
	#print target
	try:
		req = urllib2.Request(url = target, data = post)
		req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)')
		req.add_header('X-Requested-With', 'XMLHttpRequest')
		req.add_header('Content-Type', 'application/x-www-form-urlencoded')
		resp = urllib2.urlopen(req)
		#print resp.info()
		http = resp.read()
		resp.close()
		return http
	except Exception, e:
		print e
		return ''


class ARH:
	def Streams(self, url):
		print url
		return [url]

	def Archive(self, id, t):
		print t
		day=t[2]
		
		hp=GET(httpSiteUrl+"/"+id)
		L=mfindal(hp,'<li class="channel-programm-item"', '<span class="text"')
		LL=[]
		for i in L:
			try:    s_time  = float(mfind(i,'data-begin="','"'))+10800
			except: s_time  = 0
			c_day = time.gmtime(s_time)[2]
			if c_day == day:
				tm      = mfind(i,'data-name="','"')[:5]
				title   = mfind(i,'data-name="','"')[6:]
				uri     = mfind(i,'data-url="','"')
				if uri!='': LL.append({'url':uri, 'title':title, 'time':tm, 's_time':s_time})
		return LL


	def name2id(self):
		hp=GET(httpSiteUrl)
		hp=hp[hp.find('<ul class="inner channels-data">'):]
		L=mfindal(hp,'<li class="channels-item','</li>')
		LL=[]
		for i in L:
			try:
				id    = mfind(i,'href="/','"')
				title = mfind(i,'channel-text">','<')
				LL.append({'title':title, 'id':id})
				print title
			except:
				print i
		
		return LL

#p=ARH()
#print p.name2id()