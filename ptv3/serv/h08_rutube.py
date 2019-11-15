#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, urllib, urllib2, time, cookielib
#-----------------------------------------

serv_id = '8'
siteUrl = 'rutube'

httpSiteUrl = 'http://' + siteUrl
sid_file = os.path.join(os.getcwd(), siteUrl+'.sid')

cj = cookielib.FileCookieJar(sid_file) 
hr  = urllib2.HTTPCookieProcessor(cj) 
opener = urllib2.build_opener(hr) 
urllib2.install_opener(opener) 

def ru(x):return unicode(x,'utf8', 'ignore')


def getURL(url, Referer = httpSiteUrl):
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

def get_stream_rutube(rt_id):
	rt_url='https://rutube.ru/api/play/options/'+rt_id+'/?format=json&no_404=true'
	print rt_url
	hp2=getURL(rt_url)
	#print hp2
	true=True
	false=False
	null=None
	json=eval(hp2)
	#print json
	hls=json['live_streams']['hls'][0]['url']
	print hls
	return hls


class PZL:
	def Streams(self, url):
		print url
		id=url.replace('rutube:', '')
		link=get_stream_rutube(id)
		return [link,]

	def Canals(self):
		print '1'
		url='https://rutube.ru/feeds/live/?ref=menu'
		hp=getURL(url)
		print '2'
		L=mfindal(hp, 'video-card video-card_grid', 'video-card__statistics')
		LL=[]
		for i in L:
				print i
				id = mfind(i,'/video/','/')
				title = mfind(i,'title="','"').replace('Прямой эфир канала ','').replace('Прямой эфир ','')
				url = 'rutube:'+id
				LL.append({'url':url, 'title':title, 'img':''})
		
		return LL
