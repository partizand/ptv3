#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, cookielib, urllib, urllib2, time
#-----------------------------------------

serv_id = '1'
siteUrl = 'zabava-htlive.cdn.ngenix.net'
httpSiteUrl = 'http://' + siteUrl
#sid_file = os.path.join(os.getcwd(), siteUrl+'.sid')

#cj = cookielib.FileCookieJar(sid_file) 
#hr  = urllib2.HTTPCookieProcessor(cj) 
#opener = urllib2.build_opener(hr) 
#urllib2.install_opener(opener) 

def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return xbmc.translatePath(x)


def unmark(nm):
	for i in range (0,20):
		nm=nm.replace(" #"+str(i),"")
	return nm

def lower(t):
	RUS={"А":"а", "Б":"б", "В":"в", "Г":"г", "Д":"д", "Е":"е", "Ё":"ё", "Ж":"ж", "З":"з", "И":"и", "Й":"й", "К":"к", "Л":"л", "М":"м", "Н":"н", "О":"о", "П":"п", "Р":"р", "С":"с", "Т":"т", "У":"у", "Ф":"ф", "Х":"х", "Ц":"ц", "Ч":"ч", "Ш":"ш", "Щ":"щ", "Ъ":"ъ", "Ы":"ы", "Ь":"ь", "Э":"э", "Ю":"ю", "Я":"я"}
	for i in range (65,90):
		t=t.replace(chr(i),chr(i+32))
	for i in RUS.keys():
		t=t.replace(i,RUS[i])
	return t


def getURL(url, Referer = httpSiteUrl):
	urllib2.install_opener(urllib2.build_opener()) 
	req = urllib2.Request(url)
	#req.add_header('User-Agent', 'Opera/10.60 (X11; openSUSE 11.3/Linux i686; U; ru) Presto/2.6.30 Version/10.60')
	req.add_header('User-Agent', 'SmartSDK')
	req.add_header('Accept', 'text/html, application/xml, application/xhtml+xml, */*')
	req.add_header('Accept-Language', 'ru,en;q=0.9')
	#req.add_header('Referer', Referer)
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


def save_channels(ns, L):
		fp=xbmc.translatePath(os.path.join(addon.getAddonInfo('path'), 'Channels'+ns+'.py'))
		fl = open(fp, "w")
		fl.write('# -*- coding: utf-8 -*-\n')
		fl.write('Channels=[\n')
		for i in L:
			fl.write(repr(i)+',\n')
		fl.write(']\n')
		fl.close()


class PZL:
	def __init__(self):
		pass

	def Streams(self, url):
			url=url[7:]
			print url
			hp=getURL(url+'?version=2&hd')
			#print hp
			L=hp.splitlines()
			link=''
			LL=[]
			for i in L:
				if '#EXT' not in i and '.m3u8' in i: LL.append(i)
			#LL.reverse()
			return LL

	def Canals(self):
		sdp_id = '98771354'#КиноViP OTT
		sdp_id = '81204872'#стартовый
		sdp_id = '101327188'#максимальный
		
		url='https://itv.rt.ru/api/v1/channels.json?q%5Binclude_telecasts%5D=false&q%5Bsort%5D=sort_order&q%5Bsdp_id%5D='+sdp_id
		hp=getURL(url).replace('\\"','')
		null=''
		true=True
		false=False
		try:total=int(eval(hp)['meta']['num_pages'])
		except: print "errrrr"
		LL=[]
		for n in range(total+1):
			print n
			url='https://itv.rt.ru/api/v1/channels.json?q%5Binclude_telecasts%5D=false&q%5Bsort%5D=sort_order&q%5Bsdp_id%5D='+sdp_id+'&page='+str(n)#&q%5Bkeyword%5D=&q%5Bfrom_time%5D=2019-06-09
			hp=getURL(url).replace('\\"','')
			jsn = eval(hp)
			L=jsn['list']
			for i in L:
				try:
					if i["mode"] == 'uncryptedPvr':
						title = i["name"]
						url='zabava:'+i["asset_url"]
						#print url
						try:img='https://itv.rt.ru/fe-ct/images/r100x100/'+i["poster"]
						except: img=''
						LL.append({'url':url, 'img':img, 'title':title, 'group':""})
				except:
					print i

		#if LL!=[]: save_channels(serv_id, LL)
		#else: showMessage('yandex.ru', 'Не удалось загрузить каналы', times = 3000)

		return LL

