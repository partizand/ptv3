#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, urllib2, json
#-----------------------------------------

serv_id = '9'
prov = 'ipnet'
siteUrl = 'ipnet.ua'
httpSiteUrl = 'http://' + siteUrl

def getURL(url, Referer = httpSiteUrl):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.118')
	req.add_header('Accept', 'text/html, application/xml, application/xhtml+xml, */*')
	req.add_header('Accept-Language', 'ru,en;q=0.9')
	req.add_header('Referer', Referer)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

class PZL:
	def __init__(self):
		pass

	def Streams(self, url, aceproxy='false'):
		lnk=url.replace('ipnet:','')
		#print lnk
		return [lnk,]

	def Canals(self, ul=''):
			LL=[]
			url='http://api.tv.ipnet.ua/api/v2/site/channels'
			http=getURL(url)
			L=json.loads(http)['data']['categories'][0]['channels']

			for i in L:
				try: title=i['name'].encode('utf-8')
				except: pass
				url='ipnet:'+i['url']
				LL.append({'url':url, 'img':'', 'title':title, 'group':''})

			return LL
