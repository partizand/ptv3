#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, cookielib, urllib, urllib2, time
#-----------------------------------------
prov = 'corbina'
serv_id = '36'
siteUrl = 'proxytv.ru'
httpSiteUrl = 'http://' + siteUrl
sid_file = os.path.join(os.getcwd(), siteUrl+'.sid')

cj = cookielib.FileCookieJar(sid_file) 
hr  = urllib2.HTTPCookieProcessor(cj) 
opener = urllib2.build_opener(hr) 
urllib2.install_opener(opener) 


def fs(s):return s.decode('windows-1251').encode('utf-8')
def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return xbmc.translatePath(x)

def CRC32(buf):
		import binascii
		buf = (binascii.crc32(buf) & 0xFFFFFFFF)
		return str("%08X" % buf)

def showMessage(heading, message, times = 3000):
	xbmc.executebuiltin('XBMC.Notification("%s", "%s", %s, "%s")'%(heading, message, times, icon))

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


def POST(target, post=None, referer='http://proxytv.ru/index.php/poisk.html'):
	try:
		req = urllib2.Request(url = target, data = post)
		req.add_header('Referer', referer)
		req.add_header('X-Requested-With', 'XMLHttpRequest')
		resp = urllib2.urlopen(req)
		http = resp.read()
		resp.close()
		return http
	except Exception, e:
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

def mfind(t,s,e):
	r=t[t.find(s)+len(s):]
	r2=r[:r.find(e)]
	return r2

def lower(t):
	RUS={"А":"а", "Б":"б", "В":"в", "Г":"г", "Д":"д", "Е":"е", "Ё":"ё", "Ж":"ж", "З":"з", "И":"и", "Й":"й", "К":"к", "Л":"л", "М":"м", "Н":"н", "О":"о", "П":"п", "Р":"р", "С":"с", "Т":"т", "У":"у", "Ф":"ф", "Х":"х", "Ц":"ц", "Ч":"ч", "Ш":"ш", "Щ":"щ", "Ъ":"ъ", "Ы":"ы", "Ь":"ь", "Э":"э", "Ю":"ю", "Я":"я"}
	for i in range (65,90):
		t=t.replace(chr(i),chr(i+32))
	for i in RUS.keys():
		t=t.replace(i,RUS[i])
	return t

def upper(t):
	RUS={"А":"а", "Б":"б", "В":"в", "Г":"г", "Д":"д", "Е":"е", "Ё":"ё", "Ж":"ж", "З":"з", "И":"и", "Й":"й", "К":"к", "Л":"л", "М":"м", "Н":"н", "О":"о", "П":"п", "Р":"р", "С":"с", "Т":"т", "У":"у", "Ф":"ф", "Х":"х", "Ц":"ц", "Ч":"ч", "Ш":"ш", "Щ":"щ", "Ъ":"ъ", "Ы":"ы", "Ь":"ь", "Э":"э", "Ю":"ю", "Я":"я"}
	for i in RUS.keys():
		t=t.replace(RUS[i],i)
	for i in range (65,90):
		t=t.replace(chr(i+32),chr(i))
	return t

def get_id(name):
	import xid
	xmlid=xid.xmlid
	name=lower(name).replace(" (+1)","").replace(" (+2)","").replace(" (+3)","").replace(" (+4)","").replace(" (+5)","").replace(" (+6)","").replace(" (+7)","").replace(" (резерв)","").strip()
	try:
		id=xmlid[name].replace("ttv","")
	except: 
		print name
		id=''
	return id

def save_channels(n, L):
		ns=str(n)
		fp=xbmc.translatePath(os.path.join(addon.getAddonInfo('path'), 'Channels'+ns+'.py'))
		fl = open(fp, "w")
		fl.write('# -*- coding: utf-8 -*-\n')
		fl.write('Channels=[\n')
		for i in L:
			fl.write(repr(i)+',\n')
		fl.write(']\n')
		fl.write('tm='+str(time.time())+'\n')
		#fl.write('set='+get_set()+'\n')
		fl.close()

def get_cnl(s):
		print s
		fp=xbmc.translatePath(os.path.join(addon.getAddonInfo('path'), 'Channels'+s+'.py'))
		fl = open(fp, "r")
		t=fl.read()
		fl.close()
		L=eval(mfind(t,'Channels=',']')+']')
		return L

def uptm(s):
	try:
		fp=xbmc.translatePath(os.path.join(addon.getAddonInfo('path'), 'Channels'+s+'.py'))
		fl = open(fp, "r")
		t=fl.read()
		fl.close()
		tm=eval(mfind(t,'tm=','.')+'.00')
		if time.time()-tm > 7200: return True
		else:                     return False
	except:
		return False


def get_rpov():
	target='http://proxytv.ru/iptv/php/srch.php'
	post='udpxyaddr=plist'
	p = POST(target, post)
	L=[]
	for i in p.splitlines():
		if '<img alt' in i:
			prov = mfind(i,'плейлист "','"')
			print prov
			L.append(prov)
	return L



class PZL:
	def __init__(self):
		pass

	def Streams(self, url):
		print url
		#if uptm(serv_id): self.Canals()
		link=url.replace(prov+':','')
		print link
		return [link,]

	def Canals(self, ul=''):
		target='http://proxytv.ru/iptv/php/srch.php'
		post='udpxyaddr=pl%3A+'+prov
		p = POST(target, post)
		p = p.replace('#EXTINF','\n#EXTINF')
		L=[]
		for i in p.splitlines():
			if '#EXTINF' in i:
				title = mfind(i, '<b>', '<')
				cid = mfind(i, '<br>', '<')
				url=prov+":"+cid
				L.append({'url':url, 'img':'', 'title':title.strip(), 'group':''})
		
		return L


