#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, cookielib, urllib, urllib2, time

serv_id = '19'
siteUrl = 'peers.tv'
httpSiteUrl = 'http://' + siteUrl

def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return xbmc.translatePath(x)


def getURL(url, Referer = httpSiteUrl):
	urllib2.install_opener(urllib2.build_opener()) 
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Opera/10.60 (X11; openSUSE 11.3/Linux i686; U; ru) Presto/2.6.30 Version/10.60')
	#req.add_header('User-Agent', 'DuneHD/1.0.3')
	req.add_header('Accept', 'text/html, application/xml, application/xhtml+xml, */*')
	req.add_header('Accept-Language', 'ru,en;q=0.9')
	req.add_header('Referer', Referer)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def test(url):
	try:
		r=getURL(url)
		if '/block/' in r: return False
		#print r
		return True
	except:
		return False

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

m3u = ''
ttm=0
token=''

class PZL:
	def Streams(self, url):
		global m3u, ttm, token
		if token == '' or time.time()-ttm>3600:
			print 'GET TOKEN'
			token=mfind(getURL('https://peers.tv/otvrus/'),"window.AUTH_TOKEN = '","';")
			ttm=time.time()
		tail = '?token='+token#+'&client=81'
		#print token
		
		LL=[]
		CID = url.replace('peers:','')
		try:
			if m3u == '':
				m3u=getURL('https://api.peers.tv/iptv/2/playlist.m3u')
			for i in m3u.splitlines():
				if "/"+CID+"/" in i: 
					if 'variable' in i:
						try:
							m3u2 = getURL(i+tail)
							for j in m3u2.splitlines():
								if '#' not in j: LL.append(i.replace('variable.m3u8',j+tail))
						except:
							LL.append(i+tail)
					else:
							LL.append(i+tail)
			if LL!=[]: return LL
		except: pass
		
		stream1='http://hls.peers.tv/streaming/'+CID+'/16/tvrecw/playlist.m3u8'+tail#+'|User-Agent=DuneHD/1.0.3'
		stream2='http://hls.peers.tv/streaming/'+CID+'/16/variable.m3u8'+tail#+'|User-Agent=DuneHD/1.0.3'
		stream3='http://hls.peers.tv/streaming/'+CID+'/126/tvrecw/playlist.m3u8'+tail#+'|User-Agent=DuneHD/1.0.3'
		stream4='http://hls.peers.tv/streaming/'+CID+'/126/variable.m3u8'+tail#+'|User-Agent=DuneHD/1.0.3'
		
		if test(stream1): return [stream1,]
		if test(stream2): 
			LL=[]
			m3u2 = getURL(stream2+tail)
			for j in m3u2.splitlines():
				if '#' not in j: LL.append(stream2.replace('variable.m3u8',j+tail))
			if LL!=[]: return LL
			#return [stream2,]
		if test(stream3): return [stream3,]
		if test(stream4): return [stream4,]
		
		return []#stream1+'|User-Agent=DuneHD/1.0.3',stream2+'|User-Agent=DuneHD/1.0.3',]

	def Canals(self):
		print '-= peers.tv =-'
		#https://api.peers.tv/registry/2/whereami.json #интересные данные
		m3u=getURL('https://api.peers.tv/iptv/2/playlist.m3u')
		h=getURL('http://api.peers.tv/tvguide/2/channels.json').replace('\\/','/')
		true = True
		false = False
		null = None
		L=eval(h)['channels']
		LL=[]
		for i in L:
				try:
					#print i
					CID=i['alias']
					if 'cam2' not in CID:
						if "/"+CID+"/" in m3u: 
							valid = True
						else:
							valid = false
							streams=['http://hls.peers.tv/streaming/'+CID+'/126/variable.m3u8', 'http://hls.peers.tv/streaming/'+CID+'/16/variable.m3u8', 'http://hls.peers.tv/streaming/'+CID+'/16/tvrecw/playlist.m3u8']
							for s in streams:
								time.sleep(1)
								if test(s): 
									valid = True
									print s
									break
						if valid:
							url   = 'peers:'+i['alias']
							try:    img   = i['logoURL']
							except: img   = ''
							title = i['title']
							print CID
							LL.append({'url':url, 'img':img, 'title':title, 'group':''})
					else:
						break
				except:
					pass
					print 'err'
		return LL

#p=PZL()
#print p.Canals()