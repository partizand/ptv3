#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2, time
#-----------------------------------------

serv_id = '7'
siteUrl = 'oxax.tv'
httpSiteUrl = 'http://' + siteUrl

def getURL(url, Referer = httpSiteUrl):
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
	
	h = h.replace('////', '//')
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
			http=getURL(url[8:])
			ss='$.get("pley",{kes:\''
			es='\'},function(data){$('
			pl=httpSiteUrl+'/pley?kes='+mfind(http,ss,es)
			#print pl
			http2=getURL(pl)
			tmp=mfind(http2,'file:"','"')
			print tmp
			st=decoder(tmp)
			print st
			if st.rfind('=')==49: return st
			else: return ''
		except:
			return ''

def get_stream(url):
			http=getURL(url[8:])
			ss='$.get("pley",{kes:\''
			es='\'},function(data){$('
			pl=httpSiteUrl+'/pley?kes='+mfind(http,ss,es)
			http2=getURL(pl)
			tmp=mfind(http2,'file:"','"')
			st=decoder(tmp)
			return st

class PZL:
	def Streams(self, url):
			st=get_stream(url)
			return [st,]

	def Canals(self):
		LL=[]
		group='Эротика'
		img=''
		http=getURL(httpSiteUrl+'/spisok')

		ss='<div class="tv_sp"'
		es='<span><p style="background-position:'
		L=mfindal(http,ss,es)

		for i in L:
			try:
				ss='href="'
				es='.html'
				url='oxax-tv:'+httpSiteUrl+mfindal(i,ss,es)[0][len(ss):]+es

				ss='title="'
				es='"><a href='
				title=mfindal(i,ss,es)[0][len(ss):]
				try: title=title.encode('utf-8')
				except:pass

				LL.append({'url':url, 'img':img, 'title':title, 'group':group})
			except:
				pass

		return LL

#p=PZL()
#print p.Streams('00000000http://oxax.tv/fap-tv-2.html')
#time.sleep(30)