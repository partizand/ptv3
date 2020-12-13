#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2, time
#-----------------------------------------

serv_id = '5'
siteUrl = 'ontivi.net'
httpSiteUrl = 'http://' + siteUrl

def GET(url, Referer = httpSiteUrl):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36 OPR/72.0.3815.320')
	req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9')
	req.add_header('Accept-Language', 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7')
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

def decoder_old(h):
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

def decoder(h):
		import base64
		while len(h) != 144:
			for i in ['#2', '//RERERERE', '//VFRUVFRU', '//NTU1U1NT', '//UlJSUlJS', '//RlZGVkZW']:
				h = h.replace(i, '')
		return base64.b64decode(h)


def get_stream_old(url):
		try:
			http=GET(url)#[7:]
			if "silka:" in http: return mfind(http, "{silka:'", "'")
			pl=httpSiteUrl+'/open?kes='+mfind(http,"{kes:'","'")
			#print pl
			http2=GET(pl).replace("'",'"').replace(' ','')
			#print http2
			tmp=mfind(http2,'file:"','"')
			#print tmp
			st=decoder(tmp)
			#print st
			#print st.rfind('=')
			if st.rfind('=')==51 or st.rfind('=')==50: return st
			else: return ''
		except:
			return ''

def get_stream(url):
			#print 'get_stream'
			http=GET(url)
			#print '1'
			if "silka:" in http: return mfind(http, "{silka:'", "'")
			#print '2'
			pl=httpSiteUrl+'/open?kes='+mfind(http,"{kes:'","'")
			#print 'pl'
			http2=GET(pl).replace("'",'"').replace(' ','')
			tmp=mfind(http2,'file:"','"')
			#print tmp
			if '#2' in tmp or '//R' in tmp or '//V' in tmp: st=decoder(tmp)
			else: st=tmp
			return st


class PZL:
	def Streams(self, url):
				st=get_stream(url)
				print st
				print GET(st)
				return [st,]

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
#print p.Streams('http://ontivi.net/ictvtv.html')
#time.sleep(30)