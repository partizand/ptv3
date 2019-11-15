#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, cookielib, urllib, urllib2, time
import settings
#-----------------------------------------

serv_id = '2'
siteUrl = 'www.lapti.tv'
httpSiteUrl = 'http://' + siteUrl
sid_file = os.path.join(os.getcwd(), siteUrl+'.sid')

cj = cookielib.FileCookieJar(sid_file) 
hr  = urllib2.HTTPCookieProcessor(cj) 
opener = urllib2.build_opener(hr) 
urllib2.install_opener(opener) 

def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return xbmc.translatePath(x)

def showMessage(heading, message, times = 3000):
	xbmc.executebuiltin('XBMC.Notification("%s", "%s", %s, "%s")'%(heading, message, times, icon))

def unmark(nm):
	for i in range (0,20):
		nm=nm.replace(" #"+str(i),"")
	return nm

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

def testURL(url):
	try:
		import requests
		from datetime import datetime
		s = requests.session()
		d = datetime.now()
		try:
			r=s.get(url, timeout=(1, 0.8))#0000
			print '=-=-= requests -=-=-=- '
			print r
			if r=='<Response [404]>': return '<Response [404]>'
			else: return r
		except requests.exceptions.ReadTimeout:
				return '<Response [404]>'#int(str(datetime.now() - d)[-6:-3])
		except requests.exceptions.ConnectTimeout:
				return '<Response [404]>'
	except:
		return '<Response [404]>'

def POST(target, post=None, referer='https://jetune.fm'):
	#print target
	try:
		req = urllib2.Request(url = target, data = post)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36 OPR/55.0.2994.61')
		req.add_header('Accept', '*/*')
		req.add_header('Accept-Encoding', 'gzip, deflate')
		req.add_header('Referer', referer)
		req.add_header('X-Requested-With', 'XMLHttpRequest')
		resp = urllib2.urlopen(req)
		http = resp.read()
		resp.close()
		return http
	except Exception, e:
		print 'err'
		print e
		return ''


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

def getURL2(url, data = None, cookie = None, save_cookie = False, referrer = None):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0')
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    req.add_header('Accept-Language', 'en-US,en;q=0.5')
    
    if cookie: req.add_header('Cookie', cookie)
    if referrer: req.add_header('Referer', referrer)
    if data: 
        response = urllib2.urlopen(req, data, timeout=30)
    else:
        response = urllib2.urlopen(req, timeout=30)
    link=response.read()
    if save_cookie:
        setcookie = response.info().get('Set-Cookie', None)
        #print "Set-Cookie: %s" % repr(setcookie)
        #print response.info()['set-cookie']
        if setcookie:
            try:
              setcookie = response.info()['set-cookie']
            except:
              pass
            link = link + '<cookie>' + setcookie + '</cookie>'
    
    response.close()
    #print response.info()
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

def rt(x):#('&#39;','’'), ('&#145;','‘')
	L=[('&quot;','"'),('&amp;',"&"),('&#133;','…'),('&#38;','&'),('&#34;','"'), ('&#39;','"'), ('&#145;','"'), ('&#146;','"'), ('&#147;','“'), ('&#148;','”'), ('&#149;','•'), ('&#150;','–'), ('&#151;','—'), ('&#152;','?'), ('&#153;','™'), ('&#154;','s'), ('&#155;','›'), ('&#156;','?'), ('&#157;',''), ('&#158;','z'), ('&#159;','Y'), ('&#160;',''), ('&#161;','?'), ('&#162;','?'), ('&#163;','?'), ('&#164;','¤'), ('&#165;','?'), ('&#166;','¦'), ('&#167;','§'), ('&#168;','?'), ('&#169;','©'), ('&#170;','?'), ('&#171;','«'), ('&#172;','¬'), ('&#173;',''), ('&#174;','®'), ('&#175;','?'), ('&#176;','°'), ('&#177;','±'), ('&#178;','?'), ('&#179;','?'), ('&#180;','?'), ('&#181;','µ'), ('&#182;','¶'), ('&#183;','·'), ('&#184;','?'), ('&#185;','?'), ('&#186;','?'), ('&#187;','»'), ('&#188;','?'), ('&#189;','?'), ('&#190;','?'), ('&#191;','?'), ('&#192;','A'), ('&#193;','A'), ('&#194;','A'), ('&#195;','A'), ('&#196;','A'), ('&#197;','A'), ('&#198;','?'), ('&#199;','C'), ('&#200;','E'), ('&#201;','E'), ('&#202;','E'), ('&#203;','E'), ('&#204;','I'), ('&#205;','I'), ('&#206;','I'), ('&#207;','I'), ('&#208;','?'), ('&#209;','N'), ('&#210;','O'), ('&#211;','O'), ('&#212;','O'), ('&#213;','O'), ('&#214;','O'), ('&#215;','?'), ('&#216;','O'), ('&#217;','U'), ('&#218;','U'), ('&#219;','U'), ('&#220;','U'), ('&#221;','Y'), ('&#222;','?'), ('&#223;','?'), ('&#224;','a'), ('&#225;','a'), ('&#226;','a'), ('&#227;','a'), ('&#228;','a'), ('&#229;','a'), ('&#230;','?'), ('&#231;','c'), ('&#232;','e'), ('&#233;','e'), ('&#234;','e'), ('&#235;','e'), ('&#236;','i'), ('&#237;','i'), ('&#238;','i'), ('&#239;','i'), ('&#240;','?'), ('&#241;','n'), ('&#242;','o'), ('&#243;','o'), ('&#244;','o'), ('&#245;','o'), ('&#246;','o'), ('&#247;','?'), ('&#248;','o'), ('&#249;','u'), ('&#250;','u'), ('&#251;','u'), ('&#252;','u'), ('&#253;','y'), ('&#254;','?'), ('&#255;','y'), ('&laquo;','"'), ('&raquo;','"'), ('&nbsp;',' ')]
	for i in L:
		x=x.replace(i[0], i[1])
	return x


def save_aid(ns, d):
		fp=xbmc.translatePath(os.path.join(addon.getAddonInfo('path'), 'aid'+ns+'.py'))
		fl = open(fp, "w")
		fl.write('# -*- coding: utf-8 -*-\n')
		fl.write('n2id=')
		fl.write(repr(d))
		fl.close()

def get_tv(url):
		print url
		i=getURL(url)
		ss="value='src="
		es="&ar="
		tvpl = i[i.find(ss)+11:i.find(es)]
		print tvpl
		i=getURL(tvpl)
		tv = i[i.find('http://'):i.find('&e=')]+'&e=99999999999999999'
		print tv
		return tv

class ARH:
	def __init__(self):
		pass
		#self.name2id()

	def Streams(self, id):
#		try:
			#print '=============lapti================='
			f   = mfind(id,'lapti:','|')
			cid = id[id.rfind('|')+1:]
			#print f
			#print cid
			file = f.replace('/','%2F')+'(1200).m3u8'
			false=False
			true=True
			link=eval(POST('http://'+cid+'.lapti.tv/src/getserver.php', 'server_type=archive&days=0&file='+file))['player'].replace('\\/','/')
			#print link
			return [link]

	def Archive(self, id, t):
		idl=eval(id)
		id1=idl[0]
		id2=idl[1]
		id3=idl[2]
		id4=idl[3]
		url='http://'+id1+'.lapti.tv/src/ajax.php'
		dt=time.strftime('%Y-%m-%d',t)#.replace('-0','-')[1:]
		#url='http://www.gamak.tv/'+id+'/'+dt#+'/00:00/'
		post='nowdate='+dt+'&chanel='+id2+'&sli=3&filter='#urllib.quote_plus()
		
		#print url
		#print post
		http=POST(url, post)
		#print http
		http=mfind(http, 'programm js-selected-date', '</div>')
		#print http
		ss='<span  id="prog'
		es='<span class="clear">'
		L=mfindal(http,ss,es)
		LL=[]
		for i in L:
			try:
				#print i
				tm=mfind(i,'00">', '<')
				print tm
				ttl=mfind(i,'class="name">', '<')
				print ttl
				dts=dt.replace('-','/')
				tms=tm.replace(':','-')
				uri='lapti:'+id4+'/'+dts+'/'+tms+'|'+id1
				#print uri
				
				if tm!='': LL.append({'url':uri, 'title':ttl, 'time':tm})
			except: pass
		return LL

	def name2id(self):
		url='http://www.lapti.tv/header2.html'
		http=getURL(url)
		L=http.splitlines()
		d={}
		L=[]
		for i in L:
			if '<li class="active">' in i:
				print i
				nmc = mfind(i,'title = "','"')
				
				idc1 = mfind(i,'href="http://','.')
				idc3 = mfind(i,'<a class="','"')
				irl='http://'+idc1+'.lapti.tv'
				tp=getURL(irl)
				idc2 = mfind(tp,'id="sys" value="','"')
				idc4 = mfind(tp,'id="stream" value="','"')
				
				idc='["'+idc1+'","'+idc2+'","'+idc3+'","'+idc4+'"]'
				print nmc
				print idc
				d[nmc] = idc
				L.append({'title':nmc, 'id':idc})
		#save_aid(serv_id, d)
		return L