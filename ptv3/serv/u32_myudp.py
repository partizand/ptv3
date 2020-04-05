#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, urllib2
import settings
import time
#-----------------------------------------
serv = 'myudp'
prov = settings.get('myudp')
serv_id = '32'

siteUrl = 'proxytv.ru'
httpSiteUrl = 'http://' + siteUrl
sid_file = os.path.join(os.getcwd(), siteUrl+'.sid')

udpxylist = []

try:
	import xbmcaddon
	addon = xbmcaddon.Addon(id='ptv3')
	root_dir = addon.getAddonInfo('path')
except:
	root_dir = os.getcwd()


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


def POST(target, post=None, referer='http://proxytv.ru/index.php/poisk.html'):
	try:
		req = urllib2.Request(url = target, data = post)
		req.add_header('Referer', referer)
		req.add_header('X-Requested-With', 'XMLHttpRequest')
		resp = urllib2.urlopen(req)
		http = resp.read()
		resp.close()
		return http
	except Exception, e:
		return ''


def test(url):
	urllib2.install_opener(urllib2.build_opener())
	try:
		response = urllib2.urlopen(url, timeout=1)
		r=response.getcode()
		data=response.read(128)
		if '404' in repr(data): r='404'
		if 'html' in repr(data): r='404'
		if r=='404': print 'BAD'
		else: print 'GOOD'
		return r
	except:
		print 'BAD'
		return '404'


def get_channels(prov):
	try:
		target='http://proxytv.ru/iptv/php/srch.php'
		post='udpxyaddr=pl%3A+'+prov
		p = POST(target, post)
		p = p.replace('#EXTINF','\n#EXTINF')
		L=[]
		for i in p.splitlines():
			if '#EXTINF' in i:
				t = mfind(i, '<b>', '<')
				title = t[:t.rfind('-')].strip()
				
				cid = mfind(i, '/udp/', '<')
				url=serv+":"+cid
				L.append({'url':url, 'img':'', 'title':title.strip(), 'group':''})
		return {'data': L, 'time':time.time()}
	except:
		return {'data': [], 'time':0}
'''
def save_channels(n, L):
	try:
		sys.path.append(root_dir)
		import uxydb
		D={'data': L, 'time':time.time()}
		uxydb.add(n, D)
	except:
		print 'ERR ADD uxydb'
'''
def get_ux_ip():
			global udpxylist
			import random
			if udpxylist == []: udpxylist = get_all_xy()
			uip = random.choice(udpxylist)
			return uip#+':'+str(port)

def get_all_xy():
	LL=[]
	target='http://proxytv.ru/iptv/php/srch.php'
	post='udpxyaddr=udpxy%3A+'+prov
	p = POST(target, post)
	p = p.replace('</b></div>','\n')
	L=[]
	for i in p.splitlines():
		if '<br>' in i:
			LL = i.split('<br>')
			return LL


class PZL:
	def Streams(self, url):
			print url
			mcast = url.replace(serv+':','')
			udpxy = settings.get(serv+'_'+prov)
			stream = 'http://%s/udp/%s\n' % (udpxy, mcast)
			if test(stream) != '404': 
				return [stream,]
			else:
				#n = len(udpxylist)
				#if n>10: n=10
				for i in range(10): # проверкa альтернативных вариантов
						udpxy = get_ux_ip()
						stream = 'http://%s/udp/%s\n' % (udpxy, mcast)
						print stream
						if test(stream) != '404': 
							settings.set(prov, udpxy)
							return [stream,]
			return []
	
	def Canals(self):
			L = get_channels(prov)['data']
			#update()
			return L