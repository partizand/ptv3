#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2, time
#-----------------------------------------

serv_id = '5'
siteUrl = 'ontivi.net'
httpSiteUrl = 'http://' + siteUrl

def GET(url, Referer = httpSiteUrl):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0')
	req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
	req.add_header('Accept-Language', 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3')
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

def decoder(h):
	import base64#'//REREREREln', 
	L = ['#2', '//RERERERE', '//RERERER', '//VFRUVFRUE', '//VFRUVFRU', '//NTU1U1NT', '//UlJSUlJS', '//RlZGVkZW']
	h = h.replace('//NTU1//', '//')
	h = h.replace('//UlJS//', '//')
	h = h.replace('//RERE//', '//')
	h = h.replace('//VFRU//', '//')
	h = h.replace('//RlZG//', '//')
	
	h = h.replace('//NTU1U//', '//')
	h = h.replace('//UlJSU//', '//')
	h = h.replace('//RERER//', '//')
	h = h.replace('//VFRUV//', '//')
	h = h.replace('//RlZGV//', '//')
	
	#h = h.replace('////', '//')
	for i in L:
		h = h.replace(i, '')
	print '-'
	print h
	print '-'
	r = base64.b64decode(h)
	return r


def get_stream(url):
		try:
			http=GET(url)#[7:]
			if "silka:" in http: return mfind(http, "{silka:'", "'")
			pl=httpSiteUrl+'/open?kes='+mfind(http,"{kes:'","'")
			print pl
			http2=GET(pl)
			tmp=mfind(http2,'file : "','"')
			print tmp
			st=decoder(tmp)
			print st
			print st.rfind('=')
			if st.rfind('=')==51 or st.rfind('=')==50: return st
			else: return ''
		except:
			return ''


class PZL:
	def __init__(self):
		pass

	def Streams(self, url):
			for i in range(3):
				st=get_stream(url)
				if st!='': 
					print GET(st)
					return [st,]
			return []

	def Canals(self):
		http=GET(httpSiteUrl+'/chanel?catidd=0')
		
		LL=[]
		ss='<li data-id'
		es='class="k_kon">'
		L=mfindal(http,ss,es)
		
		for i in L:
			try:
				url   = httpSiteUrl+mfind(i,'href="','"')
				title = mfind(i,'name">','<')
				try: title=title.encode('utf-8')
				except:pass
				tmp = GET(url)
				if "silka:" in tmp or "{kes:" in tmp:
					print url
					LL.append({'url':url, 'img':'', 'title':title})
			except:
				pass
		#print LL
		return LL

#p=PZL()
#p.Canals()
#print p.Streams('00000000http://oxax.tv/fap-tv-2.html')
#time.sleep(30)