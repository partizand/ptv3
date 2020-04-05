#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, urllib, urllib2, time, sys#, cookielib
import settings
#-----------------------------------------

serv_id = '14'
siteUrl = 'domatv.net'
httpSiteUrl = 'http://' + siteUrl

try:
	import xbmcaddon
	addon = xbmcaddon.Addon(id='ptv3')
	root_dir = addon.getAddonInfo('path')
except:
	root_dir = os.getcwd()


def ru(x):return unicode(x,'utf8', 'ignore')


def GET(url, Referer = httpSiteUrl):
	urllib2.install_opener(urllib2.build_opener())
	req = urllib2.Request(url)
	#req.add_header('User-Agent', 'Opera/10.60 (X11; openSUSE 11.3/Linux i686; U; ru) Presto/2.6.30 Version/10.60')
	req.add_header('User-Agent', 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36')
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

def save_KEY(n, KEY):
	try:
		sys.path.append(root_dir)
		import pomdb
		D={'data': KEY, 'time':time.time()}
		pomdb.add('dtv/'+n, D)
	except:
		print 'ERR ADD pom_db'

def get_KEY(n):
	try:
		sys.path.append(root_dir)
		import pomdb
		D = pomdb.get_info('dtv/'+n)
		return D
	except:
		return {'data': '', 'time':0}

def save_CID(n, KEY):
	try:
		sys.path.append(root_dir)
		import pomdb
		D={'data': KEY, 'time':time.time()}
		pomdb.add('dtc/'+n, D)
	except:
		print 'ERR ADD pom_db'

def get_CID(n):
	try:
		sys.path.append(root_dir)
		import pomdb
		D = pomdb.get_info('dtc/'+n)
		return D
	except:
		return {'data': '', 'time':0}


def decoder(d, rev=False):
	import base64
	for i in range(12):
		try:
			if rev: 
				r = base64.b64decode(d[:-i])
				if 'v3}' in r or 'Sign' in r or '/ind' in r: return r
				#return base64.b64decode(d[:-i])
			else:   
				r = base64.b64decode(d[i:])
				if 'v3}' in r or 'Sign' in r or '/ind' in r: return r
				#return base64.b64decode(d[i:])
		except: pass
	return ''

def parser(url, CID = '', KEY = ''):
	if CID != '' and KEY != '': return {'CID':CID, 'KEY':KEY, 'ERR':False}
	#print 'parser'
	nn = ''
	kk = ''
	for i in range(20):
		h = GET (url)
		t = mfind(h, 'file:"#2', '"')
		n = t[:t.find('//')]
		#print t
		#print n
		dn = decoder(n)
		if len(dn)>len(nn): nn = dn
		
		k = t[t.rfind('//')+2:]
		if '00' in k: k = k[k.rfind('00')+2:]
		dk = decoder(k)
		if len(dk)>len(kk): kk = dk
		#print '==========='
		#print nn
		#print kk
		if 'v3}' in nn and '/ind' in nn: CID = mfind(nn, 'v3}/', '/ind')
		if 'Sign' in kk: KEY = kk[kk.rfind('Sign'):]
		if CID!='' and len(KEY)>56: return {'CID':CID, 'KEY':KEY, 'ERR':False}
		#	d_url = 'http://50.7.172.20:8081/'+CID+'/index.m3u8?wmsAuth'+KEY
		#	print d_url
		#	return d_url
		#	break
		#print '==========='
	#print CID
	#print KEY
	return {'CID':CID, 'KEY':KEY, 'ERR':True}

try:    CD = eval(settings.get('dtv'))
except: CD = {}
DB = {}

class PZL:
	def __init__(self):
		pass
	
	def Streams(self, url):
			#try:
				print url
				CID = ''
				KEY = ''
				udk = True
				ID = mfind(url,'.net/', '.htm')
				
				ch = get_KEY(ID)
				tm = time.time()-ch['time']
				if tm<3600:
					print '== pom_db =='
					KEY = ch['data']
					udk = False
				#if ID in DB.keys(): KEY=DB[ID]
				
				if ID in CD.keys(): CID=CD[ID]
				else: 
					CID=get_CID(ID)['data']
				D=parser(url, CID, KEY)
				if D['ERR']: return []
				CID = D['CID']
				KEY = D['KEY']
				link1 = 'http://50.7.172.20:8081/' +CID+'/index.m3u8?wmsAuth'+KEY
				link2 = 'http://50.7.144.155:8081/'+CID+'/index.m3u8?wmsAuth'+KEY
				#print link1
				
				try:
					try: 
						http = GET(link1, url)
						link = link1
					except:
						http = GET(link2, url)
						link = link2
					#DB[ID] = KEY
					if udk: save_KEY(ID, KEY)
					#save_CID(ID, CID)
					if ID not in CD.keys():
						CD[ID] = CID
						settings.set('dtv', repr(CD))
				except: return []
				return [link,]
			#except:
			#	return []


	def Canals(self):
		LL=[]
		url='http://domatv.net/63-tvc.html'
		http=GET(url)
		
		L=http.splitlines()
		
		for i in L:
			if 'ggtwetwygzzzf' in i:
				try:
					#print i
					url   = mfind(i, 'href="', '"')
					img   = httpSiteUrl+mfind(i, 'src="', '"')
					title = mfind(i, 'alt=""/>', '<').strip()
					title=title.replace('Еда ТВ','ЕДА HD')
					LL.append({'url':url, 'img':img, 'title':title})
				except:
					pass
		
		return LL

#p=PZL()
#print p.Streams('http://domatv.net/217-multimuzyka.html')
#time.sleep(30)