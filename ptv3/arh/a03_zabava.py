#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, cookielib, urllib, urllib2, time
import settings
#-----------------------------------------

serv_id = '3'
siteUrl = 'zabava-htlive.cdn.ngenix.net'
httpSiteUrl = 'http://' + siteUrl

try: port = settings.get('port')
except: port = 8185
if port=='': port = 8185

try: ip = settings.get('ip')
except: ip = '127.0.0.1'



def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return xbmc.translatePath(x)

def showMessage(heading, message, times = 3000):
	print message



def lower(s):
	try:s=s.decode('utf-8')
	except: pass
	try:s=s.decode('windows-1251')
	except: pass
	s=s.lower().encode('utf-8')
	return s

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

def test_url(url):
		print 'test'
		try:
			urllib2.install_opener(urllib2.build_opener())
			print url
			response = urllib2.urlopen(url, timeout=3)
			r = response.read(512)
			#print r
			if r=='404': 
				print '404'
				return False
			else:
				print '200'
				return True
		except:
			print '???'
			return False

def GET(url, Referer = ''):
	urllib2.install_opener(urllib2.build_opener())
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Opera/10.60 (X11; openSUSE 11.3/Linux i686; U; ru) Presto/2.6.30 Version/10.60')
	req.add_header('Accept', 'text/html, application/xml, application/xhtml+xml, */*')
	req.add_header('Accept-Language', 'ru,en;q=0.9')
	#req.add_header('Referer', Referer)
	#req.add_header('x-requested-with', 'XMLHttpRequest')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

UserAgent='SmartSDK'
#UserAgent='Opera/10.60 (X11; openSUSE 11.3/Linux i686; U; ru) Presto/2.6.30 Version/10.60'

def streams1(id, head):
	#print '== streams1 =='
	L=[]
	id1, id2 = id.split(":")
	t = eval(id2)#+125
	bd= 459999960/60
	#:
	i=0
	if True:
		#print i
		if i>1: t = t+i*1800
		if i==1:t+=m1*30 
		d = int(t/28800)*28800
		t1= int(t/1800)*1800
		m1 = int((t-t1)/30)
		b = bd*m1
		#r = 2400000-int(2400000/30*m1)
		r = int((459999960-b)/188)
		
		uri1=head+'/'+str(d)+'/'+str(t1)+'.ts/0r2_'+str(b)+'r'+str(r)+'.ts'+'|user-agent='+UserAgent
		#print uri1
		L.append(uri1)
	
	for i in range(6):
		b=b+r*188
		#r=1000000
		r=int((459999960-b)/188)#2400000-int(2400000/30*m2)
		if r>2390000: r=2390000
		if r<120: 
			r = 1000000
			b+=1880000
		
		if b>=459999960:
			b-=459999960
			t1=t1+1800
			#r=1000000
		else:
			pass
			#t1=t1
		m2 = int((t-t1)/30)
		uri2=head+'/'+str(d)+'/'+str(t1)+'.ts/0r2_'+str(b)+'r'+str(r)+'.ts'+'|user-agent='+UserAgent
		
		#print uri2
		L.append(uri2)
	return L

def streams2(id, head):
	L=[]
	id1, id2 = id.split(":")
	t = eval(id2)+512
	bd= 460000000/60
	for i in range(4):
		#print i
		if i>1: t = t+i*1800
		if i==1:t+=m2*60 
		d = int(t/28800)*28800
		#t2= int(t/3600)*3600
		t2= int(t/1800)*1800
		m2 = int((t-t2)/60)
		b2 = bd*m2
		r2 = 2400000-int(2400000/30*m2)
		uri1=head+'/'+str(d)+'/'+str(t2)+'.ts/0r2_'+str(b2)+'r'+str(r2)+'.ts'+'|user-agent=SmartSDK'
		
		L.append(uri1)
	return L


def POST(target, post=None, referer='http://torrentino.net'):
	#print target
	try:
		req = urllib2.Request(url = target, data = post)
		req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)')
		req.add_header('X-Requested-With', 'XMLHttpRequest')
		req.add_header('Content-Type', 'application/x-www-form-urlencoded')
		resp = urllib2.urlopen(req)
		#print resp.info()
		http = resp.read()
		resp.close()
		return http
	except Exception, e:
		print e
		return ''

def convertor(L):
	import base64
	url='http://'+ip+':'+str(port)+'/playlist/make/'+base64.b64encode(repr(L))
	return 'http://'+ip+':'+str(port)+'/restream/'+base64.b64encode(url)

class ARH:
	
	def Streams(self, id):
		id=id[7:]
		id1, id2 = id.split(":")
		#print id1
		#print id2
		url='http://zabava-htlive.cdn.ngenix.net/hls/CH_'+id1+'/variant.m3u8'+'?version=2&hd'
		#print url
		hp=GET(url)
		#print hp
		L=hp.splitlines()
		for i in L:
			if '#' not in i and '2000000' in i:
				#print i
				head = 'http'+mfind(i,'http','/playlist')
				#print head
		Luri1=streams1(id, head)
		return Luri1
		
		#if test_url(Luri1[0].replace('|user-agent=SmartSDK','')): return Luri1
		#Luri2=streams2(id, head)
		#if test_url(Luri2[0].replace('|user-agent=SmartSDK','')): return Luri2
		
		return []
	
	def Streams_off(self, id):
		Lr=[]
		#print id
		id=id[7:]
		id1, id2 = id.split(":")
		#print id1
		#print id2
		
		t = eval(id2)
		#print t
		bd= 460000000/60
		d = int(t/28800)*28800
		t1= int(t/1800)*1800
		t2= int(t/3600)*3600
		m1 = int((t-t1)/30)
		m2 = int((t-t2)/60)
		b1 = bd*m1
		b2 = bd*m2
		r1 = 2400000-(2400000/30*m1)#460000000 - b1
		r2 = 2400000-(2400000/30*m2)#460000000 - b2
		url='http://zabava-htlive.cdn.ngenix.net/hls/CH_'+id1+'/variant.m3u8'
		#print url
		hp=GET(url)
		#print hp
		L=hp.splitlines()
		for i in L:
			if '#' not in i and '2000000' in i:
				#print i
				head = 'http'+mfind(i,'http','/playlist')
				#print head
		uri1=head+'/'+str(d)+'/'+str(t1)+'.ts/0r2_'+str(b1)+'r'+str(r1)+'.ts'#|user-agent=SmartSDK'
		uri2=head+'/'+str(d)+'/'+str(t2)+'.ts/0r2_'+str(b2)+'r'+str(r2)+'.ts'#|user-agent=SmartSDK'
		
		if test_url(uri1): Lr.append(uri1+'|user-agent=SmartSDK')
		if test_url(uri2): Lr.append(uri2+'|user-agent=SmartSDK')
		#print Lr
		return Lr

	def Archive(self, id, t):
		id1, id2 = id.split(":")
		#print t
		dt=time.strftime('%Y-%m-%d', t)
		
		url='https://itv.rt.ru/api/v1/telecasts.json?q%5Bs%5D=beginning%20asc&q%5Bchannel_id_eq%5D='+id1+'&q%5Bbeginning_gt%5D='+dt#2019-06-10
		#print url
		hp=GET(url)#.replace('\\"','')
		#print hp
		null=''
		true=True
		false=False
		json=eval(hp)
		LL=[]
		for i in json['telecasts']:
			try:
				try:s_time  = time.mktime(time.strptime(i['beginning'], '%Y-%m-%dT%H:%M:00Z'))+ 10800
				except: s_time  = 0
				uri     = 'zabava:'+id2+':'+str(s_time)
				tm      = time.strftime('%H:%M', time.gmtime(s_time+ 10800))#i['beginning'][11:16]
				title   = i['name']
				
				if s_time<time.time():
					LL.append({'url':uri, 'title':title, 'time':tm, 's_time':s_time})
				#print uri
			except:
				print i
		return LL
		


	def name2id(self):
		sdp_id = '98771354'#КиноViP OTT
		sdp_id = '81204872'#стартовый
		sdp_id = '101327188'#максимальный
		
		url='https://itv.rt.ru/api/v1/channels.json?q%5Binclude_telecasts%5D=false&q%5Bsort%5D=sort_order&q%5Bsdp_id%5D='+sdp_id
		hp=GET(url)#.replace('\\"','')
		null=''
		true=True
		false=False
		try:total=int(eval(hp)['meta']['num_pages'])
		except: print "errrrr"
		LL=[]
		for n in range(total+1):
			#print n
			url='https://itv.rt.ru/api/v1/channels.json?q%5Binclude_telecasts%5D=false&q%5Bsort%5D=sort_order&q%5Bsdp_id%5D='+sdp_id+'&page='+str(n)#&q%5Bkeyword%5D=&q%5Bfrom_time%5D=2019-06-09
			hp=GET(url).replace('\\"','')
			jsn = eval(hp)
			L=jsn['list']
			for i in L:
				try:
					if i["mode"] == 'uncryptedPvr':
						title = i["name"]
						id=i["asset_id"]+":"+mfind(i["asset_url"], '/CH_', '/')
						try:img='https://itv.rt.ru/fe-ct/images/r100x100/'+i["poster"]
						except: img=''
						LL.append({'title':title, 'id':id})
				except:
					print i
		
		return LL
