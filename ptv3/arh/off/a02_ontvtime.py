#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, cookielib, urllib, urllib2, time
#import settings
#-----------------------------------------

serv_id = '2'
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
	#print response.info()
	link=response.read()
	response.close()
	return link

def COOKE(url, Referer = ''):
	if Referer == '': Referer = url
	urllib2.install_opener(urllib2.build_opener())
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Opera/10.60 (X11; openSUSE 11.3/Linux i686; U; ru) Presto/2.6.30 Version/10.60')
	req.add_header('Accept', 'text/html, application/xml, application/xhtml+xml, */*')
	req.add_header('Accept-Language', 'ru,en;q=0.9')
	req.add_header('Referer', Referer)
	response = urllib2.urlopen(req)
	info = str(response.info())
	res  = response.read()
	response.close()
	gid = mfind(res, "var gid = '","'")
	c={'gid':gid}
	for i in info.splitlines():
		if 'Set-Cookie' in i:
			i=i.replace('Set-Cookie:', '')
			i=i.strip()
			if ';' in i:
				for j in i.split(';'):
					j=j.strip()
					c[j.split('=')[0]]=j.split('=')[1]
			else:
				c[i.split('=')[0]]=i.split('=')[1]
			
	return c


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

def utf(t):
	try:t=t.decode('windows-1251')
	except: pass
	try:t=t.encode('utf-8')
	except: pass
	return t


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
			#id = uid.split('_')[0]
			#record = uid.split('_')[1]
			#url = 'http://www.ontvtime.ru/index.php?option=com_content&task=view_record&id='+id+'&start_record='+record #2019-06-02-10-00
			print url
			c = COOKE(url)
			print c
			host = urllib2.unquote(c['tv'])
			gid  = c['gid']
			sid  = c['tv2']
			time1= c['tv1']
			stream = "a" + sid + "MseInit?time=" + time1 #playlist.m3u8?time=
			link = 'http://'+host+'/stream/' + gid + '/' + stream
			print link
			return [link, ]


	def Archive(self, id, t):
		#print t
		dt=time.strftime('%Y-%m-%d',t)
		url='http://www.ontvtime.ru/index.php?option=com_content&task=select_time&id='+id+'&start_record='+dt+'-06-00'
		print url
		hp=GET(url)
		L=mfindal(hp, '<div class="ann_time1">', 'javascript:show_more')
		LL=[]
		for i in L:
			i=i.replace('\n','').replace('\t','').replace('<font color=#FF3030>','')
			tm    = mfind(i, '">', '<').strip()
			uri   = 'http://www.ontvtime.ru'+mfind(i, 'href="', '"').replace('&amp;','&')
			
			if 'class=' not in uri:
				print uri 
				rid=mfind(i, 'start_record=', '"')
				s_time  = time.mktime(time.strptime(rid, '%Y-%m-%d-%H-%M'))
				title = utf(mfind(i, '<b>', '</b>'))
				
				LL.append({'url':uri, 'title':title, 'time':tm, 's_time':s_time})
		return LL
		
	#get_streams('4d1d6979385d28ebab8faae66cd97d72')


	def name2id(self):
		url = 'http://www.ontvtime.ru/records/index.php'
		hp=GET(url)
		#print '--1--'
		L1=mfindal(hp, '<div><a href="/records', "</td></tr>');")
		#print '--2--'
		L=[]
		for i in L1:
			try:
				title = utf(mfind(i, '">', ','))
				cid = mfind(i, '/records/', '.html')
				url2 = 'http://www.ontvtime.ru/records/'+cid+'.html'
				t=GET(url2)
				id = mfind(t, 'select_time&amp;id=','&')
				L.append({'title':title, 'id':id})
				print title
			except:
				print i
		#save_aid(serv_id, d)
		return L

#s=ARH()
#s.name2id()