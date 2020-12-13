# -*- coding: utf-8 -*-
import sys, os
import urllib, urllib2
from ftplib import FTP
temp_dir = "d:\\"

try:
	import xbmcaddon
	addon = xbmcaddon.Addon(id='ptv3')
	temp_dir = addon.getAddonInfo('path')
except:
	temp_dir = os.getcwd()


def ru(x):return unicode(x,'utf8', 'ignore')

def getURL(url,Referer = 'http://emulations.ru/'):
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
	s='/pom/'+id+'.info'
	return s

def make_id(ftp, id):
	ret='/pom/'+id+'.info'
	return ret

def verifid_id(ftp, id):
	try:size=ftp.size(get_path(id))
	except: size=0
	return size

def add(id, info):
	HUP=get_host()
	HOST=HUP['HOST']
	USER=HUP['USER']
	PASS=HUP['PASS']
	ftp = FTP(HOST)
	ftp.login(USER, PASS)
	print 'ADD DB: '+id
	dir=make_id(ftp, id)
	path = save_inf(repr(info))
	upload(ftp, path, dir)
	ftp.quit()

def get_info(id):
	if id == 'HOST': HOST = 'roms.my1.ru'
	else:            HOST=get_host()['HOST']
	url='http://'+HOST+'/pom/'+id+'.info'
	info=eval(getURL(url))
	return info

def get_host():
	return get_info('HOST')
