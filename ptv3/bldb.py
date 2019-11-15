# -*- coding: utf-8 -*-
import sys, os
import urllib, urllib2, cookielib
from ftplib import FTP
temp_dir = "d:\\"

sid_file = os.path.join(os.getcwd(), 'tmp.sid')

cj = cookielib.FileCookieJar(sid_file) 
hr  = urllib2.HTTPCookieProcessor(cj) 
opener = urllib2.build_opener(hr) 


try:
	import xbmcaddon
	addon = xbmcaddon.Addon(id='ptv3')
	temp_dir = addon.getAddonInfo('path')
except:
	temp_dir = os.getcwd()


def ru(x):return unicode(x,'utf8', 'ignore')

def getURL(url,Referer = 'http://emulations.ru/'):
	urllib2.install_opener(opener) 
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
		#sn=http[s:]
		e=http.find(es)
		i=http[s:e]
		L.append(i)
		http=http[e+2:]
	return L

def mfind(t,s,e):
	r=t[t.find(s)+len(s):]
	r2=r[:r.find(e)]
	return r2

def CRC32(buf):
		import binascii
		buf = (binascii.crc32(buf) & 0xFFFFFFFF)
		return str("%08X" % buf)

def dbid(id):
	return id[:2].replace('e','0').replace('E','0').replace('f','0').replace('F','0')

def save_inf(s):
	p = os.path.join(ru(temp_dir),"temp.txt")
	f = open(p, "w")
	f.write(s)
	f.close()
	return p

def upload(ftp, path, ftp_path):
	with open(path, 'rb') as fobj:
		ftp.storbinary('STOR ' + ftp_path, fobj, 1024)


def get_path(id):
	HOST=get_host()['HOST']
	s='/bl/'+dbid(id)+'.info'
	return s

def make_id(ftp, id):
	ret='/bl/'+dbid(id)+'.info'
	return ret

def verifid_id(ftp, id):
	try:size=ftp.size(get_path(id))
	except: size=0
	return size

def add(id, nfo):
	HUP=get_host()
	HOST=HUP['HOST']
	USER=HUP['USER']
	PASS=HUP['PASS']
	ftp = FTP(HOST)
	ftp.login(USER, PASS)
	print 'ADD DB: '+id
	dir=make_id(ftp, id)
	url='http://'+HOST+'/bl/'+dbid(id)+'.info'
	try:info=eval(getURL(url))
	except: info={}
	info[id]=nfo
	path = save_inf(repr(info))
	upload(ftp, path, dir)
	ftp.quit()

def get_info(id):
	if id == 'HOST': HOST = 'segaroms.my1.ru'
	else:            HOST=get_host()['HOST']
	url='http://'+HOST+'/bl/'+dbid(id)+'.info'
	try:info=eval(getURL(url))
	except: info={}
	if id in info.keys(): return info[id]
	else: return {}


def get_host():
	return get_info('HOST')
