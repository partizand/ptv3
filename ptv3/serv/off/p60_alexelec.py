#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import base64
import settings
#-----------------------------------------

prov = 'alexelec'
serv_id = '60'
siteUrl = 'playlist.alexelec.in.ua'
httpSiteUrl = 'http://' + siteUrl

def getURL(url, Referer = httpSiteUrl):
	username = settings.get("ae_login")
	password = settings.get("ae_password")
	if username == '': username = 'test'
	if password == '': password = 'test'
	req = urllib2.Request(url)
	base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
	req.add_header('User-Agent', 'AlexELEC (Linux)')
	req.add_header('Accept', 'text/html, application/xml, application/xhtml+xml, */*')
	req.add_header('Accept-Language', 'ru,en;q=0.9')
	req.add_header('Referer', Referer)
	req.add_header("Authorization", "Basic %s" % base64string)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def ru_gr(t):
	gr=t
	if 'erotic_18_plus'		in t : gr='ЭРОТИКА'
	if 'sport'				in t : gr='СПОРТ'
	if 'movies'				in t : gr='ФИЛЬМЫ'
	if 'series'				in t : gr='ФИЛЬМЫ'
	if 'informational'		in t : gr='НОВОСТНЫЕ'
	if 'Новостные'			in t : gr='НОВОСТНЫЕ'
	if 'music'				in t : gr='МУЗЫКА'
	if 'educational'		in t : gr='ПОЗНАВАТЕЛЬНЫЕ'
	if 'documentaries'		in t : gr='ПОЗНАВАТЕЛЬНЫЕ'
	if 'kids'				in t : gr='ДЕТСКИЕ'
	if 'regional'			in t : gr='РЕГИОНАЛЬНЫЕ'
	if 'religion'			in t : gr='РЕЛИГИОЗНЫЕ'
	if 'entertaining'		in t : gr='ОБЩИЕ'
	if 'webcam'				in t : gr='Другие'
	if 'tv'					in t : gr='Другие'
	if 'NotSet'				in t : gr='Другие'
	if 'Allfon'				in t : gr='Другие'
	return gr

class PZL:
	def __init__(self):
		pass

	def Streams(self, url):
		lnk=url.replace(prov+':','acestream://')
		print lnk
		return [lnk,]

	def Canals(self, ul=''):
			LL = []
			url = httpSiteUrl+'/channels/'
			try: http = getURL(url)
			except: return LL
			L = http.splitlines()

			for cnLine in L:
				try:
					title, group, ihash = cnLine.split("#")
					title = title.strip()
					group = group.strip()
					ihash = ihash.strip()
					gr = ru_gr(group)
					url = prov+':'+ihash
					LL.append({'url':url, 'img':'', 'title':title, 'group':gr})
				except: pass

			return LL
