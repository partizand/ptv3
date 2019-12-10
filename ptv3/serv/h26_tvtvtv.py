#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, cookielib, urllib, urllib2, time

serv_id = '26'
siteUrl = 'tvtvtv.ru'
httpSiteUrl = 'http://' + siteUrl

def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return xbmc.translatePath(x)


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

def html5(data):
	import base64
	bu = mfind(data,'player_html5("','"')
	url= base64.b64decode(bu)
	if 'm3u' not in url: url= base64.b64decode(url)
	return url

def player_flash(data):
	import base64
	bu = mfind(mfind(data,'player_flash("',')'),'", "','"')
	print bu
	url= base64.b64decode(bu)
	if 'm3u' not in url: url= base64.b64decode(url)
	return url.replace('file=','').replace('&auto=play','')

def flash(data):
	return mfind(data,'file=','"')

class PZL:

	def Streams(self, url):
		url = url.replace('tvtvtv:',httpSiteUrl+'/popup.php?ch=')
		h=getURL(url)
		#print h
		if 'frontend.vh.yandex.ru' in h:
			url2 = mfind(h,'20px;" src="','"')
			h2=getURL(url2)
			url3 = mfind(h2,'content_url" content="','"')
			return ya(url3)
		elif 'player_html5' in h: stream = html5(h)
		elif 'player_flash' in h: stream = player_flash(h)
		elif 'flashvars' in h: stream = flash(h)
		#stream = url#mfind(h,'file:"','"')
		
		return [stream,]


	def Canals(self):
		LL=[]
		for p in range(20):
			print p
			h=getURL(httpSiteUrl+'/index.php?co=60&pg='+str(p))
			h=mfind(h,'<div id="panel_7" style="display:block;">','</table><table')
			
			L=mfindal(h, 'class="tb_title">', '></td></tr>')
			
			for i in L:
					try:
						print i
						if 'HTML5 Player' in i or 'Flash Player' in i:
							url   = 'tvtvtv:'+mfind(i,'php?ch=','"')
							img   =  httpSiteUrl+'/'+mfind(i,'<img src="','"')
							title =  mfind(i,'<b>','</b>').strip()
							LL.append({'url':url, 'img':img, 'title':title, 'group':''})
					except:
						pass
		return LL

#p=PZL()
#print p.Canals()