#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, cookielib, urllib, urllib2, time
import settings
#-----------------------------------------

serv_id = '1'
siteUrl = 'peers.tv'
httpSiteUrl = 'http://' + siteUrl
sid_file = os.path.join(os.getcwd(), siteUrl+'.sid')
tmp_file = os.path.join(os.getcwd(),  'peers.m3u8')

cj = cookielib.FileCookieJar(sid_file) 
hr  = urllib2.HTTPCookieProcessor(cj) 
opener = urllib2.build_opener(hr) 
urllib2.install_opener(opener) 

def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return x
def rt(x):
	L=[('&raquo;','"'),('&laquo;','"'),('&#x2011;','-'),('&nbsp;',' '),('&#39;','’'),('&#39;','’'), ('&#145;','‘'), ('&#146;','’'), ('&#147;','“'), ('&#148;','”'), ('&#149;','•'), ('&#150;','–'), ('&#151;','—'), ('&#152;','?'), ('&#153;','™'), ('&#154;','s'), ('&#155;','›'), ('&#156;','?'), ('&#157;',''), ('&#158;','z'), ('&#159;','Y'), ('&#160;',''), ('&#161;','?'), ('&#162;','?'), ('&#163;','?'), ('&#164;','¤'), ('&#165;','?'), ('&#166;','¦'), ('&#167;','§'), ('&#168;','?'), ('&#169;','©'), ('&#170;','?'), ('&#171;','«'), ('&#172;','¬'), ('&#173;',''), ('&#174;','®'), ('&#175;','?'), ('&#176;','°'), ('&#177;','±'), ('&#178;','?'), ('&#179;','?'), ('&#180;','?'), ('&#181;','µ'), ('&#182;','¶'), ('&#183;','·'), ('&#184;','?'), ('&#185;','?'), ('&#186;','?'), ('&#187;','»'), ('&#188;','?'), ('&#189;','?'), ('&#190;','?'), ('&#191;','?'), ('&#192;','A'), ('&#193;','A'), ('&#194;','A'), ('&#195;','A'), ('&#196;','A'), ('&#197;','A'), ('&#198;','?'), ('&#199;','C'), ('&#200;','E'), ('&#201;','E'), ('&#202;','E'), ('&#203;','E'), ('&#204;','I'), ('&#205;','I'), ('&#206;','I'), ('&#207;','I'), ('&#208;','?'), ('&#209;','N'), ('&#210;','O'), ('&#211;','O'), ('&#212;','O'), ('&#213;','O'), ('&#214;','O'), ('&#215;','?'), ('&#216;','O'), ('&#217;','U'), ('&#218;','U'), ('&#219;','U'), ('&#220;','U'), ('&#221;','Y'), ('&#222;','?'), ('&#223;','?'), ('&#224;','a'), ('&#225;','a'), ('&#226;','a'), ('&#227;','a'), ('&#228;','a'), ('&#229;','a'), ('&#230;','?'), ('&#231;','c'), ('&#232;','e'), ('&#233;','e'), ('&#234;','e'), ('&#235;','e'), ('&#236;','i'), ('&#237;','i'), ('&#238;','i'), ('&#239;','i'), ('&#240;','?'), ('&#241;','n'), ('&#242;','o'), ('&#243;','o'), ('&#244;','o'), ('&#245;','o'), ('&#246;','o'), ('&#247;','?'), ('&#248;','o'), ('&#249;','u'), ('&#250;','u'), ('&#251;','u'), ('&#252;','u'), ('&#253;','y'), ('&#254;','?'), ('&#255;','y')]
	for i in L:
		x=x.replace(i[0], i[1])
	return x

def showMessage(heading, message, times = 3000):
	xbmc.executebuiltin('XBMC.Notification("%s", "%s", %s, "%s")'%(heading, message, times, icon))

def getURL(url, Referer = httpSiteUrl):
	urllib2.install_opener(urllib2.build_opener())
	req = urllib2.Request(url)
	#req.add_header('User-Agent', 'Opera/10.60 (X11; openSUSE 11.3/Linux i686; U; ru) Presto/2.6.30 Version/10.60')
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36 OPR/65.0.3467.48')
	req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3')#'text/html, application/xml, application/xhtml+xml, */*'
	req.add_header('Accept-Language', 'ru,en;q=0.9')
	#req.add_header('content-type', 'application/json; charset=UTF-8')
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

def save_aid(ns, d):
		fp=xbmc.translatePath(os.path.join(addon.getAddonInfo('path'), 'aid'+ns+'.py'))
		fl = open(fp, "w")
		fl.write('# -*- coding: utf-8 -*-\n')
		fl.write('n2id=')
		fl.write(repr(d))
		fl.close()

def save_tmp(L):
		fl = open(tmp_file, "w")
		for i in L:
			fl.write(i)
		fl.close()



class ARH:
	def __init__(self):
		pass

	def Streams(self, url):
		print url
		return ['HLS:'+url]
		'''
		if 'peers.tv' in url:
			hp=getURL(url)
			print hp
			L=hp.splitlines()
			link=''
			LL=[]
			for i in L:
				if '.m3u8' in i: 
					#print i
					link='HLS:'+i
					#print link
					LL.append(link)
			return LL
		'''

	def Archive(self, id, t):
		dt=time.strftime('%Y-%m-%d',t)
		url='https://peers.tv/ajax/program/'+id+'/'+dt+'/'
		#http://peers.tv/ajax/program/10338258/2019-06-04
		#print url
		http=getURL(url)
		js=eval(http.replace('\\/','/').replace('false','"false"').replace('true','"true"'))
		L=js['telecasts']
		LL=[]
		#print 'telecasts ok'
		for i in L:
			try:
				title=rt(i["title"])
				#print title
				try:image='http:'+i["image"]
				except:image=''
				try:subtitle=rt(i["subtitle"])
				except:subtitle=''
				tm=i["time"][11:16]
				files=i["files"]
				uri=files[0]['movie']
				print uri
				s_time  = time.mktime(time.strptime(i["time"][:16], '%m/%d/%Y %H:%M'))
				LL.append({'url':uri, 'title':title+" "+subtitle, 'time':tm, 's_time':s_time})
			except:
				pass
				#break
				#print i
		return LL

	def name2id(self):
			url2='http://api.peers.tv/tvguide/2/channels.json'#?t=126&channel='+ssn[:-1]
			#print url2
			json2=getURL(url2)
			jd=eval(json2.replace('\\/','/'))
			channels=jd['channels']
			d={}
			L=[]
			print 'channels: '+str(len(channels))
			for i in channels:
				title=i['title']
				channelId=str(i['channelId'])
				#print channelId
				if i['hasSchedule'] == 1:
					try:
						curl='http://peers.tv/ajax/program/'+channelId+'/'+time.strftime('%Y-%m-%d',time.localtime())+'/'
						#print curl
						tmp = getURL(curl)
						if 'm3u8' in tmp:
							L.append({'title':title, 'id':channelId})
							print channelId+' - '+title
					except:
						pass
						print 'error'
				if '26552780' in channelId: break
			print 'channels ok'
			#save_aid(serv_id, d)
			return L
