#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, cookielib, urllib, urllib2, time
#import settings
#-----------------------------------------

serv_id = '5'
siteUrl = 'strm.yandex.ru'
httpSiteUrl = 'http://' + siteUrl
sid_file = os.path.join(os.getcwd(), siteUrl+'.sid')

cj = cookielib.FileCookieJar(sid_file) 
hr  = urllib2.HTTPCookieProcessor(cj) 
opener = urllib2.build_opener(hr) 
urllib2.install_opener(opener) 

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

def GET(url, Referer = 'https://m.knigavuhe.ru/'):
	urllib2.install_opener(urllib2.build_opener())
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Opera/10.60 (X11; openSUSE 11.3/Linux i686; U; ru) Presto/2.6.30 Version/10.60')
	req.add_header('Accept', 'text/html, application/xml, application/xhtml+xml, */*')
	req.add_header('Accept-Language', 'ru,en;q=0.9')
	req.add_header('Referer', Referer)
	req.add_header('x-requested-with', 'XMLHttpRequest')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

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

def mfindal(http, ss, es):
	L=[]
	while http.find(es)>0:
		s=http.find(ss)
		e=http.find(es)
		i=http[s:e]
		L.append(i)
		http=http[e+2:]
	return L


def save_aid(ns, d):
		fp=xbmc.translatePath(os.path.join(addon.getAddonInfo('path'), 'aid'+ns+'.py'))
		fl = open(fp, "w")
		fl.write('# -*- coding: utf-8 -*-\n')
		fl.write('n2id=')
		fl.write(repr(d))
		fl.close()

class ARH:
	def __init__(self):
		pass

	def Streams(self, url):
		print url
		hp=GET(url)#+'&start=1552610400&end=1552616100'
		#print hp
		L=hp.splitlines()
		LL=[]
		Ltmp=[]
		for i in L:
			if '#' not in i:
				if 'redundant' in i:tmp=i[:i.rfind('&')]
				else: 				tmp=i
				if tmp not in Ltmp:
					LL.append('https://strm.yandex.ru'+i)
					Ltmp.append(tmp)
					print i
		LL.reverse()
		return LL

	#Streams ("https://strm.yandex.ru/kal/zvezda_supres/zvezda_supres0.m3u8?end=1552616100&from=efir&   imp_id=36&partner_id=278914&start=1552610400&target_ref=https%3A//yastatic.net&uuid=47db04cf4378f160896388887b60a1e1&video_category_id=1011")
	#Streams ("https://strm.yandex.ru/kal/zvezda_supres/zvezda_supres0.m3u8?from=unknown&imp_id=40&partner_id=278914")

	def Archive(self, id, t):
		print t
		dt=t[3]*60*60+t[4]*60
		
		if t[2] != time.localtime(time.time())[2]:
			st=str(int(time.mktime(t))+86400+3600-dt)
		else:
			st=str(int(time.mktime(t)))
		
		et=str(int(time.mktime(t))-86400-14400+dt)
		print st
		print et
		#end_date__from=1552615200&start_date__to=1552701300
		url='https://frontend.vh.yandex.ru/v22/episodes.json?end_date__from='+et+'&start_date__to='+st+'&parent_id='+id
		#print url
		hp=GET(url)
		true=True
		false=False
		json=eval(hp)
		LL=[]
		for i in json['set']:
			tm      = i['computed_title'][-5:]
			try:program = i['program_title']
			except: program = ''
			title   = i['title']
			if title!=program: title=program+' '+ title
			uri     = i['content_url']
			try:s_time  = i['start_time']
			except: s_time  = 0
			LL.append({'url':uri, 'title':title, 'time':tm, 's_time':s_time})
		return LL
		
	#get_streams('4d1d6979385d28ebab8faae66cd97d72')


	def name2id(self):
		url = 'https://www.yandex.ru/portal/tvstream_json/channels?locale=ru&from=efir'
		hp=GET(url)
		null=''
		true=True
		false=False
		#print '--1--'
		L1=eval(hp)['set']
		#print '--2--'
		d={}
		L=[]
		for i in L1:
			try:
				status = i['status']
				category = i['channel_category']
				try:    plus = repr(i['ya_plus'])
				except: plus = ''
				try:    hidden = int(i['hidden'])
				except: hidden = 0
				try:    cachup = int(i['has_cachup'])
				except: cachup = 0
				#if 'has_cachup' in status and 'yandex' not in category:
				if cachup!=0 and hidden==0 and 'yandex' not in category and 'PREMIUM' not in plus:
					title = i["title"]
					url=i["content_url"]
					#id = mfind(url, '&uuid=', '&')
					id = i["content_id"]
					L.append({'title':title, 'id':id})
					print title
			except:
				print i
		#save_aid(serv_id, d)
		return L
