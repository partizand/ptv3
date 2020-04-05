#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, urllib, urllib2, time
#-----------------------------------------

serv_id = '12'
siteUrl = 'viks.fm'
httpSiteUrl = 'http://' + siteUrl


def ru(x):return unicode(x,'utf8', 'ignore')

def getURL(url, Referer = httpSiteUrl):
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


def save_channels(n, L):
		ns=str(n)
		fp=xbmc.translatePath(os.path.join(addon.getAddonInfo('path'), 'Channels'+ns+'.py'))
		fl = open(fp, "w")
		fl.write('# -*- coding: utf-8 -*-\n')
		fl.write('Channels=[\n')
		for i in L:
			fl.write(repr(i)+',\n')
		fl.write(']\n')
		fl.close()


def decoder(w,i,s,e):
	A1=0
	A2=0
	A3=0
	L1=[]
	L2=[]

	while True:
		if A1<5: L2.append(w[A1])
		elif A1<len(w): L1.append(w[A1])
		A1+=1
		
		if A2<5: L2.append(i[A2])
		elif A2<len(i): L1.append(i[A2])
		A2+=1
		
		if A3<5: L2.append(s[A3])
		elif A3<len(s): L1.append(s[A3])
		A3+=1
		
		if(len(w)+len(i)+len(s)+len(e)==len(L1)+len(L2)+len(e)): break

	B1=''.join(L1)
	B2=''.join(L2)
	A2=0
	A1=0
	L3=[]
	while A1<len(L1):
		C1=-1
		if ord(B2[A2])%2: C1=1
		L3.append(unichr(int(B1[A1:A1+2],36)-C1))
		A2+=1
		if A2>=len(L2):A2=0
		A1+=2
	
	return u''.join(L3)

def decoder2(w,i,s,e):
		s = 0
		st = ''
		while s<len(w):
			st += unichr(int(w[s:s+2],36))
			s += 2
		return st

class PZL:
	def __init__(self):
		pass

	def Streams_off(self, url):
			#try:
					print url
					LL=[]
					http=getURL(url).replace('http:','\nhttp:')
					print http
					L=http.splitlines()
					for i in L:
						if '.m3u8' in i:
							link=''
							if '==' in i: link = i[:i.find('==')+2]
							elif '</' in i: link = i[:i.find('</')]
							#print link
							if link!="": LL.append(link)
					return LL
			#except:
			#	return []


	def Streams(self, url):
		#url='http://viks.tv/358-che-tv.html'
		http=getURL(url)
		r0=http[http.find(';eval(function(w,i,s,e)'):]
		r1=r0[r0.find(".join('');}('"):].replace(".join('');}","")
		r=r1[:r1.find("'));")]+"')"
		#print r
		w,i,s,e=eval(r)
		rez = decoder(w,i,s,e)
		for p in range (0,6):
			#print p
			if "');}('" in rez:
				#print 'in rez'
				r=rez[rez.rfind("('"):-2]
				#print r
				w,i,s,e=eval(r)
				#print 'eval r'
				rez = decoder(w,i,s,e)
				#print rez
			if 'viks' in rez:
				#print 'rez OK'
				L=rez.split(';')
				L2=[]
				for i in L:
					if 'http:' in i : 
						getURL(i[i.find('http:'):-1])
						L2.append(i[i.find('http:'):-1])
					#if 'rtmp:' in i : L2.append(i[i.find('rtmp:'):-1])
				return L2
		return []
		
	
	def Canals(self):
		LL=[]
		url=httpSiteUrl+'/page/'
		http=''
		for p in ['1','2','3']:
			hp=getURL(url+p)
			hp=hp[hp.find('dle-content'):]
			http+=hp
		L=http.splitlines()
		for i in L:
			if '</span></a>' in i:
				try:
					ss='href="'
					es='.html'
					url=mfindal(i,ss,es)[0][len(ss):]+es
					
					ss='src="'
					es='"><span>'
					img='http://viks.tv'+mfindal(i,ss,es)[0][len(ss):]
					
					ss='title="'
					es='"><img'
					title=mfindal(i,ss,es)[0][len(ss):]
					print title
					title=title.replace('1000', 'TV 1000')
					if title=='Еда ТВ': title='Еда HD'
					LL.append({'url':url, 'img':img, 'title':title})
				except:
					print 'err item'
		#if LL!=[]:save_channels(serv_id, LL)
		#else:showMessage('viks.tv', 'Не удалось загрузить каналы', times = 3000)
				
		return LL
